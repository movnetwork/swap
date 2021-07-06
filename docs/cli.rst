============================
Command Line Interface (CLI)
============================

After you have installed, type ``swap`` to verify that it worked:

::

    $ swap
    Usage: swap [OPTIONS] COMMAND [ARGS]...

    Options:
      -v, --version  Show Swap version and exit.
      -h, --help     Show this message and exit.

    Commands:
      bitcoin   Select Bitcoin provider.
      bytom     Select Bytom provider.
      ethereum  Select Ethereum provider.
      vapor     Select Vapor provider.
      xinfin    Select XinFin provider.


.. click:: swap.cli.__main__:main
  :prog: swap
  :show-nested: