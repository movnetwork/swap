#!/usr/bin/env python3

from btcpy.structs.crypto import PublicKey
from btcpy.structs.address import Address
from btcpy.structs.script import P2pkhScript
from hdwallet import HDWallet
from hdwallet.cryptocurrencies import (
    BitcoinMainnet, BitcoinTestnet
)
from typing import TypeVar, Optional, Any

from .utils import is_address
from .rpc import get_balance, get_unspent_transactions
from ...utils.exceptions import AddressError, NetworkError
from ..config import bitcoin

# Bitcoin config
config = bitcoin()
# Var Wallet class
_Wallet = TypeVar("_Wallet", bound="Wallet")


class Wallet(HDWallet):
    """
    Bitcoin Wallet class.

    :param network: Bitcoin network, defaults to mainnet.
    :type network: str
    :returns: Wallet -- Bitcoin wallet instance.

    .. note::
        Bitcoin has only two networks, ``mainnet`` and ``mainnet``.
    """

    def __init__(self, network: str = config["mainnet"]):

        if network == "mainnet":
            self._network: str = "mainnet"
            self._cryptocurrency: Any = BitcoinMainnet
            self._hdwallet: HDWallet = HDWallet(cryptocurrency=BitcoinMainnet)
        elif network == "testnet":
            self._network: str = "testnet"
            self._cryptocurrency: Any = BitcoinTestnet
            self._hdwallet: HDWallet = HDWallet(cryptocurrency=BitcoinTestnet)
        else:
            raise NetworkError(f"Invalid '{network}' network",
                               "choose only 'mainnet' or 'testnet' networks.")
        super().__init__(cryptocurrency=self._cryptocurrency)

    def from_entropy(self, entropy: str, passphrase: str = None, language: str = "english") -> _Wallet:
        """
        Initialize wallet from entropy.

        :param entropy: Bitcoin wallet entropy.
        :type entropy: str
        :param passphrase: Bitcoin wallet passphrase, default to None.
        :type passphrase: str
        :param language: Bitcoin wallet language, default to english.
        :type language: str
        :returns: Wallet -- Bitcoin wallet instance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        <swap.providers.bitcoin.wallet.Wallet object at 0x040DA268>
        """
        self._hdwallet.from_entropy(entropy, passphrase, language)
        return self

    def from_mnemonic(self, mnemonic: str, passphrase: str = None, language: str = None) -> _Wallet:
        """
        Initialize wallet from mnemonic.

        :param mnemonic: Bitcoin wallet mnemonic.
        :type mnemonic: str
        :param passphrase: Bitcoin wallet passphrase, default to None.
        :type passphrase: str
        :param language: Bitcoin wallet language, default to english.
        :type language: str
        :returns: Wallet -- Bitcoin wallet instance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_mnemonic("extend length miss suit broken rescue around harbor vehicle vicious jelly quality")
        <swap.providers.bitcoin.wallet.Wallet object at 0x040DA268>
        """
        self._hdwallet.from_mnemonic(mnemonic, passphrase, language)
        return self

    def from_seed(self, seed: str) -> _Wallet:
        """
        Initialize wallet from seed.

        :param seed: Bitcoin wallet seed.
        :type seed: str
        :returns: Wallet -- Bitcoin wallet instance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_seed("51a0f6fb9abd5e5aa27f42dd375d8e4fc6944c704c859454e557fc419d3979e5a50273743c93e5035244adb09e9a37914abc583fdfae0da1ae2bedaa373f050e")
        <swap.providers.bitcoin.wallet.Wallet object at 0x040DA268>
        """
        self._hdwallet.from_seed(seed)
        return self

    def from_root_xprivate_key(self, root_xprivate_key: str) -> _Wallet:
        """
        Initialize wallet from root xprivate key.

        :param root_xprivate_key: Bitcoin wallet root xprivate key.
        :type root_xprivate_key: str
        :returns: Wallet -- Bitcoin wallet instance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_root_xprivate_key("xprv9s21ZrQH143K4QXLfi9Ht3fz7CciYxE2MuTdNxvDs8kRQRyPByvJLRSvfNBa3kh6twMksiJtZuyT2Cor7aLAAag3f7TPpnnjBADARWmrJmx")
        <swap.providers.bitcoin.wallet.Wallet object at 0x040DA268>
        """
        self._hdwallet.from_root_xprivate_key(root_xprivate_key)
        return self

    def from_xprivate_key(self, xprivate_key: str) -> _Wallet:
        """
        Initialize wallet from xprivate key.

        :param xprivate_key: Bitcoin wallet xprivate key.
        :type xprivate_key: str
        :returns: Wallet -- Bitcoin wallet instance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_xprivate_key("xprvA2WJkML27XMaNmtrsuVcvCCXTR5LiBKAwkV6LapBFmw7eGFkHHzVa57gPRjBToTnvr2PpkN4s1reiDW6Ay9yXxi8WaVskDXRwzZLxiPBQfL")
        <swap.providers.bitcoin.wallet.Wallet object at 0x040DA268>
        """
        self._hdwallet.from_xprivate_key(xprivate_key)
        return self

    def from_wif(self, wif: str) -> _Wallet:
        """
        Initialize wallet from wallet important format (WIF).

        :param wif: Bitcoin wallet important format.
        :type wif: str
        :returns: Wallet -- Bitcoin wallet instance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_wif("L4p5duRK9PZVP22rPLTZ8Zar77JQ1Pc6dz3Js5drL89wPRH1kz6R")
        <swap.providers.bitcoin.wallet.Wallet object at 0x040DA268>
        """
        self._hdwallet.from_wif(wif)
        return self

    def from_private_key(self, private_key) -> _Wallet:
        """
        Initialize wallet from private key.

        :param private_key: Bitcoin wallet private key.
        :type private_key: str
        :returns: Wallet -- Bitcoin wallet instance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_private_key("e28afe15f98501502fac7da75939d41a0c8d074aeb76d0131f5a5c5ce3132a79")
        <swap.providers.bitcoin.wallet.Wallet object at 0x040DA268>
        """
        self._hdwallet.from_private_key(private_key)
        return self

    def from_path(self, path: str) -> _Wallet:
        """
        Drive Bitcoin wallet from path.

        :param path: Bitcoin wallet path.
        :type path: str
        :returns: Wallet -- Bitcoin wallet instance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        <swap.providers.bitcoin.wallet.Wallet object at 0x040DA268>
        """
        self._hdwallet.from_path(path)
        return self

    def from_index(self, index: int, harden: bool = False) -> _Wallet:
        """
        Drive Bitcoin wallet from index.

        :param index: Bitcoin wallet index.
        :type index: int
        :param harden: Use harden, default to False.
        :type harden: bool
        :returns: Wallet -- Bitcoin wallet instance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.from_index(44, harden=True)
        >>> wallet.from_index(0, harden=True)
        >>> wallet.from_index(0, harden=True)
        >>> wallet.from_index(0)
        >>> wallet.from_index(0)
        <swap.providers.bitcoin.wallet.Wallet object at 0x040DA268>
        """
        self._hdwallet.from_index(index, harden)
        return self

    def clean_derivation(self) -> _Wallet:
        """
        Clean derivation Bitcoin wallet.

        :returns: Wallet -- Bitcoin wallet instance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
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

    def entropy(self) -> Optional[str]:
        """
        Get Bitcoin wallet entropy.

        :return: str -- Bitcoin wallet entropy.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.entropy()
        "50f002376c81c96e430b48f1fe71df57"
        """
        return self._hdwallet.entropy()

    def mnemonic(self) -> Optional[str]:
        """
        Get Bitcoin wallet mnemonic.

        :return: str -- Bitcoin wallet mnemonic.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.mnemonic()
        "extend length miss suit broken rescue around harbor vehicle vicious jelly quality"
        """
        return self._hdwallet.mnemonic()

    def passphrase(self) -> Optional[str]:
        """
        Get Bitcoin wallet passphrase.

        :return: str -- Bitcoin wallet passphrase.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57", passphrase="meherett")
        >>> wallet.passphrase()
        "meherett"
        """
        return self._hdwallet.passphrase()

    def language(self) -> Optional[str]:
        """
        Get Bitcoin wallet language.

        :return: str -- Bitcoin wallet language.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.language()
        "english"
        """
        return self._hdwallet.language()

    def seed(self) -> Optional[str]:
        """
        Get Bitcoin wallet seed.

        :return: str -- Bitcoin wallet seed.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.seed()
        "51a0f6fb9abd5e5aa27f42dd375d8e4fc6944c704c859454e557fc419d3979e5a50273743c93e5035244adb09e9a37914abc583fdfae0da1ae2bedaa373f050e"
        """
        return self._hdwallet.seed()

    def root_xprivate_key(self, encoded: bool = True) -> Optional[str]:
        """
        Get Bitcoin wallet root xprivate key.

        :param encoded: Encoded root xprivate key, default to True.
        :type encoded: bool
        :return: str -- Bitcoin wallet root xprivate key.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.root_xprivate_key()
        "xprv9s21ZrQH143K4QXLfi9Ht3fz7CciYxE2MuTdNxvDs8kRQRyPByvJLRSvfNBa3kh6twMksiJtZuyT2Cor7aLAAag3f7TPpnnjBADARWmrJmx"
        """
        return self._hdwallet.root_xprivate_key(encoded)

    def root_xpublic_key(self, encoded: bool = True) -> Optional[str]:
        """
        Get Bitcoin wallet root xpublic key.

        :param encoded: Encoded root xprivate key, default to True.
        :type encoded: bool
        :return: str -- Bitcoin wallet root xpublic key.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.root_xpublic_key()
        "xpub661MyMwAqRbcGtbomjgJFBcifETCxQwsj8PEBMKqRUHQHEJXjXEYtDmQWdoFYwDCpQWXhUt7Ce6D34r9gq7osUQR5RpUWSHjTWMCEHYZQ48"
        """
        return self._hdwallet.root_xpublic_key(encoded)

    def xprivate_key(self, encoded=True) -> Optional[str]:
        """
        Get Bitcoin wallet xprivate key.

        :param encoded: Encoded xprivate key, default to True.
        :type encoded: bool
        :return: str -- Bitcoin wallet xprivate key.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.xprivate_key()
        "xprvA2WJkML27XMaNmtrsuVcvCCXTR5LiBKAwkV6LapBFmw7eGFkHHzVa57gPRjBToTnvr2PpkN4s1reiDW6Ay9yXxi8WaVskDXRwzZLxiPBQfL"
        """
        return self._hdwallet.xprivate_key(encoded)

    def xpublic_key(self, encoded: bool = True) -> Optional[str]:
        """
        Get Bitcoin wallet xpublic key.

        :param encoded: Encoded xprivate key, default to True.
        :type encoded: bool
        :return: str -- Bitcoin wallet xpublic key.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.xpublic_key()
        "xpub6FVf9rruwtusbFyKyw2dHL9G1Suq7e32JyQh8yDnp7U6X4atpqJk7sSAEgfR45VFNs64tsRF67XnGFjuHER3SbTrzWEhzwkuAhKcHbpxb44"
        """
        return self._hdwallet.xpublic_key(encoded)

    def uncompressed(self) -> str:
        """
        Get Bitcoin wallet uncompressed public key.

        :return: str -- Bitcoin wallet uncompressed public key.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.uncompressed()
        "d5fb6799738d146d7558ac0b14c74cc66f879bd846231b64296fb7cc7c9d974fc6e73408a18811a99906fd10f6a8c1ec401f034ae49ca4a6e8c09275c5ae44b6"
        """
        return self._hdwallet.uncompressed()

    def compressed(self) -> str:
        """
        Get Bitcoin wallet compressed public key.

        :return: str -- Bitcoin wallet compressed public key.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.compressed()
        "02d5fb6799738d146d7558ac0b14c74cc66f879bd846231b64296fb7cc7c9d974f"
        """
        return self._hdwallet.compressed()

    def chain_code(self) -> str:
        """
        Get Bitcoin wallet chain code.

        :return: str -- Bitcoin wallet chain code.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.chain_code()
        "baa85729cc8400fd0321ec6df70e7f976a601b133c1aae91a5ec2638fa748017"
        """
        return self._hdwallet.chain_code()

    def private_key(self) -> str:
        """
        Get Bitcoin wallet private key.

        :return: str -- Bitcoin wallet private key.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.private_key()
        "e28afe15f98501502fac7da75939d41a0c8d074aeb76d0131f5a5c5ce3132a79"
        """
        return self._hdwallet.private_key()

    def public_key(self, private_key: str = None) -> str:
        """
        Get Bitcoin wallet public key.

        :return: str -- Bitcoin wallet public key.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.public_key()
        "02d5fb6799738d146d7558ac0b14c74cc66f879bd846231b64296fb7cc7c9d974f"
        """
        return self._hdwallet.public_key(private_key)

    def path(self) -> Optional[str]:
        """
        Get Bitcoin wallet path.

        :return: str -- Bitcoin wallet path.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
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
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.address()
        "18Ac1AiZuNU7ywC1qP6Ref3hGbdRM74Rxv"
        """
        return self._hdwallet.address()

    def wif(self) -> str:
        """
        Get Bitcoin wallet important format (WIF).

        :return: str -- Bitcoin wallet important format.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.wif()
        "L4p5duRK9PZVP22rPLTZ8Zar77JQ1Pc6dz3Js5drL89wPRH1kz6R"
        """
        return self._hdwallet.wif()

    def hash(self) -> str:
        """
        Get Bitcoin wallet public key/address hash.

        :return: str -- Bitcoin wallet public key/address hash.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.hash()
        "4e99d7d43ebb41a620426aa836dbd4c4fa85667e"
        """
        return PublicKey.unhexlify(self.public_key()).to_address(
            mainnet=True if self._network == "mainnet" else False).hash.hex()

    def p2pkh(self) -> str:
        """
        Get Bitcoin wallet public key/address p2pkh.

        :return: str -- Bitcoin wallet public key/address p2pkh.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.p2pkh()
        "76a9144e99d7d43ebb41a620426aa836dbd4c4fa85667e88ac"
        """
        return P2pkhScript(Address.from_string(self.address())).hexlify()

    def balance(self) -> int:
        """
        Get Bitcoin wallet balance.

        :return: int -- Bitcoin wallet balance.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.balance()
        1000000
        """
        return get_balance(self.address(), self._network)

    def unspent(self, address: str = None, network: str = config["network"], limit: int = 15) -> list:
        """
        Get Bitcoin wallet unspent transaction output.

        :param address: Bitcoin balance, default is None.
        :type address: str
        :param network: Bitcoin balance, default is mainnet.
        :type network: str
        :param limit: Bitcoin balance, default is 15.
        :type limit: int
        :return: list -- Bitcoin unspent transaction outputs.

        >>> from swap.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_entropy("50f002376c81c96e430b48f1fe71df57")
        >>> wallet.from_path("m/44'/0'/0'/0/0")
        >>> wallet.unspent()
        [{'index': 0, 'hash': 'be346626628199608926792d775381e54d8632c14b3ce702f90639481722392c', 'output_index': 1, 'amount': 12340, 'script': '76a9146bce65e58a50b97989930e9a4ff1ac1a77515ef188ac'}]
        """
        if address is None:
            address = str(self.address())
            network = str(self._network)
        unspent = list()
        if not is_address(address=address, network=network):
            raise AddressError(f"Invalid {network} '{address}' address")
        unspent_transactions = get_unspent_transactions(
            address, network, limit=limit)
        for index, unspent_transaction in enumerate(unspent_transactions):
            unspent.append(dict(
                index=index,
                hash=unspent_transaction["tx_hash"],
                output_index=unspent_transaction["tx_output_n"],
                amount=unspent_transaction["value"],
                script=unspent_transaction["script"]
            ))
        return unspent
