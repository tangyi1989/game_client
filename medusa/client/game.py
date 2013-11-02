# *_* coding=utf8 *_*
#!/usr/bin/env python

import os
from pyglet import font

from cocos.director import director
from cocos.scene import Scene
from cocos.scenes.transitions import *
from cocos.menu import *

from HUD import *
from twisted.internet import protocol, reactor
from threading import Thread

class MainMenu(Menu):

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

        items.append(MenuItem('Login', self.login_game))
        items.append(MenuItem('Register', self.register_game))
        items.append(MenuItem('More Game', self.more_game))
        items.append(MenuItem('Quit', self.on_quit))

        self.create_menu(items, shake(), shake_back())

    def login_game(self):
        import gameview
        director.push(
            FlipAngular3DTransition(gameview.get_newgame(), 1.5))

    def register_game(self):
        pass

    def more_game(self):
        pass

    def on_quit(self):
        reactor.stop()
        pyglet.app.exit()


def start():
    data_path = os.path.join(os.path.dirname(__file__), "data")
    pyglet.resource.path.append(data_path)
    pyglet.resource.reindex()
    font.add_directory(data_path)

    director.init(width=800, height=600, caption="Medusa Client")
    scene = Scene()
    scene.add(MainMenu(), z=1)
    director.run(scene)

if __name__ == '__main__':
    start()
