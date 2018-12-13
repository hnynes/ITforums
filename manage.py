#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © superliuliuliu1
# File Name: manage.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-11-10 16:42:50 (CST)
# Last Update:
#          By:
# Description:
# **************************************************************************

import os
from app import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app.models import Carousel, Area, Post
from app.frontstage import models as front_models
from app.cms import models as cms_models


app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)

CMSUser = cms_models.CMSUser
CMSRole = cms_models.CMSRole
CMSpower = cms_models.CMSpower

FrontUser = front_models.FrontUser

manager.add_command('db', MigrateCommand)

# 利用命令行来生成后台用户
@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-e','--email',dest='email')
def create_cms_user(username,password,email):
    user = CMSUser(username=username,password=password,email=email)
    db.session.add(user)
    db.session.commit()
    print(u'cms用户添加成功！')

# 利用命令行的形式生成一系列的角色，并为角色分配相应的权限
@manager.command
def create_role():
    # visitor角色, 其权限不用修改应为权限默认即为CMSpower.VISTOR
    Visitor = CMSRole(name = "Visitor", description="访问者角色，能够浏览后台管理系统并修改个人信息，但不能执行其他操作，比如删除帖子")

    # 普通管理员，能够管理帖子、评论、前台用户
    Admin = CMSRole(name = "Admin", description="在浏览者的基础之上增加了管理帖子、评论、前台用户的权限")
    Admin.power = CMSpower.VISTOR | CMSpower.FRONTUSER | CMSpower.COMMOENT | CMSpower.FORUM

    # leader ,拥有除了管理管理员的所有权限
    Leader = CMSRole(name="Leader", description="Leader")
    Leader.power = CMSpower.VISTOR | CMSpower.CMSUSER | CMSpower.COMMOENT | CMSpower.FORUM | CMSpower.FRONTUSER | CMSpower.AREA

    # 超级管理员
    Root = CMSRole(name = "Root", description="超级管理员，拥有所有权限")
    Root.power = CMSpower.ROOTPOWER

    db.session.add_all([Visitor, Admin, Leader, Root])
    db.session.commit()

# 生成测试帖子，以测试前端的设计效果
@manager.command
def create_testpost():
    # 执行一次生成20篇测试帖子
    for i in range(2, 20):
        theme = "测试帖子%s" %i
        content = "这只是测试数据，后期会删除 %s" %i
        area = Area.query.first()
        author = FrontUser.query.first()
        post = Post(theme=theme, content=content)
        post.area = area
        area.number = area.number + 1
        post.author = author
        db.session.add(post)
        db.session.commit()
    print("测试数据添加完成")

# 为用户分配权限
@manager.option('-e','--email',dest='email')
@manager.option('-n','--name',dest='name')
def add_user2_role(email, name):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
        else:
            print("不存在这个角色：%s" %name)
    else:
        print("不存在这个用户：%s" %email)

# 命令行的形式增加前台用户
@manager.option('-t', '--telephone', dest='telephone')
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--eamil', dest='email')
def add_front_user(telephone, username, password, email):
    user = FrontUser(telephone = telephone, username = username, password = password, email = email)
    db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    manager.run()
