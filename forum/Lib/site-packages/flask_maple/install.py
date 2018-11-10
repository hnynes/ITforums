#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ********************************************************************************
# Copyright © 2018 jianglin
# File Name: install.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2018-02-22 10:12:59 (CST)
# Last Update: Sunday 2018-03-04 23:03:00 (CST)
#          By:
# Description:
# ********************************************************************************
from flask import render_template, request, redirect, current_app
from os import urandom
import os

DEFAULT_CONFIG = {
    "base": {
        "SECRET_KEY": {
            "alias": "密钥",
            "default": str(urandom(24)),
            "help": ""
        },
        "SECRET_KEY_SALT": {
            "alias": "密钥加盐",
            "default": "",
            "help": ""
        }
    },
    "db": {
        "SQLALCHEMY_DATABASE_URI": {
            "alias": "数据库",
            "default": "",
            "help": ""
        },
        "SQLALCHEMY_TRACK_MODIFICATIONS": {
            "alias": "数据自动更新",
            "default": False,
            "help": ""
        }
    },
    "mail": {
        "MAIL_SERVER": {
            "alias": "邮箱服务器",
            "default": "",
            "help": ""
        },
        "MAIL_PORT": {
            "alias": "邮箱端口",
            "default": 25,
            "help": ""
        },
        "MAIL_USE_TLS": {
            "alias": "邮箱是否使用TLS",
            "default": [True, False],
            "help": ""
        },
        "MAIL_USE_SSL": {
            "alias": "邮箱是否使用SSL",
            "default": [True, False],
            "help": ""
        },
        "MAIL_USERNAME": {
            "alias": "邮箱名",
            "default": "",
            "help": ""
        },
        "MAIL_PASSWORD": {
            "alias": "邮箱密码",
            "default": "",
            "help": ""
        },
        "MAIL_DEFAULT_SENDER": {
            "alias": "默认发送邮箱",
            "default": "",
            "help": ""
        }
    },
    "cache": {
        "CACHE_TYPE": {
            "alias": "缓存类型",
            "default": "",
            "help": ""
        },
        "CACHE_DEFAULT_TIMEOUT": {
            "alias": "缓存超时",
            "default": 60,
            "help": ""
        },
        "CACHE_KEY_PREFIX": {
            "alias": "缓存prefix",
            "default": "",
            "help": ""
        },
        "CACHE_REDIS_HOST": {
            "alias": "redis缓存HOST",
            "default": "",
            "help": ""
        },
        "CACHE_REDIS_PORT": {
            "alias": "redis缓存端口",
            "default": 30,
            "help": ""
        },
        "CACHE_REDIS_PASSWORD": {
            "alias": "redis缓存密码",
            "default": "",
            "help": ""
        },
        "CACHE_REDIS_DB": {
            "alias": "redis缓存数据库",
            "default": 2,
            "help": ""
        },
        "CACHE_NO_NULL_WARNING": {
            "alias": "缓存为空不警告",
            "default": [True, False],
            "help": ""
        },
    }
}


class Install(object):
    def __init__(self, app=None, config=DEFAULT_CONFIG):
        self.app = app
        self.config = config
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.add_url_rule(
            '/install', view_func=self.install, methods=["GET", "POST"])

    def install(self):
        if request.method == "POST":
            data = "\n".join(["{0} = \"{1}\"".format(key, value)
                              for key, value in request.form.items()])
            data = "#!/usr/bin/env python\n# -*- coding: utf-8 -*-\n" + data
            cfg_path = os.path.join(current_app.root_path, os.pardir, 'c.py')
            with open(cfg_path, 'w') as f:
                f.write(data)
            return redirect("/install")
        return render_template('maple/install.html', config=self.config)
