from django.contrib import admin
from df_home import models

# Register your models here.

"""
    配置Django admin
"""

class FreshTypeAdmin(admin.ModelAdmin):
    list_display = ['id','ttitle']    # 显示的内容

class FreshInfoAdmin(admin.ModelAdmin):
    list_per_page = 15    # 每页显示15条数据
    list_display = ['id','ftitle','fpic','fprice','funit','fclick','fsynopsis','fcontent','ftype',]

admin.site.register(models.FreshType,FreshTypeAdmin)
admin.site.register(models.FreshInfo,FreshInfoAdmin)