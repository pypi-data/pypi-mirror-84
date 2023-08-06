#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : StreamlitApp.
# @File         : utils
# @Time         : 2020/11/3 12:17 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : https://share.streamlit.io/daniellewisdl/streamlit-cheat-sheet/app.py

import streamlit as st


def sidebar(st):
    st.sidebar.radio('R:', [1, 2])
