#!/usr/bin/env python3

from pybytom.wallet import Wallet as HDWallet
from pybytom.rpc import account_create
from typing import (
    Optional, List
)

from ...utils import is_mnemonic
from ...exceptions import NetworkError
from ..config import bytom as config
from .rpc import (
    get_balance, get_utxos
)

# Default path and indexes derivation
DEFAULT_PATH: str = config["path"]
DEFAULT_INDEXES: List[str] = config["indexes"]
DEFAULT_BIP44: str = config["BIP44"]


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

    def from_entropy(self, entropy: str, passphrase: Optional[str] = None, language: str = "english") -> "Wallet":
        """
        Initiate Bytom wallet from entropy.

        :param entropy: Bytom wallet entropy.
        :type entropy: str
        :param passphrase: Bytom wallet passphrase, default to None.
        :type passphrase: str
        :param language: Bytom wallet language, default to english.
        :type language: str

        :returns: Wallet -- Bytom wallet instance.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        <swap.providers.bytom.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_entropy(entropy, passphrase, language)
        return self

    def from_mnemonic(self, mnemonic: str, passphrase: Optional[str] = None,
                      language: Optional[str] = None) -> "Wallet":
        """
        Initialize Bytom wallet from mnemonic.

        :param mnemonic: Bytom wallet mnemonic.
        :type mnemonic: str
        :param passphrase: Bytom wallet passphrase, default to None.
        :type passphrase: str
        :param language: Bytom wallet language, default to english.
        :type language: str

        :returns: Wallet -- Bytom wallet class instance.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        <swap.providers.bytom.wallet.Wallet object at 0x040DA268>
        """

        # Check parameter instances
        if not is_mnemonic(mnemonic=mnemonic, language=language):
            raise ValueError("Invalid Mnemonic words.")

        self._hdwallet.from_mnemonic(mnemonic, passphrase, language)
        return self

    def from_seed(self, seed: str) -> "Wallet":
        """
        Initialize Bytom wallet from seed.

        :param seed: Bytom wallet seed.
        :type seed: str

        :returns: Wallet -- Bytom wallet class instance.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_seed("baff3e1fe60e1f2a2d840d304acc98d1818140c79354a353b400fb019bfb256bc392d7aa9047adff1f14bce0342e14605c6743a6c08e02150588375eb2eb7d49")
        <swap.providers.bytom.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_seed(seed)
        return self

    def from_xprivate_key(self, xprivate_key: str) -> "Wallet":
        """
        Initiate Bytom wallet from xprivate key.

        :param xprivate_key: Bytom wallet xprivate key.
        :type xprivate_key: str

        :returns: Wallet -- Bytom wallet instance.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_xprivate_key("205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
        <swap.providers.bytom.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_xprivate_key(xprivate_key)
        return self

    def from_private_key(self, private_key: str) -> "Wallet":
        """
        Initialize Bytom wallet from private key.

        :param private_key: Bytom private key.
        :type private_key: str

        :returns: Wallet -- Bytom wallet instance.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_private_key("e07af52746e7cccd0a7d1fba6651a6f474bada481f34b1c5bab5e2d71e36ee515803ee0a6682fb19e279d8f4f7acebee8abd0fc74771c71565f9a9643fd77141")
        <swap.providers.bytom.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_private_key(private_key)
        return self

    def from_path(self, path: str) -> "Wallet":
        """
        Drive Bytom wallet from path.

        :param path: Bytom wallet path.
        :type path: str

        :returns: Wallet -- Bytom wallet instance.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44/153/1/0/1")
        <swap.providers.bytom.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_path(path)
        return self

    def from_indexes(self, indexes: List[str]) -> "Wallet":
        """
        Drive Bytom wallet from indexes.

        :param indexes: Bytom derivation indexes.
        :type indexes: list

        :returns: Wallet -- Bytom wallet class instance.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_xprivate_key("205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
        >>> wallet.from_indexes(["2c000000", "99000000", "01000000", "00000000", "01000000"])
        <swap.providers.bytom.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_indexes(indexes)
        return self

    def from_index(self, index: int, harden: bool = False) -> "Wallet":
        """
        Drive Bytom wallet from index.

        :param index: Bytom wallet index.
        :type index: int
        :param harden: Use harden, default to False.
        :type harden: bool

        :returns: Wallet -- Bytom wallet instance.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_index(44)
        >>> wallet.from_index(153)
        >>> wallet.from_index(1)
        >>> wallet.from_index(0)
        >>> wallet.from_index(1)
        <swap.providers.bytom.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_index(index, harden)
        return self

    def clean_derivation(self) -> "Wallet":
        """
        Clean derivation Bytom wallet.

        :returns: Wallet -- Bytom wallet instance.

        >>> from swap.providers.bytom.wallet import Wallet
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
        Get Bytom wallet strength.

        :return: int -- Bytom wallet strength.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.strength()
        128
        """

        return self._hdwallet.strength()

    def entropy(self) -> Optional[str]:
        """
        Get Bytom wallet entropy.

        :return: str -- Bytom wallet entropy.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.entropy()
        "72fee73846f2d1a5807dc8c953bf79f1"
        """

        return self._hdwallet.entropy()

    def mnemonic(self) -> Optional[str]:
        """
        Get Bytom wallet mnemonic.

        :return: str -- Bytom wallet mnemonic.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.mnemonic()
        "indicate warm sock mistake code spot acid ribbon sing over taxi toast"
        """

        return self._hdwallet.mnemonic()

    def passphrase(self) -> Optional[str]:
        """
        Get Bytom wallet passphrase.

        :return: str -- Bytom wallet passphrase.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1", passphrase="meherett")
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
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
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
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.seed()
        "baff3e1fe60e1f2a2d840d304acc98d1818140c79354a353b400fb019bfb256bc392d7aa9047adff1f14bce0342e14605c6743a6c08e02150588375eb2eb7d49"
        """

        return self._hdwallet.seed()

    def path(self) -> Optional[str]:
        """
        Get Bytom wallet derivation path.

        :return: str -- Bytom derivation path.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet", change=True, address=3)
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
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
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
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
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.xprivate_key()
        "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"
        """

        return self._hdwallet.xprivate_key()

    def xpublic_key(self) -> Optional[str]:
        """
        Get Bytom wallet xpublic key.

        :return: str -- Bytom xpublic key.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.xpublic_key()
        "16476b7fd68ca2acd92cfc38fa353e75d6103f828276f44d587e660a6bd7a5c5ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"
        """

        return self._hdwallet.xpublic_key()

    def expand_xprivate_key(self) -> Optional[str]:
        """
        Get Bytom wallet expand xprivate key.

        :return: str -- Bytom expand xprivate key.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.expand_xprivate_key()
        "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee5102416c643cfb46ab1ae5a524c8b4aaa002eb771d0d9cfc7490c0c3a8177e053e"
        """

        return self._hdwallet.expand_xprivate_key()

    def child_xprivate_key(self) -> Optional[str]:
        """
        Get Bytom child wallet xprivate key.

        :return: str -- Bytom child xprivate key.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44/153/1/0/1")
        >>> wallet.child_xprivate_key()
        "e07af52746e7cccd0a7d1fba6651a6f474bada481f34b1c5bab5e2d71e36ee515803ee0a6682fb19e279d8f4f7acebee8abd0fc74771c71565f9a9643fd77141"
        """

        return self._hdwallet.child_xprivate_key()

    def child_xpublic_key(self) -> Optional[str]:
        """
        Get Bytom child wallet xpublic key.

        :return: str -- Bytom child xpublic key.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44/153/1/0/1")
        >>> wallet.child_xpublic_key()
        "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e25803ee0a6682fb19e279d8f4f7acebee8abd0fc74771c71565f9a9643fd77141"
        """

        return self._hdwallet.child_xpublic_key()

    def guid(self) -> Optional[str]:
        """
        Get Bytom wallet Blockcenter GUID.

        :return: str -- Bytom Blockcenter GUID.

        >>> from swap.providers.bytom.wallet import Wallet
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
        Get Bytom wallet private key.

        :return: str -- Bytom private key.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44/153/1/0/1")
        >>> wallet.private_key()
        "e07af52746e7cccd0a7d1fba6651a6f474bada481f34b1c5bab5e2d71e36ee515803ee0a6682fb19e279d8f4f7acebee8abd0fc74771c71565f9a9643fd77141"
        """

        return self._hdwallet.private_key()

    def public_key(self) -> str:
        """
        Get Bytom wallet public key.

        :return: str -- Bytom public key.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44/153/1/0/1")
        >>> wallet.public_key()
        "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2"
        """

        return self._hdwallet.public_key()

    def program(self) -> str:
        """
        Get Bytom wallet control program.

        :return: str -- Bytom control program.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44/153/1/0/1")
        >>> wallet.program()
        "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a"
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
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_indexes(["2c000000", "99000000", "01000000", "00000000", "01000000"])
        >>> wallet.address(network="mainnet")
        "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7"
        """
        return self._hdwallet.address()

    def balance(self, asset: str = config["asset"]) -> int:
        """
        Get Bytom wallet balance.

        :param asset: Bytom asset id, defaults to BTM asset.
        :type asset: str

        :return: int -- Bytom wallet balance (NEU amount).

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44/153/1/0/1")
        >>> wallet.balance()
        71510800
        """

        return get_balance(address=self.address(), asset=asset, network=self._network)

    def utxos(self, asset: str = config["asset"], limit: int = 15) -> list:
        """
        Get Bytom wallet unspent transaction output (UTXO's).

        :param asset: Bytom asset id, defaults to BTM asset.
        :type asset: str
        :param limit: Bytom balance, default is 15.
        :type limit: int

        :return: list -- Bytom unspent transaction outputs.

        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44/153/1/0/1")
        >>> wallet.utxos()
        [{'hash': '7c1e20e6ff719176a3ed6f5332ec3ff665ab28754d2511950e591267e0e675df', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 71510800}, {'hash': '01b07c3523085b75f1e047be3a73b263635d0b86f9b751457a51b26c5a97a110', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 50000}, {'hash': 'e46cfecc1f1a26413172ce81c78affb19408e613915642fa5fb04d3b0a4ffa65', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 100}]
        """

        return get_utxos(program=self.program(), asset=asset, limit=limit)
