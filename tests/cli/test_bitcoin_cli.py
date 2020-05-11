#!/usr/bin/env python3
# coding=utf-8

from shuttle.cli.__main__ import main as cli_main

import pytest

PRIVATE_KEY = "92cbbc5990cb5090326a76feeb321cad01048635afe5756523bbf9f7a75bf38b"

HTLC_BYTECODE = "63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a91498f879fb7f8b495" \
                "1dee9bc8a0327b792fbe332b888ac670164b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68"

FUND_RAW = \
    "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMWQyNDFjY2ZkMmZhMTc4OTNhNGE1YWNkZjg1ZWJjOWE1YjFkYTIzOGZhMmZhMDE2N" \
    "jMyMTFjZWNhZjVmMDc0Y2UwMTAwMDAwMDAwZmZmZmZmZmYwMmQwMDcwMDAwMDAwMDAwMDAxN2E5MTQ2ZjA4YjI1NGU0YzU4ZGM2NWY2Zj" \
    "M5OWMzYmU3MTc3YjkwMWY0YTY2ODc3MjA3MGYwMDAwMDAwMDAwMTk3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE" \
    "5MmQ1NTM0ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiA5ODc2MjQsICJuIjogMSwgInNjcmlwdCI6ICI3NmE5MTQ2" \
    "NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogI" \
    "mJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"

FUND_SIGNED = \
    "eyJyYXciOiAiMDIwMDAwMDAwMWQyNDFjY2ZkMmZhMTc4OTNhNGE1YWNkZjg1ZWJjOWE1YjFkYTIzOGZhMmZhMDE2NjMyMTFjZWNhZj" \
    "VmMDc0Y2UwMTAwMDAwMDZhNDczMDQ0MDIyMDI0ZjBkYzc0MmJkY2JiNmZlYzYwMGU0ZjBjMTAzZGFjNzkwYTI3NDhjMGI4YjYxMjll" \
    "MzI5MWU2ZTlhMjdhZDUwMjIwM2Y0YmMwNzQyNTJhZTQ2MDMwZDViZWQ3ZTg5M2RkY2E2NWZiN2E1MGYwM2U0MDZkZjU3YTFiNDgwMD" \
    "Y2MDBjYjAxMjEwM2M1NmE2MDA1ZDRhODg5MmQyOGNjM2Y3MjY1ZTU2ODViNTQ4NjI3ZDU5MTA4OTczZTQ3NGM0ZTI2ZjY5YTRjODRm" \
    "ZmZmZmZmZjAyZDAwNzAwMDAwMDAwMDAwMDE3YTkxNDZmMDhiMjU0ZTRjNThkYzY1ZjZmMzk5YzNiZTcxNzdiOTAxZjRhNjY4NzcyMD" \
    "cwZjAwMDAwMDAwMDAxOTc2YTkxNDY0YTgzOTBiMGIxNjg1ZmNiZjJkNGI0NTcxMThkYzhkYTkyZDU1MzQ4OGFjMDAwMDAwMDAiLCAi" \
    "ZmVlIjogNjc4LCAibmV0d29yayI6ICJ0ZXN0bmV0IiwgInR5cGUiOiAiYml0Y29pbl9mdW5kX3NpZ25lZCJ9"

CLAIM_RAW = "eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTUyYzIzZGM2NDU2N2IxY2ZhZjRkNzc2NjBjNzFjNzUxZjkwZTliYTVjMzc" \
            "0N2ZhYzFkMDA1MTgwOGVhMGQ2NTEwMDAwMDAwMDAwZmZmZmZmZmYwMWE4MDEwMDAwMDAwMDAwMDAxOTc2YTkxNDk4Zjg3OWZiN2" \
            "Y4YjQ5NTFkZWU5YmM4YTAzMjdiNzkyZmJlMzMyYjg4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IFt7ImFtb3VudCI6IDUwMDAsI" \
            "CJuIjogMCwgInNjcmlwdCI6ICJhOTE0NDMzZThlZDU5YjlhNjdmMGYxODdjNjNlYjQ1MGIwZDU2ZTI1NmVjMjg3In1dLCAicmVj" \
            "aXBpZW50X2FkZHJlc3MiOiAibXVUbmZmTERSNUx0RmVMUjJpM1dzS1ZmZHl2emZ5UG5WQiIsICJzZW5kZXJfYWRkcmVzcyI6ICJ" \
            "tcGhCUFpmMTVjUkZjTDV0VXE2bUNiRTg0WG9iWjF2ZzdRIiwgInNlY3JldCI6ICJIZWxsbyBNZWhlcmV0ISIsICJuZXR3b3JrIj" \
            "ogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX2NsYWltX3Vuc2lnbmVkIn0="

CLAIM_SIGNED = "eyJyYXciOiAiMDIwMDAwMDAwMTUyYzIzZGM2NDU2N2IxY2ZhZjRkNzc2NjBjNzFjNzUxZjkwZTliYTVjMzc0N2ZhYzFkMDA1" \
               "MTgwOGVhMGQ2NTEwMDAwMDAwMGQ5NDgzMDQ1MDIyMTAwZGVkZjY3ODAyNjdiMTE3ZDAzMmIyMDdkYmZiODdhNmQyM2JmNzYx" \
               "ZWU2YTAzZTc5OGZmZWQyNWExOTE5NjQ2NDAyMjAwZWY4NzJmZWRkZWFiMWRhZWE0MWM0MmI1NTljYTJhMTNjZWE2YWYwMWE3" \
               "ZWQ4YzMzZDJhZTk0ZmI2MGNlMWI4MDEyMTAzYzU2YTYwMDVkNGE4ODkyZDI4Y2MzZjcyNjVlNTY4NWI1NDg2MjdkNTkxMDg5" \
               "NzNlNDc0YzRlMjZmNjlhNGM4NDBlNDg2NTZjNmM2ZjIwNGQ2NTY4NjU3MjY1NzQyMTUxNGM1YzYzYWEyMDgyMTEyNGI1NTRk" \
               "MTNmMjQ3YjFlNWQxMGI4NGU0NGZiMTI5NmYxOGYzOGJiYWExYmVhMzRhMTJjODQzZTAxNTg4ODc2YTkxNDk4Zjg3OWZiN2Y4" \
               "YjQ5NTFkZWU5YmM4YTAzMjdiNzkyZmJlMzMyYjg4OGFjNjcwMTY0YjI3NTc2YTkxNDY0YTgzOTBiMGIxNjg1ZmNiZjJkNGI0" \
               "NTcxMThkYzhkYTkyZDU1MzQ4OGFjNjhmZmZmZmZmZjAxYTgwMTAwMDAwMDAwMDAwMDE5NzZhOTE0OThmODc5ZmI3ZjhiNDk1" \
               "MWRlZTliYzhhMDMyN2I3OTJmYmUzMzJiODg4YWMwMDAwMDAwMCIsICJmZWUiOiA1NzYsICJuZXR3b3JrIjogInRlc3RuZXQi" \
               "LCAidHlwZSI6ICJiaXRjb2luX2NsYWltX3NpZ25lZCJ9"

REFUND_RAW = "eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTUyYzIzZGM2NDU2N2IxY2ZhZjRkNzc2NjBjNzFjNzUxZjkwZTliYTVjMz" \
             "c0N2ZhYzFkMDA1MTgwOGVhMGQ2NTEwMDAwMDAwMDAwZmZmZmZmZmYwMWE4MDEwMDAwMDAwMDAwMDAxOTc2YTkxNDY0YTgzOTBi" \
             "MGIxNjg1ZmNiZjJkNGI0NTcxMThkYzhkYTkyZDU1MzQ4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IFt7ImFtb3VudCI6IDUwMD" \
             "AsICJuIjogMCwgInNjcmlwdCI6ICJhOTE0NDMzZThlZDU5YjlhNjdmMGYxODdjNjNlYjQ1MGIwZDU2ZTI1NmVjMjg3In1dLCAi" \
             "cmVjaXBpZW50X2FkZHJlc3MiOiAibXVUbmZmTERSNUx0RmVMUjJpM1dzS1ZmZHl2emZ5UG5WQiIsICJzZW5kZXJfYWRkcmVzcy" \
             "I6ICJtcGhCUFpmMTVjUkZjTDV0VXE2bUNiRTg0WG9iWjF2ZzdRIiwgInNlY3JldCI6ICJIZWxsbyBNZWhlcmV0ISIsICJuZXR3" \
             "b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX3JlZnVuZF91bnNpZ25lZCJ9"

REFUND_SIGNED = "eyJyYXciOiAiMDIwMDAwMDAwMTUyYzIzZGM2NDU2N2IxY2ZhZjRkNzc2NjBjNzFjNzUxZjkwZTliYTVjMzc0N2ZhYzFkMDA" \
                "1MTgwOGVhMGQ2NTEwMDAwMDAwMGM5NDczMDQ0MDIyMDM4MTdjNTRhZTgwZjc5YTQ0NGI2ZTM2ODVhZjgyN2QwOGY0MWNkMz" \
                "cyNGZmNDAyZjliYjVhYTNiNTc5Y2UyZWQwMjIwNTZhNGMxMWUxZDhlMWJhMjVjODYzMDM4YjgyM2Q3YmVlY2YzZWNjZjIyY" \
                "zYxYWNlODFmNDg0ZmViZmU4OGQyMTAxMjEwM2M1NmE2MDA1ZDRhODg5MmQyOGNjM2Y3MjY1ZTU2ODViNTQ4NjI3ZDU5MTA4" \
                "OTczZTQ3NGM0ZTI2ZjY5YTRjODQwMDRjNWM2M2FhMjA4MjExMjRiNTU0ZDEzZjI0N2IxZTVkMTBiODRlNDRmYjEyOTZmMTh" \
                "mMzhiYmFhMWJlYTM0YTEyYzg0M2UwMTU4ODg3NmE5MTQ5OGY4NzlmYjdmOGI0OTUxZGVlOWJjOGEwMzI3Yjc5MmZiZTMzMm" \
                "I4ODhhYzY3MDE2NGIyNzU3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYzY4NjQwM" \
                "DAwMDAwMWE4MDEwMDAwMDAwMDAwMDAxOTc2YTkxNDY0YTgzOTBiMGIxNjg1ZmNiZjJkNGI0NTcxMThkYzhkYTkyZDU1MzQ4" \
                "OGFjMDAwMDAwMDAiLCAiZmVlIjogNTc2LCAibmV0d29yayI6ICJ0ZXN0bmV0IiwgInR5cGUiOiAiYml0Y29pbl9yZWZ1bmR" \
                "fc2lnbmVkIn0="


def test_bitcoin_cli(cli_tester):
    assert cli_tester.invoke(cli_main,
                             ["bitcoin"]).exit_code == 0

    # Testing bitcoin htlc command.
    htlc = cli_tester.invoke(cli_main,
                             "bitcoin htlc --secret-hash 3a26da82ead15a80533a02696656b14b5dbfd84eb14790"
                             "f2e1be5e9e45820eeb --recipient-address muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB "
                             "--sender-address mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q --sequence 100 "
                             "--network testnet".split(" "))
    assert htlc.exit_code == 0
    assert htlc.output == HTLC_BYTECODE + "\n"

    htlc = cli_tester.invoke(cli_main,
                             "bitcoin htlc --secret-hash 3a26da82ead15a80533a02696656b14b5dbfd84eb14790"
                             "f2e1be5e9e45820eeb --recipient-address 3464563463456346334666666546456gfdfgsdg "
                             "--sender-address mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q --sequence 100 "
                             "--network testnet".split(" "))
    assert htlc.exit_code == 0
    assert htlc.output

    # Testing bitcoin fund command.
    fund = cli_tester.invoke(cli_main,
                             ["bitcoin", "fund", "--sender-address", "mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q",
                              "--amount", 10000, "--bytecode", HTLC_BYTECODE, "--version", 2, "--network", "testnet"])
    assert fund.exit_code == 0
    assert fund.output == "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTg4OGJlN2VjMDY1MDk3ZDk1NjY0NzYzZjI3NmQ0MjU1N" \
                          "TJkNzM1ZmIxZDk3NGFlNzhiZjcyMTA2ZGNhMGYzOTEwMTAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMD" \
                          "AwMDAxN2E5MTQ2ZjA4YjI1NGU0YzU4ZGM2NWY2ZjM5OWMzYmU3MTc3YjkwMWY0YTY2ODdiY2RkMGUwMDAwMDA" \
                          "wMDAwMTk3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYzAwMDAwMDAw" \
                          "IiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiA5ODQ5NDYsICJuIjogMSwgInNjcmlwdCI6ICI3NmE5MTQ2NGE4M" \
                          "zkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldC" \
                          "IsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9" + "\n"

    fund = cli_tester.invoke(cli_main,
                             ["bitcoin", "fund", "--sender-address", 3456346436344456456456,
                              "--amount", 10000, "--bytecode", HTLC_BYTECODE, "--version", 2, "--network", "testnet"])
    assert fund.exit_code == 0
    assert fund.output

    # Testing bitcoin claim command.
    claim = cli_tester.invoke(cli_main,
                              ["bitcoin", "claim", "--transaction", "f7a709ffe08856d7539a155b857913e69e1e6ab4079"
                                                                    "a47d1c4b94eaa38982768",
                               "--recipient-address", "muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB", "--amount", 700,
                               "--version", 2, "--network", "testnet"])
    assert claim.exit_code == 0
    assert claim.output == "eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTY4Mjc5ODM4YWE0ZWI5YzRkMTQ3OWEwN2I0NmExZTllZT" \
                           "YxMzc5ODU1YjE1OWE1M2Q3NTY4OGUwZmYwOWE3ZjcwMDAwMDAwMDAwZmZmZmZmZmYwMTdjMDAwMDAwMDAwMDAw" \
                           "MDAxOTc2YTkxNDk4Zjg3OWZiN2Y4YjQ5NTFkZWU5YmM4YTAzMjdiNzkyZmJlMzMyYjg4OGFjMDAwMDAwMDAiLC" \
                           "Aib3V0cHV0cyI6IFt7ImFtb3VudCI6IDEwMDAsICJuIjogMCwgInNjcmlwdCI6ICJhOTE0ZDJlMmM1ODJlNzRk" \
                           "ZjVmMzdmOWI2NmE1YmYyODZjMzQ2N2M5ZWM2NTg3In1dLCAicmVjaXBpZW50X2FkZHJlc3MiOiAibXVUbmZmTE" \
                           "RSNUx0RmVMUjJpM1dzS1ZmZHl2emZ5UG5WQiIsICJzZW5kZXJfYWRkcmVzcyI6ICJtcUx5ck5EanBFTlJNWkFv" \
                           "RHBzcEg3a1I5UnRndmhXellFIiwgInNlY3JldCI6IG51bGwsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZS" \
                           "I6ICJiaXRjb2luX2NsYWltX3Vuc2lnbmVkIn0=" + "\n"

    claim = cli_tester.invoke(cli_main,
                              ["bitcoin", "claim", "--transaction", "f7a709ffe08856d7539a155b857913e69e1e6ab4079"
                                                                    "a47d1c4b94eaa38982768",
                               "--recipient-address", 253425345345345, "--amount", 700,
                               "--version", 2, "--network", "testnet"])
    assert claim.exit_code == 0
    assert claim.output

    # Testing bitcoin refund command.
    refund = cli_tester.invoke(cli_main,
                               ["bitcoin", "refund", "--transaction", "f7a709ffe08856d7539a155b857913e69e1e6ab4079"
                                                                      "a47d1c4b94eaa38982768",
                                "--recipient-address", "muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB", "--amount", 700,
                                "--version", 2, "--network", "testnet"])
    assert refund.exit_code == 0
    assert refund.output == "eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTY4Mjc5ODM4YWE0ZWI5YzRkMTQ3OWEwN2I0NmExZTllZT" \
                            "YxMzc5ODU1YjE1OWE1M2Q3NTY4OGUwZmYwOWE3ZjcwMDAwMDAwMDAwZmZmZmZmZmYwMTdjMDAwMDAwMDAwMDAw" \
                            "MDAxOTc2YTkxNDZiY2U2NWU1OGE1MGI5Nzk4OTkzMGU5YTRmZjFhYzFhNzc1MTVlZjE4OGFjMDAwMDAwMDAiLC" \
                            "Aib3V0cHV0cyI6IFt7ImFtb3VudCI6IDEwMDAsICJuIjogMCwgInNjcmlwdCI6ICJhOTE0ZDJlMmM1ODJlNzRk" \
                            "ZjVmMzdmOWI2NmE1YmYyODZjMzQ2N2M5ZWM2NTg3In1dLCAicmVjaXBpZW50X2FkZHJlc3MiOiAibXVUbmZmTE" \
                            "RSNUx0RmVMUjJpM1dzS1ZmZHl2emZ5UG5WQiIsICJzZW5kZXJfYWRkcmVzcyI6ICJtcUx5ck5EanBFTlJNWkFv" \
                            "RHBzcEg3a1I5UnRndmhXellFIiwgInNlY3JldCI6IG51bGwsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZS" \
                            "I6ICJiaXRjb2luX3JlZnVuZF91bnNpZ25lZCJ9" + "\n"

    refund = cli_tester.invoke(cli_main,
                               ["bitcoin", "refund", "--transaction", "f7a709ffe08856d7539a155b857913e69e1e6ab4079"
                                                                      "a47d1c4b94eaa38982768",
                                "--recipient-address", 234234234234, "--amount", 700,
                                "--version", 2, "--network", "testnet"])
    assert refund.exit_code == 0
    assert refund.output

    # Testing bitcoin decode command.
    decode = cli_tester.invoke(cli_main,
                               ["bitcoin", "decode", "--raw", FUND_RAW])
    assert decode.exit_code == 0
    assert decode.output != "\n"

    decode = cli_tester.invoke(cli_main,
                               ["bitcoin", "decode", "--raw", "asdfhklajdfhklsjdhfkladsjf"])
    assert decode.exit_code == 0
    assert decode.output

    decode = cli_tester.invoke(cli_main,
                               ["bitcoin", "decode", "--raw", "eyJtZWhlcmV0dA=="])
    assert decode.exit_code == 0
    assert decode.output

    decode = cli_tester.invoke(cli_main,
                               ["bitcoin", "decode", "--raw", "eyJtZWhlcmV0dCI6ICJhc2RmYXNkZmFzZGYifQ=="])
    assert decode.exit_code == 0
    assert decode.output

    # Testing bitcoin sign command.
    fund_sign = cli_tester.invoke(cli_main,
                                  ["bitcoin", "sign", "--raw", FUND_RAW, "--private", PRIVATE_KEY])
    assert fund_sign.exit_code == 0
    assert fund_sign.output == FUND_SIGNED + "\n"

    fund_sign = cli_tester.invoke(cli_main,
                                  ["bitcoin", "sign", "--raw", "eyJtZWhlcmV0dCI6ICJhc2RmYXNkZmFzZGYifQ==", "--private", PRIVATE_KEY])
    assert fund_sign.exit_code == 0
    assert fund_sign.output

    fund_sign = cli_tester.invoke(cli_main,
                                  ["bitcoin", "sign", "--raw", "eyJtZWhlcmV0dA==", "--private", PRIVATE_KEY])
    assert fund_sign.exit_code == 0
    assert fund_sign.output

    # Testing bitcoin sign command.
    claim_sign = cli_tester.invoke(cli_main,
                                   ["bitcoin", "sign", "--raw", CLAIM_RAW, "--private", PRIVATE_KEY])
    assert claim_sign.exit_code == 0
    assert claim_sign.output == CLAIM_SIGNED + "\n"

    claim_sign = cli_tester.invoke(cli_main,
                                   ["bitcoin", "sign", "--raw", "eyJtZWhlcmV0dCI6ICJhc2RmYXNkZmFzZGYifQ==", "--private", PRIVATE_KEY])
    assert claim_sign.exit_code == 0
    assert claim_sign.output

    claim_sign = cli_tester.invoke(cli_main,
                                   ["bitcoin", "sign", "--raw", "eyJtZWhlcmV0dA==", "--private", PRIVATE_KEY])
    assert claim_sign.exit_code == 0
    assert claim_sign.output

    # Testing bitcoin sign command.
    refund_sign = cli_tester.invoke(cli_main,
                                    ["bitcoin", "sign", "--raw", REFUND_RAW, "--private", PRIVATE_KEY])
    assert refund_sign.exit_code == 0
    assert refund_sign.output == REFUND_SIGNED + "\n"

    refund_sign = cli_tester.invoke(cli_main,
                                    ["bitcoin", "sign", "--raw", "eyJtZWhlcmV0dCI6ICJhc2RmYXNkZmFzZGYifQ==", "--private", PRIVATE_KEY])
    assert refund_sign.exit_code == 0
    assert refund_sign.output

    refund_sign = cli_tester.invoke(cli_main,
                                    ["bitcoin", "sign", "--raw", "eyJtZWhlcmV0dA==", "--private", PRIVATE_KEY])
    assert refund_sign.exit_code == 0
    assert refund_sign.output

    # Testing bitcoin submit command.
    submit = cli_tester.invoke(cli_main,
                               ["bitcoin", "submit", "--raw", REFUND_RAW])
    assert submit.exit_code == 0
    assert submit.output == "Error: Missing inputs" + "\n"

    submit = cli_tester.invoke(cli_main,
                               ["bitcoin", "submit", "--raw", "asdfasdfasdfasdfasdfsdfasdf"])
    assert submit.exit_code == 0
    assert submit.output
