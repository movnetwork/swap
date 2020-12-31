#!/usr/bin/env python3

import json
import os

from swap.providers.bitcoin.signature import (
    Signature, NormalSignature, FundSignature, ClaimSignature, RefundSignature
)
from swap.providers.bitcoin.solver import (
    NormalSolver, FundSolver, ClaimSolver, RefundSolver
)
from swap.utils import clean_transaction_raw

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_bitcoin_normal_signature():

    unsigned_normal_transaction_raw = _["bitcoin"]["normal"]["unsigned"]["transaction_raw"]

    normal_solver = NormalSolver(
        root_xprivate_key=_["bitcoin"]["wallet"]["sender"]["root_xprivate_key"],
        path=_["bitcoin"]["wallet"]["sender"]["derivation"]["path"],
        account=_["bitcoin"]["wallet"]["sender"]["derivation"]["account"],
        change=_["bitcoin"]["wallet"]["sender"]["derivation"]["change"],
        address=_["bitcoin"]["wallet"]["sender"]["derivation"]["address"]
    )

    signature = Signature(network=_["bitcoin"]["network"]).sign(
        transaction_raw=unsigned_normal_transaction_raw,
        solver=normal_solver
    )

    assert signature.type() == _["bitcoin"]["normal"]["signed"]["type"]
    assert signature.fee() == _["bitcoin"]["normal"]["signed"]["fee"]
    assert signature.hash() == _["bitcoin"]["normal"]["signed"]["hash"]
    assert signature.raw() == _["bitcoin"]["normal"]["signed"]["raw"]
    assert signature.json() == _["bitcoin"]["normal"]["signed"]["json"]
    assert signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bitcoin"]["normal"]["signed"]["transaction_raw"]
    )

    normal_signature = NormalSignature(network=_["bitcoin"]["network"]).sign(
        transaction_raw=unsigned_normal_transaction_raw,
        solver=normal_solver
    )

    assert normal_signature.type() == _["bitcoin"]["normal"]["signed"]["type"]
    assert normal_signature.fee() == _["bitcoin"]["normal"]["signed"]["fee"]
    assert normal_signature.hash() == _["bitcoin"]["normal"]["signed"]["hash"]
    assert normal_signature.raw() == _["bitcoin"]["normal"]["signed"]["raw"]
    assert normal_signature.json() == _["bitcoin"]["normal"]["signed"]["json"]
    assert normal_signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bitcoin"]["normal"]["signed"]["transaction_raw"]
    )


def test_bitcoin_fund_signature():

    unsigned_fund_transaction_raw = _["bitcoin"]["fund"]["unsigned"]["transaction_raw"]

    fund_solver = FundSolver(
        root_xprivate_key=_["bitcoin"]["wallet"]["sender"]["root_xprivate_key"],
        path=_["bitcoin"]["wallet"]["sender"]["derivation"]["path"],
        account=_["bitcoin"]["wallet"]["sender"]["derivation"]["account"],
        change=_["bitcoin"]["wallet"]["sender"]["derivation"]["change"],
        address=_["bitcoin"]["wallet"]["sender"]["derivation"]["address"]
    )

    signature = Signature(network=_["bitcoin"]["network"]).sign(
        transaction_raw=unsigned_fund_transaction_raw,
        solver=fund_solver
    )

    assert signature.type() == _["bitcoin"]["fund"]["signed"]["type"]
    assert signature.fee() == _["bitcoin"]["fund"]["signed"]["fee"]
    assert signature.hash() == _["bitcoin"]["fund"]["signed"]["hash"]
    assert signature.raw() == _["bitcoin"]["fund"]["signed"]["raw"]
    assert signature.json() == _["bitcoin"]["fund"]["signed"]["json"]
    assert signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bitcoin"]["fund"]["signed"]["transaction_raw"]
    )

    fund_signature = FundSignature(network=_["bitcoin"]["network"]).sign(
        transaction_raw=unsigned_fund_transaction_raw,
        solver=fund_solver
    )

    assert fund_signature.type() == _["bitcoin"]["fund"]["signed"]["type"]
    assert fund_signature.fee() == _["bitcoin"]["fund"]["signed"]["fee"]
    assert fund_signature.hash() == _["bitcoin"]["fund"]["signed"]["hash"]
    assert fund_signature.raw() == _["bitcoin"]["fund"]["signed"]["raw"]
    assert fund_signature.json() == _["bitcoin"]["fund"]["signed"]["json"]
    assert fund_signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bitcoin"]["fund"]["signed"]["transaction_raw"]
    )


def test_bitcoin_claim_signature():

    unsigned_claim_transaction_raw = _["bitcoin"]["claim"]["unsigned"]["transaction_raw"]

    claim_solver = ClaimSolver(
        root_xprivate_key=_["bitcoin"]["wallet"]["recipient"]["root_xprivate_key"],
        secret_key=_["bitcoin"]["htlc"]["secret"]["key"],
        bytecode=_["bitcoin"]["htlc"]["bytecode"],
        path=_["bitcoin"]["wallet"]["recipient"]["derivation"]["path"],
        account=_["bitcoin"]["wallet"]["recipient"]["derivation"]["account"],
        change=_["bitcoin"]["wallet"]["recipient"]["derivation"]["change"],
        address=_["bitcoin"]["wallet"]["recipient"]["derivation"]["address"]
    )

    signature = Signature(network=_["bitcoin"]["network"]).sign(
        transaction_raw=unsigned_claim_transaction_raw,
        solver=claim_solver
    )

    assert signature.type() == _["bitcoin"]["claim"]["signed"]["type"]
    assert signature.fee() == _["bitcoin"]["claim"]["signed"]["fee"]
    assert signature.hash() == _["bitcoin"]["claim"]["signed"]["hash"]
    assert signature.raw() == _["bitcoin"]["claim"]["signed"]["raw"]
    assert signature.json() == _["bitcoin"]["claim"]["signed"]["json"]
    assert signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bitcoin"]["claim"]["signed"]["transaction_raw"]
    )

    claim_signature = ClaimSignature(network=_["bitcoin"]["network"]).sign(
        transaction_raw=unsigned_claim_transaction_raw,
        solver=claim_solver
    )

    assert claim_signature.type() == _["bitcoin"]["claim"]["signed"]["type"]
    assert claim_signature.fee() == _["bitcoin"]["claim"]["signed"]["fee"]
    assert claim_signature.hash() == _["bitcoin"]["claim"]["signed"]["hash"]
    assert claim_signature.raw() == _["bitcoin"]["claim"]["signed"]["raw"]
    assert claim_signature.json() == _["bitcoin"]["claim"]["signed"]["json"]
    assert claim_signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bitcoin"]["claim"]["signed"]["transaction_raw"]
    )


def test_bitcoin_refund_signature():

    unsigned_refund_transaction_raw = _["bitcoin"]["refund"]["unsigned"]["transaction_raw"]

    refund_solver = RefundSolver(
        root_xprivate_key=_["bitcoin"]["wallet"]["sender"]["root_xprivate_key"],
        bytecode=_["bitcoin"]["htlc"]["bytecode"],
        sequence=_["bitcoin"]["htlc"]["sequence"],
        path=_["bitcoin"]["wallet"]["sender"]["derivation"]["path"],
        account=_["bitcoin"]["wallet"]["sender"]["derivation"]["account"],
        change=_["bitcoin"]["wallet"]["sender"]["derivation"]["change"],
        address=_["bitcoin"]["wallet"]["sender"]["derivation"]["address"]
    )

    signature = Signature(network=_["bitcoin"]["network"]).sign(
        transaction_raw=unsigned_refund_transaction_raw,
        solver=refund_solver
    )

    assert signature.type() == _["bitcoin"]["refund"]["signed"]["type"]
    assert signature.fee() == _["bitcoin"]["refund"]["signed"]["fee"]
    assert signature.hash() == _["bitcoin"]["refund"]["signed"]["hash"]
    assert signature.raw() == _["bitcoin"]["refund"]["signed"]["raw"]
    assert signature.json() == _["bitcoin"]["refund"]["signed"]["json"]
    assert signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bitcoin"]["refund"]["signed"]["transaction_raw"]
    )

    refund_signature = RefundSignature(network=_["bitcoin"]["network"]).sign(
        transaction_raw=unsigned_refund_transaction_raw,
        solver=refund_solver
    )

    assert refund_signature.type() == _["bitcoin"]["refund"]["signed"]["type"]
    assert refund_signature.fee() == _["bitcoin"]["refund"]["signed"]["fee"]
    assert refund_signature.hash() == _["bitcoin"]["refund"]["signed"]["hash"]
    assert refund_signature.raw() == _["bitcoin"]["refund"]["signed"]["raw"]
    assert refund_signature.json() == _["bitcoin"]["refund"]["signed"]["json"]
    assert refund_signature.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["bitcoin"]["refund"]["signed"]["transaction_raw"]
    )
