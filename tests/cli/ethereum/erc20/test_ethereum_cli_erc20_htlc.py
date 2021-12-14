#!/usr/bin/env python3

import json
import os

from swap.cli.__main__ import main as cli_main

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_ethereum_cli_erc20_htlc(cli_tester):

    erc20_htlc = cli_tester.invoke(
        cli_main, [
            "ethereum",
            "htlc",
            "--contract-address", _["ethereum"]["erc20_htlc"]["contract_address"],
            "--network", _["ethereum"]["network"],
            "--erc20", True
        ]
    )

    assert erc20_htlc.exit_code == 0
    assert erc20_htlc.output == str(json.dumps(dict(
        abi=_["ethereum"]["erc20_htlc"]["abi"],
        bytecode=_["ethereum"]["erc20_htlc"]["bytecode"],
        bytecode_runtime=_["ethereum"]["erc20_htlc"]["bytecode_runtime"],
        contract_address=_["ethereum"]["erc20_htlc"]["contract_address"]
    ), indent=4)) + "\n"
