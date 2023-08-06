#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-App.
# @File         : ann_search
# @Time         : 2020/11/5 4:04 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import requests
from functools import lru_cache
from iapp import App

app_ = App()
app = app_.app


@lru_cache(256)
def get_bert_vector(text):
    return requests.get(f"http://tql.algo.browser.miui.srv/bert/simbert?texts=['{text}']").json()['vectors']


def xindao_search(**kwargs):
    text = kwargs.get('text', '')
    topk = kwargs.get('topk', 5)
    return_ids = kwargs.get('return_ids', 0)

    query_embedding = get_bert_vector(text)
    body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "vector": {
                            "embedding": {
                                "topk": topk,
                                "values": query_embedding,
                                "metric_type": "IP",
                                "params": {
                                    "nprobe": 1
                                }
                            }
                        }
                    }
                ]
            }
        },
        "fields": []
    }

    ann_url = f"http://xindao-ann-cl33103.c3.ingress.mice.cc.d.xiaomi.net/collections/demo/entities"

    r = requests.get(ann_url, json=body).json()
    if return_ids:
        return [i['id'] for i in r['data']['result'][0]]
    else:
        return r


app_.add_route('/xindao_search', xindao_search)

if __name__ == '__main__':
    app_.run(f"{app_.app_file_name(__file__)}", port=9955, debug=True, reload=True)
