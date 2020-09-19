#!/usr/bin/env python3

from pybytom.utils import is_network, is_address

import requests
import json

from ...utils.exceptions import (
    ClientError, APIError, NetworkError, AddressError
)
from ..config import bytom

# Bytom config
config = bytom()


def get_balance(address: str, asset: str = config["asset"],
                network: str = config["network"], timeout: int = config["timeout"]) -> int:
    """
    Get Bytom balance.

    :param address: Bytom address.
    :type address: str
    :param asset: Bytom asset, default to BTM asset.
    :type asset: str
    :param network: Bytom network, defaults to mainnet.
    :type network: str
    :param timeout: request timeout, default to 15.
    :type timeout: int
    :returns: int -- Bytom asset balance (NEU amount).

    >>> from swap.providers.bytom.rpc import get_balance
    >>> get_balance(address="bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", network="mainnet")
    2580000000
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid '{network}' network, must be 'mainnet', 'solonet' or 'testnet' networks.")
    if not is_address(address=address, network=network):
        raise AddressError(f"Invalid '{address}' {network} address/type")

    url = f"{config[network]['blockmeta']}/address/{address}/asset"
    response = requests.get(url=url, headers=config["headers"], timeout=timeout)
    if response.json() is None:
        return 0
    for _asset in response.json():
        if asset == _asset["asset_id"]:
            return int(_asset["balance"])
    return 0


def build_transaction(address: str, transaction: dict,
                      network: str = config["network"], timeout: int = config["timeout"]) -> dict:
    """
    Build Bytom transaction.

    :param address: Bytom address.
    :type address: str
    :param transaction: Bytom transaction.
    :type transaction: dict
    :param network: Bytom network, defaults to mainnet.
    :type network: str
    :param timeout: request timeout, default to 60.
    :type timeout: int
    :returns: dict -- Bytom built transaction.

    >>> from swap.providers.bytom.rpc import build_transaction
    >>> build_transaction(address="bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", transaction={...}, network="mainnet")
    {...}
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid '{network}' network, must be 'mainnet', 'solonet' or 'testnet' networks.")
    if not is_address(address=address, network=network):
        raise AddressError(f"Invalid '{address}' {network} address/type")

    url = f"{config[network]['blockcenter']['v3']}/merchant/build-advanced-tx"
    params = dict(address=address)
    response = requests.post(
        url=url, data=json.dumps(transaction), params=params, headers=config["headers"], timeout=timeout
    )
    if response.status_code == 200 and response.json()["code"] == 300:
        raise APIError(response.json()["msg"], response.json()["code"])
    elif response.status_code == 200 and response.json()["code"] == 503:
        raise APIError(response.json()["msg"], response.json()["code"])
    elif response.status_code == 200 and response.json()["code"] == 422:
        raise ClientError(f"There is no any asset balance recorded on this '{address}' address.")
    return response.json()["data"][0]


def get_transaction(transaction_id: str, network: str = config["network"],
                    timeout: int = config["timeout"]) -> dict:
    """
    Get Bytom transaction detail.

    :param transaction_id: Bytom transaction id.
    :type transaction_id: str
    :param network: Bytom network, defaults to mainnet.
    :type network: str
    :param timeout: request timeout, default to 60.
    :type timeout: int
    :returns: dict -- Bytom transaction detail.

    >>> from swap.providers.bytom.rpc import get_transaction
    >>> get_transaction(transaction_id="4e91bca76db112d3a356c17366df93e364a4922993414225f65390220730d0c1", network="mainnet")
    {...}
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid '{network}' network/type",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")
    url = f"{config[network]['blockcenter']['v2']}/merchant/get-transaction"
    response = requests.post(
        url=url, data=json.dumps(dict(tx_id=transaction_id)), headers=config["headers"], timeout=timeout
    )
    if response.status_code == 200 and response.json()["code"] == 300:
        raise APIError(response.json()["msg"], response.json()["code"])
    return response.json()["result"]["data"]


def submit_transaction_raw(address: str, transaction_raw: str, signatures: list,
                           network: str = config["network"], timeout: int = config["timeout"]) -> str:
    """
     Submit Bytom transaction raw to blockchain.

    :param address: Bytom address.
    :type address: str
    :param transaction_raw: Bytom transaction raw.
    :type transaction_raw: str
    :param signatures: Bytom signed datas.
    :type signatures: list
    :param network: Bytom network, defaults to solonet.
    :type network: str
    :param timeout: request timeout, default to 60.
    :type timeout: int
    :returns: str -- Bytom submitted transaction id/hash.

    >>> from swap.providers.bytom.rpc import submit_transaction_raw
    >>> submit_transaction_raw(address="bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", transaction_raw="...", signatures=[[...], ...], network="mainnet")
    "2993414225f65390220730d0c1a356c14e91bca76db112d37366df93e364a492"
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid '{network}' network, must be 'mainnet', 'solonet' or 'testnet' networks.")

    url = f"{config[network]['blockcenter']['v3']}/merchant/submit-payment"
    data = dict(raw_transaction=transaction_raw, signatures=signatures)
    params = dict(address=address)
    response = requests.post(
        url=url, data=json.dumps(data), params=params, headers=config["headers"], timeout=timeout
    )
    if response.json()["code"] != 200:
        raise APIError(response.json()["msg"], response.json()["code"])
    return response.json()["data"]["tx_hash"]


def decode_transaction_raw(transaction_raw: str, network: str = config["network"],
                           timeout: int = config["timeout"]) -> dict:
    """
    Get decode transaction raw.

    :param transaction_raw: Bytom transaction raw.
    :type transaction_raw: str
    :param network: Bytom network, defaults to solonet.
    :type network: str
    :param timeout: request timeout, default to 60.
    :type timeout: int
    :returns: dict -- Bytom decoded transaction raw.

    >>> from swap.providers.bytom.rpc import decode_transaction_raw
    >>> decode_transaction_raw(transaction_raw="...", network="testnet")
    {...}
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid '{network}' network/type",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")
    url = f"{config[network]['bytom-core']}/decode-raw-transaction"
    data = dict(raw_transaction=transaction_raw)
    response = requests.post(
        url=url, data=json.dumps(data), headers=config["headers"], timeout=timeout
    )
    if response.status_code == 400:
        raise APIError(response.json()["msg"], response.json()["code"])
    return response.json()["data"]
