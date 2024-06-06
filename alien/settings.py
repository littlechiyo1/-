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

        # 添加背景图像路径设置
        self.ready_background_image = 'images/back_1.jpg'
        self.game_background_image = 'images/back_2.jpg'
        self.button_background_image = 'images/button_1.png'

        # 颜色
        self.button_text_color = (0, 0, 0)  # 按钮颜色
        self.text_color = (0, 0, 0)         # 文本颜色

        # 飞船移动速度
        self.ship_speed = 10  # 飞船速度，单位：像素/秒
        # 飞船血量
        self.ship_limit = 1

        # 子弹设置
        self.bullet_speed = self.ship_speed + 1  # 子弹速度
        self.bullet_width = 10
        self.bullet_height = 30
        self.bullet_color = (255, 48, 48)

        # 射击速度（每秒射击子弹数）
        self.fire_speed = 5  # 射击速度，单位：颗/秒

        # 外星人设置
        self.alien_speed = 5  # 外星人速度，单位：像素/秒
        self.alien_spawn_time_str = 10  # 生成外星人的速度
        self.alien_spawn_time = 1 / self.alien_spawn_time_str * 1000  # 生成外星人的时间间隔（毫秒）

        # 计分设置
        self.alien_points = int(self.alien_speed * self.alien_spawn_time_str / 10)

        # 难度等级设置
        self.level = 1

        # 按钮设置
        self.button_color = 0, 255, 255
