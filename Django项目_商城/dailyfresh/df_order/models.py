from django.db import models

# Create your models here.

class OrderInfo(models.Model):
    ouser = models.ForeignKey("df_user.UserInfo")
    otime = models.DateTimeField(auto_now=True)   # 自动生成时间
    oIspay = models.BooleanField(default=False)
    ototal = models.DecimalField(max_digits=6,decimal_places=2)   # 订单总价
    oaddr = models.CharField(max_length=200)    # 订单收货地址

class OrderDetailInfo(models.Model):
    ogoods = models.ForeignKey('df_home.FreshInfo')    # 商品外键
    oorder = models.ForeignKey('OrderInfo')    # 订单外键
    ocount = models.IntegerField()    # 订单每件商品的个数
    oprice = models.DecimalField(max_digits=5,decimal_places=2)    # 订单每件商品的小计
