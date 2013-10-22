#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import constants
import pygame

pygame.init()

# 游戏的基本设置
GAME_TITLE = "Our Erlang game!"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30

# 文件路径
root_path = os.path.dirname(__file__)
data_path = os.path.join(root_path, '..', 'data')

# 游戏引擎，主循环
game_engine = None

# SDL
screen_surface = None
# 游戏的主要区域，显示游戏世界
game_surface = pygame.Surface((800, 450))
# 游戏交互界面，包括游戏的主显示区和其他的控件
gui_surface = pygame.Surface((800, 600))

# 游戏状态
game_state = constants.MENU_LOGIN