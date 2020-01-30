#!/usr/bin/env python3

from btcpy.structs.crypto import PublicKey, PrivateKey
from btcpy.structs.address import Address
from btcpy.structs.script import P2pkhScript, P2shScript
from cryptos import Bitcoin

import hashlib

from .utils import is_address
from .rpc import get_balance, get_unspent_transactions


# Bitcoin Wallet.
class Wallet:

    # PyShuttle Bitcoin (BTC) wallet init.
    def __init__(self, network="testnet"):
        # Bitcoin network.
        self.network = network
        self.testnet = True if network == "testnet" else False
        # Bitcoin wallet initialization.
        self.bitcoin = Bitcoin(testnet=self.testnet)

        # Main wallet init.
        self._private_key, self._public_key, self._address = None, None, None

    def from_private_key(self, private_key):
        self._private_key = PrivateKey.unhexlify(private_key)
        self._public_key = PublicKey.unhexlify(
            self.bitcoin.privtopub(self._private_key.hexlify()))
        self._address = self._public_key.to_address(mainnet=(not self.testnet))
        return self

    def from_passphrase(self, passphrase):
        private_key = hashlib.sha256(passphrase).hexdigest()
        self._private_key = PrivateKey.unhexlify(private_key)
        self._public_key = PublicKey.unhexlify(
            self.bitcoin.privtopub(self._private_key.hexlify()))
        self._address = self._public_key.to_address(mainnet=(not self.testnet))
        return self

    def from_mnemonic(self, mnemonic):
        private_key = hashlib.sha256(mnemonic).hexdigest()
        self._private_key = PrivateKey.unhexlify(private_key)
        self._public_key = PublicKey.unhexlify(
            self.bitcoin.privtopub(self._private_key.hexlify()))
        self._address = self._public_key.to_address(mainnet=(not self.testnet))
        return self

    def from_address(self, address):
        self._address = Address.from_string(address)
        return self

    # Bitcoin main private key.
    def private_key(self):
        return self._private_key.hexlify()

    # Bitcoin main public key.
    def public_key(self, private_key=None):
        if private_key is None:
            return self._public_key.hexlify()
        return PublicKey.unhexlify(private_key).hexlify()

    # Compressed public key.
    def compressed(self, public_key=None):
        if public_key is None:
            return self._public_key.compressed.hex()
        return PublicKey.unhexlify(public_key).compressed.hex()

    # Uncompressed public key.
    def uncompressed(self, public_key=None):
        if public_key is None:
            return self._public_key.uncompressed.hex()
        return PublicKey.unhexlify(public_key).uncompressed.hex()

    # Bitcoin main _address.
    def address(self, public_key=None):
        if public_key is None:
            return str(self._address)
        return PublicKey.unhexlify(public_key)\
            .to__address(mainnet=(not self.testnet))

    # Bitcoin main _address hash.
    def hash(self, public_key=None):
        if public_key is None:
            return self._address.hash.hex()
        return PublicKey.unhexlify(public_key)\
            .to__address(mainnet=(not self.testnet)).hash.hex()

    # Bitcoin public to public key hash script.
    def p2pkh(self, address=None):
        if address is None:
            return P2pkhScript(self._address).hexlify()
        assert is_address(address, self.testnet), "Invalid %s _address!" % self.network
        address = Address.from_string(address)
        return P2pkhScript(address).hexlify()

    # Bitcoin public to script hash script.
    def p2sh(self, address=None):
        if address is None:
            return P2shScript(P2pkhScript(self._address)).hexlify()
        assert is_address(address, self.network), "Invalid %s _address!" % self.network
        address = Address.from_string(address)
        return P2shScript(P2pkhScript(address)).hexlify()

    # Bitcoin balance
    def balance(self, address=None, network="testnet"):
        if address is None:
            return get_balance(str(self._address), self.network)
        return get_balance(address, network)

    def unspent(self, address=None, network="testnet", limit=15):
        if address is None:
            address = str(self._address)
            network = str(self.network)
        unspent = list()
        assert is_address(address, network), "Invalid %s address!" % network
        unspent_transactions = get_unspent_transactions(
            address, network, limit=limit)
        for index, unspent_transaction in enumerate(unspent_transactions):
            unspent.append(dict(
                index=index,
                hash=unspent_transaction["tx_hash"],
                output_index=unspent_transaction["tx_output_n"],
                amount=unspent_transaction["value"],
                script=unspent_transaction["script"]
            ))
        return unspent
