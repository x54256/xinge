from django.shortcuts import render,redirect,HttpResponse
from hashlib import sha1
from df_user import models
from df_user.forms.account import RegisterForm,LoginForm
import json

# Create your views here.
"""
    登录、注册、注销登录页面
"""
def register(request):
    """
    页面信息：注册页面
    完成度：100%
    功能：
    前端通过ajax的方式提交过来request
    将request放到form表单中验证
    如果验证通过，将数据保存进mysql数据库，返回True跳转到login页面
    失败返回错误信息
    前端有JavaScript的错误验证，后端再次验证一遍
    :param request:
    :return:
    """
    if request.method == "GET":
        return render(request, 'df_user/register.html', {"title": "天天生鲜-注册"})
    elif request.method == 'POST':
        print(request.POST)
        obj = RegisterForm(request.POST)    # 将数据拿到form表单中验证
        result = {'status': False, 'error_username': None,'error_pwd': None,'error_email': None,'error_2': None}    # 是否通过验证，错误信息
        if obj.is_valid():
            cleaned_data = obj.clean()    # {'user_name': '12345687', 'pwd': '123456789', 'email': '123@qq.com'}
            # 获取前端传来的值
            uname = request.POST.get("user_name")
            upwd = request.POST.get("pwd")
            uemail = request.POST.get("email")

            # 加密用户的密码
            s1 = sha1()
            s1.update(upwd.encode('utf-8'))
            upwd3 = s1.hexdigest()
            models.UserInfo.objects.create(uname=uname, upwd=upwd3, uemail=uemail)  # 储存数据
            result['status'] = True

        else:
            errors = obj.errors     # 获取错误信息
            if 'user_name' in errors:
                result['error_username'] = errors['user_name'][0]
            if 'pwd' in errors:
                result['error_pwd'] = errors['pwd'][0]
            if 'cpwd' in errors:
                result['error_2'] = errors['cpwd'][0]
            if 'email' in errors:
                result['error_email'] = errors['email'][0]
        return HttpResponse(json.dumps(result))

def login(request):
    """
    页面信息：登录页面
    完成度：100%
    功能：
    前端通过ajax的方式提交过来request
    将request放到form表单中验证
    如果验证通过，将数据保存到session中，
    如果勾选了rmb30天，将session过期时间设置成30天，
    然后返回True跳转到login页面
    如果失败返回错误信息
    :param request:
    :return:
    """
    if request.method == 'GET':
        request.session['before_log'] = request.META.get('HTTP_REFERER', '/')  # 将访问之前的页面记住，登录后跳转到之前的页面
        # request.get_full_path()获取完整地址(有参数)，request.path
        return render(request, 'df_user/login.html', {'title': '天天生鲜-登录'})
    elif request.method == "POST":
        obj = LoginForm(request.POST)
        result = {'status':False,'error_user':None,'error_pwd':None,'data':None}   # 保存错误信息
        if obj.is_valid():
            result['status'] = True
            rmb = request.POST.get("rmb")   # 是否勾选了rmb30天
            user_dic = models.UserInfo.objects.values('id','uname', 'uemail').first()  # 将当前user的信息取出，放到session中
            request.session['user_info'] = user_dic
            if rmb:
                request.session.set_expiry(60 * 60 * 24 * 30)   # 如果勾选了rmb，则将session的过期时间设置成30天
            result['data'] = request.session.get('before_log')

        else:
            errors = obj.errors
            if 'username' in errors:
                result['error_username'] = errors['username'][0]
            if 'pwd' in errors:
                result['error_pwd'] = errors['pwd'][0]
            if '__all__' in errors:
                result['error_pwd'] = errors['__all__'][0]
        return HttpResponse(json.dumps(result))

def logout(request):
    """
    退出登录
    :param request:
    :return:
    """
    request.session.clear()     # 将session清除
    return redirect(request.META.get('HTTP_REFERER', '/'))    # 返回之前的页面





