#!/usr/bin/env python3

from swap.providers.bytom.wallet import Wallet
from swap.providers.bytom.utils import (
    is_address, decode_swap_transaction_raw, submit_swap_transaction_raw
)
from swap.utils.exceptions import TransactionRawError

import pytest


def test_bytom_utils_exceptions():

    assert is_address("sm1q9ndylx02syfwd7npehfxz4lddhzqsve2gdsdcs", "solonet")
    assert is_address("sm1q9ndylx02syfwd7npehfxz4lddhzqsve2gdsdcs")

    with pytest.raises(TransactionRawError, match="Invalid swap Bytom transaction raw"):
        decode_swap_transaction_raw("YXNkZg==")

    with pytest.raises(TransactionRawError, match="Invalid swap Bytom transaction raw"):
        decode_swap_transaction_raw("eyJub25lIjogbnVsbH0=")

    with pytest.raises(TransactionRawError, match="Invalid swap Bytom transaction raw"):
        submit_swap_transaction_raw("YXNkZg==")

    with pytest.raises(TransactionRawError, match="Invalid swap Bytom transaction raw"):
        submit_swap_transaction_raw("eyJub25lIjogbnVsbH0=")
