#!/usr/bin/env python
#coding:utf-8

import codecs
import os.path
import re
import sys
from setuptools import find_packages, setup
from ezspot import version

setup(
    name = 'ezspot',
    version = version.VERSION,
    description = 'EZSpot - the spot management tool help you to use AWS EC2 spot instance easily. ',
    long_description=open('README.md').read(),
    url = 'https://github.com/finishy1995/ezspot',
    author = 'David Wang 王元恺',
    author_email = 'finishy@qq.com',
    license = 'MIT',
    keywords = 'cli',
    packages = find_packages(exclude=['examples', 'tests']),
    install_requires = ['six', 'boto3'],
    entry_points = {
        'console_scripts': [
            'ezspot=ezspot.ezspot:main',
        ],
    },
)
