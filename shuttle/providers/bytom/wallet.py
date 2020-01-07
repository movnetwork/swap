#!/usr/bin/env python3

from btmhdw import BytomHDWallet

from .rpc import get_balance, account_create


# Bytom Wallet.
class Wallet:

    # PyShuttle Bytom (BTM) wallet init.
    def __init__(self, network="testnet", account=1, change=0, address=1):
        # Bytom network.
        if network not in ["mainnet", "testnet"]:
            raise Exception("Network initialization error.")
        self.network = network
        # Bytom wallet initialization.
        self.bytom = BytomHDWallet()

        # Derivation
        self._account = account
        self._change = change
        self._address = address

    # Bytom wallet from mnemonic
    def from_mnemonic(self, mnemonic):
        self.bytom = self.bytom.master_key_from_mnemonic(mnemonic=mnemonic)
        self.derivation()
        return self

    # Bytom wallet from seed
    def from_seed(self, seed):
        self.bytom = self.bytom.master_key_from_seed(seed=seed)
        self.derivation()
        return self

    # Bytom wallet from entropy
    def from_entropy(self, entropy):
        self.bytom = self.bytom.master_key_from_entropy(entropy=entropy)
        self.derivation()
        return self

    # Bytom wallet from xprivate key
    def from_xprivate_key(self, xprivate):
        self.bytom = self.bytom.master_key_from_xprivate(xprivate=xprivate)
        self.derivation()
        return self

    # Path derivation
    def derivation(self):
        self.bytom.from_index(44)
        self.bytom.from_index(153)
        self.bytom.from_index(self._account)
        self.bytom.from_index(self._change)
        self.bytom.from_index(self._address)
        return self

    # Getting seed
    def seed(self):
        return self.bytom.seed

    # Getting path derivation indexes
    def indexes(self):
        return self.bytom.get_indexes()

    # Getting xprivate key
    def xprivate_key(self):
        return self.bytom.xprivate_key()

    # Getting xpublic key
    def xpublic_key(self):
        return self.bytom.xpublic_key()

    # Getting expand xprivate key
    def expand_xprivate_key(self):
        return self.bytom.expand_xprivate_key()

    # Getting public key
    def public_key(self):
        return self.bytom.public_key()

    # Getting control program
    def program(self):
        return self.bytom.program()

    # Getting address
    def address(self):
        return self.bytom.address(network=self.network)

    # Getting guid from blockcenter
    def guid(self):
        return account_create(
            xpublic_key=self.xpublic_key(), network=self.network)["guid"]

    # Getting balance
    def balance(self):
        return get_balance(self.bytom.address(
            network=self.network), self. network)
