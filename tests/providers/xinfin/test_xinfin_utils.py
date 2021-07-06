#!/usr/bin/env python3

import pytest
import json
import os

from swap.exceptions import TransactionRawError
from swap.providers.xinfin.utils import (
    is_network, is_address, is_transaction_raw,
    decode_transaction_raw, submit_transaction_raw
)

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_xinfin_utils():

    assert is_network(network=_["xinfin"]["network"])
    assert not is_network(network="unknown")

    assert is_address(address=_["xinfin"]["wallet"]["sender"]["address"])
    assert is_address(address=_["xinfin"]["wallet"]["recipient"]["address"])

    assert is_transaction_raw(transaction_raw=_["xinfin"]["fund"]["unsigned"]["transaction_raw"])
    assert not is_transaction_raw(transaction_raw="unknown")

    assert decode_transaction_raw(transaction_raw=_["xinfin"]["fund"]["unsigned"]["transaction_raw"]) == \
        {
            "fee": _["xinfin"]["fund"]["unsigned"]["fee"],
            "network": _["xinfin"]["network"],
            "signatures": None,
            "transaction": _["xinfin"]["fund"]["unsigned"]["json"],
            "type": "xinfin_fund_unsigned"
        }

    # Wrong Ethereum transaction raw must be signed, not unsigned transaction raw.
    with pytest.raises(TransactionRawError):
        submit_transaction_raw(transaction_raw=_["xinfin"]["fund"]["unsigned"]["transaction_raw"])
