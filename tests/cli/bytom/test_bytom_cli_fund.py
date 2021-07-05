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


def test_bytom_cli_fund(cli_tester):

    fund = cli_tester.invoke(
        cli_main, [
            "bytom",
            "fund",
            "--address", _["bytom"]["wallet"]["sender"]["address"],
            "--contract-address", _["bytom"]["htlc"]["contract_address"],
            "--asset", _["bytom"]["asset"],
            "--amount", _["bytom"]["amount"],
            "--unit", _["bytom"]["unit"],
            "--network", _["bytom"]["network"]
        ]
    )
    assert fund.exit_code == 0
    assert fund.output == clean_transaction_raw(
        transaction_raw=_["bytom"]["fund"]["unsigned"]["transaction_raw"]
    ) + "\n"
