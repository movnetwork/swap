#!/usr/bin/env python3

import json
import os

from swap.cli.__main__ import main as cli_main
from swap.providers.ethereum.utils import is_transaction_raw

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_ethereum_cli_erc20_refund(cli_tester):

    erc20_refund = cli_tester.invoke(
        cli_main, [
            "ethereum",
            "refund",
            "--address", _["ethereum"]["wallet"]["sender"]["address"],
            "--transaction-hash", _["ethereum"]["erc20_transaction_hash"],
            "--network", _["ethereum"]["network"],
            "--erc20", True
        ]
    )

    assert erc20_refund.exit_code == 0
    assert is_transaction_raw(erc20_refund.output)
