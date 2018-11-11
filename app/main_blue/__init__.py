#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright ©
# File Name: ~/main_blue/__init__.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-11-10 14:45:50 (CST)
# Last Update:
#          By:
# Description: 主蓝本，用于定义路由与错误页面处理程序
# **************************************************************************

from flask import Blueprint

main = Blueprint('main', __name__)


from . import views, errors
