from django.shortcuts import render,HttpResponse,redirect
from django.utils.safestring import mark_safe
from  utils import pagination

import json
# Create your views here.

from cmdb import models

def login(request):
    if request.method == 'GET':
        return render(request,'login.html')

    elif request.method == 'POST':
        ret={'static':True,'error123':None,'data123':None}

        u = request.POST.get('username')
        p = request.POST.get('password')
        print(u,p)
        obj = models.UserInfo.objects.filter(username=u).first()
        try:
            if u:
                if p:
                    if obj:
                        if p == obj.password:
                            erro_dic = json.dumps(ret)
                            res = HttpResponse(erro_dic)
                            res.set_cookie('username111',u)
                            userid = obj.id
                            res.set_cookie('uid',userid)
                            print('123safsdv')
                            return res
                        else:
                            ret['static']=False
                            ret['error123']='密码输入错误'
                    else:
                        ret['static'] = False
                        ret['error123'] = '账号输入错误'
                else:
                    ret['static'] = False
                    ret['error123'] = '请输入密码'
            else:
                ret['static'] = False
                ret['error123'] = '请输入用户名'
            erro_dic = json.dumps(ret)
            return HttpResponse(erro_dic)
        except Exception as e:
            ret['stactic']=False
            ret['error']='其他错误'


def auth(func):
    def inner(reqeust,*args,**kwargs):
        v = reqeust.COOKIES.get('username111')
        if not v:
            return redirect('/login/')
        return func(reqeust, *args,**kwargs)
    return inner


@auth
def index(request):
        v = request.COOKIES.get('username111')
        uid = request.COOKIES.get('uid')
        print(v)
    # if v:
        if request.method == 'GET':
            obj = models.UserInfo.objects.filter(username=v).first()
            group_host_list = []
            host_obj = obj.h.all()
            group_obj = obj.g.all()
            for i in host_obj:
                group_host_list.append(i)

            for i in group_obj:
                group_id = i.gid
                obj2 = models.Host.objects.filter(hostgroup_id=group_id)
                for i in obj2:
                    group_host_list.append(i)
            LIST= group_host_list
            current_page = request.GET.get('p', 1)  # 1是干嘛的 ==> 第一次请求的时候默认看第一页
            current_page = int(current_page)
            page_obj = pagination.Page(current_page, len(LIST),5)
            data = LIST[page_obj.start:page_obj.end]
            page_str = page_obj.page_str("/index/")


            return render(request, 'index.html', { 'page_str': page_str,'current_user':v,'group_host_list': data, 'group_obj':group_obj})

        elif request.method == 'POST':
            gid = request.POST.get('gid')
            hid = request.POST.get('hid')

            try:
                # obj.g.remove(gid)
                obj = models.Host.objects.filter(hid=hid)
                print(obj)      # <QuerySet [<Host: Host object>]>
                obj.update(hostgroup_id=None)
            except Exception as e:
                print('123')
            else:
                obj = models.UserInfo.objects.get(id=uid)  # get和filter出来的对象还不一样 666
                print(obj)   # UserInfo object
                obj.h.remove(hid)
            return HttpResponse(123)
        # else:
        #     return redirect('/login/')

@auth
def edit(request):
    v = request.COOKIES.get('username111')
    uid = request.COOKIES.get('uid')
    hid = request.COOKIES.get('hid')
    hostgroup_id = request.COOKIES.get('hostgroup_id')  #不可以修改组的id只能修改信息
    host_name = request.COOKIES.get('host_name')
    ip = request.COOKIES.get('ip')
    port = request.COOKIES.get('port')

    if request.method == 'GET':
        result = "<p><input type='text' name='hid' value='%s' style='display:none'/></p>" \
                 "<p>主机名：<input type='text' name='host_name' value='%s' /></p>" \
                 "<p>IP地址：<input type='text' name='ip' value='%s' /></p>" \
                 "<p>端口号：<input type='text' name='port' value='%s' /></p>" \
                 "<p><input type='submit'/></p>"%(hid,host_name,ip,port)

        host_info = mark_safe(result)

        return render(request,'edit.html',{'host_info':host_info})
    elif request.method == 'POST':
        obj = models.Host.objects.filter(hid=hid)
        host_name2 = request.POST.get('host_name')
        ip2 = request.POST.get('ip')
        port2 = request.POST.get('port')
        obj.update(host_name=host_name2,ip=ip2,port=port2)
        return redirect('/index/')

@auth
def add(request):
    v = request.COOKIES.get('username111')
    uid = request.COOKIES.get('uid')
    blest=''
    if request.method == 'POST':
        u = request.POST.get('user')
        p = request.POST.get('pwd')
        h = request.POST.getlist('host_list')
        g = request.POST.getlist('group_list')
        print(g)
        obj = models.UserInfo.objects.create(username=u,password=p)
        obj.h.add(*h)
        obj.g.add(*g)
        blest = '用户添加成功'


    host_list = models.Host.objects.all()
    group_list = models.Host_Group.objects.all()

    return render(request,'add.html',{'current_user':v,'host_list':host_list,'group_list':group_list,'blest':blest})




def exit(request):
    v = request.COOKIES.get('username111')
    res = redirect('/login/')
    import datetime
    current_date = datetime.datetime.utcnow()
    res.set_cookie('username111',v,expires=current_date)
    return res

















