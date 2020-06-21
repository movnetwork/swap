#!/usr/bin/env python3

from shuttle.providers.bitcoin.wallet import Wallet
from shuttle.cli.__main__ import main as cli_main


version = 2
network = "testnet"
sender_wallet = Wallet(network=network).from_passphrase("meheret tesfaye batu bayou")
recipient_wallet = Wallet(network=network).from_passphrase("meheret")
unsigned_transaction_raw = "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMWVjMzEyZTkyZDgzODdiMTVmNjIzOGQ0" \
                           "OTE4MzQ0YjYyYWIxNDdkN2YzODQ0ZGM4MWU2NTM3NzZmZThiODRlZjMwMTAwMDAwMDAwZmZm" \
                           "ZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQyYmIwMTNjM2U0YmViMDg0MjFkZWRjZjgx" \
                           "NWNiNjVhNWMzODgxNzhiODc1MDhhMGUwMDAwMDAwMDAwMTk3NmE5MTQ2NGE4MzkwYjBiMTY4" \
                           "NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBb" \
                           "eyJhbW91bnQiOiA5NjM1OTAsICJuIjogMSwgInNjcmlwdCI6ICI3NmE5MTQ2NGE4MzkwYjBi" \
                           "MTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVz" \
                           "dG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"


def test_bitcoin_cli_decode(cli_tester):

    decode = cli_tester.invoke(
        cli_main, [
            "bitcoin",
            "decode",
            "--raw", unsigned_transaction_raw
        ]
    )
    assert decode.exit_code == 0
    assert decode.output != {
        "fee": 576,
        "type": "bitcoin_refund_unsigned",
        "tx": {
            "hex": "0200000001ec312e92d8387b15f6238d4918344b62ab147d7f3844dc81e653776fe8b84ef30000000000ffff"
                   "ffff01d0240000000000001976a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac00000000",
            "txid": "a2022290e62f4073bc642d6b45f92ec3686c6524d0ef3d67d9edfd5f7dab0ea1",
            "hash": "a2022290e62f4073bc642d6b45f92ec3686c6524d0ef3d67d9edfd5f7dab0ea1",
            "size": 85,
            "vsize": 85,
            "version": 2,
            "locktime": 0,
            "vin": [
                {
                    "txid": "f34eb8e86f7753e681dc44387f7d14ab624b3418498d23f6157b38d8922e31ec",
                    "vout": 0,
                    "scriptSig": {
                        "asm": "",
                        "hex": ""
                    },
                    "sequence": "4294967295"
                }
            ],
            "vout": [
                {
                    "value": "0.00009424",
                    "n": 0,
                    "scriptPubKey": {
                        "asm": "OP_DUP OP_HASH160 64a8390b0b1685fcbf2d4b457118dc8da92d5534 OP_EQUALVERIFY OP_CHECKSIG",
                        "hex": "76a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac",
                        "type": "p2pkh",
                        "address": "mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q"
                    }
                }
            ]
        },
        "network": "testnet"
    }

    decode = cli_tester.invoke(
        cli_main, [
            "bitcoin",
            "decode",
            "--raw", "asdfhklajdfhklsjdhfkladsjf"
        ]
    )
    assert decode.exit_code == 0
    assert decode.output == "Error: invalid Bitcoin transaction raw" + "\n"

    decode = cli_tester.invoke(
        cli_main, [
            "bitcoin",
            "decode",
            "--raw", "eyJtZWhlcmV0dA=="
        ]
    )
    assert decode.exit_code == 0
    assert decode.output == "Error: invalid Bitcoin transaction raw" + "\n"

    decode = cli_tester.invoke(
        cli_main, [
            "bitcoin",
            "decode",
            "--raw", "eyJtZWhlcmV0dCI6ICJhc2RmYXNkZmFzZGYifQ=="
        ]
    )
    assert decode.exit_code == 0
    assert decode.output == "Error: invalid Bitcoin transaction raw" + "\n"
