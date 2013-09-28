#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pygame
from menu import login
import global_vars as g

class Engine:

    def __init__(self):
        self.login_menu = login.MenuLogin(g.screen_surface)

    def start(self):
        self.game_loop()

    def game_loop(self):
        while True:
            self.login_menu.draw()

            for event in pygame.event.get():
                self.login_menu._handle_event(event)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    break