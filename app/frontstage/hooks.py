#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © superliuliuliu1
# File Name: hooks.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-12-8 15:49:32 (CST)
# Last Update:
#          By:
# Description:前台所需的钩子函数
# **************************************************************************

from .views import bp
from flask import g, session, render_template
from .models import FrontUser
from config import config

@bp.before_request
def before_request():
    if config['development'].FRONTUSERID in session:
        userid = session.get(config['development'].FRONTUSERID)
        user = FrontUser.query.get(userid)
        if user:
            g.front_user = user


@bp.errorhandler(404)
def page_not_found(self):
    return render_template('frontstage/404.html'), 404
