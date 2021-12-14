#!/usr/bin/env python3

import json
import os

from swap.providers.ethereum.wallet import Wallet
from swap.providers.ethereum.solver import (
    NormalSolver, FundSolver, WithdrawSolver, RefundSolver
)

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_ethereum_erc20_normal_solver():

    erc20_normal_solver = NormalSolver(
        xprivate_key=_["ethereum"]["wallet"]["sender"]["root_xprivate_key"],
        path=_["ethereum"]["wallet"]["sender"]["derivation"]["path"],
        account=_["ethereum"]["wallet"]["sender"]["derivation"]["account"],
        change=_["ethereum"]["wallet"]["sender"]["derivation"]["change"],
        address=_["ethereum"]["wallet"]["sender"]["derivation"]["address"]
    )

    assert isinstance(erc20_normal_solver.solve(network=_["ethereum"]["network"]), Wallet)


def test_ethereum_erc20_fund_solver():

    erc20_fund_solver = FundSolver(
        xprivate_key=_["ethereum"]["wallet"]["sender"]["root_xprivate_key"],
        path=_["ethereum"]["wallet"]["sender"]["derivation"]["path"],
        account=_["ethereum"]["wallet"]["sender"]["derivation"]["account"],
        change=_["ethereum"]["wallet"]["sender"]["derivation"]["change"],
        address=_["ethereum"]["wallet"]["sender"]["derivation"]["address"]
    )

    assert isinstance(erc20_fund_solver.solve(network=_["ethereum"]["network"]), Wallet)


def test_ethereum_erc20_withdraw_solver():

    erc20_withdraw_solver = WithdrawSolver(
        xprivate_key=_["ethereum"]["wallet"]["recipient"]["root_xprivate_key"],
        path=_["ethereum"]["wallet"]["recipient"]["derivation"]["path"],
        account=_["ethereum"]["wallet"]["recipient"]["derivation"]["account"],
        change=_["ethereum"]["wallet"]["recipient"]["derivation"]["change"],
        address=_["ethereum"]["wallet"]["recipient"]["derivation"]["address"]
    )

    assert isinstance(erc20_withdraw_solver.solve(network=_["ethereum"]["network"]), Wallet)


def test_ethereum_erc20_refund_solver():

    erc20_refund_solver = RefundSolver(
        xprivate_key=_["ethereum"]["wallet"]["sender"]["root_xprivate_key"],
        path=_["ethereum"]["wallet"]["sender"]["derivation"]["path"],
        account=_["ethereum"]["wallet"]["sender"]["derivation"]["account"],
        change=_["ethereum"]["wallet"]["sender"]["derivation"]["change"],
        address=_["ethereum"]["wallet"]["sender"]["derivation"]["address"]
    )

    assert isinstance(erc20_refund_solver.solve(network=_["ethereum"]["network"]), Wallet)
