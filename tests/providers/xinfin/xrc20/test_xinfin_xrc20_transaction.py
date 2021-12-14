#!/usr/bin/env python3

import json
import os

from swap.providers.xinfin.htlc import HTLC
from swap.providers.xinfin.transaction import (
    NormalTransaction, FundTransaction, WithdrawTransaction, RefundTransaction
)
from swap.providers.xinfin.solver import (
    NormalSolver, FundSolver, WithdrawSolver, RefundSolver
)
from swap.utils import get_current_timestamp

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_xinfin_xrc20_normal_transaction():

    unsigned_xrc20_normal_transaction = NormalTransaction(network=_["xinfin"]["network"], xrc20=True)

    unsigned_xrc20_normal_transaction.build_transaction(
        address=_["xinfin"]["wallet"]["sender"]["address"],
        recipient={
            _["xinfin"]["wallet"]["recipient"]["address"]: _["xinfin"]["xrc20_amount"] * (10 ** _["xinfin"]["decimals"])
        },
        token_address=_["xinfin"]["xrc20_htlc"]["agreements"]["token_address"]
    )

    assert unsigned_xrc20_normal_transaction.type() == _["xinfin"]["xrc20_normal"]["unsigned"]["type"]
    assert unsigned_xrc20_normal_transaction.fee() == _["xinfin"]["xrc20_normal"]["unsigned"]["fee"]
    assert unsigned_xrc20_normal_transaction.hash() == _["xinfin"]["xrc20_normal"]["unsigned"]["hash"]
    assert unsigned_xrc20_normal_transaction.raw() == _["xinfin"]["xrc20_normal"]["unsigned"]["raw"]
    assert isinstance(unsigned_xrc20_normal_transaction.json(), dict)
    assert unsigned_xrc20_normal_transaction.signature() == _["xinfin"]["xrc20_normal"]["unsigned"]["signature"]
    assert isinstance(unsigned_xrc20_normal_transaction.transaction_raw(), str)

    signed_xrc20_normal_transaction = unsigned_xrc20_normal_transaction.sign(
        solver=NormalSolver(
            xprivate_key=_["xinfin"]["wallet"]["sender"]["root_xprivate_key"],
            path=_["xinfin"]["wallet"]["sender"]["derivation"]["path"],
            account=_["xinfin"]["wallet"]["sender"]["derivation"]["account"],
            change=_["xinfin"]["wallet"]["sender"]["derivation"]["change"],
            address=_["xinfin"]["wallet"]["sender"]["derivation"]["address"]
        )
    )

    assert signed_xrc20_normal_transaction.type() == _["xinfin"]["xrc20_normal"]["signed"]["type"]
    assert signed_xrc20_normal_transaction.fee() == _["xinfin"]["xrc20_normal"]["signed"]["fee"]
    assert isinstance(signed_xrc20_normal_transaction.hash(), str)
    assert isinstance(signed_xrc20_normal_transaction.raw(), str)
    assert isinstance(signed_xrc20_normal_transaction.json(), dict)
    assert isinstance(signed_xrc20_normal_transaction.signature(), dict)
    assert isinstance(signed_xrc20_normal_transaction.transaction_raw(), str)


def test_xinfin_xrc20_fund_transaction():

    xrc20_htlc = HTLC(
        contract_address=_["xinfin"]["xrc20_htlc"]["contract_address"],
        network=_["xinfin"]["network"],
        xrc20=True
    ).build_htlc(
        secret_hash=_["xinfin"]["xrc20_htlc"]["secret"]["hash"],
        recipient_address=_["xinfin"]["wallet"]["recipient"]["address"],
        sender_address=_["xinfin"]["wallet"]["sender"]["address"],
        endtime=get_current_timestamp(plus=3600),
        token_address=_["xinfin"]["xrc20_htlc"]["agreements"]["token_address"]
    )

    unsigned_xrc20_fund_transaction = FundTransaction(network=_["xinfin"]["network"], xrc20=True)

    unsigned_xrc20_fund_transaction.build_transaction(
        address=_["xinfin"]["wallet"]["sender"]["address"],
        htlc=xrc20_htlc,
        amount=_["xinfin"]["xrc20_amount"] * (10 ** _["xinfin"]["decimals"])
    )

    assert unsigned_xrc20_fund_transaction.type() == _["xinfin"]["xrc20_fund"]["unsigned"]["type"]
    assert unsigned_xrc20_fund_transaction.fee() == _["xinfin"]["xrc20_fund"]["unsigned"]["fee"]
    assert unsigned_xrc20_fund_transaction.hash() == _["xinfin"]["xrc20_fund"]["unsigned"]["hash"]
    assert unsigned_xrc20_fund_transaction.raw() == _["xinfin"]["xrc20_fund"]["unsigned"]["raw"]
    assert isinstance(unsigned_xrc20_fund_transaction.json(), dict)
    assert unsigned_xrc20_fund_transaction.signature() == _["xinfin"]["xrc20_fund"]["unsigned"]["signature"]
    assert isinstance(unsigned_xrc20_fund_transaction.transaction_raw(), str)

    signed_xrc20_fund_transaction = unsigned_xrc20_fund_transaction.sign(
        solver=FundSolver(
            xprivate_key=_["xinfin"]["wallet"]["sender"]["root_xprivate_key"],
            path=_["xinfin"]["wallet"]["sender"]["derivation"]["path"],
            account=_["xinfin"]["wallet"]["sender"]["derivation"]["account"],
            change=_["xinfin"]["wallet"]["sender"]["derivation"]["change"],
            address=_["xinfin"]["wallet"]["sender"]["derivation"]["address"]
        )
    )

    assert signed_xrc20_fund_transaction.type() == _["xinfin"]["xrc20_fund"]["signed"]["type"]
    assert signed_xrc20_fund_transaction.fee() == _["xinfin"]["xrc20_fund"]["signed"]["fee"]
    assert isinstance(signed_xrc20_fund_transaction.hash(), str)
    assert isinstance(signed_xrc20_fund_transaction.raw(), str)
    assert isinstance(signed_xrc20_fund_transaction.json(), dict)
    assert isinstance(signed_xrc20_fund_transaction.signature(), dict)
    assert isinstance(signed_xrc20_fund_transaction.transaction_raw(), str)


def test_xinfin_xrc20_withdraw_transaction():

    unsigned_xrc20_withdraw_transaction = WithdrawTransaction(network=_["xinfin"]["network"], xrc20=True)

    unsigned_xrc20_withdraw_transaction.build_transaction(
        address=_["xinfin"]["wallet"]["recipient"]["address"],
        transaction_hash=_["xinfin"]["xrc20_transaction_hash"],
        secret_key=_["xinfin"]["xrc20_htlc"]["secret"]["key"]
    )

    assert unsigned_xrc20_withdraw_transaction.type() == _["xinfin"]["xrc20_withdraw"]["unsigned"]["type"]
    assert unsigned_xrc20_withdraw_transaction.fee() == _["xinfin"]["xrc20_withdraw"]["unsigned"]["fee"]
    assert unsigned_xrc20_withdraw_transaction.hash() == _["xinfin"]["xrc20_withdraw"]["unsigned"]["hash"]
    assert unsigned_xrc20_withdraw_transaction.raw() == _["xinfin"]["xrc20_withdraw"]["unsigned"]["raw"]
    assert isinstance(unsigned_xrc20_withdraw_transaction.json(), dict)
    assert unsigned_xrc20_withdraw_transaction.signature() == _["xinfin"]["xrc20_withdraw"]["unsigned"]["signature"]
    assert isinstance(unsigned_xrc20_withdraw_transaction.transaction_raw(), str)

    signed_xrc20_withdraw_transaction = unsigned_xrc20_withdraw_transaction.sign(
        solver=WithdrawSolver(
            xprivate_key=_["xinfin"]["wallet"]["recipient"]["root_xprivate_key"],
            path=_["xinfin"]["wallet"]["recipient"]["derivation"]["path"],
            account=_["xinfin"]["wallet"]["recipient"]["derivation"]["account"],
            change=_["xinfin"]["wallet"]["recipient"]["derivation"]["change"],
            address=_["xinfin"]["wallet"]["recipient"]["derivation"]["address"]
        )
    )

    assert signed_xrc20_withdraw_transaction.type() == _["xinfin"]["xrc20_withdraw"]["signed"]["type"]
    assert signed_xrc20_withdraw_transaction.fee() == _["xinfin"]["xrc20_withdraw"]["signed"]["fee"]
    assert isinstance(signed_xrc20_withdraw_transaction.hash(), str)
    assert isinstance(signed_xrc20_withdraw_transaction.raw(), str)
    assert isinstance(signed_xrc20_withdraw_transaction.json(), dict)
    assert isinstance(signed_xrc20_withdraw_transaction.signature(), dict)
    assert isinstance(signed_xrc20_withdraw_transaction.transaction_raw(), str)


def test_xinfin_xrc20_refund_transaction():

    unsigned_xrc20_refund_transaction = RefundTransaction(network=_["xinfin"]["network"], xrc20=True)

    unsigned_xrc20_refund_transaction.build_transaction(
        address=_["xinfin"]["wallet"]["sender"]["address"],
        transaction_hash=_["xinfin"]["xrc20_transaction_hash"]
    )

    assert unsigned_xrc20_refund_transaction.type() == _["xinfin"]["xrc20_refund"]["unsigned"]["type"]
    assert unsigned_xrc20_refund_transaction.fee() == _["xinfin"]["xrc20_refund"]["unsigned"]["fee"]
    assert unsigned_xrc20_refund_transaction.hash() == _["xinfin"]["xrc20_refund"]["unsigned"]["hash"]
    assert unsigned_xrc20_refund_transaction.raw() == _["xinfin"]["xrc20_refund"]["unsigned"]["raw"]
    assert isinstance(unsigned_xrc20_refund_transaction.json(), dict)
    assert unsigned_xrc20_refund_transaction.signature() == _["xinfin"]["xrc20_refund"]["unsigned"]["signature"]
    assert isinstance(unsigned_xrc20_refund_transaction.transaction_raw(), str)

    signed_xrc20_refund_transaction = unsigned_xrc20_refund_transaction.sign(
        solver=RefundSolver(
            xprivate_key=_["xinfin"]["wallet"]["sender"]["root_xprivate_key"],
            path=_["xinfin"]["wallet"]["sender"]["derivation"]["path"],
            account=_["xinfin"]["wallet"]["sender"]["derivation"]["account"],
            change=_["xinfin"]["wallet"]["sender"]["derivation"]["change"],
            address=_["xinfin"]["wallet"]["sender"]["derivation"]["address"]
        )
    )

    assert signed_xrc20_refund_transaction.type() == _["xinfin"]["xrc20_refund"]["signed"]["type"]
    assert signed_xrc20_refund_transaction.fee() == _["xinfin"]["xrc20_refund"]["signed"]["fee"]
    assert isinstance(signed_xrc20_refund_transaction.hash(), str)
    assert isinstance(signed_xrc20_refund_transaction.raw(), str)
    assert isinstance(signed_xrc20_refund_transaction.json(), dict)
    assert isinstance(signed_xrc20_refund_transaction.signature(), dict)
    assert isinstance(signed_xrc20_refund_transaction.transaction_raw(), str)
