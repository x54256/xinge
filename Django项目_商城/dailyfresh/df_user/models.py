from django.db import models

# Create your models here.

class UserInfo(models.Model):   # 用户信息表
    uname = models.CharField(max_length=32)
    upwd = models.CharField(max_length=64)
    uemail = models.CharField(max_length=32)

class UserAddr(models.Model):   # 用户住址表
    ureceiver = models.CharField(max_length=32)          # 收货人
    uaddress = models.CharField(max_length=64)           # 收货地址
    uphone = models.CharField(max_length=11)             # 收货人手机号
    current_addr = models.BooleanField(default=False)  # 当前绑定的收货地址，bool类型，默认值是False
    user_info = models.ForeignKey("UserInfo")          # 绑外键到userinfo表

