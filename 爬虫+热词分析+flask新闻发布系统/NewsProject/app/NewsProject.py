import pymysql

from flask import Flask,render_template,request,redirect
from utils import pagination


app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/all')


@app.route('/<any(news_hots,news_tech,news_entertainment,news_game,news_sports,news_car,news_finance,news_world,news_baby,news_military,all):page_name>',methods=['GET'])
def category(page_name):
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='5456', db='newsdb',charset='utf8')  # 创建连接

    cursor = conn.cursor()  # 创建游标，为了日后的回滚

    if page_name == 'all':
        cursor.execute('select a_id,a_title,a_time,a_img from article')  # 执行SQL，并返回收影响行数
    else:
        cursor.execute('select c_id from category where c_enname= %s;',[page_name,])

        c_id = cursor.fetchone()[0]

        cursor.execute('select a_id,a_title,a_time,a_img from article where a_category = %s;', [c_id, ])  # 执行SQL，并返回收影响行数

    obj = cursor.fetchall()  # 获取全部类别的article的信息

    conn.commit()  # 提交，不然无法保存新建或者修改的数据

    cursor.close()  # 关闭游标

    conn.close()  # 关闭连接


    current_page = request.args.get('p', 1)  # 第一次请求的时候默认看第一页
    current_page = int(current_page)

    page_obj = pagination.Pagination(current_page,len(obj))

    data = obj[page_obj.start:page_obj.end]

    page_str = page_obj.page_str("/"+page_name)


    return render_template('index.html', obj=data, page_str=page_str)



@app.route('/<int:a_id>',methods=['GET'])
def article(a_id):
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='5456', db='newsdb',charset='utf8')  # 创建连接

    cursor = conn.cursor()  # 创建游标，为了日后的回滚

    cursor.execute('select * from article where a_id = %s;', [a_id, ])  # 执行SQL，并返回收影响行数

    obj = cursor.fetchone()     # 获取article的信息

    conn.commit()  # 提交，不然无法保存新建或者修改的数据

    cursor.close()  # 关闭游标

    conn.close()  # 关闭连接

    return render_template('article.html', obj=obj)



if __name__ == '__main__':
    app.run()
