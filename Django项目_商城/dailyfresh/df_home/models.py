from django.db import models
from tinymce.models import HTMLField

# Create your models here.

class FreshType(models.Model):
    ttitle = models.CharField(max_length=32)    # 生鲜的种类
    tentitle = models.CharField(max_length=32,default='firut')    # 生鲜的种类英文名
    def __str__(self):
        return self.ttitle

class FreshInfo(models.Model):
    ftitle = models.CharField(max_length=32)    # 生鲜的名字
    fpic = models.ImageField(upload_to='fresh_info')    # 生鲜的图片
    fbigpic = models.ImageField(upload_to='fresh_info_bigimg')    # 生鲜的大图
    fprice = models.DecimalField(max_digits=5,decimal_places=2) # 生鲜的价格max_digits是最大总位数，decimal_places是小数位数
    funit = models.CharField(max_length=32,default='500g')     # 生鲜的价格单位，默认500g
    fclick = models.IntegerField()      # 单个商品的点击率
    fsynopsis = models.CharField(max_length=200)    # 商品简介
    fcontent = HTMLField()      # 富文本编辑框，用于Django admin
    ftype = models.ForeignKey('FreshType')    # 绑外键，水果种类
    def __str__(self):
        return self.ftitle