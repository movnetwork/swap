from btmhdw import BytomHDWallet

from .rpc import get_balance


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

        # Path derivation
        self.bytom.fromIndex(44)
        self.bytom.fromIndex(153)
        self.bytom.fromIndex(account)
        self.bytom.fromIndex(change)
        self.bytom.fromIndex(address)

        # Main wallet init.
        self._xprivate_key, self._xpublic_key, self._address = None, None, None

    def from_mnemonic(self, mnemonic):
        self.bytom.masterKeyFromMnemonic(mnemonic=mnemonic)
        return self

    def from_seed(self, seed):
        self.bytom.masterKeyFromSeed(seed=seed)
        return self

    def from_entropy(self, entropy):
        self.bytom.masterKeyFromEntropy(entropy=entropy)
        return self

    def from_xprivate(self, xprivate):
        self.bytom.masterKeyFromXPrivate(xprivate=xprivate)
        return self

    def seed(self):
        return self.bytom.seed.hex()

    def indexes(self):
        return self.bytom.getIndexes()

    def xprivate_key(self):
        return self.bytom.xprivateKey()

    def xpublic_key(self):
        return self.bytom.xpublicKey()

    def expand_xprivate_key(self):
        return self.bytom.expandPrivateKey()

    def public_key(self):
        return self.bytom.publicKey()

    def program(self):
        return self.bytom.program()

    def address(self):
        return self.bytom.address(network=self.network)

    def balance(self):
        return get_balance(
            self.bytom.address(network=self.network),self. network)
