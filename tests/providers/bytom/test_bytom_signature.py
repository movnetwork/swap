#!/usr/bin/env python3

from swap.providers.bytom.wallet import Wallet
from swap.providers.bytom.signature import (
    Signature, FundSignature, ClaimSignature, RefundSignature
)
from swap.providers.bytom.solver import (
    FundSolver, ClaimSolver, RefundSolver
)
from swap.utils import sha256, transaction_raw_cleaner
from swap.utils.exceptions import NetworkError

import pytest
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


def test_bytom_fund_signature():

    unsigned_fund_transaction_raw = TEST_VALUES["bytom"]["fund"]["unsigned"]["unsigned_raw"]

    signature = Signature(network=network).sign(
        unsigned_raw=unsigned_fund_transaction_raw,
        solver=FundSolver(
            xprivate_key=sender_wallet.xprivate_key()
        )
    )

    assert signature.type() == TEST_VALUES["bytom"]["fund"]["signed"]["type"]
    assert signature.fee() == TEST_VALUES["bytom"]["fund"]["signed"]["fee"]
    assert signature.hash() == TEST_VALUES["bytom"]["fund"]["signed"]["hash"]
    assert signature.raw() == TEST_VALUES["bytom"]["fund"]["signed"]["raw"]
    # assert signature.json() == TEST_VALUES["bytom"]["fund"]["signed"]["json"]
    assert signature.unsigned_datas() == TEST_VALUES["bytom"]["fund"]["signed"]["unsigned_datas"]
    assert signature.signatures() == TEST_VALUES["bytom"]["fund"]["signed"]["signatures"]
    assert signature.signed_raw() == transaction_raw_cleaner(
        raw=TEST_VALUES["bytom"]["fund"]["signed"]["signed_raw"]
    )

    fund_signature = FundSignature(network=network).sign(
        unsigned_raw=unsigned_fund_transaction_raw,
        solver=FundSolver(
            xprivate_key=sender_wallet.xprivate_key()
        )
    )

    assert fund_signature.type() == TEST_VALUES["bytom"]["fund"]["signed"]["type"]
    assert fund_signature.fee() == TEST_VALUES["bytom"]["fund"]["signed"]["fee"]
    assert fund_signature.hash() == TEST_VALUES["bytom"]["fund"]["signed"]["hash"]
    assert fund_signature.raw() == TEST_VALUES["bytom"]["fund"]["signed"]["raw"]
    # assert fund_signature.json() == TEST_VALUES["bytom"]["fund"]["signed"]["json"]
    assert fund_signature.unsigned_datas() == TEST_VALUES["bytom"]["fund"]["signed"]["unsigned_datas"]
    assert fund_signature.signatures() == TEST_VALUES["bytom"]["fund"]["signed"]["signatures"]
    assert fund_signature.signed_raw() == transaction_raw_cleaner(
        raw=TEST_VALUES["bytom"]["fund"]["signed"]["signed_raw"]
    )


def test_bytom_claim_signature():

    unsigned_claim_transaction_raw = TEST_VALUES["bytom"]["claim"]["unsigned"]["unsigned_raw"]

    signature = Signature(network=network).sign(
        unsigned_raw=unsigned_claim_transaction_raw,
        solver=ClaimSolver(
            xprivate_key=recipient_wallet.xprivate_key(),
            secret=TEST_VALUES["bytom"]["htlc"]["secret"]["key"],
            secret_hash=TEST_VALUES["bytom"]["htlc"]["secret"]["hash"],
            recipient_public=recipient_wallet.public_key(),
            sender_public=sender_wallet.public_key(),
            sequence=TEST_VALUES["bytom"]["htlc"]["sequence"]
        )
    )

    assert signature.type() == TEST_VALUES["bytom"]["claim"]["signed"]["type"]
    assert signature.fee() == TEST_VALUES["bytom"]["claim"]["signed"]["fee"]
    assert signature.hash() == TEST_VALUES["bytom"]["claim"]["signed"]["hash"]
    assert signature.raw() == TEST_VALUES["bytom"]["claim"]["signed"]["raw"]
    # assert signature.json() == TEST_VALUES["bytom"]["claim"]["signed"]["json"]
    assert signature.unsigned_datas() == TEST_VALUES["bytom"]["claim"]["signed"]["unsigned_datas"]
    assert signature.signatures() == TEST_VALUES["bytom"]["claim"]["signed"]["signatures"]
    assert signature.signed_raw() == transaction_raw_cleaner(
        raw=TEST_VALUES["bytom"]["claim"]["signed"]["signed_raw"]
    )

    claim_signature = ClaimSignature(network=network).sign(
        unsigned_raw=unsigned_claim_transaction_raw,
        solver=ClaimSolver(
            xprivate_key=recipient_wallet.xprivate_key(),
            secret="Hello Meheret!",
            bytecode=TEST_VALUES["bytom"]["htlc"]["bytecode"]
        )
    )

    assert claim_signature.type() == TEST_VALUES["bytom"]["claim"]["signed"]["type"]
    assert claim_signature.fee() == TEST_VALUES["bytom"]["claim"]["signed"]["fee"]
    assert claim_signature.hash() == TEST_VALUES["bytom"]["claim"]["signed"]["hash"]
    assert claim_signature.raw() == TEST_VALUES["bytom"]["claim"]["signed"]["raw"]
    # assert claim_signature.json() == TEST_VALUES["bytom"]["claim"]["signed"]["json"]
    assert claim_signature.unsigned_datas() == TEST_VALUES["bytom"]["claim"]["signed"]["unsigned_datas"]
    assert claim_signature.signatures() == TEST_VALUES["bytom"]["claim"]["signed"]["signatures"]
    assert claim_signature.signed_raw() == transaction_raw_cleaner(
        raw=TEST_VALUES["bytom"]["claim"]["signed"]["signed_raw"]
    )


def test_bytom_refund_signature():

    unsigned_refund_transaction_raw = TEST_VALUES["bytom"]["refund"]["unsigned"]["unsigned_raw"]

    signature = Signature(network=network).sign(
        unsigned_raw=unsigned_refund_transaction_raw,
        solver=RefundSolver(
            xprivate_key=sender_wallet.xprivate_key(),
            secret_hash=TEST_VALUES["bytom"]["htlc"]["secret"]["hash"],
            recipient_public=recipient_wallet.public_key(),
            sender_public=sender_wallet.public_key(),
            sequence=TEST_VALUES["bytom"]["htlc"]["sequence"]
        )
    )

    assert signature.type() == TEST_VALUES["bytom"]["refund"]["signed"]["type"]
    assert signature.fee() == TEST_VALUES["bytom"]["refund"]["signed"]["fee"]
    assert signature.hash() == TEST_VALUES["bytom"]["refund"]["signed"]["hash"]
    assert signature.raw() == TEST_VALUES["bytom"]["refund"]["signed"]["raw"]
    # assert signature.json() == TEST_VALUES["bytom"]["refund"]["signed"]["json"]
    assert signature.unsigned_datas() == TEST_VALUES["bytom"]["refund"]["signed"]["unsigned_datas"]
    assert signature.signatures() == TEST_VALUES["bytom"]["refund"]["signed"]["signatures"]
    assert signature.signed_raw() == transaction_raw_cleaner(
        raw=TEST_VALUES["bytom"]["refund"]["signed"]["signed_raw"]
    )

    refund_signature = RefundSignature(network=network).sign(
        unsigned_raw=unsigned_refund_transaction_raw,
        solver=RefundSolver(
            xprivate_key=sender_wallet.xprivate_key(),
            bytecode=TEST_VALUES["bytom"]["htlc"]["bytecode"]
        )
    )

    assert refund_signature.type() == TEST_VALUES["bytom"]["refund"]["signed"]["type"]
    assert refund_signature.fee() == TEST_VALUES["bytom"]["refund"]["signed"]["fee"]
    assert refund_signature.hash() == TEST_VALUES["bytom"]["refund"]["signed"]["hash"]
    assert refund_signature.raw() == TEST_VALUES["bytom"]["refund"]["signed"]["raw"]
    # assert refund_signature.json() == TEST_VALUES["bytom"]["refund"]["signed"]["json"]
    assert refund_signature.unsigned_datas() == TEST_VALUES["bytom"]["refund"]["signed"]["unsigned_datas"]
    assert refund_signature.signatures() == TEST_VALUES["bytom"]["refund"]["signed"]["signatures"]
    assert refund_signature.signed_raw() == transaction_raw_cleaner(
        raw=TEST_VALUES["bytom"]["refund"]["signed"]["signed_raw"]
    )


def test_signature_exceptions():

    with pytest.raises(NetworkError,
                       match="Invalid 'bytomnet' network/type, choose only 'mainnet', 'solonet' or 'testnet' networks."):
        Signature(network="bytomnet")

    with pytest.raises(ValueError, match="transaction script is none, sign first"):
        Signature().hash()

    with pytest.raises(ValueError, match="transaction script is none, sign first"):
        Signature().json()

    with pytest.raises(ValueError, match="transaction script is none, build transaction first"):
        Signature().raw()

    with pytest.raises(ValueError, match="not found type, sign first"):
        Signature().type()

    with pytest.raises(ValueError, match="transaction script is none, build transaction first"):
        Signature().unsigned_datas()

    with pytest.raises(ValueError, match="there is no signed data, sign first"):
        Signature().signed_raw()

    with pytest.raises(TypeError, match=r"invalid Bytom fund unsigned transaction type, .*"):
        FundSignature().sign(
            unsigned_raw="eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiNTcxNzg0YTgtMDk0NS00ZDc4LWI5NzMtYWFjNGIwOWQ2NDM5IiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbIjZkNzk3OTEyMDk4YTFhNDgyM2ViMzAxMDgwMjgyNjA1NjEyODI1MTY5N2Q1YWNjNjViM2M3MzhiN2ZkZDU3MGQiXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBbIjliNmNlMjM5MjQ1YzVkMjRjZGE5ZTBmYmQ1M2Q0ZWI1YzRhOTJhMDVjZDBlZjkwNmRiY2M0YzNkYzBkZDMxOTAiXSwgInB1YmxpY19rZXkiOiAiM2UwYTM3N2FlNGFmYTAzMWQ0NTUxNTk5ZDliYjdkNWIyN2Y0NzM2ZDc3Zjc4Y2FjNGQ0NzZmMGZmYmE1YWUzZSIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgImhhc2giOiAiYjM4MWMxYmE1YmY1MzA5Y2Y1MTljNTIwMjZhZDBhMjQ0ODA5N2UwM2YwMzdlY2EyNzllOGRiODAxNDYxYmYwYyIsICJyYXciOiAiMDcwMTAwMDIwMTY5MDE2NzAyZTBiMWFkMjEwNzIyMmNmYzEzYWI2YzMzNjVkMzY2YjVkMTNiMTFlNmRjN2UxZTBjYzRhZTU2NzZjZGVlNDRmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOTA0ZTAwMDEyMjAwMjBhNWFkZGI3ZWI1NjQ5ZDEwMDMxMzA0ZWNlNzJkOWNjYzlkYzQyNGFiY2RhODk1ZDkwNGEzMDk3Mjc0MjRlNDBlMDEwMDAxNjAwMTVlMDJlMGIxYWQyMTA3MjIyY2ZjMTNhYjZjMzM2NWQzNjZiNWQxM2IxMWU2ZGM3ZTFlMGNjNGFlNTY3NmNkZWU0NGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmMDk4ODhkODAzMDEwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkyMjAxMjAzZTBhMzc3YWU0YWZhMDMxZDQ1NTE1OTlkOWJiN2Q1YjI3ZjQ3MzZkNzdmNzhjYWM0ZDQ3NmYwZmZiYTVhZTNlMDIwMTNhZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjkwNGUwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkwMDAxM2RmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjBlYmE1ZDMwMzAxMTYwMDE0ODg3ZWU2NmQ4NGE4MmYyZDg2ODI0YTQ1YmI1MWZkZWEwM2M5MmY0OTAwIiwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX3JlZnVuZF91bnNpZ25lZCJ9",
            solver=FundSolver(
                xprivate_key=sender_wallet.xprivate_key()
            )
        )

    with pytest.raises(TypeError, match=r"invalid Bytom claim unsigned transaction type, .*"):
        ClaimSignature().sign(
            unsigned_raw="eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiNTcxNzg0YTgtMDk0NS00ZDc4LWI5NzMtYWFjNGIwOWQ2NDM5IiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbImI1NTgxODRiZDJjNWNmMWQ3YWY5NTIyN2Y4OTk2Nzc3ZDQ2ZDQxMDY5YTgyZjc4YzExYzYxODBhNTMyZWViODUiXSwgInB1YmxpY19rZXkiOiAiM2UwYTM3N2FlNGFmYTAzMWQ0NTUxNTk5ZDliYjdkNWIyN2Y0NzM2ZDc3Zjc4Y2FjNGQ0NzZmMGZmYmE1YWUzZSIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgImhhc2giOiAiODljOTU0NDA0YmRiM2U2MTIzZWQ4YTQxM2ZlM2JkNTI2YmY3YjU1MjkzNmQ4MGZkOGMzN2MyZDdlYWU2ZDBjMCIsICJyYXciOiAiMDcwMTAwMDEwMTYwMDE1ZTAyZTBiMWFkMjEwNzIyMmNmYzEzYWI2YzMzNjVkMzY2YjVkMTNiMTFlNmRjN2UxZTBjYzRhZTU2NzZjZGVlNDRmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjA5ODg4ZDgwMzAxMDExNjAwMTQ4ODdlZTY2ZDg0YTgyZjJkODY4MjRhNDViYjUxZmRlYTAzYzkyZjQ5MjIwMTIwM2UwYTM3N2FlNGFmYTAzMWQ0NTUxNTk5ZDliYjdkNWIyN2Y0NzM2ZDc3Zjc4Y2FjNGQ0NzZmMGZmYmE1YWUzZTAyMDE0NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDEyMjAwMjBhNWFkZGI3ZWI1NjQ5ZDEwMDMxMzA0ZWNlNzJkOWNjYzlkYzQyNGFiY2RhODk1ZDkwNGEzMDk3Mjc0MjRlNDBlMDAwMTNkZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmUwOWRhNWQzMDMwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkwMCIsICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieXRvbV9mdW5kX3Vuc2lnbmVkIn0",
            solver=ClaimSolver(
                xprivate_key=recipient_wallet.xprivate_key(),
                secret="Hello Meheret!",
                secret_hash=sha256("Hello Meheret!"),
                recipient_public=recipient_wallet.public_key(),
                sender_public=sender_wallet.public_key(),
                sequence=1000
            )
        )

    with pytest.raises(TypeError, match=r"invalid Bytom refund unsigned transaction type, .*"):
        RefundSignature().sign(
            unsigned_raw=TEST_VALUES["bytom"]["fund"]["unsigned"]["unsigned_raw"],
            solver=RefundSolver(
                xprivate_key=sender_wallet.xprivate_key(),
                secret_hash=sha256("Hello Meheret!"),
                recipient_public=recipient_wallet.public_key(),
                sender_public=sender_wallet.public_key(),
                sequence=1000
            )
        )

    with pytest.raises(ValueError, match="invalid Bytom unsigned transaction raw"):
        Signature().sign("eyJtIjogImFzZCJ9", "")

    with pytest.raises(ValueError, match="invalid Bytom unsigned fund transaction raw"):
        FundSignature().sign("eyJtIjogImFzZCJ9", "")

    with pytest.raises(ValueError, match="invalid Bytom unsigned claim transaction raw"):
        ClaimSignature().sign("eyJtIjogImFzZCJ9", "")

    with pytest.raises(ValueError, match="invalid Bytom unsigned refund transaction raw"):
        RefundSignature().sign("eyJtIjogImFzZCJ9", "")

    with pytest.raises(TypeError, match="invalid Bytom solver, it's only takes Bytom FundSolver class"):
        FundSignature().sign(
            unsigned_raw=TEST_VALUES["bytom"]["fund"]["unsigned"]["unsigned_raw"],
            solver=RefundSolver(
                xprivate_key=sender_wallet.xprivate_key(),
                secret_hash=sha256("Hello Meheret!"),
                recipient_public=recipient_wallet.public_key(),
                sender_public=sender_wallet.public_key(),
                sequence=1000
            )
        )

    with pytest.raises(TypeError, match="invalid Bytom solver, it's only takes Bytom ClaimSolver class"):
        ClaimSignature().sign(
            unsigned_raw=TEST_VALUES["bytom"]["claim"]["unsigned"]["unsigned_raw"],
            solver=FundSolver(
                xprivate_key=sender_wallet.xprivate_key()
            )
        )

    with pytest.raises(TypeError, match="invalid Bytom solver, it's only takes Bytom RefundSolver class"):
        RefundSignature().sign(
            unsigned_raw=TEST_VALUES["bytom"]["refund"]["unsigned"]["unsigned_raw"],
            solver=ClaimSolver(
                xprivate_key=recipient_wallet.xprivate_key(),
                secret="Hello Meheret!",
                secret_hash=sha256("Hello Meheret!"),
                recipient_public=recipient_wallet.public_key(),
                sender_public=sender_wallet.public_key(),
                sequence=1000
            )
        )
