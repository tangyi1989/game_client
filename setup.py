#!/usr/bin/env python
# *_* coding=utf8 *_*


"""
描述：Medusa安装脚本。
作者：唐万万
"""

import setuptools

requirements = ['PyQt4']

setuptools.setup(
    name="medusa",
    version="2013.9",
    author="TangYi",
    description="Watch our service.",
    packages=['medusa', 'pgu'],
    scripts=['bin/medusa_map_editor', 'bin/medusa_client'],
    install_requires=requirements,
)
