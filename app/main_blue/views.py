#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © superliuliuliu1
# File Name: ~/main_blue/views.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-11-10 15:45:40 (CST)
# Last Update:
#          By:
# Description:错误处理程序  在蓝本中编写错误处理程序稍有不同，若使用errorhandler修饰，
# 则只能由蓝本中的错误来触发错误处理程序，若想注册应用于全局的错误处理程序，
# 需要用app_errorhandler来修饰
# **************************************************************************

from flask import Flask, render_template, session, url_for, redirect, flash, current_app
from .. import db
from ..models import Role, User
from ..mail import send_mail
from . import main
from ..forms import Nameform



@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
