"""
实现的是: 构建词典 实现把句子  和  数字  可以相互转化
"""

import pickle
from dataset import get_dataloader


class WordSequence:
    UNK_TAG = "UNK"  # 表示未知字符
    PAD_TAG = "PAD"  # 填充符

    UNK = 0
    PAD = 1

    def __init__(self):
        self.dict = {self.UNK_TAG: self.UNK, self.PAD_TAG: self.PAD}
        self.count = {}  # 统计词频

    def fit(self, sentence):
        """
        把单个句子保存到dict中
        :param sentence: [word1, word2, word3......]
        :return:
        """
        for word in sentence:
            self.count[word] = self.count.get(word,
                                              0) + 1  # 取 value = word  if  value exist  value +1    else  value = 1

    def build_vocab(self, min_len=0, max_len=None, max_features=None):
        """
        生成词典
        :param min_len: 最小出现的次数
        :param max_len: 最大的次数
        :param max_features: 一共保留多少个词语
        :return:
        """
        # 方法一 （复杂 慢）
        # 删除count中小于min的word     牢记下面这种遍历方法
        if min_len is not None:
            self.count = {word: value for word, value in self.count.items() if value > min_len}
        # 删除count中大于max的word
        if max_len is not None:
            self.count = {word: value for word, value in self.count.items() if value < max_len}
        # 限制保留的词语数
        if max_features is not None:
            # 要排序
            temp = sorted(self.count.items(), key=lambda x: x[-1], reverse=True)[
                   :max_features]  # count.items() : [(key:value),....]
            # 取前max_features个
            self.count = dict(temp)  # 存的是词频
        for word in self.count:  # self.count :  {hello: 2}  hello  存2次   word 是count的key值
            # 若第一个 为 {hello: 2}  则 word 为 hello  dict[hello] = 2  代表它是第二个 hello  是词典中第二个词
            self.dict[word] = len(self.dict)  # 第一遍历 dict的长度为2  只存了原始的 PAD 和 UNK

        # 得到一个反转的dict字典
        self.inverse_dict = dict(zip(self.dict.values(), self.dict.keys()))

    def transform(self, sentence, max_len=None):
        """
        把句子转化为  序列(list)
        :param sentence: [word1, word2, word3......]
        :param max_len:  int ，对句子进行填充或裁剪  为什么要设置最大长度
        :return:
        """
        if max_len is not None:
            if len(sentence) > max_len:
                sentence = sentence[:max_len]
            else:
                sentence = sentence + [self.PAD_TAG] * (max_len - len(sentence))  # 填充PAD

        # 这个为 平常的写法
        # for word in sentence:
        #     # 意思为 如果词在词典中取不到 则返回 unk 所以不用dict[word]
        #     self.dict.get(word, self.UNK)
        return [self.dict.get(word, self.UNK) for word in sentence]

    def inverse_transform(self, indices):
        """
        把序列转化为  句子list
        :param indices: [1,2,3,4,......]
        :return:
        """
        return [self.inverse_dict.get(i, self.UNK_TAG) for i in indices]  # 这里为什么没有 get(i,self.UNK_TAG)

    def __len__(self):
        return len(self.dict)

    def sava_ws_model(self, ws_model_path="./models/ws.pkl"):
        pickle.dump(self, open(ws_model_path, "wb"))

    def train_save_vocab_model(self):
        dl_train = get_dataloader(train=True)  # 训练的所有句子
        dl_test = get_dataloader(train=False)  # 测试的所有句子
        # tqdm(dl_train, total=len(dl_train))
        for reviews, labels in dl_train:
            for label in labels:
                self.fit(label)
            for sentence in reviews:
                self.fit(sentence)

        for reviews, labels in dl_test:
            for label in labels:
                self.fit(label)
            for sentence in reviews:
                self.fit(sentence)
        self.build_vocab()
        print("词典长度为:", len(self))
        self.sava_ws_model(ws_model_path="models/ws.pkl")



