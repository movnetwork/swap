#!/usr/bin/env python3

import json
import os

from swap.providers.vapor.signature import (
    Signature, NormalSignature, FundSignature, ClaimSignature, RefundSignature
)
from swap.providers.vapor.solver import (
    NormalSolver, FundSolver, ClaimSolver, RefundSolver
)
from swap.utils import clean_transaction_raw

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_vapor_normal_signature():

    unsigned_normal_transaction_raw = _["vapor"]["normal"]["unsigned"]["transaction_raw"]

    normal_solver = NormalSolver(
        xprivate_key=_["vapor"]["wallet"]["sender"]["xprivate_key"],
        path=_["vapor"]["wallet"]["sender"]["derivation"]["path"],
        account=_["vapor"]["wallet"]["sender"]["derivation"]["account"],
        change=_["vapor"]["wallet"]["sender"]["derivation"]["change"],
        address=_["vapor"]["wallet"]["sender"]["derivation"]["address"]
    )

    signature = Signature(network=_["vapor"]["network"]).sign(
        transaction_raw=unsigned_normal_transaction_raw,
        solver=normal_solver
    )

    assert signature.type() == _["vapor"]["normal"]["signed"]["type"]
    assert signature.fee() == _["vapor"]["normal"]["signed"]["fee"]
    assert signature.hash() == _["vapor"]["normal"]["signed"]["hash"]
    assert signature.raw() == _["vapor"]["normal"]["signed"]["raw"]
    # assert signature.json() == _["vapor"]["normal"]["signed"]["json"]
    assert signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["vapor"]["normal"]["signed"]["transaction_raw"]
    )

    normal_signature = NormalSignature(network=_["vapor"]["network"]).sign(
        transaction_raw=unsigned_normal_transaction_raw,
        solver=normal_solver
    )

    assert normal_signature.type() == _["vapor"]["normal"]["signed"]["type"]
    assert normal_signature.fee() == _["vapor"]["normal"]["signed"]["fee"]
    assert normal_signature.hash() == _["vapor"]["normal"]["signed"]["hash"]
    assert normal_signature.raw() == _["vapor"]["normal"]["signed"]["raw"]
    # assert normal_signature.json() == _["vapor"]["normal"]["signed"]["json"]
    assert normal_signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["vapor"]["normal"]["signed"]["transaction_raw"]
    )


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


def test_vapor_claim_signature():

    unsigned_claim_transaction_raw = _["vapor"]["claim"]["unsigned"]["transaction_raw"]

    claim_solver = ClaimSolver(
        xprivate_key=_["vapor"]["wallet"]["recipient"]["xprivate_key"],
        secret_key=_["vapor"]["htlc"]["secret"]["key"],
        bytecode=_["vapor"]["htlc"]["bytecode"],
        path=_["vapor"]["wallet"]["recipient"]["derivation"]["path"],
        account=_["vapor"]["wallet"]["recipient"]["derivation"]["account"],
        change=_["vapor"]["wallet"]["recipient"]["derivation"]["change"],
        address=_["vapor"]["wallet"]["recipient"]["derivation"]["address"]
    )

    signature = Signature(network=_["vapor"]["network"]).sign(
        transaction_raw=unsigned_claim_transaction_raw,
        solver=claim_solver
    )

    assert signature.type() == _["vapor"]["claim"]["signed"]["type"]
    assert signature.fee() == _["vapor"]["claim"]["signed"]["fee"]
    assert signature.hash() == _["vapor"]["claim"]["signed"]["hash"]
    assert signature.raw() == _["vapor"]["claim"]["signed"]["raw"]
    # assert signature.json() == _["vapor"]["claim"]["signed"]["json"]
    assert signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["vapor"]["claim"]["signed"]["transaction_raw"]
    )

    claim_signature = ClaimSignature(network=_["vapor"]["network"]).sign(
        transaction_raw=unsigned_claim_transaction_raw,
        solver=claim_solver
    )

    assert claim_signature.type() == _["vapor"]["claim"]["signed"]["type"]
    assert claim_signature.fee() == _["vapor"]["claim"]["signed"]["fee"]
    assert claim_signature.hash() == _["vapor"]["claim"]["signed"]["hash"]
    assert claim_signature.raw() == _["vapor"]["claim"]["signed"]["raw"]
    # assert claim_signature.json() == _["vapor"]["claim"]["signed"]["json"]
    assert claim_signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["vapor"]["claim"]["signed"]["transaction_raw"]
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
