#!/usr/bin/env python
# -*- coding:utf8 -*-

from setuptools import find_packages, setup

version = "0.0.0"
long_description = """
    JSP: http://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/jobshop1.txt
    FJSP: http://people.idsia.ch/~monaldo/fjsp.html
    FSP: http://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/flowshop1.txt
    
    Author: Yang Guangcan
    E-mail: 2315466330@qq.com
    """

setup(
    name="shopschedule",
    version=version,
    author="hufuture",
    author_email="1623025938@163.com",
    url=None,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=['numpy', "matplotlib", "plotly", "colorama", "chardet"]
)
