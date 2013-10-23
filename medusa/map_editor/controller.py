#*_* coding=utf8 *_*
#!/usr/bin/env python

from PyQt4 import QtGui
from medusa.map import map as tiled_map
from medusa.map_editor.widget.editor import EditorWidget
from medusa.map_editor.window import MainWindow

"""
地图控制器

作者：唐万万
时间：2013-10-23
"""

class MapController(object):

    """ 地图控制器 """

    def __init__(self):
        self.tiled_map = None

    def create_new_map(self):
        self.tiled_map = tiled_map.TiledMap()
        self.view.on_changed_tiled_map(self.tiled_map)

    def open_map_file(self):
        """ 打开一个地图文件 """

        map_file_path = QtGui.QFileDialog.getOpenFileName(
            self.view, u"打开地图文件", filter="*.mcm")

        if map_file_path:
            try:
                self.tiled_map = tiled_map.TiledMapSerializer().read_from_file(
                    map_file_path)
            except Exception as e:
                message = u"打开地图文件时出现异常：%s" % e.message
                QtGui.QMessageBox.warning(None, u"警告", message)
                return

            self.view.on_changed_tiled_map(self.tiled_map)

    def open_map_picture(self):
        """ 打开游戏地图的背景图片 """

        image_file_path = QtGui.QFileDialog.getOpenFileName(
            self.view, u"打开背景文件", filter="*.jpg")

        if image_file_path:
            map_image = QtGui.QImage()
            if not map_image.load(image_file_path):
                message = u"打开地图图片错误:%s" % image_file_path
                QtGui.QMessageBox.warning(None, u"错误", message)
                return

            self.view.on_changed_map_image(map_image)

    def save_map_file(self):
        """ 保存地图文件 """
        file_path = QtGui.QFileDialog.getSaveFileName(
            self.view, u"保存地图文件", "", ".mcm")
        if file_path:
            try:
                tiled_map.TiledMapSerializer().dump_to_file(
                    self.tiled_map, file_path)
            except Exception as e:
                message = u"保存地图文件时出现异常：%s" % e.message
                QtGui.QMessageBox.warning(None, u"警告", message)
                return

    def quit(self):
        """ 退出程序 """
        QtGui.QMessageBox.warning(None, u"退出", u"警告")

    def init(self):
        self.map_widget = EditorWidget(self)
        self.view = self.map_widget

        self.main_window = MainWindow(self)
        self.main_window.setCentralWidget(self.map_widget)
        self.main_window.show()

        self.create_new_map()
