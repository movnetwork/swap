#!/usr/bin/env python3

from swap.providers.bytom.wallet import Wallet
from swap.cli.__main__ import main as cli_main
from swap.utils import transaction_raw_cleaner

import json
import os

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
_ = open(file_path, "r")
TEST_VALUES = json.loads(_.read())
_.close()

network: str = TEST_VALUES["bytom"]["network"]
sender_wallet: Wallet = Wallet(network=network).from_mnemonic(
    mnemonic=TEST_VALUES["bytom"]["wallet"]["sender"]["mnemonic"],
    passphrase=TEST_VALUES["bytom"]["wallet"]["recipient"]["passphrase"]
).from_path(
    path=TEST_VALUES["bytom"]["wallet"]["sender"]["path"]
)
recipient_wallet: Wallet = Wallet(network=network).from_mnemonic(
    mnemonic=TEST_VALUES["bytom"]["wallet"]["recipient"]["mnemonic"],
    passphrase=TEST_VALUES["bytom"]["wallet"]["recipient"]["passphrase"]
).from_path(
    path=TEST_VALUES["bytom"]["wallet"]["recipient"]["path"]
)
transaction_id = TEST_VALUES["bytom"]["transaction_id"]
asset = TEST_VALUES["bytom"]["asset"]
amount = TEST_VALUES["bytom"]["amount"]


def test_bytom_cli_refund(cli_tester):

    refund = cli_tester.invoke(
        cli_main, [
            "bytom",
            "refund",
            "--transaction", transaction_id,
            "--address", sender_wallet.address(),
            "--amount", amount,
            "--asset", asset,
            "--network", network
        ]
    )
    assert refund.exit_code == 0
    assert refund.output == transaction_raw_cleaner(
        raw=TEST_VALUES["bytom"]["refund"]["unsigned"]["unsigned_raw"]
    ) + "\n"

    refund = cli_tester.invoke(
        cli_main, [
            "bytom",
            "refund",
            "--transaction", transaction_id,
            "--address", 634653654354,
            "--amount", amount,
            "--asset", asset,
            "--network", network
        ]
    )
    assert refund.exit_code == 0
    assert refund.output == "Error: address must be string format" + "\n"

    refund = cli_tester.invoke(
        cli_main, [
            "bytom",
            "refund",
            "--transaction", transaction_id,
            "--address", str(),
            "--amount", amount,
            "--asset", asset,
            "--network", network
        ]
    )
    assert refund.exit_code == 0
    assert refund.output == "Error: Invalid '' mainnet address/type" + "\n"
