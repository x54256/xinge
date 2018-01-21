from django.shortcuts import render,redirect,HttpResponse
from django import forms
from django.forms import fields,widgets
from io import BytesIO
from web import models
from django.core.exceptions import ValidationError
import time,os

from django.core.validators import RegexValidator

from utils.check_code import create_check_code
class UserForm(forms.Form):
    """
    登录页面的表单验证
    """
    username = fields.CharField(
        widget=widgets.TextInput(attrs={'class':"form-control",'placeholder':"请输入用户名"}),
    )
    password = fields.CharField(
        widget=widgets.PasswordInput(attrs={'class': "form-control", 'placeholder': "请输入密码"}),
    )
    check_code = fields.CharField(
        widget=widgets.TextInput(attrs={'class':"form-control",'placeholder':"请输入验证码",})
    )

class RegisterForm(forms.Form):
    """
    注册页面的表单验证
    """
    username = fields.CharField(
        widget=widgets.TextInput(attrs={'class':"form-control",'placeholder':"请输入用户名"}),
        error_messages={'required':'用户名不能为空'}
    )
    email = fields.CharField(
        widget=widgets.EmailInput(attrs={'class': "form-control", 'placeholder': "请输入邮箱"}),
    )
    password1 = fields.CharField(
        widget=widgets.PasswordInput(attrs={'class': "form-control", 'placeholder': "请输入密码"}),
    )
    password2 = fields.CharField(
        widget=widgets.PasswordInput(attrs={'class': "form-control", 'placeholder': "请输入密码"}),
    )
    check_code = fields.CharField(
        widget=widgets.TextInput(attrs={'class':"form-control",'placeholder':"请输入验证码",})
    )

    # def clean(self):
    #     v1 = self.cleaned_data['password1']
    #     v2 = self.cleaned_data['password2']
    #     if v1 == v2:
    #         print('2')
    #         pass
    #     else:
    #         print('1')
    #         raise ValidationError('用户名或邮箱输入错误')

    # id = fields.CharField(
    #     validators=[RegexValidator(r'^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$', '请输入正确的格式')],
    #     widget=widgets.TextInput(attrs={'class': "form-control", 'placeholder': "请输入身份证号", }),
    #     max_length=18,
    #     min_length=18
    # )


def check_code(request):
    """
    获取生成的验证码
    :param request:
    :return:
    """
    stream = BytesIO()	# 内存读写io
    img, code = create_check_code()
    print(code)
    img.save(stream,'PNG')
    request.session['Check_Code'] = code
    return HttpResponse(stream.getvalue())

def login(request):
    """
    登录页面
    :param request:
    :return:
    """

    errors = ''
    if request.method == 'GET':
        obj = UserForm()
        request.session['before_log'] = request.META.get('HTTP_REFERER', '/')   # 将访问之前的页面记住，登录后跳转到之前的页面
        return render(request,'login.html',{'obj':obj,'errors':errors})
    elif request.method == 'POST':
        obj = UserForm(request.POST)
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        check_code = request.POST.get('check_code')
        checked = request.POST.get('checked')
        user_obj = models.UserInfo.objects.filter(username=user,password=pwd)
        if obj.is_valid():
            if user_obj:
                if check_code.upper() == request.session['Check_Code'].upper():
                    if checked:
                        request.session.set_expiry(value=60*60*24*30)       # 设置超时时间为一个月
                    request.session['is_login'] = True
                    request.session['username'] = user
                    return redirect(request.session['before_log'])
                else:
                    errors = '验证码输入错误'
            else:
                errors = '用户名或密码错误'
            return render(request, 'login.html', {'obj': obj,'errors':errors})

def register(request):
    """
    注册页面
    :param request:
    :return:
    """
    errors = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        check_code = request.POST.get('check_code')
        obj = RegisterForm(request.POST)
        if obj.is_valid():
            user_obj = models.UserInfo.objects.filter(username=username)
            print(user_obj)
            if not user_obj:
                if password2 == password1:
                    if check_code.upper() == request.session['Check_Code'].upper():
                        # 数据库操作
                        dic = {'username':username,'password':password1,'email':email,'user_img':'/static/imgs/avatar/default.png',
                               'follow':0,'fans':0,'task':0,'notic':0,'news':0}
                        models.UserInfo.objects.create(**dic)
                        os.makedirs('static/home/'+username+'/data/')       # 创建用户文件夹
                        os.makedirs('static/home/' + username + '/imgs/')

                        return redirect('login.html')   # 这块就现在这么着把,中间加个过度页面
                    else:
                        errors = '验证码输入错误'
                else:
                    errors = '两次密码输入不一致'
            else:
                errors = '该用户名已存在'
        return render(request, 'register.html', {'obj': obj,'errors':errors})
    elif request.method == 'GET':
        obj = RegisterForm()
        return render(request,'register.html',{'obj':obj})

def exit(request):
    """
    退出，清除session
    :param request:
    :return:
    """
    request.session.clear()
    return redirect('/')
