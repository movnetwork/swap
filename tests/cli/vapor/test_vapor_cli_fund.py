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


def test_vapor_cli_fund(cli_tester):

    fund = cli_tester.invoke(
        cli_main, [
            "vapor",
            "fund",
            "--address", _["vapor"]["wallet"]["sender"]["address"],
            "--contract-address", _["vapor"]["htlc"]["contract_address"],
            "--asset", _["vapor"]["asset"],
            "--amount", _["vapor"]["amount"],
            "--unit", _["vapor"]["unit"],
            "--network", _["vapor"]["network"]
        ]
    )
    assert fund.exit_code == 0
    assert fund.output == clean_transaction_raw(
        transaction_raw=_["vapor"]["fund"]["unsigned"]["transaction_raw"]
    ) + "\n"
