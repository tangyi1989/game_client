# *_* coding=utf8 *_*
#!/usr/bin/env python

import os

class Config(object):

    def __init__(self, config_list):
        self.config_dict = dict()
        for (key, value) in config_list:
            self.config_dict.setdefault(key, value)

    def __getattr__(self, key):
        return self.config_dict[key]

medusa_config = [
    ("data_path", os.path.join(os.path.dirname(__name__) , "data")),
    ("caption", "Medusa Client"),
    ("window_width", 800),
    ("window_height", 600),
]

CONF = Config(medusa_config)