#!/usr/bin/env python3

import json
import os

from swap.cli.__main__ import main as cli_main
from swap.providers.xinfin.utils import is_transaction_raw

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_xinfin_cli_refund(cli_tester):

    refund = cli_tester.invoke(
        cli_main, [
            "xinfin",
            "refund",
            "--address", _["xinfin"]["wallet"]["sender"]["address"],
            "--transaction-hash", _["xinfin"]["transaction_hash"],
            "--network", _["xinfin"]["network"]
        ]
    )

    assert refund.exit_code == 0
    assert is_transaction_raw(refund.output)
