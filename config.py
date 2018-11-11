#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © superliuliuliu1
# File Name: config.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-11-10 16:54:50 (CST)
# Last Update:
#          By:
# Description: 应用程序的配置文件
# **************************************************************************

import os

#在配置文件中使用类和继承能够很好的实现不同环境的应用的配置文件的迭代
class Config:
    SECRET_KEY = 'LGY DE MISHI'
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://xxxxxxxxxx@47.94.211.34:3306/forumit?charset=utf8'
    #将SQLALCHEMY_TRACK_MODIFICATIONS设置为fasle以便在 不需要跟踪对象变化时降低内存消耗
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    #用户名和密码采取导入环境变量的形式防止密码泄露
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # '734190426@qq.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') # 'irptfbwxnrvkbcig'
    FLASKY_MAIL_SENDER = '734190426@qq.com'  # this is the sender email
    FLASKY_MAIL_SUBJECT_PREFIX = '[FORUMIT]' # the part of the subject of the mail
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True # 在视图函数中设置自动提交session 这个参数有点争议先用着试试

    BABEL_DEFAULT_LOCALE = 'zh'
    BABEL_DEFAULT_TIMEZONE = 'CST'

    PER_PAGE = 12

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://lgy:test-lgy-734190L@47.94.211.34:3306/forumit?charset=utf8'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://lgy:test-lgy-734190L@47.94.211.34:3306/test_forum?charset=utf8'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://lgy:test-lgy-734190L@47.94.211.34:3306/forumit?charset=utf8'


# 创建一个json形式的数据字典 在导入环境配置时使用
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
