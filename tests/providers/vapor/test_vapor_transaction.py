#!/usr/bin/env python3

import json
import os

from swap.providers.vapor.htlc import HTLC
from swap.providers.vapor.transaction import (
    FundTransaction, WithdrawTransaction, RefundTransaction
)
from swap.providers.vapor.solver import (
    FundSolver, WithdrawSolver, RefundSolver
)
from swap.providers.vapor.utils import amount_unit_converter
from swap.utils import clean_transaction_raw

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_vapor_fund_transaction():

    htlc = HTLC(network=_["vapor"]["network"]).build_htlc(
        secret_hash=_["vapor"]["htlc"]["secret"]["hash"],
        recipient_public_key=_["vapor"]["wallet"]["recipient"]["public_key"],
        sender_public_key=_["vapor"]["wallet"]["sender"]["public_key"],
        endblock=_["vapor"]["htlc"]["endblock"]
    )

    unsigned_fund_transaction = FundTransaction(network=_["vapor"]["network"])

    unsigned_fund_transaction.build_transaction(
        address=_["vapor"]["wallet"]["sender"]["address"],
        htlc=htlc,
        asset=_["vapor"]["asset"],
        amount=_["vapor"]["amount"],
        unit=_["vapor"]["unit"]
    )

    assert unsigned_fund_transaction.type() == _["vapor"]["fund"]["unsigned"]["type"]
    assert unsigned_fund_transaction.fee() == _["vapor"]["fund"]["unsigned"]["fee"]
    assert unsigned_fund_transaction.hash() == _["vapor"]["fund"]["unsigned"]["hash"]
    assert unsigned_fund_transaction.raw() == _["vapor"]["fund"]["unsigned"]["raw"]
    # assert unsigned_fund_transaction.json() == _["vapor"]["fund"]["unsigned"]["json"]
    assert unsigned_fund_transaction.unsigned_datas() == _["vapor"]["fund"]["unsigned"]["unsigned_datas"]
    assert unsigned_fund_transaction.signatures() == _["vapor"]["fund"]["unsigned"]["signatures"]
    assert unsigned_fund_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["vapor"]["fund"]["unsigned"]["transaction_raw"]
    )

    signed_fund_transaction = unsigned_fund_transaction.sign(
        solver=FundSolver(
            xprivate_key=_["vapor"]["wallet"]["sender"]["xprivate_key"],
            path=_["vapor"]["wallet"]["sender"]["derivation"]["path"],
            account=_["vapor"]["wallet"]["sender"]["derivation"]["account"],
            change=_["vapor"]["wallet"]["sender"]["derivation"]["change"],
            address=_["vapor"]["wallet"]["sender"]["derivation"]["address"]
        )
    )

    assert signed_fund_transaction.type() == _["vapor"]["fund"]["signed"]["type"]
    assert signed_fund_transaction.fee() == _["vapor"]["fund"]["signed"]["fee"]
    assert signed_fund_transaction.hash() == _["vapor"]["fund"]["signed"]["hash"]
    assert signed_fund_transaction.raw() == _["vapor"]["fund"]["signed"]["raw"]
    # assert signed_fund_transaction.json() == _["vapor"]["fund"]["signed"]["json"]
    assert signed_fund_transaction.unsigned_datas() == _["vapor"]["fund"]["signed"]["unsigned_datas"]
    assert signed_fund_transaction.signatures() == _["vapor"]["fund"]["signed"]["signatures"]
    assert signed_fund_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["vapor"]["fund"]["signed"]["transaction_raw"]
    )


def test_vapor_withdraw_transaction():

    unsigned_withdraw_transaction = WithdrawTransaction(network=_["vapor"]["network"])

    unsigned_withdraw_transaction.build_transaction(
        address=_["vapor"]["wallet"]["recipient"]["address"],
        transaction_hash=_["vapor"]["transaction_hash"],
        asset=_["vapor"]["asset"]
    )

    assert unsigned_withdraw_transaction.type() == _["vapor"]["withdraw"]["unsigned"]["type"]
    assert unsigned_withdraw_transaction.fee() == _["vapor"]["withdraw"]["unsigned"]["fee"]
    assert unsigned_withdraw_transaction.hash() == _["vapor"]["withdraw"]["unsigned"]["hash"]
    assert unsigned_withdraw_transaction.raw() == _["vapor"]["withdraw"]["unsigned"]["raw"]
    # assert unsigned_withdraw_transaction.json() == _["vapor"]["withdraw"]["unsigned"]["json"]
    assert unsigned_withdraw_transaction.unsigned_datas() == _["vapor"]["withdraw"]["unsigned"]["unsigned_datas"]
    assert unsigned_withdraw_transaction.signatures() == _["vapor"]["withdraw"]["unsigned"]["signatures"]
    assert unsigned_withdraw_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["vapor"]["withdraw"]["unsigned"]["transaction_raw"]
    )

    signed_withdraw_transaction = unsigned_withdraw_transaction.sign(
        solver=WithdrawSolver(
            xprivate_key=_["vapor"]["wallet"]["recipient"]["xprivate_key"],
            secret_key=_["vapor"]["htlc"]["secret"]["key"],
            bytecode=_["vapor"]["htlc"]["bytecode"],
            path=_["vapor"]["wallet"]["recipient"]["derivation"]["path"],
            account=_["vapor"]["wallet"]["recipient"]["derivation"]["account"],
            change=_["vapor"]["wallet"]["recipient"]["derivation"]["change"],
            address=_["vapor"]["wallet"]["recipient"]["derivation"]["address"]
        )
    )

    assert signed_withdraw_transaction.type() == _["vapor"]["withdraw"]["signed"]["type"]
    assert signed_withdraw_transaction.fee() == _["vapor"]["withdraw"]["signed"]["fee"]
    assert signed_withdraw_transaction.hash() == _["vapor"]["withdraw"]["signed"]["hash"]
    assert signed_withdraw_transaction.raw() == _["vapor"]["withdraw"]["signed"]["raw"]
    # assert signed_withdraw_transaction.json() == _["vapor"]["withdraw"]["signed"]["json"]
    assert signed_withdraw_transaction.unsigned_datas() == _["vapor"]["withdraw"]["signed"]["unsigned_datas"]
    assert signed_withdraw_transaction.signatures() == _["vapor"]["withdraw"]["signed"]["signatures"]
    assert signed_withdraw_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["vapor"]["withdraw"]["signed"]["transaction_raw"]
    )


def test_vapor_refund_transaction():

    unsigned_refund_transaction = RefundTransaction(network=_["vapor"]["network"])

    unsigned_refund_transaction.build_transaction(
        address=_["vapor"]["wallet"]["sender"]["address"],
        transaction_hash=_["vapor"]["transaction_hash"],
        asset=_["vapor"]["asset"]
    )

    assert unsigned_refund_transaction.type() == _["vapor"]["refund"]["unsigned"]["type"]
    assert unsigned_refund_transaction.fee() == _["vapor"]["refund"]["unsigned"]["fee"]
    assert unsigned_refund_transaction.hash() == _["vapor"]["refund"]["unsigned"]["hash"]
    assert unsigned_refund_transaction.raw() == _["vapor"]["refund"]["unsigned"]["raw"]
    # assert unsigned_refund_transaction.json() == _["vapor"]["refund"]["unsigned"]["json"]
    assert unsigned_refund_transaction.unsigned_datas() == _["vapor"]["refund"]["unsigned"]["unsigned_datas"]
    assert unsigned_refund_transaction.signatures() == _["vapor"]["refund"]["unsigned"]["signatures"]
    assert unsigned_refund_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["vapor"]["refund"]["unsigned"]["transaction_raw"]
    )

    signed_refund_transaction = unsigned_refund_transaction.sign(
        solver=RefundSolver(
            xprivate_key=_["vapor"]["wallet"]["sender"]["xprivate_key"],
            bytecode=_["vapor"]["htlc"]["bytecode"],
            path=_["vapor"]["wallet"]["sender"]["derivation"]["path"],
            account=_["vapor"]["wallet"]["sender"]["derivation"]["account"],
            change=_["vapor"]["wallet"]["sender"]["derivation"]["change"],
            address=_["vapor"]["wallet"]["sender"]["derivation"]["address"]
        )
    )

    assert signed_refund_transaction.type() == _["vapor"]["refund"]["signed"]["type"]
    assert signed_refund_transaction.fee() == _["vapor"]["refund"]["signed"]["fee"]
    assert signed_refund_transaction.hash() == _["vapor"]["refund"]["signed"]["hash"]
    assert signed_refund_transaction.raw() == _["vapor"]["refund"]["signed"]["raw"]
    # assert signed_refund_transaction.json() == _["vapor"]["refund"]["signed"]["json"]
    assert signed_refund_transaction.unsigned_datas() == _["vapor"]["refund"]["signed"]["unsigned_datas"]
    assert signed_refund_transaction.signatures() == _["vapor"]["refund"]["signed"]["signatures"]
    assert signed_refund_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["vapor"]["refund"]["signed"]["transaction_raw"]
    )
