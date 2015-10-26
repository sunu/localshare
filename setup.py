# -*- coding: utf-8 -*-

from distutils.core import setup


classifiers = [
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3 :: Only',
    'Natural Language :: English',
]

setup(
    name='localshare',
    version='0.2',
    py_modules=['localshare', 'utils'],
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
    description='localshare: A commandline utility to share files over local network.',
    classifiers=classifiers,
)
