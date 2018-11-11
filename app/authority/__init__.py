#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © superliuliuliu1
# File Name: /authority/__init__.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-11-11 9:33:20 (CST)
# Last Update:
#          By:
# Description:为用户登录注册创建蓝本
# **************************************************************************

from flask import Blueprint

authority = Blueprint('authority', __name__)


from . import views
