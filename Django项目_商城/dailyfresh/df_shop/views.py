from django.shortcuts import render,HttpResponse
from utils import decorator
from df_shop import models

# Create your views here.

@decorator.check_login
def cart(request):
    """
    购物车主页
    完成度：100%
    功能：
    获取购物车中的商品和商品总数传到前端
    :param request:
    :return:
    """
    user_id = request.session['user_info']['id']
    cart_list = models.ShoppingCart.objects.filter(suser_info_id=user_id).all()
    num = 0     # 商品总数
    for obj in cart_list:
        num += obj.snum
    return render(request,'df_user/cart.html',{'cart':1,'cart_list':cart_list,'num':num})

@decorator.check_login
def add(request):
    """
    购物车的添加商品功能
    完成度：100%
    功能：
    获取用户id和商品id和商品数量添加到数据库，如果数据库存在则只修改数据
    :param request:
    :return:
    """
    if request.method == 'POST':
        uid = request.session['user_info']['id']    # 用户id
        nid = request.POST.get("nid")   # 商品id
        num = request.POST.get("num")   # 商品数量
        obj = models.ShoppingCart.objects.filter(sfresh_info_id=nid,suser_info_id=uid)
        if obj:
            snum = obj.first().snum
            snum = snum + int(num)    # 将原商品数量加上新加的
            obj.update(snum=snum)
        else:
            snum = num
            models.ShoppingCart.objects.create(sfresh_info_id=nid,suser_info_id=uid,snum=snum)
        return HttpResponse(snum)

@decorator.check_login
def edit(request):
    """
    购物车的编辑商品数量功能
    完成度：100%
    功能：
    获取购物车id（购物车表的id）和商品数量修改数据库中的数据
    :param request:
    :return:
    """
    if request.method == "POST":
        shopping_cart_id = request.POST.get('shopping_cart_id')
        num123 = request.POST.get("num123")
        models.ShoppingCart.objects.filter(id=int(shopping_cart_id)).update(snum=int(num123))    # 修改购物车原有的数量
        return HttpResponse('ok')

@decorator.check_login
def delete(request):
    """
    购物车的删除功能
    完成度：100%
    功能：
    获取购物车id（购物车表的id）直接删除，前端局部删除，
    :param request:
    :return:
    """
    if request.method == "POST":
        shopping_cart_id = request.POST.get('shopping_cart_id')
        models.ShoppingCart.objects.filter(id=int(shopping_cart_id)).delete()
        return HttpResponse("ok")

