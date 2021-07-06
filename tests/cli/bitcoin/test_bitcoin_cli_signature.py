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


def test_bitcoin_cli_signature(cli_tester):

    signed_fund_transaction_raw = cli_tester.invoke(
        cli_main, [
            "bitcoin",
            "sign",
            "--transaction-raw", _["bitcoin"]["fund"]["unsigned"]["transaction_raw"],
            "--xprivate-key", _["bitcoin"]["wallet"]["sender"]["root_xprivate_key"],
            "--account", _["bitcoin"]["wallet"]["sender"]["derivation"]["account"],
            "--change", _["bitcoin"]["wallet"]["sender"]["derivation"]["change"],
            "--address", _["bitcoin"]["wallet"]["sender"]["derivation"]["address"],
            "--path", _["bitcoin"]["wallet"]["sender"]["derivation"]["path"]
        ]
    )

    assert signed_fund_transaction_raw.exit_code == 0
    assert signed_fund_transaction_raw.output == clean_transaction_raw(
        transaction_raw=_["bitcoin"]["fund"]["signed"]["transaction_raw"]
    ) + "\n"

    signed_withdraw_transaction_raw = cli_tester.invoke(
        cli_main, [
            "bitcoin",
            "sign",
            "--transaction-raw", _["bitcoin"]["withdraw"]["unsigned"]["transaction_raw"],
            "--xprivate-key", _["bitcoin"]["wallet"]["recipient"]["root_xprivate_key"],
            "--secret-key", _["bitcoin"]["htlc"]["secret"]["key"],
            "--bytecode", _["bitcoin"]["htlc"]["bytecode"],
            "--account", _["bitcoin"]["wallet"]["recipient"]["derivation"]["account"],
            "--change", _["bitcoin"]["wallet"]["recipient"]["derivation"]["change"],
            "--address", _["bitcoin"]["wallet"]["recipient"]["derivation"]["address"],
            "--path", _["bitcoin"]["wallet"]["recipient"]["derivation"]["path"]
        ]
    )

    assert signed_withdraw_transaction_raw.exit_code == 0
    assert signed_withdraw_transaction_raw.output == clean_transaction_raw(
        transaction_raw=_["bitcoin"]["withdraw"]["signed"]["transaction_raw"]
    ) + "\n"

    signed_refund_transaction_raw = cli_tester.invoke(
        cli_main, [
            "bitcoin",
            "sign",
            "--transaction-raw", _["bitcoin"]["refund"]["unsigned"]["transaction_raw"],
            "--xprivate-key", _["bitcoin"]["wallet"]["sender"]["root_xprivate_key"],
            "--endtime", _["bitcoin"]["htlc"]["endtime"],
            "--bytecode", _["bitcoin"]["htlc"]["bytecode"],
            "--account", _["bitcoin"]["wallet"]["sender"]["derivation"]["account"],
            "--change", _["bitcoin"]["wallet"]["sender"]["derivation"]["change"],
            "--address", _["bitcoin"]["wallet"]["sender"]["derivation"]["address"],
            "--path", _["bitcoin"]["wallet"]["sender"]["derivation"]["path"]
        ]
    )

    assert signed_refund_transaction_raw.exit_code == 0
    assert signed_refund_transaction_raw.output == clean_transaction_raw(
        transaction_raw=_["bitcoin"]["refund"]["signed"]["transaction_raw"]
    ) + "\n"
