from Tyrion.Forms import Form
from Tyrion.Fields import StringField
from Tyrion.Widget import InputPassword,InputText


class RegisterForm(Form):
    username = StringField(
        error={'required': '用户名不能为空'},
        widget=InputText(attr = {'class':"form-control",'name':"username",'id':"username",'placeholder':"用户名"})
    )

    imagecode = StringField(
        error={'required': '验证码不能为空'},
        widget=InputText(attr = {'class':"form-control",'name':"imagecode",'id':"imagecode",'placeholder':"图片验证码"})
    )

    password = StringField(
        error={'required': '密码不能为空'},
        widget=InputPassword(attr = {'class':"form-control",'name':"password",'id':"password",'placeholder':"密码"})
    )

    password2 = StringField(
        error={'required': '密码2不能为空'},
        widget=InputPassword(attr = {'class':"form-control",'name':"password2",'id':"password2",'placeholder':"确认密码"})
    )

    def clean(self):
        print('123')