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


def test_bytom_cli_htlc(cli_tester):

    htlc = cli_tester.invoke(
        cli_main, [
            "bytom",
            "htlc",
            "--secret-hash", _["bytom"]["htlc"]["secret"]["hash"],
            "--recipient-public-key", _["bytom"]["wallet"]["recipient"]["public_key"],
            "--sender-public-key", _["bytom"]["wallet"]["sender"]["public_key"],
            "--endblock", _["bytom"]["htlc"]["endblock"],
            "--network", _["bytom"]["network"]
        ]
    )

    assert htlc.exit_code == 0
    assert htlc.output == str(json.dumps(dict(
        **_["bytom"]["htlc"]["agreements"],
        bytecode=_["bytom"]["htlc"]["bytecode"],
        contract_address=_["bytom"]["htlc"]["contract_address"]
    ), indent=4)) + "\n"
