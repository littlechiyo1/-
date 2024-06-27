# Alien Invasion

Alien Invasion 是一个使用 Pygame 制作的2D射击游戏。玩家控制飞船消灭不断出现的外星人，通过得分提高游戏难度。

## 目录

- [游戏玩法](#游戏玩法)
- [文件结构](#文件结构)
- [设置和自定义](#设置和自定义)
- [致谢](#致谢)
- [许可证](#许可证)

## 安装

克隆仓库：

   ```sh
   git clone https://github.com/littlechiyo1/Alien.git
   ```

## 游戏玩法
使用AD 键控制飞船移动。

按空格键射击子弹。

消灭外星人以获得分数。

游戏难度会在得分达到10、20、30等时自动提高。

游戏结束时显示最终得分和最高得分。


## 文件结构
alien_invasion/
├── alien_invasion.py        主游戏文件，包含游戏的主要逻辑。
├── settings.py              包含所有游戏设置。
├── game_stats.py            跟踪游戏的统计信息。
├── scoreboard.py            显示得分、最高分和等级信息。
├── button.py                定义按钮类。
├── ship.py                  定义飞船类。
├── bullet.py                定义子弹类。
├── alien.py                 定义外星人类。
├── images/                  包含游戏使用的图像资源。
│   ├── back_1.jpg
│   ├── back_2.jpg
│   ├── back_3.jpg
│   ├── alien_2.png
│   ├── alien_3.png
│   ├── button_1.png
│   ├── ship.bmp
│   └── ship_2.png
└── music/                  包含游戏使用的音乐和音效资源。
    ├── 背景-1999.flac
    ├── 背景-欢乐节拍.mp3
    ├── 子弹-1.mp3
    └── 游戏失败-1.mp3
    

## 设置和自定义
你可以通过编辑 settings.py 文件来自定义游戏设置。例如，可以更改屏幕大小、飞船速度、子弹速度等。

## 致谢
感谢 Pygame 社区提供的优秀游戏开发库。

## 许可证
该项目使用 MIT 许可证。请参见 LICENSE 文件以获取更多信息。
