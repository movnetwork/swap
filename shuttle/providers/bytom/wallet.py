#!/usr/bin/env python3

from btmhdw import BytomHDWallet

from .rpc import get_balance, account_create


# Bytom Wallet.
class Wallet:

    # PyShuttle Bytom (BTM) wallet init.
    def __init__(self, network="testnet",
                 account=1, change=0, address=1, path=None, indexes=None):
        # Bytom network.
        if network not in ["mainnet", "solonet", "testnet"]:
            raise Exception("Network initialization error.")
        self.network = network
        # Bytom wallet initialization.
        self.bytom = None

        # Derivation
        self._account = account
        self._change = change
        self.__address = address
        # Derivation path
        self._path = path
        # Derivation indexes
        self._indexes = indexes

        # Wallet info's
        self._public_key = None
        self._xpublic_key = None
        self._program = None
        self._address = None

    # Bytom wallet from mnemonic
    def from_mnemonic(self, mnemonic):
        # Bytom wallet initialization.
        self.bytom = BytomHDWallet()\
            .master_key_from_mnemonic(mnemonic=mnemonic)
        self.derivation()
        self._xpublic_key = self.bytom.xpublic_key()
        self._public_key = self.bytom.public_key()
        self._program = self.bytom.program()
        self._address = self.bytom.address(network=self.network)
        return self

    # Bytom wallet from seed
    def from_seed(self, seed):
        # Bytom wallet initialization.
        self.bytom = BytomHDWallet()\
            .master_key_from_seed(seed=seed)
        self.derivation()
        self._xpublic_key = self.bytom.xpublic_key()
        self._public_key = self.bytom.public_key()
        self._program = self.bytom.program()
        self._address = self.bytom.address(network=self.network)
        return self

    # Bytom wallet from entropy
    def from_entropy(self, entropy):
        # Bytom wallet initialization.
        self.bytom = BytomHDWallet()\
            .master_key_from_entropy(entropy=entropy)
        self.derivation()
        self._xpublic_key = self.bytom.xpublic_key()
        self._public_key = self.bytom.public_key()
        self._program = self.bytom.program()
        self._address = self.bytom.address(network=self.network)
        return self

    # Bytom wallet from xprivate key
    def from_xprivate_key(self, xprivate):
        # Bytom wallet initialization.
        self.bytom = BytomHDWallet()\
            .master_key_from_xprivate(xprivate=xprivate)
        self.derivation()
        self._xpublic_key = self.bytom.xpublic_key()
        self._public_key = self.bytom.public_key()
        self._program = self.bytom.program()
        self._address = self.bytom.address(network=self.network)
        return self

    # Bytom wallet from xpublic key
    def from_xpublic_key(self, xpublic):
        # Bytom wallet initialization.
        bytom = BytomHDWallet()
        self._xpublic_key = xpublic
        self._public_key = bytom.public_key(xpublic=self._xpublic_key, path=self.path())
        self._program = bytom.program(public=self._public_key)
        self._address = bytom.address(
            program=self._program, network=self.network)
        return self

    # Bytom wallet from public key
    def from_public_key(self, public):
        # Bytom wallet initialization.
        bytom = BytomHDWallet()
        self._public_key = public
        self._program = bytom.program(
            public=self._public_key)
        self._address = bytom.address(
            program=self._program, network=self.network)
        return self

    # Path derivation
    def derivation(self):
        if self._path:
            self.bytom.from_path(self._path)
        elif self._indexes:
            self.bytom.from_indexes(self._indexes)
        else:
            self.bytom.from_index(44)
            self.bytom.from_index(153)
            self.bytom.from_index(self._account)
            self.bytom.from_index(self._change)
            self.bytom.from_index(self.__address)
        return self

    # Getting path
    def path(self):
        if self._xpublic_key is None:
            raise Exception("You can't get path from public key")
        if self.bytom is not None:
            return self.bytom.get_path()
        else:
            if self._path:
                return self._path
            elif self._indexes:
                return BytomHDWallet()\
                    .get_path(indexes=self._indexes)
            else:
                return "m/44/153/%d/%d/%d" % \
                       (self._account, self._change, self.__address)

    # Getting seed
    def seed(self):
        if self.bytom is None:
            raise Exception("You can't get seed from xpublic | public key")
        return self.bytom.seed

    # Getting path derivation indexes
    def indexes(self):
        return self.bytom.get_indexes()

    # Getting xprivate key
    def xprivate_key(self):
        if self.bytom is None:
            raise Exception("You can't get xprivate key from xpublic | public key")
        return self.bytom.xprivate_key()

    # Getting xpublic key
    def xpublic_key(self):
        if self._xpublic_key is None:
            raise Exception("You can't get xpublic key from public key")
        return self._xpublic_key

    # Getting expand xprivate key
    def expand_xprivate_key(self):
        if self.bytom is None:
            raise Exception("You can't get expand xprivate key from xpublic | public key")
        return self.bytom.expand_xprivate_key()

    # Getting public key
    def public_key(self):
        return self._public_key

    # Getting control program
    def program(self):
        return self._program

    # Getting address
    def address(self):
        return self._address

    # Getting guid from blockcenter
    def guid(self):
        return account_create(
            xpublic_key=self.xpublic_key(), network=self.network)["guid"]

    # Getting balance
    def balance(self):
        return get_balance(address=self.address(), network=self. network)
