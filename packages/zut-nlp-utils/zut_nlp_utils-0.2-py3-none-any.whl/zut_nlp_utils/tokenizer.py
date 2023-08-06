import re
import jieba
import logging

jieba.setLogLevel(logging.INFO)  # 禁止 jieba 运行时的 INFO提示


def tokenizer(text):
    """
    定义TEXT的tokenize规则
    """

    # 去掉不在(所有中文、大小写字母、数字)中的非法字符
    regex = re.compile(r'[^\u4e00-\u9fa5A-Za-z0-9]')
    text = regex.sub(' ', text)

    # 使用jieba分词
    return [word for word in jieba.cut(text) if word.strip()]
