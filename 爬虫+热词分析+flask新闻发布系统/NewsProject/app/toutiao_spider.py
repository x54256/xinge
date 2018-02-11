# coding:utf-8
import sys
sys.path.append("..")

import json
import requests
import pymysql
import datetime
import time
import gevent

from lxml import etree
from selenium import webdriver
from app.HotWords import hotwords
from app.models import search


hot = hotwords()

class TouTiaoSpider(object):
    def __init__(self,url):
        self.headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}
        self.mysql_conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='5456', db='newsdb',charset='utf8')
        self.driver = webdriver.PhantomJS()
        self.driver.get(url)

    def get_json_data(self):
        response = self.driver.page_source.strip('<html><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">')
        json_datas = json.loads(response)['data']
        self.driver.execute_script("location.reload();")
        for data in json_datas:
            try:
                img_url = data['image_url']      # 小图片的url
                source_url = 'https://www.toutiao.com' + data['source_url']     # 下次请求的url
                tag = data['tag_url']       # 文章类别
                abstract = data['abstract']     # 文章摘要
            except:
                pass
            else:
                if 'group' in data['source_url']:
                    if data['source'] != '悟空问答':
                        self.get_article(source_url,tag,abstract,img_url)

    def get_article(self,source_url,tag,abstract,img_url):
        #print(source_url)
        response = requests.get(source_url,headers = self.headers).text
        time.sleep(1)
        html = etree.HTML(response.encode("utf-8"))
        try:
            title = html.xpath('//h1/text()')[0]
            content = html.xpath('//div[@class="article-content"]//p')
            img_content = html.xpath('//div[@class="article-content"]//p/img/@src')
            airt_time = html.xpath('//span[@class="time"]/text()')[0]
        except:
            pass
        else:
            text = ""
            num = 0
            #print(title,airt_time)
            try:
                for i in content:
                    if i.text != None:
                        text += '<p>' + i.text + '</p>'
                    else:
                        text += '<img src=' + img_content[num] + '>'
                        num += 1
            except Exception as e:
                print('--------------------------------',e)
            else:
                self.to_mysql(title,airt_time,text,tag,abstract,img_url)


    def to_mysql(self,title,airt_time,text,tag,abstract,img_url):
        cursor = self.mysql_conn.cursor()
        cursor.execute('select c_id from category where c_enname = %s;', [tag, ])
        group = cursor.fetchone()
        if group:
            c_id = group[0]
            cursor.execute('insert into article(a_title,a_time,a_text,a_abstract,a_category_id,a_img_url,a_ctime) values (%s,%s,%s,%s,%s,%s,%s);',[title,airt_time,text,abstract, c_id,img_url,datetime.datetime.now()])
        else:
            cursor.execute('insert into article(a_title,a_time,a_text,a_abstract,a_category_id,a_img_url,a_ctime) values (%s,%s,%s,%s,%s,%s,%s);',[title,airt_time,text,abstract, 1,img_url,datetime.datetime.now()])
        print(title,'已经入库')
        self.mysql_conn.commit()  # 提交，不然无法保存新建或者修改的数据
        cursor.close()  # 关闭游标
        hot.splitSentence(abstract)   #分析热词


    def close(self):
        self.driver.close()     # 关闭浏览器
        self.mysql_conn.close()     # 关闭mysql连接

if __name__ == '__main__':
    # 热点：
    a = TouTiaoSpider("https://www.toutiao.com/api/pc/feed/?category=news_hot&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A1B58A768DC80D0&cp=5A6D48307D705E1&_signature=lx.i8gAAzX7Lc00a6.MU1Jcf4u")
    # 科技：
    b = TouTiaoSpider("https://www.toutiao.com/api/pc/feed/?category=news_tech&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A1958AE63DD812F&cp=5A6D48A1328FCE1&_signature=l71gmQAAzdzL0c9xv-s9epe9YI")
    # #娱乐：
    c = TouTiaoSpider("https://www.toutiao.com/api/pc/feed/?category=news_entertainment&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A1252A860D6814D&cp=5A6D68E1D47D4E1&_signature=l4NppwAAzfrL78ZPxDvn85eDab")
    #游戏：
    d = TouTiaoSpider("https://www.toutiao.com/api/pc/feed/?category=news_game&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A1154A66AD48188&cp=5A6DA8E1A858CE1&_signature=lEcViwAAzjbIK7pj.3m0vpRHFZ")
    #体育：
    e = TouTiaoSpider("https://www.toutiao.com/api/pc/feed/?category=news_sports&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A135EA562D881AB&cp=5A6DD8515A4BEE1&_signature=lCCtsgAAzlnITAJa7dfxoJQgra")
    #汽车：
    f = TouTiaoSpider("https://www.toutiao.com/api/pc/feed/?category=news_car&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A145CA06BD781C9&cp=5A6D4841BCC93E1&_signature=lAbA1wAAznfIam8.IsYiEpQGwM")
    #财经：
    g = TouTiaoSpider("https://www.toutiao.com/api/pc/feed/?category=news_finance&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A1353AD6CD981F0&cp=5A6D9801CF001E1&_signature=lP9HDgAAzp7Ik-jm8R68NpT.Rx")
    #国际：
    h = TouTiaoSpider("https://www.toutiao.com/api/pc/feed/?category=news_world&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A1C5AA06AD28206&cp=5A6D681280060E1&_signature=lMUSvwAAzrTIqb1XYTEW0ZTFEq")
    #育儿：
    i = TouTiaoSpider("https://www.toutiao.com/api/pc/feed/?category=news_baby&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A1B59A360DB828D&cp=5A6DF892E81D9E1&_signature=lUJH9AAAzzvJLugcj0ZnF5VCR")
    #军事：
    j = TouTiaoSpider("https://www.toutiao.com/api/pc/feed/?category=news_military&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=0&tadrequire=true&as=A195FA369D482AF&cp=5A6D0892DA9FCE1&_signature=lTzz.QAAz13JUFwVGrOIKJU88")

    num = 1
    while num:
        gevent.joinall([
            gevent.spawn(a.get_json_data()),
            gevent.spawn(b.get_json_data()),
            gevent.spawn(c.get_json_data()),
            gevent.spawn(d.get_json_data()),
            gevent.spawn(e.get_json_data()),
            gevent.spawn(f.get_json_data()),
            gevent.spawn(g.get_json_data()),
            gevent.spawn(h.get_json_data()),
            gevent.spawn(i.get_json_data()),
            gevent.spawn(j.get_json_data()),
        ])
        num -= 1
        time.sleep(10)
    a.close()
    b.close()
    c.close()
    d.close()
    e.close()
    f.close()
    g.close()
    h.close()
    i.close()
    j.close()
    hot.close()
    search.create_index()  # 建立索引

