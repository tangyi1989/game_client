#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import pygame

pygame.init()

GAME_TITLE = "Our Erlang game!"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# 文件路径
root_path = os.path.dirname(__file__)
data_path = os.path.join(root_path, '..', 'data')

# 游戏引擎，主循环
game_engine = None

# SDL
game_surface = pygame.Surface((480, 352))
gui_surface = pygame.Surface((800, 600))

