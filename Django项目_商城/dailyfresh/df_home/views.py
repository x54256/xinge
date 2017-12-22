from django.shortcuts import render,redirect,HttpResponse
from df_home import models
from df_shop import models as shop_models
from  utils import pagination

# Create your views here.
"""
    网站主页
    各个分类主页
"""

def index(request):
    """
    网站的主页
    完成度：100%
    功能：
    从数据库中取出各个各类的点击量最高和最近更新的4个数据发送到前端
    :param request:
    :return:
    """
    typelist = models.FreshType.objects.all()   # 查出所有的类型
    type1_new = typelist[0].freshinfo_set.order_by('-id')[0:4]     # 按照更新时间（id的倒序）排列取出前4个
    type1_hot = typelist[0].freshinfo_set.order_by('fclick')[0:4]   # 按点击量排序，取前4个
    type2_new = typelist[1].freshinfo_set.order_by('-id')[0:4]     # 按照更新时间（id的倒序）排列取出前4个
    type2_hot = typelist[1].freshinfo_set.order_by('fclick')[0:4]   # 按点击量排序，取前4个
    type3_new = typelist[2].freshinfo_set.order_by('-id')[0:4]     # 按照更新时间（id的倒序）排列取出前4个
    type3_hot = typelist[2].freshinfo_set.order_by('fclick')[0:4]   # 按点击量排序，取前4个
    type4_new = typelist[3].freshinfo_set.order_by('-id')[0:4]     # 按照更新时间（id的倒序）排列取出前4个
    type4_hot = typelist[3].freshinfo_set.order_by('fclick')[0:4]   # 按点击量排序，取前4个
    type5_new = typelist[4].freshinfo_set.order_by('-id')[0:4]     # 按照更新时间（id的倒序）排列取出前4个
    type5_hot = typelist[4].freshinfo_set.order_by('fclick')[0:4]   # 按点击量排序，取前4
    type6_new = typelist[5].freshinfo_set.order_by('-id')[0:4]     # 按照更新时间（id的倒序）排列取出前4个
    type6_hot = typelist[5].freshinfo_set.order_by('fclick')[0:4]   # 按点击量排序，取前4个

    try:
        user_id = request.session['user_info']['id']
        cart_list = shop_models.ShoppingCart.objects.filter(suser_info_id=user_id).all()
        num = 0  # 商品总数
        for obj in cart_list:
            num += obj.snum
    except:
        num=0

    type_dic = {'title':'天天生鲜-首页','home':1,'type1_new':type1_new,'type1_hot':type1_hot,'type2_new':type2_new,'type2_hot':type2_hot,'type3_new':type3_new,'type3_hot':type3_hot,'type4_new':type4_new,'type4_hot':type4_hot,'type5_new':type5_new,'type5_hot':type5_hot,'type6_new':type6_new,'type6_hot':type6_hot,'num':num}
    return render(request,'df_home/index.html',type_dic)

def list(request,*args,**kwargs):
    """
    各个分类的主页
    完成度：100%
    功能：
    从数据库中取出各个各类的点击量最高的2个和相应标签的数据发送到前端
    :param request:
    :param args:
    :param kwargs: nid ==> 当前排序方式，tid ==> 当前类别，pid ==> 当前页
    :return:
    """
    try:
        type_obj = models.FreshType.objects.filter(id=kwargs['tid']).first()
        new_list = type_obj.freshinfo_set.order_by("-id")[0:2]    # 取出当前类最新的两件商品
        if kwargs['nid'] == '1':
            goods_list = type_obj.freshinfo_set.order_by("-id")     # 按更新时间排序
        elif kwargs['nid'] == '2':
            goods_list = type_obj.freshinfo_set.order_by('fprice')  # 按价格（低）排序
        elif kwargs['nid'] == '3':
            goods_list = type_obj.freshinfo_set.order_by('-fclick')  # 按点击率排序

        page_obj = pagination.Pagination(int(kwargs['pid']),int(kwargs['nid']),int(kwargs['tid']), len(goods_list))
        data = goods_list[page_obj.start:page_obj.end]
        page_str = page_obj.page_str("/")

        try:
            user_id = request.session['user_info']['id']
            cart_list = shop_models.ShoppingCart.objects.filter(suser_info_id=user_id).all()
            num = 0  # 商品总数
            for obj in cart_list:
                num += obj.snum
        except:
            num=0

        return render(request,'df_home/list.html',{'title':'天天生鲜-商品列表','type_name':type_obj.ttitle,"data":data,"page_str":page_str,'new_list':new_list,'home':1,'kwargs':kwargs,'num':num})
    except:
        return HttpResponse('404页面')

def detail(request,*args,**kwargs):
    """
    商品的详细信息
    完成度：80%   立即购买+购物车没做
    功能：
    从数据库中取出各个各类的最新的2个和当前商品信息，增加点击量
    :param request:
    :param args:
    :param kwargs: { condition:"(firut)|(seafood)|(meat)|(egg)|(vegetables)|(freeze))",nid:商品的id}
    :return:
    """
    goods_info_obj = models.FreshInfo.objects.filter(id=kwargs['nid'])
    new_click = goods_info_obj.first().fclick + 1
    goods_info_obj.update(fclick=new_click)     # 取出数据库中的点击量+1

    try:
        user_id = request.session['user_info']['id']
        cart_list = shop_models.ShoppingCart.objects.filter(suser_info_id=user_id).all()
        num = 0  # 商品总数 ==> 购物车的值
        for obj in cart_list:
            num += obj.snum
    except:
        num=0
    new_goods_list = models.FreshType.objects.get(tentitle = kwargs['condition']).freshinfo_set.order_by('-id')[0:2]    # 获取当前类商品最新的2件

    ret = render(request,'df_home/detail.html',{'home':1,'new_goods_list':new_goods_list,'goods_info_obj':goods_info_obj.first(),'kwargs':kwargs,'title':'天天生鲜-商品详情','num':num})
    # 记录最近浏览
    recently_str = request.COOKIES.get('recently_browse','')
    if recently_str != '':
        recently_list = recently_str.split(',')     # 将str切割成[]
        if kwargs['nid'] in recently_list:
            recently_list.remove(kwargs['nid'])     # 如果商品id存在列表中，删除
        recently_list.insert(0,kwargs['nid'])     # 在cookie列表前面加新值
        if len(recently_list) > 5:
            recently_list.pop()     # 删除最后一个数
        new_str = ','.join(recently_list)
    else:
        new_str = str(kwargs['nid'])
    ret.set_cookie('recently_browse',new_str)
    return ret