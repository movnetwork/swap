#!/usr/bin/env python3

import json
import os

from swap.providers.xinfin.signature import (
    Signature, FundSignature, WithdrawSignature, RefundSignature
)
from swap.providers.xinfin.solver import (
    FundSolver, WithdrawSolver, RefundSolver
)
from swap.utils import clean_transaction_raw

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_xinfin_fund_signature():

    unsigned_fund_transaction_raw = _["xinfin"]["fund"]["unsigned"]["transaction_raw"]

    fund_solver = FundSolver(
        xprivate_key=_["xinfin"]["wallet"]["sender"]["root_xprivate_key"],
        path=_["xinfin"]["wallet"]["sender"]["derivation"]["path"],
        account=_["xinfin"]["wallet"]["sender"]["derivation"]["account"],
        change=_["xinfin"]["wallet"]["sender"]["derivation"]["change"],
        address=_["xinfin"]["wallet"]["sender"]["derivation"]["address"]
    )

    signature = Signature(network=_["xinfin"]["network"]).sign(
        transaction_raw=unsigned_fund_transaction_raw,
        solver=fund_solver
    )

    assert signature.type() == _["xinfin"]["fund"]["signed"]["type"]
    assert signature.fee() == _["xinfin"]["fund"]["signed"]["fee"]
    assert signature.hash() == _["xinfin"]["fund"]["signed"]["hash"]
    assert signature.raw() == _["xinfin"]["fund"]["signed"]["raw"]
    assert signature.json() == _["xinfin"]["fund"]["signed"]["json"]
    assert signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["xinfin"]["fund"]["signed"]["transaction_raw"]
    )

    fund_signature = FundSignature(network=_["xinfin"]["network"]).sign(
        transaction_raw=unsigned_fund_transaction_raw,
        solver=fund_solver
    )

    assert fund_signature.type() == _["xinfin"]["fund"]["signed"]["type"]
    assert fund_signature.fee() == _["xinfin"]["fund"]["signed"]["fee"]
    assert fund_signature.hash() == _["xinfin"]["fund"]["signed"]["hash"]
    assert fund_signature.raw() == _["xinfin"]["fund"]["signed"]["raw"]
    assert fund_signature.json() == _["xinfin"]["fund"]["signed"]["json"]
    assert fund_signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["xinfin"]["fund"]["signed"]["transaction_raw"]
    )


def test_xinfin_withdraw_signature():

    unsigned_withdraw_transaction_raw = _["xinfin"]["withdraw"]["unsigned"]["transaction_raw"]

    withdraw_solver = WithdrawSolver(
        xprivate_key=_["xinfin"]["wallet"]["recipient"]["root_xprivate_key"],
        path=_["xinfin"]["wallet"]["recipient"]["derivation"]["path"],
        account=_["xinfin"]["wallet"]["recipient"]["derivation"]["account"],
        change=_["xinfin"]["wallet"]["recipient"]["derivation"]["change"],
        address=_["xinfin"]["wallet"]["recipient"]["derivation"]["address"]
    )

    signature = Signature(network=_["xinfin"]["network"]).sign(
        transaction_raw=unsigned_withdraw_transaction_raw,
        solver=withdraw_solver
    )

    assert signature.type() == _["xinfin"]["withdraw"]["signed"]["type"]
    assert signature.fee() == _["xinfin"]["withdraw"]["signed"]["fee"]
    assert signature.hash() == _["xinfin"]["withdraw"]["signed"]["hash"]
    assert signature.raw() == _["xinfin"]["withdraw"]["signed"]["raw"]
    assert signature.json() == _["xinfin"]["withdraw"]["signed"]["json"]
    assert signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["xinfin"]["withdraw"]["signed"]["transaction_raw"]
    )

    withdraw_signature = WithdrawSignature(network=_["xinfin"]["network"]).sign(
        transaction_raw=unsigned_withdraw_transaction_raw,
        solver=withdraw_solver
    )

    assert withdraw_signature.type() == _["xinfin"]["withdraw"]["signed"]["type"]
    assert withdraw_signature.fee() == _["xinfin"]["withdraw"]["signed"]["fee"]
    assert withdraw_signature.hash() == _["xinfin"]["withdraw"]["signed"]["hash"]
    assert withdraw_signature.raw() == _["xinfin"]["withdraw"]["signed"]["raw"]
    assert withdraw_signature.json() == _["xinfin"]["withdraw"]["signed"]["json"]
    assert withdraw_signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["xinfin"]["withdraw"]["signed"]["transaction_raw"]
    )


def test_xinfin_refund_signature():

    unsigned_refund_transaction_raw = _["xinfin"]["refund"]["unsigned"]["transaction_raw"]

    refund_solver = RefundSolver(
        xprivate_key=_["xinfin"]["wallet"]["sender"]["root_xprivate_key"],
        path=_["xinfin"]["wallet"]["sender"]["derivation"]["path"],
        account=_["xinfin"]["wallet"]["sender"]["derivation"]["account"],
        change=_["xinfin"]["wallet"]["sender"]["derivation"]["change"],
        address=_["xinfin"]["wallet"]["sender"]["derivation"]["address"]
    )

    signature = Signature(network=_["xinfin"]["network"]).sign(
        transaction_raw=unsigned_refund_transaction_raw,
        solver=refund_solver
    )

    assert signature.type() == _["xinfin"]["refund"]["signed"]["type"]
    assert signature.fee() == _["xinfin"]["refund"]["signed"]["fee"]
    assert signature.hash() == _["xinfin"]["refund"]["signed"]["hash"]
    assert signature.raw() == _["xinfin"]["refund"]["signed"]["raw"]
    assert signature.json() == _["xinfin"]["refund"]["signed"]["json"]
    assert signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["xinfin"]["refund"]["signed"]["transaction_raw"]
    )

    refund_signature = RefundSignature(network=_["xinfin"]["network"]).sign(
        transaction_raw=unsigned_refund_transaction_raw,
        solver=refund_solver
    )

    assert refund_signature.type() == _["xinfin"]["refund"]["signed"]["type"]
    assert refund_signature.fee() == _["xinfin"]["refund"]["signed"]["fee"]
    assert refund_signature.hash() == _["xinfin"]["refund"]["signed"]["hash"]
    assert refund_signature.raw() == _["xinfin"]["refund"]["signed"]["raw"]
    assert refund_signature.json() == _["xinfin"]["refund"]["signed"]["json"]
    assert refund_signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["xinfin"]["refund"]["signed"]["transaction_raw"]
    )
