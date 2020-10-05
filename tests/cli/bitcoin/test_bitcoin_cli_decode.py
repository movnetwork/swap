#!/usr/bin/env python3

import json
import os

from swap.cli.__main__ import main as cli_main

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_bitcoin_cli_decode(cli_tester):

    decode = cli_tester.invoke(
        cli_main, [
            "bitcoin",
            "decode",
            "--raw", _["bitcoin"]["fund"]["unsigned"]["transaction_raw"],
            "--indent", 0
        ]
    )

    assert decode.exit_code == 0
    assert decode.output != str({
        "fee": 678,
        "type": 'bitcoin_fund_unsigned',
        "tx": _["bitcoin"]["fund"]["unsigned"]["json"],
        "network": _["bitcoin"]["network"]
    }) + "\n"
