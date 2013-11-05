# *_* coding=utf8 *_*
#!/usr/bin/env python

import pyglet
from cocos import menu 

from cocos.scenes.transitions import FlipAngular3DTransition
from cocos.director import director

from medusa.client.main import scene

class MainMenu(menu.Menu):

    def __init__(self):
        super(MainMenu, self).__init__("MEDUSA GAME")

        self.font_title['font_name'] = 'Edit Undo Line BRK'
        self.font_title['font_size'] = 60
        self.font_title['color'] = (204, 164, 164, 255)

        self.font_item['font_name'] = 'Edit Undo Line BRK'
        self.font_item['font_size'] = 32
        self.font_item['color'] = (32, 16, 32, 255)

        self.font_item_selected['font_name'] = 'Edit Undo Line BRK'
        self.font_item_selected['font_size'] = 46
        self.font_item_selected['color'] = (32, 16, 32, 255)

        items = []

        items.append(menu.MenuItem('Login', self.login_game))
        items.append(menu.MenuItem('Register', self.register_game))
        items.append(menu.MenuItem('More Game', self.more_game))
        items.append(menu.MenuItem('Quit', self.on_quit))

        self.create_menu(items, menu.shake(), menu.shake_back())

    def login_game(self):
        game_scene = scene.GameScene()
        director.push(FlipAngular3DTransition(game_scene, 1.5))

    def register_game(self):
        pass

    def more_game(self):
        pass

    def on_quit(self):
        pyglet.app.exit()
