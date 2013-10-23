#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from pgu import gui
from medusa.client import global_vars as g

class MenuContainer(gui.Container):
    def __init__(self, **params):
        super(MenuContainer, self).__init__(**params)
        btn = gui.Button(u"退出游戏")
        btn.connect(gui.CLICK, self.quit_game, None)
        self.add(btn, 0, 0)

    def quit_game(self, btn):
        pass

class GameGUI(object):
    def __init__(self):
        self.container = gui.Container(align=0, valign=0)
        self.container.add(MenuContainer(), 0, 450)
        self.app = gui.App()
        self.app.init(self.container)

    def draw(self, surface, surface_rect):
        g.screen_surface.fill((255, 255, 255))
        g.screen_surface.blit(surface, surface_rect)
        self.app.paint()

    def _handle_event(self, event):
        self.app.event(event)