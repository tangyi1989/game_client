#!/usr/bin/env python
# *_* coding=utf8 *_*


"""
描述：Medusa安装脚本。
作者：唐万万
"""

import setuptools
from setuptools import find_packages


setuptools.setup(
    name="medusa",
    version="2013.9",
    author="TangYi",
    description="Watch our service.",
    packages=find_packages(),
    install_requires=['pygame', 'pgu', 'twisted', 'PyQt4'],
    scripts=['bin/medusa_map_editor', 'bin/medusa_client'],
)
