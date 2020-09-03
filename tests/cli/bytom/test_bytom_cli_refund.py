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
transaction_id = "049d4c26bb15885572c16e0eefac5b2f4d0fde50eaf90f002272d39507ff315b"
asset = "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
amount = 10_000


def test_bytom_cli_refund(cli_tester):

    refund = cli_tester.invoke(
        cli_main, [
            "bytom",
            "refund",
            "--transaction", transaction_id,
            "--sender-guid", sender_wallet.guid(),
            "--amount", amount,
            "--asset", asset,
            "--network", network
        ]
    )
    assert refund.exit_code == 0
    assert refund.output == "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiNTcxNzg0YTgtMDk0NS00ZDc4LWI5NzMtYWFjNGIwOWQ2NDM5IiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbIjMxNTMwY2ZlMjM0Njg5Y2RlZjVhYTUzMmE0MWI0YzZhN2Y1MzMzMjdkMzE5YWM2NGI1MGViYzY3MjhiMjZjNmYiXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBbIjZiYTZhYmZlYjkzZjQxMTlhMTQzMDJlYzg0ZWFhY2I0MDIxYTEyYWEzOTg3NDEwNWQwZTU0YWYzN2M5ZDQxMDUiXSwgInB1YmxpY19rZXkiOiAiM2UwYTM3N2FlNGFmYTAzMWQ0NTUxNTk5ZDliYjdkNWIyN2Y0NzM2ZDc3Zjc4Y2FjNGQ0NzZmMGZmYmE1YWUzZSIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgImhhc2giOiAiMjFhMDdmMWI2ZGU1ZjllNTQzNTk0OThhN2FiOGQ2ODA5YmM5ZmQ0NGExODE0YTBmMjg5NWY2YzZmYzk4MGQ5OCIsICJyYXciOiAiMDcwMTAwMDIwMTY5MDE2NzAyZTBiMWFkMjEwNzIyMmNmYzEzYWI2YzMzNjVkMzY2YjVkMTNiMTFlNmRjN2UxZTBjYzRhZTU2NzZjZGVlNDRmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOTA0ZTAwMDEyMjAwMjBhNWFkZGI3ZWI1NjQ5ZDEwMDMxMzA0ZWNlNzJkOWNjYzlkYzQyNGFiY2RhODk1ZDkwNGEzMDk3Mjc0MjRlNDBlMDEwMDAxNjAwMTVlMTM4ODFmMzI3ZTJiZTBkNWMwMGYzODU2MGYxYzI5NDg2Y2RhZjI1NWMwOWMwMWVlZTFhMWViYWEzNzgzZGRkOWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmMGViYTVkMzAzMDEwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkyMjAxMjAzZTBhMzc3YWU0YWZhMDMxZDQ1NTE1OTlkOWJiN2Q1YjI3ZjQ3MzZkNzdmNzhjYWM0ZDQ3NmYwZmZiYTVhZTNlMDIwMTNhZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjkwNGUwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkwMDAxM2RmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjBiZWMzY2UwMzAxMTYwMDE0ODg3ZWU2NmQ4NGE4MmYyZDg2ODI0YTQ1YmI1MWZkZWEwM2M5MmY0OTAwIiwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX3JlZnVuZF91bnNpZ25lZCJ9" + "\n"

    refund = cli_tester.invoke(
        cli_main, [
            "bytom",
            "refund",
            "--transaction", transaction_id,
            "--sender-guid", 634653654354,
            "--amount", amount,
            "--asset", asset,
            "--network", network
        ]
    )
    assert refund.exit_code == 0
    assert refund.output == "Error: invalid sender guid type, only takes string type" + "\n"

    refund = cli_tester.invoke(
        cli_main, [
            "bytom",
            "refund",
            "--transaction", transaction_id,
            "--sender-guid", str(),
            "--amount", amount,
            "--asset", asset,
            "--network", network
        ]
    )
    assert refund.exit_code == 0
    assert refund.output == "Error: can't find sender wallet guid from wallet" + "\n"
