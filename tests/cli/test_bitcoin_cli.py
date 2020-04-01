#!/usr/bin/env python3
# coding=utf-8

from shuttle.cli import __main__ as cli_main


RAW = "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMWQyNDFjY2ZkMmZhMTc4OTNhNGE1YWNkZjg1ZWJjOWE1YjFkYTIzOGZhMmZhMDE2N" \
      "jMyMTFjZWNhZjVmMDc0Y2UwMTAwMDAwMDAwZmZmZmZmZmYwMmQwMDcwMDAwMDAwMDAwMDAxN2E5MTQ2ZjA4YjI1NGU0YzU4ZGM2NWY2Zj" \
      "M5OWMzYmU3MTc3YjkwMWY0YTY2ODc3MjA3MGYwMDAwMDAwMDAwMTk3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE" \
      "5MmQ1NTM0ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiA5ODc2MjQsICJuIjogMSwgInNjcmlwdCI6ICI3NmE5MTQ2" \
      "NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogI" \
      "mJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"

PRIVATE_KEY = "92cbbc5990cb5090326a76feeb321cad01048635afe5756523bbf9f7a75bf38b"

SIGNED = "eyJyYXciOiAiMDIwMDAwMDAwMWQyNDFjY2ZkMmZhMTc4OTNhNGE1YWNkZjg1ZWJjOWE1YjFkYTIzOGZhMmZhMDE2NjMyMTFjZWNhZj" \
         "VmMDc0Y2UwMTAwMDAwMDZhNDczMDQ0MDIyMDI0ZjBkYzc0MmJkY2JiNmZlYzYwMGU0ZjBjMTAzZGFjNzkwYTI3NDhjMGI4YjYxMjll" \
         "MzI5MWU2ZTlhMjdhZDUwMjIwM2Y0YmMwNzQyNTJhZTQ2MDMwZDViZWQ3ZTg5M2RkY2E2NWZiN2E1MGYwM2U0MDZkZjU3YTFiNDgwMD" \
         "Y2MDBjYjAxMjEwM2M1NmE2MDA1ZDRhODg5MmQyOGNjM2Y3MjY1ZTU2ODViNTQ4NjI3ZDU5MTA4OTczZTQ3NGM0ZTI2ZjY5YTRjODRm" \
         "ZmZmZmZmZjAyZDAwNzAwMDAwMDAwMDAwMDE3YTkxNDZmMDhiMjU0ZTRjNThkYzY1ZjZmMzk5YzNiZTcxNzdiOTAxZjRhNjY4NzcyMD" \
         "cwZjAwMDAwMDAwMDAxOTc2YTkxNDY0YTgzOTBiMGIxNjg1ZmNiZjJkNGI0NTcxMThkYzhkYTkyZDU1MzQ4OGFjMDAwMDAwMDAiLCAi" \
         "ZmVlIjogNjc4LCAibmV0d29yayI6ICJ0ZXN0bmV0IiwgInR5cGUiOiAiYml0Y29pbl9mdW5kX3NpZ25lZCJ9"

DECODE_RESULT = {
    "fee": 678,
    "type": "bitcoin_fund_unsigned",
    "tx": {
        "hex": "0200000001d241ccfd2fa17893a4a5acdf85ebc9a5b1da238fa2fa01663211cecaf5f074ce0100000000ffffffff02d0"
               "0700000000000017a9146f08b254e4c58dc65f6f399c3be7177b901f4a668772070f00000000001976a91464a8390b0b"
               "1685fcbf2d4b457118dc8da92d553488ac00000000",
        "txid": "97272e7b392ca7c193ea71043e81d9bbe3fbfda90a21ededf59e5101216c0582",
        "hash": "97272e7b392ca7c193ea71043e81d9bbe3fbfda90a21ededf59e5101216c0582",
        "size": 117,
        "vsize": 117,
        "version": 2,
        "locktime": 0,
        "vin": [
            {
                "txid": "ce74f0f5cace11326601faa28f23dab1a5c9eb85dfaca5a49378a12ffdcc41d2",
                "vout": 1,
                "scriptSig": {
                    "asm": "",
                    "hex": ""
                },
                "sequence": "4294967295"
            }
        ],
        "vout": [
            {
                "value": "0.00002000",
                "n": 0,
                "scriptPubKey": {
                    "asm": "OP_HASH160 6f08b254e4c58dc65f6f399c3be7177b901f4a66 OP_EQUAL",
                    "hex": "a9146f08b254e4c58dc65f6f399c3be7177b901f4a6687",
                    "type": "p2sh",
                    "address": "2N3NKQpymf1KunR4W8BpZjs8za5La5pV5hF"
                }
            },
            {
                "value": "0.00984946",
                "n": 1,
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


# Success template
def success(_):
    return "[{}] {}".format("SUCCESS", str(_))


def test_bitcoin_cli(cli_tester):
    assert cli_tester.invoke(cli_main.shuttle,
                             ["bitcoin"]).exit_code == 0

    # Testing bitcoin decode command.
    decode = cli_tester.invoke(cli_main.shuttle,
                               ["bitcoin", "decode", "--raw", RAW])
    assert decode.exit_code == 0
    assert decode.output != success(DECODE_RESULT) + "\n"

    # Testing bitcoin sign command.
    sign = cli_tester.invoke(cli_main.shuttle,
                             ["bitcoin", "sign", "--unsigned", RAW, "--private", PRIVATE_KEY])
    assert sign.exit_code == 0
    assert sign.output == success(SIGNED) + "\n"

    # Testing bitcoin submit command.
    submit = cli_tester.invoke(cli_main.shuttle,
                               ["bitcoin", "submit", "--raw", RAW])
    assert submit.exit_code == 0
    assert submit.output == "[ERROR] Missing inputs" + "\n"
