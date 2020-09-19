#!/usr/bin/env python3

from swap.providers.bytom.wallet import Wallet
from swap.cli.__main__ import main as cli_main
from swap.utils import transaction_raw_cleaner

import json
import os

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
_ = open(file_path, "r")
TEST_VALUES = json.loads(_.read())
_.close()

network: str = TEST_VALUES["bytom"]["network"]
sender_wallet: Wallet = Wallet(network=network).from_mnemonic(
    mnemonic=TEST_VALUES["bytom"]["wallet"]["sender"]["mnemonic"],
    passphrase=TEST_VALUES["bytom"]["wallet"]["recipient"]["passphrase"]
).from_path(
    path=TEST_VALUES["bytom"]["wallet"]["sender"]["path"]
)
recipient_wallet: Wallet = Wallet(network=network).from_mnemonic(
    mnemonic=TEST_VALUES["bytom"]["wallet"]["recipient"]["mnemonic"],
    passphrase=TEST_VALUES["bytom"]["wallet"]["recipient"]["passphrase"]
).from_path(
    path=TEST_VALUES["bytom"]["wallet"]["recipient"]["path"]
)
transaction_id = TEST_VALUES["bytom"]["transaction_id"]
asset = TEST_VALUES["bytom"]["asset"]
amount = TEST_VALUES["bytom"]["amount"]


def test_bytom_cli_signature(cli_tester):

    signed_fund_transaction_raw = cli_tester.invoke(
        cli_main, [
            "bytom",
            "sign",
            "--raw", TEST_VALUES["bytom"]["fund"]["unsigned"]["unsigned_raw"],
            "--xprivate", sender_wallet.xprivate_key()
        ]
    )
    assert signed_fund_transaction_raw.exit_code == 0
    assert signed_fund_transaction_raw.output == transaction_raw_cleaner(
        raw=TEST_VALUES["bytom"]["fund"]["signed"]["signed_raw"]
    ) + "\n"

    signed_claim_transaction_raw = cli_tester.invoke(
        cli_main, [
            "bytom",
            "sign",
            "--raw", TEST_VALUES["bytom"]["claim"]["unsigned"]["unsigned_raw"],
            "--xprivate", recipient_wallet.xprivate_key(),
            "--secret", TEST_VALUES["bytom"]["htlc"]["secret"]["key"],
            "--bytecode", TEST_VALUES["bytom"]["htlc"]["bytecode"]
        ]
    )
    assert signed_claim_transaction_raw.exit_code == 0
    assert signed_claim_transaction_raw.output == transaction_raw_cleaner(
        raw=TEST_VALUES["bytom"]["claim"]["signed"]["signed_raw"]
    ) + "\n"

    signed_claim_transaction_raw = cli_tester.invoke(
        cli_main, [
            "bytom",
            "sign",
            "--raw", TEST_VALUES["bytom"]["claim"]["unsigned"]["unsigned_raw"],
            "--xprivate", recipient_wallet.xprivate_key(),
            # "--secret", TEST_VALUES["bytom"]["htlc"]["secret"]["key"],
            "--bytecode", TEST_VALUES["bytom"]["htlc"]["bytecode"]
        ]
    )
    assert signed_claim_transaction_raw.exit_code == 0
    assert signed_claim_transaction_raw.output == \
        'Error: Secret key is required for claim, use -s or --secret "Hello Meheret!"' + '\n'

    signed_claim_transaction_raw = cli_tester.invoke(
        cli_main, [
            "bytom",
            "sign",
            "--raw", TEST_VALUES["bytom"]["claim"]["unsigned"]["unsigned_raw"],
            "--xprivate", recipient_wallet.xprivate_key(),
            "--secret", TEST_VALUES["bytom"]["htlc"]["secret"]["key"],
            # "--bytecode", htlc_bytecode
        ]
    )
    assert signed_claim_transaction_raw.exit_code == 0
    assert signed_claim_transaction_raw.output == \
        'Error: Witness bytecode is required for claim, use -b or --bytecode "016..."' + '\n'

    signed_refund_transaction_raw = cli_tester.invoke(
        cli_main, [
            "bytom",
            "sign",
            "--raw", TEST_VALUES["bytom"]["refund"]["unsigned"]["unsigned_raw"],
            "--xprivate", sender_wallet.xprivate_key(),
            "--bytecode", TEST_VALUES["bytom"]["htlc"]["bytecode"]
        ]
    )
    assert signed_refund_transaction_raw.exit_code == 0
    assert signed_refund_transaction_raw.output == transaction_raw_cleaner(
        raw=TEST_VALUES["bytom"]["refund"]["signed"]["signed_raw"]
    ) + "\n"

    signed_refund_transaction_raw = cli_tester.invoke(
        cli_main, [
            "bytom",
            "sign",
            "--raw", TEST_VALUES["bytom"]["refund"]["unsigned"]["unsigned_raw"],
            "--xprivate", sender_wallet.xprivate_key(),
            # "--bytecode", TEST_VALUES["bytom"]["htlc"]["bytecode"]
        ]
    )
    assert signed_refund_transaction_raw.exit_code == 0
    assert signed_refund_transaction_raw.output == \
        'Error: Witness bytecode is required for refund, use -b or --bytecode "016..."' + '\n'

    signed = cli_tester.invoke(
        cli_main, [
            "bytom",
            "sign",
            "--raw", "eyJtZWhlcmV0dCI6ICJhc2RmYXNkZmFzZGYifQ==",
            "--xprivate", sender_wallet.xprivate_key()
        ]
    )
    assert signed.exit_code == 0
    assert str(signed.output).startswith("Warning: There is no type & network provided")

    signed = cli_tester.invoke(
        cli_main, [
            "bytom",
            "sign",
            "--raw", "eyJtZWhlcmV0dA==",
            "--xprivate", sender_wallet.xprivate_key()
        ]
    )
    assert signed.exit_code == 0
    assert signed.output == "Error: Invalid Bytom unsigned transaction raw" + "\n"

    signed = cli_tester.invoke(
        cli_main, [
            "bytom",
            "sign",
            "--raw", "eyJtZWhlcmV0dA==",
            "--xprivate", "lakdsjfhalksdjfhskldjhklsdjhfaklsjdhfklj"
        ]
    )
    assert signed.exit_code == 0
    assert signed.output == "Error: Invalid Bytom xprivate key" + "\n"

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
    assert signed.output == "Error: Unknown Bytom unsigned transaction raw type" + "\n"
