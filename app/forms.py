#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright ©
# File Name: forms.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-11-10 16:03:50 (CST)
# Last Update:
#          By:
# Description:论坛系统中用到的表单
# **************************************************************************


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class Nameform(FlaskForm):
    name = StringField(description='What is your name?', validators=[DataRequired()])
    submit = SubmitField('提交')
