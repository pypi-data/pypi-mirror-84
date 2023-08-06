#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : simbert
# @Time         : 2020-04-08 20:22
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :


import os
import numpy as np
import keras

from bert4keras.models import build_transformer_model
from bert4keras.tokenizers import Tokenizer
from bert4keras.snippets import sequence_padding

from functools import lru_cache
from loguru import logger

from appzoo import App
from appzoo.utils import normalize, get_zk_config

# BERT_DIR
BERT_DIR = './chinese_simbert_L-12_H-768_A-12'

if not os.path.exists(BERT_DIR):
    cfg = get_zk_config("mipush.ann.cfg")["mipush/ann/cfg"]
    url = f"{cfg['fds_url']}/data/bert/chinese_simbert_L-12_H-768_A-12.zip"
    os.system(f"wget {url} && unzip chinese_simbert_L-12_H-768_A-12.zip")

config_path = f'{BERT_DIR}/bert_config.json'
checkpoint_path = f'{BERT_DIR}/bert_model.ckpt'
dict_path = f'{BERT_DIR}/vocab.txt'

# 建立分词器
tokenizer = Tokenizer(dict_path, do_lower_case=True)

# 建立加载模型
bert = build_transformer_model(
    config_path,
    checkpoint_path,
    with_pool='linear',
    application='unilm',
    return_keras_model=False  # True: bert.predict([np.array([token_ids]), np.array([segment_ids])])
)

encoder = keras.models.Model(bert.model.inputs, bert.model.outputs[0])


# seq2seq = keras.models.Model(bert.model.inputs, bert.model.outputs[1])

@lru_cache(10240)
def text2vec(text):
    token_ids, segment_ids = tokenizer.encode(text)
    vec = encoder.predict([sequence_padding([token_ids]), sequence_padding([segment_ids])])
    vec = normalize(vec)

    return vec


def cache_mongodb(**kwargs):  # todo: Mongo
    pass


def get_one_vec(**kwargs):
    text = kwargs.get('text', '默认')
    is_lite = kwargs.get('is_lite', 0)

    vecs = text2vec(text)
    if is_lite:
        vecs = vecs[:, range(0, 768, 3)] if is_lite else vecs

    return vecs.tolist()


def get_batch_vec(**kwargs):
    texts = kwargs.get('texts', ['默认'])
    is_lite = kwargs.get('is_lite', 0)
    vecs = np.row_stack(list(map(text2vec, texts)))

    if is_lite:
        vecs = vecs[:, range(0, 768, 3)] if is_lite else vecs
    return normalize(vecs).tolist()


logger.info(f"初始化模型: {text2vec('语言模型')}")  # 不初始化会报线程错误

if __name__ == '__main__':
    app = App(verbose=os.environ.get('verbose'))

    app.add_route('/simbert', get_one_vec)
    app.add_route('/simbert', get_batch_vec, 'POST')

    app.run(access_log=False)
