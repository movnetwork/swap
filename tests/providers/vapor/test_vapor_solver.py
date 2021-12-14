#!/usr/bin/env python3

import json
import os

from swap.providers.vapor.solver import (
    NormalSolver, FundSolver, WithdrawSolver, RefundSolver
)

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_vapor_normal_solver():

    normal_solver = NormalSolver(
        xprivate_key=_["vapor"]["wallet"]["sender"]["xprivate_key"],
        path=_["vapor"]["wallet"]["sender"]["derivation"]["path"],
        account=_["vapor"]["wallet"]["sender"]["derivation"]["account"],
        change=_["vapor"]["wallet"]["sender"]["derivation"]["change"],
        address=_["vapor"]["wallet"]["sender"]["derivation"]["address"]
    )

    assert isinstance(normal_solver.solve(network=_["vapor"]["network"]), tuple)


def test_vapor_fund_solver():

    fund_solver = FundSolver(
        xprivate_key=_["vapor"]["wallet"]["sender"]["xprivate_key"],
        path=_["vapor"]["wallet"]["sender"]["derivation"]["path"],
        account=_["vapor"]["wallet"]["sender"]["derivation"]["account"],
        change=_["vapor"]["wallet"]["sender"]["derivation"]["change"],
        address=_["vapor"]["wallet"]["sender"]["derivation"]["address"]
    )

    assert isinstance(fund_solver.solve(network=_["vapor"]["network"]), tuple)


def test_vapor_withdraw_solver():

    withdraw_solver = WithdrawSolver(
        xprivate_key=_["vapor"]["wallet"]["recipient"]["xprivate_key"],
        secret_key=_["vapor"]["htlc"]["secret"]["key"],
        bytecode=_["vapor"]["htlc"]["bytecode"],
        path=_["vapor"]["wallet"]["recipient"]["derivation"]["path"],
        account=_["vapor"]["wallet"]["recipient"]["derivation"]["account"],
        change=_["vapor"]["wallet"]["recipient"]["derivation"]["change"],
        address=_["vapor"]["wallet"]["recipient"]["derivation"]["address"]
    )

    assert isinstance(withdraw_solver.solve(network=_["vapor"]["network"]), tuple)
    assert isinstance(withdraw_solver.witness(network=_["vapor"]["network"]), str)


def test_vapor_refund_solver():

    refund_solver = RefundSolver(
        xprivate_key=_["vapor"]["wallet"]["sender"]["xprivate_key"],
        bytecode=_["vapor"]["htlc"]["bytecode"],
        path=_["vapor"]["wallet"]["sender"]["derivation"]["path"],
        account=_["vapor"]["wallet"]["sender"]["derivation"]["account"],
        change=_["vapor"]["wallet"]["sender"]["derivation"]["change"],
        address=_["vapor"]["wallet"]["sender"]["derivation"]["address"]
    )

    assert isinstance(refund_solver.solve(network=_["vapor"]["network"]), tuple)
    assert isinstance(refund_solver.witness(network=_["vapor"]["network"]), str)
