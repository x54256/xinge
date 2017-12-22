from django.conf.urls import url,include
from django.contrib import admin
from df_user.views import account
from df_user.views import personal

urlpatterns = [
    url(r'^register/$', account.register),
    url(r'^login/$', account.login),
    url(r'^logout/$', account.logout),
    url(r'^info/$', personal.info),
    url(r'^order/(?P<nid>\d+)-(?P<tid>\d+)-(?P<pid>\d+).html', personal.order),
    url(r'^site/$', personal.site),
]
