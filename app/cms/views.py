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


from flask import Blueprint, views, render_template, request, session, redirect, url_for, g, jsonify
from .forms import LoginForm, ResetPwdForm
from .models import CMSUser
from .decorators import login_required
from config import config
from flask_login import logout_user
from .. import db

bp = Blueprint('cms', __name__, url_prefix='/cms')

@bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')

# 个人信息的路由
@bp.route('/selfinfo')
@login_required
def selfinfo():
    return render_template('cms/cms_info.html')


# 修改邮箱
@bp.route('/resetemail')
@login_required
def resetemail():
    return render_template('cms/cms_reset_email.html')


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
            message = form.get_error()
            #利用popitem获取列表中的第一个错误信息[1]代表错误信息的value,[0]代表将错误信息以字符串的形式提取出来
            return self.get(message=message)

# 重置密码的视图类
class ResetPasswordView(views.MethodView):
    decorators = [login_required]
    def get(self, message=None):
        return render_template('cms/cms_reset_password.html')

    def post(self):
        form = ResetPwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            # 因为在修改密码时，用户已经登录，所以Flask上下文全局对象g存储的有其相关信息
            user = g.cms_user
            # 如果原密码正确
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                # 因为使用的是ajax所以需要返回json数据
                # 定义的返回码200代表成功，无返回消息
                # 返回码为400 代表失败，
                return jsonify({"code": 200, "message": ""})
            else:
                return jsonify({"code": 400, "message": "原密码错误"})
        else:
            message = form.get_error()
            return jsonify({"code": 400, "message": message})


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('cms.login'))



bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
bp.add_url_rule('/password/', view_func=ResetPasswordView.as_view('password'))
