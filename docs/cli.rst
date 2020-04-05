============================
Command Line Interface (CLI)
============================

After you have installed, type ``shuttle`` to verify that it worked:

::

    $ shuttle
    Usage: shuttle [OPTIONS] COMMAND [ARGS]...

    Options:
      -v, --version  Show Shuttle version and exit.
      -h, --help     Show this message and exit.

    Commands:
      bitcoin  Select Bitcoin provider.
      bytom    Select Bytom provider.


.. click:: shuttle.cli.__main__:main
  :prog: shuttle
  :show-nested: