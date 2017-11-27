from django.shortcuts import HttpResponse,redirect,render
from  utils import page
from web import models
from django.utils.safestring import mark_safe
import os,json,time,datetime

def index(request):
    '''
    主页
    :param request:
    :return:
    '''
    current_page = request.GET.get('p', 1)  # 1是干嘛的 ==> 第一次请求的时候默认看第一页
    current_page = int(current_page)
    LIST = models.Article.objects.all().select_related()  #Queryset[obj,obj,...]
    page_obj = page.Page(current_page, len(LIST))

    data = LIST[page_obj.start:page_obj.end]

    page_str = page_obj.page_str("")

    try:
        user = request.session['username']
        str123 = mark_safe('<li><a href="/backend/base-info.html">欢迎登录%s</a></li><li><a href="/exit/">退出</a></li>'%user)
    except KeyError as e:
        str123 = mark_safe('<li><a href="/login.html">登录</a></li><li><a href="/register.html">注册</a></li>')

    return render(request,'home.html',{'article_obj':data,'page_str': page_str,'top':str123})

def result(request,site):
    '''
    分类页
    :param request:
    :param site:
    :return:
    '''
    current_page = request.GET.get('p', 1)  # 1是干嘛的 ==> 第一次请求的时候默认看第一页
    current_page = int(current_page)
    classification_id = models.Classification.objects.filter(classification_name=site).first().id
    LIST = models.Article.objects.filter(category_id = classification_id)

    # LIST = models.Article.objects.all().select_related()  #Queryset[obj,obj,...]
    page_obj = page.Page(current_page, len(LIST))

    data = LIST[page_obj.start:page_obj.end]

    page_str = page_obj.page_str("")

    try:
        user = request.session['username']
        str123 = mark_safe('<li><a href="/backend/base-info.html">欢迎登录%s</a></li><li><a href="/exit/">退出</a></li>'%user)
    except KeyError as e:
        str123 = mark_safe('<li><a href="/login.html">登录</a></li><li><a href="/register.html">注册</a></li>')

    return render(request,'home.html',{'article_obj':data,'page_str': page_str,'top':str123})


def article(request,site,pid):  # site就是某人的username，pid是文章id
    # filename = os.path.basename('x5456-2.html')
    # print(filename)
    '''
    某人的某篇文章
    :param request:
    :param site:
    :param pid:
    :return:
    '''
    url123 = request.get_full_path()    # 当前url
    inform_num = models.Article.objects.filter(author__username=site).count()    # 文章总数*****************先就这么着，回来再整
    file_path = os.path.join('static/file/',site+'-'+pid+'.html')
    LIST = models.Comm.objects.filter(comm_article_id=pid).all()  # [obj,obj,...]
    if len(LIST)<10:
        data = LIST
    else:
        data = LIST[len(LIST)-10: len(LIST)]

    try:
        with open(file_path,'rb') as e:
            files = e.read()
        obj = models.UserInfo.objects.filter(username=site).first()

        a_obj = models.Article.objects.get(id=pid)      # 获取当前访问的文章对象


        ctime = a_obj.release_date
        ctime = ctime + datetime.timedelta(hours=8)
        str_time = ctime.strftime("%Y-%m-%d")       # 文章发布时间   转换成utc时间 ==> 字符串

        # 时间的对象=================================*******============================================== 我忘了是啥了0.0..

        time_list = []
        author_obj = models.Article.objects.filter(author__username=site).all()     # 找到所有当前用户名写的文章
        for i in author_obj:
            a = i.release_date + datetime.timedelta(hours=8)    # utc+8时间
            b = a.strftime("%Y-%m-%d %H:%M:%S")     # 转换成字符串
            c = time.strptime(b,"%Y-%m-%d %H:%M:%S")    # 字符串转换成元组
            d = str(c.tm_year)+'年'+str(c.tm_mon)+'月'    # 整成某年某月的格式
            time_list.append(d)
        temp = list(set(time_list))     # 去重
        temp.sort(key=time_list.index)  # 按照列表的顺序排列
        from django.db.models import Count, Min, Max, Sum
        group_obj = models.Article.objects.filter(author__username=site).values(
            'category__classification_name').annotate(c=Count('id'))
        return render(request, 'blog.html', {'files': files,'inform_num':inform_num,     # 文章总数*****************先就这么着，回来再整
                                                 "obj":obj,'str_time':str_time,'temp':temp,
                                             'a_obj':a_obj,'url123':url123,
                                             'comm_obj':data,'group_obj':group_obj})
    except FileNotFoundError as f:
        return HttpResponse('您访问的页面不存在')    # 暂时就这样吧，到时候改成好看点的页面

def fabulous(request):
    '''
    赞
    :param request:
    :return:
    '''
    a_id = request.POST.get('art_id')   # 文章id

    try:
        user = request.session['username']
        uid = models.UserInfo.objects.get(username=user).id
        if models.article_to_reader.objects.filter(article_id=a_id, reader__username=user):
            dic = {'data': '你已经进行过踩赞操作了，请勿重复操作！！！', 'flag': ''}
        else:
            models.article_to_reader.objects.create(article_id=a_id, reader_id=uid)  # 没有的话创建
            num = models.Article.objects.get(id=a_id).fabulous
            num = num + 1
            models.Article.objects.filter(id=a_id).update(fabulous=num)
            dic = {'data': str(num), 'flag': 'true'}
    except KeyError as e:
        dic = {'data':'请您先登录...','flag':''}

    return HttpResponse(json.dumps(dic))

def opposition(request):
    '''
    踩
    :param request:
    :return:
    '''
    a_id = request.POST.get('art_id')  # 文章id

    try:
        user = request.session['username']
        uid = models.UserInfo.objects.get(username=user).id
        if models.article_to_reader.objects.filter(article_id=a_id, reader__username=user):
            dic = {'data': '你已经进行过踩赞操作了，请勿重复操作!!!', 'flag': ''}
        else:
            models.article_to_reader.objects.create(article_id=a_id, reader_id=uid)  # 没有的话创建
            num = models.Article.objects.get(id=a_id).opposition
            num = num + 1
            models.Article.objects.filter(id=a_id).update(opposition=num)
            dic = {'data': str(num), 'flag': 'true'}
    except KeyError as e:
        dic = {'data':'请您先登录...','flag':''}

    return HttpResponse(json.dumps(dic))

def load(request):
    '''博客页面判断是否登录'''
    try:
        is_login = request.session['is_login']
    except KeyError as k:
        is_login = ''
    return HttpResponse(is_login)

def comment(request):
    '''
    添加评论
    :param request:
    :return:
    '''
    aid = request.POST.get('article_id')    # 评论文章的id
    cname = request.session['username']       # 评论人的名字
    cid = models.UserInfo.objects.get(username=cname).id    # id
    abstract = request.POST.get("abstract") # 评论内容
    models.Comm.objects.create(reviewer_id=cid,comm_abstract=abstract,comm_article_id=aid)
    c_time = datetime.datetime.now()     # 注意下这个是utc+8时间
    c_time = c_time.strftime("%Y-%m-%d")
    c_time = time.strptime(c_time, "%Y-%m-%d")  # 字符串转换成元组
    c_time = str(c_time.tm_year) + '年' + str(c_time.tm_mon) + '月' + str(c_time.tm_mday) + '日' # 整成某年某月的格式

    n = models.Article.objects.get(id = aid).comm123    # 文章评论数
    n=n+1
    models.Article.objects.filter(id=aid).update(comm123=n)
    return HttpResponse(c_time)

def filter(request,site,condition):
    '''
    按照python，Linux...分类
    :param request:
    :param site:
    :param condition:
    :return:
    '''
    userobj = models.UserInfo.objects.filter(username=site)
    if userobj:
        try:
            url123 = request.get_full_path()
            obj = models.UserInfo.objects.filter(username=site).first()     # 获取用户信息
            if condition == 'all':
                a_obj = models.Article.objects.filter(author__username=site).all()  # 获取到所有分类的对象[obj,obj,..]
            else:
                cid = models.Classification.objects.get(classification_name=condition)  # 分类的id
                a_obj = models.Article.objects.filter(author__username=site,category_id=cid)  # 获取到相应分类的对象[obj,obj,..]
            num = 0
            for i in a_obj:
                num = num + i.comm123     #  评论数

            # # 还差一个时间的对象，=================================*******==============================================
            time_list = []
            author_obj = models.Article.objects.filter(author__username=site).all()  # 找到所有当前用户名写的文章
            for i in author_obj:
                a = i.release_date + datetime.timedelta(hours=8)  # utc+8时间
                b = a.strftime("%Y-%m-%d %H:%M:%S")  # 转换成字符串
                c = time.strptime(b, "%Y-%m-%d %H:%M:%S")  # 字符串转换成元组
                d = str(c.tm_year) + '年' + str(c.tm_mon) + '月'  # 整成某年某月的格式
                time_list.append(d)
            temp = list(set(time_list))  # 去重
            temp.sort(key=time_list.index)  # 按照列表的顺序排列

            from django.db.models import Count, Min, Max, Sum
            group_obj = models.Article.objects.filter(author__username=site).values(
                'category__classification_name').annotate(c=Count('id'))


            current_page = request.GET.get('p', 1)  # 1是干嘛的 ==> 第一次请求的时候默认看第一页
            current_page = int(current_page)
            LIST = a_obj
            page_obj = page.Page(current_page, len(LIST))
            data = LIST[page_obj.start:page_obj.end]
            page_str = page_obj.page_str(request.path)
            return render(request,'blog_filter.html',{'url123':url123,'obj':obj,'a_obj':data,'num':str(num),
                                                      'temp':temp,'group_obj':group_obj,'page_str':page_str})

        except KeyError:
            return HttpResponse('你走开——分类名输错了')

    else:
        return HttpResponse('你走开——用户名输错了')

def date_filter(request,site,val):
    userobj = models.UserInfo.objects.filter(username=site)
    if userobj:
        try:
            url123 = request.get_full_path()
            obj = models.UserInfo.objects.filter(username=site).first()     # 获取用户信息
            # a_obj = models.Article.objects.filter(author__username=site,release_date=val)  # 获取到相应分类的对象[obj,obj,..]
            # print(a_obj)
            a_obj = models.Article.objects.filter\
                (author__username=site).extra(where=['date_format(release_date,"%%Y-%%m")=%s'], params=[val, ]).all()
            num = 0
            for i in a_obj:
                num = num + i.comm123  # 评论数

            # # 还差一个时间的对象，=================================*******==============================================
            time_list = []
            author_obj = models.Article.objects.filter(author__username=site).all()  # 找到所有当前用户名写的文章
            for i in author_obj:
                a = i.release_date + datetime.timedelta(hours=8)  # utc+8时间
                b = a.strftime("%Y-%m-%d %H:%M:%S")  # 转换成字符串
                c = time.strptime(b, "%Y-%m-%d %H:%M:%S")  # 字符串转换成元组
                d = str(c.tm_year) + '年' + str(c.tm_mon) + '月'  # 整成某年某月的格式
                time_list.append(d)
            temp = list(set(time_list))  # 去重
            temp.sort(key=time_list.index)  # 按照列表的顺序排列

            from django.db.models import Count, Min, Max, Sum
            group_obj = models.Article.objects.filter(author__username=site).values(
                'category__classification_name').annotate(c=Count('id'))
            current_page = request.GET.get('p', 1)  # 1是干嘛的 ==> 第一次请求的时候默认看第一页
            current_page = int(current_page)
            LIST = a_obj
            page_obj = page.Page(current_page, len(LIST))
            data = LIST[page_obj.start:page_obj.end]
            page_str = page_obj.page_str(request.path)
            return render(request,'blog_filter.html',{'url123':url123,'obj':obj,'a_obj':data,
                                                      'num':str(num),'temp':temp,'group_obj':group_obj,'page_str':page_str})

        except KeyError:
            pass

    else:
        return HttpResponse('请不要瞎几把输好吧')


