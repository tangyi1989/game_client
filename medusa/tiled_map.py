#*_* coding=utf8 *_*
#!/usr/bin/env python

"""
读取和保存地图文件，
请参照具体格式请参照服务端中的地图设计，对map文件格式的分析。

作者：唐万万
日期：2013-10-18
"""

from medusa.utils.fileds import FieldsClass

class TiledMap(FieldsClass):

    """ 地图 """

    __fields__ = {
        "map_id": 0,
        "map_type": 1,
        "map_name": 'untitled',
        "map_picture": '',
        "tile_row": 0,
        "tile_col": 0,
        "element_num": 0,
        "jump_point_num": 0,
        "offset_x": 0,
        "offset_y": 0,
        "tw": 20,
        "th": 20,

        "tiles": [],
        "elements": [],
        "jump_points": []
    }

    def resize_tiles(self, tile_col, tile_row):
        """ 重置tiles的大小 """

        if tile_col < 0 or tile_row < 0:
            return

        new_tiles = []
        for x in xrange(0, tile_col):
            for y in xrange(0, tile_row):
                if x < self.tile_col and y < self.tile_row:
                    tile = self.get_tile(x, y)
                else:
                    tile = MapTile()
                
                new_tiles.append(tile)

        self.tile_col = tile_col
        self.tile_row = tile_row
        self.tiles = new_tiles

    def get_tile(self, x, y):
        """ 获取指定位置的tile """
        return self.tiles[self.tile_row * x + y]


class MapTile(FieldsClass):

    """ 地图坐标格子 """

    __fields__ = {
        "reversed": False,
        "arena": False,
        "sell": False,
        "all_safe": False,
        "safe": False,
        "run": False,
        "alpha": False,
        "exist": False,
    }

    @classmethod
    def from_byte(cls, byteval):
        def get_bit(byteval, idx):
            return ((byteval & (1 << idx)) != 0)

        tile = cls()
        tile.update_fields(
            exist=get_bit(byteval, 0),
            alpha=get_bit(byteval, 1),
            run=get_bit(byteval, 2),
            safe=get_bit(byteval, 3),
            all_safe=get_bit(byteval, 4),
            sell=get_bit(byteval, 5),
            arena=get_bit(byteval, 6),
            reversed=get_bit(byteval, 7)
        )

        return tile

    def to_byte(self):
        bits = (self.exist,
                self.alpha,
                self.run,
                self.safe,
                self.all_safe,
                self.sell,
                self.arena,
                self.reversed)

        byteval, pos = 0, 0
        for bit in bits:
            bitval = 1 if bit else 0
            byteval += bitval << pos
            pos += 1

        return byteval

    def __repr__(self):
        return str(self.to_byte())


class MapElement(FieldsClass):

    """ 地图元素(怪物,NPC等) """

    __fields__ = {
        "id": None,
        "index_tx": None,
        "index_ty": None,
        "type": None,
        "data_length": None,
        "data": ''
    }


class MapJumpPoint(FieldsClass):

    """ 地图跳转点 """

    __fields__ = {
        "id": None,
        "index_tx": None,
        "index_ty": None,
        "target_map_id": None,
        "target_index_tx": None,
        "target_index_ty": None,
        "hw": None,
        "yl": None,
        "wl": None,
        "min_level": None,
        "max_level": None,
        "data_length": None,
        "data": ''
    }

