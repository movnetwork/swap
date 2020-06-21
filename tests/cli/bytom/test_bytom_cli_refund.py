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
    assert refund.output == "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiNTcxNzg0YTgtMDk0NS00ZDc4LWI5NzMtYWFjNGIw" \
                            "OWQ2NDM5IiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbIjZkNzk3OTEyMDk4YTFhNDgy" \
                            "M2ViMzAxMDgwMjgyNjA1NjEyODI1MTY5N2Q1YWNjNjViM2M3MzhiN2ZkZDU3MGQiXSwgIm5ldHdv" \
                            "cmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBbIjliNmNlMjM5MjQ1YzVk" \
                            "MjRjZGE5ZTBmYmQ1M2Q0ZWI1YzRhOTJhMDVjZDBlZjkwNmRiY2M0YzNkYzBkZDMxOTAiXSwgInB1" \
                            "YmxpY19rZXkiOiAiM2UwYTM3N2FlNGFmYTAzMWQ0NTUxNTk5ZDliYjdkNWIyN2Y0NzM2ZDc3Zjc4" \
                            "Y2FjNGQ0NzZmMGZmYmE1YWUzZSIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0" \
                            "LzE1My8xLzAvMSJ9XSwgImhhc2giOiAiYjM4MWMxYmE1YmY1MzA5Y2Y1MTljNTIwMjZhZDBhMjQ0" \
                            "ODA5N2UwM2YwMzdlY2EyNzllOGRiODAxNDYxYmYwYyIsICJyYXciOiAiMDcwMTAwMDIwMTY5MDE2" \
                            "NzAyZTBiMWFkMjEwNzIyMmNmYzEzYWI2YzMzNjVkMzY2YjVkMTNiMTFlNmRjN2UxZTBjYzRhZTU2" \
                            "NzZjZGVlNDRmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
                            "ZmZmZmZmZmZmZmZmZmZmOTA0ZTAwMDEyMjAwMjBhNWFkZGI3ZWI1NjQ5ZDEwMDMxMzA0ZWNlNzJk" \
                            "OWNjYzlkYzQyNGFiY2RhODk1ZDkwNGEzMDk3Mjc0MjRlNDBlMDEwMDAxNjAwMTVlMDJlMGIxYWQy" \
                            "MTA3MjIyY2ZjMTNhYjZjMzM2NWQzNjZiNWQxM2IxMWU2ZGM3ZTFlMGNjNGFlNTY3NmNkZWU0NGZm" \
                            "ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
                            "ZmZmZmZmMDk4ODhkODAzMDEwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVh" \
                            "MDNjOTJmNDkyMjAxMjAzZTBhMzc3YWU0YWZhMDMxZDQ1NTE1OTlkOWJiN2Q1YjI3ZjQ3MzZkNzdm" \
                            "NzhjYWM0ZDQ3NmYwZmZiYTVhZTNlMDIwMTNhZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
                            "ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjkwNGUwMTE2MDAxNDg4N2VlNjZkODRh" \
                            "ODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkwMDAxM2RmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
                            "ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjBlYmE1ZDMwMzAxMTYw" \
                            "MDE0ODg3ZWU2NmQ4NGE4MmYyZDg2ODI0YTQ1YmI1MWZkZWEwM2M5MmY0OTAwIiwgInNpZ25hdHVy" \
                            "ZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX3JlZnVuZF91bnNp" \
                            "Z25lZCJ9" + "\n"

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
