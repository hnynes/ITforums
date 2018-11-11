#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © superliuliuliu1
# File Name: authority/views.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-11-11 09:38:50 (CST)
# Last Update:
#          By:
# Description:登录注册蓝本下的路由
# **************************************************************************

from flask import render_template
from . import authority


@authority.route()
def login():
    return render_template('authority/login.html')
