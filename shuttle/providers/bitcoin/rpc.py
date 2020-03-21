#!/usr/bin/env python3

import requests
import json

from ..config import bitcoin
from ...utils.exceptions import AddressError, APIError
from .utils import is_address


# Request headers
headers = dict()
headers.setdefault("Content-Type", "application/json")

# Bitcoin configuration
bitcoin = bitcoin()


# Get balance by address
def get_balance(address, network="testnet", timeout=bitcoin["timeout"]):
    """
    Get bitcoin balance.

    :param address: bitcoin address.
    :type address: str
    :param network: bitcoin network, defaults to testnet.
    :type network: str
    :param timeout: request timeout, default to 15.
    :type timeout: int
    :returns: int -- bitcoin balance.

    >>> from shuttle.providers.bitcoin.rpc import get_balance
    >>> get_balance(bitcoin_address, "mainnet")
    25800000
    """

    if not is_address(address=address, network=network):
        raise AddressError("invalid %s %s address" % (network, address))
    url = str(bitcoin[network]["blockcypher"]["url"]) + ("/addrs/%s/balance" % address)
    return requests.get(url=url, headers=headers, timeout=timeout).json()["balance"]


# Get unspent transaction by address
def get_unspent_transactions(address, network="testnet",
                             include_script=True, limit=15, timeout=bitcoin["timeout"]):
    """
    Get bitcoin unspent transaction output (UTXO).

    :param address: bitcoin address.
    :type address: str
    :param network: bitcoin network, defaults to testnet.
    :type network: str
    :param include_script: bitcoin include script, defaults to True.
    :type include_script: bool
    :param limit: bitcoin utxo's limit, defaults to 15.
    :type limit: int
    :param timeout: request timeout, default to 15.
    :type timeout: int
    :returns: list -- bitcoin utxo's.

    >>> from shuttle.providers.bitcoin.rpc import get_unspent_transactions
    >>> get_unspent_transactions(bitcoin_address, "testnet")
    [...]
    """

    if not is_address(address=address, network=network):
        raise AddressError("invalid %s %s address" % (network, address))
    _include_script = "true" if include_script else "false"
    parameter = dict(limit=limit, unspentOnly="true",
                     includeScript=_include_script, token=bitcoin[network]["blockcypher"]["token"])
    url = bitcoin[network]["blockcypher"]["url"] + ("/addrs/%s" % address)
    response = requests.get(url=url, params=parameter, headers=headers, timeout=timeout).json()
    return response["txrefs"] if "txrefs" in response else []


# Get transaction detail by hash
def get_transaction_detail(transaction_id, network="testnet", timeout=bitcoin["timeout"]):
    """
    Get transaction detail.

    :param transaction_id: bitcoin transaction hash or transaction id.
    :type transaction_id: str
    :param network: bitcoin network, defaults to testnet.
    :type network: str
    :param timeout: request timeout, default to 15.
    :type timeout: int
    :returns: dict -- bitcoin transaction detail.

    >>> from shuttle.providers.bitcoin.rpc import get_transaction_detail
    >>> get_transaction_detail(transaction_id, "testnet")
    {...}
    """

    parameter = dict(token=bitcoin[network]["blockcypher"]["token"])
    url = bitcoin[network]["blockcypher"]["url"] + ("/txs/%s" % transaction_id)
    return requests.get(url=url, params=parameter,
                        headers=headers, timeout=timeout).json()


# Getting decode transaction by transaction raw
def decoded_transaction_raw(transaction_raw, network="testnet", timeout=bitcoin["timeout"]):
    """
    Get decoded transaction raw.

    :param transaction_raw: bitcoin transaction raw.
    :type transaction_raw: str
    :param network: bitcoin network, defaults to testnet.
    :type network: str
    :param timeout: request timeout, default to 15.
    :type timeout: int
    :returns: dict -- bitcoin decoded transaction raw.

    >>> from shuttle.providers.bitcoin.rpc import decoded_transaction_raw
    >>> decoded_transaction_raw(transaction_raw, "testnet")
    {...}
    """

    if isinstance(transaction_raw, str):
        parameter = dict(token=bitcoin[network]["blockcypher"]["token"])
        tx = json.dumps(dict(tx=transaction_raw))
        return requests.post(url=bitcoin[network]["blockcypher"]["url"] + "/txs/decode",
                             data=tx, params=parameter, headers=headers, timeout=timeout).json()
    raise TypeError("transaction raw must be string format!")


# Submit payment from blockcypher
def submit_payment(tx_raw, network="testnet", timeout=bitcoin["timeout"]):
    """
    Submit transaction raw to Bitcoin blockchain.

    :param tx_raw: bitcoin transaction raw.
    :type tx_raw: str
    :param network: bitcoin network, defaults to testnet.
    :type network: str
    :param timeout: request timeout, default to 15.
    :type timeout: int
    :returns: dict -- bitcoin decoded transaction raw.

    >>> from shuttle.providers.bitcoin.rpc import submit_payment
    >>> submit_payment(transaction_raw, "testnet")
    {...}
    """

    if isinstance(tx_raw, str):
        tx = json.dumps(dict(tx=tx_raw))
        parameter = dict(token=bitcoin[network]["blockcypher"]["token"])
        response = requests.post(url=bitcoin[network]["blockcypher"]["url"] + "/txs/push",
                                 data=tx, params=parameter, headers=headers, timeout=timeout)
        if "error" in response.json():
            raise APIError(response.json()["error"])
        return response.json()
    raise TypeError("transaction raw must be string format!")
