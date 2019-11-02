#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2008-2014 Erik Svensson <erik.public@gmail.com>
# Copyright (c) 2019 Janne K <0x022b@gmail.com>
# Licensed under the MIT license.

from setuptools import setup

setup(
    name='transmissionrpc-ng',
    version='0.12.0',
    description='Python module that implements the Transmission BitTorent client RPC protocol.',
    author='Janne K',
    author_email='0x022b@gmail.com',
    url='https://github.com/0x022b/transmissionrpc-ng',
    keywords='transmission bittorent torrent',
    packages=['transmissionrpc'],
    test_suite="test",
    zip_safe=True,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Communications :: File Sharing',
        'Topic :: Internet'
    ]
)
