from django.db import models

# Create your models here.

class ShoppingCart(models.Model):    # 购物车表
    suser_info = models.ForeignKey("df_user.UserInfo")
    sfresh_info = models.ForeignKey("df_home.FreshInfo")
    snum = models.IntegerField()    # 每件商品的数量