import datetime,time

from app import db    #db是在app/__init__.py生成的关联后的SQLAlchemy实例

# 全文检索
from app import app
from flask_msearch import Search
from jieba.analyse import ChineseAnalyzer

search = Search(analyzer=ChineseAnalyzer())     # 使用结巴中文分词
search.init_app(app)


class Category(db.Model):
    __tablename__ = 'category'
    c_id = db.Column(db.Integer, primary_key=True)
    c_name = db.Column(db.String(32), nullable=False)
    c_enname = db.Column(db.String(32), nullable=False)



class Article(db.Model):
    __tablename__ = 'article'
    __searchable__ = ['a_title','a_abstract','a_time','a_img_url']   # 设置检索字段
    id = db.Column(db.Integer, primary_key=True)    # 自增id从10000开始
    a_title = db.Column(db.String(64), nullable=False)
    a_time = db.Column(db.String(32), nullable=False)
    a_text = db.Column(db.Text, nullable=False)
    a_abstract = db.Column(db.Text, nullable=False)
    a_img_url = db.Column(db.String(64), nullable=False)
    a_ctime = db.Column(db.DateTime,default=datetime.datetime.now)
    a_category_id = db.Column(db.Integer, db.ForeignKey('category.c_id'))


#search.create_index()    # 建立索引


"""
create table category(
    c_enname varchar(32) not null
) ENGINE=InnoDB AUTO_INCREMENT=10000 DEFAULT CHARSET=utf8;

create table article(
--     a_ctime datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
) ENGINE=InnoDB AUTO_INCREMENT=10000 DEFAULT CHARSET=utf8;

"""
