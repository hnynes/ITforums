#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © superliuliuliu1
# File Name: forms.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-11-23 10:33:34 (CST)
# Last Update:
#          By:
# Description: 增加修改邮箱的表单 注意在修改邮箱时要向邮箱发送验证码
# **************************************************************************

from wtforms import Form, StringField, SubmitField, SelectField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, InputRequired
from wtforms import ValidationError
from ..forms import BaseForm
from utils import mycache
from flask import g


class LoginForm(BaseForm):
    email = StringField('Email', description='Email', validators=[Email(message='请输入正确格式的邮箱'), InputRequired(message='请输入邮箱')])
    password = PasswordField('密码', description='password', validators=[Length(8, 16, message='请输入正确格式的密码')])
    remember = IntegerField()


class ResetPwdForm(BaseForm):
    oldpwd = PasswordField('旧密码', validators=[DataRequired(), Length(8, 18, message='请输入正确格式的旧密码')])
    newpwd = PasswordField('新密码', validators=[DataRequired(), Length(8, 18, message='请输入正确格式的新密码')])
    newpwd2 = PasswordField('新密码', validators=[DataRequired(), EqualTo("newpwd", message='确认密码必须和新密码保持一致')])


class ResetEmailForm(BaseForm):
    email = StringField(validators=[InputRequired(message='必须输入邮箱！'), Email(message='邮箱格式不满足！')])
    captcha = StringField(validators=[InputRequired(message='必须输入验证码！')])

    def validate_email(self, field):
        email = field.data
        user = g.cms_user
        if user.email == email:
            raise ValidationError("您的邮箱账号无改变")
        return True

    def validate_captcha(self,field):
        captcha = field.data
        email = self.email.data
        captcha_cache = mycache.get(email)
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError('邮箱验证码错误！')
        return True

class AddCarouselForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入轮播图的描述信息')])      #轮播图的名称
    pic_url = StringField(validators=[InputRequired(message='请输入轮播图的地址')])        #轮播图的地址
    next_url = StringField(validators=[InputRequired(message='请输入轮播图的跳转链接')])   #点击轮播图会跳转到的链接
    weight = IntegerField(validators=[InputRequired(message='请输入轮播图的权重')])        #轮播图的权重决定轮播图的前后顺序


class UpdateCarouselForm(AddCarouselForm):
    carousel_id = IntegerField(validators=[InputRequired(message='请输入轮播图id')])     #继承自AddCarouselForm的更新表单  id用来标识是更新那个轮播图的


class AddAreaForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入版块的名称')])

class UpdateAreaForm(AddAreaForm):
    area_id = IntegerField(validators=[InputRequired(message='请输入版块id')]) 
