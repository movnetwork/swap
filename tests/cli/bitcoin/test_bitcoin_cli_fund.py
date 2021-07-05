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


def test_bitcoin_cli_fund(cli_tester):

    fund = cli_tester.invoke(
        cli_main, [
            "bitcoin",
            "fund",
            "--address", _["bitcoin"]["wallet"]["sender"]["address"],
            "--contract-address", _["bitcoin"]["htlc"]["contract_address"],
            "--amount", _["bitcoin"]["amount"],
            "--unit", _["bitcoin"]["unit"],
            "--version", _["bitcoin"]["version"],
            "--network", _["bitcoin"]["network"]
        ]
    )
    assert fund.exit_code == 0
    assert fund.output == clean_transaction_raw(
        transaction_raw=_["bitcoin"]["fund"]["unsigned"]["transaction_raw"]
    ) + "\n"
