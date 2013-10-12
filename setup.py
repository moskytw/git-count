#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

import gitcount

setup(

    name = 'git-count',
    version = gitcount.__version__,
    description = 'Count your commits.',
    long_description = open('README.rst').read(),

    author = 'Mosky',
    url = 'https://github.com/moskytw/git-count',
    author_email = 'mosky.tw@gmail.com',
    license = 'MIT',
    platforms = 'any',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
        'Topic :: Software Development',
    ],


    install_requires = ['clime>=0.2'],
    py_modules = ['gitcount'],

    entry_points = {
         'console_scripts': [
             'git-count = gitcount:main',
        ]
    }

)

