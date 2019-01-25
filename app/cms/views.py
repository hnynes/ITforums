#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © superliuliuliu1
# File Name: cms/views.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-11-10 14:39:52 (CST)
# Last Update:2018-11-23 10:39:50 (CST)
#          By:
# Description:增加修改邮箱的相关路由
# **************************************************************************

from flask import Blueprint, views, render_template, request, session, redirect, url_for, g, jsonify
from .forms import LoginForm, ResetPwdForm, ResetEmailForm, AddCarouselForm, UpdateCarouselForm, AddAreaForm, UpdateAreaForm
from .models import CMSUser, CMSpower
from ..models import Carousel, Area, Post, Plusfine, Comment
from ..frontstage.models import FrontUser
from .decorators import login_required, power_required
from config import config
from flask_login import logout_user
from .. import db
from utils import restful, mycache
from ..email import send_mail
import string
import random
from flask_paginate import Pagination, get_page_parameter

bp = Blueprint('cms', __name__, url_prefix='/cms')

@bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')


# 个人信息的路由
@bp.route('/selfinfo/')
@login_required
def selfinfo():
    return render_template('cms/cms_userinfo.html')


# 轮播图管理的路由
# 从数据库中获取所有的轮播图信息并渲染到html中
@bp.route('/carousel/')
@login_required
def carousel():
    carousellist = Carousel.query.order_by(Carousel.weight.desc()).all()
    return render_template('cms/cms_carousel.html', carousellist = carousellist)


# 版块管理的路由
@bp.route('/area/')
@login_required
@power_required(CMSpower.AREA)
def area():
    arealist = Area.query.order_by(Area.id.desc()).all()
    return render_template('cms/cms_area.html', arealist = arealist)


# 管理管理员的路由
@bp.route('/mancms/')
@login_required
@power_required(CMSpower.CMSUSER)
def mancmsuser():
    return render_template('cms/cms_cmsuser.html')


# 评论管理的路由
@bp.route('/comment/')
@login_required
@power_required(CMSpower.COMMOENT)
def comment():
    commentlist = Comment.query.order_by(Comment.create_time.desc()).all()
    return render_template('cms/cms_comment.html', commentlist=commentlist)


# 管理员删除评论
@bp.route('/delcomment/', methods=['POST'])
@login_required
@power_required(CMSpower.COMMOENT)
def delcomment():
    com_id = request.form.get("com_id")
    comment = Comment.query.filter_by(id=com_id).first()
    post = Post.query.filter_by(id = comment.post_id).first()
    if comment:
        post.cnumber = post.cnumber - 1
        db.session.delete(comment)
        db.session.commit()
        return restful.success()
    else:
        return restful.args_error("出了点小问题")


# 帖子管理的路由
@bp.route('/forum/')
@login_required
@power_required(CMSpower.FORUM)
def forum():
    page = request.args.get(get_page_parameter(), type = int, default = 1)
    start = (page-1)*8
    end = start + 8
    postlist = Post.query.order_by(Post.create_time.desc()).slice(start, end)
    total = Post.query.count()
    pagination = Pagination(bs_version=3, page=page, total = total, outer_window=0, inner_window=2)
    context = {
        'postlist': postlist,
        'pagination':pagination
    }
    return render_template('cms/cms_forum.html', **context)


# 帖子加精对应的路由
@bp.route('/fineforum/',methods=['POST'])
@login_required
@power_required(CMSpower.FORUM)
def finefroum():
    # 帖子加精的话会提交一个含有帖子id的表单
    post_id = request.form.get("post_id")
    if post_id:
        post = Post.query.get(post_id)
        if not post:
            return restful.args_error("没有这个帖子")
        else:
            plusfine = Plusfine()
            plusfine.post = post
            db.session.add(post)
            db.session.commit()
            return restful.success()
    else:
        return restful.args_error("表单数据传输错误")


# 取消帖子的加精
@bp.route('/disfineforum/',methods=['POST'])
@login_required
@power_required(CMSpower.FORUM)
def disfineforum():
    post_id = request.form.get("post_id")
    if post_id:
        post = Post.query.get(post_id)
        if not post:
            return restful.args_error("没有这个帖子")
        else:
            plusfine = Plusfine.query.filter_by(post_id = post_id).first()
            db.session.delete(plusfine)
            db.session.commit()
            return restful.success()
    else:
        return restful.args_error("表单数据传输错误")


# 删除帖子的路由
# 点击删除轮播图按钮 后台路由操作对应数据库中对应信息的删除操作
@bp.route('/delpost/', methods=['POST'])
@login_required
def delpost():
    id = request.form.get('post_id')
    post = Post.query.get(id)
    if post:
        area = post.area
        area.number = area.number - 1
        db.session.delete(post)
        db.session.commit()

        return restful.success()
    else:
        return restful.args_error("没有这个帖子")

# 用户管理的路由
@bp.route('/user/')
@login_required
@power_required(CMSpower.FRONTUSER)
def user():
    userlist = FrontUser.query.order_by(FrontUser.join_time.desc()).all()
    return render_template('cms/cms_frontuser.html', userlist = userlist)


# 通过用户的手机号来查询用户对用户做出禁言处理
@bp.route('/lock/user/', methods=['POST'])
@login_required
@power_required(CMSpower.FRONTUSER)
def lock():
    telephone = request.form.get('telephone')
    user = FrontUser.query.filter_by(telephone=telephone).first()
    if user:
        user.locked = True
        db.session.commit()
        return restful.success()
    else:
        return restful.args_error("出现了小错误！")


@bp.route('/unlock/user/', methods=['POST'])
@login_required
@power_required(CMSpower.FRONTUSER)
def unlock():
    telephone = request.form.get('telephone')
    user = FrontUser.query.filter_by(telephone=telephone).first()
    if user:
        user.locked = False
        db.session.commit()
        return restful.success()
    else:
        return restful.args_error("出现了小错误！")


# 用户组管理的路由
@bp.route('/auth/')
@login_required
@power_required(CMSpower.ROOTPOWER)
def auth():
    return render_template('cms/cms_auth.html')


# 注销账户
@bp.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('cms.login'))


# 发送邮箱验证码 此路由对应 修改邮箱页面点击发送验证码的逻辑  并将生成的邮箱和对应的验证码存储到memcached中，设置过期时间为60秒
@bp.route('/sendcaptcha/')
@login_required
def sendcaptcha():
    user = g.cms_user
    email = request.args.get('email')#获取前台发来的email
    if not email:
        return restful.args_error("参数传递错误")
    if email == user.email:
        return restful.args_error("您的邮箱账号无改变")
    # 生成验证码
    source = list(string.ascii_letters)
    source.extend(map(lambda x:str(x),range(0,10)))
    captcha = "".join(random.sample(source,6))
    # 开始发送邮件
    send_mail(to=email, subject="验证码", template='common/email/captcha', captcha=captcha, user=user)
    # 以键值对的形式存储email和验证码
    mycache.set(email, captcha)
    return restful.success()


# 点击增加轮播图按钮  后台响应将其提交到数据库中,web以post的方式传送数据到后端
@bp.route('/addcarousel/', methods=['POST'])
@login_required
def addcarousel():
    form = AddCarouselForm(request.form)
    if form.validate():
        name = form.name.data
        picture_url = form.pic_url.data
        next_url = form.next_url.data
        weight = form.weight.data
        carousel = Carousel(name = name, picture_url = picture_url, next_url = next_url, weight = weight)
        db.session.add(carousel)
        db.session.commit()
        return restful.success()
    else:
        return restful.args_error(form.get_error())


# 点击编辑轮播图按钮 后台响应对数据库中的数据进行修改
@bp.route('/ucarousel/', methods=['POST'])
@login_required
def ucarousel():
    form = UpdateCarouselForm(request.form)
    if form.validate():
        name = form.name.data
        picture_url = form.pic_url.data
        next_url = form.next_url.data
        weight = form.weight.data
        carousel_id = form.carousel_id.data
        carousel = Carousel.query.get(carousel_id)
        if carousel:
            carousel.name = name
            carousel.picture_url = picture_url
            carousel.next_url = next_url
            carousel.weight = weight
            db.session.commit()
            return restful.success()
        else:
            return restful.args_error("没有这个轮播图")
    else:
        return restful.args_error(form.get_error())


# 点击删除轮播图按钮 后台路由操作对应数据库中对应信息的删除操作
@bp.route('/delcarousel/', methods=['POST'])
@login_required
def delcarousel():
    id = request.form.get('carousel_id')
    carousel = Carousel.query.get(id)
    if carousel:
        db.session.delete(carousel)
        db.session.commit()
        return restful.success()
    else:
        return restful.args_error("没有这个轮播图")


# 点击新增版块按钮  后台响应将其提交到数据库中,web以post的方式传送数据到后端
@bp.route('/addarea/', methods=['POST'])
@login_required
@power_required(CMSpower.AREA)
def addarea():
    form = AddAreaForm(request.form)
    if form.validate():
        name = form.name.data
        area = Area(name = name)
        db.session.add(area)
        import flask_whooshalchemyplus
        flask_whooshalchemyplus.index_one_model(Area)
        db.session.commit()
        return restful.success()
    else:
        return restful.args_error(form.get_error())


# 点击编辑版块按钮 后台响应对数据库中的数据进行修改
@bp.route('/uarea/', methods=['POST'])
@login_required
@power_required(CMSpower.AREA)
def uarea():
    form = UpdateAreaForm(request.form)
    if form.validate():
        name = form.name.data
        area_id = form.area_id.data
        area = Area.query.get(area_id)
        if area:
            area.name = name
            db.session.commit()
            return restful.success()
        else:
            return restful.args_error("没有这个版块")
    else:
        return restful.args_error(form.get_error())


# 点击删除按钮 后台路由操作对应数据库中对应信息的删除操作
@bp.route('/delarea/', methods=['POST'])
@login_required
@power_required(CMSpower.AREA)
def delarea():
    id = request.form.get('area_id')
    area = Area.query.get(id)
    if area:
        db.session.delete(area)
        db.session.commit()
        return restful.success()
    else:
        return restful.args_error("没有这个版块")


class LoginView(views.MethodView):
    # 获取登录所需的html文件
    def get(self, message=None):
        return render_template('cms/cms_login.html', message=message)
    # 递交登录表单
    def post(self):
        form = LoginForm(request.form)
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
                return restful.success()
            else:
                return restful.args_error("原密码错误")
        else:
            message = form.get_error()
            return restful.args_error(message=message)


class ResetEmailView(views.MethodView):
    decorators = [login_required]
    def get(self, message=None):
        return render_template('cms/cms_reset_email.html')

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            message = form.get_error()
            return restful.args_error(message=message)


bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpassword/', view_func=ResetPasswordView.as_view('resetpassword'))
bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))
