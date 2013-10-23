#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pygame
from pgu import gui
from medusa.client import constants as const
from medusa.client import global_vars as g
from medusa.proto import game_pb2

class LoginControl(gui.Table):
    def __init__(self, **params):
        gui.Table.__init__(self, **params)
        self.value = gui.Form()
        self.engine = None

        self.tr()
        self.td(gui.Label(u"江湖夜雨十年灯,一场游戏一场梦。"))

        self.tr()
        self.td(gui.Spacer(0, 30))

        self.tr()
        btn = gui.Button(u"进入游戏", width=120, height=30)
        btn.connect(gui.CLICK, self.access_game, None)
        self.td(btn)

    def access_game(self, btn):
	login_packet = game_pb2.Login()
	login_packet.name = 'tang'
	login_packet.password = 'tangwanwan'
	self.sendLine(encode(101, login_packet))
        g.game_engine.set_state(const.INGAME)


class MenuLogin(object):

    def __init__(self, surface):
        self.surface = surface
        #self.background_image = pygame.image.load(g.data_path + '/gui/background.jpg')

        # GUI
        self.app = gui.App()
        self.login_ctrl = LoginControl()
        self.login_ctrl.engine = self

        self.c = gui.Container(align=0, valign=0)
        self.c.add(self.login_ctrl, 0, 0)

        self.app.init(self.c)

        self.surface = surface

    def draw(self):
        #self.surface.blit(self.background_image, (0, 0))
        self.surface.fill((255, 255, 255))
        self.app.paint()

        pygame.display.update()

    def _handle_event(self, event):
        self.app.event(event)
