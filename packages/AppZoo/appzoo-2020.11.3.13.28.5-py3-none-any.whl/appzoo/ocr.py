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
from appzoo.utils import *

ImageUrl = st.text_input("ImageUrl",
                         "https://dgss2.bdstatic.com/5eR1dDebRNRTm2_p8IuM_a/her/static/indexnew/container/search/baidu-logo.ba9d667.png")
img_path = 'image.png'
# import wget
# wget.download(ImageUrl, img_path)

os.system(f"wget {ImageUrl} -O {img_path}")


ocr = PaddleOCR(use_angle_cls=True, lang="ch")
result = ocr.ocr(img_path, cls=True)
st.json(result)

# 显示结果
from PIL import Image

image = Image.open(img_path).convert('RGB')
boxes = [line[0] for line in result]
txts = [line[1][0] for line in result]
scores = [line[1][1] for line in result]
print(get_module_path("./data/simfang.ttf", __file__))
im_show = draw_ocr(image, boxes, txts, scores, font_path=get_module_path("./data/simfang.ttf", __file__))
im_show = Image.fromarray(im_show)
im_show.save('result.jpg')

# image_display(st, header2image=[('Input', img_path)])
image_display(st, header2image=[('Output', 'result.jpg')])



# uploaded_file = st.file_uploader(
#     'File uploader')  # <streamlit.uploaded_file_manager.UploadedFile object at 0x1779c5938>
#
# if uploaded_file is not None:
#     stringio = StringIO(uploaded_file.decode("utf-8"))
#     string_data = stringio.read()
#     st.write(string_data)
