#!/usr/bin/env python3

from pybytom.wallet import Wallet as HDWallet
from pybytom.rpc import account_create
from typing import (
    Optional, List
)

from ...utils import is_mnemonic
from ...exceptions import NetworkError
from ..config import vapor
from .rpc import (
    get_balance, get_utxos
)

# Vapor config
config: dict = vapor()
# Default path and indexes derivation
DEFAULT_PATH: str = config["path"]
DEFAULT_INDEXES: List[str] = config["indexes"]
DEFAULT_BIP44: str = config["BIP44"]


class Wallet(HDWallet):
    """
    Vapor Wallet class.

    :param network: Vapor network, defaults to mainnet.
    :type network: str

    :returns: Wallet -- Vapor wallet instance.

    .. note::
        Vapor has only two networks, ``mainnet``, ``solonet`` and ``testnet``.
    """

    def __init__(self, network: str = config["network"]):

        self._public_key: Optional[str] = None

        if network == "mainnet":
            self._network: str = "mainnet"
            self._hdwallet: HDWallet = HDWallet(network=self._network)
        elif network == "solonet":
            self._network: str = "solonet"
            self._hdwallet: HDWallet = HDWallet(network=self._network)
        elif network == "testnet":
            self._network: str = "testnet"
            self._hdwallet: HDWallet = HDWallet(network=self._network)
        else:
            raise NetworkError(f"Invalid '{network}' network",
                               "choose only 'mainnet', 'solonet' or 'testnet' networks.")
        super().__init__(network=self._network)

    def from_entropy(self, entropy: str, passphrase: Optional[str] = None, language: str = "english") -> "Wallet":
        """
        Initiate Vapor wallet from entropy.

        :param entropy: Vapor wallet entropy.
        :type entropy: str
        :param passphrase: Vapor wallet passphrase, default to None.
        :type passphrase: str
        :param language: Vapor wallet language, default to english.
        :type language: str

        :returns: Wallet -- Vapor wallet instance.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        <swap.providers.vapor.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_entropy(entropy, passphrase, language)
        return self

    def from_mnemonic(self, mnemonic: str, passphrase: Optional[str] = None,
                      language: Optional[str] = None) -> "Wallet":
        """
        Initialize Vapor wallet from mnemonic.

        :param mnemonic: Vapor wallet mnemonic.
        :type mnemonic: str
        :param passphrase: Vapor wallet passphrase, default to None.
        :type passphrase: str
        :param language: Vapor wallet language, default to english.
        :type language: str

        :returns: Wallet -- Vapor wallet class instance.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        <swap.providers.vapor.wallet.Wallet object at 0x040DA268>
        """

        # Check parameter instances
        if not is_mnemonic(mnemonic=mnemonic, language=language):
            raise ValueError("Invalid Mnemonic words.")

        self._hdwallet.from_mnemonic(mnemonic, passphrase, language)
        return self

    def from_seed(self, seed: str) -> "Wallet":
        """
        Initialize Vapor wallet from seed.

        :param seed: Vapor wallet seed.
        :type seed: str

        :returns: Wallet -- Vapor wallet class instance.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_seed("baff3e1fe60e1f2a2d840d304acc98d1818140c79354a353b400fb019bfb256bc392d7aa9047adff1f14bce0342e14605c6743a6c08e02150588375eb2eb7d49")
        <swap.providers.vapor.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_seed(seed)
        return self

    def from_xprivate_key(self, xprivate_key: str) -> "Wallet":
        """
        Initiate Vapor wallet from xprivate key.

        :param xprivate_key: Vapor wallet xprivate key.
        :type xprivate_key: str

        :returns: Wallet -- Vapor wallet instance.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_xprivate_key("205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
        <swap.providers.vapor.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_xprivate_key(xprivate_key)
        return self

    def from_private_key(self, private_key: str) -> "Wallet":
        """
        Initialize Vapor wallet from private key.

        :param private_key: Vapor private key.
        :type private_key: str

        :returns: Wallet -- Vapor wallet instance.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_private_key("e07af52746e7cccd0a7d1fba6651a6f474bada481f34b1c5bab5e2d71e36ee515803ee0a6682fb19e279d8f4f7acebee8abd0fc74771c71565f9a9643fd77141")
        <swap.providers.vapor.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_private_key(private_key)
        return self

    def from_path(self, path: str) -> "Wallet":
        """
        Drive Vapor wallet from path.

        :param path: Vapor wallet path.
        :type path: str

        :returns: Wallet -- Vapor wallet instance.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44/153/1/0/1")
        <swap.providers.vapor.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_path(path)
        return self

    def from_indexes(self, indexes: List[str]) -> "Wallet":
        """
        Drive Vapor wallet from indexes.

        :param indexes: Vapor derivation indexes.
        :type indexes: list

        :returns: Wallet -- Vapor wallet class instance.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_xprivate_key("205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
        >>> wallet.from_indexes(["2c000000", "99000000", "01000000", "00000000", "01000000"])
        <swap.providers.vapor.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_indexes(indexes)
        return self

    def from_index(self, index: int, harden: bool = False) -> "Wallet":
        """
        Drive Vapor wallet from index.

        :param index: Vapor wallet index.
        :type index: int
        :param harden: Use harden, default to False.
        :type harden: bool

        :returns: Wallet -- Vapor wallet instance.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_index(44)
        >>> wallet.from_index(153)
        >>> wallet.from_index(1)
        >>> wallet.from_index(0)
        >>> wallet.from_index(1)
        <swap.providers.vapor.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_index(index, harden)
        return self

    def clean_derivation(self) -> "Wallet":
        """
        Clean derivation Vapor wallet.

        :returns: Wallet -- Vapor wallet instance.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44/153/1/0/1")
        >>> wallet.indexes()
        ["2c000000", "99000000", "01000000", "00000000", "01000000"]
        >>> wallet.path()
        "m/44/153/1/0/1"
        >>> wallet.clean_derivation()
        >>> wallet.indexes()
        []
        >>> wallet.path()
        None
        """

        self._hdwallet.clean_derivation()
        return self

    def strength(self) -> Optional[int]:
        """
        Get Vapor wallet strength.

        :return: int -- Vapor wallet strength.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.strength()
        128
        """

        return self._hdwallet.strength()

    def entropy(self) -> Optional[str]:
        """
        Get Vapor wallet entropy.

        :return: str -- Vapor wallet entropy.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.entropy()
        "72fee73846f2d1a5807dc8c953bf79f1"
        """

        return self._hdwallet.entropy()

    def mnemonic(self) -> Optional[str]:
        """
        Get Vapor wallet mnemonic.

        :return: str -- Vapor wallet mnemonic.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.mnemonic()
        "indicate warm sock mistake code spot acid ribbon sing over taxi toast"
        """

        return self._hdwallet.mnemonic()

    def passphrase(self) -> Optional[str]:
        """
        Get Vapor wallet passphrase.

        :return: str -- Vapor wallet passphrase.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1", passphrase="meherett")
        >>> wallet.passphrase()
        "meherett"
        """

        return self._hdwallet.passphrase()

    def language(self) -> Optional[str]:
        """
        Get Vapor wallet language.

        :return: str -- Vapor wallet language.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.language()
        "english"
        """

        return self._hdwallet.language()

    def seed(self) -> Optional[str]:
        """
        Get Vapor wallet seed.

        :return: str -- Vapor wallet seed.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.seed()
        "baff3e1fe60e1f2a2d840d304acc98d1818140c79354a353b400fb019bfb256bc392d7aa9047adff1f14bce0342e14605c6743a6c08e02150588375eb2eb7d49"
        """

        return self._hdwallet.seed()

    def path(self) -> Optional[str]:
        """
        Get Vapor wallet derivation path.

        :return: str -- Vapor derivation path.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet", change=True, address=3)
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44/153/1/0/1")
        >>> wallet.path()
        "m/44/153/1/0/1"
        """

        return self._hdwallet.path()

    def indexes(self) -> list:
        """
        Get Vapor wallet derivation indexes.

        :return: list -- Vapor derivation indexes.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44/153/1/0/1")
        >>> wallet.indexes()
        ['2c000000', '99000000', '01000000', '00000000', '01000000']
        """

        return self._hdwallet.indexes()

    def xprivate_key(self) -> Optional[str]:
        """
        Get Vapor wallet xprivate key.

        :return: str -- Vapor xprivate key.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.xprivate_key()
        "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"
        """

        return self._hdwallet.xprivate_key()

    def xpublic_key(self) -> Optional[str]:
        """
        Get Vapor wallet xpublic key.

        :return: str -- Vapor xpublic key.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.xpublic_key()
        "16476b7fd68ca2acd92cfc38fa353e75d6103f828276f44d587e660a6bd7a5c5ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"
        """

        return self._hdwallet.xpublic_key()

    def expand_xprivate_key(self) -> Optional[str]:
        """
        Get Vapor wallet expand xprivate key.

        :return: str -- Vapor expand xprivate key.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.expand_xprivate_key()
        "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee5102416c643cfb46ab1ae5a524c8b4aaa002eb771d0d9cfc7490c0c3a8177e053e"
        """

        return self._hdwallet.expand_xprivate_key()

    def child_xprivate_key(self) -> Optional[str]:
        """
        Get Vapor child wallet xprivate key.

        :return: str -- Vapor child xprivate key.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44/153/1/0/1")
        >>> wallet.child_xprivate_key()
        "e07af52746e7cccd0a7d1fba6651a6f474bada481f34b1c5bab5e2d71e36ee515803ee0a6682fb19e279d8f4f7acebee8abd0fc74771c71565f9a9643fd77141"
        """

        return self._hdwallet.child_xprivate_key()

    def child_xpublic_key(self) -> Optional[str]:
        """
        Get Vapor child wallet xpublic key.

        :return: str -- Vapor child xpublic key.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44/153/1/0/1")
        >>> wallet.child_xpublic_key()
        "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e25803ee0a6682fb19e279d8f4f7acebee8abd0fc74771c71565f9a9643fd77141"
        """

        return self._hdwallet.child_xpublic_key()

    def guid(self) -> Optional[str]:
        """
        Get Vapor wallet Blockcenter GUID.

        :return: str -- Vapor Blockcenter GUID.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.guid()
        "f0ed6ddd-9d6b-49fd-8866-a52d1083a13b"
        """

        if self.xpublic_key() is None:
            return None
        return account_create(xpublic_key=self.xpublic_key(), network=self._network)["guid"]

    def private_key(self) -> str:
        """
        Get Vapor wallet private key.

        :return: str -- Vapor private key.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44/153/1/0/1")
        >>> wallet.private_key()
        "e07af52746e7cccd0a7d1fba6651a6f474bada481f34b1c5bab5e2d71e36ee515803ee0a6682fb19e279d8f4f7acebee8abd0fc74771c71565f9a9643fd77141"
        """

        return self._hdwallet.private_key()

    def public_key(self) -> str:
        """
        Get Vapor wallet public key.

        :return: str -- Vapor public key.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44/153/1/0/1")
        >>> wallet.public_key()
        "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2"
        """

        return self._hdwallet.public_key()

    def program(self) -> str:
        """
        Get Vapor wallet control program.

        :return: str -- Vapor control program.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44/153/1/0/1")
        >>> wallet.program()
        "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a"
        """

        return self._hdwallet.program()

    def address(self, network: Optional[str] = config["network"]) -> str:
        """
        Get Vapor wallet address.

        :param network: Vapor network, defaults to mainnet.
        :type network: str
        :return: str -- Vapor wallet address.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_indexes(["2c000000", "99000000", "01000000", "00000000", "01000000"])
        >>> wallet.address(network="mainnet")
        "vp1q9ndylx02syfwd7npehfxz4lddhzqsve2za23ag"
        """

        if network is None:
            network = self._network
        return self._hdwallet.address(network=network, vapor=True)

    def balance(self, asset: str = config["asset"]) -> int:
        """
        Get Vapor wallet balance.

        :param asset: Vapor asset id, defaults to BTM asset.
        :type asset: str
        :return: int -- Vapor wallet balance (NEU amount).

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44/153/1/0/1")
        >>> wallet.balance()
        47000000
        """

        return get_balance(address=self.address(), asset=asset, network=self._network)

    def utxos(self, asset: str = config["asset"], limit: int = 15) -> list:
        """
        Get Vapor wallet unspent transaction output (UTXO's).

        :param asset: Vapor asset id, defaults to BTM asset.
        :type asset: str
        :param limit: Vapor balance, default is 15.
        :type limit: int
        :return: list -- Vapor unspent transaction outputs.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44/153/1/0/1")
        >>> wallet.utxos()
        [{'hash': '4e2a17b01b9307107f0abb48ef757bec56befc74b903cfdb763981943bbe318b', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 47000000}]
        """

        return get_utxos(program=self.program(), asset=asset, limit=limit)
