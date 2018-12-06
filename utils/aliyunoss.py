# -*- coding: utf-8 -*-

import os
import shutil
import oss2
# from config import config


# 以下代码展示了基本的文件上传、下载、罗列、删除用法。


# 首先初始化AccessKeyId、AccessKeySecret、Endpoint等信息。
# 通过环境变量获取，或者把诸如“<你的AccessKeyId>”替换成真实的AccessKeyId等。
#
# 以杭州区域为例，Endpoint可以是：
#   http://oss-cn-hangzhou.aliyuncs.com
#   https://oss-cn-hangzhou.aliyuncs.com
# 分别以HTTP、HTTPS协议访问。
access_key_id = 'LTAIWzOzpEYTIHIN'
access_key_secret = 'hOb8gy9gadIE84MkQhfcQKTrTnoAp9'
bucket_name = 'forumfor'
endpoint = 'https://oss-cn-beijing.aliyuncs.com'


# 确认上面的参数都填写正确了
for param in (access_key_id, access_key_secret, bucket_name, endpoint):
    assert '<' not in param, '请设置参数：' + param


# 创建Bucket对象，所有Object相关的接口都可以通过Bucket对象来进行
bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)


# 上传本地图片
def upload_picture(pathfile):
    with open(pathfile, 'rb') as fileobj:
        bucket.put_object(pathfile, fileobj)
# 上传一段字符串。Object名是motto.txt，内容是一段名言。
