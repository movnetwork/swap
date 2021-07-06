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


def test_ethereum_cli_htlc(cli_tester):

    htlc = cli_tester.invoke(
        cli_main, [
            "ethereum",
            "htlc",
            "--contract-address", _["ethereum"]["htlc"]["contract_address"],
            "--network", _["ethereum"]["network"]
        ]
    )

    assert htlc.exit_code == 0
    assert htlc.output == str(json.dumps(dict(
        abi=_["ethereum"]["htlc"]["abi"],
        bytecode=_["ethereum"]["htlc"]["bytecode"],
        contract_address=_["ethereum"]["htlc"]["contract_address"]
    ), indent=4)) + "\n"
