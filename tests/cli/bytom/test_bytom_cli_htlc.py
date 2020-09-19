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


def test_bytom_cli_htlc(cli_tester):

    htlc = cli_tester.invoke(
        cli_main, [
            "bytom",
            "htlc",
            "--secret-hash", TEST_VALUES["bytom"]["htlc"]["secret"]["hash"],
            "--recipient-public", recipient_wallet.public_key(),
            "--sender-public", sender_wallet.public_key(),
            "--sequence", TEST_VALUES["bytom"]["htlc"]["sequence"],
            "--network", network
        ]
    )
    assert htlc.exit_code == 0
    assert htlc.output == "02e803203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e2091ff7f525" \
                          "ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2203a26da82ead15a80533a026966" \
                          "56b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000" \
                          "000537acd9f6972ae7cac00c0" + "\n"

    htlc = cli_tester.invoke(
        cli_main, [
            "bytom",
            "htlc",
            "--secret-hash", TEST_VALUES["bytom"]["htlc"]["secret"]["hash"],
            "--recipient-public", "L5tUq6mCbE84XobZ1mphBPZf15cRFcvg7Q",
            "--sender-public", sender_wallet.public_key(),
            "--sequence", TEST_VALUES["bytom"]["htlc"]["sequence"],
            "--network", network
        ]
    )
    assert htlc.exit_code == 0
    assert htlc.output == "Error: invalid recipient public key, length must be 64" + "\n"
