from django.conf.urls import url
from web.views import account
from web.views import home

urlpatterns = [
    url(r'^login.html$', account.login),
    url(r'^check_code.html$', account.check_code),
    url(r'^register.html$', account.register),
    url(r'^exit/', account.exit),

    url(r'^$', home.index),         # 主页

    url(r'^fabulous/',home.fabulous),   # 赞
    url(r'^opposition/',home.opposition),   # 踩
    url(r'^load/',home.load),   # 博客页面判断是否登录
    url(r'^comment/',home.comment),   # 添加评论

    url(r'^(?P<site>\w+)/(?P<condition>\w+).html$', home.filter),    # 某人的某类文章汇总 abc/abc.html
    url(r'^(?P<site>\w+)/(?P<val>\w+-*\w+).html', home.date_filter),    # 某人的某时间的文章汇总 ==>alex/2017-11.html,还没写


    url(r'^(\w+)/(?P<site>\w+)-(?P<pid>\d+)/$', home.article),    # 某人的某篇文章 abc/abc-123
    url(r'^(?P<site>\w+)-(?P<pid>\d+)/$', home.article),    # 某人的某篇文章，两种访问方式    abc-123/
    url(r'^(?P<site>\w+)/$', home.result),      # 分类页面     abc/

]
