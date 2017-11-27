#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render,redirect,HttpResponse
from web import models
import os,time,json
from utils import page

def auth(func):
    def inner(request,*args,**kwargs):
        try:
            v = request.session['is_login']
        except:
            v=0
        if not v:
            return redirect('/login.html')
        return func(request, *args,**kwargs)
    return inner

@auth
def base_info(request):
    """
    博主个人信息
    :param request:
    :return:
    """
    user = request.session['username']
    errors = ''
    if request.method == 'POST':
        old_p = request.POST.get('old_pwd')
        new_p1 = request.POST.get('new_pwd1')
        new_p2 = request.POST.get('new_pwd2')
        introduce = request.POST.get('introduce')
        models.UserInfo.objects.filter(username=user).update(introduce_oneself=introduce)
        if old_p:
            if old_p == models.UserInfo.objects.get(username=user).password:
                if new_p1 == new_p2:
                    models.UserInfo.objects.filter(username=user).update(password=new_p1)
                    errors = '密码修改成功'
                else:
                    errors = '两次密码输入不一致'
            else:
                errors = '旧密码输入错误'
    user_obj = models.UserInfo.objects.get(username=user)
    return render(request, 'backend_base_info.html',{'user_obj':user_obj,'errors':errors})

@auth
def upload_file(request):
    """
    iframe ajax提交显示图片****************头像***************这里要考虑不同用户上传同名的图片的问题
    :param request:
    :return:
    """
    if request.method == 'GET':
        return HttpResponse("滚")
    elif request.method == 'POST':
        user = request.session['username']
        user_img = request.FILES.get('avatarImg')
        import os
        img_path = os.path.join('static/home/'+user+'/imgs/',user_img.name)
        with open(img_path,'wb') as f:
            for item in user_img.chunks():
                f.write(item)
        models.UserInfo.objects.filter(username=user).update(user_img='/'+img_path)
        return HttpResponse(img_path)


@auth
def category(request):
    """
    博主个人分类管理
    :param request:
    :return:
    """
    current_page = request.GET.get('p', 1)  # 1是干嘛的 ==> 第一次请求的时候默认看第一页
    current_page = int(current_page)
    user = request.session['username']
    user_obj = models.UserInfo.objects.filter(username=user).all().select_related() # Queryset[obj,obj,...]
    LIST = models.user_to_class.objects.filter(user__username=user)
    page_obj = page.Page(current_page, len(LIST))
    data = LIST[page_obj.start:page_obj.end]
    page_str = page_obj.page_str("")


    return render(request, 'backend_category.html',{'group_obj':data,'user_obj':user_obj,'page_str':page_str})

@auth
def group_add(request):
    '''
    添加分组
    :param request:
    :return:
    '''
    if request.method == 'POST':
        g_name = request.POST.get('nickname')
        user = request.session['username']
        uid = models.UserInfo.objects.filter(username=user).first().id
        g = models.Classification.objects.filter(classification_name=g_name).first()
        if not g:       # 如果组在之前不存在，则添加再绑定关系
            models.Classification.objects.create(classification_name=g_name)
            gid = models.Classification.objects.filter(classification_name=g_name).first().id
            models.user_to_class.objects.create(classificate_id=gid,user_id=uid,article_num=0)
            return HttpResponse(g_name)

        elif not models.user_to_class.objects.filter(classificate_id=g.id, user_id=uid):           # 之前存在直接建立关系
            gid = g.id
            models.user_to_class.objects.create(classificate_id=gid, user_id=uid, article_num=0)
            return HttpResponse(g_name)
        else:
            return HttpResponse('你长眼睛了吗')
    else:
        return HttpResponse("滚")

@auth
def group_del(request):
    '''
    删除与分组的对应关系并删除相应组的文章
    :param request:
    :return:
    '''
    if request.method == 'POST':
        g_name = request.POST.get('gid')    # 是名字 不要在意内些细节
        user = request.session['username']
        uid = models.UserInfo.objects.filter(username=user).first().id
        gid = models.Classification.objects.filter(classification_name=g_name).first().id
        dic = {'user_id':uid,'classificate_id':gid}
        models.user_to_class.objects.filter(**dic).delete()
        dic2 = {'author_id':uid,'category_id':gid}
        models.Article.objects.filter(**dic2).all().delete()
        return HttpResponse('123')

    else:
        return HttpResponse("滚")

@auth
def group_edit(request):
    '''
    修改分组名分组***************************************ok了
    :param request:
    :return:
    '''
    if request.method == 'POST':
        new_g = request.POST.get('new_g')
        old_g = request.POST.get('old_g')
        user = request.session['username']
        uid = models.UserInfo.objects.get(username=user).id
        old_g_id = models.Classification.objects.get(classification_name=old_g).id
        obj = models.user_to_class.objects.get(classificate_id=old_g_id,user_id=uid)
        art_num = obj.article_num    # 获取之前文章数量
        obj.delete()        # 解除之前的关联
        if not models.Classification.objects.filter(classification_name=new_g):
            models.Classification.objects.create(classification_name=new_g)     # 不存在的话创建
        nid = models.Classification.objects.get(classification_name=new_g).id   # 获取类的id
        models.user_to_class.objects.create(classificate_id=nid,user_id=uid,article_num=art_num)    # 创建新关联
        models.Article.objects.filter(author__username=user,category_id=old_g_id).all().update(category_id=nid)
        return HttpResponse('ok')
    else:
        return HttpResponse("滚")


@auth
def article(request,site):
    """
    博主个人文章管理
    :param request:
    :return:
    """
    if request.method == 'GET':
        user = request.session['username']
        user_obj = models.UserInfo.objects.get(username=user)
        article_obj = models.Article.objects.filter(author__username=user)

        current_page = request.GET.get('p', 1)  # 1是干嘛的 ==> 第一次请求的时候默认看第一页
        current_page = int(current_page)

        page_obj = page.Page(current_page, len(article_obj))
        data = article_obj[page_obj.start:page_obj.end]
        page_str = page_obj.page_str("")

        from django.db.models import Count
        article_list = models.Article.objects.filter(author__username=user).\
            values('category__classification_name').annotate(c = Count('id'))

        if site == 'all':
            a_nums = len(article_obj)  # 文章总数
        elif models.Classification.objects.filter(classification_name=site):
            article_obj = models.Article.objects.filter(author__username=user,category__classification_name=site)
            a_nums = len(article_obj)  # 文章总数
        else:
            return HttpResponse('输入的分类不存在')
        return render(request, 'backend_article.html',{'user_obj':user_obj,'article_list':article_list,
                                                       'article_obj':data,'a_nums':a_nums,'page_str':page_str})

@auth
def del_article(request):
    """
    删除文章
    :param request:
    :param nid:
    :return:
    """
    nid = request.POST.get('nid')
    # models.Article.objects.get(id=nid).delete()
    return HttpResponse('删除成功')

@auth
def add_article(request):
    """
    添加文章
    :param request:
    :return:
    """
    user = request.session['username']
    if request.method == 'POST':
        title = request.POST.get('title')           # 标题
        abstract = request.POST.get('abstract')     #描述
        content = request.POST.get('content')       # 内容
        category_id = request.POST.get('category')     # 分类id
        uid = models.UserInfo.objects.get(username=user).id
        obj = models.user_to_class.objects.filter(classificate_id=category_id,user_id=uid)
        art_num = obj.first().article_num
        art_num = art_num + 1
        obj.update(article_num=art_num)     # 更新某人某类文章的数量
        # 保存文章
        dic = {
            'title': title,
            'category_id':category_id,
            'author_id':uid,
            'abstract':abstract,
            'comm123':0,
            'fabulous': 0,
            'opposition': 0,
            'click_amount': 0,
        }
        models.Article.objects.create(**dic)
        article_id = models.Article.objects.get(**dic).id
        file_path = 'static/file/'+user+'-'+ str(article_id)+'.html'
        with open(file_path,'wb')as f:
            f.write(content.encode('utf-8'))
        return HttpResponse('添加完毕')
        # 先就这样 以后在加一个添加完毕的页面

    user_obj = models.UserInfo.objects.get(username=user)
    group_obj = models.user_to_class.objects.filter(user__username=user)

    return render(request, 'backend_add_article.html',{'group_obj':group_obj,'user_obj':user_obj})

@auth
def file_manager(request):
    '''
    个人文件空间
    :param request:
    :return:
    '''
    user = request.session['username']
    dic = {}
    root_path = 'static/home/'+user+'/'
    static_root_path = '/static/home/'+user+'/'
    request_path = request.GET.get('path')
    if request_path:
        abs_current_dir_path = os.path.join(root_path, request_path)
        move_up_dir_path = os.path.dirname(request_path.rstrip('/'))
        dic['moveup_dir_path'] = move_up_dir_path + '/' if move_up_dir_path else move_up_dir_path

    else:
        abs_current_dir_path = root_path
        dic['moveup_dir_path'] = ''

    dic['current_dir_path'] = request_path
    dic['current_url'] = os.path.join(static_root_path, request_path)

    file_list = []
    for item in os.listdir(abs_current_dir_path):
        abs_item_path = os.path.join(abs_current_dir_path, item)
        a, exts = os.path.splitext(item)
        is_dir = os.path.isdir(abs_item_path)
        if is_dir:
            temp = {
                'is_dir': True,
                'has_file': True,
                'filesize': 0,
                'dir_path': '',
                'is_photo': False,
                'filetype': '',
                'filename': item,
                'datetime': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(os.path.getctime(abs_item_path)))
            }
        else:
            temp = {
                'is_dir': False,
                'has_file': False,
                'filesize': os.stat(abs_item_path).st_size,
                'dir_path': '',
                'is_photo': True if exts.lower() in ['.jpg', '.png', '.jpeg'] else False,
                'filetype': exts.lower().strip('.'),
                'filename': item,
                'datetime': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(os.path.getctime(abs_item_path)))
            }

        file_list.append(temp)
    dic['file_list'] = file_list
    return HttpResponse(json.dumps(dic))
@auth
def upload(request):
    """
    kindeditor上传文件
    :param request:
    :return:
    """
    print(request.GET.get('dir'))       # 可以用来判断发来的是什么类型（img，flash...）的东西
    file = request.FILES.get('filename')
    file_name = file.name
    user = request.session['username']
    path = os.path.join('static/home/'+user+'/data/',file_name)
    with open(path,'wb') as e:
        for i in file.chunks():
            e.write(i)
    dic = {
        'error': 0,
        'url': '/'+path,
        'message': '啦啦啦...'
    }
    return HttpResponse(json.dumps(dic))

@auth
def edit_article(request,nid):
    """
    编辑文章
    :param request:
    :return:
    """
    user = request.session['username']
    user_obj = models.UserInfo.objects.get(username=user)
    group_obj = models.user_to_class.objects.filter(user__username=user)
    au_obj = models.Article.objects.get(id=nid)
    file_path = 'static/file/' + user + '-' + str(nid) + '.html'

    if request.method == 'GET':
        file_obj = open(file_path,'rb').read()
        return render(request, 'backend_edit_article.html',{'nid':nid,'group_obj':group_obj,'user_obj':user_obj,'au_obj':au_obj,'file_obj':file_obj})
    elif request.method == 'POST':
        title = request.POST.get('title')           # 标题
        abstract = request.POST.get('abstract')     #描述
        content = request.POST.get('content')       # 内容
        category_id = request.POST.get('category')     # 分类id
        models.Article.objects.filter(id=nid).update(title=title,abstract=abstract,category_id=category_id)
        with open(file_path,'wb')as f:
            f.write(content.encode('utf-8'))
        return HttpResponse('修改完毕')

@auth
def radio(request):
    category_id = request.POST.get('category')
    if category_id:
        return HttpResponse('true')
    else:
        return HttpResponse('')


