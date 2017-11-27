from django.conf.urls import url
from .views import user

urlpatterns = [
    url(r'^base-info.html$', user.base_info),   # 修改个人信息    *ok
    url(r'^category.html$', user.category),     # 个人分类管理    *ok
    url(r'^article-(?P<site>\w+).html$', user.article),       # 个人文章管理    *ok
    url(r'^add-article.html$', user.add_article),   # 添加文章    *ok
    url(r'^edit-article-(\d+).html$', user.edit_article),   # 编辑文章
    url(r'^upload_file/', user.upload_file),    # 上传用户头像    *ok
    url(r'^group_add/', user.group_add),    # 添加分组    *ok
    url(r'^group_del/', user.group_del),  # 删除与分组的对应关系并删除相应组的文章    *ok
    url(r'^group_edit/', user.group_edit),  # 删除与分组的对应关系并删除相应组的文章    *ok
    url(r'^upload/', user.upload),          # kind...上传图片+展示    *ok
    url(r'^del-article/', user.del_article),   # 删除文章    *ok
    url(r'^radio/', user.radio),      # 判断文章是否选择分类    *ok
    url(r'^file_manager/', user.file_manager)   # 文件空间管理
]
