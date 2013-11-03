#*_* coding=utf8 *_*
#!/usr/bin/env python

import os
import signal


def drop_terminal():
    """ 让程序(Gui程序)脱离terminal运行。 """
    
    # drop tty
    if os.fork() != 0:
        os._exit(0)  # pylint: disable=W0212

    os.setsid()

    # drop stdio
    for fd in range(0, 2):
        try:
            os.close(fd)
        except OSError:
            pass

    os.open(os.devnull, os.O_RDWR)
    os.dup2(0, 1)
    os.dup2(0, 2)

    signal.signal(signal.SIGHUP, signal.SIG_IGN)


def gen_move_regions(rect_width, rect_height, region_width=100):
    """
    初始化移动区域所需数据(屏幕坐标系)，转化为游戏坐标系时，请将y轴改变方向

    当鼠标位于如下标注的格子中时，地图将会移动。 
    -------------------------------------
    |       |                   |       |
    |(-1,-1)|      (0, -1)      |(1, -1)|
    |       |                   |       |
    |-----------------------------------|
    |       |                   |       |
    |       |                   |       |
    |       |                   |       |
    |(-1, 0)|       (0, 0)      | (1, 0)|
    |       |                   |       |
    |       |                   |       |
    |       |                   |       |
    |-----------------------------------|
    |       |                   |       |
    |(-1, 1)|      (0, 1)       |(1, 1) |
    |       |                   |       |
    -------------------------------------
    """

    move_regions = [
        # 第一行
        (
            (0, 0,
             region_width, region_width), (-1, -1)
        ),
        (
            (region_width, 0,
             rect_width - region_width, region_width), (0, -1)
        ),
        (
            (rect_width - region_width, 0,
             rect_width, region_width), (1, -1)
        ),
        # 第二行
        (
            (0, region_width,
             region_width, rect_height - region_width), (-1, 0)
        ),
        (
            (region_width, region_width,
             rect_width - region_width, rect_height - region_width), (0, 0)
        ),
        (
            (rect_width - region_width, region_width,
             rect_width, rect_height - region_width), (1, 0)
        ),
        # 第三行
        (
            (0, rect_height - region_width,
             region_width, rect_height), (-1, 1)
        ),
        (
            (region_width, rect_height - region_width,
             rect_width - region_width, rect_height), (0, 1)
        ),
        (
            (rect_width - region_width, rect_height - region_width,
             rect_width, rect_height), (1, 1)
        )
    ]

    return move_regions

def get_move_direct(move_regions, cur_x, cur_y):
    """ 通过鼠标位置，获取需要地图移动的方向 """

    move_direct = (0, 0)

    for move_region in move_regions:

        region = move_region[0]
        direct = move_region[1]

        if cur_x >= region[0] and cur_y >= region[1] \
            and cur_x < region[2] and cur_y < region[3]:

            move_direct = direct
            break

    return move_direct
