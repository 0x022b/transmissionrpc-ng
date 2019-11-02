# -*- coding: utf-8 -*-
# Copyright (c) 2011-2014 Erik Svensson <erik.public@gmail.com>
# Copyright (c) 2019 Janne K <0x022b@gmail.com>
# Licensed under the MIT license.

import re
from base64 import b64encode
from io import BytesIO

import pycurl
from transmissionrpc.error import HTTPHandlerError


class HTTPHandler:
    """
    Prototype for HTTP handling.
    """

    def set_authentication(self, uri, login, password):
        """
        Transmission use basic authentication in earlier versions and digest
        authentication in later versions.

         * uri, the authentication realm URI.
         * login, the authentication login.
         * password, the authentication password.
        """
        raise NotImplementedError(
            "Bad HTTPHandler, failed to implement set_authentication.")

    def request(self, url, query, headers, timeout):
        """
        Implement a HTTP POST request here.

         * url, The URL to request.
         * query, The query data to send. This is a JSON data string.
         * headers, a dictionary of headers to send.
         * timeout, requested request timeout in seconds.
        """
        raise NotImplementedError(
            "Bad HTTPHandler, failed to implement request.")


class DefaultHTTPHandler(HTTPHandler):
    """
    The default HTTP handler provided with transmissionrpc.
    """

    def __init__(self):
        HTTPHandler.__init__(self)

    def _response_encoding(self, headers):
        encoding = None

        # Figure out what encoding was sent with the response, if any.
        # Check against lowercased header name.
        if headers and 'content-type' in headers:
            content_type = headers['content-type'].lower()
            match = re.search(r'charset=(\S+)', content_type)
            if match:
                encoding = match.group(1)

        if encoding is None:
            # Default encoding for HTML is iso-8859-1.
            # Other content types may have different default encoding,
            # or in case of binary data, may have no encoding at all.
            encoding = 'iso-8859-1'

        return encoding

    def _response_headers(self, buffer):
        headers = {}

        # HTTP standard specifies that headers are encoded in iso-8859-1.
        for line in buffer.getvalue().decode('iso-8859-1').splitlines():
            # Header lines include the first status line (HTTP/1.x ...).
            # We are going to ignore all lines that don't have a colon in them.
            # This will botch headers that are split on multiple lines...
            if ':' not in line:
                continue

            # Break the header line into header name and value.
            name, value = line.split(':', 1)

            # Remove whitespace that may be present.
            # Header lines include the trailing newline, and there may be
            # whitespace around the colon.
            name = name.strip()
            value = value.strip()

            # Header names are case insensitive.
            # Lowercase name here.
            name = name.lower()

            # Now we can actually record the header name and value.
            # Note: this only works when headers are not duplicated.
            headers[name] = value

        return headers

    def set_authentication(self, uri, login, password):
        self._authorization = b64encode(
            bytearray('{}:{}'.format(login, password), 'utf-8')).decode('utf-8')

    def request(self, url, query, headers, timeout):
        request_headers = ['{}: {}'.format(k, v) for k, v in headers.items()]

        if self._authorization:
            request_headers += ['Authorization: Basic {}'.format(self._authorization)]

        buf1, buf2 = BytesIO(), BytesIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.TIMEOUT, int(timeout))
        c.setopt(pycurl.POSTFIELDS, query)
        c.setopt(pycurl.HTTPHEADER, request_headers)
        c.setopt(pycurl.WRITEFUNCTION, buf1.write)
        c.setopt(pycurl.HEADERFUNCTION, buf2.write)
        c.perform()

        response_code = c.getinfo(pycurl.RESPONSE_CODE)
        c.close()
        response_headers = self._response_headers(buf2)
        encoding = self._response_encoding(response_headers)
        response_body = buf1.getvalue().decode(encoding)

        if response_code == 200:
            return response_body
        else:
            raise HTTPHandlerError(
                url, response_code, None, response_headers, response_body)
