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


def test_bitcoin_cli_htlc(cli_tester):

    htlc = cli_tester.invoke(
        cli_main, [
            "bitcoin",
            "htlc",
            "--secret-hash", _["bitcoin"]["htlc"]["secret"]["hash"],
            "--recipient-address", _["bitcoin"]["wallet"]["recipient"]["address"],
            "--sender-address", _["bitcoin"]["wallet"]["sender"]["address"],
            "--endtime", _["bitcoin"]["htlc"]["endtime"],
            "--network", _["bitcoin"]["network"]
        ]
    )

    assert htlc.exit_code == 0
    # assert htlc.output != str(json.dumps(dict(
    #     **_["bitcoin"]["htlc"]["agreements"],
    #     bytecode=_["bitcoin"]["htlc"]["bytecode"],
    #     contract_address=_["bitcoin"]["htlc"]["contract_address"]
    # ), indent=4)) + "\n"
