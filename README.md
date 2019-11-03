# transmissionrpc-ng

![PyPI](https://img.shields.io/pypi/v/transmissionrpc-ng?style=for-the-badge)
![CircleCI](https://img.shields.io/circleci/build/github/0x022b/transmissionrpc-ng?style=for-the-badge)
![LGTM Alerts](https://img.shields.io/lgtm/alerts/github/0x022b/transmissionrpc-ng?style=for-the-badge)
![PyPI - Downloads](https://img.shields.io/pypi/dm/transmissionrpc-ng?style=for-the-badge)
![GitHub](https://img.shields.io/github/license/0x022b/transmissionrpc-ng?style=for-the-badge)

**transmissionrpc-ng** is a Python module implementing the JSON-RPC client
protocol for the BitTorrent client Transmission.

## Getting started

transmissionrpc-ng is compatible with Transmission 1.31 - 2.94.

### Requirements

transmissionrpc-ng requires:

* Python >= 3.6

### Install

transmissionrpc-ng can be installed by either by running `setup.py` or with
`pip`, the package installer for Python.

```shell
python3 setup.py install
```

```shell
python3 -m pip install transmissionprc-ng
```

NOTE: You might need administrator privileges to install Python modules.

## Running unit tests

```shell
pipenv run python3 -m unittest test/*.py
```

## Changelog

See [CHANGELOG][changelog].

## License

This project is licensed under the MIT License.

## Developers

Copyright (c) 2008-2014 [Erik Svensson][blueluna]\
Copyright (c) 2019 [Janne K][0x022b]

[0x022b]: https://github.com/0x022b
[blueluna]: https://www.bitbucket.org/blueluna
[changelog]: https://github.com/0x022b/transmissionrpc-ng/blob/master/CHANGELOG.md
