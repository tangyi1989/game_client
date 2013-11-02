# *_* coding=utf8 *_*
#!/usr/bin/env python

from resource import *
from cocos.layer import Layer, glPushMatrix, glPopMatrix

class BackgroundLayer(Layer):

    def __init__(self, model):
        super(BackgroundLayer, self).__init__()
        self.model = model
        self.img = pyglet.resource.image('background.jpg')

    def draw(self):
        glPushMatrix()
        self.transform()
        cameral = self.model.cameral

        orgin_position = cameral.get_origin_postion()
        self.img.blit(-orgin_position[0], -orgin_position[1])
        glPopMatrix()


class PlayerLayer(Layer):

    PLAYER_IAMGES = [
        ((0, 1), PlayerAction.images_up),
        ((0, -1), PlayerAction.images_down),
        ((-1, 0), PlayerAction.images_left),
        ((1, 0), PlayerAction.images_right),
    ]

    def __init__(self, model):
        super(PlayerLayer, self).__init__()
        self.model = model

    def get_player_iamge(self, player):
        player_image = None
        for (direct, image) in PlayerLayer.PLAYER_IAMGES:
            if direct[0] == player.direct[0] and \
                    direct[1] == player.direct[1]:
                player_image = image
                break

        return player_image

    def draw(self):

        glPushMatrix()
        self.transform()

        player = self.model.player
        cameral = self.model.cameral
        orgin_position = cameral.get_origin_postion()

        x = player.location[0] - orgin_position[0]
        y = player.location[1] - orgin_position[1]
        player_image = self.get_player_iamge(player)

        if player_image is not None:
            player_image[player.image_index].blit(x, y)

        glPopMatrix()


class GameLayer(Layer):

    def __init__(self, model):
        super(GameLayer, self).__init__()
        self.background_layer = BackgroundLayer(model)
        self.player_layer = PlayerLayer(model)

        self.add(self.background_layer)
        self.add(self.player_layer)


