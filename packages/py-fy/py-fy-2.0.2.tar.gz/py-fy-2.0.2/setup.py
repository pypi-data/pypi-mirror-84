#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "py-fy",      #这里是pip项目发布的名称
    version = "2.0.2",  #版本号，数值大的会优先被pip
    keywords = ("pip", "py-fy","translate", "fy"),
    description = "An Word-translation software simple-Chinese ⇆ English",
    long_description = "An Word-translation software simple-Chinese ⇆ English",
    license = "MIT Licence",
    url = "https://github.com/zwlyn/pyfy",     #项目相关文件地址，一般是github
    author = "zwlyn",
    author_email = "1666013677@qq.com",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["pymouse", "pyinstaller"],          #这个项目需要的第三方库
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ]
)

