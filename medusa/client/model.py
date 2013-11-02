# *_* coding=utf8 *_*
#!/usr/bin/env python

#import weakref
import pyglet
from cocos.director import director


class Player(object):

    """ 代表玩家 """

    def __init__(self, current_map=None, name=u"不知火舞"):
        self.name = name
        self.speed = 15
        self.location = (30, 30)
        self.direct = (0, 1)
        self.current_map = current_map
        self.image_index = 0

    def access_new_map(self, new_map):
        """ 玩家进入新地图 """
        self.location = (30, 30)
        self.current_map = new_map

    def set_direct(self, x, y):
        """ 设置玩家的方向 """
        self.direct = [x, y]

    def move(self):
        """ 玩家移动 """
        if self.current_map is None:
            return

        next_x, next_y = (
            self.location[0] + self.speed * self.direct[0],
            self.location[1] + self.speed * self.direct[1]
        )
        if next_x >= 0 and next_y >= 0 and \
                next_x < self.current_map.map_size[0] and \
                next_y < self.current_map.map_size[1]:

            self.image_index += 1
            if self.image_index > 7:
                self.image_index = 0

            self.location = (next_x, next_y)

    def __repr__(self):
        return 'Location : %s, image_index : %s' % \
            (self.location, self.image_index)


class Map(object):

    """ 地图信息和地图状态 """

    def __init__(self):
        # 地图在左上角的其实坐标
        self.map_size = (2000, 2000)


class Cameral(object):

    """ 一架悬挂在空中的照相机 """

    def __init__(self, map_size, central_player=None):
        self.window_size = director.get_window_size()
        self.map_size = map_size
        self.central_player = central_player

    def get_origin_postion(self):
        """ 设置地图的中心位置，即玩家的位置，以此来得到渲染地图的起始点 """

        def get_cameral_origin_pos(central_pos, map_length, cameral_length):
            origin_loc = central_pos - (cameral_length / 2)

            if origin_loc < 0:
                origin_loc = 0
            elif origin_loc + cameral_length > map_length:
                origin_loc = map_length - cameral_length

            return origin_loc

        origin_position = (
            get_cameral_origin_pos(self.central_player.location[0],
                                   self.map_size[0], self.window_size[0]),
            get_cameral_origin_pos(self.central_player.location[1],
                                   self.map_size[1], self.window_size[1])
        )

        return origin_position


class GameModel(pyglet.event.EventDispatcher):

    def __init__(self):
        super(GameModel, self).__init__()
        self.map = Map()
        self.player = Player(self.map)
        self.cameral = Cameral(self.map.map_size, self.player)

GameModel.register_event_type('on_move')
