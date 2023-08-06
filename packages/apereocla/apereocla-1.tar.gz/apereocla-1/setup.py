#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='apereocla',
    version='1',
    py_modules=['apereocla'],
    description='Easy access to list of completed Apereo CLAs',
    author='Lars Kiesow',
    author_email='lkiesow@uos.de',
    url='https://github.com/lkiesow/python-apereocla',
    license='MIT',
    install_requires=[
        'requests',
        'beautifulsoup4'
    ],
    entry_points={
        'console_scripts': [
            'apereocla = apereocla:main'
        ]
    }
)
