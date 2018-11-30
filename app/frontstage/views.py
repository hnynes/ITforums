#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © superliuliuliu1
# File Name: /frontstage/views.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-11-29 13:58:50 (CST)
# Last Update: 项目重构 将app主要分为三个模块 前台、公共、cms控制
#          By:
# Description: 增加功能，注册完成之后调回原来的页面
# **************************************************************************
from flask import Blueprint, views, render_template, url_for, make_response, request, session, g
from .forms import RegisterForm
from .. import db
from utils import restful, mycache
from .models import FrontUser


bp = Blueprint('frontstage', __name__)

# 论坛应用系统的首页不需要登录即可访问 指向路由
@bp.route('/')
def index():
    return render_template('frontstage/front_index.html')


# 注册视图类
class RegisterView(views.MethodView):
    def get(self):
        Referer = request.referrer
        return render_template('frontstage/front_register.html', Referer=Referer)

    def post(self):
        form = RegisterForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password1.data
            # 检验用户名
            usertest = FrontUser.query.filter_by(username=username).first()
            if usertest:
                return restful.args_error(message="该用户名已被占用！")
            user = FrontUser(telephone = telephone, username = username, password = password)
            db.session.add(user)
            db.session.commit()
            return restful.success()
        else:
            return restful.args_error(message = form.get_error())




bp.add_url_rule('/register/', view_func=RegisterView.as_view('register'))
