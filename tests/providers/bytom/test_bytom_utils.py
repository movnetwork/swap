#!/usr/bin/env python3

from requests.exceptions import ConnectionError

import pytest
import json
import os

from swap.exceptions import APIError
from swap.providers.bytom.utils import (
    is_network, is_address, is_transaction_raw, get_address_type,
    decode_transaction_raw, submit_transaction_raw
)

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_bytom_utils():

    assert is_network(network=_["bytom"]["network"])
    assert not is_network(network="unknown")

    assert is_address(address=_["bytom"]["wallet"]["sender"]["address"])
    assert not is_address(address=_["bytom"]["wallet"]["sender"]["address"], network="testnet")
    assert is_address(address=_["bytom"]["wallet"]["sender"]["address"], network=_["bytom"]["network"])

    assert is_address(address=_["bytom"]["wallet"]["recipient"]["address"])
    assert not is_address(address=_["bytom"]["wallet"]["recipient"]["address"], network="testnet")
    assert is_address(address=_["bytom"]["wallet"]["recipient"]["address"], network=_["bytom"]["network"])

    assert is_transaction_raw(transaction_raw=_["bytom"]["fund"]["unsigned"]["transaction_raw"])
    assert not is_transaction_raw(transaction_raw="unknown")

    assert get_address_type(address=_["bytom"]["wallet"]["sender"]["address"]) == "p2wpkh"
    assert get_address_type(address=_["bytom"]["wallet"]["recipient"]["address"]) == "p2wpkh"
    assert get_address_type(address=_["bytom"]["htlc"]["contract_address"]) == "p2wsh"

    # HTTPConnectionPool(host='localhost', port=9888)
    with pytest.raises(ConnectionError):
        assert decode_transaction_raw(transaction_raw=_["bytom"]["fund"]["unsigned"]["transaction_raw"]) == \
               {
                   "address": _["bytom"]["wallet"]["sender"]["address"],
                   "fee": 10000000,
                   "network": _["bytom"]["network"],
                   "signatures": [],
                   "tx": _["bytom"]["fund"]["unsigned"]["json"],
                   "type": "bytom_fund_unsigned",
                   "unsigned_datas": _["bytom"]["fund"]["unsigned"]["unsigned_datas"]
               }

    # (600) finalize tx fail
    with pytest.raises(APIError):
        submit_transaction_raw(transaction_raw=_["bytom"]["fund"]["unsigned"]["transaction_raw"])
