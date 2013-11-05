# *_* coding=utf8 *_*
#!/usr/bin/env python

from medusa.client.resource import *
from cocos.layer import Layer, glPushMatrix, glPopMatrix

class BackgroundLayer(Layer):
    """ 背景层：绘制地图背景 """

    def __init__(self, model):
        super(BackgroundLayer, self).__init__()
        self.model = model
        self.img = pyglet.resource.image('background.jpg')

    def draw(self):
        if not self.model.loaded:
            return

        glPushMatrix()
        self.transform()
        cameral = self.model.cameral

        orgin_position = cameral.get_origin_postion()
        self.img.blit(-orgin_position[0], -orgin_position[1])
        glPopMatrix()


class PlayerLayer(Layer):
    """ 玩家层：绘制地图上的玩家 """

    PLAYER_IAMGES = [
        ((0, 1), PlayerAction.images_up),
        ((0, -1), PlayerAction.images_down),
        ((-1, 0), PlayerAction.images_left),
        ((1, 0), PlayerAction.images_right),
    ]

    def __init__(self, model):
        super(PlayerLayer, self).__init__()
        self.model = model

    def get_player_image(self, player):
        player_image = None
        for (direct, image) in PlayerLayer.PLAYER_IAMGES:
            if direct[0] == player.direct[0] and \
                    direct[1] == player.direct[1]:
                player_image = image
                break

        return player_image

    def draw(self):

        if not self.model.loaded:
            return

        glPushMatrix()
        self.transform()

        player = self.model.player
        cameral = self.model.cameral
        orgin_position = cameral.get_origin_postion()

        x = player.location[0] - orgin_position[0]
        y = player.location[1] - orgin_position[1]
        player_image = self.get_player_image(player)

        if player_image is not None:
            player_image[player.image_index].blit(x, y)

        glPopMatrix()


class AssistLayer(Layer):
    """ 辅助层:画出地图方格，坐标等信息，用于帮助调试程序 """
    def __init__(self, model):
        self.model = model

    def draw(self):

        if not self.model.loaded:
            return

        glPushMatrix()
        self.transform()

        glPopMatrix()


class GameLayer(Layer):

    def __init__(self, model):
        super(GameLayer, self).__init__()
        self.background_layer = BackgroundLayer(model)
        self.player_layer = PlayerLayer(model)

        self.add(self.background_layer)
        self.add(self.player_layer)