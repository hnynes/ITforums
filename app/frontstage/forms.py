from wtforms import Form, StringField, SubmitField, SelectField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, InputRequired
from wtforms import ValidationError
from ..forms import BaseForm
from utils import mycache
from flask import g

class RegisterForm(BaseForm):
    telephone = StringField(validators=[Regexp(r'1[345789]\d{9}')])
    # 短信验证码
    messagecode = StringField(validators=[Regexp(r'\d{6}')])
    username = StringField(validators=[Regexp(r'.{2,20}', message='请输入正确格式的用户名！')])
    password1 = StringField(validators=[Regexp(r'[0-9a-zA-Z_\.]{6,20}', message='请输入正确格式的密码！')])
    password2 = StringField(validators=[EqualTo("password1", message='两次输入的密码不一致！')])
    # 图形验证码
    picturecode = StringField(validators=[Regexp(r'\w{4}', message="验证码格式不正确！")])

    def validate_messagecode(self, field):
        totest = field.data
        telephone = self.telephone.data
        messagecode = mycache.get(telephone)
        if not messagecode or messagecode != totest:
            raise ValidationError("短信验证码错误！")

    def validate_picturecode(self, field):
        totest = field.data
        picturecode = mycache.get(totest)
        if not picturecode or totest.lower() != picturecode.lower():
            raise ValidationError("图形验证码错误！")

class LoginForm(BaseForm):
    telephone = StringField(validators=[Regexp(r'1[345789]\d{9}')])
    password = StringField(validators=[Regexp(r'[0-9a-zA-Z_\.]{6,20}', message='请输入正确格式的密码！')])
    remember = IntegerField()
