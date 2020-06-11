#!/usr/bin/env python3

from btcpy.structs.crypto import PublicKey, PrivateKey
from btcpy.structs.address import Address
from btcpy.structs.script import P2pkhScript, P2shScript
from cryptos import Bitcoin

import hashlib

from .utils import is_address
from .rpc import get_balance, get_unspent_transactions
from ...utils.exceptions import AddressError

# Public key
COMPRESSED = True


# Bitcoin Wallet.
class Wallet:
    """
    Bitcoin Wallet class.

    :param network: Bitcoin network, defaults to testnet.
    :type network: str
    :returns:  Wallet -- Bitcoin wallet instance.

    .. note::
        Bitcoin has only two networks, ``mainnet`` and ``testnet``.
    """

    # PyShuttle Bitcoin (BTC) wallet init.
    def __init__(self, network="testnet"):

        # Bitcoin network.
        self.network = network
        if self.network == "mainnet":
            self.mainnet = True
        elif self.network == "testnet":
            self.mainnet = False
        else:
            raise ValueError("invalid network, only mainnet or testnet")
        # Bitcoin wallet initialization.
        self.bitcoin = Bitcoin(testnet=(not self.mainnet))

        # Is compressed
        self.is_compressed = None
        # Main wallet init.
        self._private_key, self._public_key, self._address = None, None, None
        # Compressed and Uncompressed public key.
        self._compressed, self._uncompressed = None, None

    def from_private_key(self, private_key, compressed=COMPRESSED):
        """
        Initiate Bitcoin wallet from private key.

        :param private_key: Bitcoin wallet private key.
        :type private_key: str.
        :param compressed: Bitcoin public key compressed, default is True.
        :type compressed: bool
        :returns:  Wallet -- Bitcoin wallet instance.

        >>> from shuttle.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_private_key("92cbbc5990cb5090326a76feeb321cad01048635afe5756523bbf9f7a75bf38b")
        <shuttle.providers.bitcoin.wallet.Wallet object at 0x040DA268>
        """
        self.is_compressed = compressed
        self._private_key = PrivateKey.unhexlify(private_key)
        public_key = self.bitcoin.privtopub(self._private_key.hexlify())
        self._compressed = PublicKey.unhexlify(public_key).compressed.hex()
        self._uncompressed = PublicKey.unhexlify(public_key).uncompressed.hex()
        self._public_key = PublicKey.unhexlify(self._compressed) if self.is_compressed \
            else PublicKey.unhexlify(self._uncompressed)
        self._address = self._public_key.to_address(mainnet=self.mainnet)
        return self

    def from_passphrase(self, passphrase, compressed=COMPRESSED):
        """
        Initiate Bitcoin wallet from passphrase.

        :param passphrase: Bitcoin wallet passphrase.
        :type passphrase: str.
        :param compressed: Bitcoin public key compressed, default is True.
        :type compressed: bool
        :returns:  Wallet -- Bitcoin wallet instance.

        >>> from shuttle.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="mainnet")
        >>> wallet.from_passphrase("meherett")
        """
        self.is_compressed = compressed
        private_key = hashlib.sha256(passphrase.encode()).hexdigest()
        self._private_key = PrivateKey.unhexlify(private_key)
        public_key = self.bitcoin.privtopub(self._private_key.hexlify())
        self._compressed = PublicKey.unhexlify(public_key).compressed.hex()
        self._uncompressed = PublicKey.unhexlify(public_key).uncompressed.hex()
        self._public_key = PublicKey.unhexlify(self._compressed) if self.is_compressed \
            else PublicKey.unhexlify(self._uncompressed)
        self._address = self._public_key.to_address(mainnet=self.mainnet)
        return self

    def from_address(self, address):
        """
        Initiate Bitcoin wallet from address.

        :param address: Bitcoin wallet private key.
        :type address: str.
        :returns:  Wallet -- Bitcoin wallet instance.

        >>> from shuttle.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_address("mqLyrNDjpENRMZAoDpspH7kR9RtgvhWzYE")
        <shuttle.providers.bitcoin.wallet.Wallet object at 0x040DA268>
        """
        if not is_address(address=address, network=self.network):
            raise AddressError("invalid %s %s address" % (self.network, address))
        self._address = Address.from_string(address)
        return self

    # Bitcoin main private key.
    def private_key(self):
        """
        Get Bitcoin wallet private key.

        :returns: str -- Bitcoin private key.

        >>> from shuttle.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_passphrase("meherett")
        >>> wallet.private_key()
        "d4f5c55a45c004660b95ec833bb24569eba1559f214e90efa6e8d0b3afa14394"
        """
        return self._private_key.hexlify()

    # Bitcoin main public key.
    def public_key(self, private_key=None, compressed=COMPRESSED):
        """
        Get Bitcoin wallet public key.

        :param private_key: Bitcoin private key, default is None.
        :type private_key: str
        :param compressed: Bitcoin public key compressed, default is True.
        :type compressed: bool
        :return: str -- Bitcoin public key.

        >>> from shuttle.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_passphrase("meherett", compressed=False)
        >>> wallet.public_key()
        "04afa8301b068c2c184e0a3e77183dc95ec1130371c02ed172bec8f3bfbad6b17334244f64fe877d5e4839690c62b9d1f4095608f2ac29235e4b0299b6b96f6f35"
        """
        if private_key is None:
            return self._public_key.hexlify()
        public_key = self.bitcoin.privtopub(private_key)
        return PublicKey.unhexlify(public_key).compressed.hex() if compressed else \
            PublicKey.unhexlify(public_key).uncompressed.hex()

    # Compressed public key.
    def compressed(self, public_key=None):
        """
        Get Bitcoin wallet compressed public key.

        :param public_key: Bitcoin public key, default is None.
        :type public_key: str
        :return: str -- Bitcoin compressed public key.

        >>> from shuttle.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_passphrase("meherett")
        >>> wallet.compressed()
        "03afa8301b068c2c184e0a3e77183dc95ec1130371c02ed172bec8f3bfbad6b173"
        """
        if public_key is None:
            return self._compressed
        return PublicKey.unhexlify(public_key).compressed.hex()

    # Uncompressed public key.
    def uncompressed(self, public_key=None):
        """
        Get Bitcoin wallet uncompressed public key.

        :param public_key: Bitcoin public key, default is None.
        :type public_key: str
        :return: str -- Bitcoin uncompressed public key.

        >>> from shuttle.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_passphrase("meherett")
        >>> wallet.uncompressed()
        "04afa8301b068c2c184e0a3e77183dc95ec1130371c02ed172bec8f3bfbad6b17334244f64fe877d5e4839690c62b9d1f4095608f2ac29235e4b0299b6b96f6f35"
        """
        if public_key is None:
            return self._uncompressed
        return PublicKey.unhexlify(public_key).uncompressed.hex()

    # Bitcoin main _address.
    def address(self, public_key=None):
        """
        Get Bitcoin wallet address.

        :param public_key: Bitcoin address, default is None.
        :type public_key: str
        :return: str -- Bitcoin address.

        >>> from shuttle.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_passphrase("meherett")
        >>> wallet.address()
        "mm357rHaKqVmhEhFFwUhz6mRVAHkJaDTKt"
        """
        if public_key is None:
            return str(self._address)
        return str(PublicKey.unhexlify(public_key)
                   .to_address(mainnet=self.mainnet))

    # Bitcoin main _address hash.
    def hash(self, public_key=None):
        """
        Get Bitcoin wallet hash.

        :param public_key: Bitcoin hash, default is None.
        :type public_key: str
        :return: str -- Bitcoin hash.

        >>> from shuttle.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_passphrase("meherett")
        >>> wallet.hash()
        "3c8acde1c7cf370d970725f13eff03bf74b3fc61"
        """
        if public_key is None:
            return self._address.hash.hex()
        return PublicKey.unhexlify(public_key)\
            .to_address(mainnet=self.mainnet).hash.hex()

    # Bitcoin public to public key hash script.
    def p2pkh(self, address=None):
        """
        Get Bitcoin wallet p2pkh.

        :param address: Bitcoin p2pkh, default is None.
        :type address: str
        :return: str -- Bitcoin p2pkh.

        >>> from shuttle.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_passphrase("meherett")
        >>> wallet.p2pkh()
        "76a9143c8acde1c7cf370d970725f13eff03bf74b3fc6188ac"
        """
        if address is None:
            return P2pkhScript(self._address).hexlify()
        if not is_address(address=address, network=self.network):
            raise AddressError("invalid %s %s address" % (self.network, address))
        address = Address.from_string(address)
        return P2pkhScript(address).hexlify()

    # Bitcoin public to script hash script.
    def p2sh(self, address=None):
        """
        Get Bitcoin wallet p2sh.

        :param address: Bitcoin p2sh, default is None.
        :type address: str
        :return: str -- Bitcoin p2sh.

        >>> from shuttle.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_passphrase("meherett")
        >>> wallet.p2sh()
        "a914a3c4995d9cd0303e5f89ee1433212c797d04ee5d87"
        """
        if address is None:
            return P2shScript(P2pkhScript(self._address)).hexlify()
        if not is_address(address=address, network=self.network):
            raise AddressError("invalid %s %s address" % (self.network, address))
        address = Address.from_string(address)
        return P2shScript(P2pkhScript(address)).hexlify()

    # Bitcoin balance
    def balance(self, address=None, network="testnet"):
        """
        Get Bitcoin wallet balance.

        :param address: Bitcoin balance, default is None.
        :type address: str
        :param network: Bitcoin balance, default is testnet.
        :type network: str
        :return: int -- Bitcoin balance.

        >>> from shuttle.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_passphrase("meherett")
        >>> wallet.balance()
        1000000
        """
        if address is None:
            return get_balance(str(self._address), self.network)
        return get_balance(address, network)

    def unspent(self, address=None, network="testnet", limit=15):
        """
        Get Bitcoin wallet unspent transaction output.

        :param address: Bitcoin balance, default is None.
        :type address: str
        :param network: Bitcoin balance, default is testnet.
        :type network: str
        :param limit: Bitcoin balance, default is 15.
        :type limit: int
        :return: list -- Bitcoin unspent transaction outputs.

        >>> from shuttle.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet")
        >>> wallet.from_passphrase("meherett")
        >>> wallet.unspent()
        [{'index': 0, 'hash': 'be346626628199608926792d775381e54d8632c14b3ce702f90639481722392c', 'output_index': 1, 'amount': 12340, 'script': '76a9146bce65e58a50b97989930e9a4ff1ac1a77515ef188ac'}]
        """
        if address is None:
            address = str(self._address)
            network = str(self.network)
        unspent = list()
        if not is_address(address=address, network=network):
            raise AddressError("invalid %s %s address" % (network, address))
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
