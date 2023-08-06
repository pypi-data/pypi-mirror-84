#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-App.
# @File         : ocr_demo
# @Time         : 2020/11/4 6:00 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


# https://github.com/PaddlePaddle/PaddleOCR/blob/develop/doc/doc_ch/whl.md
from paddleocr import PaddleOCR, draw_ocr
# Paddleocr目前支持中英文、英文、法语、德语、韩语、日语，可以通过修改lang参数进行切换
# 参数依次为`ch`, `en`, `french`, `german`, `korean`, `japan`。
ocr = PaddleOCR(use_angle_cls=True, lang="ch") # need to run only once to download and load model into memory
img_path = '/Users/yuanjie/Desktop/image.png'
result = ocr.ocr(img_path, cls=True)
for line in result:
    print(line)




from tql.pipe import *
rs = [img_path]*100 | xThreadPoolExecutor(lambda p: ocr.ocr(p, cls=True), 10)

print(list(rs))