# Changelog

This project is using [Semantic Versioning 2.0.0][semver] starting from release
0.12.0.

## transmissionrpc-ng 0.13.0

- Remove non-printable characters from RPC responses
- Added support for gzip encoded torrents

## transmissionrpc-ng 0.12.0

- Renamed the fork to transmissionrpc-ng
- Started using semantic versioning
- Fixed lots of static code analysis issues
- Removed deprecated methods
- Dropped support for Python 2

## transmissionrpc 0.11

- Added support for Transmission RPC version 15.
- Minor fixes.

## transmissionrpc 0.10

- Support for Python 3 through "six".
- Dropping support for Python 2.5.
- Removed modification of default url opener.
- Description of all Transmission RPC fields in Torrent and Session.

## transmissionrpc 0.9

- Fixed message handling in TransmissionError. Issue #35. Thanks Adam Rothman.
- Made Client.start_all honour queue order. Thanks stephenharrell.
- Changed interface for Client.
- Added mutators to Torrent and Session.

## transmissionrpc 0.8

- Fixed argument "location" falsely named "ids" for Client.change. Issue #31.
- Fixed Torrent.ratio to use response value uploadRatio. Issue #30.

## transmissionrpc 0.7

- Added support for Transmission RPC version 10 and 11.
- Fixed an issue with Python 2.7 urllib2 handling. Issue #24.

## transmissionrpc 0.6

- Added support for Transmission RPC version 9.
- Fixed handing of exceptions from urllib2.urlopen. Issues #21 and #22.
- Fixed test suite to handle structure comparisons better.

[semver]: https://semver.org/spec/v2.0.0.html
