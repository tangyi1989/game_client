#*_* coding=utf8 *_*
#!/usr/bin/env python

import zlib
import struct   
try:
    from CStringIO import CStringIO as StringIO
except:
    from StringIO import StringIO

"""
读取和保存地图文件，此文件格式和数据结构和《斗破苍穹》的游戏地图一样的，
请参照具体格式请参照服务端中的地图设计，对map文件格式的分析。

作者：唐万万
日期：2013-10-18
"""

class FieldPackError(Exception):
    """ 在对某个字段进行序列化的时候出错。 """
    pass

class UnsupportConvertOption(Exception):
    """ 不支持的转换格式 """
    pass

class FieldsClass(object):

    """
    一个由描述字段组成的类
    类的成员变量使用 __fields__ 一个词典来描述，如此就能够在某些情况下
    像操作词典一样操作成员变量了。
    """

    __fields__ = dict()

    def __init__(self, **fields):
        # 进行这个调用来避免调用被重写的__setattr__
        super(FieldsClass, self).__setattr__("__self_fields__",
                                        self.__fields__.copy())
        self.update_fields(**fields)

    def __repr__(self):
        return str(self.__self_fields__)

    def __setattr__(self, key, value):
        if not self.__self_fields__.has_key(key):
            raise AttributeError

        self.__self_fields__[key] = value

    def __getattr__(self, key):
        if not self.__self_fields__.has_key(key):
            raise AttributeError

        return self.__self_fields__[key]

    def update_fields(self, **fields):
        self.__self_fields__.update(**fields)

    def get_fields(self):
        return self.__self_fields__

class FieldsSerializer(object):

    """ 对字段进行序列化和反序列化 """

    def parse_fields(self, fields_stream, fields_desc):
        """
        根据字段描述，将流中的字段转化为一个词典
        PARAMTERS:
            fields_stream : 要转换的数据流
            fields_desc : 字段描述，对流中数据的描述，用于转换，如下结构
                [
                    (fileld_name, pack_type, field_length, convert_option(可选)),
                    ...
                ]
        RETURNS:
            filelds dict() 转化后的字段
        """

        fields = {}

        for field_desc in fields_desc:
            field_name, pack_type, field_length = field_desc[:3]
            field_data = fields_stream.read(field_length)

            if len(field_desc) > 3:
                convert_option = field_desc[3]
                if convert_option == "raw":
                    value = field_data
                elif convert_option == "gb2312":
                    value = field_data.decode('gb2312')
                else:
                    raise UnsupportConvertOption

            elif len(field_desc) == 3:
                unpacked = struct.unpack(pack_type, field_data)
                value = unpacked[0] if len(unpacked) == 1 else unpacked

            fields.setdefault(field_name, value)

        return fields

    def dump_fields(self, fields_stream, fields, fields_desc):
        """
        将字段按照字段描述写入流中
        PARAMTERS:
            fields_stream : 要写入的流
            filelds : dict() 要写入的字段
            fields_desc : 字段描述，对流中数据的描述，用于转换，如下结构
                [
                    (fileld_name, pack_type, field_length, convert_option(可选)),
                    ...
                ]
        RETURNS:
            fields_stream 传入的那个流
        """

        for field_desc in fields_desc:
            field_name, pack_type, field_length = field_desc[:3]

            if not fields.has_key(field_name):
                raise AttributeError

            value = fields.get(field_name, '')
            if len(field_desc) > 3:
                convert_option = field_desc[3]
                if convert_option == "gb2312":
                    field_data = value.encode("gb2312")
                    field_data = struct.pack('%ss' % field_length, field_data)
                else:
                    raise UnsupportConvertOption
            else:
                field_data = struct.pack(pack_type, value)

            if len(field_data) != field_length:
                raise FieldPackError

            fields_stream.write(field_data)

        return fields_stream

class Map(FieldsClass):

    """ 地图 """

    __fields__ = {
        "map_id": None,
        "map_name": None,
        "map_type": None,
        "map_picture": None,
        "tile_row": None,
        "tile_col": None,
        "element_num": None,
        "jump_point_num": None,
        "offset_x": None,
        "offset_y": None,
        "tw": None,
        "th": None,

        "tiles": [],
        "elements": [],
        "jump_points": []
    }


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

class MCMSerializer(FieldsSerializer):

    """ Map文件序列化和反序列化 """

    header_fields_desc = [
        ("map_id", "!i", 4),
        ("map_type", "!i", 4),
        ("map_name", None, 32, 'gb2312'),
        ("map_picture", None, 32, 'gb2312'),
        ("tile_row", "!i", 4),
        ("tile_col", "!i", 4),
        ("element_num", "!i", 4),
        ("jump_point_num", "!i", 4),
        ("offset_x", "!i", 4),
        ("offset_y", "!i", 4),
        ("tw", "!i", 4),
        ("th", "!i", 4),
    ]

    element_header_fields_desc = [
        ("id", "!i", 4),
        ("index_tx", "!i", 4),
        ("index_ty", "!i", 4),
        ("type", "!i", 4),
        ("data_length", "!i", 4),
    ]

    jump_point_header_fields_desc = [
        ("id", "!i", 4),
        ("index_tx", "!i", 4),
        ("index_ty", "!i", 4),
        ("target_map_id", "!i", 4),
        ("target_index_tx", "!i", 4),
        ("target_index_ty", "!i", 4),
        ("hw", "!i", 4),
        ("yl", "!i", 4),
        ("wl", "!i", 4),
        ("min_level", "!i", 4),
        ("max_level", "!i", 4),
        ("data_length", "!i", 4),
    ]

    def read_from_file(self, file_path):
        """ 读取并解析map文件 """

        with open(file_path, 'rb') as f:
            compressed_bin = f.read()

        raw_binary = zlib.decompress(compressed_bin)
        map_stream = StringIO(raw_binary)

        map = Map()

        # 读取Header部分
        header_stream = StringIO(map_stream.read(104))
        header_fields = self.parse_fields(
            header_stream, self.header_fields_desc)
        map.update_fields(**header_fields)

        # 读取tiles部分
        tiles = []
        tile_length = map.tile_row * map.tile_col
        tile_stream = StringIO(map_stream.read(tile_length))
        for y in xrange(0, map.tile_row):
            tile_row = []
            for x in xrange(0, map.tile_col):
                tile_byte = struct.unpack('b', tile_stream.read(1))[0]
                tile = MapTile.from_byte(tile_byte)
                tile_row.append(tile)

            tiles.append(tile_row)

        map.tiles = tiles

        # 读取elements部分
        for i in xrange(0, map.element_num):
            element = MapElement()
            element_header_stream = StringIO(map_stream.read(20))
            element_fields = self.parse_fields(
                element_header_stream,
                self.element_header_fields_desc)

            element.update_fields(**element_fields)
            if element.data_length > 0:
                element.data = map_stream.read(element.data_length)
            else:
                element.data = ''

            map.elements.append(element)

        # 读取jump elements部分
        for i in xrange(0, map.jump_point_num):
            jump_point = MapJumpPoint()
            jump_point_header_stream = StringIO(map_stream.read(48))

            jump_point_fields = self.parse_fields(
                jump_point_header_stream,
                self.jump_point_header_fields_desc)

            jump_point.update_fields(**jump_point_fields)
            if jump_point.data_length > 0:
                jump_point.data = map_stream.read(jump_point.data_length)

            map.jump_points.append(jump_point)

        return map

    def dump_to_stream(self, map, map_stream):
        """ 将map文件保存在给定的流中 """

        # 写入map文件Header部分
        map_fields = map.get_fields()
        self.dump_fields(map_stream, map_fields, self.header_fields_desc)

        # 写入map文件Tiles部分
        assert len(map.tiles) == map.tile_row
        for tile_row in map.tiles:
            assert len(tile_row) == map.tile_col

            for tile in tile_row:
                tile_byte = struct.pack('b', tile.to_byte())
                map_stream.write(tile_byte)

        # 写入map文件Elements部分
        assert len(map.elements) == map.element_num
        for element in map.elements:
            element_fields = element.get_fields()
            self.dump_fields(
                map_stream, element_fields, self.element_header_fields_desc)

            assert len(element.data) == element.data_length
            map_stream.write(element.data)

        # 写入map文件的JumpPoint部分
        assert len(map.jump_points) == map.jump_point_num
        for jump_point in map.jump_points:
            jump_point_fields = jump_point.get_fields()
            self.dump_fields(
                map_stream, jump_point_fields, self.jump_point_header_fields_desc)

            assert len(jump_point.data) == jump_point.data_length
            map_stream.write(jump_point.data)

        return map_stream

    def dump_to_file(self, map, file_path):
        """ 将map文件保存在给定的文件中 """

        map_stream = StringIO()
        self.dump_to_stream(map, map_stream)

        map_stream.seek(0)
        compressed_bin = zlib.compress(map_stream.read())
        with open(file_path, 'wb') as f:
            f.write(compressed_bin)

if __name__ == "__main__":
    file_path = "/home/tang/code/erlang/tang/erl_game_server/resource/map/mcm/105001.mcm"
    map = MCMSerializer().read_from_file(file_path)
    MCMSerializer().dump_to_file(map, '/tmp/105001.mcm')
    map = MCMSerializer().read_from_file('/tmp/105001.mcm')
    print map
