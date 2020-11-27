#!/usr/bin/env python3

import requests
import json

from ...exceptions import (
    BalanceError, APIError, NetworkError, AddressError
)
from ..config import vapor
from .utils import (
    is_network, is_address
)

# Vapor config
config: dict = vapor()


def get_balance(address: str, asset: str = config["asset"], network: str = config["network"],
                headers: dict = config["headers"], timeout: int = config["timeout"]) -> int:
    """
    Get Vapor balance.

    :param address: Vapor address.
    :type address: str
    :param asset: Vapor asset, default to BTM asset.
    :type asset: str
    :param network: Vapor network, defaults to mainnet.
    :type network: str
    :param headers: Request headers, default to common headers.
    :type headers: dict
    :param timeout: Request timeout, default to 15.
    :type timeout: int
    :returns: int -- Vapor asset balance (NEU amount).

    >>> from swap.providers.vapor.rpc import get_balance
    >>> get_balance(address="bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", network="mainnet")
    2580000000
    """

    if not is_address(address=address, network=network):
        raise AddressError(f"Invalid Vapor '{address}' {network} address.")
    if not is_network(network=network):
        raise NetworkError(f"Invalid Vapor '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")

    url = f"{config[network]['blockmeta']}/address/{address}"
    response = requests.get(
        url=url, headers=headers, timeout=timeout
    )
    if response.json() is None or response.json()["data"] is None:
        return 0
    for _asset in response.json()["data"]["address"]:
        if asset == _asset["asset_id"]:
            return int(_asset["balance"])
    return 0


def build_transaction(address: str, transaction: dict, network: str = config["network"],
                      headers: dict = config["headers"], timeout: int = config["timeout"]) -> dict:
    """
    Build Vapor transaction.

    :param address: Vapor address.
    :type address: str
    :param transaction: Vapor transaction.
    :type transaction: dict
    :param network: Vapor network, defaults to mainnet.
    :type network: str
    :param headers: Request headers, default to common headers.
    :type headers: dict
    :param timeout: Request timeout, default to 60.
    :type timeout: int
    :returns: dict -- Vapor built transaction.

    >>> from swap.providers.vapor.rpc import build_transaction
    >>> build_transaction(address="bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", transaction={...}, network="mainnet")
    {...}
    """

    if not is_address(address=address, network=network):
        raise AddressError(f"Invalid Vapor '{address}' {network} address.")
    if not is_network(network=network):
        raise NetworkError(f"Invalid Vapor '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")

    url = f"{config[network]['blockcenter']}/merchant/build-advanced-tx"
    params = dict(address=address)
    response = requests.post(
        url=url, data=json.dumps(transaction), params=params, headers=config["headers"], timeout=timeout
    )
    if response.status_code == 200 and response.json()["code"] == 300:
        raise APIError(response.json()["msg"], response.json()["code"])
    elif response.status_code == 200 and response.json()["code"] == 503:
        raise APIError(response.json()["msg"], response.json()["code"])
    elif response.status_code == 200 and response.json()["code"] == 422:
        raise BalanceError(f"There is no any asset balance recorded on this '{address}' address.")
    elif response.status_code == 200 and response.json()["code"] == 515:
        raise BalanceError(f"Insufficient balance, check your balance and try again.")
    elif response.status_code == 200 and response.json()["code"] == 504:
        raise BalanceError(f"Insufficient balance, check your balance and try again.")
    return response.json()["data"][0]


def get_utxos(program: str, network: str = config["network"], asset: str = config["asset"],
              limit: int = 15, by: str = "amount", order: str = "desc",
              headers: dict = config["headers"], timeout: int = config["timeout"]) -> list:
    """
    Get Vapor unspent transaction outputs (UTXO's).

    :param program: Vapor control program.
    :type program: str
    :param network: Vapor network, defaults to mainnet.
    :type network: str
    :param asset: Vapor asset id, defaults to BTM asset.
    :type asset: str
    :param limit: Vapor utxo's limit, defaults to 15.
    :type limit: int
    :param by: Sort by, defaults to amount.
    :type by: str
    :param order: Sort order, defaults to desc.
    :type order: str
    :param headers: Request headers, default to common headers.
    :type headers: dict
    :param timeout: Request timeout, default to 60.
    :type timeout: int
    :returns: list -- Vapor unspent transaction outputs (UTXO's).

    >>> from swap.providers.vapor.rpc import get_utxos
    >>> get_utxos(program="00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", network="mainnet")
    [...]
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid Vapor '{network}' network",
                           "choose only 'mainnet' or 'testnet' networks.")

    url = f"{config[network]['blockcenter']}/q/utxos"
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
    Get Vapor transaction detail.

    :param transaction_id: Vapor transaction id.
    :type transaction_id: str
    :param network: Vapor network, defaults to mainnet.
    :type network: str
    :param headers: Request headers, default to common headers.
    :type headers: dict
    :param timeout: Request timeout, default to 60.
    :type timeout: int
    :returns: dict -- Vapor transaction detail.

    >>> from swap.providers.vapor.rpc import get_transaction
    >>> get_transaction(transaction_id="4e91bca76db112d3a356c17366df93e364a4922993414225f65390220730d0c1", network="mainnet")
    {...}
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid Vapor '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")

    url = f"{config[network]['blockmeta']}/tx/hash/{transaction_id}"
    response = requests.get(
        url=url, headers=headers, timeout=timeout
    )
    if response.status_code == 200 and response.json()["code"] == 200:
        return response.json()["data"]["transaction"]
    raise APIError(f"Not found this '{transaction_id}' vapor transaction id.", 500)


def decode_raw(raw: str, network: str = config["network"], 
               headers: dict = config["headers"], timeout: int = config["timeout"]) -> dict:
    """
    Decode original Vapor raw.

    :param raw: Vapor transaction raw.
    :type raw: str
    :param network: Vapor network, defaults to mainnet.
    :type network: str
    :param headers: Request headers, default to common headers.
    :type headers: dict
    :param timeout: Request timeout, default to 60.
    :type timeout: int
    :returns: dict -- Vapor decoded transaction raw.

    >>> from swap.providers.vapor.rpc import decode_raw
    >>> decode_raw(raw="...", network="testnet")
    {...}
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid Vapor '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")

    url = f"{config[network]['vapor-core']}/decode-raw-transaction"
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
     Submit original Vapor raw into blockchain.

    :param address: Vapor address.
    :type address: str
    :param raw: Vapor transaction raw.
    :type raw: str
    :param signatures: Vapor signed massage datas.
    :type signatures: list
    :param network: Vapor network, defaults to mainnet.
    :type network: str
    :param headers: Request headers, default to common headers.
    :type headers: dict
    :param timeout: Request timeout, default to 60.
    :type timeout: int
    :returns: str -- Vapor submitted transaction id/hash.

    >>> from swap.providers.vapor.rpc import submit_raw
    >>> submit_raw(address="...", raw="...", signatures=[[...], ...], network="...")
    "2993414225f65390220730d0c1a356c14e91bca76db112d37366df93e364a492"
    """

    if not is_address(address=address, network=network):
        raise AddressError(f"Invalid Vapor '{address}' {network} address.")
    if not is_network(network=network):
        raise NetworkError(f"Invalid Vapor '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")

    url = f"{config[network]['blockcenter']}/merchant/submit-payment"
    data = dict(raw_transaction=raw, signatures=signatures)
    params = dict(address=address)
    response = requests.post(
        url=url, data=json.dumps(data), params=params, headers=headers, timeout=timeout
    )
    response_json: dict = response.json()
    if response_json["code"] != 200 and response_json["code"] != 200:
        raise APIError(response_json["msg"], response_json["code"])
    return response_json["data"]["tx_hash"]
