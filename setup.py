#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='xunitparserx',
    version='1.9.10',
    description='Read JUnit/XUnit/MSTest XML files and map them to Python objects',
    long_description=open('readme.rst').read(),
    install_requires=[
       'lxml',
       'pytest'
    ],
    author='Laurent Bachelier, Cong Zhang',
    author_email='laurent@bachelier.name, congzhangzh@gmail.com',
    maintainer='Cong Zhang',
    maintainer_email='congzhangzh@gmail.com',
    url='https://github.com/medlab/xunitparserx',
    py_modules=['xunitparserx'],
    data_files=[('trx-to-junit.xslt')],
    test_suite='test',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Testing',
    ],
)
