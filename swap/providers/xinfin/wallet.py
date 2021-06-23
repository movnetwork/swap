#!/usr/bin/env python3

from hdwallet import HDWallet
from hdwallet.cryptocurrencies import XinFinMainnet
from web3.types import Wei
from typing import (
    Optional, Union
)

from ...utils import is_mnemonic
from ...exceptions import (
    NetworkError, UnitError
)
from ..config import xinfin as config
from .utils import (
    is_network, amount_unit_converter
)
from .rpc import (
    get_balance
)

# Default derivation path
DEFAULT_PATH: str = config["path"]
# Default BIP44 derivation path
DEFAULT_BIP44_PATH: str = config["BIP44"]


class Wallet(HDWallet):
    """
    XinFin Wallet class.

    :param network: XinFin network, defaults to ``ropsten``.
    :type network: str
    :param provider: XinFin network provider, defaults to ``http``.
    :type provider: str
    :param token: Infura API endpoint token, defaults to ``4414fea5f7454211956b1627621450b4``.
    :type token: str

    :returns: Wallet -- XinFin wallet instance.

    .. note::
        XinFin has only two networks, ``mainnet`` and ``testnet``.
    """

    def __init__(self, network: str = config["network"],
                 provider: str = config["provider"], token: Optional[str] = None):
        super().__init__(cryptocurrency=XinFinMainnet)

        # Check parameter instances
        if not is_network(network=network):
            raise NetworkError(f"Invalid XinFin '{network}' network",
                               "choose only 'mainnet', 'ropsten', 'kovan', 'rinkeby' or 'testnet' networks.")

        self._network, self._provider, self._token = network, provider, token
        self._hdwallet: HDWallet = HDWallet(
            cryptocurrency=XinFinMainnet, use_default_path=False
        )

    def from_entropy(self, entropy: str, language: str = "english", passphrase: Optional[str] = None) -> "Wallet":
        """
        Initialize wallet from entropy.

        :param entropy: XinFin wallet entropy.
        :type entropy: str
        :param language: XinFin wallet language, default to english.
        :type language: str
        :param passphrase: XinFin wallet passphrase, default to None.
        :type passphrase: str

        :returns: Wallet -- XinFin wallet instance.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        <swap.providers.xinfin.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_entropy(entropy=entropy, language=language, passphrase=passphrase)
        return self

    def from_mnemonic(self, mnemonic: str, language: Optional[str] = None,
                      passphrase: Optional[str] = None) -> "Wallet":
        """
        Initialize wallet from mnemonic.

        :param mnemonic: XinFin wallet mnemonic.
        :type mnemonic: str
        :param language: XinFin wallet language, default to english.
        :type language: str
        :param passphrase: XinFin wallet passphrase, default to None.
        :type passphrase: str

        :returns: Wallet -- XinFin wallet instance.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_mnemonic(mnemonic="unfair divorce remind addict add roof park clown build renew illness fault")
        <swap.providers.xinfin.wallet.Wallet object at 0x040DA268>
        """

        # Check parameter instances
        if not is_mnemonic(mnemonic=mnemonic, language=language):
            raise ValueError("Invalid Mnemonic words.")

        self._hdwallet.from_mnemonic(mnemonic=mnemonic, language=language, passphrase=passphrase)
        return self

    def from_seed(self, seed: str) -> "Wallet":
        """
        Initialize wallet from seed.

        :param seed: XinFin wallet seed.
        :type seed: str

        :returns: Wallet -- XinFin wallet instance.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_seed(seed="1cfd5df8a523d53a36cee369a93fac4e9efab5e4e138d479da2fb6df730697574409d572fe8325ec22e8ed25dea7495f498c3f5235fe6ae6d47b989267b6777c")
        <swap.providers.xinfin.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_seed(seed=seed)
        return self

    def from_root_xprivate_key(self, xprivate_key: str, strict: bool = True) -> "Wallet":
        """
        Initialize wallet from root xprivate key.

        :param xprivate_key: XinFin wallet root xprivate key.
        :type xprivate_key: str
        :param strict: Strict for must be root xprivate key, default to ``True``.
        :type strict: bool

        :returns: Wallet -- XinFin wallet instance.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_root_xprivate_key(xprivate_key="xprv9s21ZrQH143K3Y3pdbkbjreZQ9RVmqTLhRgf86uZyCJk2ou36YdUJt5frjwihGWmV1fQEDioiGZXWXUbHLy3kQf5xmhvhp8dZ2tfn6tgGUj")
        <swap.providers.xinfin.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_root_xprivate_key(xprivate_key=xprivate_key, strict=strict)
        return self

    def from_xprivate_key(self, xprivate_key: str) -> "Wallet":
        """
        Initialize wallet from xprivate key.

        :param xprivate_key: XinFin wallet xprivate key.
        :type xprivate_key: str

        :returns: Wallet -- XinFin wallet instance.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_xprivate_key(xprivate_key="xprvA3xrxQQVw6Kvc786WAccK4H7dLHhnb9XRsMUMqU3bJoZf5bWxtd5VePTNnn854tEbvV57ggjqkGHXc2u4Jx2veJzXRS1mBuokqz1aXL6tDW")
        <swap.providers.xinfin.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_xprivate_key(xprivate_key=xprivate_key)
        return self

    def from_wif(self, wif: str) -> "Wallet":
        """
        Initialize wallet from wallet important format (WIF).

        :param wif: XinFin wallet important format.
        :type wif: str

        :returns: Wallet -- XinFin wallet instance.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_wif(wif="L4AfqFc8aoBWYNTKU6PkiFbP9kbXRfVHXZWde6SpAdTewwJMc5VZ")
        <swap.providers.xinfin.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_wif(wif=wif)
        return self

    def from_private_key(self, private_key) -> "Wallet":
        """
        Initialize wallet from private key.

        :param private_key: XinFin wallet private key.
        :type private_key: str

        :returns: Wallet -- XinFin wallet instance.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_private_key(private_key="cf4c2fb2b88a556c211d5fe79335dcee6dd11403bbbc5b47a530e9cf56ee3aee")
        <swap.providers.xinfin.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_private_key(private_key=private_key)
        return self

    def from_path(self, path: str) -> "Wallet":
        """
        Drive XinFin wallet from path.

        :param path: XinFin wallet path.
        :type path: str

        :returns: Wallet -- XinFin wallet instance.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path(path="m/44'/60'/0'/0/0")
        <swap.providers.xinfin.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_path(path=path)
        return self

    def from_index(self, index: int, hardened: bool = False) -> "Wallet":
        """
        Drive XinFin wallet from index.

        :param index: XinFin wallet index.
        :type index: int
        :param hardened: Use hardened index, default to False.
        :type hardened: bool

        :returns: Wallet -- XinFin wallet instance.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_index(44, harden=True)
        >>> wallet.from_index(60, harden=True)
        >>> wallet.from_index(0, harden=True)
        >>> wallet.from_index(0)
        >>> wallet.from_index(0)
        <swap.providers.xinfin.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_index(index=index, hardened=hardened)
        return self

    def clean_derivation(self) -> "Wallet":
        """
        Clean derivation XinFin wallet.

        :returns: Wallet -- XinFin wallet instance.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path("m/44'/60'/0'/0/0")
        >>> wallet.path()
        "m/44'/60'/0'/0/0"
        >>> wallet.clean_derivation()
        <swap.providers.xinfin.wallet.Wallet object at 0x040DA268>
        >>> wallet.path()
        None
        """

        self._hdwallet.clean_derivation()
        return self

    def strength(self) -> Optional[int]:
        """
        Get XinFin wallet strength.

        :return: int -- XinFin wallet strength.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.strength()
        128
        """

        return self._hdwallet.strength()

    def entropy(self) -> Optional[str]:
        """
        Get XinFin wallet entropy.

        :return: str -- XinFin wallet entropy.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.entropy()
        "ed0802d701a033776811601dd6c5c4a9"
        """

        return self._hdwallet.entropy()

    def mnemonic(self) -> Optional[str]:
        """
        Get XinFin wallet mnemonic.

        :return: str -- XinFin wallet mnemonic.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.mnemonic()
        "unfair divorce remind addict add roof park clown build renew illness fault"
        """

        return self._hdwallet.mnemonic()

    def passphrase(self) -> Optional[str]:
        """
        Get XinFin wallet passphrase.

        :return: str -- XinFin wallet passphrase.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9", passphrase="meherett")
        >>> wallet.passphrase()
        "meherett"
        """

        return self._hdwallet.passphrase()

    def language(self) -> Optional[str]:
        """
        Get XinFin wallet language.

        :return: str -- XinFin wallet language.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.language()
        "english"
        """

        return self._hdwallet.language()

    def seed(self) -> Optional[str]:
        """
        Get XinFin wallet seed.

        :return: str -- XinFin wallet seed.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.seed()
        "1cfd5df8a523d53a36cee369a93fac4e9efab5e4e138d479da2fb6df730697574409d572fe8325ec22e8ed25dea7495f498c3f5235fe6ae6d47b989267b6777c"
        """

        return self._hdwallet.seed()

    def root_xprivate_key(self, encoded: bool = True) -> Optional[str]:
        """
        Get XinFin wallet root xprivate key.

        :param encoded: Encoded root xprivate key, default to True.
        :type encoded: bool

        :return: str -- XinFin wallet root xprivate key.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.root_xprivate_key()
        "xprv9s21ZrQH143K3Y3pdbkbjreZQ9RVmqTLhRgf86uZyCJk2ou36YdUJt5frjwihGWmV1fQEDioiGZXWXUbHLy3kQf5xmhvhp8dZ2tfn6tgGUj"
        """

        return self._hdwallet.root_xprivate_key(encoded=encoded)

    def root_xpublic_key(self, encoded: bool = True) -> Optional[str]:
        """
        Get XinFin wallet root xpublic key.

        :param encoded: Encoded root xprivate key, default to True.
        :type encoded: bool

        :return: str -- XinFin wallet root xpublic key.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.root_xpublic_key()
        "xpub661MyMwAqRbcG28HjdHc6zbHxBFzBJBC4ecFvVKBXXqiucEBe5wirgQ9hzY2WQMjnurVjJbTjMWRskHi7jnSRkJdj4oRu4Vdh7Ln1F83mLJ"
        """

        return self._hdwallet.root_xpublic_key(encoded=encoded)

    def xprivate_key(self, encoded=True) -> Optional[str]:
        """
        Get XinFin wallet xprivate key.

        :param encoded: Encoded xprivate key, default to True.
        :type encoded: bool

        :return: str -- XinFin wallet xprivate key.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path(path="m/44'/60'/0'/0/0")
        >>> wallet.xprivate_key()
        "xprvA3xrxQQVw6Kvc786WAccK4H7dLHhnb9XRsMUMqU3bJoZf5bWxtd5VePTNnn854tEbvV57ggjqkGHXc2u4Jx2veJzXRS1mBuokqz1aXL6tDW"
        """

        return self._hdwallet.xprivate_key(encoded=encoded)

    def xpublic_key(self, encoded: bool = True) -> Optional[str]:
        """
        Get XinFin wallet xpublic key.

        :param encoded: Encoded xprivate key, default to True.
        :type encoded: bool

        :return: str -- XinFin wallet xpublic key.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path(path="m/44'/60'/0'/0/0")
        >>> wallet.xpublic_key()
        "xpub6GxDMuwPmTtDpbCZcC9cgCDrBN8CC3sNo6H5ADsf9eLYXsvfWRwL3ShwE5u4gxbPPcZj1yjSDrvvLxsHEPdjtFHHk81N2bskE2U7k9pmj9q"
        """

        return self._hdwallet.xpublic_key(encoded=encoded)

    def uncompressed(self) -> str:
        """
        Get XinFin wallet uncompressed public key.

        :return: str -- XinFin wallet uncompressed public key.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path(path="m/44'/60'/0'/0/0")
        >>> wallet.uncompressed()
        "e270f9d51cad2977c0a28182b9320bb5edc3c70e6d84ff5837f8d407ed9d676d447e195e1aff5494d1a0c8dc310c74692e053c2f27ab50c1ee7767a6b8a7be75"
        """

        return self._hdwallet.uncompressed()

    def compressed(self) -> str:
        """
        Get XinFin wallet compressed public key.

        :return: str -- XinFin wallet compressed public key.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path(path="m/44'/60'/0'/0/0")
        >>> wallet.compressed()
        "03e270f9d51cad2977c0a28182b9320bb5edc3c70e6d84ff5837f8d407ed9d676d"
        """

        return self._hdwallet.compressed()

    def chain_code(self) -> str:
        """
        Get XinFin wallet chain code.

        :return: str -- XinFin wallet chain code.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path(path="m/44'/60'/0'/0/0")
        >>> wallet.chain_code()
        "9e5c492fa0a5c5cc649922c34ac3468a08473f3b61f59bba61b52cce364d6b0c"
        """

        return self._hdwallet.chain_code()

    def private_key(self) -> str:
        """
        Get XinFin wallet private key.

        :return: str -- XinFin wallet private key.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path(path="m/44'/60'/0'/0/0")
        >>> wallet.private_key()
        "cf4c2fb2b88a556c211d5fe79335dcee6dd11403bbbc5b47a530e9cf56ee3aee"
        """

        return self._hdwallet.private_key()

    def public_key(self) -> str:
        """
        Get XinFin wallet public key.

        :return: str -- XinFin wallet public key.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path("m/44'/60'/0'/0/0")
        >>> wallet.public_key()
        "03e270f9d51cad2977c0a28182b9320bb5edc3c70e6d84ff5837f8d407ed9d676d"
        """

        return self._hdwallet.public_key()

    def path(self) -> Optional[str]:
        """
        Get XinFin wallet path.

        :return: str -- XinFin wallet path.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path(path="m/44'/60'/0'/0/0")
        >>> wallet.path()
        "m/44'/60'/0'/0/0"
        """

        return self._hdwallet.path()

    def address(self) -> str:
        """
        Get XinFin wallet address.

        :return: str -- XinFin wallet address.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path(path="m/44'/60'/0'/0/0")
        >>> wallet.address()
        "xdc69e04fe16c9A6A83076B3c2dc4b4Bc21b5d9A20C"
        """

        return self._hdwallet.p2pkh_address()

    def wif(self) -> str:
        """
        Get XinFin wallet important format (WIF).

        :return: str -- XinFin wallet important format.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path(path="m/44'/60'/0'/0/0")
        >>> wallet.wif()
        "L4AfqFc8aoBWYNTKU6PkiFbP9kbXRfVHXZWde6SpAdTewwJMc5VZ"
        """

        return self._hdwallet.wif()

    def hash(self, private_key: Optional[str] = None) -> str:
        """
        Get XinFin wallet public key/address hash.

        :return: str -- XinFin wallet public key/address hash.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path(path="m/44'/60'/0'/0/0")
        >>> wallet.hash()
        "184847379abdde6617e8438fd4ff0d8fdf512cc2"
        """

        return self._hdwallet.hash(private_key=private_key)

    def balance(self, unit: str = config["unit"]) -> Union[Wei, int, float]:
        """
        Get XinFin wallet balance.

        :param unit: XinFin unit, default to ``Wei``.
        :type unit: str

        :return: Wei, int, float -- XinFin wallet balance.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path(path="m/44'/60'/0'/0/0")
        >>> wallet.balance(unit="XDC")
        96.96263982
        """

        if unit not in ["XDC", "Gwei", "Wei"]:
            raise UnitError(f"Invalid XinFin '{unit}' unit", "choose only 'XDC', 'Gwei' or 'Wei' units.")
        balance: int = get_balance(
            address=self.address(), network=self._network, provider=self._provider
        )
        return balance if unit == "Wei" else \
            amount_unit_converter(amount=balance, unit=f"Wei2{unit}")
