#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright ©
# File Name: mail.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-11-10 16:22:01 (CST)
# Last Update:
#          By:
# Description:注册账号时用到的发送邮件功能，暂时还未实现验证码，只是简单的邮件通知
# **************************************************************************

from . import mail
from threading import Thread
from flask import current_app, render_template
from flask_mail import Message

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

#收件人地址、主题、渲染邮件正文的模板和关键字参数列表
def send_mail(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, sender = app.config['FLASKY_MAIL_SENDER'], recipients = [to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=(app, msg))
    thr.start()
    return thr

# 发送注册确认邮件
def send_confirm_email(user, token):
    send_mail(to = user.email, subject = app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + 'Email Confirm', template = 'authority/email/confirm', user=user, token=token)

# 发送重置密码邮件
def send_reset_eamil(user, token):
    send_mail(to = user.email, subject = app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + 'Reset password', template = 'authority/email/repassword', user=user, token=token)
