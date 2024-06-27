

class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, ai_game):
        """初始化统计信息"""
        self.settings = ai_game.settings
        self.reset_stats()

        # 最高分(不重置)
        self.high_score = 0

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.settings.initialize_dynamic_settings()  # 重置难度设置

    def update_difficulty(self):
        """检查并更新难度等级"""
        self.settings.increase_difficulty(self.score)
