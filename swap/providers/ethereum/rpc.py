#!/usr/bin/env python3

from web3 import Web3
from web3.providers import (
    HTTPProvider, WebsocketProvider
)
from web3.datastructures import AttributeDict
from hexbytes.main import HexBytes
from eth_typing import URI
from typing import (
    Optional
)

from ...exceptions import (
    AddressError, NetworkError
)
from ..config import ethereum
from .utils import (
    is_network, is_address, to_checksum_address
)

# Ethereum configuration
config: dict = ethereum


def get_web3(network: str = config["network"], provider: str = config["provider"],
             token: Optional[str] = None) -> Web3:

    if not is_network(network=network):
        raise NetworkError(f"Invalid Ethereum '{network}' network",
                           "choose only 'mainnet', 'ropsten', 'kovan', 'rinkeby' or 'testnet' networks.")

    endpoint: str = "ganache-cli" if network == "testnet" else "infura"
    token: str = token if token else config[network][endpoint]["token"]

    if provider == "http":
        web3: Web3 = Web3(HTTPProvider(
                URI(
                    f"{config[network]['infura']['http']}/{token}"
                    if token else config[network][endpoint]["http"]
                ),
                request_kwargs={
                    "timeout": config["timeout"]
                }
            )
        )
        return web3
    elif provider == "websocket":
        web3: Web3 = Web3(WebsocketProvider(
                URI(
                    f"{config[network]['infura']['websocket']}/{token}"
                    if token else config[network][endpoint]["websocket"]
                )
            )
        )
        return web3
    else:
        raise ValueError(f"Invalid Ethereum '{provider}' provider",
                         "choose only 'http' or 'websocket' providers.")


def get_balance(address: str, network: str = config["network"]) -> int:
    """
    Get Ethereum balance.

    :param address: Ethereum address.
    :type address: str
    :param network: Ethereum network, defaults to ``ropsten``.
    :type network: str

    :returns: int -- Ethereum balance (Wei).

    >>> from swap.providers.ethereum.rpc import get_balance
    >>> get_balance("0x70c1eb09363603a3b6391deb2daa6d2561a62f52", "ropsten")
    25800000
    """

    if not is_address(address=address):
        raise AddressError(f"Invalid Ethereum '{address}' address.")

    web3: Web3 = get_web3(network=network)
    balance: int = web3.eth.getBalance(
        to_checksum_address(address=address)
    )
    return balance


def wait_for_transaction_receipt(transaction_hash: str,
                                 network: str = config["network"], timeout: int = config["timeout"]) -> dict:
    """
    Wait for Ethereum transaction receipt.

    :param transaction_hash: Ethereum transaction hash.
    :type transaction_hash: str
    :param network: Ethereum network, defaults to ``ropsten``.
    :type network: str
    :param timeout: Request timeout, default to 60.
    :type timeout: int

    :returns: dict -- Ethereum transaction receipt.

    >>> from swap.providers.ethereum.rpc import wait_for_transaction_receipt
    >>> wait_for_transaction_receipt(transaction_hash="d26220f61ff4207837ee3cf5ab2a551b2476389ae76cf1ccd2005d304bdc308d", network="testnet")
    {'transactionHash': '0xd26220f61ff4207837ee3cf5ab2a551b2476389ae76cf1ccd2005d304bdc308d', 'transactionIndex': 0, 'blockHash': '0xb325934bfb333b5ca77634081cfeaedfa53598771dcfcb482ed3ace789ec5843', 'blockNumber': 1, 'from': '0x69e04fe16c9A6A83076B3c2dc4b4Bc21b5d9A20C', 'to': None, 'gasUsed': 1582730, 'cumulativeGasUsed': 1582730, 'contractAddress': '0xeaEaC81da5E386E8Ca4De1e64d40a10E468A5b40', 'logs': [], 'status': 1, 'logsBloom': '0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'}
    """

    web3: Web3 = get_web3(network=network)
    transaction_dict: dict = web3.eth.wait_for_transaction_receipt(
        transaction_hash=HexBytes(transaction_hash), timeout=timeout
    ).__dict__
    for key, value in transaction_dict.items():
        if isinstance(value, HexBytes):
            transaction_dict[key] = transaction_dict[key].hex()
    return transaction_dict


def get_transaction_receipt(transaction_hash: str, network: str = config["network"]) -> dict:
    """
    Get Ethereum transaction receipt.

    :param transaction_hash: Ethereum transaction hash.
    :type transaction_hash: str
    :param network: Ethereum network, defaults to ``ropsten``.
    :type network: str

    :returns: dict -- Ethereum transaction receipt.

    >>> from swap.providers.ethereum.rpc import get_transaction_receipt
    >>> get_transaction_receipt(transaction_hash="d26220f61ff4207837ee3cf5ab2a551b2476389ae76cf1ccd2005d304bdc308d", network="testnet")
    {'transactionHash': '0xd26220f61ff4207837ee3cf5ab2a551b2476389ae76cf1ccd2005d304bdc308d', 'transactionIndex': 0, 'blockHash': '0xb325934bfb333b5ca77634081cfeaedfa53598771dcfcb482ed3ace789ec5843', 'blockNumber': 1, 'from': '0x69e04fe16c9A6A83076B3c2dc4b4Bc21b5d9A20C', 'to': None, 'gasUsed': 1582730, 'cumulativeGasUsed': 1582730, 'contractAddress': '0xeaEaC81da5E386E8Ca4De1e64d40a10E468A5b40', 'logs': [], 'status': 1, 'logsBloom': '0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'}
    """

    web3: Web3 = get_web3(network=network)
    transaction_dict: dict = web3.eth.get_transaction_receipt(transaction_hash).__dict__
    for key, value in transaction_dict.items():
        if isinstance(value, HexBytes):
            transaction_dict[key] = transaction_dict[key].hex()
    return transaction_dict


def submit_raw(transaction_raw: str, network: str = config["network"]) -> str:
    """
    Submit original Ethereum raw into blockchain.

    :param transaction_raw: Ethereum transaction raw.
    :type transaction_raw: str
    :param network: Ethereum network, defaults to ``ropsten``.
    :type network: str

    :returns: str -- Ethereum submitted transaction hash.

    >>> from swap.providers.ethereum.rpc import submit_raw
    >>> submit_raw(raw="0xf86c02840ee6b280825208943e0a9b2ee8f8341a1aead3e7531d75f1e395f24b8901236efcbcbb340000801ba03084982e4a9dd897d3cc1b2c8cc2d1b106b9d302eb23f6fae7d0e57e53e043f8a0116f13f9ab385f6b53e7821b3335ced924a1ceb88303347cd0af4aa75e6bfb73", network="testnet")
    "0x04b3bfb804f2b3329555c6f3a17a794b3f099b6435a9cf58c78609ed93853907"
    """

    web3: Web3 = get_web3(network=network)
    transaction_hash: HexBytes = web3.eth.send_raw_transaction(transaction_raw)
    return transaction_hash.hex()
