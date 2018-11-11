#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © superliuliuliu1
# File Name: ~/main_blue/views.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-11-10 15:45:40 (CST)
# Last Update:
#          By:
# Description:错误处理程序  在蓝本中编写错误处理程序稍有不同，若使用errorhandler修饰，
# 则只能由蓝本中的错误来触发错误处理程序，若想注册应用于全局的错误处理程序，
# 需要用app_errorhandler来修饰
# **************************************************************************

from flask import Flask, render_template, session, url_for, redirect, flash, current_app
from .. import db
from ..models import Role, User
from ..mail import send_mail
from . import main
from ..forms import Nameform



@main.route('/', methods=['GET', 'POST'])
def index():
    app = current_app._get_current_object()
    form = Nameform()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user is None:
            user = User(name=form.name.data)
            db.session.add(user)
            #db.session.commit()
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                send_mail(app.config['FLASKY_ADMIN'], 'NEW USER', 'mail/newuser', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('main.index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False))
