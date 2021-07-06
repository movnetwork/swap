===============
Installing Swap
===============

The easiest way to install Swap is via pip:

::

    $ pip install swap


If you want to run the latest version of the code, you can install from git:

::

    $ pip install git+git://github.com/meherett/swap.git


For the versions available, see the `tags on this repository <https://github.com/meherett/swap/tags>`_.

Development
===========

We welcome pull requests. To get started, just fork this `github repository <https://github.com/meherett/swap>`_, clone it locally, and run:

::

    $ pip install -e . -r requirements.txt

Once you have installed, type ``swap`` to verify that it worked:

::

    $ swap
    Usage: swap [OPTIONS] COMMAND [ARGS]...

    Options:
      -v, --version  Show Swap version and exit.
      -h, --help     Show this message and exit.

    Commands:
      bitcoin  Select Bitcoin provider.
      bytom    Select Bytom provider.
      vapor    Select Vapor provider.

Dependencies
============

Swap has the following dependencies:

* `solc v0.8.3 <https://github.com/ethereum/solidity/releases/tag/v0.8.3>`_ - Solidity, the Smart Contract Programming Language
* `bytom-wallet-desktop <https://bytom.io/en/wallet/>`_ - version `1.1.0 <https://github.com/Bytom/bytom/releases/tag/v1.1.0>`_  or greater.
* `vapor-wallet-desktop <https://github.com/Bytom/vapor/releases/>`_ - version `1.1.7 <https://github.com/Bytom/vapor/releases/tag/v1.1.7>`_  or greater.
* `pip <https://pypi.org/project/pip/>`_ - To install packages from the Python Package Index and other indexes
* `python3 <https://www.python.org/downloads/release/python-368/>`_ version 3.6 or greater
