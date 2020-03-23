# Shuttle

[![Build Status](https://travis-ci.com/meherett/shuttle.svg?branch=master)](https://travis-ci.com/meherett/shuttle)
![PyPI Version](https://img.shields.io/pypi/v/pyshuttle.svg?color=blue)
![PyPI License](https://img.shields.io/pypi/l/pyshuttle.svg?color=black)

Shuttle is a python library for cross-chain atomic swaps between the networks of two cryptocurrencies. ​Cross-chain atomic swaps are the cheapest and most secure way to swap cryptocurrencies. It’s a brand new decentralized payment environment based on Hash Time Lock Contracts (HTLCs) protocol.

## Installation
PIP to install shuttle globally. For Linux sudo may be required.
```
$ pip install pyshuttle
```
For the versions available, see the [tags on this repository](https://github.com/meherett/shuttle/tags).

## Development
We welcome pull requests. To get started, just fork this repo, clone it locally, and run:
```
$ pip install -e . -r requirements.txt
```

## Testing
Tests are still under development.

You can run the tests with:

```
$ pytest tests
```

Or use `tox` to run the complete suite against the full set of build targets, or pytest to run specific 
tests against a specific version of Python.

## Contributing
Feel free to open an issue if you find a problem, or a pull request if you've solved an issue.

## Author

Meheret Tesfaye – [@meherett](https://github.com/meherett) – meherett@zoho.com

See also the list of [contributors](https://github.com/meherett/shuttle/graphs/contributors) who participated in this project.

## License

GNU AFFERO GENERAL PUBLIC LICENSE VERSION - 3.0

Distributed under the [AGPL-3.0](https://github.com/meherett/shuttle/LICENSE) license. See ``LICENSE`` for more information.
