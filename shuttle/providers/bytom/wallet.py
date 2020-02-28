#!/usr/bin/env python3

from btmhdw import BytomHDWallet

from .rpc import get_balance, account_create


# Bytom Wallet.
class Wallet:
    """
    Bytom Wallet class.

    :param network: bytom network, defaults to testnet.
    :type network: str
    :param account: bytom derivation account, defaults to 1.
    :type account: int
    :param change: bytom derivation change, defaults to False.
    :type change: bool
    :param address: bytom derivation address, defaults to 1.
    :type address: int
    :param path: bytom derivation path, defaults to None.
    :type path: str
    :param indexes: bytom derivation indexes, defaults to None.
    :type indexes: list
    :returns:  Wallet -- bytom wallet instance.

    .. note::
        Bytom has only three networks, ``mainnet``, ``solonet`` and ``testnet``.
    """

    # PyShuttle Bytom (BTM) wallet init.
    def __init__(self, network="testnet",
                 account=1, change=False, address=1, path=None, indexes=None):
        # Bytom network.
        if network not in ["mainnet", "solonet", "testnet"]:
            raise Exception("Network initialization error.")
        self.network = network
        # Bytom wallet initialization.
        self.bytom = None

        # Derivation
        self._account = account
        if not isinstance(change, bool):
            raise TypeError("derivation change must be boolean format.")
        self._change = 1 if change else 0
        self.__address = address
        # Derivation path
        self._path = path
        # Derivation indexes
        self._indexes = indexes

        # Wallet info's
        self._public_key = None
        self._private_key = None
        self._xpublic_key = None
        self._program = None
        self._address = None
        # Blockcenter GUID
        self._guid = None

    # Bytom wallet from mnemonic
    def from_mnemonic(self, mnemonic):
        """
        Initiate bytom wallet from mnemonic.

        :param mnemonic: Bytom wallet mnemonic.
        :type mnemonic: str.
        :returns:  Wallet -- bytom wallet instance.

        >>> from shuttle.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        <shuttle.providers.bytom.wallet.Wallet object at 0x040DA268>
        """

        # Bytom wallet initialization.
        self.bytom = BytomHDWallet()\
            .master_key_from_mnemonic(mnemonic=mnemonic)
        self.derivation()
        self._xpublic_key = self.bytom.xpublic_key()
        self._private_key = self.bytom.private_key()
        self._public_key = self.bytom.public_key()
        self._program = self.bytom.program()
        self._address = self.bytom.address(network=self.network)
        return self

    # Bytom wallet from seed
    def from_seed(self, seed):
        """
        Initiate bytom wallet from seed.

        :param seed: Bytom wallet seed.
        :type seed: str.
        :returns:  Wallet -- bytom wallet instance.

        >>> from shuttle.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_seed("baff3e1fe60e1f2a2d840d304acc98d1818140c79354a353b400fb019bfb256bc392d7aa9047adff1f14bce0342e14605c6743a6c08e02150588375eb2eb7d49")
        <shuttle.providers.bytom.wallet.Wallet object at 0x040DA268>
        """

        # Bytom wallet initialization.
        self.bytom = BytomHDWallet()\
            .master_key_from_seed(seed=seed)
        self.derivation()
        self._xpublic_key = self.bytom.xpublic_key()
        self._private_key = self.bytom.private_key()
        self._public_key = self.bytom.public_key()
        self._program = self.bytom.program()
        self._address = self.bytom.address(network=self.network)
        return self

    # Bytom wallet from entropy
    def from_entropy(self, entropy):
        """
        Initiate bytom wallet from entropy.

        :param entropy: Bytom wallet entropy.
        :type entropy: str.
        :returns:  Wallet -- bytom wallet instance.

        >>> from shuttle.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("...")
        <shuttle.providers.bytom.wallet.Wallet object at 0x040DA268>
        """

        # Bytom wallet initialization.
        self.bytom = BytomHDWallet()\
            .master_key_from_entropy(entropy=entropy)
        self.derivation()
        self._xpublic_key = self.bytom.xpublic_key()
        self._private_key = self.bytom.private_key()
        self._public_key = self.bytom.public_key()
        self._program = self.bytom.program()
        self._address = self.bytom.address(network=self.network)
        return self

    # Bytom wallet from xprivate key
    def from_xprivate_key(self, xprivate):
        """
        Initiate bytom wallet from xprivate key.

        :param xprivate: Bytom wallet xprivate key.
        :type xprivate: str.
        :returns:  Wallet -- bytom wallet instance.

        >>> from shuttle.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_xprivate_key("205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
        <shuttle.providers.bytom.wallet.Wallet object at 0x040DA268>
        """

        # Bytom wallet initialization.
        self.bytom = BytomHDWallet()\
            .master_key_from_xprivate(xprivate=xprivate)
        self.derivation()
        self._xpublic_key = self.bytom.xpublic_key()
        self._private_key = self.bytom.private_key()
        self._public_key = self.bytom.public_key()
        self._program = self.bytom.program()
        self._address = self.bytom.address(network=self.network)
        return self

    # Bytom wallet from xpublic key
    def from_xpublic_key(self, xpublic):
        """
        Initiate bytom wallet from xpublic key.

        :param xpublic: Bytom wallet xpublic key.
        :type xpublic: str.
        :returns:  Wallet -- bytom wallet instance.

        >>> from shuttle.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_xpublic_key("16476b7fd68ca2acd92cfc38fa353e75d6103f828276f44d587e660a6bd7a5c5ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
        <shuttle.providers.bytom.wallet.Wallet object at 0x040DA268>
        """

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
        """
        Initiate bytom wallet from public key.

        :param public: Bytom wallet public key.
        :type public: str.
        :returns:  Wallet -- bytom wallet instance.

        >>> from shuttle.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_public_key("91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2")
        <shuttle.providers.bytom.wallet.Wallet object at 0x040DA268>
        """

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
        """
        Get bytom wallet derivation path.

        :return: str -- bytom derivation path.

        >>> from shuttle.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet", change=True, address=3)
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.path()
        "m/44/153/1/1/3"
        """

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
        """
        Get bytom wallet seed.

        :return: str -- bytom seed.

        >>> from shuttle.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.seed()
        "baff3e1fe60e1f2a2d840d304acc98d1818140c79354a353b400fb019bfb256bc392d7aa9047adff1f14bce0342e14605c6743a6c08e02150588375eb2eb7d49"
        """

        if self.bytom is None:
            raise Exception("You can't get seed from xpublic | public key")
        return self.bytom.seed

    # Getting path derivation indexes
    def indexes(self):
        """
        Get bytom wallet derivation indexes.

        :return: list -- bytom derivation indexes.

        >>> from shuttle.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.indexes()
        ['2c000000', '99000000', '01000000', '00000000', '01000000']
        """

        return self.bytom.get_indexes()

    # Getting xprivate key
    def xprivate_key(self):
        """
        Get bytom wallet xprivate key.

        :return: str -- bytom xprivate key.

        >>> from shuttle.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.xprivate_key()
        "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"
        """

        if self.bytom is None:
            raise Exception("you can't get xprivate key from xpublic | public key")
        return self.bytom.xprivate_key()

    # Getting xpublic key
    def xpublic_key(self):
        """
        Get bytom wallet xpublic key.

        :return: str -- bytom xpublic key.

        >>> from shuttle.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.xpublic_key()
        "16476b7fd68ca2acd92cfc38fa353e75d6103f828276f44d587e660a6bd7a5c5ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"
        """

        if self._xpublic_key is None:
            raise Exception("you can't get xpublic key from public key")
        return self._xpublic_key

    # Getting expand xprivate key
    def expand_xprivate_key(self):
        """
        Get bytom wallet expand xprivate key.

        :return: str -- bytom expand xprivate key.

        >>> from shuttle.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.expand_xprivate_key()
        "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee5102416c643cfb46ab1ae5a524c8b4aaa002eb771d0d9cfc7490c0c3a8177e053e"
        """

        if self.bytom is None:
            raise Exception("you can't get expand xprivate key from xpublic | public key")
        return self.bytom.expand_xprivate_key()

    # Getting private key
    def private_key(self):
        """
        Get bytom wallet private key.

        :return: str -- bytom private key.

        >>> from shuttle.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.private_key()
        "e07af52746e7cccd0a7d1fba6651a6f474bada481f34b1c5bab5e2d71e36ee515803ee0a6682fb19e279d8f4f7acebee8abd0fc74771c71565f9a9643fd77141"
        """

        return self._private_key

    # Getting public key
    def public_key(self):
        """
        Get bytom wallet public key.

        :return: str -- bytom public key.

        >>> from shuttle.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.public_key()
        "e07af52746e7cccd0a7d1fba6651a6f474bada481f34b1c5bab5e2d71e36ee515803ee0a6682fb19e279d8f4f7acebee8abd0fc74771c71565f9a9643fd77141"
        """

        return self._public_key

    # Getting control program
    def program(self):
        """
        Get bytom wallet control program.

        :return: str -- bytom control program.

        >>> from shuttle.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.program()
        "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a"
        """

        return self._program

    # Getting address
    def address(self):
        """
        Get bytom wallet address.

        :return: str -- bytom address.

        >>> from shuttle.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.address()
        "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7"
        """

        return self._address

    # Getting guid from blockcenter
    def guid(self):
        """
        Get bytom wallet blockcenter guid.

        :return: str -- bytom blockcenter guid.

        >>> from shuttle.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.guid()
        "f0ed6ddd-9d6b-49fd-8866-a52d1083a13b"
        """

        if self._guid is None:
            self._guid = account_create(
                xpublic_key=self.xpublic_key(), network=self.network)["guid"]
        return self._guid

    # Getting balance
    def balance(self):
        """
        Get bytom wallet balance.

        :return: int -- bytom balance.

        >>> from shuttle.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> wallet.balance()
        2450000000
        """

        return get_balance(address=self.address(), network=self.network)
