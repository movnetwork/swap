#!/usr/bin/env python3

from shuttle.providers.bitcoin.wallet import Wallet
from shuttle.cli.__main__ import main as cli_main


version = 2
network = "testnet"
sender_wallet = Wallet(network=network).from_passphrase("meheret tesfaye batu bayou")
recipient_wallet = Wallet(network=network).from_passphrase("meheret")
htlc_bytecode = "63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a91498f8" \
                "79fb7f8b4951dee9bc8a0327b792fbe332b888ac6702e803b27576a91464a8390b0b1685fcbf2d4b45" \
                "7118dc8da92d553488ac68"
amount = 10_000


def test_bitcoin_cli_fund(cli_tester):

    fund = cli_tester.invoke(
        cli_main, [
            "bitcoin",
            "fund",
            "--sender-address", sender_wallet.address(),
            "--amount", amount,
            "--bytecode", htlc_bytecode,
            "--version", version,
            "--network", network
        ]
    )
    assert fund.exit_code == 0
    assert fund.output == "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMWVjMzEyZTkyZDgzODdiMTVmNjIzOGQ0" \
                          "OTE4MzQ0YjYyYWIxNDdkN2YzODQ0ZGM4MWU2NTM3NzZmZThiODRlZjMwMTAwMDAwMDAwZmZm" \
                          "ZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQyYmIwMTNjM2U0YmViMDg0MjFkZWRjZjgx" \
                          "NWNiNjVhNWMzODgxNzhiODc1MDhhMGUwMDAwMDAwMDAwMTk3NmE5MTQ2NGE4MzkwYjBiMTY4" \
                          "NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBb" \
                          "eyJhbW91bnQiOiA5NjM1OTAsICJuIjogMSwgInNjcmlwdCI6ICI3NmE5MTQ2NGE4MzkwYjBi" \
                          "MTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVz" \
                          "dG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9" + "\n"

    fund = cli_tester.invoke(
        cli_main, [
            "bitcoin",
            "fund",
            "--sender-address", "L5tUq6mCbE84XobZ1mphBPZf15cRFcvg7Q",
            "--amount", amount,
            "--bytecode", htlc_bytecode,
            "--version", version,
            "--network", network
        ]
    )
    assert fund.exit_code == 0
    assert fund.output == "Error: invalid testnet L5tUq6mCbE84XobZ1mphBPZf15cRFcvg7Q address" + "\n"
