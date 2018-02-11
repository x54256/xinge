import os

# app的配置文件
appsettings=dict(
    static_path = os.path.join(os.path.dirname(__file__), "static"),
    template_path = os.path.join(os.path.dirname(__file__), "template"),
    debug = True,
    cookie_secret="2hcicVu+TqShDpfsjMWQLZ0Mkq5NPEWSk9fi0zsSt3A=",
    xsrf_cookies=True,
    login_url="/login.html"
)

# redis的配置文件
redis_config = dict(
    host='localhost',
    port=6379
)

# 图片验证码有效期，秒为单位
IMAGE_CODE_EXPIRES_SECONDS = 120

# session数据有效期，1天
SESSION_EXPIRES_SECONDS = 86400
# session数据有效期，30天
SESSION_EXPIRES_SECONDS_30 = 86400 * 30