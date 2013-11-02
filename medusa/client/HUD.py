# *_* coding=utf8 *_*
#!/usr/bin/env python

from cocos.layer import *
from cocos.director import director


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
