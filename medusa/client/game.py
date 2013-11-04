# *_* coding=utf8 *_*
#!/usr/bin/env python

from medusa.client import config
from medusa.client.menu import MainMenu
from cocos.scene import Scene
from cocos.director import director

CONF = config.CONF

def start():
    director.init(width=CONF.window_width,
                  height=CONF.window_height,
                  caption=CONF.caption)
    scene = Scene()
    scene.add(MainMenu(), z=1)
    director.run(scene)

if __name__ == '__main__':
    start()
