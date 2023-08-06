#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import pyframe

setup(

    name='pygame_frame',

    version=pyframe.__version__,

    packages=find_packages(),

    author="PØL1",

    description="A lib to simplify the use of pygame",

    long_description=open('pyframe/README.md').read(),

    install_requires=["numpy","pymunk","pygame"],

    url='https://github.com/paulnbrd/PyFrame/',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9"
    ]
)