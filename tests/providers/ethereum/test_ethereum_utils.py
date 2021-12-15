#!/usr/bin/env python3

import pytest
import json
import os

from swap.exceptions import TransactionRawError
from swap.providers.ethereum.utils import (
    is_network, is_address, is_transaction_raw, get_erc20_data,
    decode_transaction_raw, submit_transaction_raw
)

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_ethereum_utils():

    assert is_network(network=_["ethereum"]["network"])
    assert not is_network(network="unknown")

    assert is_address(address=_["ethereum"]["wallet"]["sender"]["address"])
    assert is_address(address=_["ethereum"]["wallet"]["recipient"]["address"])

    assert is_transaction_raw(transaction_raw=_["ethereum"]["fund"]["unsigned"]["transaction_raw"])
    assert not is_transaction_raw(transaction_raw="unknown")

    assert isinstance(get_erc20_data("abi"), list)
    assert isinstance(get_erc20_data("bin"), str)
    assert isinstance(get_erc20_data("bin-runtime"), str)
    assert isinstance(get_erc20_data("opcodes"), str)

    assert decode_transaction_raw(transaction_raw=_["ethereum"]["fund"]["unsigned"]["transaction_raw"]) == \
        {
            "fee": _["ethereum"]["fund"]["unsigned"]["fee"],
            "network": _["ethereum"]["network"],
            "signatures": None,
            "transaction": _["ethereum"]["fund"]["unsigned"]["json"],
            "type": "ethereum_fund_unsigned"
        }

    # Wrong Ethereum transaction raw must be signed, not unsigned transaction raw.
    with pytest.raises(TransactionRawError):
        submit_transaction_raw(transaction_raw=_["ethereum"]["fund"]["unsigned"]["transaction_raw"])
