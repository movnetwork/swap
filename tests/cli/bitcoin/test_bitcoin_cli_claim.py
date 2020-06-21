#!/usr/bin/env python3

from shuttle.providers.bitcoin.wallet import Wallet
from shuttle.cli.__main__ import main as cli_main


version = 2
network = "testnet"
sender_wallet = Wallet(network=network).from_passphrase("meheret tesfaye batu bayou")
recipient_wallet = Wallet(network=network).from_passphrase("meheret")
transaction_id = "f34eb8e86f7753e681dc44387f7d14ab624b3418498d23f6157b38d8922e31ec"
amount = 10_000


def test_bitcoin_cli_claim(cli_tester):

    claim = cli_tester.invoke(
        cli_main, [
            "bitcoin",
            "claim",
            "--transaction", transaction_id,
            "--recipient-address", recipient_wallet.address(),
            "--amount", amount,
            "--version", version,
            "--network", network
        ]
    )
    assert claim.exit_code == 0
    assert claim.output == "eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMWVjMzEyZTkyZDgzODdiMTVmNjIzOGQ0OTE" \
                           "4MzQ0YjYyYWIxNDdkN2YzODQ0ZGM4MWU2NTM3NzZmZThiODRlZjMwMDAwMDAwMDAwZmZmZmZmZm" \
                           "YwMWQwMjQwMDAwMDAwMDAwMDAxOTc2YTkxNDk4Zjg3OWZiN2Y4YjQ5NTFkZWU5YmM4YTAzMjdiN" \
                           "zkyZmJlMzMyYjg4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsiYW1vdW50IjogMTAwMDAsICJu" \
                           "IjogMCwgInNjcmlwdCI6ICJhOTE0MmJiMDEzYzNlNGJlYjA4NDIxZGVkY2Y4MTVjYjY1YTVjMzg" \
                           "4MTc4Yjg3In0sICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX2NsYWltX3" \
                           "Vuc2lnbmVkIn0=" + "\n"

    claim = cli_tester.invoke(
        cli_main, [
            "bitcoin",
            "claim",
            "--transaction", transaction_id,
            "--recipient-address", "L5tUq6mCbE84XobZ1mphBPZf15cRFcvg7Q",
            "--amount", amount,
            "--version", version,
            "--network", network
        ]
    )
    assert claim.exit_code == 0
    assert claim.output == "Error: invalid testnet L5tUq6mCbE84XobZ1mphBPZf15cRFcvg7Q address" + "\n"
