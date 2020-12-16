#!/usr/bin/env python3

from btcpy.structs.crypto import PublicKey
from btcpy.structs.address import Address
from btcpy.structs.script import P2pkhScript
from hdwallet import HDWallet
from hdwallet.cryptocurrencies import (
    BitcoinMainnet, BitcoinTestnet
)
from typing import (
    Optional, Any, Union
)

from ...utils import is_mnemonic
from ...exceptions import (
    NetworkError, SymbolError
)
from ..config import bitcoin as config
from .utils import amount_converter
from .rpc import (
    get_balance, get_utxos
)

# Default path and indexes derivation
DEFAULT_PATH: str = config["path"]
DEFAULT_BIP44: str = config["BIP44"]


class Wallet(HDWallet):
    """
    Bitcoin Wallet class.

    :param network: Bitcoin network, defaults to mainnet.
    :type network: str

    :returns: Wallet -- Bitcoin wallet instance.

    .. note::
        Bitcoin has only two networks, ``mainnet`` and ``mainnet``.
    """

    def __init__(self, network: str = config["network"]):

        if network == "mainnet":
            self._network: str = "mainnet"
            self._cryptocurrency: Any = BitcoinMainnet
            self._hdwallet: HDWallet = HDWallet(cryptocurrency=BitcoinMainnet)
        elif network == "testnet":
            self._network: str = "testnet"
            self._cryptocurrency: Any = BitcoinTestnet
            self._hdwallet: HDWallet = HDWallet(cryptocurrency=BitcoinTestnet)
        else:
            raise NetworkError(f"Invalid Bitcoin '{network}' network",
                               "choose only 'mainnet' or 'testnet' networks.")
        super().__init__(cryptocurrency=self._cryptocurrency)

    def from_entropy(self, entropy: str, language: str = "english", passphrase: Optional[str] = None) -> "Wallet":
        """
        Initialize wallet from entropy.

        :param entropy: Bitcoin wallet entropy.
        :type entropy: str
        :param language: Bitcoin wallet language, default to english.
        :type language: str
        :param passphrase: Bitcoin wallet passphrase, default to None.
        :type passphrase: str

        :returns: Wallet -- Bitcoin wallet instance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        <swap.providers.bitcoin.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_entropy(entropy=entropy, language=language, passphrase=passphrase)
        return self

    def from_mnemonic(self, mnemonic: str, language: Optional[str] = None,
                      passphrase: Optional[str] = None) -> "Wallet":
        """
        Initialize wallet from mnemonic.

        :param mnemonic: Bitcoin wallet mnemonic.
        :type mnemonic: str
        :param language: Bitcoin wallet language, default to english.
        :type language: str
        :param passphrase: Bitcoin wallet passphrase, default to None.
        :type passphrase: str

        :returns: Wallet -- Bitcoin wallet instance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        <swap.providers.bitcoin.wallet.Wallet object at 0x040DA268>
        """

        # Check parameter instances
        if not is_mnemonic(mnemonic=mnemonic, language=language):
            raise ValueError("Invalid Mnemonic words.")

        self._hdwallet.from_mnemonic(mnemonic=mnemonic, language=language, passphrase=passphrase)
        return self

    def from_seed(self, seed: str) -> "Wallet":
        """
        Initialize wallet from seed.

        :param seed: Bitcoin wallet seed.
        :type seed: str

        :returns: Wallet -- Bitcoin wallet instance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_seed("baff3e1fe60e1f2a2d840d304acc98d1818140c79354a353b400fb019bfb256bc392d7aa9047adff1f14bce0342e14605c6743a6c08e02150588375eb2eb7d49")
        <swap.providers.bitcoin.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_seed(seed=seed)
        return self

    def from_root_xprivate_key(self, root_xprivate_key: str) -> "Wallet":
        """
        Initialize wallet from root xprivate key.

        :param root_xprivate_key: Bitcoin wallet root xprivate key.
        :type root_xprivate_key: str

        :returns: Wallet -- Bitcoin wallet instance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_root_xprivate_key("tprv8ZgxMBicQKsPeLxEBy2sJ8CqLdc76FUzeaiY5egrW4JdpM4F9b9A3L6AQhsY1TRsqJAfTdH7DdRAt5hRdcdhn5LnMZPiaGRR7Snrmd8CLqR")
        <swap.providers.bitcoin.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_root_xprivate_key(root_xprivate_key=root_xprivate_key)
        return self

    def from_xprivate_key(self, xprivate_key: str) -> "Wallet":
        """
        Initialize wallet from xprivate key.

        :param xprivate_key: Bitcoin wallet xprivate key.
        :type xprivate_key: str

        :returns: Wallet -- Bitcoin wallet instance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_xprivate_key("tprv8kPCFydoWU9ybQunXq7g17Me57ac5gcj8RartGqetP4wAnoDHQAVnLY4RtbYE3WH6xBLHbBJ1VZcRutM712SRQkLFM2PCeoKfsPpndYUajZ")
        <swap.providers.bitcoin.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_xprivate_key(xprivate_key=xprivate_key)
        return self

    def from_wif(self, wif: str) -> "Wallet":
        """
        Initialize wallet from wallet important format (WIF).

        :param wif: Bitcoin wallet important format.
        :type wif: str

        :returns: Wallet -- Bitcoin wallet instance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_wif("cTQpBvBAavuh6VzpeXiutLLTA5Uckr4eAJKuFsBMU1aQXBye1Z9n")
        <swap.providers.bitcoin.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_wif(wif=wif)
        return self

    def from_private_key(self, private_key) -> "Wallet":
        """
        Initialize wallet from private key.

        :param private_key: Bitcoin wallet private key.
        :type private_key: str

        :returns: Wallet -- Bitcoin wallet instance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_private_key("adf0218f7e7276ed0f40b6919f2473497dd2bf7dcd4cabff4d4ef0e11948cde7")
        <swap.providers.bitcoin.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_private_key(private_key=private_key)
        return self

    def from_path(self, path: str) -> "Wallet":
        """
        Drive Bitcoin wallet from path.

        :param path: Bitcoin wallet path.
        :type path: str

        :returns: Wallet -- Bitcoin wallet instance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        <swap.providers.bitcoin.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_path(path=path)
        return self

    def from_index(self, index: int, harden: bool = False) -> "Wallet":
        """
        Drive Bitcoin wallet from index.

        :param index: Bitcoin wallet index.
        :type index: int
        :param harden: Use harden, default to False.
        :type harden: bool

        :returns: Wallet -- Bitcoin wallet instance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_index(44, harden=True)
        >>> wallet.from_index(0, harden=True)
        >>> wallet.from_index(0, harden=True)
        >>> wallet.from_index(0)
        >>> wallet.from_index(0)
        <swap.providers.bitcoin.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_index(index=index, harden=harden)
        return self

    def clean_derivation(self) -> "Wallet":
        """
        Clean derivation Bitcoin wallet.

        :returns: Wallet -- Bitcoin wallet instance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.path()
        "m/44'/0'/0'/0/0"
        >>> wallet.clean_derivation()
        <swap.providers.bitcoin.wallet.Wallet object at 0x040DA268>
        >>> wallet.path()
        None
        """

        self._hdwallet.clean_derivation()
        return self

    def strength(self) -> Optional[int]:
        """
        Get Bitcoin wallet strength.

        :return: int -- Bitcoin wallet strength.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.strength()
        128
        """

        return self._hdwallet.strength()

    def entropy(self) -> Optional[str]:
        """
        Get Bitcoin wallet entropy.

        :return: str -- Bitcoin wallet entropy.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.entropy()
        "72fee73846f2d1a5807dc8c953bf79f1"
        """

        return self._hdwallet.entropy()

    def mnemonic(self) -> Optional[str]:
        """
        Get Bitcoin wallet mnemonic.

        :return: str -- Bitcoin wallet mnemonic.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.mnemonic()
        "indicate warm sock mistake code spot acid ribbon sing over taxi toast"
        """

        return self._hdwallet.mnemonic()

    def passphrase(self) -> Optional[str]:
        """
        Get Bitcoin wallet passphrase.

        :return: str -- Bitcoin wallet passphrase.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1", passphrase="meherett")
        >>> wallet.passphrase()
        "meherett"
        """

        return self._hdwallet.passphrase()

    def language(self) -> Optional[str]:
        """
        Get Bitcoin wallet language.

        :return: str -- Bitcoin wallet language.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.language()
        "english"
        """

        return self._hdwallet.language()

    def seed(self) -> Optional[str]:
        """
        Get Bitcoin wallet seed.

        :return: str -- Bitcoin wallet seed.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.seed()
        "baff3e1fe60e1f2a2d840d304acc98d1818140c79354a353b400fb019bfb256bc392d7aa9047adff1f14bce0342e14605c6743a6c08e02150588375eb2eb7d49"
        """

        return self._hdwallet.seed()

    def root_xprivate_key(self, encoded: bool = True) -> Optional[str]:
        """
        Get Bitcoin wallet root xprivate key.

        :param encoded: Encoded root xprivate key, default to True.
        :type encoded: bool

        :return: str -- Bitcoin wallet root xprivate key.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.root_xprivate_key()
        "tprv8ZgxMBicQKsPeLxEBy2sJ8CqLdc76FUzeaiY5egrW4JdpM4F9b9A3L6AQhsY1TRsqJAfTdH7DdRAt5hRdcdhn5LnMZPiaGRR7Snrmd8CLqR"
        """

        return self._hdwallet.root_xprivate_key(encoded=encoded)

    def root_xpublic_key(self, encoded: bool = True) -> Optional[str]:
        """
        Get Bitcoin wallet root xpublic key.

        :param encoded: Encoded root xprivate key, default to True.
        :type encoded: bool

        :return: str -- Bitcoin wallet root xpublic key.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.root_xpublic_key()
        "tpubD6NzVbkrYhZ4Xoz25chThXrwuf83FafuDtKKNAj9vL72eqK1myxkDpi2aq9PKCbaQEbJZEaQBwiDQvYuMFZSWPNbypVJkNLfDHwvswpn4m4"
        """

        return self._hdwallet.root_xpublic_key(encoded=encoded)

    def xprivate_key(self, encoded=True) -> Optional[str]:
        """
        Get Bitcoin wallet xprivate key.

        :param encoded: Encoded xprivate key, default to True.
        :type encoded: bool

        :return: str -- Bitcoin wallet xprivate key.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.xprivate_key()
        "tprv8kPCFydoWU9ybQunXq7g17Me57ac5gcj8RartGqetP4wAnoDHQAVnLY4RtbYE3WH6xBLHbBJ1VZcRutM712SRQkLFM2PCeoKfsPpndYUajZ"
        """

        return self._hdwallet.xprivate_key(encoded=encoded)

    def xpublic_key(self, encoded: bool = True) -> Optional[str]:
        """
        Get Bitcoin wallet xpublic key.

        :param encoded: Encoded xprivate key, default to True.
        :type encoded: bool

        :return: str -- Bitcoin wallet xpublic key.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.xpublic_key()
        "tpubDH5EQPg3eqqeUswaRUnGQX1ke96YF1odhjBeAnsxJesL1H3yunz5xq9vbzGdsRqx3hnsMwZxn9icChmwC8W2gJEJR29iUaRBtCUbPrE7WXm"
        """

        return self._hdwallet.xpublic_key(encoded=encoded)

    def uncompressed(self) -> str:
        """
        Get Bitcoin wallet uncompressed public key.

        :return: str -- Bitcoin wallet uncompressed public key.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.uncompressed()
        "065e8cb5fa76699079860a450bddd0e37e0ad3dbf2ddfd01d7b600231e6cde8ebc4241db8d66eb8085d5805bd2c4dd588ab3b6f9ec50c2ac3da4c557e15eca2e"
        """

        return self._hdwallet.uncompressed()

    def compressed(self) -> str:
        """
        Get Bitcoin wallet compressed public key.

        :return: str -- Bitcoin wallet compressed public key.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.compressed()
        "02065e8cb5fa76699079860a450bddd0e37e0ad3dbf2ddfd01d7b600231e6cde8e"
        """

        return self._hdwallet.compressed()

    def chain_code(self) -> str:
        """
        Get Bitcoin wallet chain code.

        :return: str -- Bitcoin wallet chain code.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.chain_code()
        "33a1c82cd13444724d0d217da8be96a8dcf663c8289ba870231c5f60e31accc5"
        """

        return self._hdwallet.chain_code()

    def private_key(self) -> str:
        """
        Get Bitcoin wallet private key.

        :return: str -- Bitcoin wallet private key.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.private_key()
        "adf0218f7e7276ed0f40b6919f2473497dd2bf7dcd4cabff4d4ef0e11948cde7"
        """

        return self._hdwallet.private_key()

    def public_key(self, private_key: str = None) -> str:
        """
        Get Bitcoin wallet public key.

        :return: str -- Bitcoin wallet public key.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.public_key()
        "02065e8cb5fa76699079860a450bddd0e37e0ad3dbf2ddfd01d7b600231e6cde8e"
        """

        return self._hdwallet.public_key(private_key=private_key)

    def path(self) -> Optional[str]:
        """
        Get Bitcoin wallet path.

        :return: str -- Bitcoin wallet path.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.path()
        "m/44'/0'/0'/0/0"
        """

        return self._hdwallet.path()

    def address(self) -> str:
        """
        Get Bitcoin wallet address.

        :return: str -- Bitcoin wallet address.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.address()
        "mkFWGt4hT11XS8dJKzzRFsTrqjjAwZfQAC"
        """

        return self._hdwallet.address()

    def wif(self) -> str:
        """
        Get Bitcoin wallet important format (WIF).

        :return: str -- Bitcoin wallet important format.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.wif()
        "cTQpBvBAavuh6VzpeXiutLLTA5Uckr4eAJKuFsBMU1aQXBye1Z9n"
        """

        return self._hdwallet.wif()

    def hash(self) -> str:
        """
        Get Bitcoin wallet public key/address hash.

        :return: str -- Bitcoin wallet public key/address hash.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.hash()
        "33ecab3d67f0e2bde43e52f41ec1ecbdc73f11f8"
        """

        return PublicKey.unhexlify(self.public_key()).to_address(
            mainnet=True if self._network == "mainnet" else False).hash.hex()

    def p2pkh(self) -> str:
        """
        Get Bitcoin wallet public key/address p2pkh.

        :return: str -- Bitcoin wallet public key/address p2pkh.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.p2pkh()
        "76a91433ecab3d67f0e2bde43e52f41ec1ecbdc73f11f888ac"
        """

        return P2pkhScript(Address.from_string(self.address())).hexlify()

    def balance(self, symbol: str = config["symbol"]) -> Union[int, float]:
        """
        Get Bitcoin wallet balance.

        :param symbol: Bitcoin symbol, default to SATOSHI.
        :type symbol: str

        :return: int, float -- Bitcoin wallet balance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.balance(symbol="SATOSHI")
        67966
        """

        if symbol not in ["BTC", "mBTC", "SATOSHI"]:
            raise SymbolError("Invalid Bitcoin symbol, choose only BTC, mBTC or SATOSHI symbols.")
        _balance: int = get_balance(address=self.address(), network=self._network)
        return _balance if symbol == "SATOSHI" else \
            amount_converter(amount=_balance, symbol=f"SATOSHI2{symbol}")

    def utxos(self, limit: int = 15) -> list:
        """
        Get Bitcoin wallet unspent transaction output (UTXO's).

        :param limit: Limit of UTXO's, default is 15.
        :type limit: int

        :return: list -- Bitcoin unspent transaction outputs.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("72fee73846f2d1a5807dc8c953bf79f1")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.utxos()
        [{'index': 0, 'hash': '98c6a3d4e136d32d0848126e08325c94da2e8217593e92236471b11b42ee7999', 'output_index': 1, 'amount': 67966, 'script': '76a91433ecab3d67f0e2bde43e52f41ec1ecbdc73f11f888ac'}]
        """

        utxos = list()
        _utxos = get_utxos(
            address=self.address(), network=self._network, limit=limit
        )
        for index, utxo in enumerate(_utxos):
            utxos.append(dict(
                index=index,
                hash=utxo["tx_hash"],
                output_index=utxo["tx_output_n"],
                amount=utxo["value"],
                script=utxo["script"]
            ))
        return utxos
