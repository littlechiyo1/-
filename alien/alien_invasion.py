import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from scoreboard import Scoreboard


class AlienInvasion:
    """管理游戏资源和行为类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        # 设置窗口大小，例：800x600
        window_width = 1440
        window_height = 980
        self.screen = pygame.display.set_mode((window_width, window_height))
        self.settings.screen_width = window_width
        self.settings.screen_height = window_height
        pygame.display.set_caption("外星人入侵")

        # 初始化音乐
        pygame.mixer.init()
        self.menu_music = pygame.mixer.Sound(self.settings.menu_bgm)  # 主界面bgm
        self.game_music = pygame.mixer.Sound(self.settings.game_bgm)  # 游戏界面bgm
        self.game_over_music = pygame.mixer.Sound(self.settings.game_over_bgm)  # 失败音效
        self.bullet_music = pygame.mixer.Sound(self.settings.bullet_bgm)  # 子弹音效

        # 播放主菜单音乐
        self.menu_music.play(-1)  # -1表示循环播放

        # 创建一个用于存储游戏统计信息的实例，并创建记分牌
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # 加载背景图像列表
        self.background_images = [
            pygame.image.load(self.settings.game_background_image_1).convert(),
            pygame.image.load(self.settings.game_background_image_2).convert(),
            pygame.image.load(self.settings.game_background_image_3).convert()
        ]
        self.background_images = [
            pygame.transform.scale(bg, (self.settings.screen_width, self.settings.screen_height))
            for bg in self.background_images
        ]
        self.background_preview_rects = []

        self.current_background_index = 0
        self.background = self.background_images[self.current_background_index]

        # 加载按钮背景图像
        self.button_image = pygame.image.load(self.settings.button_background_image).convert()
        self.button_image = pygame.transform.scale(self.button_image, (200, 50))  # 假设按钮尺寸为200x50

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # 初始化射击状态
        self.bullet_fire = False  # 默认为False，表示未射击

        # 初始化射击计时器
        self.last_shot_time = 0  # 上次射击的时间

        # 初始化外星人生成计时器
        self.last_alien_spawn_time = 0  # 上次生成外星人的时间

        # 初始化字体
        self.font = pygame.font.SysFont(self.settings.font_path, self.settings.font_size)

        # 游戏启动后处于准备状态
        self.game_active = False
        self.show_menu = True  # 显示准备界面
        self.show_settings = False  # 显示设置界面

        # 初始化按钮
        self._init_buttons()

        # 初始化暂停状态
        self.paused = False

        # 初始化暂停界面
        self._init_pause_screen()

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            if self.game_active:
                if not self.paused:
                    # 隐藏光标
                    pygame.mouse.set_visible(False)
                    # 重置得分
                    self.sb.prep_score()
                    # 显示难度等级
                    self.sb.prep_level()
                    self.ship.update()
                    # 根据self.bullet_fire状态进行射击
                    if self.bullet_fire:
                        self._fire_bullet()
                    self._update_bullets()
                    self._update_aliens()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        # 监听键盘和鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.paused:
                    self._check_pause_buttons(mouse_pos)
                elif not self.paused:
                    self._check_buttons(mouse_pos)

    # 处理键盘按下事件
    def _check_keydown_events(self, event):
        """响应按下"""
        if event.key == pygame.K_d:
            # 向右移动飞船
            self.ship.moving_right = True
        elif event.key == pygame.K_a:
            # 向左移动飞船
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self.bullet_fire = True
            self.bullet_music.play(-1)
        elif event.key == pygame.K_q:
            self.paused = not self.paused
            if self.paused:
                pygame.mixer.pause()  # 暂停所有音乐
            else:
                pygame.mixer.unpause()  # 继续所有音乐

    # 处理键盘松开事件
    def _check_keyup_events(self, event):
        """响应释放"""
        if event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_a:
            self.ship.moving_left = False
        elif event.key == pygame.K_SPACE:
            self.bullet_fire = False
            self.bullet_music.stop()

    def _init_buttons(self):
        """初始化游戏按钮"""
        button_width, button_height = 200, 50
        screen_rect = self.screen.get_rect()

        # 开始游戏按钮
        self.start_button_rect = pygame.Rect(0, 0, button_width, button_height)
        self.start_button_rect.centerx = screen_rect.centerx
        self.start_button_rect.centery = screen_rect.centery - 50

        # 游戏设置按钮
        self.settings_button_rect = pygame.Rect(0, 0, button_width, button_height)
        self.settings_button_rect.centerx = screen_rect.centerx
        self.settings_button_rect.centery = screen_rect.centery + 60

        # 主界面的退出游戏按钮
        self.main_quit_button_rect = pygame.Rect(0, 0, button_width, button_height)
        self.main_quit_button_rect.centerx = screen_rect.centerx
        self.main_quit_button_rect.centery = screen_rect.centery + 170

        # 重新开始按钮
        self.restart_button_rect = pygame.Rect(0, 0, button_width, button_height)
        self.restart_button_rect.centerx = screen_rect.centerx
        self.restart_button_rect.centery = screen_rect.centery + 60

        # 返回暂停界面按钮
        self.back_to_pause_button_rect = pygame.Rect(0, 0, button_width, button_height)
        self.back_to_pause_button_rect.center = screen_rect.center
        self.back_to_pause_button_rect.y = screen_rect.centery + 180
        self.back_to_pause_button_text = self.font.render("返回游戏", True, (255, 255, 255))

        # 返回主界面按钮
        self.back_to_menu_button_rect = pygame.Rect(0, 0, button_width, button_height)
        self.back_to_menu_button_rect.centerx = screen_rect.centerx
        self.back_to_menu_button_rect.centery = screen_rect.centery + 120

        # 游戏结束的退出按钮
        self.game_over_quit_button_rect = pygame.Rect(0, 0, button_width, button_height)
        self.game_over_quit_button_rect.centerx = screen_rect.centerx
        self.game_over_quit_button_rect.centery = screen_rect.centery + 180

        self.button_font = pygame.font.SysFont(self.settings.font_path, self.settings.font_size)
        self.start_button_text = self.button_font.render("开始游戏", True, self.settings.button_text_color)
        self.settings_button_text = self.button_font.render("游戏设置", True, self.settings.button_text_color)
        self.main_quit_button_text = self.button_font.render("退出游戏", True, self.settings.button_text_color)
        self.restart_button_text = self.button_font.render("重新开始", True, self.settings.button_text_color)
        self.game_over_quit_button_text = self.button_font.render("退出", True, self.settings.button_text_color)
        self.back_to_menu_button_text = self.button_font.render("返回主界面", True, self.settings.button_text_color)

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.blit(self.background, (0, 0))  # 绘制背景图像

        # 主界面
        if self.show_menu:
            self._draw_menu()
        # 设置界面
        elif self.show_settings:
            self._draw_settings()
        else:
            if not self.paused:
                for bullet in self.bullets.sprites():
                    bullet.draw_bullet()
                self.ship.blitme()

                # 显示得分
                self.sb.show_score()

                # 绘制外星人
                self.aliens.draw(self.screen)

                # 绘制射击速度
                self.sb._draw_imfomation()

            # 如果游戏处于暂停状态，显示暂停界面
            if self.paused:
                self._draw_pause_screen()

            if not self.game_active:
                self._draw_game_over_screen()

        # 让最近绘制的屏幕可见
        pygame.display.flip()

    def _draw_menu(self):
        """绘制游戏主界面"""
        self.screen.blit(self.background, (0, 0))  # 绘制背景图像

        # 显示光标
        pygame.mouse.set_visible(True)

        # 绘制开始游戏按钮
        self.screen.blit(self.button_image, self.start_button_rect)
        start_button_text_rect = self.start_button_text.get_rect()
        start_button_text_rect.center = self.start_button_rect.center
        self.screen.blit(self.start_button_text, start_button_text_rect)

        # 绘制游戏设置按钮
        self.screen.blit(self.button_image, self.settings_button_rect)
        settings_button_text_rect = self.settings_button_text.get_rect()
        settings_button_text_rect.center = self.settings_button_rect.center
        self.screen.blit(self.settings_button_text, settings_button_text_rect)

        # 绘制退出游戏按钮
        self.screen.blit(self.button_image, self.main_quit_button_rect)
        main_quit_button_text_rect = self.main_quit_button_text.get_rect()
        main_quit_button_text_rect.center = self.main_quit_button_rect.center
        self.screen.blit(self.main_quit_button_text, main_quit_button_text_rect)

    def _check_buttons(self, mouse_pos):
        """在游戏准备界面或游戏结束界面检查按钮点击事件"""
        # 主界面
        if self.show_menu:
            # 从主界面开始游戏
            if self.start_button_rect.collidepoint(mouse_pos):
                self.show_menu = False
                self._reset_game()
                self.menu_music.stop()  # 停止主菜单音乐
                self.game_music.play(-1)  # 播放游戏音乐
            # 从主界面打开设置
            elif self.settings_button_rect.collidepoint(mouse_pos):
                self.show_menu = False
                self.show_settings = True
            # 从主界面退出游戏
            elif self.main_quit_button_rect.collidepoint(mouse_pos):
                sys.exit()
        # 设置界面
        elif self.show_settings:
            # 从设置界面返回主界面
            if self.back_to_menu_button_rect.collidepoint(mouse_pos):
                self.show_settings = False
                self.show_menu = True
            elif self.back_to_pause_button_rect.collidepoint(mouse_pos):
                self.show_settings = False
                self.paused = True
            else:
                self._check_setting_buttons(mouse_pos)
        # 暂停界面
        elif self.paused:
            if self.continue_button_rect.collidepoint(mouse_pos):
                self.paused = False
                pygame.mixer.unpause()  # 继续所有音乐
            elif self.return_main_menu_button_rect.collidepoint(mouse_pos):
                self.paused = False
                self.show_menu = True
            elif self.pause_settings_button_rect.collidepoint(mouse_pos):
                self.paused = True
                self.show_settings = True
            elif self.quit_button_pause_rect.collidepoint(mouse_pos):
                sys.exit()
        # 没开始游戏
        elif not self.game_active:
            # 重新开始游戏
            if self.restart_button_rect.collidepoint(mouse_pos):
                self._reset_game()
            # 返回主界面
            elif self.back_to_menu_button_rect.collidepoint(mouse_pos):
                self.show_settings = False
                self.show_menu = True
            # 退出游戏
            elif self.game_over_quit_button_rect.collidepoint(mouse_pos):
                sys.exit()

    def _draw_settings(self):
        """绘制设置界面"""
        self.screen.blit(self.background, (0, 0))  # 绘制背景图像

        # 显示光标
        pygame.mouse.set_visible(True)

        # 新增显示背景文字
        title_str = "背景（点击以切换）："
        title_image = self.font.render(title_str, True, self.settings.text_color)
        title_rect = title_image.get_rect()
        title_rect.topleft = (self.settings.screen_width // 1 - title_rect.width // 1, 50)
        self.screen.blit(title_image, title_rect)

        # 获取设置参数并绘制在屏幕上
        fire_speed_str = f"射击速度: {self.settings.fire_speed} 颗/s"
        ship_speed_str = f"飞船速度: {self.settings.ship_speed} 像素/s"
        alien_speed_str = f"外星人速度: {self.settings.alien_speed} 像素/s"
        alien_spawn_str = f"生成速度: {self.settings.alien_spawn_time_str} 个/s"

        fire_speed_image = self.font.render(fire_speed_str, True, self.settings.text_color)
        ship_speed_image = self.font.render(ship_speed_str, True, self.settings.text_color)
        alien_speed_image = self.font.render(alien_speed_str, True, self.settings.text_color)
        alien_spawn_image = self.font.render(alien_spawn_str, True, self.settings.text_color)

        fire_speed_rect = fire_speed_image.get_rect()
        ship_speed_rect = ship_speed_image.get_rect()
        alien_speed_rect = alien_speed_image.get_rect()
        alien_spawn_rect = alien_spawn_image.get_rect()

        fire_speed_rect.topleft = (100, 100)
        ship_speed_rect.topleft = (100, 150)
        alien_speed_rect.topleft = (100, 200)
        alien_spawn_rect.topleft = (100, 250)

        self.screen.blit(fire_speed_image, fire_speed_rect)
        self.screen.blit(ship_speed_image, ship_speed_rect)
        self.screen.blit(alien_speed_image, alien_speed_rect)
        self.screen.blit(alien_spawn_image, alien_spawn_rect)

        # 绘制小方框框住文字
        pygame.draw.rect(self.screen, (255, 255, 255), title_rect, 2)

        # 增加和减少按钮
        button_width, button_height = 50, 30
        self._draw_setting_buttons("fire_speed", fire_speed_rect, button_width, button_height)
        self._draw_setting_buttons("ship_speed", ship_speed_rect, button_width, button_height)
        self._draw_setting_buttons("alien_speed", alien_speed_rect, button_width, button_height)
        self._draw_setting_buttons("alien_spawn_time_str", alien_spawn_rect, button_width, button_height)

        # 绘制预览图及其小方框
        preview_width, preview_height = 200, 100
        preview_spacing = 20
        preview_x = self.settings.screen_width - preview_width - 50
        preview_y = 100

        self.background_preview_rects = []

        for i, bg_image in enumerate(self.background_images):
            preview_rect = pygame.Rect(preview_x, preview_y + (preview_height + preview_spacing) * i, preview_width,
                                       preview_height)
            self.background_preview_rects.append(preview_rect)
            scaled_bg_image = pygame.transform.scale(bg_image, (preview_width, preview_height))
            self.screen.blit(scaled_bg_image, preview_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), preview_rect, 2)  # 绘制小方框框住预览图

        # 绘制返回主界面按钮
        self.screen.blit(self.button_image, self.back_to_menu_button_rect)
        back_to_menu_button_text_rect = self.back_to_menu_button_text.get_rect()
        back_to_menu_button_text_rect.center = self.back_to_menu_button_rect.center
        self.screen.blit(self.back_to_menu_button_text, back_to_menu_button_text_rect)

        # 绘制返回游戏按钮（从设置界面返回暂停界面）
        self.screen.blit(self.button_image, self.back_to_pause_button_rect)
        back_to_pause_button_text_rect = self.back_to_pause_button_text.get_rect()
        back_to_pause_button_text_rect.center = self.back_to_pause_button_rect.center
        self.screen.blit(self.back_to_pause_button_text, back_to_pause_button_text_rect)

    def _draw_pause_screen(self):
        """绘制暂停界面"""
        self.screen.blit(self.pause_screen_bg, (0, 0))

        # 显示光标
        pygame.mouse.set_visible(True)

        # 绘制“继续游戏”按钮
        self.screen.blit(self.button_image, self.continue_button_rect)
        self.screen.blit(self.continue_text, self.continue_text_rect)

        # 绘制“返回主界面”按钮
        self.screen.blit(self.button_image, self.return_main_menu_button_rect)
        self.screen.blit(self.return_main_menu_text, self.return_main_menu_text_rect)

        # 绘制“游戏设置”按钮
        self.screen.blit(self.button_image, self.pause_settings_button_rect)
        self.screen.blit(self.pause_settings_text, self.pause_settings_text_rect)

        # 绘制“退出游戏”按钮
        self.screen.blit(self.button_image, self.quit_button_pause_rect)
        self.screen.blit(self.quit_button_pause_text, self.quit_button_pause_text_rect)

    def _draw_setting_buttons(self, setting_name, rect, button_width, button_height):
        """绘制增加和减少按钮"""
        increase_button_rect = pygame.Rect(rect.right + 10, rect.centery - button_height // 2, button_width,
                                           button_height)
        decrease_button_rect = pygame.Rect(rect.left - button_width - 10, rect.centery - button_height // 2,
                                           button_width, button_height)

        # 绘制按钮背景图像
        increase_button_image = pygame.transform.scale(self.button_image, (button_width, button_height))
        decrease_button_image = pygame.transform.scale(self.button_image, (button_width, button_height))

        self.screen.blit(increase_button_image, increase_button_rect.topleft)
        self.screen.blit(decrease_button_image, decrease_button_rect.topleft)

        increase_text = self.font.render("+", True, self.settings.button_text_color)
        decrease_text = self.font.render("-", True, self.settings.button_text_color)

        increase_text_rect = increase_text.get_rect()
        decrease_text_rect = decrease_text.get_rect()

        increase_text_rect.center = increase_button_rect.center
        decrease_text_rect.center = decrease_button_rect.center

        self.screen.blit(increase_text, increase_text_rect)
        self.screen.blit(decrease_text, decrease_text_rect)

        setattr(self, f"{setting_name}_increase_button_rect", increase_button_rect)
        setattr(self, f"{setting_name}_decrease_button_rect", decrease_button_rect)

    def _change_background(self, index):
        """更改游戏背景图像"""
        if 0 <= index < len(self.background_images):
            self.current_background_index = index
            self.background = self.background_images[index]

    def _check_setting_buttons(self, mouse_pos):
        """检查设置界面的按钮点击事件"""
        settings = {
            "fire_speed": (1, 10),
            "ship_speed": (1, 10),
            "alien_speed": (1, 10),
            "alien_spawn_time_str": (1, 10)
        }
        for setting, (min_value, max_value) in settings.items():
            increase_button_rect = getattr(self, f"{setting}_increase_button_rect")
            decrease_button_rect = getattr(self, f"{setting}_decrease_button_rect")
            current_value = getattr(self.settings, setting)

            if increase_button_rect.collidepoint(mouse_pos):
                if current_value < max_value:
                    setattr(self.settings, setting, current_value + 1)
            elif decrease_button_rect.collidepoint(mouse_pos):
                if current_value > min_value:
                    setattr(self.settings, setting, current_value - 1)

        # 检查背景预览图点击事件
        for i, preview_rect in enumerate(self.background_preview_rects):
            if preview_rect.collidepoint(mouse_pos):
                self._change_background(i)
                break

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets"""
        current_time = pygame.time.get_ticks()  # 获取当前时间
        # 根据fire_speed来决定是否可以射击
        if self.bullet_fire and current_time - self.last_shot_time > 1000 / self.settings.fire_speed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.last_shot_time = current_time  # 更新上次射击的时间

    def _update_bullets(self):
        """更新子弹位置并删除已消失的子弹"""
        # 更新子弹的位置
        self.bullets.update()

        # 删除已消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # 检查是否有子弹击中了外星人
        # 如果是，就删除相应的子弹和外星人
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

    def _create_alien(self):
        """创建一个新的外星人"""
        alien = Alien(self)
        self.aliens.add(alien)

    def _create_fleet(self):
        """创建外星舰队"""
        # 创建一个外星人
        alien = Alien(self)
        self.aliens.add(alien)

    def _update_aliens(self):
        """更新外星人位置并删除已消失的外星人"""
        self.aliens.update()

        # 更新外星人生成时间
        self.alien_spawn_time = 1000 / self.settings.alien_spawn_time_str

        # 检查是否需要生成新的外星人
        current_time = pygame.time.get_ticks()
        if current_time - self.last_alien_spawn_time > self.alien_spawn_time:
            self._create_alien()
            self.last_alien_spawn_time = current_time  # 更新上次生成外星人的时间

        # 删除已消失的外星人
        for alien in self.aliens.copy():
            if alien.rect.top > self.settings.screen_height:
                self.aliens.remove(alien)

        # 检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    def _ship_hit(self):
        """响应飞船和外星人的碰撞"""
        if self.stats.ships_left > 1:
            # 将ships_left减一
            self.stats.ships_left -= 1

            # 删除与飞船碰撞的外星人
            collided_alien = pygame.sprite.spritecollideany(self.ship, self.aliens)
            if collided_alien:
                self.aliens.remove(collided_alien)

        else:
            self.game_active = False
            self._end_game()
            self.stats.reset_stats()  # 重置游戏统计信息和难度设置

    def _end_game(self):
        """处理游戏结束情况"""
        # 显示游戏结束信息
        self._draw_game_over_screen()
        pygame.display.flip()
        # 停止游戏音乐
        self.game_music.stop()
        # 播放游戏失败音效
        self.game_over_music.play()

    def _init_pause_screen(self):
        """初始化暂停界面"""
        self.pause_screen_bg = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
        self.pause_screen_bg.set_alpha(128)  # 半透明效果
        self.pause_screen_bg.fill((0, 0, 0))  # 黑色背景

        # 创建“继续游戏”按钮
        button_width, button_height = 200, 50
        button_x = self.settings.screen_width // 2 - button_width // 2
        button_y = self.settings.screen_height // 2 - button_height // 2

        self.continue_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        self.continue_text = self.font.render("继续游戏", True, self.settings.button_text_color)
        self.continue_text_rect = self.continue_text.get_rect(center=self.continue_button_rect.center)

        # 创建“返回主界面”按钮
        self.return_main_menu_button_rect = pygame.Rect(button_x, button_y + 60, button_width, button_height)
        self.return_main_menu_text = self.font.render("返回主界面", True, self.settings.button_text_color)
        self.return_main_menu_text_rect = self.return_main_menu_text.get_rect(
            center=self.return_main_menu_button_rect.center)

        # 创建“游戏设置”按钮
        self.pause_settings_button_rect = pygame.Rect(button_x, button_y + 120, button_width, button_height)
        self.pause_settings_text = self.font.render("游戏设置", True, self.settings.button_text_color)
        self.pause_settings_text_rect = self.pause_settings_text.get_rect(center=self.pause_settings_button_rect.center)

        # 创建“退出游戏”按钮
        self.quit_button_pause_rect = pygame.Rect(button_x, button_y + 180, button_width, button_height)
        self.quit_button_pause_text = self.font.render("退出游戏", True, self.settings.button_text_color)
        self.quit_button_pause_text_rect = self.quit_button_pause_text.get_rect(
            center=self.quit_button_pause_rect.center)

    def _draw_game_over_screen(self):
        """绘制游戏结束界面"""
        screen_rect = self.screen.get_rect()

        # 显示光标
        pygame.mouse.set_visible(True)

        # 绘制半透明黑色背景
        game_over_bg = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
        game_over_bg.set_alpha(128)  # 半透明效果
        game_over_bg.fill((0, 0, 0))  # 黑色背景
        self.screen.blit(game_over_bg, (0, 0))

        # 绘制游戏结束文字（绿色）
        end_text_str = "游戏结束"
        end_text_image = self.font.render(end_text_str, True, (0, 255, 0))  # 绿色文本
        end_text_rect = end_text_image.get_rect()
        end_text_rect.center = screen_rect.center  # 设置为窗口中央
        end_text_rect.y -= 100  # 适当向上移动100像素，使其居中
        self.screen.blit(end_text_image, end_text_rect)

        # 按钮的初始y坐标
        button_start_y = end_text_rect.bottom + 50
        button_spacing = 60  # 按钮之间的间距

        # 绘制重新开始按钮
        self.restart_button_rect.midtop = (screen_rect.centerx, button_start_y)
        self.screen.blit(self.button_image, self.restart_button_rect)
        restart_button_text_rect = self.restart_button_text.get_rect()
        restart_button_text_rect.center = self.restart_button_rect.center
        self.screen.blit(self.restart_button_text, restart_button_text_rect)

        # 绘制返回主界面按钮
        self.back_to_menu_button_rect.midtop = (screen_rect.centerx, button_start_y + button_spacing)
        self.screen.blit(self.button_image, self.back_to_menu_button_rect)
        back_to_menu_button_text_rect = self.back_to_menu_button_text.get_rect()
        back_to_menu_button_text_rect.center = self.back_to_menu_button_rect.center
        self.screen.blit(self.back_to_menu_button_text, back_to_menu_button_text_rect)

        # 绘制退出按钮
        self.game_over_quit_button_rect.midtop = (screen_rect.centerx, button_start_y + 2 * button_spacing)
        self.screen.blit(self.button_image, self.game_over_quit_button_rect)
        game_over_quit_button_text_rect = self.game_over_quit_button_text.get_rect()
        game_over_quit_button_text_rect.center = self.game_over_quit_button_rect.center
        self.screen.blit(self.game_over_quit_button_text, game_over_quit_button_text_rect)

    def _check_pause_buttons(self, mouse_pos):
        if self.continue_button_rect.collidepoint(mouse_pos):
            print("继续游戏按钮被点击")
            self.paused = False
            pygame.mixer.unpause()  # 继续所有音乐
        elif self.return_main_menu_button_rect.collidepoint(mouse_pos):
            print("返回主界面按钮被点击")
            self.paused = False
            self.show_menu = True
        elif self.pause_settings_button_rect.collidepoint(mouse_pos):
            print("游戏设置按钮被点击")
            self.paused = False
            self.show_settings = True
        elif self.quit_button_pause_rect.collidepoint(mouse_pos):
            print("退出游戏按钮被点击")
            sys.exit()

    def _reset_game(self):
        """重置游戏"""
        self.stats.reset_stats()
        self.aliens.empty()
        self.bullets.empty()
        self._create_fleet()
        self.ship.center_ship()
        self.game_active = True
        self.settings.initialize_dynamic_settings()  # 重置游戏难度设置


if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
