#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ********************************************************************************
# Copyright © superliuliuliu1
# File Name: restful.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-11-21 22:48:50 (CST)
# Last Update:
#          By:
# Description:基于Flask-restful包实现自己的restful封装  主要目的是为了确定返回码的含义
# ********************************************************************************

from flask import jsonify

class MessageCode:
    ok = 200
    autherror = 401 #权限错误
    argserror = 400 #参数错误
    Internalerror = 500 #服务器内部错误

def restful_result(code, message, data):
    return jsonify({"code": code, "message": message, "data": data})

def success(message = "", data = None):
    return restful_result(code=MessageCode.ok, message=message, data=data)

def args_error(message = ""):
    return restful_result(code=MessageCode.argserror, message=message, data=None)

def auth_error(message = ""):
    return restful_result(code=MessageCode.autherror, message=message, data=None)

def internal_error(message = ""):
    return restful_result(code=MessageCode.Internalerror, message=message, data = None)
