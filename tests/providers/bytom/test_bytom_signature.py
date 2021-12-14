#!/usr/bin/env python3

import json
import os

from swap.providers.bytom.signature import (
    Signature, NormalSignature, FundSignature, WithdrawSignature, RefundSignature
)
from swap.providers.bytom.solver import (
    NormalSolver, FundSolver, WithdrawSolver, RefundSolver
)
from swap.utils import clean_transaction_raw

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_bytom_normal_signature():

    unsigned_normal_transaction_raw = _["bytom"]["normal"]["unsigned"]["transaction_raw"]

    normal_solver = NormalSolver(
        xprivate_key=_["bytom"]["wallet"]["sender"]["xprivate_key"],
        path=_["bytom"]["wallet"]["sender"]["derivation"]["path"],
        account=_["bytom"]["wallet"]["sender"]["derivation"]["account"],
        change=_["bytom"]["wallet"]["sender"]["derivation"]["change"],
        address=_["bytom"]["wallet"]["sender"]["derivation"]["address"]
    )

    signature = Signature(network=_["bytom"]["network"]).sign(
        transaction_raw=unsigned_normal_transaction_raw,
        solver=normal_solver
    )

    assert signature.type() == _["bytom"]["normal"]["signed"]["type"]
    assert signature.fee() == _["bytom"]["normal"]["signed"]["fee"]
    assert signature.hash() == _["bytom"]["normal"]["signed"]["hash"]
    assert signature.raw() == _["bytom"]["normal"]["signed"]["raw"]
    # assert signature.json() == _["bytom"]["normal"]["signed"]["json"]
    assert signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bytom"]["normal"]["signed"]["transaction_raw"]
    )

    normal_signature = NormalSignature(network=_["bytom"]["network"]).sign(
        transaction_raw=unsigned_normal_transaction_raw,
        solver=normal_solver
    )

    assert normal_signature.type() == _["bytom"]["normal"]["signed"]["type"]
    assert normal_signature.fee() == _["bytom"]["normal"]["signed"]["fee"]
    assert normal_signature.hash() == _["bytom"]["normal"]["signed"]["hash"]
    assert normal_signature.raw() == _["bytom"]["normal"]["signed"]["raw"]
    # assert normal_signature.json() == _["bytom"]["normal"]["signed"]["json"]
    assert normal_signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bytom"]["normal"]["signed"]["transaction_raw"]
    )


def test_bytom_fund_signature():

    unsigned_fund_transaction_raw = _["bytom"]["fund"]["unsigned"]["transaction_raw"]

    fund_solver = FundSolver(
        xprivate_key=_["bytom"]["wallet"]["sender"]["xprivate_key"],
        path=_["bytom"]["wallet"]["sender"]["derivation"]["path"],
        account=_["bytom"]["wallet"]["sender"]["derivation"]["account"],
        change=_["bytom"]["wallet"]["sender"]["derivation"]["change"],
        address=_["bytom"]["wallet"]["sender"]["derivation"]["address"]
    )

    signature = Signature(network=_["bytom"]["network"]).sign(
        transaction_raw=unsigned_fund_transaction_raw,
        solver=fund_solver
    )

    assert signature.type() == _["bytom"]["fund"]["signed"]["type"]
    assert signature.fee() == _["bytom"]["fund"]["signed"]["fee"]
    assert signature.hash() == _["bytom"]["fund"]["signed"]["hash"]
    assert signature.raw() == _["bytom"]["fund"]["signed"]["raw"]
    # assert signature.json() == _["bytom"]["fund"]["signed"]["json"]
    assert signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bytom"]["fund"]["signed"]["transaction_raw"]
    )

    fund_signature = FundSignature(network=_["bytom"]["network"]).sign(
        transaction_raw=unsigned_fund_transaction_raw,
        solver=fund_solver
    )

    assert fund_signature.type() == _["bytom"]["fund"]["signed"]["type"]
    assert fund_signature.fee() == _["bytom"]["fund"]["signed"]["fee"]
    assert fund_signature.hash() == _["bytom"]["fund"]["signed"]["hash"]
    assert fund_signature.raw() == _["bytom"]["fund"]["signed"]["raw"]
    # assert fund_signature.json() == _["bytom"]["fund"]["signed"]["json"]
    assert fund_signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bytom"]["fund"]["signed"]["transaction_raw"]
    )


def test_bytom_withdraw_signature():

    unsigned_withdraw_transaction_raw = _["bytom"]["withdraw"]["unsigned"]["transaction_raw"]

    withdraw_solver = WithdrawSolver(
        xprivate_key=_["bytom"]["wallet"]["recipient"]["xprivate_key"],
        secret_key=_["bytom"]["htlc"]["secret"]["key"],
        bytecode=_["bytom"]["htlc"]["bytecode"],
        path=_["bytom"]["wallet"]["recipient"]["derivation"]["path"],
        account=_["bytom"]["wallet"]["recipient"]["derivation"]["account"],
        change=_["bytom"]["wallet"]["recipient"]["derivation"]["change"],
        address=_["bytom"]["wallet"]["recipient"]["derivation"]["address"]
    )

    signature = Signature(network=_["bytom"]["network"]).sign(
        transaction_raw=unsigned_withdraw_transaction_raw,
        solver=withdraw_solver
    )

    assert signature.type() == _["bytom"]["withdraw"]["signed"]["type"]
    assert signature.fee() == _["bytom"]["withdraw"]["signed"]["fee"]
    assert signature.hash() == _["bytom"]["withdraw"]["signed"]["hash"]
    assert signature.raw() == _["bytom"]["withdraw"]["signed"]["raw"]
    # assert signature.json() == _["bytom"]["withdraw"]["signed"]["json"]
    assert signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bytom"]["withdraw"]["signed"]["transaction_raw"]
    )

    withdraw_signature = WithdrawSignature(network=_["bytom"]["network"]).sign(
        transaction_raw=unsigned_withdraw_transaction_raw,
        solver=withdraw_solver
    )

    assert withdraw_signature.type() == _["bytom"]["withdraw"]["signed"]["type"]
    assert withdraw_signature.fee() == _["bytom"]["withdraw"]["signed"]["fee"]
    assert withdraw_signature.hash() == _["bytom"]["withdraw"]["signed"]["hash"]
    assert withdraw_signature.raw() == _["bytom"]["withdraw"]["signed"]["raw"]
    # assert withdraw_signature.json() == _["bytom"]["withdraw"]["signed"]["json"]
    assert withdraw_signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bytom"]["withdraw"]["signed"]["transaction_raw"]
    )


def test_bytom_refund_signature():

    unsigned_refund_transaction_raw = _["bytom"]["refund"]["unsigned"]["transaction_raw"]

    refund_solver = RefundSolver(
        xprivate_key=_["bytom"]["wallet"]["sender"]["xprivate_key"],
        bytecode=_["bytom"]["htlc"]["bytecode"],
        path=_["bytom"]["wallet"]["sender"]["derivation"]["path"],
        account=_["bytom"]["wallet"]["sender"]["derivation"]["account"],
        change=_["bytom"]["wallet"]["sender"]["derivation"]["change"],
        address=_["bytom"]["wallet"]["sender"]["derivation"]["address"]
    )

    signature = Signature(network=_["bytom"]["network"]).sign(
        transaction_raw=unsigned_refund_transaction_raw,
        solver=refund_solver
    )

    assert signature.type() == _["bytom"]["refund"]["signed"]["type"]
    assert signature.fee() == _["bytom"]["refund"]["signed"]["fee"]
    assert signature.hash() == _["bytom"]["refund"]["signed"]["hash"]
    assert signature.raw() == _["bytom"]["refund"]["signed"]["raw"]
    # assert signature.json() == _["bytom"]["refund"]["signed"]["json"]
    assert signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bytom"]["refund"]["signed"]["transaction_raw"]
    )

    refund_signature = RefundSignature(network=_["bytom"]["network"]).sign(
        transaction_raw=unsigned_refund_transaction_raw,
        solver=refund_solver
    )

    assert refund_signature.type() == _["bytom"]["refund"]["signed"]["type"]
    assert refund_signature.fee() == _["bytom"]["refund"]["signed"]["fee"]
    assert refund_signature.hash() == _["bytom"]["refund"]["signed"]["hash"]
    assert refund_signature.raw() == _["bytom"]["refund"]["signed"]["raw"]
    # assert refund_signature.json() == _["bytom"]["refund"]["signed"]["json"]
    assert refund_signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bytom"]["refund"]["signed"]["transaction_raw"]
    )
