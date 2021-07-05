#!/usr/bin/env python3

import json
import os

from swap.providers.xinfin.wallet import Wallet
from swap.providers.xinfin.solver import (
    FundSolver, WithdrawSolver, RefundSolver
)

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_xinfin_fund_solver():

    fund_solver = FundSolver(
        xprivate_key=_["xinfin"]["wallet"]["sender"]["root_xprivate_key"],
        path=_["xinfin"]["wallet"]["sender"]["derivation"]["path"],
        account=_["xinfin"]["wallet"]["sender"]["derivation"]["account"],
        change=_["xinfin"]["wallet"]["sender"]["derivation"]["change"],
        address=_["xinfin"]["wallet"]["sender"]["derivation"]["address"]
    )

    assert isinstance(fund_solver.solve(network=_["xinfin"]["network"]), Wallet)


def test_xinfin_withdraw_solver():

    withdraw_solver = WithdrawSolver(
        xprivate_key=_["xinfin"]["wallet"]["recipient"]["root_xprivate_key"],
        path=_["xinfin"]["wallet"]["recipient"]["derivation"]["path"],
        account=_["xinfin"]["wallet"]["recipient"]["derivation"]["account"],
        change=_["xinfin"]["wallet"]["recipient"]["derivation"]["change"],
        address=_["xinfin"]["wallet"]["recipient"]["derivation"]["address"]
    )

    assert isinstance(withdraw_solver.solve(network=_["xinfin"]["network"]), Wallet)


def test_xinfin_refund_solver():

    refund_solver = RefundSolver(
        xprivate_key=_["xinfin"]["wallet"]["sender"]["root_xprivate_key"],
        path=_["xinfin"]["wallet"]["sender"]["derivation"]["path"],
        account=_["xinfin"]["wallet"]["sender"]["derivation"]["account"],
        change=_["xinfin"]["wallet"]["sender"]["derivation"]["change"],
        address=_["xinfin"]["wallet"]["sender"]["derivation"]["address"]
    )

    assert isinstance(refund_solver.solve(network=_["xinfin"]["network"]), Wallet)
