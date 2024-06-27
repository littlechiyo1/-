import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """管理飞船所发子弹的类"""

    def __init__(self, ai_game):
        """在飞船当前位置创建一个子弹对象"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # 在（0，0）处创建一个表示子弹的矩形，在设置正确的位置
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # 存储用浮点数表示的子弹位置
        self.y = float(self.rect.y)

    def update(self):
        """根据移动标志调整子弹的发射（依次向上移动子弹）"""
        # 更新子弹的准确位置
        self.y -= self.settings.bullet_speed
        # 更新表示子弹的rect位置
        self.rect.y = self.y

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets"""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
