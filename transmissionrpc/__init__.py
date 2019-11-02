# -*- coding: utf-8 -*-
# Copyright (c) 2008-2014 Erik Svensson <erik.public@gmail.com>
# Copyright (c) 2019 Janne K <0x022b@gmail.com>
# Licensed under the MIT license.

from transmissionrpc.constants import DEFAULT_PORT, DEFAULT_TIMEOUT, PRIORITY, RATIO_LIMIT, LOGGER  # noqa: F401
from transmissionrpc.error import TransmissionError, HTTPHandlerError  # noqa: F401
from transmissionrpc.httphandler import HTTPHandler, DefaultHTTPHandler  # noqa: F401
from transmissionrpc.torrent import Torrent  # noqa: F401
from transmissionrpc.session import Session  # noqa: F401
from transmissionrpc.client import Client  # noqa: F401
from transmissionrpc.utils import add_stdout_logger, add_file_logger  # noqa: F401

__author__ = 'Erik Svensson <erik.public@gmail.com>'
__version_major__ = 0
__version_minor__ = 12
__version__ = '{0}.{1}'.format(__version_major__, __version_minor__)
__copyright__ = 'Copyright (c) 2008-2014 Erik Svensson'
__license__ = 'MIT'
