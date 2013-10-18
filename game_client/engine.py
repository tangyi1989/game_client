#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pygame
import constants as const
from render import RenderEngine
from menu import login
from twisted.internet import reactor
import global_vars as g

class Engine:

    def __init__(self):
        self.login_menu = login.MenuLogin(g.screen_surface)
        self.render_engine = RenderEngine()

    def set_state(self, state):
        g.game_state = state

    def start(self):
        self.set_state(const.MENU_LOGIN)
        self.game_loop()
        reactor.run()

    def game_loop(self):
        if g.game_state == const.MENU_LOGIN:
            self.login_menu.draw()
        elif g.game_state == const.INGAME:
            self.render_engine.render()

        for event in pygame.event.get():
            if g.game_state == const.MENU_LOGIN:
                self.login_menu._handle_event(event)
            elif g.game_state == const.INGAME:
                self.render_engine._handle_event(event)

            if event.type == pygame.QUIT:
                self.quit_game()
                break

        reactor.callLater(1./g.FPS, self.game_loop)

    def quit_game(self):
        reactor.stop()
        pygame.quit()
