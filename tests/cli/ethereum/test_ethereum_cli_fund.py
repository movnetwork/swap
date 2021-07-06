#!/usr/bin/env python3

import json
import os

from swap.cli.__main__ import main as cli_main
from swap.providers.ethereum.utils import is_transaction_raw
from swap.utils import get_current_timestamp

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_ethereum_cli_fund(cli_tester):

    fund = cli_tester.invoke(
        cli_main, [
            "ethereum",
            "fund",
            "--secret-hash", _["ethereum"]["htlc"]["secret"]["hash"],
            "--recipient-address", _["ethereum"]["wallet"]["recipient"]["address"],
            "--sender-address", _["ethereum"]["wallet"]["sender"]["address"],
            "--endtime", get_current_timestamp(plus=3600),
            "--amount", _["ethereum"]["amount"],
            "--unit", _["ethereum"]["unit"],
            "--network", _["ethereum"]["network"]
        ]
    )
    assert fund.exit_code == 0
    assert is_transaction_raw(fund.output)
