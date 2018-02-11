#coding:utf-8

from views.BaseHandler import BaseHandler
from database import models
from utils.response_code import RET
from utils.check_code import create_check_code
from Form.account import RegisterForm
from io import BytesIO
from config import IMAGE_CODE_EXPIRES_SECONDS
from utils.session import Session

import logging
import config


class RegisterHandler(BaseHandler):
    def get(self):
        form = RegisterForm(self)
        self.render('register.html',form=form)
    def post(self):
        form = RegisterForm(self)
        if form.is_valid():
            code_id = self.get_argument("code_id")      # 获取验证码id
            real_text = self.redis.get("img_code_%s"%code_id).decode("utf-8").lower()     # 通过验证码id从redis中获取真实的验证码文本
            input_text = form.value_dict['imagecode'].lower()   # 获取用户输入的验证码文本

            # 判断数据库中是否存在该用户名(因为我把username设成唯一键了)
            obj = models.Session.query(models.UserInfo).filter_by(user_name=form.value_dict["username"]).first()
            if not obj:
                if real_text == input_text:
                    if form.value_dict.get("password") == form.value_dict.get("password2"):
                        # 入库+跳转
                        try:
                            user_obj=models.UserInfo(user_name=form.value_dict['username'],user_passwd=form.value_dict['password'])    #增
                            models.Session.add(user_obj)
                            models.Session.commit()  # 保存操作

                            return self.redirect("/login.html")
                        except Exception as e:
                            logging.error('======== mysql数据库插入错误 ========',e)
                    else:
                        form.error_dict['password2'] = '两次密码输入不一致'
                else:
                    form.error_dict['imagecode'] = '验证码输入错误,或已过期'
            else:
                form.error_dict['username'] = '该用户名已存在'

            self.render('register.html', form=form)

        else:
            print(form.error_dict)
            self.render('register.html', form=form)


class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        username = self.json_dict.get("username")
        password = self.json_dict.get("password")
        rmb = self.json_dict.get("rmb")
        if all((username,password)):
            # try:
            obj = models.Session.query(models.UserInfo).filter_by(user_name=username).first()
            # except Exception as e:
            #     logging.error(e)
                # return self.write(dict(errno=RET.DBERR,errmsg="用户不存在"))
            if obj:
                if obj.user_passwd == password:
                    nid = obj.user_id
                    session_obj = Session(self)
                    session_obj.data['nid'] = nid     # 往session.data中存东西
                    session_obj.data['username'] = username
                    session_obj.data['password'] = password
                    if rmb:
                        session_obj.save(config.SESSION_EXPIRES_SECONDS)      # 保存操作,将数据存到redis中
                        self.set_secure_cookie('session_id', "sess_%s" % session_obj.session_id, expires_days=1)	# 设置浏览器cookie，过期时间为1天
                    else:
                        session_obj.save(config.SESSION_EXPIRES_SECONDS_30)
                        self.set_secure_cookie('session_id', "sess_%s" % session_obj.session_id, expires_days=29)	# 设置浏览器cookie，过期时间为29天

                    return self.write(dict(errno=RET.OK,errmsg="成功",))
                else:
                    return self.write(dict(errno=RET.PWDERR,errmsg="密码错误"))
            else:
                return self.write(dict(errno=RET.USERERR,errmsg="用户不存在或未激活"))
        else:
            return self.write(dict(errno=RET.PARAMERR,errmsg="参数错误"))


class CheckCode(BaseHandler):
    def get(self):
        codeid = self.get_argument("codeid")    # 新codeid
        pcodeid = self.get_argument("pcodeid")  # 上一个codeid
        img, strs = create_check_code()     # 生成验证码图片+字符串
        try:
            self.redis.setex("img_code_%s"%codeid,IMAGE_CODE_EXPIRES_SECONDS,strs)    # 将验证码id和验证码文本存入redis中

        except Exception as e:
            logging.error(e)

        else:
            self.redis.delete("img_code_%s"%pcodeid)      # 将上一次存的codeid键值对从redis中删除

            imgbio = BytesIO()  # 内存中读写二进制数据，string类型的是：StringIO
            img.save(imgbio, 'PNG')  # 在内存中存储验证码图片
            self.set_header("Content-Type", 'image/jpg')  # 为自己设置响应头
            self.write(imgbio.getvalue())  # 从内存中获取img图片（二进制流）

