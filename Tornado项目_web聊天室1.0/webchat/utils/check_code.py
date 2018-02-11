import random
import string
from PIL import Image,ImageDraw,ImageFont,ImageFilter

source = list(string.ascii_letters)
for i in range(10):
    source.append(str(i))

def create_check_code(size=(120,30),    # 传参数
    chars = source,   # 数字+字母等要生成验证码的东西
    mode = "RGB",     # 图像模式
    bg_color = (255,255,255), # 背景颜色，白色
    fg_color = (0,0,255),     # 字体颜色，蓝色
    font_size = 18,           # 字体大小
    font_type = 'Monaco.ttf',     # 字体
    length = 4,              # 长度
    draw_lines = True,     # 是否划线
    n_line = (1,3),       # 画几条
    draw_points = True,    #是否画点
    point_chance = 2):    #花多少点[0,100]
    width,height = size
    img = Image.new(mode,size,bg_color)
    draw = ImageDraw.Draw(img)

    # 生成验证码的步骤
    # a.生成字符串
    # b.绘制图片
    # c.加干扰线和干扰点
    # d.调整斜度
    def get_chars():
        '''生成指定长度的字符串，返回列表格式'''
        return random.sample(chars,length)

    def create_strs():
        '''绘制验证码字符'''
        c_chars= get_chars()
        strs = ' %s '%''.join(c_chars)
        font = ImageFont.truetype(font_type,font_size)
        font_width,font_height = font.getsize(strs)
        draw.text(((width - font_width) / 3, (height - font_height) / 3),strs, font=font, fill=fg_color)
        return ''.join(c_chars)

    def create_lines():
        """绘制干扰线"""
        line_num = random.randint(*n_line)  # 干扰线条数

        for i in range(line_num):
            # 起始点
            begin = (random.randint(0, size[0]), random.randint(0, size[1]))
            # 结束点
            end = (random.randint(0, size[0]), random.randint(0, size[1]))
            draw.line([begin, end], fill=(0, 0, 0))

    def create_points():
        """绘制干扰点"""
        chance = min(100, max(0, int(point_chance)))  # 大小限制在[0, 100]

        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    if draw_lines:
        create_lines()
    if draw_points:
        create_points()
    strs = create_strs()

    # 图形扭曲参数
    params = [1 - float(random.randint(1, 2)) / 100,
              0,
              0,
              0,
              1 - float(random.randint(1, 10)) / 100,
              float(random.randint(1, 2)) / 500,
              0.001,
              float(random.randint(1, 2)) / 500
              ]
    img = img.transform(size, Image.PERSPECTIVE, params)  # 创建扭曲

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强（阈值更大）

    return img, strs











