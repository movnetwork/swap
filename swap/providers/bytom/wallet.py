#!/usr/bin/env python3

from pybytom.wallet import Wallet as HDWallet
from pybytom.rpc import account_create
from typing import TypeVar, Optional, List

from .rpc import get_balance
from ...utils.exceptions import NetworkError
from ..config import bytom

# Bytom config
config = bytom()
# Var Wallet class
_Wallet = TypeVar("_Wallet", bound="Wallet")


class Wallet(HDWallet):
    """
    Bytom Wallet class.

    :param network: Bytom network, defaults to mainnet.
    :type network: str
    :returns: Wallet -- Bytom wallet instance.

    .. note::
        Bytom has only two networks, ``mainnet``, ``solonet`` and ``testnet``.
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

    def from_entropy(self, entropy: str, passphrase: Optional[str] = None, language: str = "english") -> _Wallet:
        """
        Initiate Bytom wallet from entropy.

        :param entropy: Bytom wallet entropy.
        :type entropy: str
        :param passphrase: Bytom wallet passphrase, default to None.
        :type passphrase: str
        :param language: Bytom wallet language, default to english.
        :type language: str
        :returns:  Wallet -- Bytom wallet instance.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        <swap.providers.bytom.wallet.Wallet object at 0x040DA268>
        """
        self._hdwallet.from_entropy(entropy, passphrase, language)
        return self

    def from_mnemonic(self, mnemonic: str, passphrase: Optional[str] = None,
                      language: Optional[str] = None) -> _Wallet:
        """
        Initialize Bytom wallet from mnemonic.

        :param mnemonic: Bytom wallet mnemonic.
        :type mnemonic: str
        :param passphrase: Bytom wallet passphrase, default to None.
        :type passphrase: str
        :param language: Bytom wallet language, default to english.
        :type language: str
        :returns:  Wallet -- Bytom wallet class instance.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("extend length miss suit broken rescue around harbor vehicle vicious jelly quality")
        <swap.providers.bytom.wallet.Wallet object at 0x040DA268>
        """
        self._hdwallet.from_mnemonic(mnemonic, passphrase, language)
        return self

    def from_seed(self, seed: str) -> _Wallet:
        """
        Initialize Bytom wallet from seed.

        :param seed: Bytom wallet seed.
        :type seed: str
        :returns:  Wallet -- Bytom wallet class instance.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_seed("51a0f6fb9abd5e5aa27f42dd375d8e4fc6944c704c859454e557fc419d3979e5a50273743c93e5035244adb09e9a37914abc583fdfae0da1ae2bedaa373f050e")
        <swap.providers.bytom.wallet.Wallet object at 0x040DA268>
        """
        self._hdwallet.from_seed(seed)
        return self

    def from_xprivate_key(self, xprivate_key: str) -> _Wallet:
        """
        Initiate Bytom wallet from xprivate key.

        :param xprivate_key: Bytom wallet xprivate key.
        :type xprivate_key: str.
        :returns:  Wallet -- Bytom wallet instance.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_xprivate_key("d0d4862706cfe7d2ffdf53d00fba1d524587972e2eb0226ce9fff3ca58e5a14f031f74b091a04f3ff6b1722540eefcd4e2bcdcba0944a2df781cfdccf2f47e59")
        <swap.providers.bytom.wallet.Wallet object at 0x040DA268>
        """
        self._hdwallet.from_xprivate_key(xprivate_key)
        return self

    def from_private_key(self, private_key: str) -> _Wallet:
        """
        Initialize Bytom wallet from private key.

        :param private_key: Bytom private key.
        :type private_key: str.
        :returns:  Wallet -- Bytom wallet instance.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_private_key("40d171e524c5d366c87f789e293e9e8d63ab95be796b3c04b63db29321eaa14f92de5a98859ca593b63f9e421958d8ded8e171aaad775d85f7a78515a1992f6c")
        <swap.providers.bytom.wallet.Wallet object at 0x040DA268>
        """
        self._hdwallet.from_private_key(private_key)
        return self

    def from_path(self, path: str) -> _Wallet:
        """
        Drive Bytom wallet from path.

        :param path: Bytom wallet path.
        :type path: str
        :returns: Wallet -- Bytom wallet instance.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.from_path("m/44/153/1/0/1")
        <swap.providers.bytom.wallet.Wallet object at 0x040DA268>
        """
        self._hdwallet.from_path(path)
        return self

    def from_indexes(self, indexes: List[str]) -> _Wallet:
        """
        Drive Bytom wallet from indexes.

        :param indexes: Bytom derivation indexes.
        :type indexes: list.
        :returns:  Wallet -- Bytom wallet class instance.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_xprivate_key("205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
        >>> wallet.from_indexes(["2c000000", "99000000", "01000000", "00000000", "01000000"])
        <swap.providers.bytom.wallet.Wallet object at 0x040DA268>
        """
        self._hdwallet.from_indexes(indexes)
        return self

    def from_index(self, index: int, harden: bool = False) -> _Wallet:
        """
        Drive Bytom wallet from index.

        :param index: Bytom wallet index.
        :type index: int
        :param harden: Use harden, default to False.
        :type harden: bool
        :returns: Wallet -- Bytom wallet instance.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.from_index(44)
        >>> wallet.from_index(153)
        >>> wallet.from_index(1)
        >>> wallet.from_index(0)
        >>> wallet.from_index(1)
        <swap.providers.bytom.wallet.Wallet object at 0x040DA268>
        """
        self._hdwallet.from_index(index, harden)
        return self

    def clean_derivation(self) -> _Wallet:
        """
        Clean derivation Bytom wallet.

        :returns: Wallet -- Bytom wallet instance.

        >>> from swap.providers.bytom.wallet import Wallet
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

    def entropy(self) -> Optional[str]:
        """
        Get Bytom wallet entropy.

        :return: str -- Bytom wallet entropy.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.entropy()
        "50f002376c81c96e430b48f1fe71df57"
        """
        return self._hdwallet.entropy()

    def mnemonic(self) -> Optional[str]:
        """
        Get Bytom wallet mnemonic.

        :return: str -- Bytom wallet mnemonic.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.mnemonic()
        "extend length miss suit broken rescue around harbor vehicle vicious jelly quality"
        """
        return self._hdwallet.mnemonic()

    def passphrase(self) -> Optional[str]:
        """
        Get Bytom wallet passphrase.

        :return: str -- Bytom wallet passphrase.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57", passphrase="meherett")
        >>> wallet.passphrase()
        "meherett"
        """
        return self._hdwallet.passphrase()

    def language(self) -> Optional[str]:
        """
        Get Bytom wallet language.

        :return: str -- Bytom wallet language.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.language()
        "english"
        """
        return self._hdwallet.language()

    def seed(self) -> Optional[str]:
        """
        Get Bytom wallet seed.

        :return: str -- Bytom wallet seed.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.seed()
        "51a0f6fb9abd5e5aa27f42dd375d8e4fc6944c704c859454e557fc419d3979e5a50273743c93e5035244adb09e9a37914abc583fdfae0da1ae2bedaa373f050e"
        """
        return self._hdwallet.seed()

    def path(self) -> Optional[str]:
        """
        Get Bytom wallet derivation path.

        :return: str -- Bytom derivation path.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet", change=True, address=3)
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.from_path("m/44/153/1/0/1")
        >>> wallet.path()
        "m/44/153/1/0/1"
        """
        return self._hdwallet.path()

    def indexes(self) -> list:
        """
        Get Bytom wallet derivation indexes.

        :return: list -- Bytom derivation indexes.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.from_path("m/44/153/1/0/1")
        >>> wallet.indexes()
        ['2c000000', '99000000', '01000000', '00000000', '01000000']
        """
        return self._hdwallet.indexes()

    def xprivate_key(self) -> Optional[str]:
        """
        Get Bytom wallet xprivate key.

        :return: str -- Bytom xprivate key.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.xprivate_key()
        "d0d4862706cfe7d2ffdf53d00fba1d524587972e2eb0226ce9fff3ca58e5a14f031f74b091a04f3ff6b1722540eefcd4e2bcdcba0944a2df781cfdccf2f47e59"
        """
        return self._hdwallet.xprivate_key()

    def xpublic_key(self) -> Optional[str]:
        """
        Get Bytom wallet xpublic key.

        :return: str -- Bytom xpublic key.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.xpublic_key()
        "5086c8522be8c3b8674d72a6b9aa19eef43ef1992a482e71f389d99159accc39031f74b091a04f3ff6b1722540eefcd4e2bcdcba0944a2df781cfdccf2f47e59"
        """
        return self._hdwallet.xpublic_key()

    def expand_xprivate_key(self) -> Optional[str]:
        """
        Get Bytom wallet expand xprivate key.

        :return: str -- Bytom expand xprivate key.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.expand_xprivate_key()
        "d0d4862706cfe7d2ffdf53d00fba1d524587972e2eb0226ce9fff3ca58e5a14f7c15b70c1b0fc7a393fdb443c54b55e187635bf3dec62af44741085b7f12015a"
        """
        return self._hdwallet.expand_xprivate_key()

    def child_xprivate_key(self) -> Optional[str]:
        """
        Get Bytom child wallet xprivate key.

        :return: str -- Bytom child xprivate key.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.child_xprivate_key()
        "40d171e524c5d366c87f789e293e9e8d63ab95be796b3c04b63db29321eaa14f92de5a98859ca593b63f9e421958d8ded8e171aaad775d85f7a78515a1992f6c"
        """
        return self._hdwallet.child_xprivate_key()

    def child_xpublic_key(self) -> Optional[str]:
        """
        Get Bytom child wallet xpublic key.

        :return: str -- Bytom child xpublic key.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.child_xpublic_key()
        "ffbbd79031060ef98fee4deda59818732e7665de15df34dff209d1f6f9a1443992de5a98859ca593b63f9e421958d8ded8e171aaad775d85f7a78515a1992f6c"
        """
        return self._hdwallet.child_xpublic_key()

    def guid(self) -> Optional[str]:
        """
        Get Bytom wallet Blockcenter GUID.

        :return: str -- Bytom Blockcenter GUID.

        >>> from swap.providers.bytom.wallet import Wallet
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
        Get Bytom wallet private key.

        :return: str -- Bytom private key.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.from_path("m/44/153/1/0/1")
        >>> wallet.private_key()
        "40d171e524c5d366c87f789e293e9e8d63ab95be796b3c04b63db29321eaa14f92de5a98859ca593b63f9e421958d8ded8e171aaad775d85f7a78515a1992f6c"
        """
        return self._hdwallet.private_key()

    def public_key(self) -> str:
        """
        Get Bytom wallet public key.

        :return: str -- Bytom public key.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.from_path("m/44/153/1/0/1")
        >>> wallet.public_key()
        "ffbbd79031060ef98fee4deda59818732e7665de15df34dff209d1f6f9a14439"
        """
        return self._hdwallet.public_key()

    def program(self):
        """
        Get Bytom wallet control program.

        :return: str -- Bytom control program.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.from_path("m/44/153/1/0/1")
        >>> wallet.program()
        "00144eaaa3205545eac08fb3a2d1b1570b67c3b46016"
        """
        return self._hdwallet.program()

    def address(self, network: Optional[str] = config["network"]) -> str:
        """
        Get Bytom wallet address.

        :param network: Bytom network, defaults to mainnet.
        :type network: str
        :return: str -- Bytom wallet address.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.from_indexes(["2c000000", "99000000", "01000000", "00000000", "01000000"])
        >>> wallet.address(network="mainnet")
        "bm1qf642xgz4gh4vpran5tgmz4ctvlpmgcqkmhn2le"
        """
        return self._hdwallet.address()

    def balance(self, asset: str = config["asset"]) -> int:
        """
        Get Bytom wallet balance.

        :param asset: Bytom asset id, defaults to BTM asset.
        :type asset: str
        :return: int -- Bytom wallet balance.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.from_path("m/44/153/1/0/1")
        >>> wallet.balance()
        2450000000
        """
        return get_balance(address=self.address(), asset=asset, network=self._network)
