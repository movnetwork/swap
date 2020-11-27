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
        :returns:  Wallet -- Vapor wallet instance.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
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
        >>> wallet.from_mnemonic("extend length miss suit broken rescue around harbor vehicle vicious jelly quality")
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
        >>> wallet.from_seed("51a0f6fb9abd5e5aa27f42dd375d8e4fc6944c704c859454e557fc419d3979e5a50273743c93e5035244adb09e9a37914abc583fdfae0da1ae2bedaa373f050e")
        <swap.providers.vapor.wallet.Wallet object at 0x040DA268>
        """
        self._hdwallet.from_seed(seed)
        return self

    def from_xprivate_key(self, xprivate_key: str) -> "Wallet":
        """
        Initiate Vapor wallet from xprivate key.

        :param xprivate_key: Vapor wallet xprivate key.
        :type xprivate_key: str.
        :returns: Wallet -- Vapor wallet instance.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_xprivate_key("d0d4862706cfe7d2ffdf53d00fba1d524587972e2eb0226ce9fff3ca58e5a14f031f74b091a04f3ff6b1722540eefcd4e2bcdcba0944a2df781cfdccf2f47e59")
        <swap.providers.vapor.wallet.Wallet object at 0x040DA268>
        """
        self._hdwallet.from_xprivate_key(xprivate_key)
        return self

    def from_private_key(self, private_key: str) -> "Wallet":
        """
        Initialize Vapor wallet from private key.

        :param private_key: Vapor private key.
        :type private_key: str.
        :returns: Wallet -- Vapor wallet instance.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_private_key("40d171e524c5d366c87f789e293e9e8d63ab95be796b3c04b63db29321eaa14f92de5a98859ca593b63f9e421958d8ded8e171aaad775d85f7a78515a1992f6c")
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
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.from_path("m/44/153/1/0/1")
        <swap.providers.vapor.wallet.Wallet object at 0x040DA268>
        """
        self._hdwallet.from_path(path)
        return self

    def from_indexes(self, indexes: List[str]) -> "Wallet":
        """
        Drive Vapor wallet from indexes.

        :param indexes: Vapor derivation indexes.
        :type indexes: list.
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
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
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
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
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

        :return: str -- Vapor wallet strength.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
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
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.entropy()
        "50f002376c81c96e430b48f1fe71df57"
        """
        return self._hdwallet.entropy()

    def mnemonic(self) -> Optional[str]:
        """
        Get Vapor wallet mnemonic.

        :return: str -- Vapor wallet mnemonic.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.mnemonic()
        "extend length miss suit broken rescue around harbor vehicle vicious jelly quality"
        """
        return self._hdwallet.mnemonic()

    def passphrase(self) -> Optional[str]:
        """
        Get Vapor wallet passphrase.

        :return: str -- Vapor wallet passphrase.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57", passphrase="meherett")
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
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
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
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.seed()
        "51a0f6fb9abd5e5aa27f42dd375d8e4fc6944c704c859454e557fc419d3979e5a50273743c93e5035244adb09e9a37914abc583fdfae0da1ae2bedaa373f050e"
        """
        return self._hdwallet.seed()

    def path(self) -> Optional[str]:
        """
        Get Vapor wallet derivation path.

        :return: str -- Vapor derivation path.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet", change=True, address=3)
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
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
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
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
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.xprivate_key()
        "d0d4862706cfe7d2ffdf53d00fba1d524587972e2eb0226ce9fff3ca58e5a14f031f74b091a04f3ff6b1722540eefcd4e2bcdcba0944a2df781cfdccf2f47e59"
        """
        return self._hdwallet.xprivate_key()

    def xpublic_key(self) -> Optional[str]:
        """
        Get Vapor wallet xpublic key.

        :return: str -- Vapor xpublic key.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.xpublic_key()
        "5086c8522be8c3b8674d72a6b9aa19eef43ef1992a482e71f389d99159accc39031f74b091a04f3ff6b1722540eefcd4e2bcdcba0944a2df781cfdccf2f47e59"
        """
        return self._hdwallet.xpublic_key()

    def expand_xprivate_key(self) -> Optional[str]:
        """
        Get Vapor wallet expand xprivate key.

        :return: str -- Vapor expand xprivate key.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.expand_xprivate_key()
        "d0d4862706cfe7d2ffdf53d00fba1d524587972e2eb0226ce9fff3ca58e5a14f7c15b70c1b0fc7a393fdb443c54b55e187635bf3dec62af44741085b7f12015a"
        """
        return self._hdwallet.expand_xprivate_key()

    def child_xprivate_key(self) -> Optional[str]:
        """
        Get Vapor child wallet xprivate key.

        :return: str -- Vapor child xprivate key.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.child_xprivate_key()
        "40d171e524c5d366c87f789e293e9e8d63ab95be796b3c04b63db29321eaa14f92de5a98859ca593b63f9e421958d8ded8e171aaad775d85f7a78515a1992f6c"
        """
        return self._hdwallet.child_xprivate_key()

    def child_xpublic_key(self) -> Optional[str]:
        """
        Get Vapor child wallet xpublic key.

        :return: str -- Vapor child xpublic key.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.child_xpublic_key()
        "ffbbd79031060ef98fee4deda59818732e7665de15df34dff209d1f6f9a1443992de5a98859ca593b63f9e421958d8ded8e171aaad775d85f7a78515a1992f6c"
        """
        return self._hdwallet.child_xpublic_key()

    def guid(self) -> Optional[str]:
        """
        Get Vapor wallet Blockcenter GUID.

        :return: str -- Vapor Blockcenter GUID.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.guid()
        "e34d612c-f1f9-42c6-8b14-3d93c5b21715"
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
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.from_path("m/44/153/1/0/1")
        >>> wallet.private_key()
        "40d171e524c5d366c87f789e293e9e8d63ab95be796b3c04b63db29321eaa14f92de5a98859ca593b63f9e421958d8ded8e171aaad775d85f7a78515a1992f6c"
        """
        return self._hdwallet.private_key()

    def public_key(self) -> str:
        """
        Get Vapor wallet public key.

        :return: str -- Vapor public key.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.from_path("m/44/153/1/0/1")
        >>> wallet.public_key()
        "ffbbd79031060ef98fee4deda59818732e7665de15df34dff209d1f6f9a14439"
        """
        return self._hdwallet.public_key()

    def program(self):
        """
        Get Vapor wallet control program.

        :return: str -- Vapor control program.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.from_path("m/44/153/1/0/1")
        >>> wallet.program()
        "00144eaaa3205545eac08fb3a2d1b1570b67c3b46016"
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
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.from_indexes(["2c000000", "99000000", "01000000", "00000000", "01000000"])
        >>> wallet.address(network="mainnet")
        "bm1qf642xgz4gh4vpran5tgmz4ctvlpmgcqkmhn2le"
        """

        if network is None:
            network = self._network

        return self._hdwallet.address(network=network, vapor=True)

    def balance(self, asset: str = config["asset"]) -> int:
        """
        Get Vapor wallet balance.

        :param asset: Vapor asset id, defaults to BTM asset.
        :type asset: str
        :return: int -- Vapor wallet balance.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.from_path("m/44/153/1/0/1")
        >>> wallet.balance()
        2450000000
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
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.from_path("m/44/153/1/0/1")
        >>> wallet.utxos()
        [{'hash': 'e152f88d33c6659ad823d15c5c65b2ed946d207c42430022cba9bb9b9d70a7a4', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 587639800}, {'hash': '88289fa4c7633574931be7ce4102aeb24def0de20e38e7d69a5ddd6efc116b95', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 8160000}, {'hash': 'f71c68f921b434cc2bcd469d26e7927aa6db7500e4cdeef814884f11c10f5de2', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 10000}, {'hash': 'e46cfecc1f1a26413172ce81c78affb19408e613915642fa5fb04d3b0a4ffa65', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 100}]
        """

        return get_utxos(program=self.program(), asset=asset, limit=limit)
