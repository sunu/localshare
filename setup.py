# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='localshare',
    version='0.1',
    py_modules=['localshare'],
    install_requires=[
        'Click',
        'zeroconf',
        'netifaces'
    ],
    entry_points='''
        [console_scripts]
        localshare=localshare:cli
    ''',
    url='https://github.com/sunu/localshare',
    license='MIT',
    author='sunu',
    author_email='sunu@sunu.in',
    description='localshare: A commandline utility to share files over local network.'
)