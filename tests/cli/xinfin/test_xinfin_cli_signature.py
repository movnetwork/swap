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


def test_xinfin_cli_signature(cli_tester):

    signed_fund_transaction_raw = cli_tester.invoke(
        cli_main, [
            "xinfin",
            "sign",
            "--transaction-raw", _["xinfin"]["fund"]["unsigned"]["transaction_raw"],
            "--xprivate-key", _["xinfin"]["wallet"]["sender"]["root_xprivate_key"],
            "--account", _["xinfin"]["wallet"]["sender"]["derivation"]["account"],
            "--change", _["xinfin"]["wallet"]["sender"]["derivation"]["change"],
            "--address", _["xinfin"]["wallet"]["sender"]["derivation"]["address"],
            "--path", _["xinfin"]["wallet"]["sender"]["derivation"]["path"]
        ]
    )

    assert signed_fund_transaction_raw.exit_code == 0
    assert signed_fund_transaction_raw.output == clean_transaction_raw(
        transaction_raw=_["xinfin"]["fund"]["signed"]["transaction_raw"]
    ) + "\n"

    signed_withdraw_transaction_raw = cli_tester.invoke(
        cli_main, [
            "xinfin",
            "sign",
            "--transaction-raw", _["xinfin"]["withdraw"]["unsigned"]["transaction_raw"],
            "--xprivate-key", _["xinfin"]["wallet"]["recipient"]["root_xprivate_key"],
            "--account", _["xinfin"]["wallet"]["recipient"]["derivation"]["account"],
            "--change", _["xinfin"]["wallet"]["recipient"]["derivation"]["change"],
            "--address", _["xinfin"]["wallet"]["recipient"]["derivation"]["address"],
            "--path", _["xinfin"]["wallet"]["recipient"]["derivation"]["path"]
        ]
    )

    assert signed_withdraw_transaction_raw.exit_code == 0
    assert signed_withdraw_transaction_raw.output == clean_transaction_raw(
        transaction_raw=_["xinfin"]["withdraw"]["signed"]["transaction_raw"]
    ) + "\n"

    signed_refund_transaction_raw = cli_tester.invoke(
        cli_main, [
            "xinfin",
            "sign",
            "--transaction-raw", _["xinfin"]["refund"]["unsigned"]["transaction_raw"],
            "--xprivate-key", _["xinfin"]["wallet"]["sender"]["root_xprivate_key"],
            "--account", _["xinfin"]["wallet"]["sender"]["derivation"]["account"],
            "--change", _["xinfin"]["wallet"]["sender"]["derivation"]["change"],
            "--address", _["xinfin"]["wallet"]["sender"]["derivation"]["address"],
            "--path", _["xinfin"]["wallet"]["sender"]["derivation"]["path"]
        ]
    )

    assert signed_refund_transaction_raw.exit_code == 0
    assert signed_refund_transaction_raw.output == clean_transaction_raw(
        transaction_raw=_["xinfin"]["refund"]["signed"]["transaction_raw"]
    ) + "\n"
