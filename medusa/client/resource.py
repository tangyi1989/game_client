# *_* coding=utf8 *_*
#!/usr/bin/env python

import os
import pyglet
from pyglet import font


def load():
    root_path = os.path.join(os.path.dirname(__file__), "data")

    pyglet.resource.path.append(os.path.join(root_path, "player_action"))
    pyglet.resource.path.append(os.path.join(root_path, "maps/images"))
    pyglet.resource.reindex()

    font.add_directory(os.path.join(root_path, "font"))

load()


class PlayerAction(object):
    actions_up = ['up_1', 'up_2', 'up_3', 'up_4',
                  'up_5', 'up_6', 'up_7', 'up_8']       # don't remove
    actions_down = ['down_1', 'down_2', 'down_3', 'down_4',
                    'down_5', 'down_6', 'down_7', 'down_8']
    actions_left = ['left_1', 'left_2', 'left_3', 'left_4',
                    'left_5', 'left_6', 'left_7', 'left_8']
    actions_right = ['right_1', 'right_2', 'right_3', 'right_4',
                     'right_5', 'right_6', 'right_7', 'right_8']

    images_up = [pyglet.resource.image('boy_%s.png' % action)
                 for action in actions_up]
    images_down = [pyglet.resource.image('boy_%s.png' % action)
                   for action in actions_down]
    images_left = [pyglet.resource.image('boy_%s.png' % action)
                   for action in actions_left]
    images_right = [pyglet.resource.image('boy_%s.png' % action)
                    for action in actions_right]
