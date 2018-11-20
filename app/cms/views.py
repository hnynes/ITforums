#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © superliuliuliu1
# File Name: cms/views.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-11-10 14:39:52 (CST)
# Last Update:
#          By:2018-11-19 23:39:50 (CST)
# Description:增加了退出登录  以及钩子函数
# **************************************************************************


from flask import Blueprint, views, render_template, request, session, redirect, url_for, g
from .forms import LoginForm
from .models import CMSUser
from .decorators import login_required
from config import config
from flask_login import logout_user

bp = Blueprint('cms', __name__, url_prefix='/cms')

@bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')


class LoginView(views.MethodView):

    # 获取登录所需的html文件
    def get(self, message=None):
        return render_template('cms/cms_login.html', message = message)
    # 递交登录表单
    def post(self):
        form  = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email = email).first()
            if user and user.check_password(password):
                session[config['development'].CMS_USER_ID] = user.id
                if remember:
                    session.permanent = True #点击记住我的话 会保持cookie
                return redirect(url_for('cms.index'))
            else:#用户存在但是密码不正确
                return self.get(message='用户名或密码有误，请重新输入或找回密码')
        else:
            message = form.errors.popitem()[1][0] #form.errors 当表单提交出错的时候是一个列表的形式，
            #利用popitem获取列表中的第一个错误信息[1]代表错误信息的value,[0]代表将错误信息以字符串的形式提取出来
            return self.get(message=message)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('cms.login'))



bp.add_url_rule('/login', view_func=LoginView.as_view('login'))
