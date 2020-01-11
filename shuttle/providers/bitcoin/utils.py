#!/usr/bin/env python3

from btcpy.structs.script import P2pkhScript, P2shScript
from btcpy.structs.transaction import Sequence
from btcpy.structs.address import Address

import cryptos
import hashlib

from ...utils.exceptions import AddressError, NetworkError


# Checking address
def is_address(address, network="testnet"):
    if isinstance(address, str):
        if network == "testnet":
            return cryptos.Bitcoin(testnet=True).is_address(address)
        elif network == "mainnet":
            return cryptos.Bitcoin(testnet=False).is_address(address)
        else:
            raise NetworkError("Invalid %s network" % network, "Only testnet or mainnet.")
    raise TypeError("Address must be string format!")


# Double SHA256 hash
def double_sha256(data):
    if isinstance(data, bytes):
        return hashlib.sha256(hashlib.sha256(data).digest()).digest()
    raise TypeError("Data must be bytes format!")


# Transaction fee calculator
def fee_calculator(transaction_input=1, transaction_output=1):
    # 444 input 102 output
    transaction_input = ((transaction_input - 1) * 444) + 576
    transaction_output = ((transaction_output - 1) * 102)
    return transaction_input + transaction_output


# Setting expiration to script
def expiration_to_script(sequence):
    if isinstance(sequence, int):
        if sequence <= 16:
            return "OP_%d" % sequence
        else:
            return Sequence(sequence).for_script()
    raise TypeError("Sequence must be integer format!")


# Creating script from address
def script_from_address(address, network="testnet"):
    if not is_address(address, network):
        raise AddressError("Invalid %s %s address!" % (network, address))
    load_address = Address.from_string(address)
    get_type = load_address.get_type()
    if str(get_type) == "p2pkh":
        return P2pkhScript(load_address)
    elif str(get_type) == "p2sh":
        return P2shScript(load_address)


# Creating script from address
def address_to_hash(address, network="testnet"):
    if not is_address(address, network):
        raise AddressError("Invalid %s %s address!" % (network, address))
    return Address.from_string(address).hash.hex()
