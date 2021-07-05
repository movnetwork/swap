#!/usr/bin/env python3
# coding=utf-8


from swap.cli.__main__ import main as cli_main
from swap import __version__


def test_swap_cli(cli_tester):

    assert cli_tester.invoke(cli_main).exit_code == 0

    assert cli_tester.invoke(cli_main, ["bitcoin"]).exit_code == 0
    assert cli_tester.invoke(cli_main, ["bytom"]).exit_code == 0
    assert cli_tester.invoke(cli_main, ["ethereum"]).exit_code == 0
    assert cli_tester.invoke(cli_main, ["vapor"]).exit_code == 0
    assert cli_tester.invoke(cli_main, ["xinfin"]).exit_code == 0

    version = cli_tester.invoke(cli_main, ["--version"])
    assert version.exit_code == 0
    assert version.output == "v%s\n" % __version__
