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


def test_bitcoin_cli_claim(cli_tester):

    claim = cli_tester.invoke(
        cli_main, [
            "bitcoin",
            "claim",
            "--address", _["bitcoin"]["wallet"]["recipient"]["address"],
            "--transaction", _["bitcoin"]["transaction_id"],
            "--amount", _["bitcoin"]["amount"],
            "--version", _["bitcoin"]["version"],
            "--network", _["bitcoin"]["network"]
        ]
    )
    assert claim.exit_code == 0
    assert claim.output == clean_transaction_raw(
        transaction_raw=_["bitcoin"]["claim"]["unsigned"]["transaction_raw"]
    ) + "\n"
