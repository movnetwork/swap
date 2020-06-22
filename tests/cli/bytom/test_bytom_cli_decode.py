#!/usr/bin/env python3

from shuttle.cli.__main__ import main as cli_main


unsigned_transaction_raw = "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZD" \
                           "EwODNhMTNiIiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbIjgzNGRkZjFkNjk3MmJl" \
                           "NzlhODhjYmVlNTc0YjQ1MmI1ZGRmZGFlZmYwZjg0OWJhNDFlMTk2OGZhOGQ4MjBlYWIiXSwgIm" \
                           "5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBbIjcyZGY2N2U5" \
                           "OWY3ZTI0OWM2YjJmN2JjNzA4MTgzODcyM2ExNDJlMWIzY2Y5YmIxZDRkODIzNTE5MDYwMTljMG" \
                           "YiXSwgInB1YmxpY19rZXkiOiAiNjkyOTdlOWI3NWVjODhhNGNhN2YwYzdhMWJiNjFkNjRlYTkz" \
                           "OTFiMTRhOTAyY2RhNDg1ODBmZTNlMTJhODJhYiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicG" \
                           "F0aCI6ICJtLzQ0LzE1My8xLzEvMTIifV0sICJoYXNoIjogImQ1NTUwZGQxM2IxMGRhOTdiN2Nk" \
                           "MjgyM2E2YTdjYmRlODgyYmQwMWI0MThjZjJjZDkyZmRjMjA3MzA5MDM3NDkiLCAicmF3IjogIj" \
                           "A3MDEwMDAyMDE2OTAxNjcwMmUwYjFhZDIxMDcyMjJjZmMxM2FiNmMzMzY1ZDM2NmI1ZDEzYjEx" \
                           "ZTZkYzdlMWUwY2M0YWU1Njc2Y2RlZTQ0ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
                           "ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjkwNGUwMDAxMjIwMDIwYTVhZGRiN2Vi" \
                           "NTY0OWQxMDAzMTMwNGVjZTcyZDljY2M5ZGM0MjRhYmNkYTg5NWQ5MDRhMzA5NzI3NDI0ZTQwZT" \
                           "AxMDAwMTVmMDE1ZDdmMmQ3ZWNlYzNmNjFkMzBkMGIyOTY4OTczYTNhYzg0NDhmMDU5OWVhMjBk" \
                           "Y2U4ODNiNDhjOTAzYzRkNmU4N2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
                           "ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYzBmMmZkMTYwMDAxMTYwMDE0MmI1ZDExMGE4" \
                           "OWQxOTNlYThmMmYxZTU1M2E4OTIwODQ5YTU4ZTY4OTIyMDEyMDY5Mjk3ZTliNzVlYzg4YTRjYT" \
                           "dmMGM3YTFiYjYxZDY0ZWE5MzkxYjE0YTkwMmNkYTQ4NTgwZmUzZTEyYTgyYWIwMjAxM2FmZmZm" \
                           "ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
                           "ZmZmZmOTA0ZTAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMy" \
                           "YTAwMDEzY2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
                           "ZmZmZmZmZmZmZmZmZmZmZjMGM1OWIxMjAxMTYwMDE0MmI1ZDExMGE4OWQxOTNlYThmMmYxZTU1" \
                           "M2E4OTIwODQ5YTU4ZTY4OTAwIiwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJzaWduYXR1cmVzIj" \
                           "ogW10sICJ0eXBlIjogImJ5dG9tX2NsYWltX3Vuc2lnbmVkIn0="


def test_bitcoin_cli_decode(cli_tester):

    decode = cli_tester.invoke(
        cli_main, [
            "bytom",
            "decode",
            "--raw", unsigned_transaction_raw
        ]
    )
    assert decode.exit_code == 0
    assert decode.output != {
        "fee": 10000000,
        "guid": "f0ed6ddd-9d6b-49fd-8866-a52d1083a13b",
        "type": "bytom_claim_unsigned",
        "tx": {
            "tx_id": "d5550dd13b10da97b7cd2823a6a7cbde882bd01b418cf2cd92fdc20730903749",
            "version": 1,
            "size": 370,
            "time_range": 0,
            "inputs": [
                {
                    "type": "spend",
                    "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                    "asset_definition": {},
                    "amount": 10000,
                    "control_program": "0020a5addb7eb5649d10031304ece72d9ccc9dc424abcda895d904a309727424e40e",
                    "address": "bm1q5kkakl44vjw3qqcnqnkwwtvuejwugf9tek5ftkgy5vyhyapyus8qgcttcs",
                    "spent_output_id": "98a553b8cb08b8f6e0ded3c88a18841952d8cad7afdea41206881c5fa7a03548",
                    "input_id": "75565b5d1ff36b7898046d210ce53dbdff61322f4ed1e0e2a8943a99edb5b6b0",
                    "witness_arguments": None,
                    "sign_data": "834ddf1d6972be79a88cbee574b452b5ddfdaeff0f849ba41e1968fa8d820eab"
                },
                {
                    "type": "spend",
                    "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                    "asset_definition": {},
                    "amount": 48200000,
                    "control_program": "00142b5d110a89d193ea8f2f1e553a8920849a58e689",
                    "address": "bm1q9dw3zz5f6xf74re0re2n4zfqsjd93e5f9l4jxl",
                    "spent_output_id": "7e86b3f635595de17686c6d8d9d4f0281239d0db6af0bf0eaca763c46c2d455b",
                    "input_id": "5c49cf1f42e72aa418cd143628fcd321557fdda52da5249eb13cb2c57eb8d76e",
                    "witness_arguments": [
                        "69297e9b75ec88a4ca7f0c7a1bb61d64ea9391b14a902cda48580fe3e12a82ab"
                    ],
                    "sign_data": "72df67e99f7e249c6b2f7bc7081838723a142e1b3cf9bb1d4d82351906019c0f"
                }
            ],
            "outputs": [
                {
                    "type": "control",
                    "id": "a274d332fa3691ea34529d3f01949dd9bbc954978d6ea904916ea9ab5c3f17e7",
                    "position": 0,
                    "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                    "asset_definition": {},
                    "amount": 10000,
                    "control_program": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a",
                    "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7"
                },
                {
                    "type": "control",
                    "id": "0ce43636740fa0c9939b3dd1ad64afe9669c1af6b3cf7538a035bfe7aacd94e1",
                    "position": 1,
                    "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                    "asset_definition": {},
                    "amount": 38200000,
                    "control_program": "00142b5d110a89d193ea8f2f1e553a8920849a58e689",
                    "address": "bm1q9dw3zz5f6xf74re0re2n4zfqsjd93e5f9l4jxl"
                }
            ],
            "fee": 10000000
        },
        "unsigned_datas": [
            {
                "datas": [
                    "834ddf1d6972be79a88cbee574b452b5ddfdaeff0f849ba41e1968fa8d820eab"
                ],
                "network": "mainnet",
                "path": None
            },
            {
                "datas": [
                    "72df67e99f7e249c6b2f7bc7081838723a142e1b3cf9bb1d4d82351906019c0f"
                ],
                "public_key": "69297e9b75ec88a4ca7f0c7a1bb61d64ea9391b14a902cda48580fe3e12a82ab",
                "network": "mainnet",
                "path": "m/44/153/1/1/12"
            }
        ],
        "signatures": [],
        "network": "mainnet"
    }

    decode = cli_tester.invoke(
        cli_main, [
            "bytom",
            "decode",
            "--raw", "asdfhklajdfhklsjdhfkladsjf"
        ]
    )
    assert decode.exit_code == 0
    assert decode.output == "Error: invalid Bytom transaction raw" + "\n"

    decode = cli_tester.invoke(
        cli_main, [
            "bytom",
            "decode",
            "--raw", "eyJtZWhlcmV0dA=="
        ]
    )
    assert decode.exit_code == 0
    assert decode.output == "Error: invalid Bytom transaction raw" + "\n"

    decode = cli_tester.invoke(
        cli_main, [
            "bytom",
            "decode",
            "--raw", "eyJtZWhlcmV0dCI6ICJhc2RmYXNkZmFzZGYifQ=="
        ]
    )
    assert decode.exit_code == 0
    assert decode.output == "Error: invalid Bytom transaction raw" + "\n"
