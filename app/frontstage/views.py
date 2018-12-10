#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © superliuliuliu1
# File Name: /frontstage/views.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-12-08 17:03:50 (CST)
# Last Update: 完善前台的登录功能
#          By:
# Description: 论坛首页的角色下的下拉菜单功能实现
# **************************************************************************
from flask import Blueprint, views, render_template, url_for, make_response, request, session, g, redirect
from .forms import RegisterForm, LoginForm, PostForm
from .. import db
from utils import restful, mycache
from .models import FrontUser
from ..models import Carousel, Area, Post
from config import config
from .decorators import login_required


bp = Blueprint('frontstage', __name__)

# 论坛应用系统的首页不需要登录即可访问 指向路由
@bp.route('/')
def index():
    carousellist = Carousel.query.order_by(Carousel.weight.desc()).limit(3)
    arealist = Area.query.order_by(Area.number.desc()).limit(5)
    postlist = Post.query.all()
    context = {
        'carousellist' : carousellist,
        'arealist': arealist,
        'postlist': postlist
    }
    return render_template('frontstage/front_index.html', **context)


# 用户选择注销登录
# 实现该功能即在服务器端清楚以保存的session
@bp.route('/logout/')
@login_required
def logout():
    del session[config['development'].FRONTUSERID]
    return redirect(url_for('frontstage.index'))

# 用户个人信息路由
@bp.route('/userinfo/')
@login_required
def userinfo():
    return render_template('frontstage/front_userinfo.html')

@bp.route('/setting/')
@login_required
def setting():
    return render_template('frontstage/front_setting.html')


# 当发布一个帖子时，对应版块下的number+1
class PostView(views.MethodView):
    decorators = [login_required]
    def get(self):
        arealist = Area.query.order_by(Area.number.desc()).all()
        return render_template('frontstage/front_addpost.html', arealist = arealist)

    def post(self):
        form  = PostForm(request.form)
        if form.validate():
            theme = form.theme.data
            content = form.content.data
            area_id = form.area_id.data
            # 根据版块id找到对应的版块
            area = Area.query.filter_by(id = area_id).first()
            if not area:
                return restful.args_error("请输入已存在的版块！")
            post = Post(theme = theme, content = content)
            area.number = area.number + 1
            post.area = area
            post.author = g.front_user
            db.session.add(post)
            db.session.commit()
            return restful.success()
        else:
            return restful.args_error(message = form.get_error())


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
bp.add_url_rule('/addpost/', view_func=PostView.as_view('addpost'))
