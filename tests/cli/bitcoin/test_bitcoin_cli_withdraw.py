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


def test_bitcoin_cli_withdraw(cli_tester):

    withdraw = cli_tester.invoke(
        cli_main, [
            "bitcoin",
            "withdraw",
            "--address", _["bitcoin"]["wallet"]["recipient"]["address"],
            "--transaction-hash", _["bitcoin"]["transaction_hash"],
            "--version", _["bitcoin"]["version"],
            "--network", _["bitcoin"]["network"]
        ]
    )
    assert withdraw.exit_code == 0
    assert withdraw.output == clean_transaction_raw(
        transaction_raw=_["bitcoin"]["withdraw"]["unsigned"]["transaction_raw"]
    ) + "\n"
