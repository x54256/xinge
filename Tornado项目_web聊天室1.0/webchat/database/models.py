from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,DateTime,Boolean
from sqlalchemy.orm import sessionmaker
import datetime

engine=create_engine('mysql+pymysql://root:5456@localhost/xingedb',encoding='utf-8')

Base=declarative_base()    #生成orm基类

class UserInfo(Base):
    __tablename__='user_info'    #创建的表名
    user_id=Column(Integer,primary_key=True)    # 用户id
    user_name = Column(String(64),unique=True,nullable=False)   # 用户名
    user_passwd=Column(String(64),nullable=False)     # 密码
    user_avatar=Column(String(64),default='/static/favicon.ico')      # 头像
    user_utime=Column(DateTime,default=datetime.datetime.now,onupdate=datetime.datetime.now)  # 信息更新时间
    user_ctime=Column(DateTime,default=datetime.datetime.now)     # 注册时间


Base.metadata.create_all(engine)    #创建表结构
Session_class=sessionmaker(bind=engine)    #创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
Session=Session_class()    #生成实例


# Session.commit()    #保存操作
