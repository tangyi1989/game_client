# *_* coding=utf8 *_*
#!/usr/bin/env python

from medusa.client import menu
from cocos.scene import Scene
from cocos.director import director

def start():
    director.init(width=800, height=600, caption="Medusa Client")
    scene = Scene()
    scene.add(menu.MainMenu(), z=1)
    director.run(scene)

if __name__ == '__main__':
    start()
