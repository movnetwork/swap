#!/usr/bin/env python3

from pybytom.wallet import Wallet as _Wallet

from swap.providers.bytom.wallet import Wallet
from swap.providers.bytom.solver import (
    FundSolver, ClaimSolver, RefundSolver
)
from swap.utils import sha256

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


def test_bytom_fund_solver():

    fund_solver = FundSolver(
        xprivate_key=sender_wallet.xprivate_key()
    )

    assert sender_wallet.xprivate_key() == fund_solver._xprivate_key
    assert isinstance(fund_solver.solve()[0], _Wallet)


def test_bytom_claim_solver():

    htlc_claim_solver = ClaimSolver(
        xprivate_key=recipient_wallet.xprivate_key(),
        secret="Hello Meheret!",
        # Witness from HTLC agreements
        secret_hash=sha256("Hello Meheret!"),
        recipient_public=recipient_wallet.public_key(),
        sender_public=sender_wallet.public_key(),
        sequence=1000
    )

    assert recipient_wallet.xprivate_key() == htlc_claim_solver._xprivate_key
    assert isinstance(htlc_claim_solver.solve()[0], _Wallet)
    assert isinstance(htlc_claim_solver.witness("mainnet"), str)

    bytecode_claim_solver = ClaimSolver(
        xprivate_key=recipient_wallet.xprivate_key(),
        secret="Hello Meheret!",
        # Witness from HTLC bytecode
        bytecode="01642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423"
                 "a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01203a26da82ead15a80533a02696656b14b5dbf"
                 "d84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f697"
                 "2ae7cac00c0"
    )

    assert recipient_wallet.xprivate_key() == bytecode_claim_solver._xprivate_key
    assert isinstance(bytecode_claim_solver.solve()[0], _Wallet)
    assert isinstance(bytecode_claim_solver.witness("testnet"), str)


def test_bytom_refund_solver():

    htlc_refund_solver = RefundSolver(
        xprivate_key=sender_wallet.xprivate_key(),
        # Witness from HTLC agreements
        secret_hash=sha256("Hello Meheret!"),
        recipient_public=recipient_wallet.public_key(),
        sender_public=sender_wallet.public_key(),
        sequence=1000
    )

    assert sender_wallet.xprivate_key() == htlc_refund_solver._xprivate_key
    assert isinstance(htlc_refund_solver.solve()[0], _Wallet)
    assert isinstance(htlc_refund_solver.witness("mainnet"), str)

    bytecode_refund_solver = RefundSolver(
        xprivate_key=sender_wallet.xprivate_key(),
        # Witness from HTLC bytecode
        bytecode="63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a91498f879fb7f8"
                 "b4951dee9bc8a0327b792fbe332b888ac670164b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68"
    )

    assert sender_wallet.xprivate_key() == bytecode_refund_solver._xprivate_key
    assert isinstance(bytecode_refund_solver.solve()[0], _Wallet)
    assert isinstance(bytecode_refund_solver.witness("mainnet"), str)
