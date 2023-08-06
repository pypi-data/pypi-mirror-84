#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: cluckbird
# Mail: admin@muzmn.cn
# Created Time:  2020-11-3 16:35
#############################################

from setuptools import setup, find_packages

setup(
    name = "fasthash",
    version = "0.1.1",
    keywords = ("pip", "pathtool","timetool", "magetool", "mage"),
    description = "Fast calculation hash 256/512/1",
    long_description = "Fast calculation hash 256/512/1",
    license = "MIT Licence",
    url = "https://github.com/cluckbird/pip-hashsha",
    author = "cluckbird",
    author_email = "admin@muzmn.cn",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []
)