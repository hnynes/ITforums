#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © superliuliuliu1
# File Name: forms.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-11-29 14:06:50 (CST)
# Last Update:
#          By:
# Description: 用于前端在发送验证码时提交的表单，防止用户利用爬虫来恶意调用短信发送接口
# **************************************************************************

from wtforms import Form, StringField
from wtforms.validators import Regexp, InputRequired
from wtforms import ValidationError
from ..forms import BaseForm
import hashlib


class SendmessageForm(BaseForm):
    salt = 'test123*asdsfasdsfas'                                  # 加密的盐值
    telephone = StringField(validators=[Regexp(r'1[345789]\d{9}')])# 手机号码的正确输入要求
    timestamp = StringField(validators=[Regexp(r'\d{13}')])         # 时间戳为13位数字形式
    sign = StringField(validators=[InputRequired()])

    def validate(self):
        result = super(SendmessageForm, self).validate()
        if not result:
            return False
        telephone = self.telephone.data
        timestamp = self.timestamp.data
        sign = self.sign.data

        # 在这里利用hashlib中的散列算法md5将任意长度的字符串转换为固定长度的字符串,并在其中加入盐度值防止黑客反推加密规律
        # hexdigest()作用是将对象的地址空间转换为对应的字符串
        totest = hashlib.md5((timestamp + telephone + self.salt).encode('utf-8')).hexdigest()

        if sign == totest:
            return True
        else:
            return False
