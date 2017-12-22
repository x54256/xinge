from django.shortcuts import redirect

def check_login(func):
    """
    装饰器：判断用户是否登录
    :param func:
    :return:
    """
    def inner(request, *args, **kwargs):
        if request.session.get('user_info'):
            return func(request, *args, **kwargs)
        else:
            return redirect('/user/login/')
    return inner