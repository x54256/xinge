from django.shortcuts import render,HttpResponse,redirect
from df_user import models
from df_order import models as order_models
from df_home import models as home_models
from df_user.forms.address import LoginForm
import json
from utils import decorator,pagination

# Create your views here.
"""
    个人中心（主页）
"""

@decorator.check_login
def info(request):
    """
    个人主页页面
    查看基本信息，和最近浏览信息
    :param request:
    :return:
    """
    uname = request.session['user_info']['uname']
    addr_obj = models.UserAddr.objects.filter(user_info__uname=uname,current_addr=True).first()
    if addr_obj:
        currentaddr = addr_obj.uaddress
    else:
        currentaddr = "你还没有设置默认收货地址"
    recently_str = request.COOKIES.get('recently_browse','')    # cookie中str.
    obj_list = []
    if recently_str != '':
        recently_list = recently_str.split(',')     # 切割成[]
        for i in recently_list:
            obj_list.append(home_models.FreshInfo.objects.get(id=int(i)))    # 将最浏览的商品添加到商品信息列表中
    return render(request,'df_user/user_center_info.html',{'user':1,'currentaddr':currentaddr,'obj_list':obj_list,'title':'天天生鲜-用户中心'})

@decorator.check_login
def order(request,**kwargs):
    """
    订单页面
    管理用户的订单
    :param request:
    :param kwargs:
    :return:
    """
    uid = request.session['user_info']['id']
    order_list = order_models.OrderInfo.objects.filter(ouser_id=uid)
    pid = kwargs['pid']
    page_obj = pagination.Pagination(pid, 0, 0, len(order_list))
    data = order_list[page_obj.start:page_obj.end]
    page_str = page_obj.page_str('/user/order/')

    return render(request,'df_user/user_center_order.html',{'user':1,'order_list':data,"page_str":page_str,'title':'天天生鲜-用户中心'})

@decorator.check_login
def site(request):
    """
    收货地址页面
    用于设置默认收货地址，添加修改收货地址
    :param request:
    :return:
    """

    uname = request.session['user_info']['uname']
    if request.method == 'GET':
        addr_obj = models.UserAddr.objects.filter(user_info__uname=uname,current_addr=True).first()     # 取出默认收货地址
        all_addrs = models.UserAddr.objects.filter(user_info__uname=uname,current_addr=False)  # QuerySet[obj,obj,...]，其他所有收货地址
        return render(request,'df_user/user_center_site.html',{'user':1,'currentaddr':addr_obj,'addrs_list':all_addrs,'title':'天天生鲜-用户中心'})
    elif request.method == 'POST':
        obj = LoginForm(request.POST)     # 去form表单验证
        result = {'status':False,'error_receiver':None,'error_address':None,'error_phone':None}   # 保存错误信息
        if obj.is_valid():
            result['status'] = True
            ureceiver = request.POST.get('ureceiver')
            uaddress = request.POST.get('uaddress')
            uphone = request.POST.get('uphone')
            uid = models.UserInfo.objects.get(uname=uname).id
            models.UserAddr.objects.create(ureceiver=ureceiver,uaddress=uaddress,uphone=uphone,user_info_id=uid)
        else:
            errors = obj.errors
            if 'ureceiver' in errors:
                result['error_receiver'] = errors['ureceiver'][0]
            if 'uaddress' in errors:
                result['error_address'] = errors['uaddress'][0]
            if 'uphone' in errors:
                result['error_phone'] = errors['uphone'][0]

        return HttpResponse(json.dumps(result))











