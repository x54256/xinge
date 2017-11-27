from django.db import models

# Create your models here.

class UserInfo(models.Model):
    user_img = models.CharField(max_length=64)  # 用户头像  *************看这
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    email = models.EmailField()
    follow = models.IntegerField()      # 关注数
    fans = models.IntegerField()        # 粉丝数
    creat_time = models.DateTimeField(auto_now=True)  #记录时间
    task = models.IntegerField()        # 任务数
    notic = models.IntegerField()       # 通知数
    news = models.IntegerField()        # 消息数
    introduce_oneself = models.CharField(max_length=128,null=True)    # 自我介绍

# 这里再建一个关注表+粉丝表 外键绑定userinfo,我就先不做了

class Classification(models.Model):
    classification_name = models.CharField(max_length=32)    # 文章类别

class user_to_class(models.Model):  # 不要管我我想死
    user = models.ForeignKey('UserInfo')
    classificate = models.ForeignKey('Classification')
    article_num = models.IntegerField()         # 用户下的分类的文章数

class article_to_reader(models.Model):
    article = models.ForeignKey('Article')
    reader = models.ForeignKey('UserInfo')

class Article(models.Model):
    title = models.CharField(max_length=32)         # 文章标题
    category = models.ForeignKey('Classification')      # 文章分类，，，，一会改成外键
    author = models.ForeignKey('UserInfo')        # 文章作者，，，，一会改成外键
    abstract = models.CharField(max_length=64)     # 文章摘要
    release_date = models.DateTimeField(auto_now=True)  #记录时间
    comm123 = models.IntegerField()                 # 文章评论数
    fabulous = models.IntegerField()                # 赞同数
    opposition = models.IntegerField()              # 反对数
    click_amount = models.IntegerField()            # 点击量 <==> 阅读数

class Comm(models.Model):
    reviewer = models.ForeignKey('UserInfo')        # 评论人
    comm_abstract = models.CharField(max_length=255) # 评论内容
    ctime = models.DateTimeField(auto_now=True) # 评论时间
    comm_article = models.ForeignKey('Article') # 评论的文章


