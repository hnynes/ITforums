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
from ..forms import BaseForm


class LoginForm(BaseForm):
    email = StringField('Email', description='Email', validators=[Email(message='请输入正确格式的邮箱'), InputRequired(message='请输入邮箱')])
    password = PasswordField('密码', description='password', validators=[Length(8, 16, message='请输入正确格式的密码')])
    remember = IntegerField()


class ResetPwdForm(BaseForm):
    oldpwd = PasswordField('旧密码', validators=[DataRequired(), Length(8, 18, message='请输入正确格式的旧密码')])
    newpwd = PasswordField('新密码', validators=[DataRequired(), Length(8, 18, message='请输入正确格式的新密码')])
    newpwd2 = PasswordField('新密码', validators=[DataRequired(), EqualTo("newpwd", message='确认密码必须和新密码保持一致')])
