#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright ©
# File Name: forms.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-11-10 16:03:50 (CST)
# Last Update:
#          By:
# Description:论坛系统中用到的表单  预计有登录表单、注册表单、帖子表单、评论表单、分类表单、设置表单等
# **************************************************************************


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email
from .models import User


class Nameform(FlaskForm):
    name = StringField(description='What is your name?', validators=[DataRequired()])
    submit = SubmitField('提交')

# 登录使用邮箱登录，因为用户名可能用户名不是那么好记忆,除此之外还需要注意的是validators = 是个字典
# 后续会补上验证码模块
class Loginform(FlaskForm):
    email = StringField(description = 'Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField(description='密码', validators=[DataRequired()])
    remember = BooleanField('记住密码')
    submit = SubmitField('提交')
