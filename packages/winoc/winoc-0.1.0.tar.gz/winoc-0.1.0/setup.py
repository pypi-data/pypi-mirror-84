#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: cluckbird
# Mail: admin@muzmn.cn
# Created Time:  2020-11-4 7:44
#############################################

from setuptools import setup, find_packages

setup(
    name = "winoc",
    version = "0.1.0",
    keywords = ("pip", "pathtool","timetool", "magetool", "mage"),
    description = "Get windows CPU/RAM resource usage: https://github.com/cluckbird/pip-winoc",
    long_description = "Get windows CPU/RAM resource usage: https://github.com/cluckbird/pip-winoc",
    license = "MIT Licence",
    url = "https://github.com/cluckbird/pip-winoc",
    author = "cluckbird",
    author_email = "admin@muzmn.cn",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = [
        'wmi',
        'psutil',
    ]
)