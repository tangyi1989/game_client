#*_* coding=utf8 *_*
#!/usr/bin/env python

from PyQt4 import QtCore, QtGui
from medusa.map_editor.widget.tiled_map import TiledMapWidget

"""
地图编辑器主Widget

作者：唐万万
时间：2013-10-23
"""

class EditorWidget(QtGui.QWidget):

    """ 地图编辑器主Widget """

    def __init__(self, controller, parent=None):
        super(EditorWidget, self).__init__(parent)
        self.controller = controller
        self.tiled_map = None
        self.setup_layout()

    def setup_layout(self):
        """ 设置界面布局 """

        def set_layer_func(layer):
            """ 返回用于设置层的闭包函数 """
            def set_layer():
                self.tiled_map_widget.set_layer(layer)

            return set_layer

        # 主地图编辑器区域
        self.tiled_map_widget = TiledMapWidget()

        # 右边的各种按钮和Map属性
        map_name = QtGui.QLabel(u'地图名称')
        self.map_name_edit = QtGui.QLineEdit()
        map_picture = QtGui.QLabel(u'地图图片名称')
        self.map_picture_edit = QtGui.QLineEdit()

        tile_col = QtGui.QLabel(u'格子行数')
        self.tile_col_box = QtGui.QSpinBox()
        tile_row = QtGui.QLabel(u'格子列数')
        self.tile_row_box = QtGui.QSpinBox()
        self.resize_tiles_button = QtGui.QPushButton(u'重置Tiles大小')
        self.connect(self.resize_tiles_button,
                     QtCore.SIGNAL("clicked()"), self.on_resize_tiles_click)

        tile_width = QtGui.QLabel(u'格子长度')
        self.tile_width_box = QtGui.QSpinBox()
        self.tile_width_box.setValue(20)
        tile_height = QtGui.QLabel(u'格子宽度')
        self.tile_height_box = QtGui.QSpinBox()
        self.tile_height_box.setValue(20)
        self.tile_size_button = QtGui.QPushButton(u'重置Tiles尺寸')
        self.connect(self.tile_size_button,
                     QtCore.SIGNAL("clicked()"), self.on_tile_size_click)

        # 地图属性
        map_attr_layout = QtGui.QFormLayout()
        map_attr_layout.addRow(map_name, self.map_name_edit)
        map_attr_layout.addRow(map_picture, self.map_picture_edit)

        map_attr_layout.addRow(tile_col, self.tile_col_box)
        map_attr_layout.addRow(tile_row, self.tile_row_box)
        map_attr_layout.addWidget(self.resize_tiles_button)

        map_attr_layout.addRow(tile_width, self.tile_width_box)
        map_attr_layout.addRow(tile_height, self.tile_height_box)
        map_attr_layout.addWidget(self.tile_size_button)

        # 右边的布局
        right_layout = QtGui.QVBoxLayout()

        for layer in ('exist', 'alpha'):
            button = QtGui.QPushButton(u'%s层' % layer)
            self.connect(button,
                         QtCore.SIGNAL("clicked()"),
                         set_layer_func(layer))

            right_layout.addWidget(button)

        right_layout.addLayout(map_attr_layout)

        # 主布局
        main_layout = QtGui.QHBoxLayout()
        main_layout.setMargin(0)

        main_layout.addWidget(self.tiled_map_widget)
        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

    def on_resize_tiles_click(self):
        """ 重置tiles大小 """
        tile_col = self.tile_col_box.value()
        tile_row = self.tile_row_box.value()
        self.tiled_map_widget.resize_tiles(tile_col, tile_row)

    def on_tile_size_click(self):
        tile_width = self.tile_width_box.value()
        tile_height = self.tile_height_box.value()
        self.tiled_map_widget.set_tile_size(tile_width, tile_height)

    def on_changed_tiled_map(self, tiled_map):
        self.tiled_map = tiled_map
        self.tiled_map_widget.set_tiled_map(tiled_map)
        self.map_name_edit.setText(tiled_map.map_name)
        self.map_picture_edit.setText(tiled_map.map_picture)
        self.tile_col_box.setValue(tiled_map.tile_col)
        self.tile_row_box.setValue(tiled_map.tile_row)

    def on_changed_map_image(self, map_image):
        self.tiled_map_widget.set_map_image(map_image)
