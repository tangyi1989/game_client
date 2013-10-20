#*_* coding=utf8 *_*
#!/usr/bin/env python

import sys
import tiled_map
from PyQt4 import QtCore, QtGui

"""
地图编辑器

作者：唐万万
"""

app = QtGui.QApplication(sys.argv)


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
        try:
            self.tiled_map = tiled_map.TiledMapSerializer().read_from_file(
                map_file_path)
        except Exception as e:
            message = u"打开地图文件时出现异常：%s" % e.message
            QtGui.QMessageBox.warning(None, message, u"警告")
            return

        self.view.on_changed_tiled_map(self.tiled_map)

    def open_map_picture(self):
        """ 打开游戏地图的背景图片 """

        image_file_path = QtGui.QFileDialog.getOpenFileName(
            self.view, u"打开背景文件", filter="*.jpg")

        map_image = QtGui.QImage()
        if not map_image.load(image_file_path):
            message = u"打开地图图片错误:%s" % image_file_path
            QtGui.QMessageBox.warning(None, message, u"错误")
            return

        self.view.on_changed_map_image(map_image)

    def save_map_file(self):
        """ 保存地图文件 """
        pass

    def quit(self):
        """ 退出程序 """
        QtGui.QMessageBox.warning(None, u"退出", u"警告")

    def init(self):
        self.map_widget = MapWidget(self)
        self.view = self.map_widget

        self.main_window = MainWindow(self)
        self.main_window.setCentralWidget(self.map_widget)
        self.main_window.show()

        self.create_new_map()


class ThumbMapWidget(QtGui.QWidget):

    """ 地图缩略图 """

    def __init__(self, controller, parent=None):
        pass


class TiledMapIsNone(Exception):
    pass


class TiledMapWidget(QtGui.QWidget):

    """ 编辑地图区域 """

    def __init__(self, parent=None):
        super(TiledMapWidget, self).__init__(parent)
        self.resize(600, 600)
        self.setMinimumSize(600, 600)  # 这个属性是用于支持Widget布局的

        self.map_image = None
        self.tiled_map = None

        # 设置一张画布，在绘制的时候，画在内存中，再进行重绘时，再将其画在上面
        rect = self.contentsRect()
        self.rect_width = rect.width()
        self.rect_height = rect.height()

        # 格子数目
        self.tile_x_num = 30
        self.tile_y_num = 30

        self.tile_width = int(self.rect_width / self.tile_x_num)
        self.tile_height = int(self.rect_height / self.tile_y_num)

        # 起始坐标
        self.tile_begin_x = 0
        self.tile_begin_y = 0

        # 鼠标位于的正要操作的那个网格
        self.active_grid = None

        # 要显示的图层
        self.displayed_tiled_layer = 'exist'

        self.init_pixmap()
        self.setup_timer()

    def init_pixmap(self):
        # 地图后面的图片
        self.map_image_pixmap = QtGui.QPixmap(
            self.rect_width, self.rect_height)
        self.set_alpha_channel(self.map_image_pixmap)

        # Tiled层
        self.tiled_layer_pixmap = QtGui.QPixmap(
            self.rect_width, self.rect_height)
        self.tiled_layer_mask = None

        # 网格图片
        self.grid_pixmap = QtGui.QPixmap(self.rect_width, self.rect_height)
        self.grid_mask = None

        # 操作层
        self.operate_layer_pixmap = QtGui.QPixmap(
            self.rect_width, self.rect_height)
        self.operate_layer_mask = None

        # 用于合成然后绘制在屏幕上的 pixmap
        self.buffer_pixmap = QtGui.QPixmap(self.rect_width, self.rect_height)

    def setup_timer(self):
        self.timer = QtCore.QTimer(self)
        self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.timeout)
        self.timer.start(30)

    def set_map_image(self, map_image):
        self.map_image = map_image
        self.paint_map_image()
        # TODO something more

    def set_tiled_map(self, tiled_map):
        self.tiled_map = tiled_map

        # 起始坐标
        self.tile_begin_x = 0
        self.tile_begin_y = 0

        self.paint_grid()
        self.paint_tiled_layer()

    def resize_tiles(self, tile_col, tile_row):
        self.tiled_map.resize_tiles(tile_col, tile_row)

        self.paint_grid()
        self.paint_tiled_layer()

    def get_grid_pos(self, cursor_x, cursor_y):
        """ 根据鼠标的位置，获取当前鼠标放置在哪个网格上 """
        pos_x = int(cursor_x / self.tile_width)
        pos_y = int(cursor_y / self.tile_height)

        return pos_x, pos_y

    def set_alpha_channel(self, pixmap, alpha=10):
        """ 设置pixmap的apha通道（透明处理） """

        alpha_channel = pixmap.alphaChannel()
        painter = QtGui.QPainter()
        painter.begin(alpha_channel)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.white)
        painter.fillRect(pixmap.rect(), QtGui.QBrush(QtGui.QColor(0, 0, 0, alpha)))
        painter.end()
        pixmap.setAlphaChannel(alpha_channel)

        return pixmap

    def timeout(self):
        """ 定时器事件：用于定时得到鼠标位置信息，然后进行地图的移动。 """

        coursor_point = self.mapFromGlobal(QtGui.QCursor.pos())
        if coursor_point.x() >= 0 and coursor_point.y() >= 0 \
            and coursor_point.x() < self.rect_width \
            and coursor_point.y() < self.rect_height:

            grid_pos = self.get_grid_pos(coursor_point.x(), coursor_point.y())
            self.set_active_grid(grid_pos)

        else:
            self.set_active_grid(None)

    def set_active_grid(self, grid):
        """ 设置当前活跃的位置 """
        if grid == self.active_grid:
            return

        self.active_grid = grid
        self.paint_operate_layer()

    def paintEvent(self, event):
        # 将pixmap画在Widget上
        p = QtGui.QPainter(self)
        p.drawPixmap(0, 0, self.buffer_pixmap)

    def repaint(self):
        """
        将所有的Pixmap合成一个Pixmap
        然后触发 paintEvent 将合成图画在widget上
        """

        painter = QtGui.QPainter()
        painter.begin(self.buffer_pixmap)

        # 底层，地图图片层
        painter.drawPixmap(0, 0, self.map_image_pixmap)

        # tiled层
        if self.tiled_layer_mask:
            self.tiled_layer_pixmap.setMask(self.tiled_layer_mask)
        painter.drawPixmap(0, 0, self.tiled_layer_pixmap)
        self.set_alpha_channel(self.tiled_layer_pixmap)

        # 网格层
        if self.grid_mask:
            self.grid_pixmap.setMask(self.grid_mask)
        painter.drawPixmap(0, 0, self.grid_pixmap)

        # 操作层
        if self.operate_layer_mask:
            self.operate_layer_pixmap.setMask(self.operate_layer_mask)
        painter.drawPixmap(0, 0, self.operate_layer_pixmap)

        painter.end()
        self.update()

    def paint_tiled_layer(self):
        """ 绘制tiled层(只绘制某一层) """

        try:
            layer_color = QtGui.QColor(0x00ff00)

            background_color = QtGui.QColor(0x000000)
            painter = QtGui.QPainter()
            painter.begin(self.tiled_layer_pixmap)
            painter.fillRect(
                0, 0, self.rect_width, self.rect_height, background_color)

            if tiled_map is None:
                raise TiledMapIsNone

            tile_end_x = self.tiled_map.tile_col - self.tile_begin_x
            tile_end_y = self.tiled_map.tile_row - self.tile_begin_y

            if tile_end_x - self.tile_begin_x > self.tile_x_num:
                tile_end_x = self.tile_begin_x + self.tile_x_num

            if tile_end_y - self.tile_begin_y > self.tile_y_num:
                tile_end_y = self.tile_begin_y + self.tile_y_num

            for x in xrange(self.tile_begin_x, tile_end_x):
                for y in xrange(self.tile_begin_y, tile_end_y):
                    tile = self.tiled_map.get_tile(x, y)
                    filled = getattr(tile, self.displayed_tiled_layer)

                    if filled:
                        painter.fillRect(
                            x * self.tile_width, y * self.tile_height,
                            self.tile_width, self.tile_height, layer_color)

        except TiledMapIsNone:
            pass
        except Exception as e:
            print 'Exception : %s' % e.message
            raise e
        finally:
            painter.end()
            self.tiled_layer_mask = self.tiled_layer_pixmap.createMaskFromColor(
                background_color)
            self.repaint()

    def paint_operate_layer(self):
        """ 绘制操作层 """

        try:
            background_color = QtGui.QColor(0x000000)
            painter = QtGui.QPainter()
            painter.begin(self.operate_layer_pixmap)
            painter.fillRect(
                0, 0, self.rect_width, self.rect_height, background_color)

            if self.tiled_map is None:
                raise TiledMapIsNone

            painter.setPen(QtGui.QColor(255, 0, 0))

            if self.active_grid is not None:

                begin_x = self.active_grid[0] * self.tile_width
                begin_y = self.active_grid[1] * self.tile_height

                painter.drawRect(
                    begin_x, begin_y, self.tile_width, self.tile_height)
        except TiledMapIsNone:
            pass
        finally:
            painter.end()
            self.operate_layer_mask = self.operate_layer_pixmap.createMaskFromColor(
                background_color)
            self.repaint()

    def paint_grid(self):
        """ 画出地图网格 """

        try:
            painter = QtGui.QPainter()
            painter.begin(self.grid_pixmap)

            background_color = QtGui.QColor(0x000000)
            painter.fillRect(
                0, 0, self.rect_width, self.rect_height, background_color)

            if self.tiled_map is None:
                raise TiledMapIsNone

            painter.setPen(QtGui.QColor(255, 255, 0))

            tile_x_num = self.tiled_map.tile_col - self.tile_begin_x
            if tile_x_num > self.tile_x_num:
                tile_x_num = self.tile_x_num

            tile_y_num = self.tiled_map.tile_row - self.tile_begin_y
            if tile_y_num > self.tile_y_num:
                tile_y_num = self.tile_y_num

            end_x = tile_x_num * self.tile_width
            end_y = tile_y_num * self.tile_height

            for y in xrange(0, tile_y_num + 1):
                for x in xrange(0, tile_x_num + 1):
                    painter.drawLine(
                        x * self.tile_width, 0, x * self.tile_width, end_y)
                    painter.drawLine(
                        0, y * self.tile_height, end_x, y * self.tile_height)
        except TiledMapIsNone:
            pass
        finally:
            self.grid_mask = self.grid_pixmap.createMaskFromColor(
                background_color)
            painter.end()
            self.repaint()

    def paint_map_image(self):
        """ 绘制地图背景图片 """
        if self.map_image is None:
            return

        background_color = QtGui.QColor(0x000000)

        painter = QtGui.QPainter()
        painter.begin(self.map_image_pixmap)

        painter.fillRect(
            0, 0, self.rect_width, self.rect_height, background_color)
        paint_begin_x = self.tile_begin_x * self.tile_width
        paint_begin_y = self.tile_begin_y * self.tile_height
        painter.drawImage(paint_begin_x, paint_begin_y, self.map_image)

        painter.end()
        self.repaint()


class MapWidget(QtGui.QWidget):

    """ 地图编辑器主Widget """

    def __init__(self, controller, parent=None):
        super(MapWidget, self).__init__(parent)
        self.controller = controller
        self.tiled_map = None
        self.setup_layout()

    def setup_layout(self):
        """ 设置界面布局 """

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

        # 右边的布局
        right_layout = QtGui.QFormLayout()
        right_layout.addRow(map_name, self.map_name_edit)
        right_layout.addRow(map_picture, self.map_picture_edit)
        right_layout.addRow(tile_col, self.tile_col_box)
        right_layout.addRow(tile_row, self.tile_row_box)
        right_layout.addWidget(self.resize_tiles_button)

        self.exist_layer_button = QtGui.QPushButton(u'Exist层')
        self.element_layer_button = QtGui.QPushButton(u'Element层')
        # right_layout.addWidget(self.exist_layer_button)
        # right_layout.addWidget(self.element_layer_button)

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

    def on_changed_tiled_map(self, tiled_map):
        self.tiled_map = tiled_map
        self.tiled_map_widget.set_tiled_map(tiled_map)
        self.map_name_edit.setText(tiled_map.map_name)
        self.map_picture_edit.setText(tiled_map.map_picture)
        self.tile_col_box.setValue(tiled_map.tile_col)
        self.tile_row_box.setValue(tiled_map.tile_row)

    def on_changed_map_image(self, map_image):
        self.tiled_map_widget.set_map_image(map_image)


class MainWindow(QtGui.QMainWindow):

    """ 
    主窗口，之所以分离出来MainWindow和MainMapEditorWidget
    是因为QMainWidnow不支持SetLout只支持setCenterWidget.
    """

    def __init__(self, controller):
        super(MainWindow, self).__init__()
        self.title_prefix = u"Map地图编辑器"
        self.controller = controller
        self.init_UI()

    def init_UI(self):
        self.setup_menu()
        self.setWindowTitle(self.title_prefix)
        self.resize(820, 620)

    def setup_menu(self):
        """ 设置目录 """

        # 打开地图文件
        create_action = QtGui.QAction('&Create New Map', self)
        create_action.setShortcut('Ctrl+O')
        create_action.setStatusTip('Create new map')
        create_action.triggered.connect(self.controller.create_new_map)

        # 打开地图文件
        open_map_picture_action = QtGui.QAction(
            'Open Map &Backgound Image File', self)
        open_map_picture_action.setShortcut('Ctrl+O')
        open_map_picture_action.setStatusTip('Open map file')
        open_map_picture_action.triggered.connect(
            self.controller.open_map_picture)

        # 打开地图文件
        open_action = QtGui.QAction('&Open Map File', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open map file')
        open_action.triggered.connect(self.controller.open_map_file)

        # 关闭地图文件
        save_action = QtGui.QAction('&Save Map File', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Save map file')
        save_action.triggered.connect(self.controller.save_map_file)

        # 退出程序
        quit_action = QtGui.QAction('&Qave Application', self)
        quit_action.setShortcut('Ctrl+Q')
        quit_action.setStatusTip('Quit')
        quit_action.triggered.connect(self.controller.quit)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(create_action)
        file_menu.addAction(open_action)
        file_menu.addAction(open_map_picture_action)
        file_menu.addAction(save_action)
        file_menu.addAction(quit_action)


if __name__ == '__main__':
    MapController().init()
    app.exec_()
