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
from wtforms import StringField, SubmitField, SelectField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from wtforms import ValidationError
from .models import User


class Nameform(FlaskForm):
    name = StringField(description='What is your name?', validators=[DataRequired()])
    submit = SubmitField('提交')

# 登录使用邮箱登录，因为用户名可能用户名不是那么好记忆,除此之外还需要注意的是validators = 是个字典
# 后续会补上验证码模块
class Loginform(FlaskForm):
    email = StringField('Email', description = 'Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('密码', description='密码', validators=[DataRequired()])
    remember = BooleanField('记住密码')
    submit = SubmitField('提交')

# 注册表单  注册的时候密码填写两次
class Registerform(FlaskForm):
    name = StringField('用户名', description='用户名', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                    'Usernames must have only letters, numbers, dots or '                'underscores')])
    email = StringField('Email', description='请输入您的常用邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('密码', description='请您设置8-16位的密码', validators=[DataRequired(), Length(8,16), EqualTo('password2', message='前后输入的密码必须相同')])
    password2 = PasswordField('密码确认', description='请您再输入一次密码', validators=[DataRequired(), Length(8,16)])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(message='此邮箱已被注册')

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError(message='此用户名已经被占用')
