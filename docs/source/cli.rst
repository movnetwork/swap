============================
Command Line Interface (CLI)
============================

After you have installed, type ``shuttle`` to verify that it worked:

::

    $ shuttle
    Usage: shuttle [OPTIONS] COMMAND [ARGS]...

      SHUTTLE CLI

      Cross-chain atomic swaps between the networks of two cryptocurrencies.

      LICENCE AGPL-3.0 | AUTHOR Meheret Tesfaye | EMAIL meherett@zoho.com

    Options:
      -v, --version  Show Shuttle version and exit.
      -h, --help     Show this message and exit.

    Commands:
      bitcoin  Select bitcoin cryptocurrency provider.
      bytom    Select bytom cryptocurrency provider.


.. click:: shuttle.cli.__main__:shuttle
  :prog: shuttle
  :show-nested: