# -*- coding: utf-8 -*-
# Copyright (c) 2008-2014 Erik Svensson <erik.public@gmail.com>
# Copyright (c) 2019 Janne K <0x022b@gmail.com>
# Licensed under the MIT license.
# flake8: noqa

from transmissionrpc.constants import (
    DEFAULT_PORT,
    DEFAULT_TIMEOUT,
    PRIORITY,
    RATIO_LIMIT,
    LOGGER,
)
from transmissionrpc.error import TransmissionError, HTTPHandlerError
from transmissionrpc.httphandler import HTTPHandler, DefaultHTTPHandler
from transmissionrpc.torrent import Torrent
from transmissionrpc.session import Session
from transmissionrpc.client import Client
from transmissionrpc.utils import add_stdout_logger, add_file_logger

__author__ = "Janne K <0x022b@gmail.com>"
__version_major__ = 0
__version_minor__ = 14
__version_patch__ = 0
__version__ = "{0}.{1}.{2}".format(
    __version_major__, __version_minor__, __version_patch__
)
__copyright__ = "Copyright (c) 2008-2014 Erik Svensson, Copyright (c) 2019 Janne K"
__license__ = "MIT"
