#!/usr/bin/env python3

from hdwallet import HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from web3.types import Wei
from typing import (
    Optional, Union
)

from ...utils import is_mnemonic
from ...exceptions import (
    NetworkError, UnitError
)
from ..config import ethereum as config
from .utils import (
    is_network, amount_unit_converter
)
from .rpc import (
    get_balance
)

# Default path and indexes derivation
DEFAULT_PATH: str = config["path"]
DEFAULT_BIP44_PATH: str = config["BIP44"]


class Wallet(HDWallet):
    """
    Ethereum Wallet class.

    :param network: Ethereum network, defaults to ``ropsten``.
    :type network: str
    :param provider: Ethereum network provider, defaults to ``http``.
    :type provider: str
    :param token: Infura API endpoint token, defaults to ``4414fea5f7454211956b1627621450b4``.
    :type token: str

    :returns: Wallet -- Ethereum wallet instance.

    .. note::
        Ethereum has only three networks, ``mainnet``, ``ropsten``, ``kovan``, ``rinkeby`` and ``testnet``.
    """

    def __init__(self, network: str = config["network"],
                 provider: str = config["provider"], token: Optional[str] = None):
        super().__init__(cryptocurrency=EthereumMainnet)

        # Check parameter instances
        if not is_network(network=network):
            raise NetworkError(f"Invalid Ethereum '{network}' network",
                               "choose only 'mainnet', 'ropsten', 'kovan', 'rinkeby' or 'testnet' networks.")

        self._network, self._provider, self._token = network, provider, token
        self._hdwallet: HDWallet = HDWallet(
            cryptocurrency=EthereumMainnet, use_default_path=False
        )

    def from_entropy(self, entropy: str, language: str = "english", passphrase: Optional[str] = None) -> "Wallet":
        """
        Initialize wallet from entropy.

        :param entropy: Ethereum wallet entropy.
        :type entropy: str
        :param language: Ethereum wallet language, default to english.
        :type language: str
        :param passphrase: Ethereum wallet passphrase, default to None.
        :type passphrase: str

        :returns: Wallet -- Ethereum wallet instance.

        >>> from swap.providers.ethereum.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        <swap.providers.ethereum.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_entropy(entropy=entropy, language=language, passphrase=passphrase)
        return self

    def from_mnemonic(self, mnemonic: str, language: Optional[str] = None,
                      passphrase: Optional[str] = None) -> "Wallet":
        """
        Initialize wallet from mnemonic.

        :param mnemonic: Ethereum wallet mnemonic.
        :type mnemonic: str
        :param language: Ethereum wallet language, default to english.
        :type language: str
        :param passphrase: Ethereum wallet passphrase, default to None.
        :type passphrase: str

        :returns: Wallet -- Ethereum wallet instance.

        >>> from swap.providers.ethereum.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        <swap.providers.ethereum.wallet.Wallet object at 0x040DA268>
        """

        # Check parameter instances
        if not is_mnemonic(mnemonic=mnemonic, language=language):
            raise ValueError("Invalid Mnemonic words.")

        self._hdwallet.from_mnemonic(mnemonic=mnemonic, language=language, passphrase=passphrase)
        return self

    def from_seed(self, seed: str) -> "Wallet":
        """
        Initialize wallet from seed.

        :param seed: Ethereum wallet seed.
        :type seed: str

        :returns: Wallet -- Ethereum wallet instance.

        >>> from swap.providers.ethereum.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_seed("baff3e1fe60e1f2a2d840d304acc98d1818140c79354a353b400fb019bfb256bc392d7aa9047adff1f14bce0342e14605c6743a6c08e02150588375eb2eb7d49")
        <swap.providers.ethereum.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_seed(seed=seed)
        return self

    def from_root_xprivate_key(self, xprivate_key: str, strict: bool = True) -> "Wallet":
        """
        Initialize wallet from root xprivate key.

        :param xprivate_key: Ethereum wallet root xprivate key.
        :type xprivate_key: str
        :param strict: Strict for must be root xprivate key, default to ``True``.
        :type strict: bool

        :returns: Wallet -- Ethereum wallet instance.

        >>> from swap.providers.ethereum.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_root_xprivate_key("tprv8ZgxMBicQKsPeLxEBy2sJ8CqLdc76FUzeaiY5egrW4JdpM4F9b9A3L6AQhsY1TRsqJAfTdH7DdRAt5hRdcdhn5LnMZPiaGRR7Snrmd8CLqR")
        <swap.providers.ethereum.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_root_xprivate_key(xprivate_key=xprivate_key, strict=strict)
        return self

    def from_xprivate_key(self, xprivate_key: str) -> "Wallet":
        """
        Initialize wallet from xprivate key.

        :param xprivate_key: Ethereum wallet xprivate key.
        :type xprivate_key: str

        :returns: Wallet -- Ethereum wallet instance.

        >>> from swap.providers.ethereum.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_xprivate_key("tprv8kPCFydoWU9ybQunXq7g17Me57ac5gcj8RartGqetP4wAnoDHQAVnLY4RtbYE3WH6xBLHbBJ1VZcRutM712SRQkLFM2PCeoKfsPpndYUajZ")
        <swap.providers.ethereum.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_xprivate_key(xprivate_key=xprivate_key)
        return self

    def from_wif(self, wif: str) -> "Wallet":
        """
        Initialize wallet from wallet important format (WIF).

        :param wif: Ethereum wallet important format.
        :type wif: str

        :returns: Wallet -- Ethereum wallet instance.

        >>> from swap.providers.ethereum.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_wif("cTQpBvBAavuh6VzpeXiutLLTA5Uckr4eAJKuFsBMU1aQXBye1Z9n")
        <swap.providers.ethereum.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_wif(wif=wif)
        return self

    def from_private_key(self, private_key) -> "Wallet":
        """
        Initialize wallet from private key.

        :param private_key: Ethereum wallet private key.
        :type private_key: str

        :returns: Wallet -- Ethereum wallet instance.

        >>> from swap.providers.ethereum.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_private_key("adf0218f7e7276ed0f40b6919f2473497dd2bf7dcd4cabff4d4ef0e11948cde7")
        <swap.providers.ethereum.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_private_key(private_key=private_key)
        return self

    def from_path(self, path: str) -> "Wallet":
        """
        Drive Ethereum wallet from path.

        :param path: Ethereum wallet path.
        :type path: str

        :returns: Wallet -- Ethereum wallet instance.

        >>> from swap.providers.ethereum.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        <swap.providers.ethereum.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_path(path=path)
        return self

    def from_index(self, index: int, harden: bool = False) -> "Wallet":
        """
        Drive Ethereum wallet from index.

        :param index: Ethereum wallet index.
        :type index: int
        :param harden: Use harden, default to False.
        :type harden: bool

        :returns: Wallet -- Ethereum wallet instance.

        >>> from swap.providers.ethereum.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_index(44, harden=True)
        >>> wallet.from_index(0, harden=True)
        >>> wallet.from_index(0, harden=True)
        >>> wallet.from_index(0)
        >>> wallet.from_index(0)
        <swap.providers.ethereum.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_index(index=index, harden=harden)
        return self

    def clean_derivation(self) -> "Wallet":
        """
        Clean derivation Ethereum wallet.

        :returns: Wallet -- Ethereum wallet instance.

        >>> from swap.providers.ethereum.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.path()
        "m/44'/0'/0'/0/0"
        >>> wallet.clean_derivation()
        <swap.providers.ethereum.wallet.Wallet object at 0x040DA268>
        >>> wallet.path()
        None
        """

        self._hdwallet.clean_derivation()
        return self

    def strength(self) -> Optional[int]:
        """
        Get Ethereum wallet strength.

        :return: int -- Ethereum wallet strength.

        >>> from swap.providers.ethereum.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.strength()
        128
        """

        return self._hdwallet.strength()

    def entropy(self) -> Optional[str]:
        """
        Get Ethereum wallet entropy.

        :return: str -- Ethereum wallet entropy.

        >>> from swap.providers.ethereum.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.entropy()
        "72fee73846f2d1a5807dc8c953bf79f1"
        """

        return self._hdwallet.entropy()

    def mnemonic(self) -> Optional[str]:
        """
        Get Ethereum wallet mnemonic.

        :return: str -- Ethereum wallet mnemonic.

        >>> from swap.providers.ethereum.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.mnemonic()
        "indicate warm sock mistake code spot acid ribbon sing over taxi toast"
        """

        return self._hdwallet.mnemonic()

    def passphrase(self) -> Optional[str]:
        """
        Get Ethereum wallet passphrase.

        :return: str -- Ethereum wallet passphrase.

        >>> from swap.providers.ethereum.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1", passphrase="meherett")
        >>> wallet.passphrase()
        "meherett"
        """

        return self._hdwallet.passphrase()

    def language(self) -> Optional[str]:
        """
        Get Ethereum wallet language.

        :return: str -- Ethereum wallet language.

        >>> from swap.providers.ethereum.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.language()
        "english"
        """

        return self._hdwallet.language()

    def seed(self) -> Optional[str]:
        """
        Get Ethereum wallet seed.

        :return: str -- Ethereum wallet seed.

        >>> from swap.providers.ethereum.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.seed()
        "baff3e1fe60e1f2a2d840d304acc98d1818140c79354a353b400fb019bfb256bc392d7aa9047adff1f14bce0342e14605c6743a6c08e02150588375eb2eb7d49"
        """

        return self._hdwallet.seed()

    def root_xprivate_key(self, encoded: bool = True) -> Optional[str]:
        """
        Get Ethereum wallet root xprivate key.

        :param encoded: Encoded root xprivate key, default to True.
        :type encoded: bool

        :return: str -- Ethereum wallet root xprivate key.

        >>> from swap.providers.ethereum.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.root_xprivate_key()
        "tprv8ZgxMBicQKsPeLxEBy2sJ8CqLdc76FUzeaiY5egrW4JdpM4F9b9A3L6AQhsY1TRsqJAfTdH7DdRAt5hRdcdhn5LnMZPiaGRR7Snrmd8CLqR"
        """

        return self._hdwallet.root_xprivate_key(encoded=encoded)

    def root_xpublic_key(self, encoded: bool = True) -> Optional[str]:
        """
        Get Ethereum wallet root xpublic key.

        :param encoded: Encoded root xprivate key, default to True.
        :type encoded: bool

        :return: str -- Ethereum wallet root xpublic key.

        >>> from swap.providers.ethereum.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.root_xpublic_key()
        "tpubD6NzVbkrYhZ4Xoz25chThXrwuf83FafuDtKKNAj9vL72eqK1myxkDpi2aq9PKCbaQEbJZEaQBwiDQvYuMFZSWPNbypVJkNLfDHwvswpn4m4"
        """

        return self._hdwallet.root_xpublic_key(encoded=encoded)

    def xprivate_key(self, encoded=True) -> Optional[str]:
        """
        Get Ethereum wallet xprivate key.

        :param encoded: Encoded xprivate key, default to True.
        :type encoded: bool

        :return: str -- Ethereum wallet xprivate key.

        >>> from swap.providers.ethereum.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.xprivate_key()
        "tprv8kPCFydoWU9ybQunXq7g17Me57ac5gcj8RartGqetP4wAnoDHQAVnLY4RtbYE3WH6xBLHbBJ1VZcRutM712SRQkLFM2PCeoKfsPpndYUajZ"
        """

        return self._hdwallet.xprivate_key(encoded=encoded)

    def xpublic_key(self, encoded: bool = True) -> Optional[str]:
        """
        Get Ethereum wallet xpublic key.

        :param encoded: Encoded xprivate key, default to True.
        :type encoded: bool

        :return: str -- Ethereum wallet xpublic key.

        >>> from swap.providers.ethereum.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.xpublic_key()
        "tpubDH5EQPg3eqqeUswaRUnGQX1ke96YF1odhjBeAnsxJesL1H3yunz5xq9vbzGdsRqx3hnsMwZxn9icChmwC8W2gJEJR29iUaRBtCUbPrE7WXm"
        """

        return self._hdwallet.xpublic_key(encoded=encoded)

    def uncompressed(self) -> str:
        """
        Get Ethereum wallet uncompressed public key.

        :return: str -- Ethereum wallet uncompressed public key.

        >>> from swap.providers.ethereum.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.uncompressed()
        "065e8cb5fa76699079860a450bddd0e37e0ad3dbf2ddfd01d7b600231e6cde8ebc4241db8d66eb8085d5805bd2c4dd588ab3b6f9ec50c2ac3da4c557e15eca2e"
        """

        return self._hdwallet.uncompressed()

    def compressed(self) -> str:
        """
        Get Ethereum wallet compressed public key.

        :return: str -- Ethereum wallet compressed public key.

        >>> from swap.providers.ethereum.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.compressed()
        "02065e8cb5fa76699079860a450bddd0e37e0ad3dbf2ddfd01d7b600231e6cde8e"
        """

        return self._hdwallet.compressed()

    def chain_code(self) -> str:
        """
        Get Ethereum wallet chain code.

        :return: str -- Ethereum wallet chain code.

        >>> from swap.providers.ethereum.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.chain_code()
        "33a1c82cd13444724d0d217da8be96a8dcf663c8289ba870231c5f60e31accc5"
        """

        return self._hdwallet.chain_code()

    def private_key(self) -> str:
        """
        Get Ethereum wallet private key.

        :return: str -- Ethereum wallet private key.

        >>> from swap.providers.ethereum.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.private_key()
        "adf0218f7e7276ed0f40b6919f2473497dd2bf7dcd4cabff4d4ef0e11948cde7"
        """

        return self._hdwallet.private_key()

    def public_key(self) -> str:
        """
        Get Ethereum wallet public key.

        :return: str -- Ethereum wallet public key.

        >>> from swap.providers.ethereum.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.public_key()
        "02065e8cb5fa76699079860a450bddd0e37e0ad3dbf2ddfd01d7b600231e6cde8e"
        """

        return self._hdwallet.public_key()

    def path(self) -> Optional[str]:
        """
        Get Ethereum wallet path.

        :return: str -- Ethereum wallet path.

        >>> from swap.providers.ethereum.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.path()
        "m/44'/0'/0'/0/0"
        """

        return self._hdwallet.path()

    def address(self) -> str:
        """
        Get Ethereum wallet address.

        :return: str -- Ethereum wallet address.

        >>> from swap.providers.ethereum.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.address()
        "mkFWGt4hT11XS8dJKzzRFsTrqjjAwZfQAC"
        """

        return self._hdwallet.p2pkh_address()

    def wif(self) -> str:
        """
        Get Ethereum wallet important format (WIF).

        :return: str -- Ethereum wallet important format.

        >>> from swap.providers.ethereum.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.wif()
        "cTQpBvBAavuh6VzpeXiutLLTA5Uckr4eAJKuFsBMU1aQXBye1Z9n"
        """

        return self._hdwallet.wif()

    def hash(self, private_key: Optional[str] = None) -> str:
        """
        Get Ethereum wallet public key/address hash.

        :return: str -- Ethereum wallet public key/address hash.

        >>> from swap.providers.ethereum.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.hash()
        "33ecab3d67f0e2bde43e52f41ec1ecbdc73f11f8"
        """

        return self._hdwallet.hash(private_key=private_key)

    def balance(self, unit: str = config["unit"]) -> Union[Wei, int, float]:
        """
        Get Ethereum wallet balance.

        :param unit: Ethereum unit, default to ``Wei``.
        :type unit: str

        :return: Wei, int, float -- Ethereum wallet balance.

        >>> from swap.providers.ethereum.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44'/60'/0'/0/0")
        >>> wallet.balance(unit="Wei")
        67966
        """

        if unit not in ["Ether", "Gwei", "Wei"]:
            raise UnitError(f"Invalid Ethereum '{unit}' unit", "choose only 'Ether', 'Gwei' or 'Wei' units.")
        balance: int = get_balance(
            address=self.address(), network=self._network, provider=self._provider, token=self._token
        )
        return balance if unit == "Wei" else \
            amount_unit_converter(amount=balance, unit=f"Wei2{unit}")
