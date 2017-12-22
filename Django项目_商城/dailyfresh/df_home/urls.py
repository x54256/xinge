from django.conf.urls import url,include
from django.contrib import admin
from df_home import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^(?P<nid>\d+)-(?P<tid>\d+)-(?P<pid>\d+).html$', views.list),  # nid ==> 当前排序方式，tid ==> 当前类别，pid ==> 当前页
    url(r'^(?P<condition>((firut)|(seafood)|(meat)|(egg)|(vegetables)|(freeze)))/(?P<nid>\d+)$', views.detail),
    url(r'^$', views.index),
]
