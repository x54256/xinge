# encoding:utf-8
import jieba  # 导入jieba模块
import pymongo
import time

class hotwords(object):
    hot_dict = {}
    def __init__(self):
        self.stopwords = set()
        self.mongo_conn = pymongo.MongoClient('127.0.0.1',27017)
        with open('stop_words.txt', 'rb') as fstop:
            for eachWord in fstop:
                self.stopwords.add(eachWord.strip().decode('utf-8'))

    def splitSentence(self,inputText):
        seg_list = jieba.cut(inputText)
        outStr = ''
        for seg in seg_list:
            word = seg.strip()  # 去除每行首尾可能出现的空格，并转为Unicode进行处理
            if word in self.stopwords:
                pass
            else:
                outStr += word
                outStr += ' '
        self.statistics(outStr)

    def statistics(self,outText):
        for i in outText.split():
            if len(i) > 1:
                if i in hotwords.hot_dict:
                    hotwords.hot_dict[i] += 1
                else:
                    hotwords.hot_dict[i] = 1

    def close(self):
        # 将字典转为元组
        hot_tup = zip(hotwords.hot_dict.values(), hotwords.hot_dict.keys())

        top_10 = sorted(hot_tup,reverse=True)[0:9]

        print(top_10)

        db = self.mongo_conn.xingedb
        db.hotwords.insert_one({'date':time.strftime('%Y-%m-%d',time.localtime()),'top_10':top_10})     # 将今天日期和top10存入mongodb中
