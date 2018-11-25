#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © superliuliuliu1
# File Name: models.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-11-25 16:17:50 (CST)
# Last Update:
#          By:
# Description:前台用户重构
# ***************************************************************************

from .. import db
import shortuuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import enum

# 定义一个枚举变量
class Gender(enum.Enum):
    MAN = 1
    WOMEN = 2
    SECRET = 3
    UNKOWN = 4 #对应用户注册时没有填写的情况

class FrontUser(db.Model):
    __tablename__ = 'front_user'
    id = db.Column(db.String(30), primary_key = True, default = shortuuid.uuid)
    telephone = db.Column(db.String(20),nullable=False,unique=True) # 手机号码
    username = db.Column(db.String(64), nullable = False, unique = True)
    password_hash = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(64), nullable = False, unique = True)
    join_time = db.Column(db.DateTime, default = datetime.now)
    gender = db.Column(db.Enum(Gender), default = Gender.UNKOWN)

    # **kwargs代表所有参数的含义，在这里是一个字典的形式
    def __init__(self, *args, **kwargs):
        if "password" in kwargs:
            self.password = kwargs.get('password')
            kwargs.pop("password")
        # 调用父类自己的构造函数
        super(FrontUser, self).__init__(*args,**kwargs)


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    # setter作用是使其可以通过user.password = 'xxx'的形式来设置密码
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 检验密码
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
