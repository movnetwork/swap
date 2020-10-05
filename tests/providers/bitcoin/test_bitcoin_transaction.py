#!/usr/bin/env python3

import json
import os

from swap.providers.bitcoin.htlc import HTLC
from swap.providers.bitcoin.transaction import (
    FundTransaction, ClaimTransaction, RefundTransaction
)
from swap.providers.bitcoin.solver import (
    FundSolver, ClaimSolver, RefundSolver
)
from swap.utils import clean_transaction_raw

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_bitcoin_fund_transaction():

    unsigned_fund_transaction = FundTransaction(network=_["bitcoin"]["network"])

    unsigned_fund_transaction.build_transaction(
        address=_["bitcoin"]["wallet"]["sender"]["address"],
        htlc=HTLC(network=_["bitcoin"]["network"]).from_bytecode(
            bytecode=_["bitcoin"]["htlc"]["bytecode"]
        ),
        amount=_["bitcoin"]["amount"]
    )

    assert unsigned_fund_transaction.type() == _["bitcoin"]["fund"]["unsigned"]["type"]
    assert unsigned_fund_transaction.fee() == _["bitcoin"]["fund"]["unsigned"]["fee"]
    assert unsigned_fund_transaction.hash() == _["bitcoin"]["fund"]["unsigned"]["hash"]
    assert unsigned_fund_transaction.raw() == _["bitcoin"]["fund"]["unsigned"]["raw"]
    assert unsigned_fund_transaction.json() == _["bitcoin"]["fund"]["unsigned"]["json"]
    assert unsigned_fund_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bitcoin"]["fund"]["unsigned"]["transaction_raw"]
    )

    signed_fund_transaction = unsigned_fund_transaction.sign(
        solver=FundSolver(
            root_xprivate_key=_["bitcoin"]["wallet"]["sender"]["root_xprivate_key"],
            path=_["bitcoin"]["wallet"]["sender"]["derivation"]["path"],
            account=_["bitcoin"]["wallet"]["sender"]["derivation"]["account"],
            change=_["bitcoin"]["wallet"]["sender"]["derivation"]["change"],
            address=_["bitcoin"]["wallet"]["sender"]["derivation"]["address"]
        )
    )

    assert signed_fund_transaction.type() == _["bitcoin"]["fund"]["signed"]["type"]
    assert signed_fund_transaction.fee() == _["bitcoin"]["fund"]["signed"]["fee"]
    assert signed_fund_transaction.hash() == _["bitcoin"]["fund"]["signed"]["hash"]
    assert signed_fund_transaction.raw() == _["bitcoin"]["fund"]["signed"]["raw"]
    assert signed_fund_transaction.json() == _["bitcoin"]["fund"]["signed"]["json"]
    assert signed_fund_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bitcoin"]["fund"]["signed"]["transaction_raw"]
    )


def test_bitcoin_claim_transaction():

    unsigned_claim_transaction = ClaimTransaction(network=_["bitcoin"]["network"])

    unsigned_claim_transaction.build_transaction(
        transaction_id=_["bitcoin"]["transaction_id"],
        address=_["bitcoin"]["wallet"]["recipient"]["address"],
        amount=_["bitcoin"]["amount"]
    )

    assert unsigned_claim_transaction.type() == _["bitcoin"]["claim"]["unsigned"]["type"]
    assert unsigned_claim_transaction.fee() == _["bitcoin"]["claim"]["unsigned"]["fee"]
    assert unsigned_claim_transaction.hash() == _["bitcoin"]["claim"]["unsigned"]["hash"]
    assert unsigned_claim_transaction.raw() == _["bitcoin"]["claim"]["unsigned"]["raw"]
    assert unsigned_claim_transaction.json() == _["bitcoin"]["claim"]["unsigned"]["json"]
    assert unsigned_claim_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bitcoin"]["claim"]["unsigned"]["transaction_raw"]
    )

    signed_claim_transaction = unsigned_claim_transaction.sign(
        solver=ClaimSolver(
            root_xprivate_key=_["bitcoin"]["wallet"]["recipient"]["root_xprivate_key"],
            secret_key=_["bitcoin"]["htlc"]["secret"]["key"],
            bytecode=_["bitcoin"]["htlc"]["bytecode"],
            path=_["bitcoin"]["wallet"]["recipient"]["derivation"]["path"],
            account=_["bitcoin"]["wallet"]["recipient"]["derivation"]["account"],
            change=_["bitcoin"]["wallet"]["recipient"]["derivation"]["change"],
            address=_["bitcoin"]["wallet"]["recipient"]["derivation"]["address"]
        )
    )

    assert signed_claim_transaction.type() == _["bitcoin"]["claim"]["signed"]["type"]
    assert signed_claim_transaction.fee() == _["bitcoin"]["claim"]["signed"]["fee"]
    assert signed_claim_transaction.hash() == _["bitcoin"]["claim"]["signed"]["hash"]
    assert signed_claim_transaction.raw() == _["bitcoin"]["claim"]["signed"]["raw"]
    assert signed_claim_transaction.json() == _["bitcoin"]["claim"]["signed"]["json"]
    assert signed_claim_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bitcoin"]["claim"]["signed"]["transaction_raw"]
    )


def test_bitcoin_refund_transaction():

    unsigned_refund_transaction = RefundTransaction(network=_["bitcoin"]["network"])

    unsigned_refund_transaction.build_transaction(
        transaction_id=_["bitcoin"]["transaction_id"],
        address=_["bitcoin"]["wallet"]["sender"]["address"],
        amount=_["bitcoin"]["amount"]
    )

    assert unsigned_refund_transaction.type() == _["bitcoin"]["refund"]["unsigned"]["type"]
    assert unsigned_refund_transaction.fee() == _["bitcoin"]["refund"]["unsigned"]["fee"]
    assert unsigned_refund_transaction.hash() == _["bitcoin"]["refund"]["unsigned"]["hash"]
    assert unsigned_refund_transaction.raw() == _["bitcoin"]["refund"]["unsigned"]["raw"]
    assert unsigned_refund_transaction.json() == _["bitcoin"]["refund"]["unsigned"]["json"]
    assert unsigned_refund_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bitcoin"]["refund"]["unsigned"]["transaction_raw"]
    )

    signed_refund_transaction = unsigned_refund_transaction.sign(
        solver=RefundSolver(
            root_xprivate_key=_["bitcoin"]["wallet"]["sender"]["root_xprivate_key"],
            bytecode=_["bitcoin"]["htlc"]["bytecode"],
            sequence=_["bitcoin"]["htlc"]["sequence"],
            path=_["bitcoin"]["wallet"]["sender"]["derivation"]["path"],
            account=_["bitcoin"]["wallet"]["sender"]["derivation"]["account"],
            change=_["bitcoin"]["wallet"]["sender"]["derivation"]["change"],
            address=_["bitcoin"]["wallet"]["sender"]["derivation"]["address"]
        )
    )

    assert signed_refund_transaction.type() == _["bitcoin"]["refund"]["signed"]["type"]
    assert signed_refund_transaction.fee() == _["bitcoin"]["refund"]["signed"]["fee"]
    assert signed_refund_transaction.hash() == _["bitcoin"]["refund"]["signed"]["hash"]
    assert signed_refund_transaction.raw() == _["bitcoin"]["refund"]["signed"]["raw"]
    assert signed_refund_transaction.json() == _["bitcoin"]["refund"]["signed"]["json"]
    assert signed_refund_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bitcoin"]["refund"]["signed"]["transaction_raw"]
    )
