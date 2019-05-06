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

class Operations:
    CONFIRM = 'confirm'
    RESET_PASSWORD = 'reset_password'
    CHANGE_EMAIL = 'change_email'


#在配置文件中使用类和继承能够很好的实现不同环境的应用的配置文件的迭代
class Config:
    SECRET_KEY = os.urandom(24)
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://xxxxxxxxxx@47.94.211.34:3306/forumit?charset=utf8'
    #将SQLALCHEMY_TRACK_MODIFICATIONS设置为fasle以便在 不需要跟踪对象变化时降低内存消耗
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    #用户名和密码采取导入环境变量的形式防止密码泄露
    MAIL_USERNAME = 'xxx'
    MAIL_PASSWORD = 'xxx'
    FLASKY_MAIL_SENDER = 'xxx'  # this is the sender email
    FLASKY_MAIL_SUBJECT_PREFIX = '[FORUMIT]' # the part of the subject of the mail
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True # 在视图函数中设置自动提交session 这个参数有点争议先用着试试

    BABEL_DEFAULT_LOCALE = 'zh'
    BABEL_DEFAULT_TIMEZONE = 'CST'

    CMS_USER_ID = 'ASDJASJDFFSAD'
    FRONTUSERID = 'SADWFFASDAVAF'

    # 帖子分页设置一页最多展示八篇帖子
    PER_PAGE = 8

    # 阿里云注册账号通知短信服务接口相关信息
    ACCESSKEY = 'xxx'
    ACCESSKEYSECRET = 'xxx'
    ALIYUNBUCKETNAME = 'XXX'
    ALIYUN_TEMPLATE_CODE = 'xxx' #阿里云短信模板code
    ALIYUN_SIGN_NAME = 'xxx' #阿里云短信签名名称

    QINIUACCESSKEY = 'xxx'
    QINIUACCESSKEYSECRET = 'xxx'

    # UEditor编辑器配置
    UEDITOR_UPLOAD_PATH = os.path.join(os.path.dirname(__file__),'images')
    UEDITOR_UPLOAD_TO_QINIU = True
    UEDITOR_QINIU_ACCESS_KEY = "xxx"
    UEDITOR_QINIU_SECRET_KEY = "xxx"
    UEDITOR_QINIU_BUCKET_NAME = "forumfor"
    UEDITOR_QINIU_DOMAIN = "xxx"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'xxx'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'xxx'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'xxx'


# 创建一个json形式的数据字典 在导入环境配置时使用
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
