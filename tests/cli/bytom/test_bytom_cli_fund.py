#!/usr/bin/env python3

from shuttle.providers.bytom.wallet import Wallet
from shuttle.cli.__main__ import main as cli_main


network = "mainnet"
sender_wallet = Wallet(network=network).from_mnemonic(
    mnemonic="hint excuse upgrade sleep easily deputy erase cluster section other ugly limit"
).from_guid(
    guid="571784a8-0945-4d78-b973-aac4b09d6439"
)
recipient_wallet = Wallet(network=network).from_mnemonic(
    mnemonic="indicate warm sock mistake code spot acid ribbon sing over taxi toast"
).from_guid(
    guid="f0ed6ddd-9d6b-49fd-8866-a52d1083a13b"
)
htlc_bytecode = "02e803203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e2091ff" \
                "7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2203a26da82ead15a80" \
                "533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a" \
                "7cae7cac631f000000537acd9f6972ae7cac00c0"
asset = "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
amount = 10_000


def test_bytom_cli_fund(cli_tester):

    fund = cli_tester.invoke(
        cli_main, [
            "bytom",
            "fund",
            "--sender-guid", sender_wallet.guid(),
            "--amount", amount,
            "--asset", asset,
            "--bytecode", htlc_bytecode,
            "--network", network
        ]
    )
    assert fund.exit_code == 0
    assert fund.output == "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiNTcxNzg0YTgtMDk0NS00ZDc4LWI5NzMtYWFjN" \
                          "GIwOWQ2NDM5IiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbImI1NTgxODRiZDJjNW" \
                          "NmMWQ3YWY5NTIyN2Y4OTk2Nzc3ZDQ2ZDQxMDY5YTgyZjc4YzExYzYxODBhNTMyZWViODUiXSw" \
                          "gInB1YmxpY19rZXkiOiAiM2UwYTM3N2FlNGFmYTAzMWQ0NTUxNTk5ZDliYjdkNWIyN2Y0NzM2" \
                          "ZDc3Zjc4Y2FjNGQ0NzZmMGZmYmE1YWUzZSIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0a" \
                          "CI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgImhhc2giOiAiODljOTU0NDA0YmRiM2U2MTIzZWQ4YT" \
                          "QxM2ZlM2JkNTI2YmY3YjU1MjkzNmQ4MGZkOGMzN2MyZDdlYWU2ZDBjMCIsICJyYXciOiAiMDc" \
                          "wMTAwMDEwMTYwMDE1ZTAyZTBiMWFkMjEwNzIyMmNmYzEzYWI2YzMzNjVkMzY2YjVkMTNiMTFl" \
                          "NmRjN2UxZTBjYzRhZTU2NzZjZGVlNDRmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZ" \
                          "mZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjA5ODg4ZDgwMzAxMDExNjAwMTQ4OD" \
                          "dlZTY2ZDg0YTgyZjJkODY4MjRhNDViYjUxZmRlYTAzYzkyZjQ5MjIwMTIwM2UwYTM3N2FlNGF" \
                          "mYTAzMWQ0NTUxNTk5ZDliYjdkNWIyN2Y0NzM2ZDc3Zjc4Y2FjNGQ0NzZmMGZmYmE1YWUzZTAy" \
                          "MDE0NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZ" \
                          "mZmZmZmZmZmZmZmZmY5MDRlMDEyMjAwMjBhNWFkZGI3ZWI1NjQ5ZDEwMDMxMzA0ZWNlNzJkOW" \
                          "NjYzlkYzQyNGFiY2RhODk1ZDkwNGEzMDk3Mjc0MjRlNDBlMDAwMTNkZmZmZmZmZmZmZmZmZmZ" \
                          "mZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmUwOWRh" \
                          "NWQzMDMwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkwM" \
                          "CIsICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieX" \
                          "RvbV9mdW5kX3Vuc2lnbmVkIn0=" + "\n"

    fund = cli_tester.invoke(
        cli_main, [
            "bytom",
            "fund",
            "--sender-guid", sender_wallet.guid(),
            "--amount", amount,
            "--asset", asset,
            "--bytecode", 100000000000,
            "--network", network
        ]
    )
    assert fund.exit_code == 0
    assert fund.output == "Error: invalid bytecode type, bytecode must be string format" + "\n"
