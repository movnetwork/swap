#!/usr/bin/env python3

from binascii import (
    hexlify, unhexlify
)
from typing import Union
from web3 import Web3

from ...exceptions import (
    BalanceError, AddressError, UnitError
)
from ..config import ethereum

# Ethereum configuration
config: dict = ethereum


def is_network(network: str) -> bool:
    """
    Check Ethereum network.

    :param network: Ethereum network.
    :type network: str

    :returns: bool -- Ethereum valid/invalid network.

    >>> from swap.providers.ethereum.utils import is_network
    >>> is_network(network="kovan")
    True
    """

    if not isinstance(network, str):
        raise TypeError(f"Network must be str, not '{type(network)}' type.")

    return network in ["mainnet", "ropsten", "kovan", "rinkeby", "testnet"]


def is_address(address: str) -> bool:
    """
    Check Ethereum address.

    :param address: Ethereum address.
    :type address: str

    :returns: bool -- Ethereum valid/invalid address.

    >>> from swap.providers.ethereum.utils import is_address
    >>> is_address(address="0x1ee11011ae12103a488a82dc33e03f337bc93ba7")
    True
    """

    if not isinstance(address, str):
        raise TypeError(f"Address must be str, not '{type(address)}' type.")

    return Web3.isAddress(address)


def is_checksum_address(address: str) -> bool:
    """
    Check Ethereum checksum address.

    :param address: Ethereum address.
    :type address: str

    :returns: bool -- Ethereum valid/invalid checksum address.

    >>> from swap.providers.ethereum.utils import is_checksum_address
    >>> is_checksum_address(address="0x1ee11011ae12103a488a82dc33e03f337bc93ba7")
    False
    >>> is_checksum_address(address="0x1Ee11011ae12103a488A82DC33e03f337Bc93ba7")
    True
    """

    if not isinstance(address, str):
        raise TypeError(f"Address must be str, not '{type(address)}' type.")

    return Web3.isChecksumAddress(address)


def to_checksum_address(address: str) -> str:
    """
    Change Ethereum address to checksum address.

    :param address: Ethereum address.
    :type address: str

    :returns: str -- Ethereum checksum address.

    >>> from swap.providers.ethereum.utils import to_checksum_address
    >>>  is_checksum_address(address="0x1ee11011ae12103a488a82dc33e03f337bc93ba7")
    "0x1Ee11011ae12103a488A82DC33e03f337Bc93ba7"
    """

    if not is_address(address):
        raise AddressError(f"Invalid Ethereum '{type(address)}' address.")

    return Web3.toChecksumAddress(address)


def submit_transaction_raw(web3, signed):
    try:
        tx_hash = web3.eth.sendRawTransaction(signed)
    except ValueError as value_error:
        if str(value_error).find("sender doesn't have enough funds to send tx") != -1:
            raise BalanceError("insufficient spend balance")
        raise value_error
    return hexlify(tx_hash).decode()


def amount_unit_converter(amount: Union[int, float], unit: str = "Wei2Ether") -> Union[int, float]:
    """
    XinFin amount unit converter.

    :param amount: XinFIn amount.
    :type amount: int, float
    :param unit: XinFIn unit, default to Wei2Ether
    :type unit: str

    :returns: int, float -- XinFin amount.

    >>> from swap.providers.ethereum.utils import amount_unit_converter
    >>> amount_unit_converter(amount=100_000_000, unit="Wei2Ether")
    0.1
    """

    if unit not in ["Ether2Gwei", "Ether2Wei", "Gwei2Ether", "Gwei2Wei", "Wei2Ether", "Wei2Gwei"]:
        raise UnitError(f"Invalid Ethereum '{unit}' unit",
                        "choose only 'Ether2Gwei', 'Ether2Wei', 'Gwei2Ether', 'Gwei2Wei', 'Wei2Ether' or 'Wei2Gwei' units.")

    # Constant values
    Ether, Gwei, Wei = (
        config["units"]["Ether"],
        config["units"]["Gwei"],
        config["units"]["Wei"]
    )

    if unit == "Ether2Gwei":
        return float((amount * Gwei) / Ether)
    elif unit == "Ether2Wei":
        return int((amount * Wei) / Ether)
    elif unit == "Gwei2Ether":
        return float((amount * Ether) / Gwei)
    elif unit == "Gwei2Wei":
        return int((amount * Wei) / Gwei)
    elif unit == "Wei2Ether":
        return float((amount * Ether) / Wei)
    elif unit == "Wei2Gwei":
        return int((amount * Gwei) / Wei)
