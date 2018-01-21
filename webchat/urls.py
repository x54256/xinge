from views import Passport
from views import Chat

url = [
    (r"^/register.html$", Passport.RegisterHandler),
    (r"^/login.html$", Passport.LoginHandler),
    (r"^/$", Chat.IndexHandler),
    (r"/chat", Chat.ChatHandler),   # 连接websocket
    (r"^/imagecode$", Passport.CheckCode),  # 验证码
]