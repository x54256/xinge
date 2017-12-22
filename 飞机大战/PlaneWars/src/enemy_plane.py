import pygame,random,os
from config.settings import *


class BaseEnemy(pygame.sprite.Sprite):
    def __init__(self,bg_size,screen,img,speed,energy,plane_type):
        super(BaseEnemy,self).__init__()
        self.screen = screen  # 画布
        self.plane_type = plane_type  # 飞机类型
        self.energy = energy  # 血量
        self.e1_destroy_index = 0  # 敌机的图片序号
        self.color_green = (0, 255, 0)
        self.color_red = (255, 0, 0)
        self.image = pygame.image.load(os.path.join(BASE_DIR,img))  # 小型机的图片
        self.rect = self.image.get_rect()  # 获取敌机的初始位置 <==> 长宽
        self.width, self.height = bg_size[0], bg_size[1]  # 获取窗口的大小
        self.mask = pygame.mask.from_surface(self.image)  # 获取飞机图像的掩膜用以更加精确的碰撞检测
        self.speed = speed  # 初始速度
        self.enemy_bullet_list = []
        self.rect.left, self.rect.top = (
            random.randint(0, self.width - self.rect.width),  # 随机生成出来的横坐标
            random.randint(-25 * self.rect.height, -55)  # 随机生成出来的初始纵坐标
        )
        self.active = True  # 是否存活

    def reset(self):
        """
        如果飞机超出屏幕界限+摧毁，将原来的内架飞机生成一个随机位置重新显示
        :return:
        """
        self.rect.left, self.rect.top = (random.randint(0, self.width - self.rect.width), random.randint(-5 * self.rect.height, 0))
        self.active = True
        if self.plane_type == 'SmallEnemy':
            self.energy = SmallEnemy.energy
        elif self.plane_type == 'MiddleEnemy':
            self.energy = MiddleEnemy.energy
        elif self.plane_type == 'BigEnemy':
            self.energy = BigEnemy.energy

    def move(self):
        """
        定义敌机的移动函数
        :return:
        """
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def display(self):
        self.screen.blit(self.image,self.rect)     # 显示每一架小型机
        self.move()    # 往下走

        if self.plane_type == 'SmallEnemy':
            energy_remain = self.energy / SmallEnemy.energy  # 如果血量大约百分之二十则为绿色，否则为红色
        elif self.plane_type == 'MiddleEnemy':
            energy_remain = self.energy / MiddleEnemy.energy  # 如果血量大约百分之二十则为绿色，否则为红色
        elif self.plane_type == 'BigEnemy':
            energy_remain = self.energy / BigEnemy.energy  # 如果血量大约百分之二十则为绿色，否则为红色
        if energy_remain > 0.2:
            energy_color = self.color_green
        else:
            energy_color = self.color_red
        pygame.draw.line(self.screen, energy_color,  # 画血量的内条线
                         (self.rect.left, self.rect.top - 5),
                         (self.rect.left + self.rect.width * energy_remain, self.rect.top - 5),
                         2)

    def destroy(self):
        self.screen.blit(self.destroy_images[self.e1_destroy_index],self.rect)      # 显示小型机爆炸的图片
        self.e1_destroy_index = (self.e1_destroy_index + 1) % 4
        if self.e1_destroy_index == 0:
            if self.plane_type == 'SmallEnemy':
                enemy1_down_sound.play()  # 播放摧毁的音效
            elif self.plane_type == 'MiddleEnemy':
                enemy2_down_sound.play()  # 播放摧毁的音效
            elif self.plane_type == 'BigEnemy':
                enemy3_down_sound.play()    # 播放摧毁的音效
            self.reset()   # 重新生成小型机

class SmallEnemy(BaseEnemy):
    energy = 1
    def __init__(self,bg_size,screen):
        super(SmallEnemy,self).__init__(bg_size,screen,"static/image/enemy1.png",2,1,'SmallEnemy')
        self.destroy_images = []
        self.destroy_images.extend(     # 加载飞机损毁图片
            [
                pygame.image.load(os.path.join(BASE_DIR,"static/image/enemy1_down1.png")),
                pygame.image.load(os.path.join(BASE_DIR,"static/image/enemy1_down2.png")),
                pygame.image.load(os.path.join(BASE_DIR,"static/image/enemy1_down3.png")),
                pygame.image.load(os.path.join(BASE_DIR,"static/image/enemy1_down4.png"))
            ]
        )

class MiddleEnemy(BaseEnemy):
    energy = 3
    def __init__(self,bg_size,screen):
        super(MiddleEnemy,self).__init__(bg_size,screen,"static/image/enemy2.png",1,3,'MiddleEnemy')
        self.destroy_images = []
        self.destroy_images.extend(     # 加载飞机损毁图片
            [
                pygame.image.load(os.path.join(BASE_DIR,"static/image/enemy2_down1.png")),
                pygame.image.load(os.path.join(BASE_DIR,"static/image/enemy2_down2.png")),
                pygame.image.load(os.path.join(BASE_DIR,"static/image/enemy2_down3.png")),
                pygame.image.load(os.path.join(BASE_DIR,"static/image/enemy2_down4.png"))
            ]
        )


class BigEnemy(BaseEnemy):
    energy = 10
    def __init__(self,bg_size,screen):
        super(BigEnemy,self).__init__(bg_size,screen,"static/image/enemy3_hit.png",1,10,'BigEnemy')
        self.destroy_images = []
        self.destroy_images.extend(     # 加载飞机损毁图片
            [
                pygame.image.load(os.path.join(BASE_DIR,"static/image/enemy3_down1.png")),
                pygame.image.load(os.path.join(BASE_DIR,"static/image/enemy3_down2.png")),
                pygame.image.load(os.path.join(BASE_DIR,"static/image/enemy3_down3.png")),
                pygame.image.load(os.path.join(BASE_DIR,"static/image/enemy3_down4.png")),
                pygame.image.load(os.path.join(BASE_DIR,"static/image/enemy3_down5.png")),
                pygame.image.load(os.path.join(BASE_DIR,"static/image/enemy3_down6.png")),
            ]
        )


