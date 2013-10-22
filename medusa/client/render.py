#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pygame
from gui.gui import GameGUI
import global_vars as g

class RenderEngine():
    def __init__(self):
        self.surface = g.game_surface
        self.game_GUI = GameGUI()
        self.surface_rect = g.game_surface.get_rect()

    def render(self):
        self.game_GUI.draw(self.surface, self.surface_rect)
        pygame.display.update()

    def _handle_event(self, event):
        self.game_GUI._handle_event(event)
