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


def test_xinfin_cli_xrc20_htlc(cli_tester):

    xrc20_htlc = cli_tester.invoke(
        cli_main, [
            "xinfin",
            "htlc",
            "--contract-address", _["xinfin"]["xrc20_htlc"]["contract_address"],
            "--network", _["xinfin"]["network"],
            "--xrc20", True
        ]
    )

    assert xrc20_htlc.exit_code == 0
    assert xrc20_htlc.output == str(json.dumps(dict(
        abi=_["xinfin"]["xrc20_htlc"]["abi"],
        bytecode=_["xinfin"]["xrc20_htlc"]["bytecode"],
        bytecode_runtime=_["xinfin"]["xrc20_htlc"]["bytecode_runtime"],
        contract_address=_["xinfin"]["xrc20_htlc"]["contract_address"]
    ), indent=4)) + "\n"
