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


def test_bitcoin_cli_submit(cli_tester):

    submit = cli_tester.invoke(
        cli_main, [
            "bitcoin",
            "submit",
            "--transaction-raw", _["bitcoin"]["refund"]["unsigned"]["transaction_raw"],
            "--endpoint", "smartbit"
        ]
    )
    assert submit.exit_code == 0
    assert submit.output == "Error: (REQ_ERROR), 16: mandatory-script-verify-flag-failed " \
                            "(Operation not valid with the current stack size)" + "\n" or \
           str(submit.output).startswith("Error: HTTPSConnectionPool")
