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
unsigned_fund_transaction_raw = "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiNTcxNzg0YTgtMDk0NS00ZDc4LWI5NzMtYWFjN" \
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
                                "RvbV9mdW5kX3Vuc2lnbmVkIn0="
unsigned_claim_transaction_raw = "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUy" \
                                 "ZDEwODNhMTNiIiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbImRjOTdiYjAzYjU1" \
                                 "ODE0MzUzYjBiODAyNmUxNTZiZjZhNTI5ZGJlYzcyOTA1NmI3MTIwNzkwY2JjNzcwMDIzYzUi" \
                                 "XSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBbImEw" \
                                 "NmVlZWIzODZlYTkxNjZkYjMwMTM1YmQ0YjQ1Nzk1ZjE5OWQxZDNlODlmNjVhNzlkMTVlN2E1" \
                                 "NmQ2ZmFmMmQiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0" \
                                 "MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1h" \
                                 "aW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgImhhc2giOiAiMjU1NGM2OTU0" \
                                 "YjczNWIwOTJmNjRiOWFhM2QzMWQ3NDVmMTRhYmVlYTc1NWQ3NWY5Y2RmYzBlMjUzMWQ3NWYx" \
                                 "YiIsICJyYXciOiAiMDcwMTAwMDIwMTY5MDE2NzAyZTBiMWFkMjEwNzIyMmNmYzEzYWI2YzMz" \
                                 "NjVkMzY2YjVkMTNiMTFlNmRjN2UxZTBjYzRhZTU2NzZjZGVlNDRmZmZmZmZmZmZmZmZmZmZm" \
                                 "ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOTA0ZTAw" \
                                 "MDEyMjAwMjBhNWFkZGI3ZWI1NjQ5ZDEwMDMxMzA0ZWNlNzJkOWNjYzlkYzQyNGFiY2RhODk1" \
                                 "ZDkwNGEzMDk3Mjc0MjRlNDBlMDEwMDAxNjAwMTVlNThjMmZjODFjNDY5ZWM3YTljOWQ5Mjhi" \
                                 "NzhkZWMxOGNjZTEwYmQwMjUwNGRhYWQxYWI5ZjRlMGFjYmM3NzYxY2ZmZmZmZmZmZmZmZmZm" \
                                 "ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZlMDlh" \
                                 "YmJlNTAzMDEwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMz" \
                                 "MmEyMjAxMjA5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWRl" \
                                 "Zjk1NThhZDFiNjQ0OGYyMmUyMDIwMTNhZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
                                 "ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjkwNGUwMTE2MDAxNDJjZGE0Zjk5" \
                                 "ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEwMDAxM2RmZmZmZmZmZmZmZmZmZmZm" \
                                 "ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZTBlZGQ4" \
                                 "ZTAwMzAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTAw" \
                                 "IiwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJzaWduYXR1cmVzIjogW10sICJ0eXBlIjogImJ5" \
                                 "dG9tX2NsYWltX3Vuc2lnbmVkIn0"
unsigned_refund_transaction_raw = "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiNTcxNzg0YTgtMDk0NS00ZDc4LWI5NzMtYWFjNGIw" \
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
                                  "Z25lZCJ9"
htlc_bytecode = "02e803203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e2091ff7f525ff408" \
                "74c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2203a26da82ead15a80533a02696656b14b5dbf" \
                "d84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972" \
                "ae7cac00c0"
secret = "Hello Meheret!"


def test_bytom_cli_signature(cli_tester):

    signed_fund_transaction_raw = cli_tester.invoke(
        cli_main, [
            "bytom",
            "sign",
            "--raw", unsigned_fund_transaction_raw,
            "--xprivate", sender_wallet.xprivate_key()
        ]
    )
    assert signed_fund_transaction_raw.exit_code == 0
    assert signed_fund_transaction_raw.output == "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiNTcxNzg0YTgtMDk0NS00ZDc4L" \
                                                 "WI5NzMtYWFjNGIwOWQ2NDM5IiwgInJhdyI6ICIwNzAxMDAwMTAxNjAwMTVlMD" \
                                                 "JlMGIxYWQyMTA3MjIyY2ZjMTNhYjZjMzM2NWQzNjZiNWQxM2IxMWU2ZGM3ZTF" \
                                                 "lMGNjNGFlNTY3NmNkZWU0NGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
                                                 "ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmMDk4ODhkODAzM" \
                                                 "DEwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOT" \
                                                 "JmNDkyMjAxMjAzZTBhMzc3YWU0YWZhMDMxZDQ1NTE1OTlkOWJiN2Q1YjI3ZjQ" \
                                                 "3MzZkNzdmNzhjYWM0ZDQ3NmYwZmZiYTVhZTNlMDIwMTQ2ZmZmZmZmZmZmZmZm" \
                                                 "ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZ" \
                                                 "mZmZmZmZjkwNGUwMTIyMDAyMGE1YWRkYjdlYjU2NDlkMTAwMzEzMDRlY2U3Mm" \
                                                 "Q5Y2NjOWRjNDI0YWJjZGE4OTVkOTA0YTMwOTcyNzQyNGU0MGUwMDAxM2RmZmZ" \
                                                 "mZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
                                                 "ZmZmZmZmZmZmZmZmZmZmZTA5ZGE1ZDMwMzAxMTYwMDE0ODg3ZWU2NmQ4NGE4M" \
                                                 "mYyZDg2ODI0YTQ1YmI1MWZkZWEwM2M5MmY0OTAwIiwgImhhc2giOiAiODljOT" \
                                                 "U0NDA0YmRiM2U2MTIzZWQ4YTQxM2ZlM2JkNTI2YmY3YjU1MjkzNmQ4MGZkOGM" \
                                                 "zN2MyZDdlYWU2ZDBjMCIsICJ1bnNpZ25lZF9kYXRhcyI6IFt7ImRhdGFzIjog" \
                                                 "WyJiNTU4MTg0YmQyYzVjZjFkN2FmOTUyMjdmODk5Njc3N2Q0NmQ0MTA2OWE4M" \
                                                 "mY3OGMxMWM2MTgwYTUzMmVlYjg1Il0sICJwdWJsaWNfa2V5IjogIjNlMGEzNz" \
                                                 "dhZTRhZmEwMzFkNDU1MTU5OWQ5YmI3ZDViMjdmNDczNmQ3N2Y3OGNhYzRkNDc" \
                                                 "2ZjBmZmJhNWFlM2UiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAi" \
                                                 "bS80NC8xNTMvMS8wLzEifV0sICJuZXR3b3JrIjogIm1haW5uZXQiLCAic2lnb" \
                                                 "mF0dXJlcyI6IFtbImUwYWYwODg2ZTEyNjkyNGZhMTYzNzMxNGUzODY2OTUxMm" \
                                                 "QyNzU5ZTYwYjZjZjY5Njk5NjE2ZDhkYTViMGEzMTZiN2Y2NjJmZWQ1NThjOGF" \
                                                 "kYzY1ZjI4OGU5MzdmYzFlMjczZDIzNTg3ZmJhZWE2Mjk5NGQxYWQxZmE3OTVm" \
                                                 "MTAzIl1dLCAidHlwZSI6ICJieXRvbV9mdW5kX3NpZ25lZCJ9" + "\n"

    signed_claim_transaction_raw = cli_tester.invoke(
        cli_main, [
            "bytom",
            "sign",
            "--raw", unsigned_claim_transaction_raw,
            "--xprivate", recipient_wallet.xprivate_key(),
            "--secret", secret,
            "--bytecode", htlc_bytecode
        ]
    )
    assert signed_claim_transaction_raw.exit_code == 0
    assert signed_claim_transaction_raw.output == "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkL" \
                                                  "Tg4NjYtYTUyZDEwODNhMTNiIiwgInJhdyI6ICIwNzAxMDAwMjAxNjkwMTY3MD" \
                                                  "JlMGIxYWQyMTA3MjIyY2ZjMTNhYjZjMzM2NWQzNjZiNWQxM2IxMWU2ZGM3ZTF" \
                                                  "lMGNjNGFlNTY3NmNkZWU0NGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
                                                  "ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDAwMTIyM" \
                                                  "DAyMGE1YWRkYjdlYjU2NDlkMTAwMzEzMDRlY2U3MmQ5Y2NjOWRjNDI0YWJjZG" \
                                                  "E4OTVkOTA0YTMwOTcyNzQyNGU0MGUwMTAwMDE2MDAxNWU1OGMyZmM4MWM0Njl" \
                                                  "lYzdhOWM5ZDkyOGI3OGRlYzE4Y2NlMTBiZDAyNTA0ZGFhZDFhYjlmNGUwYWNi" \
                                                  "Yzc3NjFjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZ" \
                                                  "mZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmUwOWFiYmU1MDMwMTAxMTYwMDE0Mm" \
                                                  "NkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTIyMDEyMDk" \
                                                  "xZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVm" \
                                                  "OTU1OGFkMWI2NDQ4ZjIyZTIwMjAxM2FmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZ" \
                                                  "mZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOTA0ZT" \
                                                  "AxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzM" \
                                                  "yYTAwMDEzZGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
                                                  "ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZlMGVkZDhlMDAzMDExNjAwMTQyY" \
                                                  "2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAiaG" \
                                                  "FzaCI6ICIyNTU0YzY5NTRiNzM1YjA5MmY2NGI5YWEzZDMxZDc0NWYxNGFiZWV" \
                                                  "hNzU1ZDc1ZjljZGZjMGUyNTMxZDc1ZjFiIiwgInVuc2lnbmVkX2RhdGFzIjog" \
                                                  "W3siZGF0YXMiOiBbImRjOTdiYjAzYjU1ODE0MzUzYjBiODAyNmUxNTZiZjZhN" \
                                                  "TI5ZGJlYzcyOTA1NmI3MTIwNzkwY2JjNzcwMDIzYzUiXSwgIm5ldHdvcmsiOi" \
                                                  "AibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBbImEwNmVlZWI" \
                                                  "zODZlYTkxNjZkYjMwMTM1YmQ0YjQ1Nzk1ZjE5OWQxZDNlODlmNjVhNzlkMTVl" \
                                                  "N2E1NmQ2ZmFmMmQiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3N" \
                                                  "GM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMj" \
                                                  "JlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8" \
                                                  "xLzAvMSJ9XSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJzaWduYXR1cmVzIjog" \
                                                  "W1siNDg2NTZjNmM2ZjIwNGQ2NTY4NjU3MjY1NzQyMSIsICI4MzNjYjdlOTQ0N" \
                                                  "jg4YjBhN2I4YzA5ZmJiOTIwYmNjNjdlMzlmNDQzNWE2OWU4N2Q2N2MzODYwMD" \
                                                  "Q2NzRjMjNlODBlYzk1YzYyMTk1ZTJlNTY0YzdmZmM1YzQ4ZDk1YTJkZDI2MWU" \
                                                  "xY2UyYTFkNjk3YWFlZDZlNWNlNzU2N2YwMyIsICIwMCIsICIwMmU4MDMyMDNl" \
                                                  "MGEzNzdhZTRhZmEwMzFkNDU1MTU5OWQ5YmI3ZDViMjdmNDczNmQ3N2Y3OGNhY" \
                                                  "zRkNDc2ZjBmZmJhNWFlM2UyMDkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiND" \
                                                  "JlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIyMDNhMjZkYTg" \
                                                  "yZWFkMTVhODA1MzNhMDI2OTY2NTZiMTRiNWRiZmQ4NGViMTQ3OTBmMmUxYmU1" \
                                                  "ZTllNDU4MjBlZWI3NDFmNTQ3YTY0MTYwMDAwMDA1NTdhYTg4ODUzN2E3Y2FlN" \
                                                  "2NhYzYzMWYwMDAwMDA1MzdhY2Q5ZjY5NzJhZTdjYWMwMGMwIl0sIFsiMWY4Ym" \
                                                  "MwOWM0MDRiMWE2ZTY3NDE1NjkwZmY1NjA1OWM3NTRjODhmNjc0N2NhMDZkOTl" \
                                                  "kYTQ1NTI3YmVlMWY3ZDNjNGNlMzZhMDhkYjNiM2IyNWY2MWU5MjNhMDU1Mjg5" \
                                                  "ZmYyMjYxNjFiZjg3Y2RhM2U3YWQyZDcxMGVjZDIyMDEiXV0sICJ0eXBlIjogI" \
                                                  "mJ5dG9tX2NsYWltX3NpZ25lZCJ9" + "\n"

    signed_claim_transaction_raw = cli_tester.invoke(
        cli_main, [
            "bytom",
            "sign",
            "--raw", unsigned_claim_transaction_raw,
            "--xprivate", recipient_wallet.xprivate_key(),
            # "--secret", secret,
            "--bytecode", htlc_bytecode
        ]
    )
    assert signed_claim_transaction_raw.exit_code == 0
    assert signed_claim_transaction_raw.output == \
        'Error: secret key is required for claim, use -s or --secret "Hello Meheret!"' + '\n'

    signed_claim_transaction_raw = cli_tester.invoke(
        cli_main, [
            "bytom",
            "sign",
            "--raw", unsigned_claim_transaction_raw,
            "--xprivate", recipient_wallet.xprivate_key(),
            "--secret", secret,
            # "--bytecode", htlc_bytecode
        ]
    )
    assert signed_claim_transaction_raw.exit_code == 0
    assert signed_claim_transaction_raw.output == \
        'Error: witness bytecode is required for claim, use -b or --bytecode "016..."' + '\n'

    signed_refund_transaction_raw = cli_tester.invoke(
        cli_main, [
            "bytom",
            "sign",
            "--raw", unsigned_refund_transaction_raw,
            "--xprivate", sender_wallet.xprivate_key(),
            "--bytecode", htlc_bytecode
        ]
    )
    assert signed_refund_transaction_raw.exit_code == 0
    assert signed_refund_transaction_raw.output == "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiNTcxNzg0YTgtMDk0NS00ZD" \
                                                   "c4LWI5NzMtYWFjNGIwOWQ2NDM5IiwgInJhdyI6ICIwNzAxMDAwMjAxNjkw" \
                                                   "MTY3MDJlMGIxYWQyMTA3MjIyY2ZjMTNhYjZjMzM2NWQzNjZiNWQxM2IxMW" \
                                                   "U2ZGM3ZTFlMGNjNGFlNTY3NmNkZWU0NGZmZmZmZmZmZmZmZmZmZmZmZmZm" \
                                                   "ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
                                                   "Y5MDRlMDAwMTIyMDAyMGE1YWRkYjdlYjU2NDlkMTAwMzEzMDRlY2U3MmQ5" \
                                                   "Y2NjOWRjNDI0YWJjZGE4OTVkOTA0YTMwOTcyNzQyNGU0MGUwMTAwMDE2MD" \
                                                   "AxNWUwMmUwYjFhZDIxMDcyMjJjZmMxM2FiNmMzMzY1ZDM2NmI1ZDEzYjEx" \
                                                   "ZTZkYzdlMWUwY2M0YWU1Njc2Y2RlZTQ0ZmZmZmZmZmZmZmZmZmZmZmZmZm" \
                                                   "ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
                                                   "ZmYwOTg4OGQ4MDMwMTAxMTYwMDE0ODg3ZWU2NmQ4NGE4MmYyZDg2ODI0YT" \
                                                   "Q1YmI1MWZkZWEwM2M5MmY0OTIyMDEyMDNlMGEzNzdhZTRhZmEwMzFkNDU1" \
                                                   "MTU5OWQ5YmI3ZDViMjdmNDczNmQ3N2Y3OGNhYzRkNDc2ZjBmZmJhNWFlM2" \
                                                   "UwMjAxM2FmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
                                                   "ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOTA0ZTAxMTYwMDE0ODg3ZW" \
                                                   "U2NmQ4NGE4MmYyZDg2ODI0YTQ1YmI1MWZkZWEwM2M5MmY0OTAwMDEzZGZm" \
                                                   "ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
                                                   "ZmZmZmZmZmZmZmZmZmZmZmZmZmMGViYTVkMzAzMDExNjAwMTQ4ODdlZTY2" \
                                                   "ZDg0YTgyZjJkODY4MjRhNDViYjUxZmRlYTAzYzkyZjQ5MDAiLCAiaGFzaC" \
                                                   "I6ICJiMzgxYzFiYTViZjUzMDljZjUxOWM1MjAyNmFkMGEyNDQ4MDk3ZTAz" \
                                                   "ZjAzN2VjYTI3OWU4ZGI4MDE0NjFiZjBjIiwgInVuc2lnbmVkX2RhdGFzIj" \
                                                   "ogW3siZGF0YXMiOiBbIjZkNzk3OTEyMDk4YTFhNDgyM2ViMzAxMDgwMjgy" \
                                                   "NjA1NjEyODI1MTY5N2Q1YWNjNjViM2M3MzhiN2ZkZDU3MGQiXSwgIm5ldH" \
                                                   "dvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBb" \
                                                   "IjliNmNlMjM5MjQ1YzVkMjRjZGE5ZTBmYmQ1M2Q0ZWI1YzRhOTJhMDVjZD" \
                                                   "BlZjkwNmRiY2M0YzNkYzBkZDMxOTAiXSwgInB1YmxpY19rZXkiOiAiM2Uw" \
                                                   "YTM3N2FlNGFmYTAzMWQ0NTUxNTk5ZDliYjdkNWIyN2Y0NzM2ZDc3Zjc4Y2" \
                                                   "FjNGQ0NzZmMGZmYmE1YWUzZSIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAi" \
                                                   "cGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgIm5ldHdvcmsiOiAibWFpbm" \
                                                   "5ldCIsICJzaWduYXR1cmVzIjogW1siOTZlYmQ2YTI2NzZmMWU0MzM1MzU0" \
                                                   "NjBlZDAwYjA3MDNjZWJmYTViMmU3ZTcwNTMzYmY5Mjk3NzFiNDc5MzAxZm" \
                                                   "JiYzhmMDE2MzNkYmVmNzFlZGU2ZDI2ZjBiOTcyM2NjMzUxYzkwZDJmOTcy" \
                                                   "M2E3YzZkYjljNDkwMmYxNTdjMDgiLCAiMDEiLCAiMDJlODAzMjAzZTBhMz" \
                                                   "c3YWU0YWZhMDMxZDQ1NTE1OTlkOWJiN2Q1YjI3ZjQ3MzZkNzdmNzhjYWM0" \
                                                   "ZDQ3NmYwZmZiYTVhZTNlMjA5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYj" \
                                                   "QyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1NThhZDFiNjQ0OGYyMmUyMjAzYTI2" \
                                                   "ZGE4MmVhZDE1YTgwNTMzYTAyNjk2NjU2YjE0YjVkYmZkODRlYjE0NzkwZj" \
                                                   "JlMWJlNWU5ZTQ1ODIwZWViNzQxZjU0N2E2NDE2MDAwMDAwNTU3YWE4ODg1" \
                                                   "MzdhN2NhZTdjYWM2MzFmMDAwMDAwNTM3YWNkOWY2OTcyYWU3Y2FjMDBjMC" \
                                                   "JdLCBbImRkZTE2OWM2ZDUxY2JmZjYwZjFjMmVjYTZhNTMxODY1NTc4Nzcw" \
                                                   "ZmVmYWU5MGUwMmQyYjY2MTQwMGQ1ZmJmMTc3OTljNGY2NTE3NGI0NDAyZm" \
                                                   "JlN2E3ZDRkMzU0ZmRjYjc0MmU0OWQ1MTA1YTc1MjM2YTgyMjcyY2NhNmNh" \
                                                   "YjBhIl1dLCAidHlwZSI6ICJieXRvbV9yZWZ1bmRfc2lnbmVkIn0=" + "\n"

    signed_refund_transaction_raw = cli_tester.invoke(
        cli_main, [
            "bytom",
            "sign",
            "--raw", unsigned_refund_transaction_raw,
            "--xprivate", sender_wallet.xprivate_key(),
            # "--bytecode", htlc_bytecode
        ]
    )
    assert signed_refund_transaction_raw.exit_code == 0
    assert signed_refund_transaction_raw.output == \
        'Error: witness bytecode is required for refund, use -b or --bytecode "016..."' + '\n'

    signed = cli_tester.invoke(
        cli_main, [
            "bytom",
            "sign",
            "--raw", "eyJtZWhlcmV0dCI6ICJhc2RmYXNkZmFzZGYifQ==",
            "--xprivate", sender_wallet.xprivate_key()
        ]
    )
    assert signed.exit_code == 0
    assert str(signed.output).startswith("Warning: there is no type & network provided")

    signed = cli_tester.invoke(
        cli_main, [
            "bytom",
            "sign",
            "--raw", "eyJtZWhlcmV0dA==",
            "--xprivate", sender_wallet.xprivate_key()
        ]
    )
    assert signed.exit_code == 0
    assert signed.output == "Error: invalid Bytom unsigned transaction raw" + "\n"

    signed = cli_tester.invoke(
        cli_main, [
            "bytom",
            "sign",
            "--raw", "eyJtZWhlcmV0dA==",
            "--xprivate", "lakdsjfhalksdjfhskldjhklsdjhfaklsjdhfklj"
        ]
    )
    assert signed.exit_code == 0
    assert signed.output == "Error: invalid Bytom xprivate key" + "\n"

    signed = cli_tester.invoke(
        cli_main, [
            "bytom",
            "sign",
            "--raw", "eyJyYXciOiAiMDIwMDAwMDAwMWVjMzEyZTkyZDgzODdiMTVmNjIzOGQ0OTE4MzQ0YjYyYWIxNDdkN2YzODQ0ZG"
                     "M4MWU2NTM3NzZmZThiODRlZjMwMDAwMDAwMGNhNDczMDQ0MDIyMDBiMGZjM2IzYjg5MTc2MWU1Y2JlZTViYzFm"
                     "M2M2ZDdiMDkwNGMxMzQ3NWVlZjViNzk2NWM5YmZkYTFkMDhhMmEwMjIwNWViZGM3MmNiNzYzYTJlN2YyOTA3OD"
                     "diOGQ3ZGVmZDk3MmI0MWEyYjRkYzFjNDk5ZDY5OTkxZjBlNDUwNjY1OTAxMjEwM2M1NmE2MDA1ZDRhODg5MmQy"
                     "OGNjM2Y3MjY1ZTU2ODViNTQ4NjI3ZDU5MTA4OTczZTQ3NGM0ZTI2ZjY5YTRjODQwMDRjNWQ2M2FhMjA4MjExMj"
                     "RiNTU0ZDEzZjI0N2IxZTVkMTBiODRlNDRmYjEyOTZmMThmMzhiYmFhMWJlYTM0YTEyYzg0M2UwMTU4ODg3NmE5"
                     "MTQ5OGY4NzlmYjdmOGI0OTUxZGVlOWJjOGEwMzI3Yjc5MmZiZTMzMmI4ODhhYzY3MDJlODAzYjI3NTc2YTkxND"
                     "Y0YTgzOTBiMGIxNjg1ZmNiZjJkNGI0NTcxMThkYzhkYTkyZDU1MzQ4OGFjNjhlODAzMDAwMDAxZDAyNDAwMDAw"
                     "MDAwMDAwMDE5NzZhOTE0NjRhODM5MGIwYjE2ODVmY2JmMmQ0YjQ1NzExOGRjOGRhOTJkNTUzNDg4YWMwMDAwMD"
                     "AwMCIsICJmZWUiOiA1NzYsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX3JlZnVuZF9z"
                     "aWduZWQifQ==",
            "--xprivate", sender_wallet.xprivate_key()
        ]
    )
    assert signed.exit_code == 0
    assert signed.output == "Error: unknown Bytom unsigned transaction raw type" + "\n"
