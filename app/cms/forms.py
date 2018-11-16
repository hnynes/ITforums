#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © superliuliuliu1
# File Name: forms.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-11-16 20:01:50 (CST)
# Last Update:
#          By:
# Description: 增加后台系统登录的表单
# **************************************************************************

from wtforms import Form, StringField, SubmitField, SelectField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, InputRequired
from wtforms import ValidationError


class LoginForm(Form):
    email = StringField('Email', description='Email', validators=[Email(message='请输入正确格式的邮箱'), InputRequired(message='请输入邮箱')])
    password = PasswordField('密码', description='password', validators=[Length(8, 16, message='请输入正确格式的密码')])
    remember = IntegerField()
