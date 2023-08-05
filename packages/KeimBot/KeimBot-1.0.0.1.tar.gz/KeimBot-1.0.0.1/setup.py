#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: mage
# Mail: mage@woodcol.com
# Created Time:  2018-1-23 19:17:34
#############################################


from setuptools import setup, find_packages

setup(
    name = "KeimBot",
    version = "1.0.0.1",
    keywords = ("python", "pip","Bot", "KeimSoft", "Baidu-aip"),
    description = "Customer Bot",
    #long_description = "time and path tool",
    license = "Keimsoft Licence",

    url = "https://github.com/f21281046/Bot",
    author = "zhaofeng",
    author_email = "zhaofeng_qjj@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['pyperclip','pyautogui','win32gui','win32con','win32gui','win32api','cv2','numpy','baidu-aip','PIL']
)