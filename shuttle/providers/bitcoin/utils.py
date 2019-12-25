#!/usr/bin/env python3

from btcpy.structs.script import P2pkhScript, P2shScript
from btcpy.structs.transaction import Sequence
from btcpy.structs.address import Address

import cryptos
import hashlib


# Checking address
def is_address(address, testnet=True):
    if isinstance(address, str):
        if isinstance(testnet, bool):
            return cryptos.Bitcoin(testnet=testnet).is_address(address)
        elif isinstance(testnet, str):
            testnet = True if testnet == "testnet" else False
            return cryptos.Bitcoin(testnet=testnet).is_address(address)
    raise TypeError("Address must be string format!")


# Double SHA256 hash
def double_sha256(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


# Transaction fee calculator
def fee_calculator(tx_input=2, tx_output=4):
    # 576 input 1 output 1
    # 678 input 1 output 2
    # 780 input 1 output 3
    # 882 input 1 output 4

    # 1020 input 2 output 1
    # 1122 input 2 output 2
    # 1224 input 2 output 3
    # 1326 input 2 output 4

    # 444 input
    # 102 output

    tx_input = ((tx_input - 1) * 444) + 576
    tx_output = ((tx_output - 1) * 102)
    return tx_input + tx_output


# Setting expiration to script
def expiration_to_script(expiration):
    if isinstance(expiration, int):
        if expiration <= 16:
            return "OP_%d" % expiration
        else:
            return Sequence(expiration).for_script()
    raise TypeError("Expiration must be integer format!")


# Creating script from address
def script_from_address(address, testnet=True):
    if isinstance(address, str) and cryptos.Bitcoin(testnet=testnet).is_address(address):
        load_address = Address.from_string(address)
        get_type = load_address.get_type()
        if str(get_type) == "p2pkh":
            return P2pkhScript(load_address)
        elif str(get_type) == "p2sh":
            return P2shScript(load_address)
    raise TypeError("Address must be string format!")


# Creating script from address
def address_to_hash(address, testnet=True):
    if isinstance(address, str) and \
            cryptos.Bitcoin(testnet=testnet).is_address(address):
        return Address.from_string(address).hash.hex()

    raise TypeError("Address must be string format!")

