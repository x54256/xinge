# coding:utf-8
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 数据库连接
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:5456@localhost:3306/newsdb?charset=utf8'
SQLALCHEMY_TRACK_MODIFICATIONS = True


# # 配置查询数据库
# WHOOSH_BASE = os.path.join(BASE_DIR, 'newsdb.db')
# # 全文检索返回最大数量
# MAX_SEARCH_RESULTS = 50

WHOOSH_BASE = 'whoosh_index'
MSEARCH_BACKEND  = 'whoosh' #自动创建或更新索引
WHOOSH_ENABLE = True