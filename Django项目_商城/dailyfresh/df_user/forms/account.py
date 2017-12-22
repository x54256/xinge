from django.forms import Form
from django.forms import widgets
from django.forms import fields
import re
from django.core.exceptions import ValidationError
from df_user import models
from hashlib import sha1

"""
    登录注册的form表单验证
"""

class RegisterForm(Form):
    user_name = fields.CharField(
        max_length=20,
        min_length=5,
        error_messages = {'required':"用户名不能为空",'max_length':"请输入5-20个字符的用户名",'min_length':"请输入5-20个字符的用户名"}
    )

    pwd = fields.CharField(
        max_length=20,
        min_length=8,
        error_messages={'required':"密码不能为空",'max_length':"密码最少8位，最长20位",'min_length':"密码最少8位，最长20位"}
    )
    cpwd = fields.CharField(

    )

    email = fields.CharField(
        error_messages={'required': '邮箱不能为空'}
    )

    # 自定义错误验证
    def clean_email(self):
        try:    # 如果相应值为空会raise KeyError的错误
            pattern = re.compile(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$')
            value = self.cleaned_data['email']
            if not pattern.search(value):
                raise ValidationError('邮箱格式输入错误')
        except:
            raise ValidationError('邮箱格式输入错误')

    def clean_cpwd(self):
        try:
            pwd = self.cleaned_data['pwd']
            pwd2 = self.cleaned_data['cpwd']
            if pwd != pwd2:
                raise ValidationError('两次密码输入不一致')
        except:
            raise ValidationError('两次密码输入不一致')

    def clean_user_name(self):
        try:
            username = self.cleaned_data['user_name']
            if models.UserInfo.objects.filter(uname=username).first():
                raise ValidationError('该用户名已被使用')
        except:
            raise ValidationError('该用户名已被使用')

class LoginForm(Form):
    username = fields.CharField(
        error_messages={"required":'用户名不能为空'}
    )
    pwd = fields.CharField(
        error_messages={"required":'密码不能为空'}
    )
    def clean(self):
        try:
            uname = self.cleaned_data['username']
            upwd = self.cleaned_data['pwd']
            s1 = sha1()
            s1.update(upwd.encode("utf-8"))
            upwd = s1.hexdigest()
            if not models.UserInfo.objects.filter(uname=uname,upwd=upwd):
                raise ValidationError('用户名或密码输入不正确')
        except:
            raise ValidationError('用户名或密码输入不正确')
