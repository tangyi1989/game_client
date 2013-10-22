#*_* coding=utf8 *_*
#!/usr/bin/env python


import struct
from medusa import exception

class FieldsClass(object):

    """
    一个由描述字段组成的类
    类的成员变量使用 __fields__ 一个词典来描述，如此就能够在某些情况下
    像操作词典一样操作成员变量了。

    Example:

    class A(FieldsClass):

        __fields__ = {
            "propery_a": None,
            "propery_b": None,
        }

    a = A()
    print a.propery_a
    a.propery_a = 'something'
    """

    __fields__ = dict()

    def __init__(self, **kwargs):
        # 进行这个调用来避免调用被重写的__setattr__
        super(FieldsClass, self).__setattr__("__self_fields__",
                                        self.__fields__.copy())
        self.update_fields(**kwargs)

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

    def update_fields(self, **kwargs):
        self.__self_fields__.update(**kwargs)

    def get_fields(self):
        return self.__self_fields__

    @classmethod
    def fields(cls):
        return cls.__fields__.keys()

class FieldsSerializer(object):

    """
    对字段进行序列化和反序列化

    Example:
    
    a = {
            "a" : 1,
            "b" : "abc",
            "c" : 3
        }

    filelds_desc = [
        ("a", "!i", 4),
        ("b",  None, 32, "gb2312"),
        ("c", "!i", 4,)
    ]

    str_io = StringIO()
    FieldsSerializer().dumps_fields(str_io, a, filelds_desc)
    str_io.seek(0)
    fileds = FieldsSerializer().parse_fields(str_io, filelds_desc)
    """

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
                    value = field_data.decode('gb2312').rstrip()
                else:
                    raise exception.UnsupportConvertOption

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
                    raise exception.UnsupportConvertOption
            else:
                field_data = struct.pack(pack_type, value)

            if len(field_data) != field_length:
                raise exception.FieldPackError

            fields_stream.write(field_data)

        return fields_stream
