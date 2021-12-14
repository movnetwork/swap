#!/usr/bin/env python3

import json
import os

from swap.providers.xinfin.signature import (
    Signature, NormalSignature, FundSignature, WithdrawSignature, RefundSignature
)
from swap.providers.xinfin.solver import (
    NormalSolver, FundSolver, WithdrawSolver, RefundSolver
)
from swap.utils import clean_transaction_raw

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_xinfin_xrc20_normal_signature():

    unsigned_xrc20_normal_transaction_raw = _["xinfin"]["xrc20_normal"]["unsigned"]["transaction_raw"]

    xrc20_normal_solver = NormalSolver(
        xprivate_key=_["xinfin"]["wallet"]["sender"]["root_xprivate_key"],
        path=_["xinfin"]["wallet"]["sender"]["derivation"]["path"],
        account=_["xinfin"]["wallet"]["sender"]["derivation"]["account"],
        change=_["xinfin"]["wallet"]["sender"]["derivation"]["change"],
        address=_["xinfin"]["wallet"]["sender"]["derivation"]["address"]
    )

    signature = Signature(network=_["xinfin"]["network"], xrc20=True).sign(
        transaction_raw=unsigned_xrc20_normal_transaction_raw,
        solver=xrc20_normal_solver
    )

    assert signature.type() == _["xinfin"]["xrc20_normal"]["signed"]["type"]
    assert signature.fee() == _["xinfin"]["xrc20_normal"]["signed"]["fee"]
    assert signature.hash() == _["xinfin"]["xrc20_normal"]["signed"]["hash"]
    assert signature.raw() == _["xinfin"]["xrc20_normal"]["signed"]["raw"]
    assert signature.json() == _["xinfin"]["xrc20_normal"]["signed"]["json"]
    assert signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["xinfin"]["xrc20_normal"]["signed"]["transaction_raw"]
    )

    xrc20_normal_signature = NormalSignature(network=_["xinfin"]["network"], xrc20=True).sign(
        transaction_raw=unsigned_xrc20_normal_transaction_raw,
        solver=xrc20_normal_solver
    )

    assert xrc20_normal_signature.type() == _["xinfin"]["xrc20_normal"]["signed"]["type"]
    assert xrc20_normal_signature.fee() == _["xinfin"]["xrc20_normal"]["signed"]["fee"]
    assert xrc20_normal_signature.hash() == _["xinfin"]["xrc20_normal"]["signed"]["hash"]
    assert xrc20_normal_signature.raw() == _["xinfin"]["xrc20_normal"]["signed"]["raw"]
    assert xrc20_normal_signature.json() == _["xinfin"]["xrc20_normal"]["signed"]["json"]
    assert xrc20_normal_signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["xinfin"]["xrc20_normal"]["signed"]["transaction_raw"]
    )


def test_xinfin_xrc20_fund_signature():

    unsigned_xrc20_fund_transaction_raw = _["xinfin"]["xrc20_fund"]["unsigned"]["transaction_raw"]

    xrc20_fund_solver = FundSolver(
        xprivate_key=_["xinfin"]["wallet"]["sender"]["root_xprivate_key"],
        path=_["xinfin"]["wallet"]["sender"]["derivation"]["path"],
        account=_["xinfin"]["wallet"]["sender"]["derivation"]["account"],
        change=_["xinfin"]["wallet"]["sender"]["derivation"]["change"],
        address=_["xinfin"]["wallet"]["sender"]["derivation"]["address"]
    )

    signature = Signature(network=_["xinfin"]["network"], xrc20=True).sign(
        transaction_raw=unsigned_xrc20_fund_transaction_raw,
        solver=xrc20_fund_solver
    )

    assert signature.type() == _["xinfin"]["xrc20_fund"]["signed"]["type"]
    assert signature.fee() == _["xinfin"]["xrc20_fund"]["signed"]["fee"]
    assert signature.hash() == _["xinfin"]["xrc20_fund"]["signed"]["hash"]
    assert signature.raw() == _["xinfin"]["xrc20_fund"]["signed"]["raw"]
    assert signature.json() == _["xinfin"]["xrc20_fund"]["signed"]["json"]
    assert signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["xinfin"]["xrc20_fund"]["signed"]["transaction_raw"]
    )

    xrc20_fund_signature = FundSignature(network=_["xinfin"]["network"], xrc20=True).sign(
        transaction_raw=unsigned_xrc20_fund_transaction_raw,
        solver=xrc20_fund_solver
    )

    assert xrc20_fund_signature.type() == _["xinfin"]["xrc20_fund"]["signed"]["type"]
    assert xrc20_fund_signature.fee() == _["xinfin"]["xrc20_fund"]["signed"]["fee"]
    assert xrc20_fund_signature.hash() == _["xinfin"]["xrc20_fund"]["signed"]["hash"]
    assert xrc20_fund_signature.raw() == _["xinfin"]["xrc20_fund"]["signed"]["raw"]
    assert xrc20_fund_signature.json() == _["xinfin"]["xrc20_fund"]["signed"]["json"]
    assert xrc20_fund_signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["xinfin"]["xrc20_fund"]["signed"]["transaction_raw"]
    )


def test_xinfin_xrc20_withdraw_signature():

    unsigned_xrc20_withdraw_transaction_raw = _["xinfin"]["xrc20_withdraw"]["unsigned"]["transaction_raw"]

    xrc20_withdraw_solver = WithdrawSolver(
        xprivate_key=_["xinfin"]["wallet"]["recipient"]["root_xprivate_key"],
        path=_["xinfin"]["wallet"]["recipient"]["derivation"]["path"],
        account=_["xinfin"]["wallet"]["recipient"]["derivation"]["account"],
        change=_["xinfin"]["wallet"]["recipient"]["derivation"]["change"],
        address=_["xinfin"]["wallet"]["recipient"]["derivation"]["address"]
    )

    signature = Signature(network=_["xinfin"]["network"], xrc20=True).sign(
        transaction_raw=unsigned_xrc20_withdraw_transaction_raw,
        solver=xrc20_withdraw_solver,
    )

    assert signature.type() == _["xinfin"]["xrc20_withdraw"]["signed"]["type"]
    assert signature.fee() == _["xinfin"]["xrc20_withdraw"]["signed"]["fee"]
    assert signature.hash() == _["xinfin"]["xrc20_withdraw"]["signed"]["hash"]
    assert signature.raw() == _["xinfin"]["xrc20_withdraw"]["signed"]["raw"]
    assert signature.json() == _["xinfin"]["xrc20_withdraw"]["signed"]["json"]
    assert signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["xinfin"]["xrc20_withdraw"]["signed"]["transaction_raw"]
    )

    xrc20_withdraw_signature = WithdrawSignature(network=_["xinfin"]["network"], xrc20=True).sign(
        transaction_raw=unsigned_xrc20_withdraw_transaction_raw,
        solver=xrc20_withdraw_solver
    )

    assert xrc20_withdraw_signature.type() == _["xinfin"]["xrc20_withdraw"]["signed"]["type"]
    assert xrc20_withdraw_signature.fee() == _["xinfin"]["xrc20_withdraw"]["signed"]["fee"]
    assert xrc20_withdraw_signature.hash() == _["xinfin"]["xrc20_withdraw"]["signed"]["hash"]
    assert xrc20_withdraw_signature.raw() == _["xinfin"]["xrc20_withdraw"]["signed"]["raw"]
    assert xrc20_withdraw_signature.json() == _["xinfin"]["xrc20_withdraw"]["signed"]["json"]
    assert xrc20_withdraw_signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["xinfin"]["xrc20_withdraw"]["signed"]["transaction_raw"]
    )


def test_xinfin_xrc20_refund_signature():

    unsigned_xrc20_refund_transaction_raw = _["xinfin"]["xrc20_refund"]["unsigned"]["transaction_raw"]

    xrc20_refund_solver = RefundSolver(
        xprivate_key=_["xinfin"]["wallet"]["sender"]["root_xprivate_key"],
        path=_["xinfin"]["wallet"]["sender"]["derivation"]["path"],
        account=_["xinfin"]["wallet"]["sender"]["derivation"]["account"],
        change=_["xinfin"]["wallet"]["sender"]["derivation"]["change"],
        address=_["xinfin"]["wallet"]["sender"]["derivation"]["address"]
    )

    signature = Signature(network=_["xinfin"]["network"], xrc20=True).sign(
        transaction_raw=unsigned_xrc20_refund_transaction_raw,
        solver=xrc20_refund_solver
    )

    assert signature.type() == _["xinfin"]["xrc20_refund"]["signed"]["type"]
    assert signature.fee() == _["xinfin"]["xrc20_refund"]["signed"]["fee"]
    assert signature.hash() == _["xinfin"]["xrc20_refund"]["signed"]["hash"]
    assert signature.raw() == _["xinfin"]["xrc20_refund"]["signed"]["raw"]
    assert signature.json() == _["xinfin"]["xrc20_refund"]["signed"]["json"]
    assert signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["xinfin"]["xrc20_refund"]["signed"]["transaction_raw"]
    )

    xrc20_refund_signature = RefundSignature(network=_["xinfin"]["network"], xrc20=True).sign(
        transaction_raw=unsigned_xrc20_refund_transaction_raw,
        solver=xrc20_refund_solver
    )

    assert xrc20_refund_signature.type() == _["xinfin"]["xrc20_refund"]["signed"]["type"]
    assert xrc20_refund_signature.fee() == _["xinfin"]["xrc20_refund"]["signed"]["fee"]
    assert xrc20_refund_signature.hash() == _["xinfin"]["xrc20_refund"]["signed"]["hash"]
    assert xrc20_refund_signature.raw() == _["xinfin"]["xrc20_refund"]["signed"]["raw"]
    assert xrc20_refund_signature.json() == _["xinfin"]["xrc20_refund"]["signed"]["json"]
    assert xrc20_refund_signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["xinfin"]["xrc20_refund"]["signed"]["transaction_raw"]
    )
