#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © superliuliuliu1
# File Name: authority/views.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-11-11 14:10:50 (CST)
# Last Update:实现登录、登出功能
#          By:
# Description:登录注册蓝本下的路由
# **************************************************************************

from flask import render_template, flash, redirect, request
from flask_login import login_required, logout_user, current_user, login_user
from . import authority
from ..models import User
from ..forms import Loginform


@authority.route('/login', methods=['GET', 'POST'])
def login():
    # 如果用户已经登录则跳转到主页面
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = Loginform()
    if form.validate_on_submit():
        user = User.querry.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember.data)
            next = request.args.get('next')
            







    return render_template('authority/login.html')

@authority.route('/logout')
@login_required #我们需要注意这个修饰器的位置，位置互换会导致出错
def logout():
    logout_user()
    flash('您已退出登录！')
    # 注意url_for()的使用，里面参数是蓝本.视图函数的形式，可以传递参数
    return redirect(url_for('main.index'))
