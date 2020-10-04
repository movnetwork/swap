#!/usr/bin/env python3

from btcpy.structs.transaction import MutableTransaction
from btcpy.setup import setup as stp

import requests
import json

from ...utils.exceptions import (
    AddressError, APIError, NetworkError
)
from ..config import bitcoin
from .utils import (
    is_network, is_address
)

# Bitcoin config
config = bitcoin()


def get_balance(address: str, network: str = config["network"],
                headers: dict = config["headers"], timeout: int = config["timeout"]) -> int:
    """
    Get Bitcoin balance.

    :param address: Bitcoin address.
    :type address: str
    :param network: Bitcoin network, defaults to testnet.
    :type network: str
    :param headers: Request headers, default to common headers.
    :type headers: dict
    :param timeout: Request timeout, default to 60.
    :type timeout: int
    :returns: int -- Bitcoin balance (SATOSHI amount).

    >>> from swap.providers.bitcoin.rpc import get_balance
    >>> get_balance(address="mkFWGt4hT11XS8dJKzzRFsTrqjjAwZfQAC", network="testnet")
    25800000
    """

    if not is_address(address=address, network=network):
        raise AddressError(f"Invalid Bitcoin '{address}' {network} address.")
    if not is_network(network=network):
        raise NetworkError(f"Invalid Bitcoin '{network}' network",
                           "choose only 'mainnet' or 'testnet' networks.")
    
    url = f"{config[network]['blockcypher']['url']}/addrs/{address}/balance"
    response = requests.get(
        url=url, headers=headers, timeout=timeout
    )
    response_json = response.json()
    return response_json["balance"]


def get_utxos(address: str, network: str = config["network"], include_script: bool = True,
              limit: int = 15, headers: dict = config["headers"], timeout: int = config["timeout"]) -> list:
    """
    Get Bitcoin unspent transaction outputs (UTXO's).

    :param address: Bitcoin address.
    :type address: str
    :param network: Bitcoin network, defaults to testnet.
    :type network: str
    :param include_script: Bitcoin include script, defaults to True.
    :type include_script: bool
    :param limit: Bitcoin utxo's limit, defaults to 15.
    :type limit: int
    :param headers: Request headers, default to common headers.
    :type headers: dict
    :param timeout: Request timeout, default to 60.
    :type timeout: int
    :returns: list -- Bitcoin unspent transaction outputs (UTXO's).

    >>> from swap.providers.bitcoin.rpc import get_utxos
    >>> get_utxos(address="mkFWGt4hT11XS8dJKzzRFsTrqjjAwZfQAC", network="testnet")
    [...]
    """

    if not is_address(address=address, network=network):
        raise AddressError(f"Invalid Bitcoin '{address}' {network} address.")
    if not is_network(network=network):
        raise NetworkError(f"Invalid Bitcoin '{network}' network",
                           "choose only 'mainnet' or 'testnet' networks.")
    
    parameter = dict(
        limit=limit, unspentOnly="true", 
        includeScript=("true" if include_script else "false"),
        token=config[network]["blockcypher"]["token"]
    )
    url = f"{config[network]['blockcypher']['url']}/addrs/{address}"
    response = requests.get(
        url=url, params=parameter, headers=headers, timeout=timeout
    )
    response_json = response.json()
    return response_json["txrefs"] if "txrefs" in response_json else []


def get_transaction(transaction_id: str, network: str = config["network"],
                    headers: dict = config["headers"], timeout: int = config["timeout"]) -> dict:
    """
    Get Bitcoin transaction detail.

    :param transaction_id: Bitcoin transaction id/hash.
    :type transaction_id: str
    :param network: Bitcoin network, defaults to testnet.
    :type network: str
    :param headers: Request headers, default to common headers.
    :type headers: dict
    :param timeout: Request timeout, default to 60.
    :type timeout: int
    :returns: dict -- Bitcoin transaction detail.

    >>> from swap.providers.bitcoin.rpc import get_transaction
    >>> get_transaction(transaction_id="4e91bca76db112d3a356c17366df93e364a4922993414225f65390220730d0c1", network="testnet")
    {...}
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid Bitcoin '{network}' network",
                           "choose only 'mainnet' or 'testnet' networks.")

    url = f"{config[network]['blockcypher']['url']}/txs/{transaction_id}"
    parameter = dict(token=config[network]["blockcypher"]["token"])
    response = requests.get(
        url=url, params=parameter, headers=headers, timeout=timeout
    )
    response_json = response.json()
    return response_json


def decode_raw(raw: str, network: str = config["network"], offline: bool = True,
               headers: dict = config["headers"], timeout: int = config["timeout"]) -> dict:
    """
    Decode original Bitcoin raw.

    :param raw: Bitcoin transaction raw.
    :type raw: str
    :param network: Bitcoin network, defaults to testnet.
    :type network: str
    :param offline: Offline decode, defaults to True.
    :type offline: bool
    :param headers: Request headers, default to common headers.
    :type headers: dict
    :param timeout: Request timeout, default to 60.
    :type timeout: int
    :returns: dict -- Bitcoin decoded transaction raw.

    >>> from swap.providers.bitcoin.rpc import decode_raw
    >>> decode_raw(raw="02000000011823f39a8c5f6f27845dd13a65e03fe2ef5108d235e7a36edb6eb267b0459c5a010000006a47304402207018b7fd1ba6624fe9bb0f16cd65fa243d202e32fdff452699f56465b61ab648022009f0dc1a0a63109246c45e120fc0d34b40e789dfc4d05e64f269602c7d67d9210121027f0dc0894bd690635412af782d05e4f79d3d40bf568978c650f3f1ca1a96cf36ffffffff02102700000000000017a9149418feed4647e156d6663db3e0cef7c050d038678734330100000000001976a91433ecab3d67f0e2bde43e52f41ec1ecbdc73f11f888ac00000000", network="testnet")
    {...}
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid Bitcoin '{network}' network",
                           "choose only 'mainnet' or 'testnet' networks.")

    if offline:
        stp(network, strict=True)
        tx = MutableTransaction.unhexlify(raw)
        return tx.json()

    url = f"{config[network]['blockcypher']['url']}/txs/decode"
    parameter = dict(token=config[network]["blockcypher"]["token"])
    data = dict(tx=raw)
    response = requests.post(
        url=url, data=json.dumps(data), params=parameter, headers=headers, timeout=timeout
    )
    response_json = response.json()
    return response_json


def submit_raw(raw: str, network: str = config["network"],
               headers: dict = config["headers"], timeout: int = config["timeout"]) -> str:
    """
    Submit original Bitcoin raw into blockchain.

    :param raw: Bitcoin transaction raw.
    :type raw: str
    :param network: Bitcoin network, defaults to testnet.
    :type network: str
    :param headers: Request headers, default to common headers.
    :type headers: dict
    :param timeout: Request timeout, default to 60.
    :type timeout: int
    :returns: dict -- Bitcoin submitted transaction id/hash.

    >>> from swap.providers.bitcoin.rpc import submit_raw
    >>> submit_raw(raw="02000000011823f39a8c5f6f27845dd13a65e03fe2ef5108d235e7a36edb6eb267b0459c5a010000006a47304402207018b7fd1ba6624fe9bb0f16cd65fa243d202e32fdff452699f56465b61ab648022009f0dc1a0a63109246c45e120fc0d34b40e789dfc4d05e64f269602c7d67d9210121027f0dc0894bd690635412af782d05e4f79d3d40bf568978c650f3f1ca1a96cf36ffffffff02102700000000000017a9149418feed4647e156d6663db3e0cef7c050d038678734330100000000001976a91433ecab3d67f0e2bde43e52f41ec1ecbdc73f11f888ac00000000", network="testnet")
    "167faa4043ff622e7860ee5228d1ad6d763c5a6cfce79dbc3b9b5fc7bded6394"
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid Bitcoin '{network}' network",
                           "choose only 'mainnet' or 'testnet' networks.")

    url = f"{config[network]['smartbit']}/pushtx"
    data = dict(hex=raw)
    response = requests.post(
        url=url, data=json.dumps(data), headers=headers, timeout=timeout
    )
    response_json = response.json()
    if "success" in response_json and not response_json["success"]:
        raise APIError(response_json["error"]["message"], response_json["error"]["code"])
    elif "success" in response_json and response_json["success"]:
        return response_json["txid"]
    else:
        raise APIError("Unknown Bitcoin submit payment error.")
