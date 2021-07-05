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


def test_bytom_cli_signature(cli_tester):

    signed_fund_transaction_raw = cli_tester.invoke(
        cli_main, [
            "bytom",
            "sign",
            "--transaction-raw", _["bytom"]["fund"]["unsigned"]["transaction_raw"],
            "--xprivate-key", _["bytom"]["wallet"]["sender"]["xprivate_key"],
            "--account", _["bytom"]["wallet"]["sender"]["derivation"]["account"],
            "--change", _["bytom"]["wallet"]["sender"]["derivation"]["change"],
            "--address", _["bytom"]["wallet"]["sender"]["derivation"]["address"],
            "--path", _["bytom"]["wallet"]["sender"]["derivation"]["path"]
        ]
    )

    assert signed_fund_transaction_raw.exit_code == 0
    assert signed_fund_transaction_raw.output == clean_transaction_raw(
        transaction_raw=_["bytom"]["fund"]["signed"]["transaction_raw"]
    ) + "\n"

    signed_withdraw_transaction_raw = cli_tester.invoke(
        cli_main, [
            "bytom",
            "sign",
            "--transaction-raw", _["bytom"]["withdraw"]["unsigned"]["transaction_raw"],
            "--xprivate-key", _["bytom"]["wallet"]["recipient"]["xprivate_key"],
            "--secret-key", _["bytom"]["htlc"]["secret"]["key"],
            "--bytecode", _["bytom"]["htlc"]["bytecode"],
            "--account", _["bytom"]["wallet"]["recipient"]["derivation"]["account"],
            "--change", _["bytom"]["wallet"]["recipient"]["derivation"]["change"],
            "--address", _["bytom"]["wallet"]["recipient"]["derivation"]["address"],
            "--path", _["bytom"]["wallet"]["recipient"]["derivation"]["path"]
        ]
    )

    assert signed_withdraw_transaction_raw.exit_code == 0
    assert signed_withdraw_transaction_raw.output == clean_transaction_raw(
        transaction_raw=_["bytom"]["withdraw"]["signed"]["transaction_raw"]
    ) + "\n"

    signed_refund_transaction_raw = cli_tester.invoke(
        cli_main, [
            "bytom",
            "sign",
            "--transaction-raw", _["bytom"]["refund"]["unsigned"]["transaction_raw"],
            "--xprivate-key", _["bytom"]["wallet"]["sender"]["xprivate_key"],
            "--bytecode", _["bytom"]["htlc"]["bytecode"],
            "--account", _["bytom"]["wallet"]["sender"]["derivation"]["account"],
            "--change", _["bytom"]["wallet"]["sender"]["derivation"]["change"],
            "--address", _["bytom"]["wallet"]["sender"]["derivation"]["address"],
            "--path", _["bytom"]["wallet"]["sender"]["derivation"]["path"]
        ]
    )

    assert signed_refund_transaction_raw.exit_code == 0
    assert signed_refund_transaction_raw.output == clean_transaction_raw(
        transaction_raw=_["bytom"]["refund"]["signed"]["transaction_raw"]
    ) + "\n"
