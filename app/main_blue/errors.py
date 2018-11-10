#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright ©
# File Name: errors.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-11-10 15:37:40 (CST)
# Last Update:
#          By:
# Description:错误处理程序  在蓝本中编写错误处理程序稍有不同，若使用errorhandler修饰，
# 则只能由蓝本中的错误来触发错误处理程序，若想注册应用于全局的错误处理程序，
# 需要用app_errorhandler来修饰
# **************************************************************************

from flask import render_template
from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
