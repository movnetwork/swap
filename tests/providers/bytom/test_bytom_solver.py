#!/usr/bin/env python3

from btcpy.structs.sig import (
    P2pkhSolver, IfElseSolver
)

import json
import os

from swap.providers.bytom.solver import (
    FundSolver, ClaimSolver, RefundSolver
)

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_bytom_fund_solver():

    fund_solver = FundSolver(
        xprivate_key=_["bytom"]["wallet"]["sender"]["xprivate_key"],
        path=_["bytom"]["wallet"]["sender"]["derivation"]["path"],
        account=_["bytom"]["wallet"]["sender"]["derivation"]["account"],
        change=_["bytom"]["wallet"]["sender"]["derivation"]["change"],
        address=_["bytom"]["wallet"]["sender"]["derivation"]["address"]
    )

    assert isinstance(fund_solver.solve(network=_["bytom"]["network"]), tuple)


def test_bytom_claim_solver():

    claim_solver = ClaimSolver(
        xprivate_key=_["bytom"]["wallet"]["recipient"]["xprivate_key"],
        secret_key=_["bytom"]["htlc"]["secret"]["key"],
        bytecode=_["bytom"]["htlc"]["bytecode"],
        path=_["bytom"]["wallet"]["recipient"]["derivation"]["path"],
        account=_["bytom"]["wallet"]["recipient"]["derivation"]["account"],
        change=_["bytom"]["wallet"]["recipient"]["derivation"]["change"],
        address=_["bytom"]["wallet"]["recipient"]["derivation"]["address"]
    )

    assert isinstance(claim_solver.solve(network=_["bytom"]["network"]), tuple)
    assert isinstance(claim_solver.witness(network=_["bytom"]["network"]), str)


def test_bytom_refund_solver():

    refund_solver = RefundSolver(
        xprivate_key=_["bytom"]["wallet"]["sender"]["xprivate_key"],
        bytecode=_["bytom"]["htlc"]["bytecode"],
        path=_["bytom"]["wallet"]["sender"]["derivation"]["path"],
        account=_["bytom"]["wallet"]["sender"]["derivation"]["account"],
        change=_["bytom"]["wallet"]["sender"]["derivation"]["change"],
        address=_["bytom"]["wallet"]["sender"]["derivation"]["address"]
    )

    assert isinstance(refund_solver.solve(network=_["bytom"]["network"]), tuple)
    assert isinstance(refund_solver.witness(network=_["bytom"]["network"]), str)
