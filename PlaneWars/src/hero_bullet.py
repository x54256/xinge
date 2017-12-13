import pygame,os
from config.settings import BASE_DIR

class HeroBullet(pygame.sprite.Sprite):
    def __init__(self,position):
        super(HeroBullet,self).__init__()
        self.image = pygame.image.load(os.path.join(BASE_DIR,'static/image/bullet1.png'))
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = position[0]-5,position[1]-25
        self.speed = 30
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        """
        子弹移动, 超出屏幕范围, 则设置死亡
        :return:
        """
        if self.rect.top < 0:
            self.active = False
        else:
            self.rect.top -= self.speed