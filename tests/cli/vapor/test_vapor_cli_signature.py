#!/usr/bin/env python3

import json
import os

from swap.cli.__main__ import main as cli_main
from swap.utils import clean_transaction_raw

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_vapor_cli_signature(cli_tester):

    signed_fund_transaction_raw = cli_tester.invoke(
        cli_main, [
            "vapor",
            "sign",
            "--transaction-raw", _["vapor"]["fund"]["unsigned"]["transaction_raw"],
            "--xprivate-key", _["vapor"]["wallet"]["sender"]["xprivate_key"],
            "--account", _["vapor"]["wallet"]["sender"]["derivation"]["account"],
            "--change", _["vapor"]["wallet"]["sender"]["derivation"]["change"],
            "--address", _["vapor"]["wallet"]["sender"]["derivation"]["address"],
            "--path", _["vapor"]["wallet"]["sender"]["derivation"]["path"]
        ]
    )

    assert signed_fund_transaction_raw.exit_code == 0
    assert signed_fund_transaction_raw.output == clean_transaction_raw(
        transaction_raw=_["vapor"]["fund"]["signed"]["transaction_raw"]
    ) + "\n"

    signed_withdraw_transaction_raw = cli_tester.invoke(
        cli_main, [
            "vapor",
            "sign",
            "--transaction-raw", _["vapor"]["withdraw"]["unsigned"]["transaction_raw"],
            "--xprivate-key", _["vapor"]["wallet"]["recipient"]["xprivate_key"],
            "--secret-key", _["vapor"]["htlc"]["secret"]["key"],
            "--bytecode", _["vapor"]["htlc"]["bytecode"],
            "--account", _["vapor"]["wallet"]["recipient"]["derivation"]["account"],
            "--change", _["vapor"]["wallet"]["recipient"]["derivation"]["change"],
            "--address", _["vapor"]["wallet"]["recipient"]["derivation"]["address"],
            "--path", _["vapor"]["wallet"]["recipient"]["derivation"]["path"]
        ]
    )

    assert signed_withdraw_transaction_raw.exit_code == 0
    assert signed_withdraw_transaction_raw.output == clean_transaction_raw(
        transaction_raw=_["vapor"]["withdraw"]["signed"]["transaction_raw"]
    ) + "\n"

    signed_refund_transaction_raw = cli_tester.invoke(
        cli_main, [
            "vapor",
            "sign",
            "--transaction-raw", _["vapor"]["refund"]["unsigned"]["transaction_raw"],
            "--xprivate-key", _["vapor"]["wallet"]["sender"]["xprivate_key"],
            "--bytecode", _["vapor"]["htlc"]["bytecode"],
            "--account", _["vapor"]["wallet"]["sender"]["derivation"]["account"],
            "--change", _["vapor"]["wallet"]["sender"]["derivation"]["change"],
            "--address", _["vapor"]["wallet"]["sender"]["derivation"]["address"],
            "--path", _["vapor"]["wallet"]["sender"]["derivation"]["path"]
        ]
    )

    assert signed_refund_transaction_raw.exit_code == 0
    assert signed_refund_transaction_raw.output == clean_transaction_raw(
        transaction_raw=_["vapor"]["refund"]["signed"]["transaction_raw"]
    ) + "\n"
