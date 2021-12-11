#!/usr/bin/env python3

from hdwallet import HDWallet
from hdwallet.cryptocurrencies import XinFinMainnet
from web3.types import Wei
from typing import (
    Optional, Union, Tuple
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
    get_balance, get_xrc20_balance
)

# Default derivation path
DEFAULT_PATH: str = config["path"]


class Wallet(HDWallet):
    """
    XinFin Wallet class.

    :param network: XinFin network, defaults to ``mainnet``.
    :type network: str
    :param provider: XinFin network provider, defaults to ``http``.
    :type provider: str

    :returns: Wallet -- XinFin wallet instance.

    .. note::
        XinFin has only two networks, ``mainnet``, ``apothem`` and ``testnet``.
    """

    def __init__(self, network: str = config["network"], provider: str = config["provider"]):
        super().__init__(cryptocurrency=XinFinMainnet)

        # Check parameter instances
        if not is_network(network=network):
            raise NetworkError(f"Invalid XinFin '{network}' network",
                               "choose only 'mainnet', 'apothem' or 'testnet' networks.")

        self._network, self._provider, = network, provider
        self._hdwallet: HDWallet = HDWallet(
            cryptocurrency=XinFinMainnet, use_default_path=False
        )

    def from_entropy(self, entropy: str, language: str = "english", passphrase: Optional[str] = None) -> "Wallet":
        """
        Master from Entropy.

        :param entropy: XinFin wallet entropy.
        :type entropy: str
        :param language: XinFin wallet language, default to ``english``.
        :type language: str
        :param passphrase: XinFin wallet passphrase, default to ``None``.
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
        Master from Mnemonic.

        :param mnemonic: XinFin wallet mnemonic.
        :type mnemonic: str
        :param language: XinFin wallet language, default to ``english``.
        :type language: str
        :param passphrase: XinFin wallet passphrase, default to ``None``.
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
        Master from Seed.

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

    def from_xprivate_key(self, xprivate_key: str, strict: bool = True) -> "Wallet":
        """
        Master from Root XPrivate Key.

        :param xprivate_key: XinFin root xprivate key.
        :type xprivate_key: str
        :param strict: Strict for must be root xprivate key, default to ``True``.
        :type strict: bool

        :returns: Wallet -- XinFin wallet instance.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_xprivate_key(xprivate_key="xprv9s21ZrQH143K3Y3pdbkbjreZQ9RVmqTLhRgf86uZyCJk2ou36YdUJt5frjwihGWmV1fQEDioiGZXWXUbHLy3kQf5xmhvhp8dZ2tfn6tgGUj")
        <swap.providers.xinfin.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_xprivate_key(xprivate_key=xprivate_key, strict=strict)
        return self

    def from_xpublic_key(self, xpublic_key: str, strict: bool = True) -> "Wallet":
        """
        Master from Root XPublic Key.

        :param xpublic_key: XinFin root xpublic key.
        :type xpublic_key: str
        :param strict: Strict for must be root xprivate key, default to ``True``.
        :type strict: bool

        :returns: Wallet -- XinFin wallet instance.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_xpublic_key(xpublic_key="xpub661MyMwAqRbcG28HjdHc6zbHxBFzBJBC4ecFvVKBXXqiucEBe5wirgQ9hzY2WQMjnurVjJbTjMWRskHi7jnSRkJdj4oRu4Vdh7Ln1F83mLJ")
        <swap.providers.xinfin.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_xpublic_key(xpublic_key=xpublic_key, strict=strict)
        return self

    def from_wif(self, wif: str) -> "Wallet":
        """
        Master from Wallet Important Format (WIF).

        :param wif: XinFin wallet important format.
        :type wif: str

        :returns: Wallet -- XinFin wallet instance.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_wif(wif="L1rYHjuxQtgTeU4qMUP6qnGqW9nstFt5drQktRuFGFSuGcCpZoJq")
        <swap.providers.xinfin.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_wif(wif=wif)
        return self

    def from_private_key(self, private_key) -> "Wallet":
        """
        Master from Private Key.

        :param private_key: XinFin private key.
        :type private_key: str

        :returns: Wallet -- XinFin wallet instance.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_private_key(private_key="8a4bc8131e99a5d1064cdbca6949aa2ec16152967b19f2cee3096daefd5ca857")
        <swap.providers.xinfin.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_private_key(private_key=private_key)
        return self

    def from_path(self, path: str) -> "Wallet":
        """
        Drive XinFin wallet from path.

        :param path: XinFin derivation path.
        :type path: str

        :returns: Wallet -- XinFin wallet instance.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path(path="m/44'/550'/0'/0/0")
        <swap.providers.xinfin.wallet.Wallet object at 0x040DA268>
        """

        self._hdwallet.from_path(path=path)
        return self

    def from_index(self, index: int, hardened: bool = False) -> "Wallet":
        """
        Drive XinFin wallet from index.

        :param index: XinFin derivation index.
        :type index: int
        :param hardened: Use hardened index, default to ``False``.
        :type hardened: bool

        :returns: Wallet -- XinFin wallet instance.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_index(44, harden=True)
        >>> wallet.from_index(550, harden=True)
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
        >>> wallet.from_path("m/44'/550'/0'/0/0")
        >>> wallet.path()
        "m/44'/550'/0'/0/0"
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

        :param encoded: Encoded root xprivate key, default to ``True``.
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

        :param encoded: Encoded root xprivate key, default to ``True``.
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
        >>> wallet.from_path(path="m/44'/550'/0'/0/0")
        >>> wallet.xprivate_key()
        "xprvA3QFrUVTkKpfRhqjgPq897uDFAYtt9VhMdDuZVbPboVf9uPMcMmr7W8sTsrd8nFCsVGSBCpGC3jreRpu8Zs1xsG5U98GZL24AqXYNPuo1rg"
        """

        return self._hdwallet.xprivate_key(encoded=encoded)

    def xpublic_key(self, encoded: bool = True) -> Optional[str]:
        """
        Get XinFin wallet xpublic key.

        :param encoded: Encoded xprivate key, default to ``True``.
        :type encoded: bool

        :return: str -- XinFin wallet xpublic key.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path(path="m/44'/550'/0'/0/0")
        >>> wallet.xpublic_key()
        "xpub6GPcFz2MahNxeBvCnRN8WFqwoCPPHcDYir9WMt11A92e2hiW9u66fJTMKAB81ns7kpAT3vsKi4QHWVSNt7V6crGXc8ie3yjn1GvD1inKxEw"
        """

        return self._hdwallet.xpublic_key(encoded=encoded)

    def uncompressed(self) -> str:
        """
        Get XinFin wallet uncompressed public key.

        :return: str -- XinFin wallet uncompressed public key.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path(path="m/44'/550'/0'/0/0")
        >>> wallet.uncompressed()
        "33fbc2f498d145a1827ee894a2ed5f14928523712047ad9fffc59cdda7d314e6707f731cc5b9a5018878fdfd503a8502c6d714a2cef1161603a002845b83310f"
        """

        return self._hdwallet.uncompressed()

    def compressed(self) -> str:
        """
        Get XinFin wallet compressed public key.

        :return: str -- XinFin wallet compressed public key.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path(path="m/44'/550'/0'/0/0")
        >>> wallet.compressed()
        "0333fbc2f498d145a1827ee894a2ed5f14928523712047ad9fffc59cdda7d314e6"
        """

        return self._hdwallet.compressed()

    def chain_code(self) -> str:
        """
        Get XinFin wallet chain code.

        :return: str -- XinFin wallet chain code.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path(path="m/44'/550'/0'/0/0")
        >>> wallet.chain_code()
        "ba8572f00241c17616903b07fed8ddcc1442677fa54ccd38e85049eee2310246"
        """

        return self._hdwallet.chain_code()

    def private_key(self) -> str:
        """
        Get XinFin wallet private key.

        :return: str -- XinFin wallet private key.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path(path="m/44'/550'/0'/0/0")
        >>> wallet.private_key()
        "8a4bc8131e99a5d1064cdbca6949aa2ec16152967b19f2cee3096daefd5ca857"
        """

        return self._hdwallet.private_key()

    def public_key(self) -> str:
        """
        Get XinFin wallet public key.

        :return: str -- XinFin wallet public key.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path("m/44'/550'/0'/0/0")
        >>> wallet.public_key()
        "0333fbc2f498d145a1827ee894a2ed5f14928523712047ad9fffc59cdda7d314e6"
        """

        return self._hdwallet.public_key()

    def path(self) -> Optional[str]:
        """
        Get XinFin wallet path.

        :return: str -- XinFin wallet path.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path(path="m/44'/550'/0'/0/0")
        >>> wallet.path()
        "m/44'/550'/0'/0/0"
        """

        return self._hdwallet.path()

    def address(self) -> str:
        """
        Get XinFin wallet address.

        :return: str -- XinFin wallet address.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path(path="m/44'/550'/0'/0/0")
        >>> wallet.address()
        "xdc2224caA2235DF8Da3D2016d2AB1137D2d548A232"
        """

        return self._hdwallet.p2pkh_address()

    def wif(self) -> str:
        """
        Get XinFin wallet important format (WIF).

        :return: str -- XinFin wallet important format.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path(path="m/44'/550'/0'/0/0")
        >>> wallet.wif()
        "L1rYHjuxQtgTeU4qMUP6qnGqW9nstFt5drQktRuFGFSuGcCpZoJq"
        """

        return self._hdwallet.wif()

    def hash(self, private_key: Optional[str] = None) -> str:
        """
        Get XinFin wallet public key/address hash.

        :return: str -- XinFin wallet public key/address hash.

        >>> from swap.providers.xinfin.wallet import Wallet
        >>> wallet: Wallet = Wallet(network="testnet")
        >>> wallet.from_entropy(entropy="ed0802d701a033776811601dd6c5c4a9")
        >>> wallet.from_path(path="m/44'/550'/0'/0/0")
        >>> wallet.hash()
        "dc8f505fccd7cb6f6ba93fd3795174f97efb43ae"
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
        >>> wallet.from_path(path="m/44'/550'/0'/0/0")
        >>> wallet.balance(unit="XDC")
        96.96263982
        """

        if unit not in ["XDC", "Gwei", "Wei"]:
            raise UnitError(f"Invalid XinFin '{unit}' unit", "choose only 'XDC', 'Gwei' or 'Wei' units.")
        balance: int = get_balance(
            address=self.address(), network=self._network, provider=self._provider
        )
        return balance if unit == "Wei" else \
            amount_unit_converter(amount=balance, unit_from=f"Wei2{unit}")

    def xrc20_balance(self, token_address: str) -> Tuple[int, str, str, int, str]:
        """
        Get XinFin HTLC XRC20 balance.

        :param token_address: XinFin XRC20 token address.
        :type token_address: str

        :return: tuple -- XinFin HTLC XRC20 balance and decimal.

        >>> from swap.providers.xinfin.htlc import HTLC
        >>> htlc: HTLC = HTLC(contract_address="0x94c4B5f13392AcD2A6E59C9A180758fB386631C3", network="testnet", erc20=True)
        >>> htlc.xrc20_balance(token_address="0xDaB6844e863bdfEE6AaFf888D2D34Bf1B7c37861")
        (99999999999999999999999999998, 18)
        """

        return get_xrc20_balance(address=self.address(), token_address=token_address, network=self._network)
