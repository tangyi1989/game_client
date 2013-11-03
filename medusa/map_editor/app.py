#*_* coding=utf8 *_*
#!/usr/bin/env python

import sys
from PyQt4 import QtGui

from medusa.utils import misc as misc_utils
from medusa.map_editor import controller

"""
地图编辑器App启动

作者：唐万万
时间：2013-10-23
"""

app = QtGui.QApplication(sys.argv)

def start():
    # misc_utils.drop_terminal()
    controller.MapController().init()
    app.exec_()
