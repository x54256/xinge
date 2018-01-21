import json
import redis
from config import redis_config

from tornado.web import RequestHandler


class BaseHandler(RequestHandler):
    @property
    def redis(self):
        redis_conn = redis.StrictRedis(host=redis_config['host'], port=redis_config['port'])
        return redis_conn

    # @property
    # def mysql(self):
        # mysql_conn = pymysql.
        # return mysql_conn

    def prepare(self):
        if self.request.headers.get("Content-Type",'').startswith("application/json"):
            self.json_dict = json.loads(self.request.body.decode('utf-8'))
        else:
            self.json_dict = None

    def set_default_headers(self):
        pass

    def write_error(self, status_code, **kwargs):
        pass

    def initialize(self):
        pass

    def on_finish(self):
        pass


    def get_current_user(self):
        """在此完成用户的认证逻辑"""
        session_id = self.get_secure_cookie('session_id')
        if session_id:
            session_data = self.redis.get(session_id)
        else:
            session_data = ''
        return session_data