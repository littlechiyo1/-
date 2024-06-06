import pygame.font


class Scoreboard:
    """显示得分信息的类"""

    def __init__(self, ai_game):
        """初始化显示得分涉及的属性"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # 显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont('KaiTi', 48)

        # 准备得分和最高分图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()

    def prep_score(self):
        """将得分渲染为图像"""
        rounded_score = round(self.stats.score, 0)
        score_str = f"当前得分: {rounded_score:,}"
        self.score_image = self.font.render(score_str, True,
                                            self.text_color)

        # 在屏幕左上角显示得分
        self.score_rect = self.score_image.get_rect()
        self.score_rect.left = self.screen_rect.left + 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """将最高分渲染为图像"""
        high_score = round(self.stats.high_score, 0)
        high_score_str = f"最高得分: {high_score:,}"
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color)

        # 在屏幕上方显示最高分
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """将等级渲染为图像"""
        level_str = f"当前难度等级: {str(self.stats.level)}"
        self.level_image = self.font.render(level_str, True,
                                            self.text_color)

        # 将等级放在得分下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = self.score_rect.left
        self.level_rect.top = self.score_rect.bottom + 10

    def check_high_score(self):
        """检查是否诞生了新的最高分"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        """在屏幕上显示得分和等级"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)

    def _draw_imfomation(self):
        """在屏幕右上角显示当前的射击速度、飞船速度、外星人速度和生成间隔"""
        fire_speed_str = f"射击速度: {self.settings.fire_speed} 颗/s"
        ship_speed_str = f"飞船速度: {self.settings.ship_speed} 像素/s"
        alien_speed_str = f"外星人速度: {self.settings.alien_speed} 像素/s"
        alien_spawn_str = f"生成速度: {self.settings.alien_spawn_time_str} 个/s"

        # 绘制射击速度文本（绿色）
        fire_speed_image = self.font.render(fire_speed_str, True, self.text_color)
        fire_speed_rect = fire_speed_image.get_rect()
        fire_speed_rect.topright = (self.settings.screen_width - 20, 20)
        self.screen.blit(fire_speed_image, fire_speed_rect)

        # 绘制飞船速度文本（绿色）
        ship_speed_image = self.font.render(ship_speed_str, True, self.text_color)
        ship_speed_rect = ship_speed_image.get_rect()
        ship_speed_rect.topright = (self.settings.screen_width - 20, fire_speed_rect.bottom + 10)
        self.screen.blit(ship_speed_image, ship_speed_rect)

        # 绘制外星人速度文本（绿色）
        alien_speed_image = self.font.render(alien_speed_str, True, self.text_color)
        alien_speed_rect = alien_speed_image.get_rect()
        alien_speed_rect.topright = (self.settings.screen_width - 20, ship_speed_rect.bottom + 10)
        self.screen.blit(alien_speed_image, alien_speed_rect)

        # 绘制外星人生成间隔文本（绿色）
        alien_spawn_image = self.font.render(alien_spawn_str, True, self.text_color)
        alien_spawn_rect = alien_spawn_image.get_rect()
        alien_spawn_rect.topright = (self.settings.screen_width - 20, alien_speed_rect.bottom + 10)
        self.screen.blit(alien_spawn_image, alien_spawn_rect)