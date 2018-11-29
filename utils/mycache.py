#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © superliuliuliu1
# File Name: mycached.py
# Author: superliuliuliu1
# Email: superliuliuliu1@gmail.com
# Created: 2018-11-23 19:48:50 (CST)
# Last Update:
#          By:
# Description:
# **************************************************************************
import memcache
cache = memcache.Client(['127.0.0.1:15000'], debug=True)


# 设置缓存的函数，默认过期时间1分钟
def set(key=None, value=None, timeout=120):
    if key and value:
        result = cache.set(key, value, timeout)
        return result
    return False


# 从缓存中获取数据
def get(key=None):
    if key:
        return cache.get(key)
    return None


# 删除缓存
def delete(key=None):
    if key:
        cache.delete(key)
        return True
    return False
