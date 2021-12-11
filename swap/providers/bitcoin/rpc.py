#!/usr/bin/env python3

from btcpy.structs.transaction import MutableTransaction
from btcpy.setup import setup as stp
from typing import Optional

import requests
import json

from ...exceptions import (
    AddressError, APIError, NetworkError
)
from ..config import bitcoin as config
from .utils import (
    is_network, is_address
)


def get_balance(address: str, network: str = config["network"],
                headers: dict = config["headers"], timeout: int = config["timeout"]) -> int:
    """
    Get Bitcoin balance.

    :param address: Bitcoin address.
    :type address: str
    :param network: Bitcoin network, defaults to ``mainnet``.
    :type network: str
    :param headers: Request headers, default to ``common-headers``.
    :type headers: dict
    :param timeout: Request timeout, default to ``60``.
    :type timeout: int

    :returns: int -- Bitcoin balance (Satoshi amount).

    >>> from swap.providers.bitcoin.rpc import get_balance
    >>> get_balance(address="n1wgm6kkzMcNfAtJmes8YhpvtDzdNhDY5a", network="testnet")
    1394238
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid Bitcoin '{network}' network",
                           "choose only 'mainnet' or 'testnet' networks.")
    if not is_address(address=address, network=network):
        raise AddressError(f"Invalid Bitcoin '{address}' {network} address.")
    
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
    :param network: Bitcoin network, defaults to ``mainnet``.
    :type network: str
    :param include_script: Bitcoin include script, defaults to ``True``.
    :type include_script: bool
    :param limit: Bitcoin utxo's limit, defaults to ``15``.
    :type limit: int
    :param headers: Request headers, default to ``common-headers``.
    :type headers: dict
    :param timeout: Request timeout, default to ``60``.
    :type timeout: int
    :returns: list -- Bitcoin unspent transaction outputs (UTXO's).

    >>> from swap.providers.bitcoin.rpc import get_utxos
    >>> get_utxos(address="mkFWGt4hT11XS8dJKzzRFsTrqjjAwZfQAC", network="testnet")
    [{'tx_hash': '98c6a3d4e136d32d0848126e08325c94da2e8217593e92236471b11b42ee7999', 'block_height': 1890810, 'tx_input_n': -1, 'tx_output_n': 1, 'value': 67966, 'ref_balance': 146610, 'spent': False, 'confirmations': 5278, 'confirmed': '2020-11-09T08:53:01Z', 'double_spend': False, 'script': '76a91433ecab3d67f0e2bde43e52f41ec1ecbdc73f11f888ac'}]
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


def get_transaction(transaction_hash: str, network: str = config["network"],
                    headers: dict = config["headers"], timeout: int = config["timeout"]) -> dict:
    """
    Get Bitcoin transaction detail.

    :param transaction_hash: Bitcoin transaction hash/id.
    :type transaction_hash: str
    :param network: Bitcoin network, defaults to ``mainnet``.
    :type network: str
    :param headers: Request headers, default to ``common-headers``.
    :type headers: dict
    :param timeout: Request timeout, default to ``60``.
    :type timeout: int

    :returns: dict -- Bitcoin transaction detail.

    >>> from swap.providers.bitcoin.rpc import get_transaction
    >>> get_transaction(transaction_hash="4e91bca76db112d3a356c17366df93e364a4922993414225f65390220730d0c1", network="testnet")
    {'block_hash': '000000000000006fb2aec57209181feb54750319e47263c48eca24369bdbee86', 'block_height': 1890810, 'block_index': 37, 'hash': '98c6a3d4e136d32d0848126e08325c94da2e8217593e92236471b11b42ee7999', 'addresses': ['2N1NiQVBaSXmdZVATeST9sMQWVPeL5oA8Ks', 'mkFWGt4hT11XS8dJKzzRFsTrqjjAwZfQAC'], 'total': 77966, 'fees': 678, 'size': 224, 'preference': 'low', 'relayed_by': '104.197.28.151:18333', 'confirmed': '2020-11-09T08:53:01Z', 'received': '2020-11-09T08:47:10.889Z', 'ver': 2, 'double_spend': False, 'vin_sz': 1, 'vout_sz': 2, 'confirmations': 5279, 'confidence': 1, 'inputs': [{'prev_hash': '9825b68e57c8a924285828dde37869c2eca3bb3784b171353962f0d7e7577da1', 'output_index': 1, 'script': '483045022100e906ed456dc5d2c2546e70385b028dbbe62e9abc94324e9477c1374f8355501e02201072a242ebae5891b4be67478fa8126b45ebc2bb0ee7687773cbf1fc1099eef3012102065e8cb5fa76699079860a450bddd0e37e0ad3dbf2ddfd01d7b600231e6cde8e', 'output_value': 78644, 'sequence': 4294967295, 'addresses': ['mkFWGt4hT11XS8dJKzzRFsTrqjjAwZfQAC'], 'script_type': 'pay-to-pubkey-hash', 'age': 1837431}], 'outputs': [{'value': 10000, 'script': 'a914592ba3ba46263dc5c976ede5a6f91f75e5b6f69f87', 'addresses': ['2N1NiQVBaSXmdZVATeST9sMQWVPeL5oA8Ks'], 'script_type': 'pay-to-script-hash'}, {'value': 67966, 'script': '76a91433ecab3d67f0e2bde43e52f41ec1ecbdc73f11f888ac', 'addresses': ['mkFWGt4hT11XS8dJKzzRFsTrqjjAwZfQAC'], 'script_type': 'pay-to-pubkey-hash'}]}
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid Bitcoin '{network}' network",
                           "choose only 'mainnet' or 'testnet' networks.")

    url = f"{config[network]['blockcypher']['url']}/txs/{transaction_hash}"
    parameter = dict(token=config[network]["blockcypher"]["token"])
    response = requests.get(
        url=url, params=parameter, headers=headers, timeout=timeout
    )
    response_json = response.json()
    return response_json


def find_p2sh_utxo(transaction: dict) -> Optional[dict]:
    """
    Find Bitcoin pay to script hash UTXO info's.

    :param transaction: Bitcoin transaction detail.
    :type transaction: dict

    :returns: dict -- Pay to Secript Hash (P2SH) UTXO info's.

    >>> from swap.providers.bitcoin.rpc import find_p2sh_utxo, get_transaction
    >>> find_p2sh_utxo(transaction=get_transaction("868f81fd172b8f1d24e0c195af011489c3a7948513521d4b6257b8b5fb2ef409", "testnet"))
    {'value': 10050780, 'script': 'a9149418feed4647e156d6663db3e0cef7c050d0386787', 'addresses': ['2N6kHwQy6Ph5EdKNgzGrcW2WhGHKGfmP5ae'], 'script_type': 'pay-to-script-hash'}
    """

    transaction_outputs, utxo, position = transaction["outputs"], None, 0
    for index, transaction_output in enumerate(transaction_outputs):
        if transaction_output["script_type"] == "pay-to-script-hash":
            utxo = transaction_output
            position += index
            break
    return dict(position=position, **utxo)


def decode_raw(raw: str, network: str = config["network"], offline: bool = True,
               headers: dict = config["headers"], timeout: int = config["timeout"]) -> dict:
    """
    Decode original Bitcoin raw.

    :param raw: Bitcoin transaction raw.
    :type raw: str
    :param network: Bitcoin network, defaults to ``mainnet``.
    :type network: str
    :param offline: Offline decode, defaults to ``True``.
    :type offline: bool
    :param headers: Request headers, default to ``common-headers``.
    :type headers: dict
    :param timeout: Request timeout, default to ``60``.
    :type timeout: int

    :returns: dict -- Bitcoin decoded transaction raw.

    >>> from swap.providers.bitcoin.rpc import decode_raw
    >>> decode_raw(raw="02000000011823f39a8c5f6f27845dd13a65e03fe2ef5108d235e7a36edb6eb267b0459c5a010000006a47304402207018b7fd1ba6624fe9bb0f16cd65fa243d202e32fdff452699f56465b61ab648022009f0dc1a0a63109246c45e120fc0d34b40e789dfc4d05e64f269602c7d67d9210121027f0dc0894bd690635412af782d05e4f79d3d40bf568978c650f3f1ca1a96cf36ffffffff02102700000000000017a9149418feed4647e156d6663db3e0cef7c050d038678734330100000000001976a91433ecab3d67f0e2bde43e52f41ec1ecbdc73f11f888ac00000000", network="testnet")
    {'hex': '02000000011823f39a8c5f6f27845dd13a65e03fe2ef5108d235e7a36edb6eb267b0459c5a010000006a47304402207018b7fd1ba6624fe9bb0f16cd65fa243d202e32fdff452699f56465b61ab648022009f0dc1a0a63109246c45e120fc0d34b40e789dfc4d05e64f269602c7d67d9210121027f0dc0894bd690635412af782d05e4f79d3d40bf568978c650f3f1ca1a96cf36ffffffff02102700000000000017a9149418feed4647e156d6663db3e0cef7c050d038678734330100000000001976a91433ecab3d67f0e2bde43e52f41ec1ecbdc73f11f888ac00000000', 'txid': '6e5c80f600f45acda3c3101128bb3075bf2cf7af4bab0d99c9d856ebfb4b0953', 'hash': '6e5c80f600f45acda3c3101128bb3075bf2cf7af4bab0d99c9d856ebfb4b0953', 'size': 223, 'vsize': 223, 'version': 2, 'locktime': 0, 'vin': [{'txid': '5a9c45b067b26edb6ea3e735d20851efe23fe0653ad15d84276f5f8c9af32318', 'vout': 1, 'scriptSig': {'asm': '304402207018b7fd1ba6624fe9bb0f16cd65fa243d202e32fdff452699f56465b61ab648022009f0dc1a0a63109246c45e120fc0d34b40e789dfc4d05e64f269602c7d67d92101 027f0dc0894bd690635412af782d05e4f79d3d40bf568978c650f3f1ca1a96cf36', 'hex': '47304402207018b7fd1ba6624fe9bb0f16cd65fa243d202e32fdff452699f56465b61ab648022009f0dc1a0a63109246c45e120fc0d34b40e789dfc4d05e64f269602c7d67d9210121027f0dc0894bd690635412af782d05e4f79d3d40bf568978c650f3f1ca1a96cf36'}, 'sequence': '4294967295'}], 'vout': [{'value': '0.00010000', 'n': 0, 'scriptPubKey': {'asm': 'OP_HASH160 9418feed4647e156d6663db3e0cef7c050d03867 OP_EQUAL', 'hex': 'a9149418feed4647e156d6663db3e0cef7c050d0386787', 'type': 'p2sh', 'address': '2N6kHwQy6Ph5EdKNgzGrcW2WhGHKGfmP5ae'}}, {'value': '0.00078644', 'n': 1, 'scriptPubKey': {'asm': 'OP_DUP OP_HASH160 33ecab3d67f0e2bde43e52f41ec1ecbdc73f11f8 OP_EQUALVERIFY OP_CHECKSIG', 'hex': '76a91433ecab3d67f0e2bde43e52f41ec1ecbdc73f11f888ac', 'type': 'p2pkh', 'address': 'mkFWGt4hT11XS8dJKzzRFsTrqjjAwZfQAC'}}]}
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid Bitcoin '{network}' network",
                           "choose only 'mainnet' or 'testnet' networks.")

    if offline:
        stp(network, strict=True, force=True)
        tx = MutableTransaction.unhexlify(raw)
        return tx.to_json()

    url = f"{config[network]['blockcypher']['url']}/txs/decode"
    parameter = dict(token=config[network]["blockcypher"]["token"])
    data = dict(tx=raw)
    response = requests.post(
        url=url, data=json.dumps(data), params=parameter, headers=headers, timeout=timeout
    )
    response_json = response.json()
    return response_json


def submit_raw(raw: str, network: str = config["network"], endpoint: str = "sochain",
               headers: dict = config["headers"], timeout: int = config["timeout"]) -> str:
    """
    Submit original Bitcoin raw into blockchain.

    :param raw: Bitcoin transaction raw.
    :type raw: str
    :param network: Bitcoin network, defaults to ``mainnet``.
    :type network: str
    :param endpoint: Bitcoin transaction submiter endpoint api name, defaults to ``sochain``.
    :type endpoint: str
    :param headers: Request headers, default to ``common-headers``.
    :type headers: dict
    :param timeout: Request timeout, default to ``60``.
    :type timeout: int

    :returns: dict -- Bitcoin submitted transaction id/hash.

    >>> from swap.providers.bitcoin.rpc import submit_raw
    >>> submit_raw(raw="02000000011823f39a8c5f6f27845dd13a65e03fe2ef5108d235e7a36edb6eb267b0459c5a010000006a47304402207018b7fd1ba6624fe9bb0f16cd65fa243d202e32fdff452699f56465b61ab648022009f0dc1a0a63109246c45e120fc0d34b40e789dfc4d05e64f269602c7d67d9210121027f0dc0894bd690635412af782d05e4f79d3d40bf568978c650f3f1ca1a96cf36ffffffff02102700000000000017a9149418feed4647e156d6663db3e0cef7c050d038678734330100000000001976a91433ecab3d67f0e2bde43e52f41ec1ecbdc73f11f888ac00000000", network="testnet")
    "167faa4043ff622e7860ee5228d1ad6d763c5a6cfce79dbc3b9b5fc7bded6394"
    """

    if not is_network(network=network):
        raise NetworkError(f"Invalid Bitcoin '{network}' network",
                           "choose only 'mainnet' or 'testnet' networks.")

    if endpoint == "smartbit":
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
    elif endpoint == "sochain":
        url = str(config[network]['sochain']).format(links="send_tx")
        data = dict(tx_hex=raw)
        response = requests.post(
            url=url, data=json.dumps(data), headers=headers, timeout=timeout
        )
        response_json = response.json()
        if "status" in response_json and response_json["status"] == "success":
            return response_json["data"]["txid"]
        elif "status" in response_json and response_json["status"] == "fail":
            raise APIError(response_json["data"]["tx_hex"])
        else:
            raise APIError("Unknown Bitcoin submit payment error.")
    else:
        raise TypeError("Invalid Bitcoin endpoint api name, please choose only smartbit or sochain only.")
