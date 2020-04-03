#!/usr/bin/env python3
# coding=utf-8

from shuttle.cli import __main__ as cli_main

PRIVATE_KEY = "92cbbc5990cb5090326a76feeb321cad01048635afe5756523bbf9f7a75bf38b"

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


# Success template
def success(_):
    return "[{}] {}".format("SUCCESS", str(_))


def test_bitcoin_cli(cli_tester):
    assert cli_tester.invoke(cli_main.shuttle,
                             ["bitcoin"]).exit_code == 0

    # Testing bitcoin decode command.
    decode = cli_tester.invoke(cli_main.shuttle,
                               ["bitcoin", "decode", "--raw", FUND_RAW])
    assert decode.exit_code == 0
    assert decode.output != success("DECODE_RESULT") + "\n"

    # Testing bitcoin sign command.
    fund_sign = cli_tester.invoke(cli_main.shuttle,
                                  ["bitcoin", "sign", "--unsigned", FUND_RAW, "--private", PRIVATE_KEY])
    assert fund_sign.exit_code == 0
    assert fund_sign.output == success(FUND_SIGNED) + "\n"

    # Testing bitcoin sign command.
    claim_sign = cli_tester.invoke(cli_main.shuttle,
                                   ["bitcoin", "sign", "--unsigned", CLAIM_RAW, "--private", PRIVATE_KEY])
    assert claim_sign.exit_code == 0
    assert claim_sign.output == success(CLAIM_SIGNED) + "\n"

    # Testing bitcoin sign command.
    refund_sign = cli_tester.invoke(cli_main.shuttle,
                                    ["bitcoin", "sign", "--unsigned", REFUND_RAW, "--private", PRIVATE_KEY])
    assert refund_sign.exit_code == 0
    assert refund_sign.output == success(REFUND_SIGNED) + "\n"

    # Testing bitcoin submit command.
    submit = cli_tester.invoke(cli_main.shuttle,
                               ["bitcoin", "submit", "--raw", REFUND_RAW])
    assert submit.exit_code == 0
    assert submit.output == "[ERROR] Missing inputs" + "\n"
