#coding:utf-8
import pymongo

from flask import Blueprint, render_template, redirect,request
from .models import Category,Article,search
from utils import pagination

toutiao = Blueprint('toutiao',__name__)

def get_hot_words():
    client = pymongo.MongoClient('127.0.0.1', 27017)
    db = client.xingedb
    count = db.hotwords.count()
    hot_today = db.hotwords.find().limit(1).skip(count-1).next()
    return hot_today['top_10']

@toutiao.route('/')
def index():
    return redirect('/toutiao/all')


@toutiao.route('/<any(news_hots,news_tech,news_entertainment,news_game,news_sports,news_car,news_finance,news_world,news_baby,news_military,all):page_name>',methods=['GET'])
def category(page_name):

    if page_name != 'all':
        c_id = Category.query.filter_by(c_enname=page_name).first().c_id
        obj = Article.query.filter_by(a_category_id=c_id).all()
    else:
        obj = Article.query.all()

    top_10 = get_hot_words()

    # 页码
    current_page = request.args.get('p', 1)  # 第一次请求的时候默认看第一页
    current_page = int(current_page)

    page_obj = pagination.Pagination(current_page,len(obj))

    data = obj[page_obj.start:page_obj.end]

    page_str = page_obj.page_str("/toutiao/"+page_name)


    return render_template('index.html', obj=data, page_str=page_str,top_10=top_10)



@toutiao.route('/<int:a_id>',methods=['GET'])
def article(a_id):
    obj = Article.query.filter_by(id=a_id).first()

    top_10 = get_hot_words()

    return render_template('article.html', obj=obj,top_10=top_10)


@toutiao.route('/search')
def w_search():
    word = request.args.get('keyword')
    search.create_index(update=True)  # 建立索引
    results = search.whoosh_search(Article, query=word, fields=['a_title','a_abstract','a_time','a_img_url'], limit=20)
    #print(results)
    li = []
    for i in results:
        if i in li:
            pass
        else:
            li.append(i)
    #print(li)

    top_10 = get_hot_words()

    # 页码
    current_page = request.args.get('p', 1)  # 第一次请求的时候默认看第一页
    current_page = int(current_page)

    page_obj = pagination.Pagination(current_page, len(li))

    data = li[page_obj.start:page_obj.end]


    page_str = page_obj.page_str("/toutiao/search")

    return render_template('search.html', obj=data,top_10=top_10,page_str=page_str)
