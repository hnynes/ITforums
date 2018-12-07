#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © superliuliuliu1
# File Name: manage.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-12-07 12:54:50 (CST)
# Last Update:
#          By:
# Description: 前端生成验证码 发送短信验证码  上传图片到七牛等功能
# **************************************************************************


from flask import Blueprint, render_template, request, make_response, jsonify
from utils.picture import Captcha
from io import BytesIO
from utils import aliyunmessage, restful, mycache
import string
import random
from .forms import SendmessageForm
from ..frontstage.models import FrontUser
from qiniu import Auth, put_file
from config import config

bp = Blueprint('common', __name__, url_prefix='/common')

@bp.route('/')
def index():
    return 'common page'

@bp.route('/picture/')
def growpicture():
    text, image = Captcha.gene_graph_captcha()
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    p = make_response(out.read())
    p.content_type = "image/png"
    # 存储图形验证码内容到memached中
    mycache.set(text.lower(), text.lower())
    return p

# 防止受到攻击 对调用短信接口进行加密操作  这次采用post的方式来发送验证码
# 加密操作的原理 是让前台在向后端服务器发送手机号码数据时，要加上其他的信息 比如时间戳等(当然更安全的是采取一些加密机制防止爬虫) 只有这些信息检验正确时才会调用短信接口去执行相应的操作
@bp.route('/sendmessage/', methods=['POST'])
def sendmessage():
    form = SendmessageForm(request.form)
    if form.validate():
        source = list(map(lambda x: str(x), range(0, 10)))
        code = "".join(random.sample(source, 6))
        phonenumber = form.telephone.data
        testphone = FrontUser.query.filter_by(telephone=phonenumber).first()
        if testphone:
            return restful.args_error("此手机号已注册过账号，请检查或者去登录！")
        if aliyunmessage.send_sms(phone_numbers = phonenumber, code = code):
            # 将验证码存储到memached中
            mycache.set(phonenumber, code)
            return restful.success()
        else:
            return restful.args_error("短信验证码发送失败")
    else:
        return restful.args_error("参数错误")


# 生成登录七牛云需要使用的token  在这里选择返回json形式的数据 因为在前端需要用到
@bp.route('/uptoken/')
def uptoken():
    #需要填写你的 Access Key 和 Secret Key 这里通过类来加载
    access_key = config['development'].QINIUACCESSKEY
    secret_key = config['development'].QINIUACCESSKEYSECRET
    #构建鉴权对象
    q = Auth(access_key, secret_key)
    #要上传的空间
    bucket_name = 'forumfor'
    token = q.upload_token(bucket_name)
    return jsonify({'uptoken':token})
