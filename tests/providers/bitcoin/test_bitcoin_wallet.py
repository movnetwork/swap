#!/usr/bin/env python3

from shuttle.providers.bitcoin.wallet import Wallet


def test_from_passphrase():
    passphrase = "meheret tesfaye batu bayou"
    # Initialize bitcoin wallet
    bitcoin_from_passphrase = Wallet(network="testnet") \
        .from_passphrase(passphrase)

    bitcoin_from_private_key = Wallet(network="testnet") \
        .from_private_key("92cbbc5990cb5090326a76feeb321cad01048635afe5756523bbf9f7a75bf38b")

    private_key = "92cbbc5990cb5090326a76feeb321cad01048635afe5756523bbf9f7a75bf38b"
    assert bitcoin_from_private_key.private_key() == private_key == bitcoin_from_passphrase.private_key()

    public_key = "03c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84"
    assert bitcoin_from_private_key.public_key() == public_key

    address = "mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q"
    assert bitcoin_from_private_key.address() == address

    # Initialize bitcoin wallet
    bitcoin_from_passphrase = Wallet(network="testnet")\
        .from_passphrase(passphrase, False)

    private_key = "92cbbc5990cb5090326a76feeb321cad01048635afe5756523bbf9f7a75bf38b"
    assert bitcoin_from_passphrase.private_key() == private_key

    public_key = "04c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84fee63d89a5979801c9659" \
                 "94963c77bfb470dff5afd351a442ebf329f3b2c2835"
    assert bitcoin_from_passphrase.public_key() == public_key

    compressed = "03c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84"
    assert bitcoin_from_passphrase.compressed() == compressed

    uncompressed = "04c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84fee63d89a5979801c96" \
                   "5994963c77bfb470dff5afd351a442ebf329f3b2c2835"
    assert bitcoin_from_passphrase.uncompressed() == uncompressed

    assert bitcoin_from_passphrase.uncompressed() == bitcoin_from_passphrase.public_key()

    address = "mqLyrNDjpENRMZAoDpspH7kR9RtgvhWzYE"
    assert bitcoin_from_passphrase.address() == address

    _hash = "6bce65e58a50b97989930e9a4ff1ac1a77515ef1"
    assert bitcoin_from_passphrase.hash() == _hash

    p2pkh = "76a9146bce65e58a50b97989930e9a4ff1ac1a77515ef188ac"
    assert bitcoin_from_passphrase.p2pkh() == p2pkh

    p2sh = "a914347283eee92ad685909044619adaa70370b2538787"
    assert bitcoin_from_passphrase.p2sh() == p2sh


def test_from_private_key():
    # testing from private keky
    private_key = "92cbbc5990cb5090326a76feeb321cad01048635afe5756523bbf9f7a75bf38b"

    # Initialize bitcoin wallet
    bitcoin_from_private_key = Wallet(network="testnet")\
        .from_private_key(private_key)

    private_key = "92cbbc5990cb5090326a76feeb321cad01048635afe5756523bbf9f7a75bf38b"
    assert bitcoin_from_private_key.private_key() == private_key

    public_key = "03c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84"
    assert bitcoin_from_private_key.public_key() == public_key

    address = "mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q"
    assert bitcoin_from_private_key.address() == address

    # Initialize bitcoin wallet
    bitcoin_from_private_key = Wallet(network="testnet") \
        .from_private_key(private_key, False)

    private_key = "92cbbc5990cb5090326a76feeb321cad01048635afe5756523bbf9f7a75bf38b"
    assert bitcoin_from_private_key.private_key() == private_key

    public_key = "04c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84fee63d89a5979801c9659" \
                 "94963c77bfb470dff5afd351a442ebf329f3b2c2835"
    assert bitcoin_from_private_key.public_key() == public_key

    compressed = "03c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84"
    assert bitcoin_from_private_key.compressed() == compressed

    uncompressed = "04c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84fee63d89a5979801c96" \
                   "5994963c77bfb470dff5afd351a442ebf329f3b2c2835"
    assert bitcoin_from_private_key.uncompressed() == uncompressed

    assert bitcoin_from_private_key.uncompressed() == bitcoin_from_private_key.public_key()

    address = "mqLyrNDjpENRMZAoDpspH7kR9RtgvhWzYE"
    assert bitcoin_from_private_key.address() == address

    _hash = "6bce65e58a50b97989930e9a4ff1ac1a77515ef1"
    assert bitcoin_from_private_key.hash() == _hash

    p2pkh = "76a9146bce65e58a50b97989930e9a4ff1ac1a77515ef188ac"
    assert bitcoin_from_private_key.p2pkh() == p2pkh

    p2sh = "a914347283eee92ad685909044619adaa70370b2538787"
    assert bitcoin_from_private_key.p2sh() == p2sh


def test_from_address():
    # testing from address
    address = "mqLyrNDjpENRMZAoDpspH7kR9RtgvhWzYE"

    # Initialize bitcoin wallet
    bitcoin_from_address = Wallet(network="testnet").from_address(address)

    assert bitcoin_from_address.address() == address

    _hash = "6bce65e58a50b97989930e9a4ff1ac1a77515ef1"
    assert bitcoin_from_address.hash() == _hash

    p2pkh = "76a9146bce65e58a50b97989930e9a4ff1ac1a77515ef188ac"
    assert bitcoin_from_address.p2pkh() == p2pkh

    p2sh = "a914347283eee92ad685909044619adaa70370b2538787"
    assert bitcoin_from_address.p2sh() == p2sh


def test_bitcoin_wallet_tools():
    wallet = Wallet(network="testnet")
    private_key = "92cbbc5990cb5090326a76feeb321cad01048635afe5756523bbf9f7a75bf38b"
    public_key = wallet.public_key(private_key=private_key)
    assert public_key == "03c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84"
    public_key = "04c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84fee63d89a5979801c96" \
                 "5994963c77bfb470dff5afd351a442ebf329f3b2c2835"

    compressed = wallet.compressed(public_key=public_key)
    assert compressed == "03c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84"
    uncompressed = wallet.uncompressed(public_key=public_key)
    assert uncompressed == public_key
    address = wallet.address(public_key=uncompressed)
    assert address == "mqLyrNDjpENRMZAoDpspH7kR9RtgvhWzYE"
    _hash = wallet.hash(public_key=uncompressed)
    assert _hash == "6bce65e58a50b97989930e9a4ff1ac1a77515ef1"
    p2pkh = wallet.p2pkh(address=address)
    assert p2pkh == "76a9146bce65e58a50b97989930e9a4ff1ac1a77515ef188ac"
    p2sh = wallet.p2sh(address=address)
    assert p2sh == "a914347283eee92ad685909044619adaa70370b2538787"
    balance = wallet.balance(address=address, network="testnet")
    assert isinstance(balance, int)
    unspent = wallet.unspent(address=address, network="testnet", limit=1)
    assert isinstance(unspent, list)
