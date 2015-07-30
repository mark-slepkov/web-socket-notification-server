#! /usr/bin/env python
__author__ = 'Mark Slepkov'

from setuptools import setup, find_packages
from os.path import join, dirname

requires = [
    'python3-memcached',
    'tornado'
]

setup(
    name='ws_notify',
    version='0.0.5',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    install_requires=requires,
)