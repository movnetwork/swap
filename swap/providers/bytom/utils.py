#!/usr/bin/env python3

from base64 import b64decode
from pybytom.utils import is_address as btm_is_address
from typing import Optional, Union

import json
import binascii
import datetime

from ..config import bytom
from ...utils.exceptions import (
    NetworkError, TransactionRawError, SymbolError
)
from .rpc import decode_transaction_raw, submit_transaction_raw

# Bytom config.
config = bytom()


def is_address(address: str, network: Optional[str] = None) -> bool:
    """
    Check Bytom address.

    :param address: Bytom address.
    :type address: str
    :param network: Bytom network, defaults to None.
    :type network: str
    :returns: bool -- Bytom valid/Invalid address.

    >>> from swap.providers.bytom.utils import is_address
    >>> is_address("bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "mainnet")
    True
    """

    if network is None:
        return btm_is_address(address=address)
    elif not isinstance(network, str) or network not in ["mainnet", "solonet", "testnet"]:
        raise NetworkError(f"Invalid `{network}` network", "only takes mainnet, solonet or testnet networks.")
    return btm_is_address(address=address, network=network)


def amount_converter(amount: Union[int, float], symbol: str = "NEU2BTM") -> Union[int, float]:
    """
    Amount converter

    :param amount: Bytom amount.
    :type amount: Union[int, float]
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


def decode_swap_transaction_raw(transaction_raw: str) -> dict:
    """
    Decode swap Bytom transaction raw.

    :param transaction_raw: Bytom transaction raw.
    :type transaction_raw: str
    :returns: dict -- decoded Bytom transaction.

    >>> from swap.providers.bytom.utils import decode_swap_transaction_raw
    >>> decode_swap_transaction_raw(transaction_raw)
    {'fee': ..., 'type': '...', 'address': '...', 'transaction': {...}, 'unsigned_datas': [...], 'signatures': [...], 'network': '...'}
    """

    try:
        # Fixing transaction raw.
        swap_transaction_raw = str(transaction_raw + "=" * (-len(transaction_raw) % 4))
        # Decoding transaction raw
        decoded_swap_transaction_raw = json.loads(b64decode(str(swap_transaction_raw).encode()).decode())
    except (binascii.Error, json.decoder.JSONDecodeError) as _error:
        raise TransactionRawError("Invalid swap Bytom transaction raw.")
    if "type" not in decoded_swap_transaction_raw:
        raise TransactionRawError("Invalid swap Bytom transaction raw, it has not transaction type.")
    elif not str(decoded_swap_transaction_raw["type"]).startswith("bytom"):
        raise TransactionRawError("Invalid swap Bytom transaction raw, it is not Bytom type.")

    return dict(
        fee=decoded_swap_transaction_raw["fee"],
        address=decoded_swap_transaction_raw["address"],
        type=decoded_swap_transaction_raw["type"],
        tx=decode_transaction_raw(transaction_raw=decoded_swap_transaction_raw["raw"]),
        unsigned_datas=decoded_swap_transaction_raw["unsigned_datas"],
        signatures=decoded_swap_transaction_raw["signatures"],
        network=decoded_swap_transaction_raw["network"]
    )


def submit_swap_transaction_raw(transaction_raw: str) -> dict:
    """
    Submit swap Bytom transaction raw.

    :param transaction_raw: Bytom transaction raw.
    :type transaction_raw: str
    :returns: dict -- Bytom submitted fee, type, transaction id, network and date.

    >>> from swap.providers.bytom.utils import submit_swap_transaction_raw
    >>> submit_swap_transaction_raw(transaction_raw)
    {'fee': ..., 'type': '...', 'transaction_id': '...', 'network': '...', 'date': '...'}
    """

    try:
        # Fixing transaction raw.
        transaction_raw = str(transaction_raw + "=" * (-len(transaction_raw) % 4))
        # Decoding transaction raw.
        decoded_swap_transaction_raw = json.loads(b64decode(str(transaction_raw).encode()).decode())
    except (binascii.Error, json.decoder.JSONDecodeError) as _error:
        raise TransactionRawError("Invalid swap Bytom transaction raw.")
    if "type" not in decoded_swap_transaction_raw:
        raise TransactionRawError("Invalid swap Bytom transaction raw, it has not transaction type.")
    elif not str(decoded_swap_transaction_raw["type"]).startswith("bytom"):
        raise TransactionRawError("Invalid swap Bytom transaction raw, it is not Bytom type.")

    submitted_swap_transaction_id = submit_transaction_raw(
        address=decoded_swap_transaction_raw["address"],
        transaction_raw=decoded_swap_transaction_raw["raw"],
        signatures=decoded_swap_transaction_raw["signatures"],
        network=decoded_swap_transaction_raw["network"]
    )
    return dict(
        fee=decoded_swap_transaction_raw["fee"],
        type=decoded_swap_transaction_raw["type"],
        transaction_id=submitted_swap_transaction_id,
        network=decoded_swap_transaction_raw["network"],
        date=str(datetime.datetime.utcnow())
    )
