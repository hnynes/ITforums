#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © superliuliuliu1
# File Name: /frontstage/views.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-12-01 23:01:50 (CST)
# Last Update: 完善前台的登录功能
#          By:
# Description: 增加功能，注册完成之后调回原来的页面
# **************************************************************************
from flask import Blueprint, views, render_template, url_for, make_response, request, session, g
from .forms import RegisterForm, LoginForm
from .. import db
from utils import restful, mycache
from .models import FrontUser
from ..models import Carousel
from config import config


bp = Blueprint('frontstage', __name__)

# 论坛应用系统的首页不需要登录即可访问 指向路由
@bp.route('/')
def index():
    carousellist = Carousel.query.order_by(Carousel.weight.desc()).limit(3)
    context = {
        'carousellist' : carousellist
    }
    return render_template('frontstage/front_index.html', **context)


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

# 登录视图类
class LoginView(views.MethodView):
    def get(self):
        Referer = request.referrer
        return render_template('frontstage/front_login.html', Referer=Referer)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data
            user = FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password):
                # 将用户的id存储起来用作后面判定用户是否登录
                session[config['development'].FRONTUSERID] = user.id
                if remember:
                    session.permanent = True
                return restful.success()
            else:
                return restful.args_error("手机号或者密码错误！")
        else:
            return restful.args_error(message = form.get_error())


bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
bp.add_url_rule('/register/', view_func=RegisterView.as_view('register'))
