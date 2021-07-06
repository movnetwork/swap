#!/usr/bin/env python3

from pybytom.wallet import Wallet as HDWallet
from typing import (
    Optional, List, Union
)

from ...utils import is_mnemonic
from ...exceptions import (
    NetworkError, UnitError
)
from ..config import vapor as config
from .assets import AssetNamespace
from .utils import amount_unit_converter
from .rpc import (
    get_balance, get_utxos, account_create
)

# Default derivation path
DEFAULT_PATH: str = config["path"]


class Wallet(HDWallet):
    """
    Vapor Wallet class.

    :param network: Vapor network, defaults to ``mainnet``.
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
            raise NetworkError(f"Invalid Vapor '{network}' network",
                               "choose only 'mainnet', 'solonet' or 'testnet' networks.")
        super().__init__(network=self._network)

    def from_entropy(self, entropy: str, language: str = "english", passphrase: Optional[str] = None) -> "Wallet":
        """
        Initiate Vapor wallet from entropy.

        :param entropy: Vapor entropy hex string.
        :type entropy: str
        :param language: Vapor wallet language, default to ``english``.
        :type language: str
        :param passphrase: Vapor wallet passphrase, default to ``None``.
        :type passphrase: str

        :returns: Wallet -- Vapor wallet instance.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        <swap.providers.vapor.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_entropy(entropy=entropy, language=language, passphrase=passphrase)
        return self

    def from_mnemonic(self, mnemonic: str, language: Optional[str] = None,
                      passphrase: Optional[str] = None) -> "Wallet":
        """
        Initialize Vapor wallet from mnemonic.

        :param mnemonic: Vapor mnemonic words.
        :type mnemonic: str
        :param language: Vapor wallet language, default to ``english``.
        :type language: str
        :param passphrase: Vapor wallet passphrase, default to ``None``.
        :type passphrase: str

        :returns: Wallet -- Vapor wallet instance.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic(mnemonic="unfair divorce remind addict add roof park clown build renew illness fault")
        <swap.providers.vapor.wallet.Wallet object at 0x040DA268>
        """

        # Check parameter instances
        if not is_mnemonic(mnemonic=mnemonic, language=language):
            raise ValueError("Invalid Mnemonic words.")

        self._hdwallet.from_mnemonic(mnemonic=mnemonic, language=language, passphrase=passphrase)
        return self

    def from_seed(self, seed: str) -> "Wallet":
        """
        Initialize Vapor wallet from seed.

        :param seed: Vapor Seed hex string.
        :type seed: str

        :returns: Wallet -- Vapor wallet instance.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="mainnet")
        >>> wallet.from_seed(seed="1cfd5df8a523d53a36cee369a93fac4e9efab5e4e138d479da2fb6df730697574409d572fe8325ec22e8ed25dea7495f498c3f5235fe6ae6d47b989267b6777c")
        <swap.providers.vapor.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_seed(seed=seed)
        return self

    def from_xprivate_key(self, xprivate_key: str) -> "Wallet":
        """
        Initiate Vapor wallet from xprivate key.

        :param xprivate_key: Vapor XPrivate key.
        :type xprivate_key: str

        :returns: Wallet -- Vapor wallet instance.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="mainnet")
        >>> wallet.from_xprivate_key(xprivate_key="58775359b7b3588dcdc1bcf373489fa1272cacc03909f78469657b0208e66e46daedfdd0fd8f8df14e2084c7e8df4701db3062dded1c713e0aae734ac09c4afd")
        <swap.providers.vapor.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_xprivate_key(xprivate_key=xprivate_key)
        return self

    def from_private_key(self, private_key: str) -> "Wallet":
        """
        Initialize Vapor wallet from private key.

        :param private_key: Vapor Private key.
        :type private_key: str

        :returns: Wallet -- Vapor wallet instance.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="mainnet")
        >>> wallet.from_private_key(private_key="b0f9552e4fedac7f2e750ae984e36a97cf2b24609f7ec43f35606ed65eec6e46db35f71c405fd5948ecffa2c512adafb35cc621f99a60ecb6ec8aef815a8c6e5")
        <swap.providers.vapor.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_private_key(private_key=private_key)
        return self

    def from_path(self, path: str) -> "Wallet":
        """
        Drive Vapor wallet from path.

        :param path: Vapor derivation path.
        :type path: str

        :returns: Wallet -- Vapor wallet instance.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path(path="m/44/153/1/0/1")
        <swap.providers.vapor.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_path(path=path)
        return self

    def from_indexes(self, indexes: List[str]) -> "Wallet":
        """
        Drive Vapor wallet from indexes.

        :param indexes: Vapor derivation indexes.
        :type indexes: list

        :returns: Wallet -- Vapor wallet instance.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="mainnet")
        >>> wallet.from_xprivate_key(xprivate_key="58775359b7b3588dcdc1bcf373489fa1272cacc03909f78469657b0208e66e46daedfdd0fd8f8df14e2084c7e8df4701db3062dded1c713e0aae734ac09c4afd")
        >>> wallet.from_indexes(indexes=["2c000000", "99000000", "01000000", "00000000", "01000000"])
        <swap.providers.vapor.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_indexes(indexes=indexes)
        return self

    def from_index(self, index: int, hardened: bool = False) -> "Wallet":
        """
        Drive Vapor wallet from index.

        :param index: Vapor wallet index.
        :type index: int
        :param hardened: Use hardened, default to ``False``.
        :type hardened: bool

        :returns: Wallet -- Vapor wallet instance.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_index(index=44)
        >>> wallet.from_index(index=153)
        >>> wallet.from_index(index=1)
        >>> wallet.from_index(index=0)
        >>> wallet.from_index(index=1)
        <swap.providers.vapor.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_index(index=index, harden=hardened)
        return self

    def clean_derivation(self) -> "Wallet":
        """
        Clean derivation Vapor wallet.

        :returns: Wallet -- Vapor wallet instance.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path(path="m/44/153/1/0/1")
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
        >>> wallet: Wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.strength()
        128
        """

        return self._hdwallet.strength()

    def entropy(self) -> Optional[str]:
        """
        Get Vapor wallet entropy.

        :return: str -- Vapor wallet entropy.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.entropy()
        "ed0802d701a033776811601dd6c5c4a9"
        """

        return self._hdwallet.entropy()

    def mnemonic(self) -> Optional[str]:
        """
        Get Vapor wallet mnemonic.

        :return: str -- Vapor wallet mnemonic.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.mnemonic()
        "unfair divorce remind addict add roof park clown build renew illness fault"
        """

        return self._hdwallet.mnemonic()

    def passphrase(self) -> Optional[str]:
        """
        Get Vapor wallet passphrase.

        :return: str -- Vapor wallet passphrase.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9", passphrase="meherett")
        >>> wallet.passphrase()
        "meherett"
        """

        return self._hdwallet.passphrase()

    def language(self) -> Optional[str]:
        """
        Get Vapor wallet language.

        :return: str -- Vapor wallet language.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.language()
        "english"
        """

        return self._hdwallet.language()

    def seed(self) -> Optional[str]:
        """
        Get Vapor wallet seed.

        :return: str -- Vapor wallet seed.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.seed()
        "1cfd5df8a523d53a36cee369a93fac4e9efab5e4e138d479da2fb6df730697574409d572fe8325ec22e8ed25dea7495f498c3f5235fe6ae6d47b989267b6777c"
        """

        return self._hdwallet.seed()

    def path(self) -> Optional[str]:
        """
        Get Vapor wallet derivation path.

        :return: str -- Vapor derivation path.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet = Wallet(network="mainnet", change=True, address=3)
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path(path="m/44/153/1/0/1")
        >>> wallet.path()
        "m/44/153/1/0/1"
        """

        return self._hdwallet.path()

    def indexes(self) -> list:
        """
        Get Vapor wallet derivation indexes.

        :return: list -- Vapor derivation indexes.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path(path="m/44/153/1/0/1")
        >>> wallet.indexes()
        ['2c000000', '99000000', '01000000', '00000000', '01000000']
        """

        return self._hdwallet.indexes()

    def xprivate_key(self) -> Optional[str]:
        """
        Get Vapor wallet xprivate key.

        :return: str -- Vapor xprivate key.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.xprivate_key()
        "58775359b7b3588dcdc1bcf373489fa1272cacc03909f78469657b0208e66e46daedfdd0fd8f8df14e2084c7e8df4701db3062dded1c713e0aae734ac09c4afd"
        """

        return self._hdwallet.xprivate_key()

    def xpublic_key(self) -> Optional[str]:
        """
        Get Vapor wallet xpublic key.

        :return: str -- Vapor xpublic key.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.xpublic_key()
        "f80a401807fde1ee5727ae032ee144e4b757e69431e68e6cd732eda3c8cd3936daedfdd0fd8f8df14e2084c7e8df4701db3062dded1c713e0aae734ac09c4afd"
        """

        return self._hdwallet.xpublic_key()

    def expand_xprivate_key(self) -> Optional[str]:
        """
        Get Vapor wallet expand xprivate key.

        :return: str -- Vapor expand xprivate key.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.expand_xprivate_key()
        "58775359b7b3588dcdc1bcf373489fa1272cacc03909f78469657b0208e66e465c68d75d8a29eb3ffd7e82138088eec937e0c3d753946d35ae2d40d84a03bcf9"
        """

        return self._hdwallet.expand_xprivate_key()

    def child_xprivate_key(self) -> Optional[str]:
        """
        Get Vapor child wallet xprivate key.

        :return: str -- Vapor child xprivate key.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path(path="m/44/153/1/0/1")
        >>> wallet.child_xprivate_key()
        "b0f9552e4fedac7f2e750ae984e36a97cf2b24609f7ec43f35606ed65eec6e46db35f71c405fd5948ecffa2c512adafb35cc621f99a60ecb6ec8aef815a8c6e5"
        """

        return self._hdwallet.child_xprivate_key()

    def child_xpublic_key(self) -> Optional[str]:
        """
        Get Vapor child wallet xpublic key.

        :return: str -- Vapor child xpublic key.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path(path="m/44/153/1/0/1")
        >>> wallet.child_xpublic_key()
        "fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212db35f71c405fd5948ecffa2c512adafb35cc621f99a60ecb6ec8aef815a8c6e5"
        """

        return self._hdwallet.child_xpublic_key()

    def guid(self) -> Optional[str]:
        """
        Get Vapor wallet Blockcenter GUID.

        :return: str -- Vapor Blockcenter GUID.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.guid()
        "9ed61a9b-e7b6-4cb7-94fb-932b738e4f66"
        """

        if self.xpublic_key() is None:
            return None
        return account_create(xpublic_key=self.xpublic_key(), network=self._network)["guid"]

    def private_key(self) -> str:
        """
        Get Vapor wallet private key.

        :return: str -- Vapor private key.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path(path="m/44/153/1/0/1")
        >>> wallet.private_key()
        "b0f9552e4fedac7f2e750ae984e36a97cf2b24609f7ec43f35606ed65eec6e46db35f71c405fd5948ecffa2c512adafb35cc621f99a60ecb6ec8aef815a8c6e5"
        """

        return self._hdwallet.private_key()

    def public_key(self) -> str:
        """
        Get Vapor wallet public key.

        :return: str -- Vapor public key.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path(path="m/44/153/1/0/1")
        >>> wallet.public_key()
        "fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212"
        """

        return self._hdwallet.public_key()

    def program(self) -> str:
        """
        Get Vapor wallet control program.

        :return: str -- Vapor control program.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path(path="m/44/153/1/0/1")
        >>> wallet.program()
        "0014b1592acbb917f13937166c2a9b6ce973296ebb60"
        """

        return self._hdwallet.program()

    def address(self, network: Optional[str] = None) -> str:
        """
        Get Vapor wallet address.

        :param network: Vapor network, defaults to ``mainnet``.
        :type network: str

        :return: str -- Vapor wallet address.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_indexes(indexes=["2c000000", "99000000", "01000000", "00000000", "01000000"])
        >>> wallet.address(network="mainnet")
        "bm1qk9vj4jaezlcnjdckds4fkm8fwv5kawmq9qrufx"
        """

        if network is None:
            network = self._network
        return self._hdwallet.address(network=network, vapor=True)

    def balance(self, asset: Union[str, AssetNamespace] = config["asset"],
                unit: str = config["unit"]) -> Union[int, float]:
        """
        Get Vapor wallet balance.

        :param asset: Vapor asset id, defaults to ``BTM asset``.
        :type asset: str, vapor.assets.AssetNamespace
        :param unit: Vapor unit, default to ``NEU``.
        :type unit: str

        :return: int, float -- Vapor wallet balance.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path(path="m/44/153/1/0/1")
        >>> wallet.balance(unit="BTM")
        2.0
        """

        if unit not in ["BTM", "mBTM", "NEU"]:
            raise UnitError("Invalid Vapor unit, choose only BTM, mBTM or NEU units.")
        _balance: int = get_balance(
            address=self.address(),
            asset=(str(asset.ID) if isinstance(asset, AssetNamespace) else asset),
            network=self._network
        )
        return _balance if unit == "NEU" else \
            amount_unit_converter(amount=_balance, unit_from=f"NEU2{unit}")

    def utxos(self, asset: Union[str, AssetNamespace] = config["asset"], limit: int = 15) -> list:
        """
        Get Vapor wallet unspent transaction output (UTXO's).

        :param asset: Vapor asset id, defaults to ``BTM asset``.
        :type asset: str, vapor.assets.AssetNamespace
        :param limit: Limit of UTXO's, default is ``15``.
        :type limit: int

        :return: list -- Vapor unspent transaction outputs.

        >>> from swap.providers.vapor.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path(path="m/44/153/1/0/1")
        >>> wallet.utxos()
        [{'hash': '9843c9b9130bd87a9683f2c4e66456326beeefb2522c3352326de870c5c1329e', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 200000000}]
        """

        return get_utxos(
            program=self.program(),
            asset=(str(asset.ID) if isinstance(asset, AssetNamespace) else asset),
            limit=limit
        )
