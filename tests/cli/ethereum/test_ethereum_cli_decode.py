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


def test_ethereum_cli_decode(cli_tester):

    decode = cli_tester.invoke(
        cli_main, [
            "ethereum",
            "decode",
            "--transaction-raw", _["ethereum"]["fund"]["unsigned"]["transaction_raw"],
            "--indent", 0
        ]
    )

    assert decode.exit_code == 0
    assert decode.output != str(json.dumps(dict(
        fee=_["ethereum"]["fund"]["unsigned"]["fee"],
        network=_["ethereum"]["network"],
        transaction=_["ethereum"]["fund"]["unsigned"]["json"],
        type=_["ethereum"]["fund"]["unsigned"]["type"],
    ), indent=4)) + "\n"
