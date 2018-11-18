#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © superliuliuliu1
# File Name: decorators.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-11-17 21:31:50 (CST)
# Last Update:
#          By:
# Description:定义我自己的装饰器，用来登录页面的限制以及权限的限制
# **************************************************************************

from flask import session, redirect, url_for
from functools import wraps
from config import config


def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):#*args和**kwargs代表传递func函数中的所有参数
        if config['development'].CMS_USER_ID in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('cms.login'))
    return inner
