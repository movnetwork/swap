#!/usr/bin/env python3

import json
import os

from swap.providers.bytom.htlc import HTLC
from swap.providers.bytom.transaction import (
    FundTransaction, WithdrawTransaction, RefundTransaction
)
from swap.providers.bytom.solver import (
    FundSolver, WithdrawSolver, RefundSolver
)
from swap.utils import clean_transaction_raw

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_bytom_fund_transaction():

    htlc = HTLC(network=_["bytom"]["network"]).build_htlc(
        secret_hash=_["bytom"]["htlc"]["secret"]["hash"],
        recipient_public_key=_["bytom"]["wallet"]["recipient"]["public_key"],
        sender_public_key=_["bytom"]["wallet"]["sender"]["public_key"],
        endblock=_["bytom"]["htlc"]["endblock"]
    )

    unsigned_fund_transaction = FundTransaction(network=_["bytom"]["network"])

    unsigned_fund_transaction.build_transaction(
        address=_["bytom"]["wallet"]["sender"]["address"],
        htlc=htlc,
        asset=_["bytom"]["asset"],
        amount=_["bytom"]["amount"],
        unit=_['bytom']['unit']
    )

    assert unsigned_fund_transaction.type() == _["bytom"]["fund"]["unsigned"]["type"]
    assert unsigned_fund_transaction.fee() == _["bytom"]["fund"]["unsigned"]["fee"]
    assert unsigned_fund_transaction.hash() == _["bytom"]["fund"]["unsigned"]["hash"]
    assert unsigned_fund_transaction.raw() == _["bytom"]["fund"]["unsigned"]["raw"]
    # assert unsigned_fund_transaction.json() == _["bytom"]["fund"]["unsigned"]["json"]
    assert unsigned_fund_transaction.unsigned_datas() == _["bytom"]["fund"]["unsigned"]["unsigned_datas"]
    assert unsigned_fund_transaction.signatures() == _["bytom"]["fund"]["unsigned"]["signatures"]
    assert unsigned_fund_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bytom"]["fund"]["unsigned"]["transaction_raw"]
    )

    signed_fund_transaction = unsigned_fund_transaction.sign(
        solver=FundSolver(
            xprivate_key=_["bytom"]["wallet"]["sender"]["xprivate_key"],
            path=_["bytom"]["wallet"]["sender"]["derivation"]["path"],
            account=_["bytom"]["wallet"]["sender"]["derivation"]["account"],
            change=_["bytom"]["wallet"]["sender"]["derivation"]["change"],
            address=_["bytom"]["wallet"]["sender"]["derivation"]["address"]
        )
    )

    assert signed_fund_transaction.type() == _["bytom"]["fund"]["signed"]["type"]
    assert signed_fund_transaction.fee() == _["bytom"]["fund"]["signed"]["fee"]
    assert signed_fund_transaction.hash() == _["bytom"]["fund"]["signed"]["hash"]
    assert signed_fund_transaction.raw() == _["bytom"]["fund"]["signed"]["raw"]
    # assert signed_fund_transaction.json() == _["bytom"]["fund"]["signed"]["json"]
    assert signed_fund_transaction.unsigned_datas() == _["bytom"]["fund"]["signed"]["unsigned_datas"]
    assert signed_fund_transaction.signatures() == _["bytom"]["fund"]["signed"]["signatures"]
    assert signed_fund_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bytom"]["fund"]["signed"]["transaction_raw"]
    )


def test_bytom_withdraw_transaction():

    unsigned_withdraw_transaction = WithdrawTransaction(network=_["bytom"]["network"])

    unsigned_withdraw_transaction.build_transaction(
        address=_["bytom"]["wallet"]["recipient"]["address"],
        transaction_hash=_["bytom"]["transaction_hash"],
        asset=_["bytom"]["asset"]
    )

    assert unsigned_withdraw_transaction.type() == _["bytom"]["withdraw"]["unsigned"]["type"]
    assert unsigned_withdraw_transaction.fee() == _["bytom"]["withdraw"]["unsigned"]["fee"]
    assert unsigned_withdraw_transaction.hash() == _["bytom"]["withdraw"]["unsigned"]["hash"]
    assert unsigned_withdraw_transaction.raw() == _["bytom"]["withdraw"]["unsigned"]["raw"]
    # assert unsigned_withdraw_transaction.json() == _["bytom"]["withdraw"]["unsigned"]["json"]
    assert unsigned_withdraw_transaction.unsigned_datas() == _["bytom"]["withdraw"]["unsigned"]["unsigned_datas"]
    assert unsigned_withdraw_transaction.signatures() == _["bytom"]["withdraw"]["unsigned"]["signatures"]
    assert unsigned_withdraw_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bytom"]["withdraw"]["unsigned"]["transaction_raw"]
    )

    signed_withdraw_transaction = unsigned_withdraw_transaction.sign(
        solver=WithdrawSolver(
            xprivate_key=_["bytom"]["wallet"]["recipient"]["xprivate_key"],
            secret_key=_["bytom"]["htlc"]["secret"]["key"],
            bytecode=_["bytom"]["htlc"]["bytecode"],
            path=_["bytom"]["wallet"]["recipient"]["derivation"]["path"],
            account=_["bytom"]["wallet"]["recipient"]["derivation"]["account"],
            change=_["bytom"]["wallet"]["recipient"]["derivation"]["change"],
            address=_["bytom"]["wallet"]["recipient"]["derivation"]["address"]
        )
    )

    assert signed_withdraw_transaction.type() == _["bytom"]["withdraw"]["signed"]["type"]
    assert signed_withdraw_transaction.fee() == _["bytom"]["withdraw"]["signed"]["fee"]
    assert signed_withdraw_transaction.hash() == _["bytom"]["withdraw"]["signed"]["hash"]
    assert signed_withdraw_transaction.raw() == _["bytom"]["withdraw"]["signed"]["raw"]
    # assert signed_withdraw_transaction.json() == _["bytom"]["withdraw"]["signed"]["json"]
    assert signed_withdraw_transaction.unsigned_datas() == _["bytom"]["withdraw"]["signed"]["unsigned_datas"]
    assert signed_withdraw_transaction.signatures() == _["bytom"]["withdraw"]["signed"]["signatures"]
    assert signed_withdraw_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bytom"]["withdraw"]["signed"]["transaction_raw"]
    )


def test_bytom_refund_transaction():

    unsigned_refund_transaction = RefundTransaction(network=_["bytom"]["network"])

    unsigned_refund_transaction.build_transaction(
        address=_["bytom"]["wallet"]["sender"]["address"],
        transaction_hash=_["bytom"]["transaction_hash"],
        asset=_["bytom"]["asset"]
    )

    assert unsigned_refund_transaction.type() == _["bytom"]["refund"]["unsigned"]["type"]
    assert unsigned_refund_transaction.fee() == _["bytom"]["refund"]["unsigned"]["fee"]
    assert unsigned_refund_transaction.hash() == _["bytom"]["refund"]["unsigned"]["hash"]
    assert unsigned_refund_transaction.raw() == _["bytom"]["refund"]["unsigned"]["raw"]
    # assert unsigned_refund_transaction.json() == _["bytom"]["refund"]["unsigned"]["json"]
    assert unsigned_refund_transaction.unsigned_datas() == _["bytom"]["refund"]["unsigned"]["unsigned_datas"]
    assert unsigned_refund_transaction.signatures() == _["bytom"]["refund"]["unsigned"]["signatures"]
    assert unsigned_refund_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bytom"]["refund"]["unsigned"]["transaction_raw"]
    )

    signed_refund_transaction = unsigned_refund_transaction.sign(
        solver=RefundSolver(
            xprivate_key=_["bytom"]["wallet"]["sender"]["xprivate_key"],
            bytecode=_["bytom"]["htlc"]["bytecode"],
            path=_["bytom"]["wallet"]["sender"]["derivation"]["path"],
            account=_["bytom"]["wallet"]["sender"]["derivation"]["account"],
            change=_["bytom"]["wallet"]["sender"]["derivation"]["change"],
            address=_["bytom"]["wallet"]["sender"]["derivation"]["address"]
        )
    )

    assert signed_refund_transaction.type() == _["bytom"]["refund"]["signed"]["type"]
    assert signed_refund_transaction.fee() == _["bytom"]["refund"]["signed"]["fee"]
    assert signed_refund_transaction.hash() == _["bytom"]["refund"]["signed"]["hash"]
    assert signed_refund_transaction.raw() == _["bytom"]["refund"]["signed"]["raw"]
    # assert signed_refund_transaction.json() == _["bytom"]["refund"]["signed"]["json"]
    assert signed_refund_transaction.unsigned_datas() == _["bytom"]["refund"]["signed"]["unsigned_datas"]
    assert signed_refund_transaction.signatures() == _["bytom"]["refund"]["signed"]["signatures"]
    assert signed_refund_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bytom"]["refund"]["signed"]["transaction_raw"]
    )
