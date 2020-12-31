#!/usr/bin/env python3

import json
import os

from swap.cli.__main__ import main as cli_main

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_vapor_cli_submit(cli_tester):

    submit = cli_tester.invoke(
        cli_main, [
            "vapor",
            "submit",
            "--transaction-raw", _["vapor"]["refund"]["unsigned"]["transaction_raw"]
        ]
    )
    assert submit.exit_code == 0
    assert submit.output == "Error: (600), finalize tx fail" + "\n"
