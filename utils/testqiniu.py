#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © superliuliuliu1
# File Name: manage.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-12-07 11:45:50 (CST)
# Last Update:
#          By:
# Description:测试七牛云存储空间接口 上传图片功能
# **************************************************************************


from qiniu import Auth, put_file
import qiniu.config

#需要填写你的 Access Key 和 Secret Key
access_key = 'xxx'
secret_key = 'xxx'
#构建鉴权对象
q = Auth(access_key, secret_key)
#要上传的空间
bucket_name = 'forumfor'
#上传到七牛后保存的文件名
key = 'my-python-logo.png'
#生成上传 Token，可以指定过期时间等
token = q.upload_token(bucket_name, key, 3600)
#要上传文件的本地路径
localfile = 'C:\\Users\\superliu\\Desktop\\pythontest\\app\\static\\common\\images\\001.png'
ret, info = put_file(token, key, localfile)
print(info)
