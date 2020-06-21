#!/usr/bin/env python3

from shuttle.providers.bitcoin.wallet import Wallet
from shuttle.cli.__main__ import main as cli_main


version = 2
network = "testnet"
sender_wallet = Wallet(network=network).from_passphrase("meheret tesfaye batu bayou")
recipient_wallet = Wallet(network=network).from_passphrase("meheret")
transaction_id = "f34eb8e86f7753e681dc44387f7d14ab624b3418498d23f6157b38d8922e31ec"
amount = 10_000


def test_bitcoin_cli_refund(cli_tester):

    refund = cli_tester.invoke(
        cli_main, [
            "bitcoin",
            "refund",
            "--transaction", transaction_id,
            "--sender-address", sender_wallet.address(),
            "--amount", amount,
            "--version", version,
            "--network", network
        ]
    )
    assert refund.exit_code == 0
    assert refund.output == "eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMWVjMzEyZTkyZDgzODdiMTVmNjIzOGQ0OT" \
                           "E4MzQ0YjYyYWIxNDdkN2YzODQ0ZGM4MWU2NTM3NzZmZThiODRlZjMwMDAwMDAwMDAwZmZmZmZm" \
                           "ZmYwMWQwMjQwMDAwMDAwMDAwMDAxOTc2YTkxNDY0YTgzOTBiMGIxNjg1ZmNiZjJkNGI0NTcxMT" \
                           "hkYzhkYTkyZDU1MzQ4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsidmFsdWUiOiAxMDAwMCwg" \
                           "Im4iOiAwLCAic2NyaXB0X3B1YmtleSI6ICJhOTE0MmJiMDEzYzNlNGJlYjA4NDIxZGVkY2Y4MT" \
                           "VjYjY1YTVjMzg4MTc4Yjg3In0sICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRj" \
                           "b2luX3JlZnVuZF91bnNpZ25lZCJ9" + "\n"

    refund = cli_tester.invoke(
        cli_main, [
            "bitcoin",
            "refund",
            "--transaction", transaction_id,
            "--sender-address", "L5tUq6mCbE84XobZ1mphBPZf15cRFcvg7Q",
            "--amount", amount,
            "--version", version,
            "--network", network
        ]
    )

    assert refund.exit_code == 0
    assert refund.output == "Error: invalid testnet L5tUq6mCbE84XobZ1mphBPZf15cRFcvg7Q address" + "\n"
