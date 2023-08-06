import torch
import torch.nn as nn
import torch.nn.functional as F

"""
Attention 机制适合于seq2seq模型  即 具有 encoder   decoder
"""


class Attention(nn.Module):
    def __init__(self, config, method="dot"):
        super(Attention, self).__init__()
        assert method in ["dot", "general", "concat"], "method error"
        self.method = method

        if self.method == "general":
            self.Wa = nn.Linear(config.encoder_hidden_size, config.decoder_hidden_size, bias=False)

        elif self.method == "concat":
            self.Wa = nn.Linear(config.encoder_hidden_size + config.decoder_hidden_size, config.decoder_hidden_size,
                                bias=False)

            self.Va = nn.Linear(config.decoder_hidden_size, 1, bias=False)

    def forward(self, hidden_state, encoder_output):
        """

        Parameters
        ----------
        hidden_state [ num_layer, batch_size, decoder_hidden_size ]
        encoder_output [ batch_size, seq_len, encoder_hidden_size ]

        Returns [ batch_size, seq_len ]
        -------

        """
        # TODO ----->dot
        if self.method == "dot":
            hidden_state = hidden_state[-1].unsqueeze(dim=-1)  # [ batch_size, decoder_hidden_size, 1 ]
            att = torch.bmm(encoder_output, hidden_state).squeeze(dim=-1)  # [ batch_size, seq_len ]
            att_weight = F.softmax(att, dim=-1)  # [ batch_size, seq_len ]
        # TODO ----->general
        elif self.method == "general":
            encoder_output = self.Wa(encoder_output)  # [ batch_size, seq_len, decoder_hidden_size ]
            hidden_state = hidden_state[-1].unsqueeze(dim=-1)  # [ batch_size, decoder_hidden_size, 1 ]
            att = torch.bmm(encoder_output, hidden_state).squeeze(dim=-1)  # [ batch_size, seq_len ]
            att_weight = F.softmax(att, dim=-1)  # [ batch_size, seq_len ]
        # TODO ----->concat
        elif self.method == "concat":
            hidden_state = hidden_state[-1]  # [ batch_size, decoder_hidden_size ]
            hidden_state = hidden_state.repeat(1, encoder_output.size(1),
                                               1)  # [ batch_size, seq_len, decoder_hidden_size ]
            cat_ed = torch.cat([hidden_state, encoder_output], dim=-1)
            att = self.Va(F.tanh(self.Wa(cat_ed))).squeeze(dim=-1)  # [ batch_size, seq_len ]
            att_weight = F.softmax(att, dim=-1)  # [ batch_size, seq_len ]

        return att_weight
