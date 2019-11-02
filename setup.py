#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2008-2014 Erik Svensson <erik.public@gmail.com>
# Copyright (c) 2019 Janne K <0x022b@gmail.com>
# Licensed under the MIT license.

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='transmissionrpc-ng',
    version='0.13.0',
    author='Janne K',
    author_email='0x022b@gmail.com',
    description='Python module that implements the Transmission BitTorent client RPC protocol.',
    long_description=long_description,
    long_description_content_type="text/markdown",
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
    ],
    python_requires='>=3.6',
)
