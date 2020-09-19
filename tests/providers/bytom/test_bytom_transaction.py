#!/usr/bin/env python3

from swap.providers.bytom.wallet import Wallet
from swap.providers.bytom.htlc import HTLC
from swap.providers.bytom.transaction import (
    FundTransaction, ClaimTransaction, RefundTransaction
)
from swap.providers.bytom.solver import (
    FundSolver, ClaimSolver, RefundSolver
)
from swap.utils import transaction_raw_cleaner

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
transaction_id = TEST_VALUES["bytom"]["transaction_id"]
asset = TEST_VALUES["bytom"]["asset"]
amount = TEST_VALUES["bytom"]["amount"]


def test_bytom_fund_transaction():

    unsigned_transaction = FundTransaction(network=network)

    unsigned_transaction.build_transaction(
        address=sender_wallet.address(),
        htlc=HTLC(network=network).from_bytecode(
            bytecode=TEST_VALUES["bytom"]["htlc"]["bytecode"]
        ),
        amount=amount,
        asset=asset
    )

    assert unsigned_transaction.type() == TEST_VALUES["bytom"]["fund"]["unsigned"]["type"]
    assert unsigned_transaction.fee() == TEST_VALUES["bytom"]["fund"]["unsigned"]["fee"]
    assert unsigned_transaction.hash() == TEST_VALUES["bytom"]["fund"]["unsigned"]["hash"]
    assert unsigned_transaction.raw() == TEST_VALUES["bytom"]["fund"]["unsigned"]["raw"]
    # assert unsigned_transaction.json() == TEST_VALUES["bytom"]["fund"]["unsigned"]["json"]
    assert unsigned_transaction.unsigned_datas() == TEST_VALUES["bytom"]["fund"]["unsigned"]["unsigned_datas"]
    assert unsigned_transaction.signatures() == TEST_VALUES["bytom"]["fund"]["unsigned"]["signatures"]
    assert unsigned_transaction.unsigned_raw() == transaction_raw_cleaner(
        raw=TEST_VALUES["bytom"]["fund"]["unsigned"]["unsigned_raw"]
    )

    signed_transaction = unsigned_transaction.sign(
        solver=FundSolver(
            xprivate_key=sender_wallet.xprivate_key(),
            path=TEST_VALUES["bytom"]["wallet"]["sender"]["path"]
        )
    )

    assert signed_transaction.type() == TEST_VALUES["bytom"]["fund"]["signed"]["type"]
    assert signed_transaction.fee() == TEST_VALUES["bytom"]["fund"]["signed"]["fee"]
    assert signed_transaction.hash() == TEST_VALUES["bytom"]["fund"]["signed"]["hash"]
    assert signed_transaction.raw() == TEST_VALUES["bytom"]["fund"]["signed"]["raw"]
    # assert signed_transaction.json() == TEST_VALUES["bytom"]["fund"]["signed"]["json"]
    assert signed_transaction.unsigned_datas() == TEST_VALUES["bytom"]["fund"]["signed"]["unsigned_datas"]
    assert signed_transaction.signatures() == TEST_VALUES["bytom"]["fund"]["signed"]["signatures"]
    assert signed_transaction.unsigned_raw() == transaction_raw_cleaner(
        raw=TEST_VALUES["bytom"]["fund"]["signed"]["unsigned_raw"]
    )


def test_bytom_claim_transaction():

    unsigned_transaction = ClaimTransaction(network=network)

    unsigned_transaction.build_transaction(
        transaction_id=transaction_id,
        address=recipient_wallet.address(),
        amount=amount,
        asset=asset
    )

    assert unsigned_transaction.type() == TEST_VALUES["bytom"]["claim"]["unsigned"]["type"]
    assert unsigned_transaction.fee() == TEST_VALUES["bytom"]["claim"]["unsigned"]["fee"]
    assert unsigned_transaction.hash() == TEST_VALUES["bytom"]["claim"]["unsigned"]["hash"]
    assert unsigned_transaction.raw() == TEST_VALUES["bytom"]["claim"]["unsigned"]["raw"]
    # assert unsigned_transaction.json() == TEST_VALUES["bytom"]["claim"]["unsigned"]["json"]
    assert unsigned_transaction.unsigned_datas() == TEST_VALUES["bytom"]["claim"]["unsigned"]["unsigned_datas"]
    assert unsigned_transaction.signatures() == TEST_VALUES["bytom"]["claim"]["unsigned"]["signatures"]
    assert unsigned_transaction.unsigned_raw() == transaction_raw_cleaner(
        raw=TEST_VALUES["bytom"]["claim"]["unsigned"]["unsigned_raw"]
    )

    signed_transaction = unsigned_transaction.sign(
        solver=ClaimSolver(
            xprivate_key=recipient_wallet.xprivate_key(),
            secret=TEST_VALUES["bytom"]["htlc"]["secret"]["key"],
            secret_hash=TEST_VALUES["bytom"]["htlc"]["secret"]["hash"],
            recipient_public=recipient_wallet.public_key(),
            sender_public=sender_wallet.public_key(),
            sequence=TEST_VALUES["bytom"]["htlc"]["sequence"]
        )
    )

    assert signed_transaction.type() == TEST_VALUES["bytom"]["claim"]["signed"]["type"]
    assert signed_transaction.fee() == TEST_VALUES["bytom"]["claim"]["signed"]["fee"]
    assert signed_transaction.hash() == TEST_VALUES["bytom"]["claim"]["signed"]["hash"]
    assert signed_transaction.raw() == TEST_VALUES["bytom"]["claim"]["signed"]["raw"]
    # assert signed_transaction.json() == TEST_VALUES["bytom"]["claim"]["signed"]["json"]
    assert signed_transaction.unsigned_datas() == TEST_VALUES["bytom"]["claim"]["signed"]["unsigned_datas"]
    assert signed_transaction.signatures() == TEST_VALUES["bytom"]["claim"]["signed"]["signatures"]
    assert signed_transaction.unsigned_raw() == transaction_raw_cleaner(
        raw=TEST_VALUES["bytom"]["claim"]["signed"]["unsigned_raw"]
    )


def test_bytom_refund_transaction():

    unsigned_transaction = RefundTransaction(network=network)

    unsigned_transaction.build_transaction(
        transaction_id=transaction_id,
        address=sender_wallet.address(),
        amount=amount,
        asset=asset
    )

    assert unsigned_transaction.type() == TEST_VALUES["bytom"]["refund"]["unsigned"]["type"]
    assert unsigned_transaction.fee() == TEST_VALUES["bytom"]["refund"]["unsigned"]["fee"]
    assert unsigned_transaction.hash() == TEST_VALUES["bytom"]["refund"]["unsigned"]["hash"]
    assert unsigned_transaction.raw() == TEST_VALUES["bytom"]["refund"]["unsigned"]["raw"]
    # assert unsigned_transaction.json() == TEST_VALUES["bytom"]["refund"]["unsigned"]["json"]
    assert unsigned_transaction.unsigned_datas() == TEST_VALUES["bytom"]["refund"]["unsigned"]["unsigned_datas"]
    assert unsigned_transaction.signatures() == TEST_VALUES["bytom"]["refund"]["unsigned"]["signatures"]
    assert unsigned_transaction.unsigned_raw() == transaction_raw_cleaner(
        raw=TEST_VALUES["bytom"]["refund"]["unsigned"]["unsigned_raw"]
    )

    signed_transaction = unsigned_transaction.sign(
        solver=RefundSolver(
            xprivate_key=sender_wallet.xprivate_key(),
            bytecode=TEST_VALUES["bytom"]["htlc"]["bytecode"]
        )
    )

    assert signed_transaction.type() == TEST_VALUES["bytom"]["refund"]["signed"]["type"]
    assert signed_transaction.fee() == TEST_VALUES["bytom"]["refund"]["signed"]["fee"]
    assert signed_transaction.hash() == TEST_VALUES["bytom"]["refund"]["signed"]["hash"]
    assert signed_transaction.raw() == TEST_VALUES["bytom"]["refund"]["signed"]["raw"]
    # assert signed_transaction.json() == TEST_VALUES["bytom"]["refund"]["signed"]["json"]
    assert signed_transaction.unsigned_datas() == TEST_VALUES["bytom"]["refund"]["signed"]["unsigned_datas"]
    assert signed_transaction.signatures() == TEST_VALUES["bytom"]["refund"]["signed"]["signatures"]
    assert signed_transaction.unsigned_raw() == transaction_raw_cleaner(
        raw=TEST_VALUES["bytom"]["refund"]["signed"]["unsigned_raw"]
    )
