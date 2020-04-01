#!/usr/bin/env python3
# coding=utf-8


from shuttle.cli import __main__ as cli_main
from shuttle import __version__


def test_shuttle_cli(cli_tester):
    assert cli_tester.invoke(cli_main.shuttle).exit_code == 0
    version = cli_tester.invoke(cli_main.shuttle, ["--version"])
    assert version.exit_code == 0
    assert version.output == "PyShuttle version " + __version__ + "\n"
