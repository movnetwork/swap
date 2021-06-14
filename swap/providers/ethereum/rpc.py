#!/usr/bin/env python3

from web3 import Web3
from web3.providers import (
    HTTPProvider, WebsocketProvider
)
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


def get_balance(address: str, network: str = "ropsten") -> int:
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
