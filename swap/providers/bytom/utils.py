#!/usr/bin/env python3

from base64 import b64decode
from pybytom.utils import is_address as btm_is_address
from typing import Optional, Union

import requests
import json
import datetime

from ...utils import clean_transaction_raw
from ...exceptions import (
    NetworkError, APIError, TransactionRawError, SymbolError
)
from ..config import bytom

# Bytom config
config = bytom()


def amount_converter(amount: Union[int, float], symbol: str = "NEU2BTM") -> Union[int, float]:
    """
    Amount converter

    :param amount: Bytom amount.
    :type amount: int, float
    :param symbol: Bytom symbol, default to NEU2BTM.
    :type symbol: str
    :returns: float -- BTM asset amount.

    >>> from swap.providers.bytom.utils import amount_converter
    >>> amount_converter(amount=10_000_000, symbol="NEU2BTM")
    0.1
    """

    if symbol not in ["BTM2mBTM", "BTM2NEU", "mBTM2BTM", "mBTM2NEU", "NEU2BTM", "NEU2mBTM"]:
        raise SymbolError(f"Invalid '{symbol}' symbol/type",
                          "choose only 'BTM2mBTM', 'BTM2NEU', 'mBTM2BTM', 'mBTM2NEU', 'NEU2BTM' or 'NEU2mBTM' symbols.")

    # Constant values
    BTM, mBTM, NEU = (1, 1000, 100_000_000)

    if symbol == "BTM2mBTM":
        return float((amount * mBTM) / BTM)
    elif symbol == "BTM2NEU":
        return int((amount * NEU) / BTM)
    elif symbol == "mBTM2BTM":
        return float((amount * BTM) / mBTM)
    elif symbol == "mBTM2NEU":
        return int((amount * NEU) / mBTM)
    elif symbol == "NEU2BTM":
        return float((amount * BTM) / NEU)
    elif symbol == "NEU2mBTM":
        return int((amount * mBTM) / NEU)


def is_network(network: str) -> bool:
    """
    Check Bytom network.

    :param network: Bytom network.
    :type network: str
    :returns: bool -- Bytom valid/invalid network.

    >>> from swap.providers.bytom.utils import is_network
    >>> is_network("solonet")
    True
    """

    if not isinstance(network, str):
        raise TypeError(f"Network must be str, not '{type(network)}' type.")
    return network in ["mainnet", "solonet", "testnet"]


def is_address(address: str, network: Optional[str] = None) -> bool:
    """
    Check Bytom address.

    :param address: Bytom address.
    :type address: str
    :param network: Bytom network, defaults to None.
    :type network: str
    :returns: bool -- Bytom valid/invalid address.

    >>> from swap.providers.bytom.utils import is_address
    >>> is_address("bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "mainnet")
    True
    """

    if network is None:
        return btm_is_address(address=address)
    elif not is_network(network=network):
        raise NetworkError(f"Invalid Bytom '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")
    return btm_is_address(address=address, network=network)


def is_transaction_raw(transaction_raw: str) -> bool:
    """
    Check Bytom transaction raw.

    :param transaction_raw: Bytom transaction raw.
    :type transaction_raw: str
    :returns: bool -- Bytom valid/invalid transaction raw.

    >>> from swap.providers.bytom.utils import is_transaction_raw
    >>> is_transaction_raw("...")
    True
    """

    if not isinstance(transaction_raw, str):
        raise TypeError(f"Transaction raw must be str, not '{type(transaction_raw)}' type.")
    
    try:
        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())
        return loaded_transaction_raw["type"] in [
            "bytom_fund_unsigned", "bytom_fund_signed",
            "bytom_claim_unsigned", "bytom_claim_signed",
            "bytom_refund_unsigned", "bytom_refund_signed"
        ]
    except:
        return False


def decode_transaction_raw(transaction_raw: str, headers: dict = config["headers"],
                           timeout: int = config["timeout"]) -> dict:
    """
    Decode Bytom transaction raw.

    :param transaction_raw: Bytom transaction raw.
    :type transaction_raw: str
    :param headers: Request headers, default to common headers.
    :type headers: dict
    :param timeout: Request timeout, default to 60.
    :type timeout: int
    :returns: dict -- Decoded Bytom transaction raw.

    >>> from swap.providers.bytom.utils import decode_transaction_raw
    >>> decode_transaction_raw(transaction_raw)
    {'fee': ..., 'type': '...', 'address': '...', 'transaction': {...}, 'unsigned_datas': [...], 'signatures': [...], 'network': '...'}
    """
    
    if not is_transaction_raw(transaction_raw=transaction_raw):
        raise TransactionRawError("Invalid Bytom transaction raw.")

    transaction_raw = clean_transaction_raw(transaction_raw)
    decoded_transaction_raw = b64decode(transaction_raw.encode())
    loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

    url = f"{config[loaded_transaction_raw['network']]['bytom-core']}/decode-raw-transaction"
    data = dict(raw_transaction=loaded_transaction_raw["raw"])
    response = requests.post(
        url=url, data=json.dumps(data), headers=headers, timeout=timeout
    )
    response_json = response.json()
    if response.status_code == 400:
        raise APIError(response_json["msg"], response_json["code"])

    return dict(
        fee=loaded_transaction_raw["fee"],
        address=loaded_transaction_raw["address"],
        type=loaded_transaction_raw["type"],
        tx=response_json["data"],
        unsigned_datas=loaded_transaction_raw["unsigned_datas"],
        signatures=loaded_transaction_raw["signatures"],
        network=loaded_transaction_raw["network"]
    )


def submit_transaction_raw(transaction_raw: str, headers: dict = config["headers"],
                           timeout: int = config["timeout"]) -> dict:
    """
    Submit Bytom transaction raw.

    :param transaction_raw: Bytom transaction raw.
    :type transaction_raw: str
    :param headers: Request headers, default to common headers.
    :type headers: dict
    :param timeout: Request timeout, default to 60.
    :type timeout: int
    :returns: dict -- Bytom submitted.

    >>> from swap.providers.bytom.utils import submit_transaction_raw
    >>> submit_transaction_raw(transaction_raw)
    {'fee': ..., 'type': '...', 'transaction_id': '...', 'network': '...', 'date': '...'}
    """

    if not is_transaction_raw(transaction_raw=transaction_raw):
        raise TransactionRawError("Invalid Bytom transaction raw.")

    transaction_raw = clean_transaction_raw(transaction_raw)
    decoded_transaction_raw = b64decode(transaction_raw.encode())
    loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

    url = f"{config[loaded_transaction_raw['network']]['blockcenter']['v3']}/merchant/submit-payment"
    data = dict(raw_transaction=loaded_transaction_raw["raw"], signatures=loaded_transaction_raw["signatures"])
    params = dict(address=loaded_transaction_raw["address"])
    response = requests.post(
        url=url, data=json.dumps(data), params=params, headers=headers, timeout=timeout
    )
    response_json = response.json()
    if response_json["code"] != 200:
        raise APIError(response_json["msg"], response_json["code"])

    return dict(
        fee=loaded_transaction_raw["fee"],
        type=loaded_transaction_raw["type"],
        transaction_id=response_json["data"]["tx_hash"],
        network=loaded_transaction_raw["network"],
        date=str(datetime.datetime.utcnow())
    )
