import pygame,sys
from pygame.locals import *
from config.settings import *
from src.hero_plane import OurPlane
from src.hero_bullet import HeroBullet
from src.enemy_plane import *


bg_size = 480, 685  # 初始化游戏背景大小(宽, 高)
screen = pygame.display.set_mode(bg_size)  # 设置背景对话框
pygame.display.set_caption("PlaneWars")  # 设置游戏的标题
pygame.mixer.music.play(-1)     # 设置背景音乐，-1代表循环播放
background = pygame.image.load(os.path.join(BASE_DIR, "static/image/background.png"))  # 加载背景图片,并设置为不透明



SmallEnemy_list = []    # 存储实例化的小型机对象
MiddleEnemy_list = []    # 存储实例化的中型机对象
BigEnemy_list = []    # 存储实例化的大型机对象
def smallplane(num):
    """
    生成小型敌机的函数
    :param num:
    :return:
    """
    for i in range(num):
        smallplane = SmallEnemy(bg_size,screen)
        SmallEnemy_list.append(smallplane)
def middleplane(num):
    """
    生成中型敌机的函数
    :param num:
    :return:
    """
    for i in range(num):
        middleplane = MiddleEnemy(bg_size,screen)
        MiddleEnemy_list.append(middleplane)
def bigplane(num):
    """
    生成中型敌机的函数
    :param num:
    :return:
    """
    for i in range(num):
        bigplane = BigEnemy(bg_size,screen)
        BigEnemy_list.append(bigplane)

smallplane(6)   # 起始时生成6架小型机
middleplane(2)   # 起始时生成6架小型机
bigplane(1)   # 起始时生成6架小型机

our_plane = OurPlane(bg_size,screen,SmallEnemy_list,MiddleEnemy_list,BigEnemy_list)    # 实例化英雄飞机


while True:
    screen.blit(background, (0, 0))     # 绘制背景图

    clock = pygame.time.Clock()     # 控制每个循环多长时间运行一次
    clock.tick(60)    # 将帧数设置成60，即每秒运行60次

    for small_enemy in SmallEnemy_list:     # 生成小型机+摧毁时的动画效果
        if small_enemy.active:
            small_enemy.display()
        else:    # 当active=False时
            small_enemy.destroy()

    for middle_enemy in MiddleEnemy_list:
        if middle_enemy.active:
            middle_enemy.display()
        else:  # 当active=False时
            middle_enemy.destroy()

    for bid_enemy in BigEnemy_list:
        if bid_enemy.active:
            bid_enemy.display()
        else:  # 当active=False时
            bid_enemy.destroy()


    if our_plane.active:    # 如果飞机存活
        our_plane.display()

    else:   # 飞机死亡
        our_plane.destroy()

    # 调用 pygame 实现的碰撞方法 spritecollide (我方飞机如果和敌机碰撞, 更改飞机的存活属性)
    enemies_down1 = pygame.sprite.spritecollide(our_plane, SmallEnemy_list, False, pygame.sprite.collide_mask)
    enemies_down2 = pygame.sprite.spritecollide(our_plane, MiddleEnemy_list, False, pygame.sprite.collide_mask)
    enemies_down3 = pygame.sprite.spritecollide(our_plane, BigEnemy_list, False, pygame.sprite.collide_mask)
    if enemies_down1 or enemies_down2 or enemies_down3:    # 如果与敌机碰撞，将hero和敌机全部消灭
        our_plane.active = False
        for row in SmallEnemy_list:
            row.active = False
        for row in MiddleEnemy_list:
            row.active = False
        for row in BigEnemy_list:
            row.active = False

# =============================================================================================

    for event in pygame.event.get():   # 获取用户点击的事件
        if event.type == 12:  # 如果用户按下屏幕上的关闭按钮，触发QUIT事件，程序退出
            pygame.quit()
            sys.exit()

    key_pressed = pygame.key.get_pressed()      # 检测键盘
    if key_pressed[K_w] or key_pressed[K_UP]:
        our_plane.move_up()
    if key_pressed[K_s] or key_pressed[K_DOWN]:
        our_plane.move_down()
    if key_pressed[K_a] or key_pressed[K_LEFT]:
        our_plane.move_left()
    if key_pressed[K_d] or key_pressed[K_RIGHT]:
        our_plane.move_right()

    pygame.display.flip()   # 绘制图像并输出到屏幕上面
