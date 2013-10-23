# *_* coding=utf8 *_*
#!/usr/bin/env python

import sys
import engine
import pygame
import global_vars as g

reload(sys)
sys.setdefaultencoding('utf-8')
pygame.display.set_caption(g.GAME_TITLE)
g.screen_surface = pygame.display.set_mode((g.SCREEN_WIDTH, g.SCREEN_HEIGHT))

def start():
    g.game_engine = engine.Engine()
    g.game_engine.start()

if __name__ == '__main__':
    start()