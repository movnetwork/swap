#!/usr/bin/env python3

import json
import os

from swap.cli.__main__ import main as cli_main
from swap.utils import clean_transaction_raw

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_bytom_cli_withdraw(cli_tester):

    withdraw = cli_tester.invoke(
        cli_main, [
            "bytom",
            "withdraw",
            "--address", _["bytom"]["wallet"]["recipient"]["address"],
            "--transaction-hash", _["bytom"]["transaction_hash"],
            "--asset", _["bytom"]["asset"],
            "--network", _["bytom"]["network"]
        ]
    )
    assert withdraw.exit_code == 0
    assert withdraw.output == clean_transaction_raw(
        transaction_raw=_["bytom"]["withdraw"]["unsigned"]["transaction_raw"]
    ) + "\n"
