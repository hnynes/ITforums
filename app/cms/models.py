#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © superliuliuliu1
# File Name: /cms/models.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-11-16 8:51:50 (CST)
# Last Update:
#          By:
# Description:定义后台管理的数据库模型
# **************************************************************************


from .. import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# 定义权限 以二进制形式来定义权限 8位 如果8位全为1代表权限为超级用户  通过位运算可以赋予一个用户以不同的权限
class CMSpower(object):
    # root权限
    ROOTPOWER = 0b11111111
    # 仅能访问后台权限
    VISTOR    = 0b00000001
    # 管理帖子的权限
    FORUM     = 0b00000010
    # 管理评论的权限
    COMMOENT  = 0b00000100
    # 管理板块的权限
    AREA      = 0b00001000
    # 管理前台用户的权限
    FRONTUSER = 0b00010000
    # 管理后台用户的权限
    CMSUSER   = 0b00100000

#定义一个关联表 用来将用户和角色关联起来 对应处理多对多关系
cms_user_role = db.Table(
    'cms_user_role',
    db.Column('cms_role_id', db.Integer, db.ForeignKey('cms_role.id'), primary_key=True),
    db.Column('cms_user_id', db.Integer, db.ForeignKey('cms_user.id'), primary_key=True)
    )

# 定义角色，一个角色可以继承多个权限 ，通过将用户赋予角色从而确定用户的权限,初始化角色权限为访问者
class CMSRole(db.Model):
    __tablename__ = 'cms_role'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(64), nullable = False)
    create_time = db.Column(db.DateTime, default = datetime.now)
    description = db.Column(db.String(100), nullable = True)
    power = db.Column(db.Integer, default = CMSpower.VISTOR)
    users = db.relationship('CMSUser', secondary=cms_user_role, backref='roles')


# 后台管理用户模型
class CMSUser(db.Model):
    __tablename__ = 'cms_user'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(64), nullable = False)
    password_hash = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(64), nullable = False, unique = True)
    join_time = db.Column(db.DateTime, default = datetime.now)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password  #此处会调用setter修饰的函数，将password转换为hash形式并存储到数据库中
        self.email = email

    #对外以password的形式，对内以password_hash的形式
    #property  将类的方法定义成属性的形式,其往往和setter组合使用
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    # setter作用是使其可以通过user.password = 'xxx'的形式来设置密码
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 检验密码
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
