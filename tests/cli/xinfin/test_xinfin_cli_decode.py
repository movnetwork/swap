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


def test_xinfin_cli_decode(cli_tester):

    decode = cli_tester.invoke(
        cli_main, [
            "xinfin",
            "decode",
            "--transaction-raw", _["xinfin"]["fund"]["unsigned"]["transaction_raw"],
            "--indent", 0
        ]
    )

    assert decode.exit_code == 0
    assert decode.output != str(json.dumps(dict(
        fee=_["xinfin"]["fund"]["unsigned"]["fee"],
        network=_["xinfin"]["network"],
        transaction=_["xinfin"]["fund"]["unsigned"]["json"],
        type=_["xinfin"]["fund"]["unsigned"]["type"],
    ), indent=4)) + "\n"
