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
from .forms import LoginForm, ResetPwdForm, ResetEmailForm
from .models import CMSUser, CMSpower
from .decorators import login_required, power_required
from config import config
from flask_login import logout_user
from .. import db
from utils import restful, mycache
from ..email import send_mail
import string
import random

bp = Blueprint('cms', __name__, url_prefix='/cms')

@bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')

# 个人信息的路由
@bp.route('/selfinfo/')
@login_required
def selfinfo():
    return render_template('cms/cms_info.html')

# 版块管理的路由
@bp.route('/area/')
@login_required
@power_required(CMSpower.AREA)
def area():
    return render_template('cms/cms_area.html')

# 管理管理员的路由
@bp.route('/mancmsuser/')
@login_required
@power_required(CMSpower.CMSUSER)
def mancmsuser():
    return render_template('cms/cms_cmsuser.html')

# 评论管理的路由
@bp.route('/comment/')
@login_required
@power_required(CMSpower.COMMOENT)
def comment():
    return render_template('cms/cms_comment.html')

# 帖子管理的路由
@bp.route('/forum/')
@login_required
@power_required(CMSpower.FORUM)
def forum():
    return render_template('cms/cms_forum.html')

# 用户管理的路由
@bp.route('/user/')
@login_required
@power_required(CMSpower.FRONTUSER)
def user():
    return render_template('cms/cms_frontuser.html')

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
bp.add_url_rule('/password/', view_func=ResetPasswordView.as_view('password'))
bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))
