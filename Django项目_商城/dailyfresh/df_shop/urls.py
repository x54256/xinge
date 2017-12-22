from django.conf.urls import url,include
from df_shop import views

urlpatterns = [
    url(r'^cart/', views.cart),
    url(r'^add/', views.add),
    url(r'^edit/', views.edit),
    url(r'^del/', views.delete),
]
