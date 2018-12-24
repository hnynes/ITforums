#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © superliuliuliu1
# File Name: models.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-11-11 10:12:50 (CST)
# Last Update:2018-12-9
#          By:
# Description:为了实现全站搜索功能向数据库模型中增加索引
# **************************************************************************
from . import db
from datetime import datetime


class Carousel(db.Model):
    __tablename__ = 'Carousel'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(256), nullable = False)
    picture_url = db.Column(db.String(256), nullable = False)
    next_url = db.Column(db.String(256), nullable = False)
    weight = db.Column(db.Integer, default = 0)
    create_time = db.Column(db.DateTime, default = datetime.now)


class Area(db.Model):
    __tablename__ = 'area'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(256), nullable = False, unique = True, index = True)
    number = db.Column(db.Integer, default = 0)
    create_time = db.Column(db.DateTime, default = datetime.now)


class Post(db.Model):
    __tablename__ = 'Post'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    theme = db.Column(db.String(150), nullable = False, unique = True, index = True) #帖子的主题
    content = db.Column(db.Text, nullable = False)     #帖子的内容
    create_time = db.Column(db.DateTime, default = datetime.now)
    area_id = db.Column(db.Integer, db.ForeignKey("area.id")) # 外键
    author_id = db.Column(db.String(64), db.ForeignKey("front_user.id"))
    author = db.relationship('FrontUser', backref = 'posts')
    area = db.relationship('Area', backref = 'posts')    #定义版块和帖子的双向关系,即使area拥有posts属性能够查看版块下所含的帖子


# 新建一个数据库表单用来记录帖子的加精时间
class Plusfine(db.Model):
    __tablename__ = 'fineforums'
    id = id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    post_id = db.Column(db.Integer, db.ForeignKey("Post.id"))
    create_time = db.Column(db.DateTime, default = datetime.now)
    post = db.relationship('Post', backref = 'plusfine')


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    content = db.Column(db.Text, nullable = False )
    create_time = db.Column(db.DateTime, default = datetime.now)
    author_id = db.Column(db.String(64), db.ForeignKey("front_user.id"))
    author = db.relationship('FrontUser', backref = 'comments')
    post_id = db.Column(db.Integer, db.ForeignKey("Post.id"))
    post = db.relationship('Post', backref = 'comments')
