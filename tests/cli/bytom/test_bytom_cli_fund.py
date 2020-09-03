#!/usr/bin/env python3

from swap.providers.bytom.wallet import Wallet
from swap.cli.__main__ import main as cli_main


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
    assert fund.output == "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiNTcxNzg0YTgtMDk0NS00ZDc4LWI5NzMtYWFjNGIwOWQ2NDM5IiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbImY4NGM3NmU5YmU2NzA3MmFlNWJjM2YzM2FmNzc2ZTkxMjQxMWEyZjc0OTkzODUwNTBjZmZmNzhjMjEwZTc5NjQiXSwgInB1YmxpY19rZXkiOiAiM2UwYTM3N2FlNGFmYTAzMWQ0NTUxNTk5ZDliYjdkNWIyN2Y0NzM2ZDc3Zjc4Y2FjNGQ0NzZmMGZmYmE1YWUzZSIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9LCB7ImRhdGFzIjogWyJmMzkzNWNhNDExNjM0ZWQyYTdiOTUyYjQxYmEyMWM0NTNlMmFhMTk3ZTZjOWVmZWViZWRhODM2OGEzMGU5MzZhIl0sICJwdWJsaWNfa2V5IjogIjNlMGEzNzdhZTRhZmEwMzFkNDU1MTU5OWQ5YmI3ZDViMjdmNDczNmQ3N2Y3OGNhYzRkNDc2ZjBmZmJhNWFlM2UiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJoYXNoIjogIjhkN2Q5ZWJlOTEzZTI5YTM0MDQ5OWMxZjhkMGE4Mjc0MDdjYmQ4OGIzNTBjMDEzYTU1NDBhMTUyNmZlNGQyMjIiLCAicmF3IjogIjA3MDEwMDAyMDE1ZDAxNWIxMzg4MWYzMjdlMmJlMGQ1YzAwZjM4NTYwZjFjMjk0ODZjZGFmMjU1YzA5YzAxZWVlMWExZWJhYTM3ODNkZGQ5ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjkwNGUwMDAxMTYwMDE0ODg3ZWU2NmQ4NGE4MmYyZDg2ODI0YTQ1YmI1MWZkZWEwM2M5MmY0OTIyMDEyMDNlMGEzNzdhZTRhZmEwMzFkNDU1MTU5OWQ5YmI3ZDViMjdmNDczNmQ3N2Y3OGNhYzRkNDc2ZjBmZmJhNWFlM2UwMTYwMDE1ZTEzODgxZjMyN2UyYmUwZDVjMDBmMzg1NjBmMWMyOTQ4NmNkYWYyNTVjMDljMDFlZWUxYTFlYmFhMzc4M2RkZDlmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjBlYmE1ZDMwMzAxMDExNjAwMTQ4ODdlZTY2ZDg0YTgyZjJkODY4MjRhNDViYjUxZmRlYTAzYzkyZjQ5MjIwMTIwM2UwYTM3N2FlNGFmYTAzMWQ0NTUxNTk5ZDliYjdkNWIyN2Y0NzM2ZDc3Zjc4Y2FjNGQ0NzZmMGZmYmE1YWUzZTAyMDE0NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDEyMjAwMjBhNWFkZGI3ZWI1NjQ5ZDEwMDMxMzA0ZWNlNzJkOWNjYzlkYzQyNGFiY2RhODk1ZDkwNGEzMDk3Mjc0MjRlNDBlMDAwMTNkZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYwYmVjM2NlMDMwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkwMCIsICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieXRvbV9mdW5kX3Vuc2lnbmVkIn0=" + "\n"

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
