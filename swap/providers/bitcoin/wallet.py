#!/usr/bin/env python3

from hdwallet import HDWallet
from hdwallet.cryptocurrencies import (
    BitcoinMainnet, BitcoinTestnet
)
from typing import (
    Optional, Any, Union
)

from ...utils import is_mnemonic
from ...exceptions import (
    NetworkError, UnitError
)
from ..config import bitcoin as config
from .utils import (
    is_network, amount_unit_converter
)
from .rpc import (
    get_balance, get_utxos
)

# Default derivation path
DEFAULT_PATH: str = config["path"]


class Wallet(HDWallet):
    """
    Bitcoin hierarchical deterministic wallet.

    :param network: Bitcoin network, defaults to ``mainnet``.
    :type network: str
    :param use_default_path: Use default derivation path, defaults to ``False``.
    :type use_default_path: bool

    :returns: Wallet -- Bitcoin instance.

    .. note::
        Bitcoin has only two networks, ``mainnet`` and ``mainnet``.
    """

    def __init__(self, network: str = config["network"], use_default_path: bool = False):

        # Check parameter instances
        if not is_network(network=network):
            raise NetworkError(f"Invalid Bitcoin '{network}' network",
                               "choose only 'mainnet' or 'testnet' networks.")

        self._network: str = network
        self._cryptocurrency: Any = (
            BitcoinMainnet if self._network == "mainnet" else BitcoinTestnet
        )
        self._hdwallet: HDWallet = HDWallet(
            cryptocurrency=self._cryptocurrency, use_default_path=use_default_path
        )

        super().__init__(cryptocurrency=self._cryptocurrency)

    def from_entropy(self, entropy: str, language: str = "english", passphrase: Optional[str] = None) -> "Wallet":
        """
        Initialize wallet from entropy.

        :param entropy: Bitcoin entropy.
        :type entropy: str
        :param language: Bitcoin language, default to english.
        :type language: str
        :param passphrase: Bitcoin passphrase, default to None.
        :type passphrase: str

        :returns: Wallet -- Bitcoin instance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        <swap.providers.bitcoin.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_entropy(entropy=entropy, language=language, passphrase=passphrase)
        return self

    def from_mnemonic(self, mnemonic: str, language: Optional[str] = None,
                      passphrase: Optional[str] = None) -> "Wallet":
        """
        Initialize wallet from mnemonic.

        :param mnemonic: Bitcoin mnemonic.
        :type mnemonic: str
        :param language: Bitcoin language, default to english.
        :type language: str
        :param passphrase: Bitcoin passphrase, default to None.
        :type passphrase: str

        :returns: Wallet -- Bitcoin instance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_mnemonic(mnemonic="unfair divorce remind addict add roof park clown build renew illness fault")
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

        :param seed: Bitcoin seed.
        :type seed: str

        :returns: Wallet -- Bitcoin instance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_seed(seed="1cfd5df8a523d53a36cee369a93fac4e9efab5e4e138d479da2fb6df730697574409d572fe8325ec22e8ed25dea7495f498c3f5235fe6ae6d47b989267b6777c")
        <swap.providers.bitcoin.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_seed(seed=seed)
        return self

    def from_root_xprivate_key(self, xprivate_key: str, strict: bool = True) -> "Wallet":
        """
        Master from Root XPrivate Key.

        :param xprivate_key: Bitcoin XPrivate key.
        :type xprivate_key: str
        :param strict: Strict for must be root xprivate key, default to ``True``.
        :type strict: bool

        :returns: Wallet -- Bitcoin instance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_xprivate_key(xprivate_key="tprv8ZgxMBicQKsPeMHMJAc6uWGYiGqi1MVM2ybmzXL2TAoDpQe85uyDpdT7mv7Nhdu5rTCBEKLZsd9KyP2LQZJzZTvgVQvENArgU8e6DoYBiXf")
        <swap.providers.bitcoin.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_root_xprivate_key(xprivate_key=xprivate_key, strict=strict)
        return self

    def from_root_xpublic_key(self, xpublic_key: str, strict: bool = True) -> "Wallet":
        """
        Master from Root XPublic Key.

        :param xpublic_key: Bitcoin XPublic key.
        :type xpublic_key: str
        :param strict: Strict for must be root xprivate key, default to ``True``.
        :type strict: bool

        :returns: Wallet -- Bitcoin instance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_root_xpublic_key(xpublic_key="tpubD6NzVbkrYhZ4XpK9BpGhJuvfHJMeAggFcHCZH3NKsSbcetttiJnp184yx2cp2uJyapPQLt7LGTLUZvnKWbdgKBkvnfYjab9sH4wBmEpTZhJ")
        <swap.providers.bitcoin.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_root_xpublic_key(xpublic_key=xpublic_key, strict=strict)
        return self

    def from_xprivate_key(self, xprivate_key: str) -> "Wallet":
        """
        Initialize wallet from root xprivate key.

        :param xprivate_key: Bitcoin root xprivate key.
        :type xprivate_key: str

        :returns: Wallet -- Bitcoin instance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_xprivate_key(xprivate_key="tprv8kqWVfMdSgo9WhUAxbmL6GNW4ivePvEZBu8QiiRfMXbVDgnHx16vndnAsv7Uds4iFvjMpdJiB6q6hhh753fRb89XFjHGjYJ8BsMZGv3RTKz")
        <swap.providers.bitcoin.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_xprivate_key(xprivate_key=xprivate_key)
        return self

    def from_xpublic_key(self, xpublic_key: str) -> "Wallet":
        """
        Initialize wallet from XPrivate key.

        :param xpublic_key: Bitcoin XPrivate key.
        :type xpublic_key: str

        :returns: Wallet -- Bitcoin instance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_xprivate_key(xprivate_key="tpubDHXYe5Psb4UpQAVxrFRvVg2cdkSaZFRTmCjC1ETxmoPt4B34aPvWy8Q343tUsTaCQCiSJVpzgyP1NQ3mffY7oF6u6cJ6Csx3AhgFFLVoUBu")
        <swap.providers.bitcoin.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_xpublic_key(xpublic_key=xpublic_key)
        return self

    def from_wif(self, wif: str) -> "Wallet":
        """
        Initialize wallet from wallet important format (WIF).

        :param wif: Bitcoin important format.
        :type wif: str

        :returns: Wallet -- Bitcoin instance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_wif(wif="cS6utJFQYTQEAY455hRQ5nardhCCoc2yf4M45P71ve5Dx44ag7qg")
        <swap.providers.bitcoin.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_wif(wif=wif)
        return self

    def from_private_key(self, private_key) -> "Wallet":
        """
        Initialize wallet from private key.

        :param private_key: Bitcoin private key.
        :type private_key: str

        :returns: Wallet -- Bitcoin instance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_private_key(private_key="86e4296c4b8804b952933ddf9b786a0bad1049c1d5b372e43f9336eb4ac2fcb6")
        <swap.providers.bitcoin.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_private_key(private_key=private_key)
        return self

    def from_path(self, path: str) -> "Wallet":
        """
        Drive Bitcoin from path.

        :param path: Bitcoin path.
        :type path: str

        :returns: Wallet -- Bitcoin instance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet", use_default_path=False)
        >>> wallet.from_entropy("ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path(path="m/44'/1'/0'/0/0")
        <swap.providers.bitcoin.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_path(path=path)
        return self

    def from_index(self, index: int, hardened: bool = False) -> "Wallet":
        """
        Drive Bitcoin from index.

        :param index: Bitcoin index.
        :type index: int
        :param hardened: Use harden, default to False.
        :type hardened: bool

        :returns: Wallet -- Bitcoin instance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet", use_default_path=False)
        >>> wallet.from_entropy("ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_index(index=44, hardened=True)
        >>> wallet.from_index(index=1, hardened=True)
        >>> wallet.from_index(index=0, hardened=True)
        >>> wallet.from_index(index=0)
        >>> wallet.from_index(index=0)
        <swap.providers.bitcoin.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_index(index=index, hardened=hardened)
        return self

    def clean_derivation(self) -> "Wallet":
        """
        Clean derivation Bitcoin.

        :returns: Wallet -- Bitcoin instance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path("m/44'/1'/0'/0/0")
        >>> wallet.path()
        "m/44'/1'/0'/0/0"
        >>> wallet.clean_derivation()
        <swap.providers.bitcoin.wallet.Wallet object at 0x040DA268>
        >>> wallet.path()
        None
        """

        self._hdwallet.clean_derivation()
        return self

    def strength(self) -> Optional[int]:
        """
        Get Bitcoin strength.

        :return: int -- Bitcoin strength.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.strength()
        128
        """

        return self._hdwallet.strength()

    def entropy(self) -> Optional[str]:
        """
        Get Bitcoin entropy.

        :return: str -- Bitcoin entropy.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_mnemonic(mnemonic="unfair divorce remind addict add roof park clown build renew illness fault")
        >>> wallet.entropy()
        "ed0802d701a033776811601dd6c5c4a9"
        """

        return self._hdwallet.entropy()

    def mnemonic(self) -> Optional[str]:
        """
        Get Bitcoin mnemonic.

        :return: str -- Bitcoin mnemonic.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.mnemonic()
        "unfair divorce remind addict add roof park clown build renew illness fault"
        """

        return self._hdwallet.mnemonic()

    def passphrase(self) -> Optional[str]:
        """
        Get Bitcoin passphrase.

        :return: str -- Bitcoin passphrase.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("ed0802d701a033776811601dd6c5c4a9", passphrase="meherett")
        >>> wallet.passphrase()
        "meherett"
        """

        return self._hdwallet.passphrase()

    def language(self) -> Optional[str]:
        """
        Get Bitcoin language.

        :return: str -- Bitcoin language.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.language()
        "english"
        """

        return self._hdwallet.language()

    def seed(self) -> Optional[str]:
        """
        Get Bitcoin seed.

        :return: str -- Bitcoin seed.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.seed()
        "1cfd5df8a523d53a36cee369a93fac4e9efab5e4e138d479da2fb6df730697574409d572fe8325ec22e8ed25dea7495f498c3f5235fe6ae6d47b989267b6777c"
        """

        return self._hdwallet.seed()

    def root_xprivate_key(self, encoded: bool = True) -> Optional[str]:
        """
        Get Bitcoin root xprivate key.

        :param encoded: Encoded root xprivate key, default to True.
        :type encoded: bool

        :return: str -- Bitcoin root xprivate key.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.root_xprivate_key()
        "tprv8ZgxMBicQKsPeMHMJAc6uWGYiGqi1MVM2ybmzXL2TAoDpQe85uyDpdT7mv7Nhdu5rTCBEKLZsd9KyP2LQZJzZTvgVQvENArgU8e6DoYBiXf"
        """

        return self._hdwallet.root_xprivate_key(encoded=encoded)

    def root_xpublic_key(self, encoded: bool = True) -> Optional[str]:
        """
        Get Bitcoin root xpublic key.

        :param encoded: Encoded root xpublic key, default to True.
        :type encoded: bool

        :return: str -- Bitcoin root xpublic key.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.root_xpublic_key()
        "tpubD6NzVbkrYhZ4XpK9BpGhJuvfHJMeAggFcHCZH3NKsSbcetttiJnp184yx2cp2uJyapPQLt7LGTLUZvnKWbdgKBkvnfYjab9sH4wBmEpTZhJ"
        """

        return self._hdwallet.root_xpublic_key(encoded=encoded)

    def xprivate_key(self, encoded: bool = True) -> Optional[str]:
        """
        Get Bitcoin root xprivate key.

        :param encoded: Encoded root xprivate key, default to True.
        :type encoded: bool

        :return: str -- Bitcoin root xprivate key.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path("m/44'/1'/0'/0/0")
        >>> wallet.xprivate_key()
        "tprv8kqWVfMdSgo9WhUAxbmL6GNW4ivePvEZBu8QiiRfMXbVDgnHx16vndnAsv7Uds4iFvjMpdJiB6q6hhh753fRb89XFjHGjYJ8BsMZGv3RTKz"
        """

        return self._hdwallet.xprivate_key(encoded=encoded)

    def xpublic_key(self, encoded: bool = True) -> Optional[str]:
        """
        Get Bitcoin xpublic key.

        :param encoded: Encoded xprivate key, default to True.
        :type encoded: bool

        :return: str -- Bitcoin xpublic key.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path("m/44'/1'/0'/0/0")
        >>> wallet.xpublic_key()
        "tpubDHXYe5Psb4UpQAVxrFRvVg2cdkSaZFRTmCjC1ETxmoPt4B34aPvWy8Q343tUsTaCQCiSJVpzgyP1NQ3mffY7oF6u6cJ6Csx3AhgFFLVoUBu"
        """

        return self._hdwallet.xpublic_key(encoded=encoded)

    def uncompressed(self, compressed: Optional[str] = None) -> str:
        """
        Get Bitcoin Uncompressed public key.

        :param compressed: Compressed public key, default to ``None``.
        :type compressed: str

        :return: str -- Bitcoin Uncompressed public key.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path("m/44'/1'/0'/0/0")
        >>> wallet.uncompressed()
        "f4206f9c6d35f50b3b05edc13118ab64d27959d0b7412638bfea5d132b3fb36c6d9515384318aab7fc4d15d5a1ed7999c12ae6b9d1fe11979309630d201ba632"
        """

        return self._hdwallet.uncompressed(compressed=compressed)

    def compressed(self, uncompressed: Optional[str] = None) -> str:
        """
        Get Bitcoin Compressed public key.
        
        :param uncompressed: Uncompressed public key, default to ``None``.
        :type uncompressed: str

        :return: str -- Bitcoin Compressed public key.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path("m/44'/1'/0'/0/0")
        >>> wallet.compressed()
        "02f4206f9c6d35f50b3b05edc13118ab64d27959d0b7412638bfea5d132b3fb36c"
        """

        return self._hdwallet.compressed(uncompressed=uncompressed)

    def chain_code(self) -> str:
        """
        Get Bitcoin chain code.

        :return: str -- Bitcoin chain code.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path("m/44'/1'/0'/0/0")
        >>> wallet.chain_code()
        "cbe00345c4cfa83dc315e52b1d5acaf2c6fce1bc8760f02696c05c3a94171304"
        """

        return self._hdwallet.chain_code()

    def private_key(self) -> str:
        """
        Get Bitcoin private key.

        :return: str -- Bitcoin private key.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path("m/44'/1'/0'/0/0")
        >>> wallet.private_key()
        "86e4296c4b8804b952933ddf9b786a0bad1049c1d5b372e43f9336eb4ac2fcb6"
        """

        return self._hdwallet.private_key()

    def public_key(self,  compressed: bool = True, private_key: str = None) -> str:
        """
        Get Bitcoin Public key.

        :param compressed: Compressed public key, default to ``True``.
        :type compressed: bool
        :param private_key: Private key hex string, default to ``None``.
        :type private_key: str

        :return: str -- Bitcoin public key.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path("m/44'/1'/0'/0/0")
        >>> wallet.public_key()
        "02f4206f9c6d35f50b3b05edc13118ab64d27959d0b7412638bfea5d132b3fb36c"
        """

        return self._hdwallet.public_key(compressed=compressed, private_key=private_key)

    def path(self) -> Optional[str]:
        """
        Get Bitcoin path.

        :return: str -- Bitcoin path.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path("m/44'/1'/0'/0/0")
        >>> wallet.path()
        "m/44'/1'/0'/0/0"
        """

        return self._hdwallet.path()

    def wif(self) -> str:
        """
        Get Bitcoin important format (WIF).

        :return: str -- Bitcoin important format.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path("m/44'/1'/0'/0/0")
        >>> wallet.wif()
        "cS6utJFQYTQEAY455hRQ5nardhCCoc2yf4M45P71ve5Dx44ag7qg"
        """

        return self._hdwallet.wif()

    def hash(self, private_key: Optional[str] = None) -> str:
        """
        Get Bitcoin public key/address hash.

        :return: str -- Bitcoin public key/address hash.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path("m/44'/1'/0'/0/0")
        >>> wallet.hash()
        "e00ff2a640b7ce2d336860739169487a57f84b15"
        """

        return self._hdwallet.hash(private_key=private_key)

    def address(self) -> str:
        """
        Get Bitcoin address.

        :return: str -- Bitcoin address.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path("m/44'/1'/0'/0/0")
        >>> wallet.address()
        "n1wgm6kkzMcNfAtJmes8YhpvtDzdNhDY5a"
        """

        return self._hdwallet.p2pkh_address()

    def balance(self, unit: str = config["unit"]) -> Union[int, float]:
        """
        Get Bitcoin balance.

        :param unit: Bitcoin unit, default to Satoshi.
        :type unit: str

        :return: int, float -- Bitcoin balance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path("m/44'/1'/0'/0/0")
        >>> wallet.balance(unit="BTC")
        0.2
        """

        if unit not in ["BTC", "mBTC", "Satoshi"]:
            raise UnitError("Invalid Bitcoin unit, choose only BTC, mBTC or Satoshi units.")
        _balance: int = get_balance(address=self.address(), network=self._network)
        return _balance if unit == "Satoshi" else \
            amount_unit_converter(amount=_balance, unit_from=f"Satoshi2{unit}")

    def utxos(self, limit: int = 15) -> list:
        """
        Get Bitcoin unspent transaction output (UTXO's).

        :param limit: Limit of UTXO's, default is 15.
        :type limit: int

        :return: list -- Bitcoin unspent transaction outputs.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy("ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path("m/44'/1'/0'/0/0")
        >>> wallet.utxos()
        [{'index': 0, 'hash': '9d60a8b4dd16d4bf02835a21a3e9154e636ba06ad55368f36114eb7e930b35e8', 'output_index': 1, 'amount': 100000, 'script': '76a914e00ff2a640b7ce2d336860739169487a57f84b1588ac'}, {'index': 1, 'hash': '77ecb5ffe0f85454183bcab0cf1e15bfc62dc86cbdeaf374224ba03cb5cd7d29', 'output_index': 0, 'amount': 10000, 'script': '76a914e00ff2a640b7ce2d336860739169487a57f84b1588ac'}, {'index': 2, 'hash': 'e3ed50900a06990c123f3e87187009ce124cb65a46cd45eba5773fb0979fce43', 'output_index': 0, 'amount': 1797372, 'script': '76a914e00ff2a640b7ce2d336860739169487a57f84b1588ac'}]
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
