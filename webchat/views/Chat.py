from views.BaseHandler import BaseHandler
from tornado.websocket import WebSocketHandler
import tornado.web

import datetime,json


users = set()  # 用来存放在线用户的容器
users_data = []     # 用来存放在线用户信息的容器


class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        session_id = self.get_secure_cookie('session_id')
        json_dic = self.redis.get(session_id)
        data = json.loads(json_dic.decode("utf-8"))
        datatime = datetime.datetime.now().strftime("%H:%M")
        data['datatime'] = datatime
        self.render("index.html",users_data = users_data,data=data,datatime=datatime)


class ChatHandler(WebSocketHandler,BaseHandler):
    def __init__(self,*args,**kwargs):
        super(ChatHandler,self).__init__(*args,**kwargs)

        self.session_id = self.get_secure_cookie('session_id')
        json_dic = self.redis.get(self.session_id)
        self.data = json.loads(json_dic.decode("utf-8"))
        self.data['datatime'] = datetime.datetime.now().strftime("%H:%M")

    def open(self):
        users.add(self)  # 建立连接后添加用户到容器中
        users_data.append(self.data)     # 建立连接后添加用户信息到容器中
        for u in users:  # 向已在线用户发送消息
            msg = u"[%s]-[%s]-进入聊天室" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            code = '1'
            u.write_message({'msg':msg,'nocode':code,'userdata':self.data})

    def on_message(self, message):
        for u in users:  # 向在线用户广播消息

            msg = u"[%s]-[%s]-说：%s" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message)
            code = '0'
            u.write_message({'msg':msg,'nocode':code,'userdata':self.data})

    def on_close(self):
        users.remove(self)  # 用户关闭连接后从容器中移除用户
        users_data.remove(self.data)
        for u in users:
            msg = u"[%s]-[%s]-离开聊天室" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            code = '2'
            u.write_message({'msg': msg, 'nocode': code, 'userdata': self.data})

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求