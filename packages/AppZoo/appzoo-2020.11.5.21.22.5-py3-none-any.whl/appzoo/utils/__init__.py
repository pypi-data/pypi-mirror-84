#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-App.
# @File         : __init__.py
# @Time         : 2019-08-15 13:17
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import os
import requests
# from .Templates import Templates

get_module_path = lambda path, file=__file__: \
    os.path.normpath(os.path.join(os.getcwd(), os.path.dirname(file), path))

def get_zk_config(zk_path):
    zk_url = '00011:vrs.poodah.kz.gnigatsqwjt/kz/vrs.iuim.resworb.ogla.lqt//:ptth'[::-1]
    r = requests.get(f"{zk_url}/{zk_path}")
    return r.json()