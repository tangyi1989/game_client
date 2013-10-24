#*_* coding=utf8 *_*
#!/usr/bin/env python

import zlib
import struct
try:
    from CStringIO import CStringIO as StringIO
except:
    from StringIO import StringIO

from medusa.utils.fields import FieldsSerializer
from medusa.map.map import TiledMap, MapTile, \
    MapElement, MapJumpPoint


class TiledMapSerializer(FieldsSerializer):

    """ Map文件序列化和反序列化 """

    header_fields_desc = [
        ("map_id", "!i", 4),
        ("map_type", "!i", 4),
        ("map_name", None, 32, 'gb2312'),
        ("map_picture", None, 32, 'gb2312'),
        ("tile_col", "!i", 4),
        ("tile_row", "!i", 4),
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
        tiled_map_stream = StringIO(raw_binary)

        tiled_map = TiledMap()

        # 读取Header部分
        header_stream = StringIO(tiled_map_stream.read(104))
        header_fields = self.parse_fields(
            header_stream, self.header_fields_desc)
        tiled_map.update_fields(**header_fields)

        # 读取tiles部分
        tiles = []
        tile_length = tiled_map.tile_row * tiled_map.tile_col
        tile_stream = StringIO(tiled_map_stream.read(tile_length))

        for i in xrange(0, tiled_map.tile_row * tiled_map.tile_col):
            tile_byte = struct.unpack('b', tile_stream.read(1))[0]
            tile = MapTile.from_byte(tile_byte)
            tiles.append(tile)

        tiled_map.tiles = tiles

        # 读取elements部分
        for i in xrange(0, tiled_map.element_num):
            element = MapElement()
            element_header_stream = StringIO(tiled_map_stream.read(20))
            element_fields = self.parse_fields(
                element_header_stream,
                self.element_header_fields_desc)

            element.update_fields(**element_fields)
            if element.data_length > 0:
                element.data = tiled_map_stream.read(element.data_length)
            else:
                element.data = ''

            tiled_map.elements.append(element)

        # 读取jump elements部分
        for i in xrange(0, tiled_map.jump_point_num):
            jump_point = MapJumpPoint()
            jump_point_header_stream = StringIO(tiled_map_stream.read(48))

            jump_point_fields = self.parse_fields(
                jump_point_header_stream,
                self.jump_point_header_fields_desc)

            jump_point.update_fields(**jump_point_fields)
            if jump_point.data_length > 0:
                jump_point.data = tiled_map_stream.read(jump_point.data_length)

            tiled_map.jump_points.append(jump_point)

        return tiled_map

    def dump_to_stream(self, tiled_map, tiled_map_stream):
        """ 将tiled_map保存在给定的流中 """

        # 写入Header部分
        tiled_map_fields = tiled_map.get_fields()
        self.dump_fields(
            tiled_map_stream, tiled_map_fields, self.header_fields_desc)

        # 写入Tiles部分
        tile_num = tiled_map.tile_row * tiled_map.tile_col
        assert len(tiled_map.tiles) == tile_num
        for tile in tiled_map.tiles:
            tile_byte = struct.pack('b', tile.to_byte())
            tiled_map_stream.write(tile_byte)

        # 写入Elements部分
        assert len(tiled_map.elements) == tiled_map.element_num
        for element in tiled_map.elements:
            element_fields = element.get_fields()
            self.dump_fields(
                tiled_map_stream, element_fields, self.element_header_fields_desc)

            assert len(element.data) == element.data_length
            tiled_map_stream.write(element.data)

        # 写入JumpPoint部分
        assert len(tiled_map.jump_points) == tiled_map.jump_point_num
        for jump_point in tiled_map.jump_points:
            jump_point_fields = jump_point.get_fields()
            self.dump_fields(
                tiled_map_stream, jump_point_fields, self.jump_point_header_fields_desc)

            assert len(jump_point.data) == jump_point.data_length
            tiled_map_stream.write(jump_point.data)

        return tiled_map_stream

    def dump_to_file(self, tiled_map, file_path):
        """ 将tiled_map保存在给定的文件中 """

        tiled_map_stream = StringIO()
        self.dump_to_stream(tiled_map, tiled_map_stream)

        tiled_map_stream.seek(0)
        compressed_bin = zlib.compress(tiled_map_stream.read())
        with open(file_path, 'wb') as f:
            f.write(compressed_bin)
