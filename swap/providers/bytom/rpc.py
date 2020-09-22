#!/usr/bin/env python3

import requests
import json

from ...utils.exceptions import (
    ClientError, APIError, NetworkError, AddressError
)
from ..config import bytom
from .utils import (
    is_network, is_address
)

# Bytom config
config = bytom()


def get_balance(address: str, asset: str = config["asset"], network: str = config["network"],
                headers: dict = config["headers"], timeout: int = config["timeout"]) -> int:
    """
    Get Bytom balance.

    :param address: Bytom address.
    :type address: str
    :param asset: Bytom asset, default to BTM asset.
    :type asset: str
    :param network: Bytom network, defaults to mainnet.
    :type network: str
    :param headers: Request headers, default to common headers.
    :type headers: dict
    :param timeout: Request timeout, default to 15.
    :type timeout: int
    :returns: int -- Bytom asset balance (NEU amount).

    >>> from swap.providers.bytom.rpc import get_balance
    >>> get_balance(address="bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", network="mainnet")
    2580000000
    """

    if not is_address(address=address, network=network):
        raise AddressError(f"Invalid Bytom '{address}' {network} address.")
    if not is_network(network=network):
        raise NetworkError(f"Invalid Bytom '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")

    url = f"{config[network]['blockmeta']}/address/{address}/asset"
    response = requests.get(
        url=url, headers=headers, timeout=timeout
    )
    response_json = response.json()
    if response_json is None:
        return 0
    for _asset in response_json:
        if asset == _asset["asset_id"]:
            return int(_asset["balance"])
    return 0


def build_transaction(address: str, transaction: dict, network: str = config["network"],
                      headers: dict = config["headers"], timeout: int = config["timeout"]) -> dict:
    """
    Build Bytom transaction.

    :param address: Bytom address.
    :type address: str
    :param transaction: Bytom transaction.
    :type transaction: dict
    :param network: Bytom network, defaults to mainnet.
    :type network: str
    :param headers: Request headers, default to common headers.
    :type headers: dict
    :param timeout: Request timeout, default to 60.
    :type timeout: int
    :returns: dict -- Bytom built transaction.

    >>> from swap.providers.bytom.rpc import build_transaction
    >>> build_transaction(address="bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", transaction={...}, network="mainnet")
    {...}
    """

    if not is_address(address=address, network=network):
        raise AddressError(f"Invalid Bytom '{address}' {network} address.")
    if not is_network(network=network):
        raise NetworkError(f"Invalid Bytom '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")

    url = f"{config[network]['blockcenter']['v3']}/merchant/build-advanced-tx"
    params = dict(address=address)
    response = requests.post(
        url=url, data=json.dumps(transaction), params=params, headers=headers, timeout=timeout
    )
    response_json = response.json()
    if response.status_code == 200 and response_json["code"] == 300:
        raise APIError(response_json["msg"], response_json["code"])
    elif response.status_code == 200 and response_json["code"] == 503:
        raise APIError(response_json["msg"], response_json["code"])
    elif response.status_code == 200 and response_json["code"] == 422:
        raise ClientError(f"There is no any asset balance recorded on this '{address}' address.")
    return response_json["data"][0]


def get_utxos(program: str, network: str = config["network"], asset: str = config["asset"],
              limit: int = 15, by: str = "amount", order: str = "desc",
              headers: dict = config["headers"], timeout: int = config["timeout"]) -> list:
    """
    Get Bytom unspent transaction outputs (UTXO's).

    :param program: Bytom control program.
    :type program: str
    :param network: Bytom network, defaults to mainnet.
    :type network: str
    :param asset: Bytom asset id, defaults to BTM asset.
    :type asset: str
    :param limit: Bytom utxo's limit, defaults to 15.
    :type limit: int
    :param by: Sort by, defaults to amount.
    :type by: str
    :param order: Sort order, defaults to desc.
    :type order: str
    :param headers: Request headers, default to common headers.
    :type headers: dict
    :param timeout: Request timeout, default to 60.
    :type timeout: int
    :returns: list -- Bytom unspent transaction outputs (UTXO's).

    >>> from swap.providers.bytom.rpc import get_utxos
    >>> get_utxos(program="00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", network="mainnet")
    [...]
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid Bytom '{network}' network",
                           "choose only 'mainnet' or 'testnet' networks.")

    url = f"{config[network]['blockcenter']['v3']}/q/utxos"
    data = dict(filter=dict(script=program, asset=asset), sort=dict(by=by, order=order))
    params = dict(limit=limit)
    response = requests.post(
        url=url, data=json.dumps(data), params=params, headers=headers, timeout=timeout
    )
    response_json = response.json()
    return response_json["data"]


def get_transaction(transaction_id: str, network: str = config["network"],
                    headers: dict = config["headers"], timeout: int = config["timeout"]) -> dict:
    """
    Get Bytom transaction detail.

    :param transaction_id: Bytom transaction id.
    :type transaction_id: str
    :param network: Bytom network, defaults to mainnet.
    :type network: str
    :param headers: Request headers, default to common headers.
    :type headers: dict
    :param timeout: Request timeout, default to 60.
    :type timeout: int
    :returns: dict -- Bytom transaction detail.

    >>> from swap.providers.bytom.rpc import get_transaction
    >>> get_transaction(transaction_id="4e91bca76db112d3a356c17366df93e364a4922993414225f65390220730d0c1", network="mainnet")
    {...}
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid Bytom '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")

    url = f"{config[network]['blockcenter']['v2']}/merchant/get-transaction"
    response = requests.post(
        url=url, data=json.dumps(dict(tx_id=transaction_id)), headers=headers, timeout=timeout
    )
    response_json = response.json()
    if response.status_code == 200 and response_json["code"] == 300:
        raise APIError(response_json["msg"], response_json["code"])
    return response_json["result"]["data"]


def decode_raw(raw: str, network: str = config["network"], 
               headers: dict = config["headers"], timeout: int = config["timeout"]) -> dict:
    """
    Decode original Bytom raw.

    :param raw: Bytom transaction raw.
    :type raw: str
    :param network: Bytom network, defaults to mainnet.
    :type network: str
    :param headers: Request headers, default to common headers.
    :type headers: dict
    :param timeout: Request timeout, default to 60.
    :type timeout: int
    :returns: dict -- Bytom decoded transaction raw.

    >>> from swap.providers.bytom.rpc import decode_raw
    >>> decode_raw(raw="...", network="testnet")
    {...}
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid Bytom '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")

    url = f"{config[network]['bytom-core']}/decode-raw-transaction"
    data = dict(raw_transaction=raw)
    response = requests.post(
        url=url, data=json.dumps(data), headers=headers, timeout=timeout
    )
    response_json = response.json()
    if response.status_code == 400:
        raise APIError(response_json["msg"], response_json["code"])
    return response_json["data"]


def submit_raw(address: str, raw: str, signatures: list, network: str = config["network"],
               headers: dict = config["headers"], timeout: int = config["timeout"]) -> str:
    """
     Submit original Bytom raw into blockchain.

    :param address: Bytom address.
    :type address: str
    :param raw: Bytom transaction raw.
    :type raw: str
    :param signatures: Bytom signed massage datas.
    :type signatures: list
    :param network: Bytom network, defaults to mainnet.
    :type network: str
    :param headers: Request headers, default to common headers.
    :type headers: dict
    :param timeout: Request timeout, default to 60.
    :type timeout: int
    :returns: str -- Bytom submitted transaction id/hash.

    >>> from swap.providers.bytom.rpc import submit_raw
    >>> submit_raw(address="...", raw="...", signatures=[[...], ...], network="...")
    "2993414225f65390220730d0c1a356c14e91bca76db112d37366df93e364a492"
    """

    if not is_address(address=address, network=network):
        raise AddressError(f"Invalid Bytom '{address}' {network} address.")
    if not is_network(network=network):
        raise NetworkError(f"Invalid Bytom '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")

    url = f"{config[network]['blockcenter']['v3']}/merchant/submit-payment"
    data = dict(raw_transaction=raw, signatures=signatures)
    params = dict(address=address)
    response = requests.post(
        url=url, data=json.dumps(data), params=params, headers=headers, timeout=timeout
    )
    response_json = response.json()
    if response_json["code"] != 200:
        raise APIError(response_json["msg"], response_json["code"])
    return response_json["data"]["tx_hash"]
