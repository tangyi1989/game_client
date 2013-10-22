#*_* coding=utf8 *_*
#!/usr/bin/env python

class MedusaException(Exception):
    pass

class InternalException(MedusaException):
    """ 写程序时出现的非外界异常 """
    pass

# fileds
class FieldPackError(InternalException):
    """ 在对某个字段进行序列化的时候出错。 """
    pass

class UnsupportConvertOption(InternalException):
    """ 进行序列化(反序列化)时遇到不支持的转换格式 """
    pass

# map editor
class TiledMapIsNone(InternalException):
    """ TiledMapWidget控件未设置tiled_map属性 """
    pass