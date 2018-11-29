from flask import Blueprint, render_template, request, make_response
from utils.picture import Captcha
from io import BytesIO
from utils import aliyunmessage, restful
import string
import random

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
    return p

@bp.route('/sendmessage/')
def sendmessage():
    phonenumber = request.args.get('telephone')
    if not phonenumber:
        # 如果没有输入手机号码就点击发送验证码 则提示输入手机号
        return restful.args_error("请输入手机号码")
    else:
        # 验证码为随机生成的6位数字
        source = list(map(lambda x: str(x), range(0, 10)))
        code = "".join(random.sample(source, 6))
        if aliyunmessage.send_sms(phone_numbers = phonenumber, code = code):
            return restful.success()
        else:
            return restful.args_error("短信验证码发送失败")
