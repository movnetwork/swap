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


def test_ethereum_cli_signature(cli_tester):

    signed_fund_transaction_raw = cli_tester.invoke(
        cli_main, [
            "ethereum",
            "sign",
            "--transaction-raw", _["ethereum"]["fund"]["unsigned"]["transaction_raw"],
            "--xprivate-key", _["ethereum"]["wallet"]["sender"]["root_xprivate_key"],
            "--account", _["ethereum"]["wallet"]["sender"]["derivation"]["account"],
            "--change", _["ethereum"]["wallet"]["sender"]["derivation"]["change"],
            "--address", _["ethereum"]["wallet"]["sender"]["derivation"]["address"],
            "--path", _["ethereum"]["wallet"]["sender"]["derivation"]["path"]
        ]
    )

    assert signed_fund_transaction_raw.exit_code == 0
    assert signed_fund_transaction_raw.output == clean_transaction_raw(
        transaction_raw=_["ethereum"]["fund"]["signed"]["transaction_raw"]
    ) + "\n"

    signed_withdraw_transaction_raw = cli_tester.invoke(
        cli_main, [
            "ethereum",
            "sign",
            "--transaction-raw", _["ethereum"]["withdraw"]["unsigned"]["transaction_raw"],
            "--xprivate-key", _["ethereum"]["wallet"]["recipient"]["root_xprivate_key"],
            "--account", _["ethereum"]["wallet"]["recipient"]["derivation"]["account"],
            "--change", _["ethereum"]["wallet"]["recipient"]["derivation"]["change"],
            "--address", _["ethereum"]["wallet"]["recipient"]["derivation"]["address"],
            "--path", _["ethereum"]["wallet"]["recipient"]["derivation"]["path"]
        ]
    )

    assert signed_withdraw_transaction_raw.exit_code == 0
    assert signed_withdraw_transaction_raw.output == clean_transaction_raw(
        transaction_raw=_["ethereum"]["withdraw"]["signed"]["transaction_raw"]
    ) + "\n"

    signed_refund_transaction_raw = cli_tester.invoke(
        cli_main, [
            "ethereum",
            "sign",
            "--transaction-raw", _["ethereum"]["refund"]["unsigned"]["transaction_raw"],
            "--xprivate-key", _["ethereum"]["wallet"]["sender"]["root_xprivate_key"],
            "--account", _["ethereum"]["wallet"]["sender"]["derivation"]["account"],
            "--change", _["ethereum"]["wallet"]["sender"]["derivation"]["change"],
            "--address", _["ethereum"]["wallet"]["sender"]["derivation"]["address"],
            "--path", _["ethereum"]["wallet"]["sender"]["derivation"]["path"]
        ]
    )

    assert signed_refund_transaction_raw.exit_code == 0
    assert signed_refund_transaction_raw.output == clean_transaction_raw(
        transaction_raw=_["ethereum"]["refund"]["signed"]["transaction_raw"]
    ) + "\n"
