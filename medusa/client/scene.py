# *_* coding=utf8 *_*
#!/usr/bin/env python



from cocos.scene import Scene

from medusa.client import view
from medusa.client import model
from medusa.client import control


class GameScene(Scene):

    def __init__(self):
        super(GameScene, self).__init__()
        self.model = model.GameModel()
        self.ctrl = control.GameCtrl(self.model)
        self.view = view.GameLayer(self.model)
        self.add(self.ctrl, z=1, name="controller")
        self.add(self.view, z=2, name="view")