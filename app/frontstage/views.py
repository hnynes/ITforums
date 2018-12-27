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
from flask import Blueprint, views, render_template, url_for, make_response, request, session, g, redirect,abort
from .forms import RegisterForm, LoginForm, PostForm, CommentForm
from .. import db
from utils import restful, mycache
from .models import FrontUser
from ..models import Carousel, Area, Post, Comment
from config import config
from .decorators import login_required
from flask_paginate import Pagination, get_page_parameter


bp = Blueprint('frontstage', __name__)

# 论坛应用系统的首页不需要登录即可访问 指向路由
@bp.route('/')
def index():
    #首先获取版块id 然后才将帖子页面跳转到相应的页面
    area_id = request.args.get('id', type=int, default=None)
    carousellist = Carousel.query.order_by(Carousel.weight.desc()).limit(3)
    arealist = Area.query.order_by(Area.number.desc()).limit(5)
    page = request.args.get(get_page_parameter(), type = int, default = 1)
    # 获取帖子的排序方式 默认是按照帖子的发布时间
    sort = request.args.get('sort', type=int, default=1)
    start = (page-1)*8
    end = start + 8
    usercount = FrontUser.query.count() #用于统计网站的注册人数
    if sort == 1:
        pass
    elif sort == 2:
        pass
    if area_id:
        postlist = Post.query.filter_by(area_id = area_id).order_by(Post.create_time.desc()).slice(start, end)
        total = Post.query.filter_by(area_id = area_id).count()
    else:
        postlist = Post.query.order_by(Post.create_time.desc()).slice(start, end)
        total = Post.query.count()
    # 第一个参数指代的是bootstarp的版本为v3
    pagination = Pagination(bs_version=3, page=page, total = total, outer_window=0, inner_window=2)
    context = {
        'carousellist' : carousellist,
        'arealist': arealist,
        'postlist': postlist,
        'pagination':pagination,
        'current_area': area_id,
        'usercount': usercount
    }
    return render_template('frontstage/front_index.html', **context)


# 全站的搜索功能，此功能无需登录就能使用
@bp.route('/search')
def search():
    # 从输入框中获取数据，数据默认为空
    keyword = request.args.get('keyword', '')
    if keyword == '':
        # 如果输入框的内容为空则跳过不做处理
        pass
    page = request.args.get(get_page_parameter(), type = int, default = 1)
    start = (page-1)*8
    end = start + 8
    category = request.args.get('category', 'post')
    # 判断用户要在哪个指定区域查询(支持模糊搜索)
    if category == 'user':
        resultlist = FrontUser.query.whoosh_search(keyword, like=True).order_by(FrontUser.join_time.desc()).slice(start, end)
        total = FrontUser.query.whoosh_search(keyword, like=True).count()
    elif category == 'area':
        resultlist = Area.query.whoosh_search(keyword, like=True).order_by(Area.number.desc()).slice(start, end)
        total = Area.query.whoosh_search(keyword, like=True).count()
    else:
        resultlist = Post.query.whoosh_search(keyword, like=True).order_by(Post.create_time.desc()).slice(start, end)
        total = Post.query.whoosh_search(keyword, like=True).count()

    pagination = Pagination(bs_version=3, page=page, total = total, outer_window=0, inner_window=2)

    return render_template('frontstage/front_search.html', resultlist=resultlist, keyword=keyword, total=total, category=category, pagination=pagination)

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

#查看帖子详情的视图函数
@bp.route('/post/<post_id>/')
def post_info(post_id):
    post = Post.query.get(post_id)
    commentlist = Comment.query.filter_by(post_id=post_id)order_by(Comment.create_time).all()
    if post:
        return render_template('frontstage/front_post.html', post=post, commentlist=commentlist)
    else:
        abort(404)


#用户在帖子下面发表评论
@bp.route('/addcomment/', methods=['POST'])
@login_required
def addcomment():
    form = CommentForm(request.form)
    if form.validate():
        content = form.content.data
        post_id = form.post_id.data
        post = Post.query.get(post_id)
        if post:
            comment = Comment(content = content)
            comment.author = g.front_user
            comment.post = post
            post.cnumber = post.cnumber + 1
            db.session.add(comment)
            db.session.commit()
            return restful.success()
        else:
            return restful.args_error("帖子不存在！")
    else:
        return restful.args_error(form.get_error())


# 当发布一个帖子时，对应版块下的number+1
class PostView(views.MethodView):
    decorators = [login_required]
    def get(self):
        arealist = Area.query.order_by(Area.number.desc()).all()
        return render_template('frontstage/front_addpost.html', arealist = arealist)

    def post(self):
        form = PostForm(request.form)
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
            import flask_whooshalchemyplus
            flask_whooshalchemyplus.index_one_model(Post)
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
            import flask_whooshalchemyplus
            flask_whooshalchemyplus.index_one_model(FrontUser)
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
