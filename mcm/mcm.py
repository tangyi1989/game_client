#*_* coding=utf8 *_*
#!/usr/bin/env python

import zlib
import struct   
try:
    from CStringIO import CStringIO as StringIO
except:
    from StringIO import StringIO


class Fields(object):

    __fields__ = dict()

    def __init__(self, **fields):
        # 进行这个调用来避免调用被重写的__setattr__
        super(Fields, self).__setattr__("__self_fields__",
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


class MCM(Fields):

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

        "tiles": [[]],
        "elements": [],
        "jump_points": []
    }


class Tile(Fields):

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


class Element(Fields):
    __fields__ = {
        "id": None,
        "index_tx": None,
        "index_ty": None,
        "type": None,
        "data_length": None,
        "data": ''
    }


class JumpPoint(Fields):
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


class FieldPackError(Exception):
    pass


class MCMSerialize(object):

    """ MCM文件读取器 """

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

    def parse_fields(self, fields_stream, fields_desc):
        """ 转换流中的字段 """

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
            elif len(field_desc) == 3:
                unpacked = struct.unpack(pack_type, field_data)
                value = unpacked[0] if len(unpacked) == 1 else unpacked

            fields.setdefault(field_name, value)

        return fields

    def dump_fields(self, fields_stream, fields, fields_desc):
        """ 将字段按照字段描述写入流中 """

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
                field_data = struct.pack(pack_type, value)

            if len(field_data) != field_length:
                raise FieldPackError

            fields_stream.write(field_data)

        return fields_stream

    def read_from_file(self, file_path):
        """ 读取并解析mcm文件 """

        with open(file_path, 'rb') as f:
            compressed_bin = f.read()

        raw_binary = zlib.decompress(compressed_bin)
        mcm_stream = StringIO(raw_binary)

        mcm = MCM()

        # 读取Header部分
        header_stream = StringIO(mcm_stream.read(104))
        header_fields = self.parse_fields(
            header_stream, self.header_fields_desc)
        mcm.update_fields(**header_fields)

        # 读取tiles部分
        tiles = []
        tile_length = mcm.tile_row * mcm.tile_col
        tile_stream = StringIO(mcm_stream.read(tile_length))
        for y in xrange(0, mcm.tile_row):
            tile_row = []
            for x in xrange(0, mcm.tile_col):
                tile_byte = struct.unpack('b', tile_stream.read(1))[0]
                tile = Tile.from_byte(tile_byte)
                tile_row.append(tile)

            tiles.append(tile_row)

        mcm.tiles = tiles

        # 读取elements部分
        for i in xrange(0, mcm.element_num):
            element = Element()
            element_header_stream = StringIO(mcm_stream.read(20))
            element_fields = self.parse_fields(
                element_header_stream,
                self.element_header_fields_desc)

            element.update_fields(**element_fields)
            if element.data_length > 0:
                element.data = mcm_stream.read(element.data_length)
            else:
                element.data = ''

            mcm.elements.append(element)

        # 读取jump elements部分
        for i in xrange(0, mcm.jump_point_num):
            jump_point = JumpPoint()
            jump_point_header_stream = StringIO(mcm_stream.read(48))

            jump_point_fields = self.parse_fields(
                jump_point_header_stream,
                self.jump_point_header_fields_desc)

            jump_point.update_fields(**jump_point_fields)
            if jump_point.data_length > 0:
                jump_point.data = mcm_stream.read(jump_point.data_length)

            mcm.jump_points.append(jump_point)

        return mcm

    def dump_to_stream(self, mcm, mcm_stream):
        """ 将mcm文件保存在给定的流中 """

        # 写入mcm文件Header部分
        mcm_fields = mcm.get_fields()
        self.dump_fields(mcm_stream, mcm_fields, self.header_fields_desc)

        # 写入mcm文件Tiles部分
        assert len(mcm.tiles) == mcm.tile_row
        for tile_row in mcm.tiles:
            assert len(tile_row) == mcm.tile_col

            for tile in tile_row:
                tile_byte = struct.pack('b', tile.to_byte())
                mcm_stream.write(tile_byte)

        # 写入mcm文件Elements部分
        assert len(mcm.elements) == mcm.element_num
        for element in mcm.elements:
            element_fields = element.get_fields()
            self.dump_fields(
                mcm_stream, element_fields, self.element_header_fields_desc)

            assert len(element.data) == element.data_length
            mcm_stream.write(element.data)

        # 写入mcm文件的JumpPoint部分
        assert len(mcm.jump_points) == mcm.jump_point_num
        for jump_point in mcm.jump_points:
            jump_point_fields = jump_point.get_fields()
            self.dump_fields(
                mcm_stream, jump_point_fields, self.jump_point_header_fields_desc)

            assert len(jump_point.data) == jump_point.data_length
            mcm_stream.write(jump_point.data)

        return mcm_stream

    def dump_to_file(self, mcm, file_path):
        """ 将mcm文件保存在给定的文件中 """

        mcm_stream = StringIO()
        self.dump_to_stream(mcm, mcm_stream)

        mcm_stream.seek(0)
        compressed_bin = zlib.compress(mcm_stream.read())
        with open(file_path, 'wb') as f:
            f.write(compressed_bin)

if __name__ == "__main__":
    file_path = "/home/tang/code/erlang/tang/erl_game_server/resource/map/mcm/105001.mcm"
    mcm = MCMSerialize().read_from_file(file_path)
    MCMSerialize().dump_to_file(mcm, '/tmp/105001.mcm')
    mcm = MCMSerialize().read_from_file('/tmp/105001.mcm')
