"""
导入另一个模型的相同部分到新的模型
模型导入参数时，如果两个模型结构不一致，
则直接导入参数会报错。用下面方法可以把另一个模型的相同的部分导入到新的模型中。
"""


# model_new代表新的模型
# model_saved代表其他模型，比如用torch.load导入的已保存的模型
def load_model_dict_from_old_model(model_new, model_saved):
    model_new_dict = model_new.state_dict()
    model_common_dict = {k: v for k, v in model_saved.items() if k in model_new_dict.keys()}
    model_new_dict.update(model_common_dict)
    model_new.load_state_dict(model_new_dict)
