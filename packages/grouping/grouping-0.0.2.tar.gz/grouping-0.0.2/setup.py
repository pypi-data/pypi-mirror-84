#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
from setuptools import setup

setup(
    name = 'grouping',
    version='0.0.2',
    license='GNU General Public License v3',
    author='Travis Li',
    author_email='weixing.li@verisk.com',
    description='Display and adjust the grouping results',
    packages=['grouping'],
    platforms='any',
    install_requires=[
        'flask',
    ],
    classifiers=[],
    include_package_data=True,
    entry_points={
        'console_scripts': ['grouping_run=grouping.cli:main']
    }
)
