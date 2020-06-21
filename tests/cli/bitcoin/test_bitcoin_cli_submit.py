#!/usr/bin/env python3

from shuttle.cli.__main__ import main as cli_main


fund_transaction_raw = "eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTUyYzIzZGM2NDU2N2IxY2ZhZjRkNzc2NjBj" \
                       "NzFjNzUxZjkwZTliYTVjMzc0N2ZhYzFkMDA1MTgwOGVhMGQ2NTEwMDAwMDAwMDAwZmZmZmZmZmYw" \
                       "MWE4MDEwMDAwMDAwMDAwMDAxOTc2YTkxNDY0YTgzOTBiMGIxNjg1ZmNiZjJkNGI0NTcxMThkYzhk" \
                       "YTkyZDU1MzQ4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IFt7ImFtb3VudCI6IDUwMDAsICJuIjog" \
                       "MCwgInNjcmlwdCI6ICJhOTE0NDMzZThlZDU5YjlhNjdmMGYxODdjNjNlYjQ1MGIwZDU2ZTI1NmVj" \
                       "Mjg3In1dLCAicmVjaXBpZW50X2FkZHJlc3MiOiAibXVUbmZmTERSNUx0RmVMUjJpM1dzS1ZmZHl2" \
                       "emZ5UG5WQiIsICJzZW5kZXJfYWRkcmVzcyI6ICJtcGhCUFpmMTVjUkZjTDV0VXE2bUNiRTg0WG9i" \
                       "WjF2ZzdRIiwgInNlY3JldCI6ICJIZWxsbyBNZWhlcmV0ISIsICJuZXR3b3JrIjogInRlc3RuZXQi" \
                       "LCAidHlwZSI6ICJiaXRjb2luX3JlZnVuZF91bnNpZ25lZCJ9"


def test_bitcoin_cli_submit(cli_tester):

    submit = cli_tester.invoke(
        cli_main, [
            "bitcoin",
            "submit",
            "--raw", fund_transaction_raw
        ]
    )
    assert submit.exit_code == 0
    assert submit.output == "Error: Missing inputs" + "\n"

    submit = cli_tester.invoke(
        cli_main, [
            "bitcoin",
            "submit",
            "--raw", "asdfasdfasdfasdfasdfsdfasdf"
        ]
    )
    assert submit.exit_code == 0
    assert submit.output == "Error: invalid Bitcoin signed transaction raw" + "\n"
