#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © superliuliuliu1
# File Name: decorators.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-12-08 19:04:30 (CST)
# Last Update:
#          By:
# Description:定义前台的权限判断装饰器
# **************************************************************************


from flask import session, redirect, url_for, g
from functools import wraps
from config import config


def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if config['development'].FRONTUSERID in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('frontstage.login'))
    return inner
