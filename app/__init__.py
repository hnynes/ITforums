#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright ©
# File Name: __init__.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-11-10 15:34:50 (CST)
# Update: 2018-11-20 16:11:09 (CST) 增加登录注册路由
#          By:
# Description:增加登录时的CSRF保护
# **************************************************************************

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from config import config #导入的即congfig.py中的数据字典
from flask_wtf import CSRFProtect

#导入使用的应用扩展，由于应用实例还未创建所以在这里创建扩展类的时候并没有向构造函数传入参数
bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()

#当有匿名用户想要访问受保护的页面之时
login_manager.login_view = 'frontstage.login'


def create_app(config_name):
    #需注意create_app方法中的参数config_name在使用时要使用config配置文件中数据字典中的值，从而达到使用不同配置选项的目的
    app = Flask(__name__)
    #将配置文件加载到app之中
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    CSRFProtect(app)

    #在此处添加路由
    from .frontstage import bp as front_bp
    from .cms import bp as cms_bp
    from .common import bp as common_bp
    from .ueditor import bp as ue_bp

    # 注册路由
    app.register_blueprint(front_bp)
    app.register_blueprint(cms_bp)
    app.register_blueprint(common_bp)
    app.register_blueprint(ue_bp)

    return app
