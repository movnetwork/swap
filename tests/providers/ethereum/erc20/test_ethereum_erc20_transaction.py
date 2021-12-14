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
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_ethereum_erc20_normal_transaction():

    unsigned_erc20_normal_transaction = NormalTransaction(network=_["ethereum"]["network"], erc20=True)

    unsigned_erc20_normal_transaction.build_transaction(
        address=_["ethereum"]["wallet"]["sender"]["address"],
        recipient={
            _["ethereum"]["wallet"]["recipient"]["address"]: _["ethereum"]["erc20_amount"] * (10 ** _["ethereum"]["decimals"])
        },
        token_address=_["ethereum"]["erc20_htlc"]["agreements"]["token_address"]
    )

    assert unsigned_erc20_normal_transaction.type() == _["ethereum"]["erc20_normal"]["unsigned"]["type"]
    assert unsigned_erc20_normal_transaction.fee() == _["ethereum"]["erc20_normal"]["unsigned"]["fee"]
    assert unsigned_erc20_normal_transaction.hash() == _["ethereum"]["erc20_normal"]["unsigned"]["hash"]
    assert unsigned_erc20_normal_transaction.raw() == _["ethereum"]["erc20_normal"]["unsigned"]["raw"]
    assert isinstance(unsigned_erc20_normal_transaction.json(), dict)
    assert unsigned_erc20_normal_transaction.signature() == _["ethereum"]["erc20_normal"]["unsigned"]["signature"]
    assert isinstance(unsigned_erc20_normal_transaction.transaction_raw(), str)

    signed_erc20_normal_transaction = unsigned_erc20_normal_transaction.sign(
        solver=NormalSolver(
            xprivate_key=_["ethereum"]["wallet"]["sender"]["root_xprivate_key"],
            path=_["ethereum"]["wallet"]["sender"]["derivation"]["path"],
            account=_["ethereum"]["wallet"]["sender"]["derivation"]["account"],
            change=_["ethereum"]["wallet"]["sender"]["derivation"]["change"],
            address=_["ethereum"]["wallet"]["sender"]["derivation"]["address"]
        )
    )

    assert signed_erc20_normal_transaction.type() == _["ethereum"]["erc20_normal"]["signed"]["type"]
    assert signed_erc20_normal_transaction.fee() == _["ethereum"]["erc20_normal"]["signed"]["fee"]
    assert isinstance(signed_erc20_normal_transaction.hash(), str)
    assert isinstance(signed_erc20_normal_transaction.raw(), str)
    assert isinstance(signed_erc20_normal_transaction.json(), dict)
    assert isinstance(signed_erc20_normal_transaction.signature(), dict)
    assert isinstance(signed_erc20_normal_transaction.transaction_raw(), str)


def test_ethereum_erc20_fund_transaction():

    erc20_htlc = HTLC(
        contract_address=_["ethereum"]["erc20_htlc"]["contract_address"],
        network=_["ethereum"]["network"],
        erc20=True
    ).build_htlc(
        secret_hash=_["ethereum"]["erc20_htlc"]["secret"]["hash"],
        recipient_address=_["ethereum"]["wallet"]["recipient"]["address"],
        sender_address=_["ethereum"]["wallet"]["sender"]["address"],
        endtime=get_current_timestamp(plus=3600),
        token_address=_["ethereum"]["erc20_htlc"]["agreements"]["token_address"]
    )

    unsigned_erc20_fund_transaction = FundTransaction(network=_["ethereum"]["network"], erc20=True)

    unsigned_erc20_fund_transaction.build_transaction(
        address=_["ethereum"]["wallet"]["sender"]["address"],
        htlc=erc20_htlc,
        amount=_["ethereum"]["erc20_amount"] * (10 ** _["ethereum"]["decimals"])
    )

    assert unsigned_erc20_fund_transaction.type() == _["ethereum"]["erc20_fund"]["unsigned"]["type"]
    assert unsigned_erc20_fund_transaction.fee() == _["ethereum"]["erc20_fund"]["unsigned"]["fee"]
    assert unsigned_erc20_fund_transaction.hash() == _["ethereum"]["erc20_fund"]["unsigned"]["hash"]
    assert unsigned_erc20_fund_transaction.raw() == _["ethereum"]["erc20_fund"]["unsigned"]["raw"]
    assert isinstance(unsigned_erc20_fund_transaction.json(), dict)
    assert unsigned_erc20_fund_transaction.signature() == _["ethereum"]["erc20_fund"]["unsigned"]["signature"]
    assert isinstance(unsigned_erc20_fund_transaction.transaction_raw(), str)

    signed_erc20_fund_transaction = unsigned_erc20_fund_transaction.sign(
        solver=FundSolver(
            xprivate_key=_["ethereum"]["wallet"]["sender"]["root_xprivate_key"],
            path=_["ethereum"]["wallet"]["sender"]["derivation"]["path"],
            account=_["ethereum"]["wallet"]["sender"]["derivation"]["account"],
            change=_["ethereum"]["wallet"]["sender"]["derivation"]["change"],
            address=_["ethereum"]["wallet"]["sender"]["derivation"]["address"]
        )
    )

    assert signed_erc20_fund_transaction.type() == _["ethereum"]["erc20_fund"]["signed"]["type"]
    assert signed_erc20_fund_transaction.fee() == _["ethereum"]["erc20_fund"]["signed"]["fee"]
    assert isinstance(signed_erc20_fund_transaction.hash(), str)
    assert isinstance(signed_erc20_fund_transaction.raw(), str)
    assert isinstance(signed_erc20_fund_transaction.json(), dict)
    assert isinstance(signed_erc20_fund_transaction.signature(), dict)
    assert isinstance(signed_erc20_fund_transaction.transaction_raw(), str)


def test_ethereum_erc20_withdraw_transaction():

    unsigned_erc20_withdraw_transaction = WithdrawTransaction(network=_["ethereum"]["network"], erc20=True)

    unsigned_erc20_withdraw_transaction.build_transaction(
        address=_["ethereum"]["wallet"]["recipient"]["address"],
        transaction_hash=_["ethereum"]["erc20_transaction_hash"],
        secret_key=_["ethereum"]["erc20_htlc"]["secret"]["key"]
    )

    assert unsigned_erc20_withdraw_transaction.type() == _["ethereum"]["erc20_withdraw"]["unsigned"]["type"]
    assert unsigned_erc20_withdraw_transaction.fee() == _["ethereum"]["erc20_withdraw"]["unsigned"]["fee"]
    assert unsigned_erc20_withdraw_transaction.hash() == _["ethereum"]["erc20_withdraw"]["unsigned"]["hash"]
    assert unsigned_erc20_withdraw_transaction.raw() == _["ethereum"]["erc20_withdraw"]["unsigned"]["raw"]
    assert isinstance(unsigned_erc20_withdraw_transaction.json(), dict)
    assert unsigned_erc20_withdraw_transaction.signature() == _["ethereum"]["erc20_withdraw"]["unsigned"]["signature"]
    assert isinstance(unsigned_erc20_withdraw_transaction.transaction_raw(), str)

    signed_erc20_withdraw_transaction = unsigned_erc20_withdraw_transaction.sign(
        solver=WithdrawSolver(
            xprivate_key=_["ethereum"]["wallet"]["recipient"]["root_xprivate_key"],
            path=_["ethereum"]["wallet"]["recipient"]["derivation"]["path"],
            account=_["ethereum"]["wallet"]["recipient"]["derivation"]["account"],
            change=_["ethereum"]["wallet"]["recipient"]["derivation"]["change"],
            address=_["ethereum"]["wallet"]["recipient"]["derivation"]["address"]
        )
    )

    assert signed_erc20_withdraw_transaction.type() == _["ethereum"]["erc20_withdraw"]["signed"]["type"]
    assert signed_erc20_withdraw_transaction.fee() == _["ethereum"]["erc20_withdraw"]["signed"]["fee"]
    assert isinstance(signed_erc20_withdraw_transaction.hash(), str)
    assert isinstance(signed_erc20_withdraw_transaction.raw(), str)
    assert isinstance(signed_erc20_withdraw_transaction.json(), dict)
    assert isinstance(signed_erc20_withdraw_transaction.signature(), dict)
    assert isinstance(signed_erc20_withdraw_transaction.transaction_raw(), str)


def test_ethereum_erc20_refund_transaction():

    unsigned_erc20_refund_transaction = RefundTransaction(network=_["ethereum"]["network"], erc20=True)

    unsigned_erc20_refund_transaction.build_transaction(
        address=_["ethereum"]["wallet"]["sender"]["address"],
        transaction_hash=_["ethereum"]["erc20_transaction_hash"]
    )

    assert unsigned_erc20_refund_transaction.type() == _["ethereum"]["erc20_refund"]["unsigned"]["type"]
    assert unsigned_erc20_refund_transaction.fee() == _["ethereum"]["erc20_refund"]["unsigned"]["fee"]
    assert unsigned_erc20_refund_transaction.hash() == _["ethereum"]["erc20_refund"]["unsigned"]["hash"]
    assert unsigned_erc20_refund_transaction.raw() == _["ethereum"]["erc20_refund"]["unsigned"]["raw"]
    assert isinstance(unsigned_erc20_refund_transaction.json(), dict)
    assert unsigned_erc20_refund_transaction.signature() == _["ethereum"]["erc20_refund"]["unsigned"]["signature"]
    assert isinstance(unsigned_erc20_refund_transaction.transaction_raw(), str)

    signed_erc20_refund_transaction = unsigned_erc20_refund_transaction.sign(
        solver=RefundSolver(
            xprivate_key=_["ethereum"]["wallet"]["sender"]["root_xprivate_key"],
            path=_["ethereum"]["wallet"]["sender"]["derivation"]["path"],
            account=_["ethereum"]["wallet"]["sender"]["derivation"]["account"],
            change=_["ethereum"]["wallet"]["sender"]["derivation"]["change"],
            address=_["ethereum"]["wallet"]["sender"]["derivation"]["address"]
        )
    )

    assert signed_erc20_refund_transaction.type() == _["ethereum"]["erc20_refund"]["signed"]["type"]
    assert signed_erc20_refund_transaction.fee() == _["ethereum"]["erc20_refund"]["signed"]["fee"]
    assert isinstance(signed_erc20_refund_transaction.hash(), str)
    assert isinstance(signed_erc20_refund_transaction.raw(), str)
    assert isinstance(signed_erc20_refund_transaction.json(), dict)
    assert isinstance(signed_erc20_refund_transaction.signature(), dict)
    assert isinstance(signed_erc20_refund_transaction.transaction_raw(), str)
