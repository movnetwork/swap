#!/usr/bin/env python3

import json
import os

from swap.providers.vapor.transaction import (
    NormalTransaction, FundTransaction, ClaimTransaction, RefundTransaction
)
from swap.providers.vapor.solver import (
    NormalSolver, FundSolver, ClaimSolver, RefundSolver
)
from swap.providers.vapor.utils import amount_unit_converter
from swap.utils import clean_transaction_raw

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_vapor_normal_transaction():

    unsigned_normal_transaction = NormalTransaction(network=_["vapor"]["network"])

    unsigned_normal_transaction.build_transaction(
        address=_["vapor"]["wallet"]["sender"]["address"],
        asset=_["vapor"]["asset"],
        recipients={
            _["vapor"]["wallet"]["recipient"]["address"]: (
                _["vapor"]["amount"] if _["vapor"]["unit"] == "NEU" else amount_unit_converter(
                    _["vapor"]["amount"], f"{_['vapor']['unit']}2NEU")
            )
        }
    )

    assert unsigned_normal_transaction.type() == _["vapor"]["normal"]["unsigned"]["type"]
    assert unsigned_normal_transaction.fee() == _["vapor"]["normal"]["unsigned"]["fee"]
    assert unsigned_normal_transaction.hash() == _["vapor"]["normal"]["unsigned"]["hash"]
    assert unsigned_normal_transaction.raw() == _["vapor"]["normal"]["unsigned"]["raw"]
    # assert unsigned_normal_transaction.json() == _["vapor"]["normal"]["unsigned"]["json"]
    assert unsigned_normal_transaction.unsigned_datas() == _["vapor"]["normal"]["unsigned"]["unsigned_datas"]
    assert unsigned_normal_transaction.signatures() == _["vapor"]["normal"]["unsigned"]["signatures"]
    assert unsigned_normal_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["vapor"]["normal"]["unsigned"]["transaction_raw"]
    )

    signed_normal_transaction = unsigned_normal_transaction.sign(
        solver=NormalSolver(
            xprivate_key=_["vapor"]["wallet"]["sender"]["xprivate_key"],
            path=_["vapor"]["wallet"]["sender"]["derivation"]["path"],
            account=_["vapor"]["wallet"]["sender"]["derivation"]["account"],
            change=_["vapor"]["wallet"]["sender"]["derivation"]["change"],
            address=_["vapor"]["wallet"]["sender"]["derivation"]["address"]
        )
    )

    assert signed_normal_transaction.type() == _["vapor"]["normal"]["signed"]["type"]
    assert signed_normal_transaction.fee() == _["vapor"]["normal"]["signed"]["fee"]
    assert signed_normal_transaction.hash() == _["vapor"]["normal"]["signed"]["hash"]
    assert signed_normal_transaction.raw() == _["vapor"]["normal"]["signed"]["raw"]
    # assert signed_normal_transaction.json() == _["vapor"]["normal"]["signed"]["json"]
    assert signed_normal_transaction.unsigned_datas() == _["vapor"]["normal"]["signed"]["unsigned_datas"]
    assert signed_normal_transaction.signatures() == _["vapor"]["normal"]["signed"]["signatures"]
    assert signed_normal_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["vapor"]["normal"]["signed"]["transaction_raw"]
    )


def test_vapor_fund_transaction():

    unsigned_fund_transaction = FundTransaction(network=_["vapor"]["network"])

    unsigned_fund_transaction.build_transaction(
        address=_["vapor"]["wallet"]["sender"]["address"],
        htlc_address=_["vapor"]["htlc"]["address"],
        asset=_["vapor"]["asset"],
        amount=(
            _["vapor"]["amount"] if _["vapor"]["unit"] == "NEU" else amount_unit_converter(
                _["vapor"]["amount"], f"{_['vapor']['unit']}2NEU")
        )
    )

    assert unsigned_fund_transaction.type() == _["vapor"]["fund"]["unsigned"]["type"]
    assert unsigned_fund_transaction.fee() == _["vapor"]["fund"]["unsigned"]["fee"]
    assert unsigned_fund_transaction.hash() == _["vapor"]["fund"]["unsigned"]["hash"]
    assert unsigned_fund_transaction.raw() == _["vapor"]["fund"]["unsigned"]["raw"]
    # assert unsigned_fund_transaction.json() == _["vapor"]["fund"]["unsigned"]["json"]
    assert unsigned_fund_transaction.unsigned_datas() == _["vapor"]["fund"]["unsigned"]["unsigned_datas"]
    assert unsigned_fund_transaction.signatures() == _["vapor"]["fund"]["unsigned"]["signatures"]
    assert unsigned_fund_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["vapor"]["fund"]["unsigned"]["transaction_raw"]
    )

    signed_fund_transaction = unsigned_fund_transaction.sign(
        solver=FundSolver(
            xprivate_key=_["vapor"]["wallet"]["sender"]["xprivate_key"],
            path=_["vapor"]["wallet"]["sender"]["derivation"]["path"],
            account=_["vapor"]["wallet"]["sender"]["derivation"]["account"],
            change=_["vapor"]["wallet"]["sender"]["derivation"]["change"],
            address=_["vapor"]["wallet"]["sender"]["derivation"]["address"]
        )
    )

    assert signed_fund_transaction.type() == _["vapor"]["fund"]["signed"]["type"]
    assert signed_fund_transaction.fee() == _["vapor"]["fund"]["signed"]["fee"]
    assert signed_fund_transaction.hash() == _["vapor"]["fund"]["signed"]["hash"]
    assert signed_fund_transaction.raw() == _["vapor"]["fund"]["signed"]["raw"]
    # assert signed_fund_transaction.json() == _["vapor"]["fund"]["signed"]["json"]
    assert signed_fund_transaction.unsigned_datas() == _["vapor"]["fund"]["signed"]["unsigned_datas"]
    assert signed_fund_transaction.signatures() == _["vapor"]["fund"]["signed"]["signatures"]
    assert signed_fund_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["vapor"]["fund"]["signed"]["transaction_raw"]
    )


def test_vapor_claim_transaction():

    unsigned_claim_transaction = ClaimTransaction(network=_["vapor"]["network"])

    unsigned_claim_transaction.build_transaction(
        address=_["vapor"]["wallet"]["recipient"]["address"],
        transaction_id=_["vapor"]["transaction_id"],
        amount=(
            _["vapor"]["amount"] if _["vapor"]["unit"] == "NEU" else amount_unit_converter(
                _["vapor"]["amount"], f"{_['vapor']['unit']}2NEU")
        ),
        max_amount=_["vapor"]["max_amount"],
        asset=_["vapor"]["asset"],
    )

    assert unsigned_claim_transaction.type() == _["vapor"]["claim"]["unsigned"]["type"]
    assert unsigned_claim_transaction.fee() == _["vapor"]["claim"]["unsigned"]["fee"]
    assert unsigned_claim_transaction.hash() == _["vapor"]["claim"]["unsigned"]["hash"]
    assert unsigned_claim_transaction.raw() == _["vapor"]["claim"]["unsigned"]["raw"]
    # assert unsigned_claim_transaction.json() == _["vapor"]["claim"]["unsigned"]["json"]
    assert unsigned_claim_transaction.unsigned_datas() == _["vapor"]["claim"]["unsigned"]["unsigned_datas"]
    assert unsigned_claim_transaction.signatures() == _["vapor"]["claim"]["unsigned"]["signatures"]
    assert unsigned_claim_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["vapor"]["claim"]["unsigned"]["transaction_raw"]
    )

    signed_claim_transaction = unsigned_claim_transaction.sign(
        solver=ClaimSolver(
            xprivate_key=_["vapor"]["wallet"]["recipient"]["xprivate_key"],
            secret_key=_["vapor"]["htlc"]["secret"]["key"],
            bytecode=_["vapor"]["htlc"]["bytecode"],
            path=_["vapor"]["wallet"]["recipient"]["derivation"]["path"],
            account=_["vapor"]["wallet"]["recipient"]["derivation"]["account"],
            change=_["vapor"]["wallet"]["recipient"]["derivation"]["change"],
            address=_["vapor"]["wallet"]["recipient"]["derivation"]["address"]
        )
    )

    assert signed_claim_transaction.type() == _["vapor"]["claim"]["signed"]["type"]
    assert signed_claim_transaction.fee() == _["vapor"]["claim"]["signed"]["fee"]
    assert signed_claim_transaction.hash() == _["vapor"]["claim"]["signed"]["hash"]
    assert signed_claim_transaction.raw() == _["vapor"]["claim"]["signed"]["raw"]
    # assert signed_claim_transaction.json() == _["vapor"]["claim"]["signed"]["json"]
    assert signed_claim_transaction.unsigned_datas() == _["vapor"]["claim"]["signed"]["unsigned_datas"]
    assert signed_claim_transaction.signatures() == _["vapor"]["claim"]["signed"]["signatures"]
    assert signed_claim_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["vapor"]["claim"]["signed"]["transaction_raw"]
    )


def test_vapor_refund_transaction():

    unsigned_refund_transaction = RefundTransaction(network=_["vapor"]["network"])

    unsigned_refund_transaction.build_transaction(
        address=_["vapor"]["wallet"]["sender"]["address"],
        transaction_id=_["vapor"]["transaction_id"],
        amount=(
            _["vapor"]["amount"] if _["vapor"]["unit"] == "NEU" else amount_unit_converter(
                _["vapor"]["amount"], f"{_['vapor']['unit']}2NEU")
        ),
        max_amount=_["vapor"]["max_amount"],
        asset=_["vapor"]["asset"],
    )

    assert unsigned_refund_transaction.type() == _["vapor"]["refund"]["unsigned"]["type"]
    assert unsigned_refund_transaction.fee() == _["vapor"]["refund"]["unsigned"]["fee"]
    assert unsigned_refund_transaction.hash() == _["vapor"]["refund"]["unsigned"]["hash"]
    assert unsigned_refund_transaction.raw() == _["vapor"]["refund"]["unsigned"]["raw"]
    # assert unsigned_refund_transaction.json() == _["vapor"]["refund"]["unsigned"]["json"]
    assert unsigned_refund_transaction.unsigned_datas() == _["vapor"]["refund"]["unsigned"]["unsigned_datas"]
    assert unsigned_refund_transaction.signatures() == _["vapor"]["refund"]["unsigned"]["signatures"]
    assert unsigned_refund_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["vapor"]["refund"]["unsigned"]["transaction_raw"]
    )

    signed_refund_transaction = unsigned_refund_transaction.sign(
        solver=RefundSolver(
            xprivate_key=_["vapor"]["wallet"]["sender"]["xprivate_key"],
            bytecode=_["vapor"]["htlc"]["bytecode"],
            path=_["vapor"]["wallet"]["sender"]["derivation"]["path"],
            account=_["vapor"]["wallet"]["sender"]["derivation"]["account"],
            change=_["vapor"]["wallet"]["sender"]["derivation"]["change"],
            address=_["vapor"]["wallet"]["sender"]["derivation"]["address"]
        )
    )

    assert signed_refund_transaction.type() == _["vapor"]["refund"]["signed"]["type"]
    assert signed_refund_transaction.fee() == _["vapor"]["refund"]["signed"]["fee"]
    assert signed_refund_transaction.hash() == _["vapor"]["refund"]["signed"]["hash"]
    assert signed_refund_transaction.raw() == _["vapor"]["refund"]["signed"]["raw"]
    # assert signed_refund_transaction.json() == _["vapor"]["refund"]["signed"]["json"]
    assert signed_refund_transaction.unsigned_datas() == _["vapor"]["refund"]["signed"]["unsigned_datas"]
    assert signed_refund_transaction.signatures() == _["vapor"]["refund"]["signed"]["signatures"]
    assert signed_refund_transaction.transaction_raw() == clean_transaction_raw(
        transaction_raw=_["vapor"]["refund"]["signed"]["transaction_raw"]
    )
