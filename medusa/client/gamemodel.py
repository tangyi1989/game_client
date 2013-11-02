# *_* coding=utf8 *_*
#!/usr/bin/env python

#import weakref
import pyglet
from cocos.director import director


class Player(object):

    """ 代表玩家 """

    def __init__(self, name=u"不知火舞"):
        self.name = name
        self.speed = 15
        self.location = (30, 30)
        self.direct = (0, 1)

        self.image_index = 0

    def set_direct(self, x, y):
        """ 设置玩家的方向 """
        self.direct = [x, y]

    def move_to(self, x, y):
        """ 玩家移动 """
        if self.location == (x, y):
            return

        self.image_index += 1
        if self.image_index > 7:
            self.image_index = 0

        self.location = (x, y)

    def stop(self):
        """ 玩家停止移动 """
        pass

    def __repr__(self):
        return 'Location : %s, image_index : %s' % (self.location, self.image_index)

    def get_next_location(self):
        """ 获取下一个时刻玩家的位置 """
        return (
            self.location[0] + self.speed * self.direct[0],
            self.location[1] + self.speed * self.direct[1]
        )


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
        self.player = Player()
        self.map = Map()
        self.cameral = Cameral(self.map.map_size, self.player)

    def player_move(self):
        """ 玩家开始移动 """
        player_x, player_y = self.player.get_next_location()
        if player_x >= 0 and player_y >= 0 and \
                player_x < self.map.map_size[0] and \
                player_y < self.map.map_size[1]:
            self.player.move_to(player_x, player_y)
        else:
            self.player.stop()

    def stop_player_move(self):
        """ 玩家停止移动 """
        self.player.stop()

GameModel.register_event_type('on_move')
