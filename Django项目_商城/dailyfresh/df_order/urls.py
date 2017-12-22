from django.conf.urls import url,include
from django.contrib import admin
from df_order import views

urlpatterns = [
    url(r'^submit/$', views.submit),
    url(r'^handler/$', views.handler),
    url(r'^handler2/$', views.handler2),
]
