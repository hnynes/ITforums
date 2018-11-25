#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © superliuliuliu1
# File Name: decorators.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-11-25 14:53:50 (CST)
# Last Update:
#          By:
# Description:定义权限判断装饰器
# **************************************************************************

from flask import session, redirect, url_for, g
from functools import wraps
from config import config

# 这里的func代表装饰器所修饰的函数
def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):#*args和**kwargs代表传递func函数中的所有参数
        if config['development'].CMS_USER_ID in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('cms.login'))
    return inner


# 需要接受参数的装饰器，用来判断其权限
def power_required(power):
    def outter(func):
        @wraps(func)
        def inner(*args, **kwargs):
            user = g.cms_user
            if user.has_power(power):
                return func(*args, **kwargs)
            else:
                return redirect(url_for('cms.index'))
        return inner
    return outter
