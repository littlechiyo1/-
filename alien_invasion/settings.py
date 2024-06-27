class Settings:
    """存储所有设置的类"""

    def __init__(self):
        """初始化游戏的设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800

        # 文本设置
        self.font_path = "KaiTi"  # 字体文件的路径
        self.font_size = 38  # 字体大小

        # 音乐、音效设置
        self.menu_bgm = 'music/背景-1999.flac'
        self.game_bgm = 'music/背景-欢乐节拍.mp3'
        self.game_over_bgm = 'music/游戏失败-1.mp3'
        self.bullet_bgm = 'music/子弹-1.mp3'

        # 添加背景图像路径设置
        self.game_background_image_1 = 'images/back_1.jpg'
        self.game_background_image_2 = 'images/back_2.jpg'
        self.game_background_image_3 = 'images/back_3.jpg'
        self.button_background_image = 'images/button_1.png'

        # 颜色
        self.button_text_color = (0, 0, 0)  # 按钮颜色
        self.text_color = (0, 0, 0)  # 文本颜色

        # 难度等级设置
        self.level = 1
        # 定义提升难度的得分
        self.level_up_scores = [5, 10, 20, 50, 80, 100, 130, 140, 170, 190, 200, 215, 230, 250, 270, 290, 300]

        # 飞船移动速度
        self.ship_speed = 5  # 飞船速度，单位：像素/秒

        # 飞船血量
        self.ship_limit = 3

        # 子弹设置
        self.bullet_speed = 10  # 子弹速度
        self.bullet_width = 10
        self.bullet_height = 30
        self.bullet_color = (255, 48, 48)

        # 射击速度（每秒射击子弹数）
        self.fire_speed = 2  # 射击速度，单位：颗/秒

        # 外星人设置
        self.alien_speed = 2  # 外星人速度，单位：像素/秒
        self.alien_spawn_time_str = 2  # 生成外星人的速度

        # 计分设置
        self.alien_points = 1

        # 按钮设置
        self.button_color = 0, 255, 255

        self.initialize_dynamic_settings()

    def increase_difficulty(self, current_score):
        """根据当前得分更新难度等级"""
        if current_score in self.level_up_scores:
            self.level += 1
            # 更新与难度相关的设置
            self.ship_speed += 1
            self.bullet_speed += 1
            self.alien_speed += 0.5
            self.fire_speed += 1
            self.alien_spawn_time_str += 1  # 生成速度加快

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.level = 1
        self.ship_speed = 5
        self.bullet_speed = 10
        self.alien_speed = 2
        self.fire_speed = 2
        self.alien_spawn_time_str = 1
