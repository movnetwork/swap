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


def test_bytom_cli_decode(cli_tester):

    decode = cli_tester.invoke(
        cli_main, [
            "bytom",
            "decode",
            "--transaction-raw", _["bytom"]["fund"]["unsigned"]["transaction_raw"],
            "--indent", 0
        ]
    )

    assert decode.exit_code == 0
    assert decode.output != str({
        "address": _["bytom"]["wallet"]["sender"]["address"],
        "fee": 10000000,
        "network": _["bytom"]["network"],
        "signatures": [],
        "tx": _["bytom"]["fund"]["unsigned"]["json"],
        "type": "bytom_fund_unsigned",
        "unsigned_datas": _["bytom"]["fund"]["unsigned"]["unsigned_datas"]
    }) + "\n"
