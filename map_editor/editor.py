#*_* coding=utf8 *_*
#!/usr/bin/env python

import sys
from PyQt4 import QtCore, QtGui

app = QtGui.QApplication(sys.argv)

class MapEdiorWindow(QtGui.QMainWindow):
    
    """ 地图编辑器 """
    
    def __init__( self ):
        QtGui.QMainWindow.__init__( self )
        self.init()
        self.setup_file_menu()

    def init(self):
        self.setWindowTitle(u"mcm地图编辑器")
        self.resize(300, 200)

    def setup_file_menu(self):
        open_action = QtGui.QAction('&Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open Mcm file')
        open_action.triggered.connect(self.open_mcm_file)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(open_action)

    def open_mcm_file(self):
        pass

MapEditorWindow = MapEdiorWindow()

def start():
    MapEditorWindow.show()
    app.exec_()

if __name__ == '__main__':
    start()