#!/usr/bin/env python3

import json
import os

from swap.providers.ethereum.signature import (
    Signature, NormalSignature, FundSignature, WithdrawSignature, RefundSignature
)
from swap.providers.ethereum.solver import (
    NormalSolver, FundSolver, WithdrawSolver, RefundSolver
)
from swap.utils import clean_transaction_raw

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_ethereum_normal_signature():

    unsigned_normal_transaction_raw = _["ethereum"]["normal"]["unsigned"]["transaction_raw"]

    normal_solver = NormalSolver(
        xprivate_key=_["ethereum"]["wallet"]["sender"]["root_xprivate_key"],
        path=_["ethereum"]["wallet"]["sender"]["derivation"]["path"],
        account=_["ethereum"]["wallet"]["sender"]["derivation"]["account"],
        change=_["ethereum"]["wallet"]["sender"]["derivation"]["change"],
        address=_["ethereum"]["wallet"]["sender"]["derivation"]["address"]
    )

    signature = Signature(network=_["ethereum"]["network"]).sign(
        transaction_raw=unsigned_normal_transaction_raw,
        solver=normal_solver
    )

    assert signature.type() == _["ethereum"]["normal"]["signed"]["type"]
    assert signature.fee() == _["ethereum"]["normal"]["signed"]["fee"]
    assert signature.hash() == _["ethereum"]["normal"]["signed"]["hash"]
    assert signature.raw() == _["ethereum"]["normal"]["signed"]["raw"]
    assert signature.json() == _["ethereum"]["normal"]["signed"]["json"]
    assert signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["ethereum"]["normal"]["signed"]["transaction_raw"]
    )

    normal_signature = NormalSignature(network=_["ethereum"]["network"]).sign(
        transaction_raw=unsigned_normal_transaction_raw,
        solver=normal_solver
    )

    assert normal_signature.type() == _["ethereum"]["normal"]["signed"]["type"]
    assert normal_signature.fee() == _["ethereum"]["normal"]["signed"]["fee"]
    assert normal_signature.hash() == _["ethereum"]["normal"]["signed"]["hash"]
    assert normal_signature.raw() == _["ethereum"]["normal"]["signed"]["raw"]
    assert normal_signature.json() == _["ethereum"]["normal"]["signed"]["json"]
    assert normal_signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["ethereum"]["normal"]["signed"]["transaction_raw"]
    )


def test_ethereum_fund_signature():

    unsigned_fund_transaction_raw = _["ethereum"]["fund"]["unsigned"]["transaction_raw"]

    fund_solver = FundSolver(
        xprivate_key=_["ethereum"]["wallet"]["sender"]["root_xprivate_key"],
        path=_["ethereum"]["wallet"]["sender"]["derivation"]["path"],
        account=_["ethereum"]["wallet"]["sender"]["derivation"]["account"],
        change=_["ethereum"]["wallet"]["sender"]["derivation"]["change"],
        address=_["ethereum"]["wallet"]["sender"]["derivation"]["address"]
    )

    signature = Signature(network=_["ethereum"]["network"]).sign(
        transaction_raw=unsigned_fund_transaction_raw,
        solver=fund_solver
    )

    assert signature.type() == _["ethereum"]["fund"]["signed"]["type"]
    assert signature.fee() == _["ethereum"]["fund"]["signed"]["fee"]
    assert signature.hash() == _["ethereum"]["fund"]["signed"]["hash"]
    assert signature.raw() == _["ethereum"]["fund"]["signed"]["raw"]
    assert signature.json() == _["ethereum"]["fund"]["signed"]["json"]
    assert signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["ethereum"]["fund"]["signed"]["transaction_raw"]
    )

    fund_signature = FundSignature(network=_["ethereum"]["network"]).sign(
        transaction_raw=unsigned_fund_transaction_raw,
        solver=fund_solver
    )

    assert fund_signature.type() == _["ethereum"]["fund"]["signed"]["type"]
    assert fund_signature.fee() == _["ethereum"]["fund"]["signed"]["fee"]
    assert fund_signature.hash() == _["ethereum"]["fund"]["signed"]["hash"]
    assert fund_signature.raw() == _["ethereum"]["fund"]["signed"]["raw"]
    assert fund_signature.json() == _["ethereum"]["fund"]["signed"]["json"]
    assert fund_signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["ethereum"]["fund"]["signed"]["transaction_raw"]
    )


def test_ethereum_withdraw_signature():

    unsigned_withdraw_transaction_raw = _["ethereum"]["withdraw"]["unsigned"]["transaction_raw"]

    withdraw_solver = WithdrawSolver(
        xprivate_key=_["ethereum"]["wallet"]["recipient"]["root_xprivate_key"],
        path=_["ethereum"]["wallet"]["recipient"]["derivation"]["path"],
        account=_["ethereum"]["wallet"]["recipient"]["derivation"]["account"],
        change=_["ethereum"]["wallet"]["recipient"]["derivation"]["change"],
        address=_["ethereum"]["wallet"]["recipient"]["derivation"]["address"]
    )

    signature = Signature(network=_["ethereum"]["network"]).sign(
        transaction_raw=unsigned_withdraw_transaction_raw,
        solver=withdraw_solver
    )

    assert signature.type() == _["ethereum"]["withdraw"]["signed"]["type"]
    assert signature.fee() == _["ethereum"]["withdraw"]["signed"]["fee"]
    assert signature.hash() == _["ethereum"]["withdraw"]["signed"]["hash"]
    assert signature.raw() == _["ethereum"]["withdraw"]["signed"]["raw"]
    assert signature.json() == _["ethereum"]["withdraw"]["signed"]["json"]
    assert signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["ethereum"]["withdraw"]["signed"]["transaction_raw"]
    )

    withdraw_signature = WithdrawSignature(network=_["ethereum"]["network"]).sign(
        transaction_raw=unsigned_withdraw_transaction_raw,
        solver=withdraw_solver
    )

    assert withdraw_signature.type() == _["ethereum"]["withdraw"]["signed"]["type"]
    assert withdraw_signature.fee() == _["ethereum"]["withdraw"]["signed"]["fee"]
    assert withdraw_signature.hash() == _["ethereum"]["withdraw"]["signed"]["hash"]
    assert withdraw_signature.raw() == _["ethereum"]["withdraw"]["signed"]["raw"]
    assert withdraw_signature.json() == _["ethereum"]["withdraw"]["signed"]["json"]
    assert withdraw_signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["ethereum"]["withdraw"]["signed"]["transaction_raw"]
    )


def test_ethereum_refund_signature():

    unsigned_refund_transaction_raw = _["ethereum"]["refund"]["unsigned"]["transaction_raw"]

    refund_solver = RefundSolver(
        xprivate_key=_["ethereum"]["wallet"]["sender"]["root_xprivate_key"],
        path=_["ethereum"]["wallet"]["sender"]["derivation"]["path"],
        account=_["ethereum"]["wallet"]["sender"]["derivation"]["account"],
        change=_["ethereum"]["wallet"]["sender"]["derivation"]["change"],
        address=_["ethereum"]["wallet"]["sender"]["derivation"]["address"]
    )

    signature = Signature(network=_["ethereum"]["network"]).sign(
        transaction_raw=unsigned_refund_transaction_raw,
        solver=refund_solver
    )

    assert signature.type() == _["ethereum"]["refund"]["signed"]["type"]
    assert signature.fee() == _["ethereum"]["refund"]["signed"]["fee"]
    assert signature.hash() == _["ethereum"]["refund"]["signed"]["hash"]
    assert signature.raw() == _["ethereum"]["refund"]["signed"]["raw"]
    assert signature.json() == _["ethereum"]["refund"]["signed"]["json"]
    assert signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["ethereum"]["refund"]["signed"]["transaction_raw"]
    )

    refund_signature = RefundSignature(network=_["ethereum"]["network"]).sign(
        transaction_raw=unsigned_refund_transaction_raw,
        solver=refund_solver
    )

    assert refund_signature.type() == _["ethereum"]["refund"]["signed"]["type"]
    assert refund_signature.fee() == _["ethereum"]["refund"]["signed"]["fee"]
    assert refund_signature.hash() == _["ethereum"]["refund"]["signed"]["hash"]
    assert refund_signature.raw() == _["ethereum"]["refund"]["signed"]["raw"]
    assert refund_signature.json() == _["ethereum"]["refund"]["signed"]["json"]
    assert refund_signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["ethereum"]["refund"]["signed"]["transaction_raw"]
    )
