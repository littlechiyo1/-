import pygame
import random
from pygame.sprite import Sprite


class Alien(Sprite):
    """表示单个外星人的类"""

    def __init__(self, ai_game):
        """初始化外星人并设置其起始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # 加载外星人图像并设置其rect属性
        self.image = pygame.image.load('images/alien_3.png')
        self.image = pygame.transform.scale(self.image, (80, 80))  # 缩放图像到50x100像素
        self.rect = self.image.get_rect()

        # 每个外星人最初都在屏幕顶部随机位置
        self.rect.x = random.randint(0, self.settings.screen_width - self.rect.width)
        self.rect.y = self.rect.height

        # 存储外星人的精确水平位置
        self.y = float(self.rect.y)

    def update(self):
        """向下移动外星人"""
        self.y += self.settings.alien_speed
        self.rect.y = self.y