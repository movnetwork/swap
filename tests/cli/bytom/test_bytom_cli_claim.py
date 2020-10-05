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


def test_bytom_cli_claim(cli_tester):

    claim = cli_tester.invoke(
        cli_main, [
            "bytom",
            "claim",
            "--address", _["bytom"]["wallet"]["recipient"]["address"],
            "--transaction", _["bytom"]["transaction_id"],
            "--amount", _["bytom"]["amount"],
            "--network", _["bytom"]["network"]
        ]
    )
    assert claim.exit_code == 0
    assert claim.output == clean_transaction_raw(
        transaction_raw=_["bytom"]["claim"]["unsigned"]["transaction_raw"]
    ) + "\n"
