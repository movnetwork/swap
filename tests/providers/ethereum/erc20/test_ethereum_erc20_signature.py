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
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_ethereum_erc20_normal_signature():

    unsigned_erc20_normal_transaction_raw = _["ethereum"]["erc20_normal"]["unsigned"]["transaction_raw"]

    erc20_normal_solver = NormalSolver(
        xprivate_key=_["ethereum"]["wallet"]["sender"]["root_xprivate_key"],
        path=_["ethereum"]["wallet"]["sender"]["derivation"]["path"],
        account=_["ethereum"]["wallet"]["sender"]["derivation"]["account"],
        change=_["ethereum"]["wallet"]["sender"]["derivation"]["change"],
        address=_["ethereum"]["wallet"]["sender"]["derivation"]["address"]
    )

    signature = Signature(network=_["ethereum"]["network"], erc20=True).sign(
        transaction_raw=unsigned_erc20_normal_transaction_raw,
        solver=erc20_normal_solver
    )

    assert signature.type() == _["ethereum"]["erc20_normal"]["signed"]["type"]
    assert signature.fee() == _["ethereum"]["erc20_normal"]["signed"]["fee"]
    assert signature.hash() == _["ethereum"]["erc20_normal"]["signed"]["hash"]
    assert signature.raw() == _["ethereum"]["erc20_normal"]["signed"]["raw"]
    assert signature.json() == _["ethereum"]["erc20_normal"]["signed"]["json"]
    assert signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["ethereum"]["erc20_normal"]["signed"]["transaction_raw"]
    )

    erc20_normal_signature = NormalSignature(network=_["ethereum"]["network"], erc20=True).sign(
        transaction_raw=unsigned_erc20_normal_transaction_raw,
        solver=erc20_normal_solver
    )

    assert erc20_normal_signature.type() == _["ethereum"]["erc20_normal"]["signed"]["type"]
    assert erc20_normal_signature.fee() == _["ethereum"]["erc20_normal"]["signed"]["fee"]
    assert erc20_normal_signature.hash() == _["ethereum"]["erc20_normal"]["signed"]["hash"]
    assert erc20_normal_signature.raw() == _["ethereum"]["erc20_normal"]["signed"]["raw"]
    assert erc20_normal_signature.json() == _["ethereum"]["erc20_normal"]["signed"]["json"]
    assert erc20_normal_signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["ethereum"]["erc20_normal"]["signed"]["transaction_raw"]
    )


def test_ethereum_erc20_fund_signature():

    unsigned_erc20_fund_transaction_raw = _["ethereum"]["erc20_fund"]["unsigned"]["transaction_raw"]

    erc20_fund_solver = FundSolver(
        xprivate_key=_["ethereum"]["wallet"]["sender"]["root_xprivate_key"],
        path=_["ethereum"]["wallet"]["sender"]["derivation"]["path"],
        account=_["ethereum"]["wallet"]["sender"]["derivation"]["account"],
        change=_["ethereum"]["wallet"]["sender"]["derivation"]["change"],
        address=_["ethereum"]["wallet"]["sender"]["derivation"]["address"]
    )

    signature = Signature(network=_["ethereum"]["network"], erc20=True).sign(
        transaction_raw=unsigned_erc20_fund_transaction_raw,
        solver=erc20_fund_solver
    )

    assert signature.type() == _["ethereum"]["erc20_fund"]["signed"]["type"]
    assert signature.fee() == _["ethereum"]["erc20_fund"]["signed"]["fee"]
    assert signature.hash() == _["ethereum"]["erc20_fund"]["signed"]["hash"]
    assert signature.raw() == _["ethereum"]["erc20_fund"]["signed"]["raw"]
    assert signature.json() == _["ethereum"]["erc20_fund"]["signed"]["json"]
    assert signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["ethereum"]["erc20_fund"]["signed"]["transaction_raw"]
    )

    erc20_fund_signature = FundSignature(network=_["ethereum"]["network"], erc20=True).sign(
        transaction_raw=unsigned_erc20_fund_transaction_raw,
        solver=erc20_fund_solver
    )

    assert erc20_fund_signature.type() == _["ethereum"]["erc20_fund"]["signed"]["type"]
    assert erc20_fund_signature.fee() == _["ethereum"]["erc20_fund"]["signed"]["fee"]
    assert erc20_fund_signature.hash() == _["ethereum"]["erc20_fund"]["signed"]["hash"]
    assert erc20_fund_signature.raw() == _["ethereum"]["erc20_fund"]["signed"]["raw"]
    assert erc20_fund_signature.json() == _["ethereum"]["erc20_fund"]["signed"]["json"]
    assert erc20_fund_signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["ethereum"]["erc20_fund"]["signed"]["transaction_raw"]
    )


def test_ethereum_erc20_withdraw_signature():

    unsigned_erc20_withdraw_transaction_raw = _["ethereum"]["erc20_withdraw"]["unsigned"]["transaction_raw"]

    erc20_withdraw_solver = WithdrawSolver(
        xprivate_key=_["ethereum"]["wallet"]["recipient"]["root_xprivate_key"],
        path=_["ethereum"]["wallet"]["recipient"]["derivation"]["path"],
        account=_["ethereum"]["wallet"]["recipient"]["derivation"]["account"],
        change=_["ethereum"]["wallet"]["recipient"]["derivation"]["change"],
        address=_["ethereum"]["wallet"]["recipient"]["derivation"]["address"]
    )

    signature = Signature(network=_["ethereum"]["network"], erc20=True).sign(
        transaction_raw=unsigned_erc20_withdraw_transaction_raw,
        solver=erc20_withdraw_solver,
    )

    assert signature.type() == _["ethereum"]["erc20_withdraw"]["signed"]["type"]
    assert signature.fee() == _["ethereum"]["erc20_withdraw"]["signed"]["fee"]
    assert signature.hash() == _["ethereum"]["erc20_withdraw"]["signed"]["hash"]
    assert signature.raw() == _["ethereum"]["erc20_withdraw"]["signed"]["raw"]
    assert signature.json() == _["ethereum"]["erc20_withdraw"]["signed"]["json"]
    assert signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["ethereum"]["erc20_withdraw"]["signed"]["transaction_raw"]
    )

    erc20_withdraw_signature = WithdrawSignature(network=_["ethereum"]["network"], erc20=True).sign(
        transaction_raw=unsigned_erc20_withdraw_transaction_raw,
        solver=erc20_withdraw_solver
    )

    assert erc20_withdraw_signature.type() == _["ethereum"]["erc20_withdraw"]["signed"]["type"]
    assert erc20_withdraw_signature.fee() == _["ethereum"]["erc20_withdraw"]["signed"]["fee"]
    assert erc20_withdraw_signature.hash() == _["ethereum"]["erc20_withdraw"]["signed"]["hash"]
    assert erc20_withdraw_signature.raw() == _["ethereum"]["erc20_withdraw"]["signed"]["raw"]
    assert erc20_withdraw_signature.json() == _["ethereum"]["erc20_withdraw"]["signed"]["json"]
    assert erc20_withdraw_signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["ethereum"]["erc20_withdraw"]["signed"]["transaction_raw"]
    )


def test_ethereum_erc20_refund_signature():

    unsigned_erc20_refund_transaction_raw = _["ethereum"]["erc20_refund"]["unsigned"]["transaction_raw"]

    erc20_refund_solver = RefundSolver(
        xprivate_key=_["ethereum"]["wallet"]["sender"]["root_xprivate_key"],
        path=_["ethereum"]["wallet"]["sender"]["derivation"]["path"],
        account=_["ethereum"]["wallet"]["sender"]["derivation"]["account"],
        change=_["ethereum"]["wallet"]["sender"]["derivation"]["change"],
        address=_["ethereum"]["wallet"]["sender"]["derivation"]["address"]
    )

    signature = Signature(network=_["ethereum"]["network"], erc20=True).sign(
        transaction_raw=unsigned_erc20_refund_transaction_raw,
        solver=erc20_refund_solver
    )

    assert signature.type() == _["ethereum"]["erc20_refund"]["signed"]["type"]
    assert signature.fee() == _["ethereum"]["erc20_refund"]["signed"]["fee"]
    assert signature.hash() == _["ethereum"]["erc20_refund"]["signed"]["hash"]
    assert signature.raw() == _["ethereum"]["erc20_refund"]["signed"]["raw"]
    assert signature.json() == _["ethereum"]["erc20_refund"]["signed"]["json"]
    assert signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["ethereum"]["erc20_refund"]["signed"]["transaction_raw"]
    )

    erc20_refund_signature = RefundSignature(network=_["ethereum"]["network"], erc20=True).sign(
        transaction_raw=unsigned_erc20_refund_transaction_raw,
        solver=erc20_refund_solver
    )

    assert erc20_refund_signature.type() == _["ethereum"]["erc20_refund"]["signed"]["type"]
    assert erc20_refund_signature.fee() == _["ethereum"]["erc20_refund"]["signed"]["fee"]
    assert erc20_refund_signature.hash() == _["ethereum"]["erc20_refund"]["signed"]["hash"]
    assert erc20_refund_signature.raw() == _["ethereum"]["erc20_refund"]["signed"]["raw"]
    assert erc20_refund_signature.json() == _["ethereum"]["erc20_refund"]["signed"]["json"]
    assert erc20_refund_signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["ethereum"]["erc20_refund"]["signed"]["transaction_raw"]
    )
