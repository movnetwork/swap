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


def test_vapor_cli_decode(cli_tester):

    decode = cli_tester.invoke(
        cli_main, [
            "vapor",
            "decode",
            "--transaction-raw", _["vapor"]["fund"]["unsigned"]["transaction_raw"],
            "--indent", 0
        ]
    )

    assert decode.exit_code == 0
    assert decode.output != str(json.dumps(dict(
        bytecode=_["vapor"]["wallet"]["sender"]["address"],
        fee=_["vapor"]["fund"]["unsigned"]["fee"],
        network=_["vapor"]["network"],
        signatures=[],
        tx=_["vapor"]["fund"]["unsigned"]["json"],
        type=_["vapor"]["fund"]["unsigned"]["type"],
        unsigned_datas=_["vapor"]["fund"]["unsigned"]["unsigned_datas"],
    ), indent=4)) + "\n"
