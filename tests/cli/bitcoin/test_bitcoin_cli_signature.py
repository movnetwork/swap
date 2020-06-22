#!/usr/bin/env python3

from shuttle.providers.bitcoin.wallet import Wallet
from shuttle.cli.__main__ import main as cli_main


version = 2
network = "testnet"
sender_wallet = Wallet(network=network).from_passphrase("meheret tesfaye batu bayou")
recipient_wallet = Wallet(network=network).from_passphrase("meheret")
transaction_id = "f34eb8e86f7753e681dc44387f7d14ab624b3418498d23f6157b38d8922e31ec"
unsigned_fund_transaction_raw = "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMWVjMzEyZTkyZDgzODdiMTVmNjIzOGQ0OTE" \
                                "4MzQ0YjYyYWIxNDdkN2YzODQ0ZGM4MWU2NTM3NzZmZThiODRlZjMwMTAwMDAwMDAwZmZmZmZmZm" \
                                "YwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQyYmIwMTNjM2U0YmViMDg0MjFkZWRjZjgxNWNiNjVhN" \
                                "WMzODgxNzhiODc1MDhhMGUwMDAwMDAwMDAwMTk3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRi" \
                                "NDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiA" \
                                "5NjM1OTAsICJuIjogMSwgInNjcmlwdCI6ICI3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiND" \
                                "U3MTE4ZGM4ZGE5MmQ1NTM0ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogI" \
                                "mJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"
unsigned_claim_transaction_raw = "eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMWVjMzEyZTkyZDgzODdiMTVmNjIzOGQ0OT" \
                                 "E4MzQ0YjYyYWIxNDdkN2YzODQ0ZGM4MWU2NTM3NzZmZThiODRlZjMwMDAwMDAwMDAwZmZmZmZm" \
                                 "ZmYwMWQwMjQwMDAwMDAwMDAwMDAxOTc2YTkxNDk4Zjg3OWZiN2Y4YjQ5NTFkZWU5YmM4YTAzMj" \
                                 "diNzkyZmJlMzMyYjg4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsiYW1vdW50IjogMTAwMDAs" \
                                 "ICJuIjogMCwgInNjcmlwdCI6ICJhOTE0MmJiMDEzYzNlNGJlYjA4NDIxZGVkY2Y4MTVjYjY1YT" \
                                 "VjMzg4MTc4Yjg3In0sICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX2Ns" \
                                 "YWltX3Vuc2lnbmVkIn0"
unsigned_refund_transaction_raw = "eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMWVjMzEyZTkyZDgzODdiMTVmNjIzOGQ0O" \
                                  "TE4MzQ0YjYyYWIxNDdkN2YzODQ0ZGM4MWU2NTM3NzZmZThiODRlZjMwMDAwMDAwMDAwZmZmZm" \
                                  "ZmZmYwMWQwMjQwMDAwMDAwMDAwMDAxOTc2YTkxNDY0YTgzOTBiMGIxNjg1ZmNiZjJkNGI0NTc" \
                                  "xMThkYzhkYTkyZDU1MzQ4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsidmFsdWUiOiAxMDAw" \
                                  "MCwgIm4iOiAwLCAic2NyaXB0X3B1YmtleSI6ICJhOTE0MmJiMDEzYzNlNGJlYjA4NDIxZGVkY" \
                                  "2Y4MTVjYjY1YTVjMzg4MTc4Yjg3In0sICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6IC" \
                                  "JiaXRjb2luX3JlZnVuZF91bnNpZ25lZCJ9"
htlc_bytecode = "63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a91498f8" \
                "79fb7f8b4951dee9bc8a0327b792fbe332b888ac6702e803b27576a91464a8390b0b1685fcbf2d4b45" \
                "7118dc8da92d553488ac68"
secret = "Hello Meheret!"
sequence = 1000


def test_bitcoin_cli_signature(cli_tester):

    signed_fund_transaction_raw = cli_tester.invoke(
        cli_main, [
            "bitcoin",
            "sign",
            "--raw", unsigned_fund_transaction_raw,
            "--private", sender_wallet.private_key()
        ]
    )
    assert signed_fund_transaction_raw.exit_code == 0
    assert signed_fund_transaction_raw.output == "eyJyYXciOiAiMDIwMDAwMDAwMWVjMzEyZTkyZDgzODdiMTVmNjIzOGQ0OT" \
                                                 "E4MzQ0YjYyYWIxNDdkN2YzODQ0ZGM4MWU2NTM3NzZmZThiODRlZjMwMTAw" \
                                                 "MDAwMDZiNDgzMDQ1MDIyMTAwYjRkNGRlNGMxMGJlYzM4MGE5ZjA3MDE5ZD" \
                                                 "UyMzJhOWFmOWYwYzIzMjFlNWVmY2YzM2Y1MzI2YTYwMzc4MTQ0NTAyMjAz" \
                                                 "ZTFhYjJkZGFhYzhhZmFkZTEzMjgzMmU3MTVmMDU1Zjk1NmQzZTczMGI5ZD" \
                                                 "AzNWE0ZTk5ZWM5ZGZkYzdhY2ZkMDEyMTAzYzU2YTYwMDVkNGE4ODkyZDI4" \
                                                 "Y2MzZjcyNjVlNTY4NWI1NDg2MjdkNTkxMDg5NzNlNDc0YzRlMjZmNjlhNG" \
                                                 "M4NGZmZmZmZmZmMDIxMDI3MDAwMDAwMDAwMDAwMTdhOTE0MmJiMDEzYzNl" \
                                                 "NGJlYjA4NDIxZGVkY2Y4MTVjYjY1YTVjMzg4MTc4Yjg3NTA4YTBlMDAwMD" \
                                                 "AwMDAwMDE5NzZhOTE0NjRhODM5MGIwYjE2ODVmY2JmMmQ0YjQ1NzExOGRj" \
                                                 "OGRhOTJkNTUzNDg4YWMwMDAwMDAwMCIsICJmZWUiOiA2NzgsICJuZXR3b3" \
                                                 "JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfc2lnbmVk" \
                                                 "In0=" + "\n"

    signed_claim_transaction_raw = cli_tester.invoke(
        cli_main, [
            "bitcoin",
            "sign",
            "--raw", unsigned_claim_transaction_raw,
            "--private", recipient_wallet.private_key(),
            "--secret", secret,
            "--bytecode", htlc_bytecode
        ]
    )
    assert signed_claim_transaction_raw.exit_code == 0
    assert signed_claim_transaction_raw.output == "eyJyYXciOiAiMDIwMDAwMDAwMWVjMzEyZTkyZDgzODdiMTVmNjIzOGQ0O" \
                                                  "TE4MzQ0YjYyYWIxNDdkN2YzODQ0ZGM4MWU2NTM3NzZmZThiODRlZjMwMD" \
                                                  "AwMDAwMGQ5NDczMDQ0MDIyMDYwMjkxYjVhODc0NzRmNzc1ZGRhNWMyNDR" \
                                                  "iMjFmYzI3MTZiZmEwOWM0NjM2ZWE0YzcwNzkxOGM5Zjc1OTM3NGUwMjIw" \
                                                  "MWVmNWU3NjhhZjEwZDAxYTEwMzEyOTRlOTUyZjZhOGVkNWMwYTc1ZTIzZ" \
                                                  "jU4YWVlMDYyYTg5ZmVkMjEzNGFmNzAxMjEwMzkyMTNlYmNhZWZkZDNlMT" \
                                                  "A5NzIwYzE3ODY3Y2UxYmQ2ZDA3NmIwZTY1ZTNiNjM5MGU2ZTM4NTQ4YTY" \
                                                  "1ZTc2YWYwZTQ4NjU2YzZjNmYyMDRkNjU2ODY1NzI2NTc0MjE1MTRjNWQ2" \
                                                  "M2FhMjA4MjExMjRiNTU0ZDEzZjI0N2IxZTVkMTBiODRlNDRmYjEyOTZmM" \
                                                  "ThmMzhiYmFhMWJlYTM0YTEyYzg0M2UwMTU4ODg3NmE5MTQ5OGY4NzlmYj" \
                                                  "dmOGI0OTUxZGVlOWJjOGEwMzI3Yjc5MmZiZTMzMmI4ODhhYzY3MDJlODA" \
                                                  "zYjI3NTc2YTkxNDY0YTgzOTBiMGIxNjg1ZmNiZjJkNGI0NTcxMThkYzhk" \
                                                  "YTkyZDU1MzQ4OGFjNjhmZmZmZmZmZjAxZDAyNDAwMDAwMDAwMDAwMDE5N" \
                                                  "zZhOTE0OThmODc5ZmI3ZjhiNDk1MWRlZTliYzhhMDMyN2I3OTJmYmUzMz" \
                                                  "JiODg4YWMwMDAwMDAwMCIsICJmZWUiOiA1NzYsICJuZXR3b3JrIjogInR" \
                                                  "lc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX2NsYWltX3NpZ25lZCJ9" + "\n"

    signed_claim_transaction_raw = cli_tester.invoke(
        cli_main, [
            "bitcoin",
            "sign",
            "--raw", unsigned_claim_transaction_raw,
            "--private", recipient_wallet.private_key(),
            # "--secret", secret,
            "--bytecode", htlc_bytecode
        ]
    )
    assert signed_claim_transaction_raw.exit_code == 0
    assert signed_claim_transaction_raw.output == \
        'Error: secret key is required for claim, use -s or --secret "Hello Meheret!"' + '\n'

    signed_claim_transaction_raw = cli_tester.invoke(
        cli_main, [
            "bitcoin",
            "sign",
            "--raw", unsigned_claim_transaction_raw,
            "--private", recipient_wallet.private_key(),
            "--secret", secret,
            # "--bytecode", htlc_bytecode
        ]
    )
    assert signed_claim_transaction_raw.exit_code == 0
    assert signed_claim_transaction_raw.output == \
        'Error: witness bytecode is required for claim, use -b or --bytecode "016..."' + '\n'

    signed_refund_transaction_raw = cli_tester.invoke(
        cli_main, [
            "bitcoin",
            "sign",
            "--raw", unsigned_refund_transaction_raw,
            "--private", sender_wallet.private_key(),
            "--sequence", sequence,
            "--bytecode", htlc_bytecode
        ]
    )
    assert signed_refund_transaction_raw.exit_code == 0
    assert signed_refund_transaction_raw.output == "eyJyYXciOiAiMDIwMDAwMDAwMWVjMzEyZTkyZDgzODdiMTVmNjIzOGQ0" \
                                                   "OTE4MzQ0YjYyYWIxNDdkN2YzODQ0ZGM4MWU2NTM3NzZmZThiODRlZjMw" \
                                                   "MDAwMDAwMGNhNDczMDQ0MDIyMDBiMGZjM2IzYjg5MTc2MWU1Y2JlZTVi" \
                                                   "YzFmM2M2ZDdiMDkwNGMxMzQ3NWVlZjViNzk2NWM5YmZkYTFkMDhhMmEw" \
                                                   "MjIwNWViZGM3MmNiNzYzYTJlN2YyOTA3ODdiOGQ3ZGVmZDk3MmI0MWEy" \
                                                   "YjRkYzFjNDk5ZDY5OTkxZjBlNDUwNjY1OTAxMjEwM2M1NmE2MDA1ZDRh" \
                                                   "ODg5MmQyOGNjM2Y3MjY1ZTU2ODViNTQ4NjI3ZDU5MTA4OTczZTQ3NGM0" \
                                                   "ZTI2ZjY5YTRjODQwMDRjNWQ2M2FhMjA4MjExMjRiNTU0ZDEzZjI0N2Ix" \
                                                   "ZTVkMTBiODRlNDRmYjEyOTZmMThmMzhiYmFhMWJlYTM0YTEyYzg0M2Uw" \
                                                   "MTU4ODg3NmE5MTQ5OGY4NzlmYjdmOGI0OTUxZGVlOWJjOGEwMzI3Yjc5" \
                                                   "MmZiZTMzMmI4ODhhYzY3MDJlODAzYjI3NTc2YTkxNDY0YTgzOTBiMGIx" \
                                                   "Njg1ZmNiZjJkNGI0NTcxMThkYzhkYTkyZDU1MzQ4OGFjNjhlODAzMDAw" \
                                                   "MDAxZDAyNDAwMDAwMDAwMDAwMDE5NzZhOTE0NjRhODM5MGIwYjE2ODVm" \
                                                   "Y2JmMmQ0YjQ1NzExOGRjOGRhOTJkNTUzNDg4YWMwMDAwMDAwMCIsICJm" \
                                                   "ZWUiOiA1NzYsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJi" \
                                                   "aXRjb2luX3JlZnVuZF9zaWduZWQifQ==" + "\n"

    signed_refund_transaction_raw = cli_tester.invoke(
        cli_main, [
            "bitcoin",
            "sign",
            "--raw", unsigned_refund_transaction_raw,
            "--private", sender_wallet.private_key(),
            "--sequence", sequence,
            # "--bytecode", htlc_bytecode
        ]
    )
    assert signed_refund_transaction_raw.exit_code == 0
    assert signed_refund_transaction_raw.output == \
        'Error: witness bytecode is required for refund, use -b or --bytecode "016..."' + '\n'

    signed = cli_tester.invoke(
        cli_main, [
            "bitcoin",
            "sign",
            "--raw", "eyJtZWhlcmV0dCI6ICJhc2RmYXNkZmFzZGYifQ==",
            "--private", sender_wallet.private_key()
        ]
    )
    assert signed.exit_code == 0
    assert str(signed.output).startswith("Warning: there is no type & network provided")

    signed = cli_tester.invoke(
        cli_main, [
            "bitcoin",
            "sign",
            "--raw", "eyJtZWhlcmV0dA==",
            "--private", sender_wallet.private_key()
        ]
    )
    assert signed.exit_code == 0
    assert signed.output == "Error: invalid Bitcoin unsigned transaction raw" + "\n"

    signed = cli_tester.invoke(
        cli_main, [
            "bitcoin",
            "sign",
            "--raw", "eyJtZWhlcmV0dA==",
            "--private", "lakdsjfhalksdjfhskldjhklsdjhfaklsjdhfklj"
        ]
    )
    assert signed.exit_code == 0
    assert signed.output == "Error: invalid Bitcoin private key" + "\n"

    signed = cli_tester.invoke(
        cli_main, [
            "bitcoin",
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
            "--private", sender_wallet.private_key()
        ]
    )
    assert signed.exit_code == 0
    assert signed.output == "Error: unknown Bitcoin unsigned transaction raw type" + "\n"
