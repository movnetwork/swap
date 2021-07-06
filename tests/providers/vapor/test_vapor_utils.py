#!/usr/bin/env python3

from requests.exceptions import ConnectionError

import pytest
import json
import os

from swap.exceptions import APIError
from swap.providers.vapor.utils import (
    is_network, is_address, is_transaction_raw, get_address_type,
    decode_transaction_raw, submit_transaction_raw
)

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_vapor_utils():

    assert is_network(network=_["vapor"]["network"])
    assert not is_network(network="unknown")

    assert is_address(address=_["vapor"]["wallet"]["sender"]["address"])
    assert not is_address(address=_["vapor"]["wallet"]["sender"]["address"], network="testnet")
    assert is_address(address=_["vapor"]["wallet"]["sender"]["address"], network=_["vapor"]["network"])

    assert is_address(address=_["vapor"]["wallet"]["recipient"]["address"])
    assert not is_address(address=_["vapor"]["wallet"]["recipient"]["address"], network="testnet")
    assert is_address(address=_["vapor"]["wallet"]["recipient"]["address"], network=_["vapor"]["network"])

    assert is_transaction_raw(transaction_raw=_["vapor"]["fund"]["unsigned"]["transaction_raw"])
    assert not is_transaction_raw(transaction_raw="unknown")

    assert get_address_type(address=_["vapor"]["wallet"]["sender"]["address"]) == "p2wpkh"
    assert get_address_type(address=_["vapor"]["wallet"]["recipient"]["address"]) == "p2wpkh"
    assert get_address_type(address=_["vapor"]["htlc"]["contract_address"]) == "p2wsh"

    # HTTPConnectionPool(host='localhost', port=9888)
    with pytest.raises(ConnectionError):
        assert decode_transaction_raw(transaction_raw=_["vapor"]["fund"]["unsigned"]["transaction_raw"]) == \
               {
                   "address": _["vapor"]["wallet"]["sender"]["address"],
                   "fee": 10000000,
                   "network": _["vapor"]["network"],
                   "signatures": [],
                   "tx": _["vapor"]["fund"]["unsigned"]["json"],
                   "type": "vapor_fund_unsigned",
                   "unsigned_datas": _["vapor"]["fund"]["unsigned"]["unsigned_datas"]
               }

    # (600) finalize tx fail
    with pytest.raises(APIError):
        submit_transaction_raw(transaction_raw=_["vapor"]["fund"]["unsigned"]["transaction_raw"])
