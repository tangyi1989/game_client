# *_* coding=utf8 *_*
#!/usr/bin/env python

from HUD import *
from gamectrl import *
from gamemodel import *
from action import *

from cocos.scene import Scene
from cocos.layer import *

class GameView(Layer):

    PLAYER_IAMGES = [
        ((0, 1), Action.images_up),
        ((0, -1), Action.images_down),
        ((-1, 0), Action.images_left),
        ((1, 0), Action.images_right),
    ]

    def __init__(self, model):
        super(GameView, self).__init__()

        self.model = model
        self.model.push_handlers(self.on_move)

    def on_move(self):
        pass

    def get_player_iamge(self, player):
        player_image = None
        for (direct, image) in GameView.PLAYER_IAMGES:
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


def get_newgame():
    '''returns the game main scene'''
    scene = Scene()

    model = GameModel()
    view = GameView(model)
    ctrl = GameCtrl(model)

    scene.add(ctrl, z=1, name="controller")
    scene.add(BackgroundLayer(model), z=0, name="background")
    scene.add(view, z=2, name="view")

    return scene
