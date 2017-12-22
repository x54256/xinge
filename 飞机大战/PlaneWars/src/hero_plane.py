from config.settings import *
import os,pygame
from src.hero_bullet import HeroBullet

class OurPlane(pygame.sprite.Sprite):   # 该类实现了碰撞方法 spritecollide，我方飞机和敌方飞机指定掩膜属性以及生存状态标志位 添加 self.mask 属性(可以实现更精准的碰撞效果)
    def __init__(self,bg_size,screen,SmallEnemy_list,MiddleEnemy_list,BigEnemy_list):
        super(OurPlane,self).__init__()
        # 让两张图片不停的切换形成动态的效果
        self.image1 = pygame.image.load(os.path.join(BASE_DIR,'static/image/hero1.png'))
        self.image2 = pygame.image.load(os.path.join(BASE_DIR,'static/image/hero2.png'))
        self.width,self.height = bg_size[0],bg_size[1]      # 获取背景图片的宽度和高度
        self.rect = self.image1.get_rect()      # 获取飞机背景图片的初始位置
        self.mask = pygame.mask.from_surface(self.image1)   # 获取飞机图像的掩膜用以更加精确的碰撞检测
        self.rect.left,self.rect.top = (self.width - self.rect.width)//2 , (self.height - self.rect.height -60)     # 获取飞机初始的位置的宽高并更新rect的位置
        self.speed = 10     # 设置飞机初始移动速度
        self.active = True      # 设置飞机存活状态(True为存活, False为死亡)
        self.bullet_list = []    # 存子弹的[]
        self.delay = 60     # 对一些效果进行延迟, 设置成60和帧数一样，即1s内就减完了
        self.screen = screen
        self.SmallEnemy_list = SmallEnemy_list
        self.MiddleEnemy_list = MiddleEnemy_list
        self.BigEnemy_list = BigEnemy_list
        self.me_destroy_index = 0
        self.destroy_images = []
        self.destroy_images.extend(     # 加载飞机损毁图片
            [
                pygame.image.load(os.path.join(BASE_DIR, "static/image/hero_blowup_n1.png")),
                pygame.image.load(os.path.join(BASE_DIR, "static/image/hero_blowup_n2.png")),
                pygame.image.load(os.path.join(BASE_DIR, "static/image/hero_blowup_n3.png")),
                pygame.image.load(os.path.join(BASE_DIR, "static/image/hero_blowup_n4.png")),
            ]
        )


    def move_up(self):
        """
        飞机向上移动的操作函数，其余移动函数方法类似
        """
        if self.rect.top > 0:  # 如果飞机尚未移动出背景区域
            self.rect.top -= self.speed
        else:  # 若即将移动出背景区域，则及时纠正为背景边缘位置
            self.rect.top = 0

    def move_down(self):
        """
        飞机向下移动
        """
        if self.rect.bottom < self.height - 60:
            self.rect.top += self.speed
        else:
            self.rect.bottom = self.height - 60

    def move_left(self):
        """
        飞机向左移动
        """
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def move_right(self):
        """
        飞机向右移动
        """
        if self.rect.right < self.width:
            self.rect.right += self.speed
        else:
            self.rect.right = self.width

    def display(self):
        if self.delay % 2:  # 如果除2有余数
            self.screen.blit(self.image1, self.rect)  # 显示英雄飞机1
        else:
            self.screen.blit(self.image2, self.rect)  # 显示英雄飞机2

        if not (self.delay % 10):  # 发射子弹
            bullet = HeroBullet(self.rect.midtop)  # 获取当前飞机的位置
            self.bullet_list.append(bullet)
        bullet_list2 = []  # 用来存储要消失的子弹
        for i in self.bullet_list:
            bullet_sound.play()
            self.screen.blit(i.image, i.rect)  # 显示子弹
            i.move()  # 子弹移动

            enemies_hit1 = pygame.sprite.spritecollide(i, self.SmallEnemy_list, False, pygame.sprite.collide_mask)
            enemies_hit2 = pygame.sprite.spritecollide(i, self.MiddleEnemy_list, False, pygame.sprite.collide_mask)
            enemies_hit3 = pygame.sprite.spritecollide(i, self.BigEnemy_list, False, pygame.sprite.collide_mask)
            if enemies_hit1:  # 如果子弹击中小型飞机
                i.active = False  # 子弹损毁
                for e in enemies_hit1:
                    e.energy -= 0.9
                    if e.energy <= 0:
                        e.active = False  # 小型敌机损毁

            elif enemies_hit2:  # 如果子弹击中中型飞机
                i.active = False  # 子弹损毁
                for e in enemies_hit2:
                    e.energy -= 0.7
                    if e.energy <= 0:
                        e.active = False  # 中型敌机损毁
            elif enemies_hit3:  # 如果子弹击中中型飞机
                i.active = False  # 子弹损毁
                for e in enemies_hit3:
                    e.energy -= 0.6
                    if e.energy <= 0:
                        e.active = False  # 中型敌机损毁

            if not i.active:  # 将要消失的子弹从列表2中
                bullet_list2.append(i)
        for bullet2 in bullet_list2:  # 将要消失的子弹从列表中删除
            self.bullet_list.remove(bullet2)

        if self.delay == 0:  # 当减到0的时候，恢复60
            self.delay = 60
        else:
            self.delay -= 1  # 每次循环将delay减1

    def destroy(self):  # 飞机死亡
        self.screen.blit(self.destroy_images[self.me_destroy_index], self.rect)  # 按照[]的索引值输出摧毁时的图片
        self.me_destroy_index = (self.me_destroy_index + 1) % 4  # 增加索引值
        if self.me_destroy_index == 0:
            me_down_sound.play()
            self.reset()  # 重新生成英雄飞机

    def reset(self):
        self.rect.left,self.rect.top = (self.width - self.rect.width)//2 , (self.height - self.rect.height -60)     # 获取飞机初始的位置的宽高并更新rect的位置
        self.active = True

