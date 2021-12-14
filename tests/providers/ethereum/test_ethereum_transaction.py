#!/usr/bin/env python3

import json
import os

from swap.providers.ethereum.htlc import HTLC
from swap.providers.ethereum.transaction import (
    NormalTransaction, FundTransaction, WithdrawTransaction, RefundTransaction
)
from swap.providers.ethereum.solver import (
    NormalSolver, FundSolver, WithdrawSolver, RefundSolver
)
from swap.utils import get_current_timestamp

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_ethereum_normal_transaction():

    unsigned_normal_transaction = NormalTransaction(network=_["ethereum"]["network"])

    unsigned_normal_transaction.build_transaction(
        address=_["ethereum"]["wallet"]["sender"]["address"],
        recipient={
            _["ethereum"]["wallet"]["recipient"]["address"]: _["ethereum"]["amount"]
        },
        unit=_["ethereum"]["unit"]
    )

    assert unsigned_normal_transaction.type() == _["ethereum"]["normal"]["unsigned"]["type"]
    assert unsigned_normal_transaction.fee() == _["ethereum"]["normal"]["unsigned"]["fee"]
    assert unsigned_normal_transaction.hash() == _["ethereum"]["normal"]["unsigned"]["hash"]
    assert unsigned_normal_transaction.raw() == _["ethereum"]["normal"]["unsigned"]["raw"]
    assert isinstance(unsigned_normal_transaction.json(), dict)
    assert unsigned_normal_transaction.signature() == _["ethereum"]["normal"]["unsigned"]["signature"]
    assert isinstance(unsigned_normal_transaction.transaction_raw(), str)

    signed_normal_transaction = unsigned_normal_transaction.sign(
        solver=NormalSolver(
            xprivate_key=_["ethereum"]["wallet"]["sender"]["root_xprivate_key"],
            path=_["ethereum"]["wallet"]["sender"]["derivation"]["path"],
            account=_["ethereum"]["wallet"]["sender"]["derivation"]["account"],
            change=_["ethereum"]["wallet"]["sender"]["derivation"]["change"],
            address=_["ethereum"]["wallet"]["sender"]["derivation"]["address"]
        )
    )

    assert signed_normal_transaction.type() == _["ethereum"]["normal"]["signed"]["type"]
    assert signed_normal_transaction.fee() == _["ethereum"]["normal"]["signed"]["fee"]
    assert isinstance(signed_normal_transaction.hash(), str)
    assert isinstance(signed_normal_transaction.raw(), str)
    assert isinstance(signed_normal_transaction.json(), dict)
    assert isinstance(signed_normal_transaction.signature(), dict)
    assert isinstance(signed_normal_transaction.transaction_raw(), str)


def test_ethereum_fund_transaction():

    htlc = HTLC(
        contract_address=_["ethereum"]["htlc"]["contract_address"],
        network=_["ethereum"]["network"]
    ).build_htlc(
        secret_hash=_["ethereum"]["htlc"]["secret"]["hash"],
        recipient_address=_["ethereum"]["wallet"]["recipient"]["address"],
        sender_address=_["ethereum"]["wallet"]["sender"]["address"],
        endtime=get_current_timestamp(plus=3600)
    )

    unsigned_fund_transaction = FundTransaction(network=_["ethereum"]["network"])

    unsigned_fund_transaction.build_transaction(
        address=_["ethereum"]["wallet"]["sender"]["address"],
        htlc=htlc,
        amount=_["ethereum"]["amount"],
        unit=_["ethereum"]["unit"]
    )

    assert unsigned_fund_transaction.type() == _["ethereum"]["fund"]["unsigned"]["type"]
    assert unsigned_fund_transaction.fee() == _["ethereum"]["fund"]["unsigned"]["fee"]
    assert unsigned_fund_transaction.hash() == _["ethereum"]["fund"]["unsigned"]["hash"]
    assert unsigned_fund_transaction.raw() == _["ethereum"]["fund"]["unsigned"]["raw"]
    assert isinstance(unsigned_fund_transaction.json(), dict)
    assert unsigned_fund_transaction.signature() == _["ethereum"]["fund"]["unsigned"]["signature"]
    assert isinstance(unsigned_fund_transaction.transaction_raw(), str)

    signed_fund_transaction = unsigned_fund_transaction.sign(
        solver=FundSolver(
            xprivate_key=_["ethereum"]["wallet"]["sender"]["root_xprivate_key"],
            path=_["ethereum"]["wallet"]["sender"]["derivation"]["path"],
            account=_["ethereum"]["wallet"]["sender"]["derivation"]["account"],
            change=_["ethereum"]["wallet"]["sender"]["derivation"]["change"],
            address=_["ethereum"]["wallet"]["sender"]["derivation"]["address"]
        )
    )

    assert signed_fund_transaction.type() == _["ethereum"]["fund"]["signed"]["type"]
    assert signed_fund_transaction.fee() == _["ethereum"]["fund"]["signed"]["fee"]
    assert isinstance(signed_fund_transaction.hash(), str)
    assert isinstance(signed_fund_transaction.raw(), str)
    assert isinstance(signed_fund_transaction.json(), dict)
    assert isinstance(signed_fund_transaction.signature(), dict)
    assert isinstance(signed_fund_transaction.transaction_raw(), str)


def test_ethereum_withdraw_transaction():

    unsigned_withdraw_transaction = WithdrawTransaction(network=_["ethereum"]["network"])

    unsigned_withdraw_transaction.build_transaction(
        address=_["ethereum"]["wallet"]["recipient"]["address"],
        transaction_hash=_["ethereum"]["transaction_hash"],
        secret_key=_["ethereum"]["htlc"]["secret"]["key"]
    )

    assert unsigned_withdraw_transaction.type() == _["ethereum"]["withdraw"]["unsigned"]["type"]
    assert unsigned_withdraw_transaction.fee() == _["ethereum"]["withdraw"]["unsigned"]["fee"]
    assert unsigned_withdraw_transaction.hash() == _["ethereum"]["withdraw"]["unsigned"]["hash"]
    assert unsigned_withdraw_transaction.raw() == _["ethereum"]["withdraw"]["unsigned"]["raw"]
    assert isinstance(unsigned_withdraw_transaction.json(), dict)
    assert unsigned_withdraw_transaction.signature() == _["ethereum"]["withdraw"]["unsigned"]["signature"]
    assert isinstance(unsigned_withdraw_transaction.transaction_raw(), str)

    signed_withdraw_transaction = unsigned_withdraw_transaction.sign(
        solver=WithdrawSolver(
            xprivate_key=_["ethereum"]["wallet"]["recipient"]["root_xprivate_key"],
            path=_["ethereum"]["wallet"]["recipient"]["derivation"]["path"],
            account=_["ethereum"]["wallet"]["recipient"]["derivation"]["account"],
            change=_["ethereum"]["wallet"]["recipient"]["derivation"]["change"],
            address=_["ethereum"]["wallet"]["recipient"]["derivation"]["address"]
        )
    )

    assert signed_withdraw_transaction.type() == _["ethereum"]["withdraw"]["signed"]["type"]
    assert signed_withdraw_transaction.fee() == _["ethereum"]["withdraw"]["signed"]["fee"]
    assert isinstance(signed_withdraw_transaction.hash(), str)
    assert isinstance(signed_withdraw_transaction.raw(), str)
    assert isinstance(signed_withdraw_transaction.json(), dict)
    assert isinstance(signed_withdraw_transaction.signature(), dict)
    assert isinstance(signed_withdraw_transaction.transaction_raw(), str)


def test_ethereum_refund_transaction():

    unsigned_refund_transaction = RefundTransaction(network=_["ethereum"]["network"])

    unsigned_refund_transaction.build_transaction(
        address=_["ethereum"]["wallet"]["sender"]["address"],
        transaction_hash=_["ethereum"]["transaction_hash"]
    )

    assert unsigned_refund_transaction.type() == _["ethereum"]["refund"]["unsigned"]["type"]
    assert unsigned_refund_transaction.fee() == _["ethereum"]["refund"]["unsigned"]["fee"]
    assert unsigned_refund_transaction.hash() == _["ethereum"]["refund"]["unsigned"]["hash"]
    assert unsigned_refund_transaction.raw() == _["ethereum"]["refund"]["unsigned"]["raw"]
    assert isinstance(unsigned_refund_transaction.json(), dict)
    assert unsigned_refund_transaction.signature() == _["ethereum"]["refund"]["unsigned"]["signature"]
    assert isinstance(unsigned_refund_transaction.transaction_raw(), str)

    signed_refund_transaction = unsigned_refund_transaction.sign(
        solver=RefundSolver(
            xprivate_key=_["ethereum"]["wallet"]["sender"]["root_xprivate_key"],
            path=_["ethereum"]["wallet"]["sender"]["derivation"]["path"],
            account=_["ethereum"]["wallet"]["sender"]["derivation"]["account"],
            change=_["ethereum"]["wallet"]["sender"]["derivation"]["change"],
            address=_["ethereum"]["wallet"]["sender"]["derivation"]["address"]
        )
    )

    assert signed_refund_transaction.type() == _["ethereum"]["refund"]["signed"]["type"]
    assert signed_refund_transaction.fee() == _["ethereum"]["refund"]["signed"]["fee"]
    assert isinstance(signed_refund_transaction.hash(), str)
    assert isinstance(signed_refund_transaction.raw(), str)
    assert isinstance(signed_refund_transaction.json(), dict)
    assert isinstance(signed_refund_transaction.signature(), dict)
    assert isinstance(signed_refund_transaction.transaction_raw(), str)
