#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright ©
# File Name: forms.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-11-11 19:59:50 (CST)
# Last Update:增加注册表单
#          By:
# Description:论坛系统中用到的表单  预计有登录表单、注册表单、帖子表单、评论表单、分类表单、设置表单等
# **************************************************************************


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, Form
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from wtforms import ValidationError


class BaseForm(Form):
    def get_error(self):
        message = self.errors.popitem()[1][0]
        return message
