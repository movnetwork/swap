#!/usr/bin/env python3

from swap.utils.exceptions import NetworkError, BalanceError, APIError, \
    AddressError, InvalidURLError, ClientError, NotFoundError

import pytest


def exceptions(error=""):
    if error == "network":
        raise NetworkError("Invalid network type.")
    elif error == "network_detail":
        raise NetworkError("Invalid network type.", "testnet")
    elif error == "balance":
        raise BalanceError("0")
    elif error == "balance_detail":
        raise BalanceError("0", "you don't enough coin")
    elif error == "api":
        raise APIError("Server error.")
    elif error == "api_detail":
        raise APIError("Server error.", "connection loss..")
    elif error == "address":
        raise AddressError("Invalid bitcoin mainnet address.")
    elif error == "address_detail":
        raise AddressError("Invalid bitcoin mainnet address.", "2N3NKQpymf1KunR4W8BpZjs8za5La5pV5hF")
    elif error == "url":
        raise InvalidURLError("Invalid URL address.")
    elif error == "client":
        raise ClientError("Invalid transaction raw.")
    elif error == "client_detail":
        raise ClientError("Invalid transaction raw.", "--raw enasdsarue5kj5435345...")
    elif error == "not_found":
        raise NotFoundError("Not Found.")


def test_exceptions():
    with pytest.raises(NetworkError, match=r".* network .*"):
        exceptions("network")
    with pytest.raises(NetworkError, match=r".* network .*, testnet"):
        exceptions("network_detail")
    with pytest.raises(BalanceError, match="0"):
        exceptions("balance")
    with pytest.raises(BalanceError, match="0, you don't enough coin"):
        exceptions("balance_detail")
    with pytest.raises(APIError, match=r".*."):
        exceptions("api")
    with pytest.raises(APIError, match=r".*."):
        exceptions("api_detail")
    with pytest.raises(AddressError, match="Invalid bitcoin mainnet address."):
        exceptions("address")
    with pytest.raises(AddressError, match="Invalid bitcoin mainnet address., 2N3NKQpymf1KunR4W8BpZjs8za5La5pV5hF"):
        exceptions("address_detail")
    with pytest.raises(InvalidURLError, match=".* URL .*"):
        exceptions("url")
    with pytest.raises(ClientError, match="Invalid transaction raw."):
        exceptions("client")
    with pytest.raises(ClientError, match="--raw enasdsarue5kj5435345..."):
        exceptions("client_detail", )
    with pytest.raises(NotFoundError, match="Not Found."):
        exceptions("not_found")
