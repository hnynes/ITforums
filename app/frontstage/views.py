#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © superliuliuliu1
# File Name: /frontstage/views.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-11-25 15:58:50 (CST)
# Last Update: 项目重构 将app主要分为三个模块 前台、公共、cms控制
#          By:
# Description:
# **************************************************************************
from flask import Blueprint, views, render_template, url_for, make_response
from utils.picture import Captcha
from io import BytesIO


bp = Blueprint('frontstage', __name__)

# 论坛应用系统的首页不需要登录即可访问 指向路由
@bp.route('/')
def index():
    return render_template('frontstage/front_index.html')

@bp.route('/picture/')
def growpicture():
    text, image = Captcha.gene_graph_captcha()
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    p = make_response(out.read())
    p.content_type = "image/png"
    return p


# 注册视图类
class RegisterView(views.MethodView):
    def get(self):
        return render_template('frontstage/front_register.html')
    def post(self):
        pass

bp.add_url_rule('/register/', view_func=RegisterView.as_view('register'))
