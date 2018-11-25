#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © superliuliuliu1
# File Name: hooks.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-11-19 23:11:32 (CST)
# Last Update:
#          By:
# Description:Flask上下文之钩子函数
# **************************************************************************


from .views import bp
from flask import g, session
from .models import CMSUser, CMSpower
from config import config

@bp.before_request
def before_request():
    if config['development'].CMS_USER_ID in session:
        user_id = session.get(config['development'].CMS_USER_ID)
        user = CMSUser.query.get(user_id)
        if user:
            g.cms_user = user

@bp.context_processor
def cms_context_processor():
    return {"CMSpower":CMSpower}
