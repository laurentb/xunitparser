#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='xunitparser',
    version='1.3.1',
    description='Read JUnit/XUnit XML files and map them to Python objects',
    long_description=open('README').read(),
    author='Laurent Bachelier',
    author_email='laurent@bachelier.name',
    url='http://git.p.engu.in/laurentb/xunitparser/',
    py_modules=['xunitparser'],
    test_suite='test',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    use_2to3=True,
)
