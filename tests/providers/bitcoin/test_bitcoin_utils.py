#!/usr/bin/env python3

from shuttle.providers.bitcoin.utils import sha256, double_sha256, \
    expiration_to_script, script_from_address, address_to_hash, is_address


def test_bitcoin_utils():

    assert sha256("meherett".encode()).hex() == \
           "d4f5c55a45c004660b95ec833bb24569eba1559f214e90efa6e8d0b3afa14394"

    assert double_sha256("meherett".encode()).hex() == \
           "2803bf9ed1e5874825350b1b0753a96c00a99236b686bde337404453b11d3288"

    assert expiration_to_script(7) == "OP_7"

    assert str(script_from_address("2N3NKQpymf1KunR4W8BpZjs8za5La5pV5hF", "testnet")) == \
           "OP_HASH160 6f08b254e4c58dc65f6f399c3be7177b901f4a66 OP_EQUAL"

    assert address_to_hash("mrmtGq2HMmqAogSsGDjCtXUpxrb7rHThFH") == \
           "7b7c4431a43b612a72f8229935c469f1f6903658"

    assert is_address("3P14159f73E4gFr7JterCCQh9QjiTjiZrG", "mainnet")
