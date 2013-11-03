#*_* coding=utf8 *_*
#!/usr/bin/env python


from PyQt4 import QtCore, QtGui

from medusa.exception import TiledMapIsNone
from medusa.utils import misc as util_misc

"""
编辑地图区域控件

作者：唐万万
时间：2013-10-23
"""


class TiledMapWidget(QtGui.QWidget):

    """ 编辑地图区域控件 """

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

        # 起始格子位置
        self.tile_begin_x = 0
        self.tile_begin_y = 0

        # 设置地图图片偏移
        self.map_image_offset_x = 0
        self.map_image_offset_y = 9

        # 鼠标位于的正要操作的那个网格
        self.active_grid = None

        # 要显示的图层
        self.displayed_tiled_layer = 'exist'

        # 定时器时间
        self.timer_ms = 30
        # 此结构是为了控制移动速度
        self.direct_stack = []
        self.repainted = False

        self.move_regions = util_misc.gen_move_regions(
            self.rect_width, self.rect_height)
        self.init_pixmap()
        self.set_tile_size(20, 20)

        self.init_timer()

    def init_pixmap(self):
        # 地图后面的图片
        self.map_image_pixmap = QtGui.QPixmap(
            self.rect_width, self.rect_height)

        # Tiled层
        self.tiled_layer_pixmap = QtGui.QPixmap(
            self.rect_width, self.rect_height)
        self.tiled_layer_mask = None

        # 网格图片
        self.grid_pixmap = QtGui.QPixmap(self.rect_width, self.rect_height)
        self.grid_mask = None

        # 操作层
        self.assist_layer_pixmap = QtGui.QPixmap(
            self.rect_width, self.rect_height)
        self.assist_layer_mask = None

        # 用于合成然后绘制在屏幕上的 pixmap
        self.buffer_pixmap = QtGui.QPixmap(self.rect_width, self.rect_height)

    def init_timer(self):
        self.timer = QtCore.QTimer(self)
        self.connect(
            self.timer, QtCore.SIGNAL("timeout()"), self.timeout_event)
        self.timer.start(self.timer_ms)

    def set_tile_size(self, width, height):
        """ 设置格子尺寸 """
        self.tile_width = width
        self.tile_height = height
        self.tile_x_num = int(self.rect_width / self.tile_width)
        self.tile_y_num = int(self.rect_height / self.tile_height)
        self.paint_grid()
        self.paint_tiled_layer()

    def set_map_image(self, map_image):
        self.map_image = map_image
        self.paint_map_image()

    def set_tiled_map(self, tiled_map):
        self.tiled_map = tiled_map

        # 起始坐标
        self.tile_begin_x = 0
        self.tile_begin_y = 0

        self.paint_grid()
        self.paint_tiled_layer()
        self.paint_assist_layer()

    def set_layer(self, layer):
        self.displayed_tiled_layer = layer
        self.paint_tiled_layer()
        self.paint_assist_layer()

    def resize_tiles(self, tile_col, tile_row):
        """ 重置地图的尺寸 """
        self.tiled_map.resize_tiles(tile_col, tile_row)

        self.paint_grid()
        self.paint_tiled_layer()

    def move_display_region(self, direct_x, direct_y):
        """ 移动眼睛可以观看的移动区域 """

        def threadhold(val, t_min, t_max):
            if val <= t_min:
                return t_min
            elif val > t_max:
                return t_max
            return val

        def do_move_display(direct_x, direct_y):
            if self.tiled_map is None:
                return

            if self.tiled_map.tile_col - self.tile_x_num > 0:
                max_x = self.tiled_map.tile_col - self.tile_x_num
            else:
                max_x = 0

            if self.tiled_map.tile_row - self.tile_y_num > 0:
                max_y = self.tiled_map.tile_row - self.tile_y_num
            else:
                max_y = 0

            x, y = (self.tile_begin_x, self.tile_begin_y)

            self.tile_begin_x = threadhold(x + direct_x, 0, max_x)
            self.tile_begin_y = threadhold(y + direct_y, 0, max_y)

            if (x, y) != (self.tile_begin_x, self.tile_begin_y):
                self.paint_grid()
                self.paint_map_image()
                self.paint_tiled_layer()

        direct = (direct_x, direct_y)

        d_stack = self.direct_stack
        d_stack.append(direct)

        if len(d_stack) != 2:
            return

        first_d = d_stack[0]
        move = True
        for d in d_stack:
            if d != first_d:
                move = False
                break

        if move:
            do_move_display(*first_d)
            self.direct_stack = []
        else:
            self.direct_stack.pop(0)

    def get_grid_pos(self, cursor_x, cursor_y):
        """ 根据鼠标的位置，获取当前鼠标放置在哪个网格上 """
        pos_x = int(cursor_x / self.tile_width)
        pos_y = int((self.rect_height - cursor_y) / self.tile_height)

        return pos_x, pos_y

    def get_tile_pos(self):
        if self.active_grid:
            x, y = self.active_grid
            x = x + self.tile_begin_x
            y = y + self.tile_begin_y

            if x < self.tiled_map.tile_col and \
                y < self.tiled_map.tile_row:

                return x, y

        return None

    def set_alpha_channel(self, pixmap, alpha=150):
        """ 设置pixmap的apha通道（透明处理） """

        alpha_channel = pixmap.alphaChannel()

        painter = QtGui.QPainter()
        painter.begin(alpha_channel)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.white)
        painter.fillRect(
            pixmap.rect(), QtGui.QBrush(QtGui.QColor(0, 0, 0, alpha)))
        painter.end()

        pixmap.setAlphaChannel(alpha_channel)

        return pixmap

    def set_active_grid(self, grid):
        """ 设置当前活跃的位置 """

        if grid == self.active_grid:
            return

        self.active_grid = grid
        self.paint_assist_layer()

    def timeout_event(self):
        """ 定时器事件：用于定时得到鼠标位置信息，然后进行地图的移动。 """

        coursor_point = self.mapFromGlobal(QtGui.QCursor.pos())
        cur_x, cur_y = coursor_point.x(), coursor_point.y()

        grid_pos = None

        if cur_x >= 0 and cur_y >= 0 and cur_x < self.rect_width \
            and cur_y < self.rect_height:

            # 设置当前鼠标所在的格子位置
            grid_pos = self.get_grid_pos(coursor_point.x(), coursor_point.y())

            # 地图要移动的方向
            direct_x, direct_y = util_misc.get_move_direct(
                self.move_regions, cur_x, cur_y)
            self.move_display_region(direct_x, -direct_y)

        self.set_active_grid(grid_pos)
        if self.repainted:
            self.repaint()
            self.update()

    def paintEvent(self, event):
        # 将pixmap画在Widget上
        p = QtGui.QPainter(self)
        p.drawPixmap(0, 0, self.buffer_pixmap)

    def mousePressEvent(self, event):
        """ 鼠标点击，设置tile """
        pos = self.get_tile_pos()
        if pos:
            x, y = pos
            tile = self.tiled_map.get_tile(x, y)
            val = getattr(tile, self.displayed_tiled_layer)
            setattr(tile, self.displayed_tiled_layer, not val)
            self.paint_tiled_layer()

    def repaint(self):
        """
        将所有的Pixmap合成一个Pixmap
        然后触发 paintEvent 将合成图画在widget上
        """

        painter = QtGui.QPainter()
        painter.begin(self.buffer_pixmap)

        # 先将图片涂黑
        painter.fillRect(0, 0, self.rect_width, self.rect_height,
                         QtGui.QColor(0x000000))

        # 底层，地图图片层
        painter.drawPixmap(0, 0, self.map_image_pixmap)

        # tiled层
        if self.tiled_layer_mask:
            self.tiled_layer_pixmap.setMask(self.tiled_layer_mask)
        painter.drawPixmap(0, 0, self.tiled_layer_pixmap)

        # 网格层
        if self.grid_mask:
            self.grid_pixmap.setMask(self.grid_mask)
        painter.drawPixmap(0, 0, self.grid_pixmap)

        # 操作层
        if self.assist_layer_mask:
            self.assist_layer_pixmap.setMask(self.assist_layer_mask)
        painter.drawPixmap(0, 0, self.assist_layer_pixmap)

        painter.end()

    def paint_tiled_layer(self):
        """ 绘制tiled层(只绘制某一层) """

        try:
            layer_color = QtGui.QColor(0x00ff00)

            background_color = QtGui.QColor(0x000000)
            painter = QtGui.QPainter()
            painter.begin(self.tiled_layer_pixmap)
            painter.fillRect(
                0, 0, self.rect_width, self.rect_height, background_color)

            if self.tiled_map is None:
                raise TiledMapIsNone

            tile_end_x = self.tile_begin_x + self.tile_x_num
            if tile_end_x > self.tiled_map.tile_col:
                tile_end_x = self.tiled_map.tile_col

            tile_end_y = self.tile_begin_y + self.tile_y_num
            if tile_end_y > self.tiled_map.tile_row:
                tile_end_y = self.tiled_map.tile_row

            for x in xrange(self.tile_begin_x, tile_end_x):
                for y in xrange(self.tile_begin_y, tile_end_y):

                    tile = self.tiled_map.get_tile(x, y)
                    filled = getattr(tile, self.displayed_tiled_layer)

                    if filled:
                        painter.fillRect(
                            (x - self.tile_begin_x) * self.tile_width,
                            self.rect_height - (y - self.tile_begin_y + 1) * self.tile_height,
                            self.tile_width, self.tile_height, layer_color)

        except TiledMapIsNone:
            pass
        finally:
            painter.end()
            self.tiled_layer_mask = self.tiled_layer_pixmap.createMaskFromColor(
                background_color)

            if self.tiled_map:
                self.set_alpha_channel(self.tiled_layer_pixmap, 125)

            self.repainted = True

    def paint_assist_layer(self):
        """ 绘制操作层 """

        try:
            background_color = QtGui.QColor(0x000000)
            painter = QtGui.QPainter()
            painter.begin(self.assist_layer_pixmap)
            painter.fillRect(
                0, 0, self.rect_width, self.rect_height, background_color)

            if self.tiled_map is None:
                raise TiledMapIsNone

            painter.setPen(QtGui.QColor(255, 0, 0))
            painter.setFont(QtGui.QFont('Decorative', 20))

            if self.active_grid is not None:

                begin_x = self.active_grid[0] * self.tile_width
                begin_y = self.rect_height - \
                    (self.active_grid[1] + 1) * self.tile_height

                painter.drawRect(
                    begin_x, begin_y, self.tile_width, self.tile_height)

            pos = self.get_tile_pos()
            if pos:
                painter.drawText(
                    QtCore.QRect(10, 30, 200, 30),
                    QtCore.Qt.AlignLeft, "Pos : %s, %s" % (pos[0], pos[1]))

            painter.drawText(
                QtCore.QRect(10, 0, 200, 30),
                QtCore.Qt.AlignLeft, "Layer : %s" % self.displayed_tiled_layer)

        except TiledMapIsNone:
            pass
        finally:
            painter.end()
            self.assist_layer_mask = self.assist_layer_pixmap.createMaskFromColor(
                background_color)

            self.repainted = True

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
            begin_y = self.rect_height - (tile_y_num * self.tile_height)

            for y in xrange(0, tile_y_num + 1):
                for x in xrange(0, tile_x_num + 1):
                    # 纵向的线
                    painter.drawLine(
                        x * self.tile_width, begin_y, x * self.tile_width, self.rect_height)
                    # 横向的线
                    painter.drawLine(
                        0, self.rect_height - y * self.tile_height,
                        end_x, self.rect_height - y * self.tile_height)

        except TiledMapIsNone:
            pass
        finally:
            self.grid_mask = self.grid_pixmap.createMaskFromColor(
                background_color)
            painter.end()
            self.repainted = True

    def paint_map_image(self):
        """ 绘制地图背景图片 """

        if self.map_image is None:
            return

        image_height = self.map_image.height()
        background_color = QtGui.QColor(0x000000)

        painter = QtGui.QPainter()
        painter.begin(self.map_image_pixmap)

        painter.fillRect(
            0, 0, self.rect_width, self.rect_height, background_color)
        paint_begin_x = self.tile_begin_x * self.tile_width
        paint_begin_y = self.rect_height - \
            (image_height - self.tile_begin_y * self.tile_height)

        painter.drawImage(-paint_begin_x, paint_begin_y, self.map_image)

        painter.end()
        self.repainted = True
