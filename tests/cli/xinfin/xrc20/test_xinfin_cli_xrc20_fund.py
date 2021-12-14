#!/usr/bin/env python3

import json
import os

from swap.cli.__main__ import main as cli_main
from swap.providers.xinfin.utils import is_transaction_raw
from swap.utils import get_current_timestamp

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_xinfin_cli_xrc20_fund(cli_tester):

    xrc20_fund = cli_tester.invoke(
        cli_main, [
            "xinfin",
            "fund",
            "--secret-hash", _["xinfin"]["xrc20_htlc"]["secret"]["hash"],
            "--recipient-address", _["xinfin"]["wallet"]["recipient"]["address"],
            "--sender-address", _["xinfin"]["wallet"]["sender"]["address"],
            "--endtime", get_current_timestamp(plus=3600),
            "--amount", _["xinfin"]["xrc20_amount"],
            "--network", _["xinfin"]["network"],
            "--token-address", _["xinfin"]["xrc20_htlc"]["agreements"]["token_address"],
            "--xrc20", True
        ]
    )
    assert xrc20_fund.exit_code == 0
    assert is_transaction_raw(xrc20_fund.output)
