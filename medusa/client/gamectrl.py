# *_* coding=utf8 *_*
#!/usr/bin/env python

from cocos.layer import Layer
from pyglet.window import key
from medusa.network.client import Client
from threading import Timer, Thread
from twisted.internet import reactor

class GameCtrl(Layer):
    is_event_handler = True

    MOVE_KEY = {
        key.LEFT: (-1, 0),
        key.RIGHT: (1, 0),
        key.UP: (0, 1),
        key.DOWN: (0, -1)
    }

    def __init__(self, model):
        super(GameCtrl, self).__init__()
        self.model = model
        self.player_moving = False
        self.schedule(self.step)

        # network connection 
        self.client = Client(self.msg_handler)
        self.client.start(ip='127.0.0.1', port=80)
        Thread(target=reactor.run, kwargs={'installSignalHandlers': 0}).start()

    def msg_handler(self, message):
        print message

    def on_key_press(self, k, m):
        # 开始进行玩家移动
        direct = GameCtrl.MOVE_KEY.get(k)
        if direct is not None:
            self.model.player.set_direct(*direct)
            self.player_moving = True

    def on_key_release(self, k, m):
        # 停止玩家移动
        if GameCtrl.MOVE_KEY.has_key(k):
            self.player_moving = False

    def step(self, dt):
        if self.player_moving:
            self.model.player.move()
