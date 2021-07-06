#!/usr/bin/env python3

import json
import os

from swap.providers.bitcoin.htlc import HTLC
from swap.providers.bitcoin.transaction import (
    FundTransaction, WithdrawTransaction, RefundTransaction
)
from swap.providers.bitcoin.solver import (
    FundSolver, WithdrawSolver, RefundSolver
)
from swap.utils import clean_transaction_raw

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_bitcoin_fund_transaction():

    htlc = HTLC(network=_["bitcoin"]["network"]).build_htlc(
        secret_hash=_["bitcoin"]["htlc"]["secret"]["hash"],
        recipient_address=_["bitcoin"]["wallet"]["recipient"]["address"],
        sender_address=_["bitcoin"]["wallet"]["sender"]["address"],
        endtime=_["bitcoin"]["htlc"]["endtime"]
    )

    unsigned_fund_transaction = FundTransaction(network=_["bitcoin"]["network"])

    unsigned_fund_transaction.build_transaction(
        address=_["bitcoin"]["wallet"]["sender"]["address"],
        htlc=htlc,
        amount=_["bitcoin"]["amount"],
        unit=_["bitcoin"]["unit"]
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
            xprivate_key=_["bitcoin"]["wallet"]["sender"]["root_xprivate_key"],
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


def test_bitcoin_withdraw_transaction():

    unsigned_withdraw_transaction = WithdrawTransaction(network=_["bitcoin"]["network"])

    unsigned_withdraw_transaction.build_transaction(
        address=_["bitcoin"]["wallet"]["recipient"]["address"],
        transaction_hash=_["bitcoin"]["transaction_hash"]
    )

    assert unsigned_withdraw_transaction.type() == _["bitcoin"]["withdraw"]["unsigned"]["type"]
    assert unsigned_withdraw_transaction.fee() == _["bitcoin"]["withdraw"]["unsigned"]["fee"]
    assert unsigned_withdraw_transaction.hash() == _["bitcoin"]["withdraw"]["unsigned"]["hash"]
    assert unsigned_withdraw_transaction.raw() == _["bitcoin"]["withdraw"]["unsigned"]["raw"]
    assert unsigned_withdraw_transaction.json() == _["bitcoin"]["withdraw"]["unsigned"]["json"]
    assert unsigned_withdraw_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bitcoin"]["withdraw"]["unsigned"]["transaction_raw"]
    )

    signed_withdraw_transaction = unsigned_withdraw_transaction.sign(
        solver=WithdrawSolver(
            xprivate_key=_["bitcoin"]["wallet"]["recipient"]["root_xprivate_key"],
            secret_key=_["bitcoin"]["htlc"]["secret"]["key"],
            bytecode=_["bitcoin"]["htlc"]["bytecode"],
            path=_["bitcoin"]["wallet"]["recipient"]["derivation"]["path"],
            account=_["bitcoin"]["wallet"]["recipient"]["derivation"]["account"],
            change=_["bitcoin"]["wallet"]["recipient"]["derivation"]["change"],
            address=_["bitcoin"]["wallet"]["recipient"]["derivation"]["address"]
        )
    )

    assert signed_withdraw_transaction.type() == _["bitcoin"]["withdraw"]["signed"]["type"]
    assert signed_withdraw_transaction.fee() == _["bitcoin"]["withdraw"]["signed"]["fee"]
    assert signed_withdraw_transaction.hash() == _["bitcoin"]["withdraw"]["signed"]["hash"]
    assert signed_withdraw_transaction.raw() == _["bitcoin"]["withdraw"]["signed"]["raw"]
    assert signed_withdraw_transaction.json() == _["bitcoin"]["withdraw"]["signed"]["json"]
    assert signed_withdraw_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bitcoin"]["withdraw"]["signed"]["transaction_raw"]
    )


def test_bitcoin_refund_transaction():

    unsigned_refund_transaction = RefundTransaction(network=_["bitcoin"]["network"])

    unsigned_refund_transaction.build_transaction(
        address=_["bitcoin"]["wallet"]["sender"]["address"],
        transaction_hash=_["bitcoin"]["transaction_hash"]
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
            xprivate_key=_["bitcoin"]["wallet"]["sender"]["root_xprivate_key"],
            bytecode=_["bitcoin"]["htlc"]["bytecode"],
            endtime=_["bitcoin"]["htlc"]["endtime"],
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
