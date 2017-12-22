from django.forms import Form
from django.forms import fields

class LoginForm(Form):
    ureceiver = fields.CharField(
        error_messages={"required":'收件人不能为空'}
    )
    uaddress = fields.CharField(
        error_messages={"required":'地址不能为空'}
    )
    uphone = fields.CharField(
        error_messages={"required":'手机号不能为空'}
    )