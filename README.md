# transmissionrpc-ng

transmissionrpc-ng is a Python module implementing the JSON-RPC client protocol
for the BitTorrent client Transmission.

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

## License

This project is licensed under the MIT License.

## Developer

transmissionrpc was originally developed by Erik Svensson. The original version
is hosted at [Bitbucket][bitbucket].

Copyright (c) 2008-2014 Erik Svensson\
Copyright (c) 2019 Janne K

[bitbucket]: http://www.bitbucket.org/blueluna/transmissionrpc/
