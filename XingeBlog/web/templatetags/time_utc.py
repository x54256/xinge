from django import template
import datetime,time

register = template.Library()

@register.simple_tag
def change(oldtime):
    a = oldtime + datetime.timedelta(hours=8)  # utc+8时间
    b = a.strftime("%Y-%m-%d %H:%M:%S")  # 转换成字符串
    c = time.strptime(b, "%Y-%m-%d %H:%M:%S")  # 字符串转换成元组
    newtime = str(c.tm_year) + '年' + str(c.tm_mon) + '月' + str(c.tm_mday) + '日' # 整成某年某月的格式
    return newtime


@register.simple_tag
def datechange(oldtime):
    list = []
    for i in oldtime:
        list.append(i)
    list[4]='-'
    list.pop()
    if len(list) == 6:
        list.insert(5,'0')
    strlist = ''.join(list)
    return strlist