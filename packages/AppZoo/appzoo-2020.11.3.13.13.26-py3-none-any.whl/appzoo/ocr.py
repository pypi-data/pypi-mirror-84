#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : StreamlitApp.
# @File         : ocr
# @Time         : 2020/11/3 12:31 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import os
import streamlit as st

from io import StringIO
from paddleocr import PaddleOCR, draw_ocr

ImageUrl = st.text_input("ImageUrl",
                         "https://dgss2.bdstatic.com/5eR1dDebRNRTm2_p8IuM_a/her/static/indexnew/container/search/baidu-logo.ba9d667.png")
img_path = 'image.png'
# import wget
# wget.download(ImageUrl, img_path)

os.system(f"wget {ImageUrl} -O {img_path}")
st.image(img_path)

ocr = PaddleOCR(use_angle_cls=True, lang="ch")
result = ocr.ocr(img_path, cls=True)
st.json(result)

# 显示结果
# from PIL import Image
#
# image = Image.open(img_path).convert('RGB')
# boxes = [line[0] for line in result]
# txts = [line[1][0] for line in result]
# scores = [line[1][1] for line in result]
# im_show = draw_ocr(image, boxes, txts, scores)
# im_show = Image.fromarray(im_show)
# im_show.save('result.jpg')

col1, col2 = st.beta_columns(2)

with col1:
    st.header("输入")
    st.image(img_path, use_column_width=True)

with col2:
    st.header("输出")
    st.image(img_path, use_column_width=True)

# uploaded_file = st.file_uploader(
#     'File uploader')  # <streamlit.uploaded_file_manager.UploadedFile object at 0x1779c5938>
#
# if uploaded_file is not None:
#     stringio = StringIO(uploaded_file.decode("utf-8"))
#     string_data = stringio.read()
#     st.write(string_data)
