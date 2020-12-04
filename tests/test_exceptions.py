#!/usr/bin/env python3

from swap.exceptions import (
    NetworkError, BalanceError, APIError, AddressError, InvalidURLError,
    ClientError, NotFoundError, SymbolError, TransactionRawError
)

import pytest


def test_exceptions():

    with pytest.raises(NetworkError, match="error"):
        raise NetworkError("error")
    with pytest.raises(NetworkError, match="error, error"):
        raise NetworkError("error", "error")
    with pytest.raises(BalanceError, match="error"):
        raise BalanceError("error")
    with pytest.raises(BalanceError, match="error, error"):
        raise BalanceError("error", "error")
    with pytest.raises(APIError, match="error"):
        raise APIError("error")
    with pytest.raises(APIError):
        raise APIError("error", "error")
    with pytest.raises(AddressError, match="error"):
        raise AddressError("error")
    with pytest.raises(AddressError, match="error, error"):
        raise AddressError("error", "error")
    with pytest.raises(InvalidURLError, match="error"):
        raise InvalidURLError("error")
    with pytest.raises(ClientError, match="error"):
        raise ClientError("error")
    with pytest.raises(ClientError):
        raise ClientError("error", "error")
    with pytest.raises(NotFoundError, match="error"):
        raise NotFoundError("error")
    with pytest.raises(SymbolError, match="error"):
        raise SymbolError("error")
    with pytest.raises(SymbolError, match="error, error"):
        raise SymbolError("error", "error")
    with pytest.raises(TransactionRawError, match="error"):
        raise TransactionRawError("error")
    with pytest.raises(TransactionRawError, match="error, error"):
        raise TransactionRawError("error", "error")
