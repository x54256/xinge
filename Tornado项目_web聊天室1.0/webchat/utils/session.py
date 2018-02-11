#coding:utf-8

import uuid
import logging
import json
import config


class Session(object):
	"""
	生成session_id，和session字典
	"""
	def __init__(self,request_handler):
		self.request_handler = request_handler
		self.session_id = self.request_handler.get_secure_cookie("session_id","")
		if not self.session_id:
			self.session_id = uuid.uuid4().hex
			self.data = {}
		else:
			try:
				data = self.request_handler.redis.get("sess_%s" % self.session_id)
				if not data:
					self.data = {}
			except Exception as e:
				logging.error(e)
				self.data = {}
			else:
				self.data = json.load(data.decode('utf-8'))

	def save(self,SESSION_EXPIRES_SECONDS):
		try:
			self.request_handler.redis.setex("sess_%s" % self.session_id,SESSION_EXPIRES_SECONDS,json.dumps(self.data,ensure_ascii=False))	# 设置session（redis中），过期时间为1天
		except Exception as e:
			logging.error(e)	# 记录，然后抛出异常
			raise e

	def clear(self):
		try:
			self.request_handler.redis.delete("sess_%s" % self.session_id)
			self.request_handler.clear_cookie("session_id")
		except Exception as e:
			logging.error(e)
			raise e