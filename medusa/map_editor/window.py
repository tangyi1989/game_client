#*_* coding=utf8 *_*
#!/usr/bin/env python

from PyQt4 import QtGui

"""
Map editor 的主窗口

作者：唐万万
时间：2013-10-23
"""

class MainWindow(QtGui.QMainWindow):

    """ 
    主窗口，之所以分离出来MainWindow和MainMapEditorWidget
    是因为QMainWidnow不支持SetLout只支持setCenterWidget.
    """

    def __init__(self, controller):
        super(MainWindow, self).__init__()
        self.title_prefix = u"地图编辑器"
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

