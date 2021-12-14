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
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_xinfin_normal_transaction():

    unsigned_normal_transaction = NormalTransaction(network=_["xinfin"]["network"])

    unsigned_normal_transaction.build_transaction(
        address=_["xinfin"]["wallet"]["sender"]["address"],
        recipient={
            _["xinfin"]["wallet"]["recipient"]["address"]: _["xinfin"]["amount"]
        },
        unit=_["xinfin"]["unit"]
    )

    assert unsigned_normal_transaction.type() == _["xinfin"]["normal"]["unsigned"]["type"]
    assert unsigned_normal_transaction.fee() == _["xinfin"]["normal"]["unsigned"]["fee"]
    assert unsigned_normal_transaction.hash() == _["xinfin"]["normal"]["unsigned"]["hash"]
    assert unsigned_normal_transaction.raw() == _["xinfin"]["normal"]["unsigned"]["raw"]
    assert isinstance(unsigned_normal_transaction.json(), dict)
    assert unsigned_normal_transaction.signature() == _["xinfin"]["normal"]["unsigned"]["signature"]
    assert isinstance(unsigned_normal_transaction.transaction_raw(), str)

    signed_normal_transaction = unsigned_normal_transaction.sign(
        solver=NormalSolver(
            xprivate_key=_["xinfin"]["wallet"]["sender"]["root_xprivate_key"],
            path=_["xinfin"]["wallet"]["sender"]["derivation"]["path"],
            account=_["xinfin"]["wallet"]["sender"]["derivation"]["account"],
            change=_["xinfin"]["wallet"]["sender"]["derivation"]["change"],
            address=_["xinfin"]["wallet"]["sender"]["derivation"]["address"]
        )
    )

    assert signed_normal_transaction.type() == _["xinfin"]["normal"]["signed"]["type"]
    assert signed_normal_transaction.fee() == _["xinfin"]["normal"]["signed"]["fee"]
    assert isinstance(signed_normal_transaction.hash(), str)
    assert isinstance(signed_normal_transaction.raw(), str)
    assert isinstance(signed_normal_transaction.json(), dict)
    assert isinstance(signed_normal_transaction.signature(), dict)
    assert isinstance(signed_normal_transaction.transaction_raw(), str)


def test_xinfin_fund_transaction():

    htlc = HTLC(
        contract_address=_["xinfin"]["htlc"]["contract_address"],
        network=_["xinfin"]["network"]
    ).build_htlc(
        secret_hash=_["xinfin"]["htlc"]["secret"]["hash"],
        recipient_address=_["xinfin"]["wallet"]["recipient"]["address"],
        sender_address=_["xinfin"]["wallet"]["sender"]["address"],
        endtime=get_current_timestamp(plus=3600)
    )

    unsigned_fund_transaction = FundTransaction(network=_["xinfin"]["network"])

    unsigned_fund_transaction.build_transaction(
        address=_["xinfin"]["wallet"]["sender"]["address"],
        htlc=htlc,
        amount=_["xinfin"]["amount"],
        unit=_["xinfin"]["unit"]
    )

    assert unsigned_fund_transaction.type() == _["xinfin"]["fund"]["unsigned"]["type"]
    assert unsigned_fund_transaction.fee() == _["xinfin"]["fund"]["unsigned"]["fee"]
    assert unsigned_fund_transaction.hash() == _["xinfin"]["fund"]["unsigned"]["hash"]
    assert unsigned_fund_transaction.raw() == _["xinfin"]["fund"]["unsigned"]["raw"]
    assert isinstance(unsigned_fund_transaction.json(), dict)
    assert unsigned_fund_transaction.signature() == _["xinfin"]["fund"]["unsigned"]["signature"]
    assert isinstance(unsigned_fund_transaction.transaction_raw(), str)

    signed_fund_transaction = unsigned_fund_transaction.sign(
        solver=FundSolver(
            xprivate_key=_["xinfin"]["wallet"]["sender"]["root_xprivate_key"],
            path=_["xinfin"]["wallet"]["sender"]["derivation"]["path"],
            account=_["xinfin"]["wallet"]["sender"]["derivation"]["account"],
            change=_["xinfin"]["wallet"]["sender"]["derivation"]["change"],
            address=_["xinfin"]["wallet"]["sender"]["derivation"]["address"]
        )
    )

    assert signed_fund_transaction.type() == _["xinfin"]["fund"]["signed"]["type"]
    assert signed_fund_transaction.fee() == _["xinfin"]["fund"]["signed"]["fee"]
    assert isinstance(signed_fund_transaction.hash(), str)
    assert isinstance(signed_fund_transaction.raw(), str)
    assert isinstance(signed_fund_transaction.json(), dict)
    assert isinstance(signed_fund_transaction.signature(), dict)
    assert isinstance(signed_fund_transaction.transaction_raw(), str)


def test_xinfin_withdraw_transaction():

    unsigned_withdraw_transaction = WithdrawTransaction(network=_["xinfin"]["network"])

    unsigned_withdraw_transaction.build_transaction(
        address=_["xinfin"]["wallet"]["recipient"]["address"],
        transaction_hash=_["xinfin"]["transaction_hash"],
        secret_key=_["xinfin"]["htlc"]["secret"]["key"]
    )

    assert unsigned_withdraw_transaction.type() == _["xinfin"]["withdraw"]["unsigned"]["type"]
    assert unsigned_withdraw_transaction.fee() == _["xinfin"]["withdraw"]["unsigned"]["fee"]
    assert unsigned_withdraw_transaction.hash() == _["xinfin"]["withdraw"]["unsigned"]["hash"]
    assert unsigned_withdraw_transaction.raw() == _["xinfin"]["withdraw"]["unsigned"]["raw"]
    assert isinstance(unsigned_withdraw_transaction.json(), dict)
    assert unsigned_withdraw_transaction.signature() == _["xinfin"]["withdraw"]["unsigned"]["signature"]
    assert isinstance(unsigned_withdraw_transaction.transaction_raw(), str)

    signed_withdraw_transaction = unsigned_withdraw_transaction.sign(
        solver=WithdrawSolver(
            xprivate_key=_["xinfin"]["wallet"]["recipient"]["root_xprivate_key"],
            path=_["xinfin"]["wallet"]["recipient"]["derivation"]["path"],
            account=_["xinfin"]["wallet"]["recipient"]["derivation"]["account"],
            change=_["xinfin"]["wallet"]["recipient"]["derivation"]["change"],
            address=_["xinfin"]["wallet"]["recipient"]["derivation"]["address"]
        )
    )

    assert signed_withdraw_transaction.type() == _["xinfin"]["withdraw"]["signed"]["type"]
    assert signed_withdraw_transaction.fee() == _["xinfin"]["withdraw"]["signed"]["fee"]
    assert isinstance(signed_withdraw_transaction.hash(), str)
    assert isinstance(signed_withdraw_transaction.raw(), str)
    assert isinstance(signed_withdraw_transaction.json(), dict)
    assert isinstance(signed_withdraw_transaction.signature(), dict)
    assert isinstance(signed_withdraw_transaction.transaction_raw(), str)


def test_xinfin_refund_transaction():

    unsigned_refund_transaction = RefundTransaction(network=_["xinfin"]["network"])

    unsigned_refund_transaction.build_transaction(
        address=_["xinfin"]["wallet"]["sender"]["address"],
        transaction_hash=_["xinfin"]["transaction_hash"]
    )

    assert unsigned_refund_transaction.type() == _["xinfin"]["refund"]["unsigned"]["type"]
    assert unsigned_refund_transaction.fee() == _["xinfin"]["refund"]["unsigned"]["fee"]
    assert unsigned_refund_transaction.hash() == _["xinfin"]["refund"]["unsigned"]["hash"]
    assert unsigned_refund_transaction.raw() == _["xinfin"]["refund"]["unsigned"]["raw"]
    assert isinstance(unsigned_refund_transaction.json(), dict)
    assert unsigned_refund_transaction.signature() == _["xinfin"]["refund"]["unsigned"]["signature"]
    assert isinstance(unsigned_refund_transaction.transaction_raw(), str)

    signed_refund_transaction = unsigned_refund_transaction.sign(
        solver=RefundSolver(
            xprivate_key=_["xinfin"]["wallet"]["sender"]["root_xprivate_key"],
            path=_["xinfin"]["wallet"]["sender"]["derivation"]["path"],
            account=_["xinfin"]["wallet"]["sender"]["derivation"]["account"],
            change=_["xinfin"]["wallet"]["sender"]["derivation"]["change"],
            address=_["xinfin"]["wallet"]["sender"]["derivation"]["address"]
        )
    )

    assert signed_refund_transaction.type() == _["xinfin"]["refund"]["signed"]["type"]
    assert signed_refund_transaction.fee() == _["xinfin"]["refund"]["signed"]["fee"]
    assert isinstance(signed_refund_transaction.hash(), str)
    assert isinstance(signed_refund_transaction.raw(), str)
    assert isinstance(signed_refund_transaction.json(), dict)
    assert isinstance(signed_refund_transaction.signature(), dict)
    assert isinstance(signed_refund_transaction.transaction_raw(), str)
