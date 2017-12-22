from django.shortcuts import render,HttpResponse
from df_shop import models as shop_models
from df_user import models as addr_models
from df_home import models as goods_models
from df_order import models
from django.db import transaction
from utils import decorator

# Create your views here.

@decorator.check_login
def submit(request):
    uid = request.session['user_info']['id']
    if 'cart_id' in request.get_full_path():
        cart_id = request.GET.get("cart_id")
        if cart_id:
            cart_id_list = cart_id.split('-')
            obj_list = shop_models.ShoppingCart.objects.filter(id__in=cart_id_list)    # 查询购物车表中id在传来的url的
            addr = addr_models.UserAddr.objects.filter(user_info_id=uid,current_addr=True).first()

            return render(request,'df_user/place_order.html',{'order':1,'obj_list':obj_list,'addr':addr})
    elif 'goods_id' in request.get_full_path():
        goods_id = request.GET.get("goods_id")
        num = request.GET.get("num")
        if goods_id:
            obj = goods_models.FreshInfo.objects.filter(id=goods_id).first()
            addr = addr_models.UserAddr.objects.filter(user_info_id=uid,current_addr=True).first()
            return render(request, 'df_user/place_order2.html', {'order': 1, 'obj': obj, 'addr': addr,'num':num})

@decorator.check_login
def handler(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # 创建订单信息
                shopcar_list = request.POST.getlist("shopcar_list")
                oaddr = request.POST.get("uaddr")
                ototal = request.POST.get("price")
                ouser_id = request.session['user_info']['id']
                oorder_id = models.OrderInfo.objects.create(ouser_id=ouser_id,ototal=ototal,oaddr=oaddr).id   # 获取创建的订单的id
                # 创建订单与商品的联系
                obj_list = shop_models.ShoppingCart.objects.filter(id__in=shopcar_list)  # 查询购物车表中id在传来的list中的
                ototal_new = 0    # 我们自己在算一下价格，更新数据库中total的值
                for i in obj_list:
                    ogoods_id = i.sfresh_info_id    # 每件商品的id
                    ocount = i.snum     # 每件商品购买的数量
                    oprice = round(ocount*i.sfresh_info.fprice,2)    # 每件商品的小计
                    ototal_new += oprice
                    models.OrderDetailInfo.objects.create(ogoods_id=ogoods_id,oorder_id=oorder_id,ocount=ocount,oprice=oprice)  # 创建订单与商品的关联（多对多）
                models.OrderInfo.objects.filter(id=oorder_id).update(ototal=ototal_new)
                obj_list.delete()
                return HttpResponse(1)

        except Exception as e:
            print('=====================',e)
            return HttpResponse(0)\

@decorator.check_login
def handler2(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # 创建订单信息
                ogoods_id = request.POST.get("goods_id")
                oaddr = request.POST.get("uaddr")
                num = request.POST.get("num")    # 购买数量
                fprice = goods_models.FreshInfo.objects.get(id=ogoods_id).fprice     # 获取商品价格
                ototal = int(num) * fprice      # 商品总价
                ouser_id = request.session['user_info']['id']
                oorder_id = models.OrderInfo.objects.create(ouser_id=ouser_id,ototal=ototal,oaddr=oaddr).id   # 获取创建的订单的id
                # 创建订单与商品的联系（多对多）
                models.OrderDetailInfo.objects.create(ogoods_id=ogoods_id,oorder_id=oorder_id,ocount=num,oprice=ototal)
                return HttpResponse(1)

        except Exception as e:
            print('=====================',e)
            return HttpResponse(0)
