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


def test_bytom_cli_claim(cli_tester):

    claim = cli_tester.invoke(
        cli_main, [
            "bytom",
            "claim",
            "--transaction", transaction_id,
            "--recipient-guid", recipient_wallet.guid(),
            "--amount", amount,
            "--asset", asset,
            "--network", network
        ]
    )
    assert claim.exit_code == 0
    assert claim.output != "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwO" \
                           "DNhMTNiIiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbIjgzNGRkZjFkNjk3MmJlNzlhOD" \
                           "hjYmVlNTc0YjQ1MmI1ZGRmZGFlZmYwZjg0OWJhNDFlMTk2OGZhOGQ4MjBlYWIiXSwgIm5ldHdvcms" \
                           "iOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBbIjcyZGY2N2U5OWY3ZTI0OWM2" \
                           "YjJmN2JjNzA4MTgzODcyM2ExNDJlMWIzY2Y5YmIxZDRkODIzNTE5MDYwMTljMGYiXSwgInB1YmxpY" \
                           "19rZXkiOiAiNjkyOTdlOWI3NWVjODhhNGNhN2YwYzdhMWJiNjFkNjRlYTkzOTFiMTRhOTAyY2RhND" \
                           "g1ODBmZTNlMTJhODJhYiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8" \
                           "xLzEvMTIifV0sICJoYXNoIjogImQ1NTUwZGQxM2IxMGRhOTdiN2NkMjgyM2E2YTdjYmRlODgyYmQw" \
                           "MWI0MThjZjJjZDkyZmRjMjA3MzA5MDM3NDkiLCAicmF3IjogIjA3MDEwMDAyMDE2OTAxNjcwMmUwY" \
                           "jFhZDIxMDcyMjJjZmMxM2FiNmMzMzY1ZDM2NmI1ZDEzYjExZTZkYzdlMWUwY2M0YWU1Njc2Y2RlZT" \
                           "Q0ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZ" \
                           "mZmZmZmZmZjkwNGUwMDAxMjIwMDIwYTVhZGRiN2ViNTY0OWQxMDAzMTMwNGVjZTcyZDljY2M5ZGM0" \
                           "MjRhYmNkYTg5NWQ5MDRhMzA5NzI3NDI0ZTQwZTAxMDAwMTVmMDE1ZDdmMmQ3ZWNlYzNmNjFkMzBkM" \
                           "GIyOTY4OTczYTNhYzg0NDhmMDU5OWVhMjBkY2U4ODNiNDhjOTAzYzRkNmU4N2ZmZmZmZmZmZmZmZm" \
                           "ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYzBmMmZ" \
                           "kMTYwMDAxMTYwMDE0MmI1ZDExMGE4OWQxOTNlYThmMmYxZTU1M2E4OTIwODQ5YTU4ZTY4OTIyMDEy" \
                           "MDY5Mjk3ZTliNzVlYzg4YTRjYTdmMGM3YTFiYjYxZDY0ZWE5MzkxYjE0YTkwMmNkYTQ4NTgwZmUzZ" \
                           "TEyYTgyYWIwMjAxM2FmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
                           "ZmZmZmZmZmZmZmZmZmZmZmZmZmOTA0ZTAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE" \
                           "1N2VkNmRjNDA4MzMyYTAwMDEzY2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
                           "ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjMGM1OWIxMjAxMTYwMDE0MmI1ZDExMGE4OWQxOTNlY" \
                           "ThmMmYxZTU1M2E4OTIwODQ5YTU4ZTY4OTAwIiwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJzaWduYX" \
                           "R1cmVzIjogW10sICJ0eXBlIjogImJ5dG9tX2NsYWltX3Vuc2lnbmVkIn0=" + "\n"

    claim = cli_tester.invoke(
        cli_main, [
            "bytom",
            "claim",
            "--transaction", transaction_id,
            "--recipient-guid", 634653654354,
            "--amount", amount,
            "--asset", asset,
            "--network", network
        ]
    )
    assert claim.exit_code == 0
    assert claim.output == "Error: invalid recipient guid type, only takes string type" + "\n"

    claim = cli_tester.invoke(
        cli_main, [
            "bytom",
            "claim",
            "--transaction", transaction_id,
            "--recipient-guid", str(),
            "--amount", amount,
            "--asset", asset,
            "--network", network
        ]
    )
    assert claim.exit_code == 0
    assert claim.output == "Error: can't find recipient wallet guid from wallet" + "\n"
