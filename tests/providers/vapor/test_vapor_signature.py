#!/usr/bin/env python3

import json
import os

from swap.providers.vapor.signature import (
    Signature, FundSignature, WithdrawSignature, RefundSignature
)
from swap.providers.vapor.solver import (
    FundSolver, WithdrawSolver, RefundSolver
)
from swap.utils import clean_transaction_raw

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_vapor_fund_signature():

    unsigned_fund_transaction_raw = _["vapor"]["fund"]["unsigned"]["transaction_raw"]

    fund_solver = FundSolver(
        xprivate_key=_["vapor"]["wallet"]["sender"]["xprivate_key"],
        path=_["vapor"]["wallet"]["sender"]["derivation"]["path"],
        account=_["vapor"]["wallet"]["sender"]["derivation"]["account"],
        change=_["vapor"]["wallet"]["sender"]["derivation"]["change"],
        address=_["vapor"]["wallet"]["sender"]["derivation"]["address"]
    )

    signature = Signature(network=_["vapor"]["network"]).sign(
        transaction_raw=unsigned_fund_transaction_raw,
        solver=fund_solver
    )

    assert signature.type() == _["vapor"]["fund"]["signed"]["type"]
    assert signature.fee() == _["vapor"]["fund"]["signed"]["fee"]
    assert signature.hash() == _["vapor"]["fund"]["signed"]["hash"]
    assert signature.raw() == _["vapor"]["fund"]["signed"]["raw"]
    # assert signature.json() == _["vapor"]["fund"]["signed"]["json"]
    assert signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["vapor"]["fund"]["signed"]["transaction_raw"]
    )

    fund_signature = FundSignature(network=_["vapor"]["network"]).sign(
        transaction_raw=unsigned_fund_transaction_raw,
        solver=fund_solver
    )

    assert fund_signature.type() == _["vapor"]["fund"]["signed"]["type"]
    assert fund_signature.fee() == _["vapor"]["fund"]["signed"]["fee"]
    assert fund_signature.hash() == _["vapor"]["fund"]["signed"]["hash"]
    assert fund_signature.raw() == _["vapor"]["fund"]["signed"]["raw"]
    # assert fund_signature.json() == _["vapor"]["fund"]["signed"]["json"]
    assert fund_signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["vapor"]["fund"]["signed"]["transaction_raw"]
    )


def test_vapor_withdraw_signature():

    unsigned_withdraw_transaction_raw = _["vapor"]["withdraw"]["unsigned"]["transaction_raw"]

    withdraw_solver = WithdrawSolver(
        xprivate_key=_["vapor"]["wallet"]["recipient"]["xprivate_key"],
        secret_key=_["vapor"]["htlc"]["secret"]["key"],
        bytecode=_["vapor"]["htlc"]["bytecode"],
        path=_["vapor"]["wallet"]["recipient"]["derivation"]["path"],
        account=_["vapor"]["wallet"]["recipient"]["derivation"]["account"],
        change=_["vapor"]["wallet"]["recipient"]["derivation"]["change"],
        address=_["vapor"]["wallet"]["recipient"]["derivation"]["address"]
    )

    signature = Signature(network=_["vapor"]["network"]).sign(
        transaction_raw=unsigned_withdraw_transaction_raw,
        solver=withdraw_solver
    )

    assert signature.type() == _["vapor"]["withdraw"]["signed"]["type"]
    assert signature.fee() == _["vapor"]["withdraw"]["signed"]["fee"]
    assert signature.hash() == _["vapor"]["withdraw"]["signed"]["hash"]
    assert signature.raw() == _["vapor"]["withdraw"]["signed"]["raw"]
    # assert signature.json() == _["vapor"]["withdraw"]["signed"]["json"]
    assert signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["vapor"]["withdraw"]["signed"]["transaction_raw"]
    )

    withdraw_signature = WithdrawSignature(network=_["vapor"]["network"]).sign(
        transaction_raw=unsigned_withdraw_transaction_raw,
        solver=withdraw_solver
    )

    assert withdraw_signature.type() == _["vapor"]["withdraw"]["signed"]["type"]
    assert withdraw_signature.fee() == _["vapor"]["withdraw"]["signed"]["fee"]
    assert withdraw_signature.hash() == _["vapor"]["withdraw"]["signed"]["hash"]
    assert withdraw_signature.raw() == _["vapor"]["withdraw"]["signed"]["raw"]
    # assert withdraw_signature.json() == _["vapor"]["withdraw"]["signed"]["json"]
    assert withdraw_signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["vapor"]["withdraw"]["signed"]["transaction_raw"]
    )


def test_vapor_refund_signature():

    unsigned_refund_transaction_raw = _["vapor"]["refund"]["unsigned"]["transaction_raw"]

    refund_solver = RefundSolver(
        xprivate_key=_["vapor"]["wallet"]["sender"]["xprivate_key"],
        bytecode=_["vapor"]["htlc"]["bytecode"],
        path=_["vapor"]["wallet"]["sender"]["derivation"]["path"],
        account=_["vapor"]["wallet"]["sender"]["derivation"]["account"],
        change=_["vapor"]["wallet"]["sender"]["derivation"]["change"],
        address=_["vapor"]["wallet"]["sender"]["derivation"]["address"]
    )

    signature = Signature(network=_["vapor"]["network"]).sign(
        transaction_raw=unsigned_refund_transaction_raw,
        solver=refund_solver
    )

    assert signature.type() == _["vapor"]["refund"]["signed"]["type"]
    assert signature.fee() == _["vapor"]["refund"]["signed"]["fee"]
    assert signature.hash() == _["vapor"]["refund"]["signed"]["hash"]
    assert signature.raw() == _["vapor"]["refund"]["signed"]["raw"]
    # assert signature.json() == _["vapor"]["refund"]["signed"]["json"]
    assert signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["vapor"]["refund"]["signed"]["transaction_raw"]
    )

    refund_signature = RefundSignature(network=_["vapor"]["network"]).sign(
        transaction_raw=unsigned_refund_transaction_raw,
        solver=refund_solver
    )

    assert refund_signature.type() == _["vapor"]["refund"]["signed"]["type"]
    assert refund_signature.fee() == _["vapor"]["refund"]["signed"]["fee"]
    assert refund_signature.hash() == _["vapor"]["refund"]["signed"]["hash"]
    assert refund_signature.raw() == _["vapor"]["refund"]["signed"]["raw"]
    # assert refund_signature.json() == _["vapor"]["refund"]["signed"]["json"]
    assert refund_signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["vapor"]["refund"]["signed"]["transaction_raw"]
    )
