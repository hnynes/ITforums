#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © superliuliuliu1
# File Name: models.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-11-11 10:12:50 (CST)
# Last Update:
#          By:
# Description:数据库用来存储轮播图的相关信息
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
