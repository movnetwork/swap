#!/usr/bin/env python3

import json
import os

from swap.providers.xinfin.wallet import Wallet
from swap.providers.xinfin.solver import (
    NormalSolver, FundSolver, WithdrawSolver, RefundSolver
)

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_xinfin_xrc20_normal_solver():

    xrc20_normal_solver = NormalSolver(
        xprivate_key=_["xinfin"]["wallet"]["sender"]["root_xprivate_key"],
        path=_["xinfin"]["wallet"]["sender"]["derivation"]["path"],
        account=_["xinfin"]["wallet"]["sender"]["derivation"]["account"],
        change=_["xinfin"]["wallet"]["sender"]["derivation"]["change"],
        address=_["xinfin"]["wallet"]["sender"]["derivation"]["address"]
    )

    assert isinstance(xrc20_normal_solver.solve(network=_["xinfin"]["network"]), Wallet)


def test_xinfin_xrc20_fund_solver():

    xrc20_fund_solver = FundSolver(
        xprivate_key=_["xinfin"]["wallet"]["sender"]["root_xprivate_key"],
        path=_["xinfin"]["wallet"]["sender"]["derivation"]["path"],
        account=_["xinfin"]["wallet"]["sender"]["derivation"]["account"],
        change=_["xinfin"]["wallet"]["sender"]["derivation"]["change"],
        address=_["xinfin"]["wallet"]["sender"]["derivation"]["address"]
    )

    assert isinstance(xrc20_fund_solver.solve(network=_["xinfin"]["network"]), Wallet)


def test_xinfin_xrc20_withdraw_solver():

    xrc20_withdraw_solver = WithdrawSolver(
        xprivate_key=_["xinfin"]["wallet"]["recipient"]["root_xprivate_key"],
        path=_["xinfin"]["wallet"]["recipient"]["derivation"]["path"],
        account=_["xinfin"]["wallet"]["recipient"]["derivation"]["account"],
        change=_["xinfin"]["wallet"]["recipient"]["derivation"]["change"],
        address=_["xinfin"]["wallet"]["recipient"]["derivation"]["address"]
    )

    assert isinstance(xrc20_withdraw_solver.solve(network=_["xinfin"]["network"]), Wallet)


def test_xinfin_xrc20_refund_solver():

    xrc20_refund_solver = RefundSolver(
        xprivate_key=_["xinfin"]["wallet"]["sender"]["root_xprivate_key"],
        path=_["xinfin"]["wallet"]["sender"]["derivation"]["path"],
        account=_["xinfin"]["wallet"]["sender"]["derivation"]["account"],
        change=_["xinfin"]["wallet"]["sender"]["derivation"]["change"],
        address=_["xinfin"]["wallet"]["sender"]["derivation"]["address"]
    )

    assert isinstance(xrc20_refund_solver.solve(network=_["xinfin"]["network"]), Wallet)
