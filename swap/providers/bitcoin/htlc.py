#!/usr/bin/env python3

from btcpy.structs.script import (
    Script, ScriptBuilder, P2shScript, IfElseScript, Hashlock256Script, RelativeTimelockScript
)
from btcpy.structs.transaction import Sequence
from typing import (
    Optional, Union
)
from binascii import unhexlify

import hashlib

from ...exceptions import (
    AddressError, NetworkError, UnitError
)
from ..config import bitcoin as config
from .rpc import (
    get_balance, get_utxos
)
from .utils import (
    get_address_hash, is_address, is_network, amount_unit_converter
)


class HTLC:
    """
    Bitcoin Hash Time Lock Contract (HTLC).

    :param network: Bitcoin network, defaults to mainnet.
    :type network: str

    :returns: HTLC -- Bitcoin HTLC instance.

    .. note::
        Bitcoin has only two networks, ``mainnet`` and ``testnet``.
    """

    def __init__(self, network: str = config["network"]):

        if not is_network(network=network):
            raise NetworkError(f"Invalid Bitcoin '{network}' network",
                               "choose only 'mainnet' or 'testnet' networks.")
        self._network: str = network
        self._script: Optional[IfElseScript, ScriptBuilder] = None

    @property
    def script(self) -> Union[IfElseScript, ScriptBuilder]:
        return self._script

    def build_htlc(self, secret_hash: str, recipient_address: str,
                   sender_address: str, sequence: int = config["sequence"]) -> "HTLC":
        """
        Build Bitcoin Hash Time Lock Contract (HTLC).

        :param secret_hash: secret sha-256 hash.
        :type secret_hash: str
        :param recipient_address: Bitcoin recipient address.
        :type recipient_address: str
        :param sender_address: Bitcoin sender address.
        :type sender_address: str
        :param sequence: Bitcoin sequence number of expiration block, defaults to 1000.
        :type sequence: int

        :returns: HTLC -- Bitcoin Hash Time Lock Contract (HTLC) instance.

        >>> from swap.providers.bitcoin.htlc import HTLC
        >>> from swap.utils import sha256
        >>> htlc = HTLC(network="testnet")
        >>> htlc.build_htlc(secret_hash=sha256("Hello Meheret!"), recipient_address="mgokpSJoX7npmAK1Zj8ze1926CLxYDt1iF", sender_address="mkFWGt4hT11XS8dJKzzRFsTrqjjAwZfQAC", sequence=1000)
        <swap.providers.bitcoin.htlc.HTLC object at 0x0409DAF0>
        """

        # Check parameter instances
        if len(secret_hash) != 64:
            raise ValueError("Invalid secret hash, length must be 64.")
        if not is_address(address=recipient_address, network=self._network):
            raise AddressError(f"Invalid Bitcoin recipient '{recipient_address}' {self._network} address.")
        if not is_address(address=sender_address, network=self._network):
            raise AddressError(f"Invalid Bitcoin sender '{sender_address}' {self._network} address.")

        self._script = IfElseScript(
            Hashlock256Script(
                hashlib.sha256(unhexlify(secret_hash)).digest(),
                get_address_hash(
                    address=recipient_address, script=True
                )
            ),
            RelativeTimelockScript(
                Sequence(sequence),
                get_address_hash(
                    address=sender_address, script=True
                )
            )
        )
        return self

    def from_opcode(self, opcode: str) -> "HTLC":
        """
        Initiate Bitcoin Hash Time Lock Contract (HTLC) from opcode script.

        :param opcode: Bitcoin opcode script.
        :type opcode: str

        :returns: HTLC -- Bitcoin Hash Time Lock Contract (HTLC) instance.

        >>> from swap.providers.bitcoin.htlc import HTLC
        >>> htlc = HTLC(network="testnet")
        >>> opcode = "OP_IF OP_HASH256 821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e0158 OP_EQUALVERIFY OP_DUP OP_HASH160 0e259e08f2ec9fc99a92b6f66fdfcb3c7914fd68 OP_EQUALVERIFY OP_CHECKSIG OP_ELSE e803 OP_CHECKSEQUENCEVERIFY OP_DROP OP_DUP OP_HASH160 33ecab3d67f0e2bde43e52f41ec1ecbdc73f11f8 OP_EQUALVERIFY OP_CHECKSIG OP_ENDIF" 
        >>> htlc.from_opcode(opcode=opcode)
        <swap.providers.bitcoin.htlc.HTLC object at 0x0409DAF0>
        """

        bytecode = Script.compile(opcode)
        self._script = ScriptBuilder.identify(bytecode)
        return self

    def from_bytecode(self, bytecode: str) -> "HTLC":
        """
        Initialize Bitcoin Hash Time Lock Contract (HTLC) from bytecode.

        :param bytecode: Bitcoin bytecode.
        :type bytecode: str

        :returns: HTLC -- Bitcoin Hash Time Lock Contract (HTLC) instance.

        >>> from swap.providers.bitcoin.htlc import HTLC
        >>> htlc = HTLC(network="testnet")
        >>> bytecode = "63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a9140e259e08f2ec9fc99a92b6f66fdfcb3c7914fd6888ac6702e803b27576a91433ecab3d67f0e2bde43e52f41ec1ecbdc73f11f888ac68"
        >>> htlc.from_bytecode(bytecode=bytecode)
        <swap.providers.bitcoin.htlc.HTLC object at 0x0409DAF0>
        """

        self._script = ScriptBuilder.identify(bytecode)
        return self

    def bytecode(self) -> str:
        """
        Get Bitcoin Hash Time Lock Contract (HTLC) bytecode.

        :returns: str -- Bitcoin HTLC bytecode.

        >>> from swap.providers.bitcoin.htlc import HTLC
        >>> from swap.utils import sha256
        >>> htlc = HTLC(network="testnet")
        >>> htlc.build_htlc(sha256("Hello Meheret!"), "mgokpSJoX7npmAK1Zj8ze1926CLxYDt1iF", "mkFWGt4hT11XS8dJKzzRFsTrqjjAwZfQAC", 1000)
        >>> htlc.bytecode()
        "63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a9140e259e08f2ec9fc99a92b6f66fdfcb3c7914fd6888ac6702e803b27576a91433ecab3d67f0e2bde43e52f41ec1ecbdc73f11f888ac68"
        """

        if self._script is None:
            raise ValueError("HTLC script is None, first build HTLC.")
        return self._script.hexlify()

    def opcode(self) -> str:
        """
        Get Bitcoin Hash Time Lock Contract (HTLC) OP_Code.

        :returns: str -- Bitcoin HTLC opcode.

        >>> from swap.providers.bitcoin.htlc import HTLC
        >>> from swap.utils import sha256
        >>> htlc = HTLC(network="testnet")
        >>> htlc.build_htlc(sha256("Hello Meheret!"), "mgokpSJoX7npmAK1Zj8ze1926CLxYDt1iF", "mkFWGt4hT11XS8dJKzzRFsTrqjjAwZfQAC", 1000)
        >>> htlc.opcode()
        "OP_IF OP_HASH256 821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e0158 OP_EQUALVERIFY OP_DUP OP_HASH160 0e259e08f2ec9fc99a92b6f66fdfcb3c7914fd68 OP_EQUALVERIFY OP_CHECKSIG OP_ELSE e803 OP_CHECKSEQUENCEVERIFY OP_DROP OP_DUP OP_HASH160 33ecab3d67f0e2bde43e52f41ec1ecbdc73f11f8 OP_EQUALVERIFY OP_CHECKSIG OP_ENDIF"
        """

        if self._script is None:
            raise ValueError("HTLC script is None, first build HTLC.")
        return self._script.decompile()

    def hash(self) -> str:
        """
        Get Bitcoin HTLC hash.

        :returns: str -- Bitcoin Hash Time Lock Contract (HTLC) hash.

        >>> from swap.providers.bitcoin.htlc import HTLC
        >>> from swap.utils import sha256
        >>> htlc = HTLC(network="testnet")
        >>> htlc.build_htlc(sha256("Hello Meheret!"), "mgokpSJoX7npmAK1Zj8ze1926CLxYDt1iF", "mkFWGt4hT11XS8dJKzzRFsTrqjjAwZfQAC", 1000)
        >>> htlc.hash()
        "a9149418feed4647e156d6663db3e0cef7c050d0386787"
        """

        if self._script is None:
            raise ValueError("HTLC script is None, first build HTLC.")
        return str(P2shScript(self._script.p2sh_hash()).hexlify())

    def address(self) -> str:
        """
        Get Bitcoin Hash Time Lock Contract (HTLC) address.

        :returns: str -- Bitcoin HTLC address.

        >>> from swap.providers.bitcoin.htlc import HTLC
        >>> from swap.utils import sha256
        >>> htlc = HTLC(network="testnet")
        >>> htlc.build_htlc(sha256("Hello Meheret!"), "mgokpSJoX7npmAK1Zj8ze1926CLxYDt1iF", "mkFWGt4hT11XS8dJKzzRFsTrqjjAwZfQAC", 1000)
        >>> htlc.address()
        "2N6kHwQy6Ph5EdKNgzGrcW2WhGHKGfmP5ae"
        """

        if self._script is None:
            raise ValueError("HTLC script is None, first build HTLC.")
        return str(P2shScript(self._script.p2sh_hash()).address(
            mainnet=(True if self._network == "mainnet" else False)
        ))

    def balance(self, unit: str = config["unit"]) -> Union[int, float]:
        """
        Get Bitcoin HTLC balance.

        :param unit: Bitcoin unit, default to SATOSHI.
        :type unit: str

        :return: int, float -- Bitcoin wallet balance.

        >>> from swap.providers.bitcoin.htlc import HTLC
        >>> from swap.utils import sha256
        >>> htlc = HTLC(network="testnet")
        >>> htlc.build_htlc(sha256("Hello Meheret!"), "mgokpSJoX7npmAK1Zj8ze1926CLxYDt1iF", "mkFWGt4hT11XS8dJKzzRFsTrqjjAwZfQAC", 1000)
        >>> htlc.balance(unit="unit")
        1000010
        """

        if unit not in ["BTC", "mBTC", "SATOSHI"]:
            raise UnitError("Invalid Bitcoin unit, choose only BTC, mBTC or SATOSHI units.")
        _balance: int = get_balance(address=self.address(), network=self._network)
        return _balance if unit == "SATOSHI" else \
            amount_unit_converter(amount=_balance, unit_from=f"SATOSHI2{unit}")

    def utxos(self, limit: int = 15) -> list:
        """
        Get Bitcoin HTLC unspent transaction output (UTXO's).

        :param limit: Limit of UTXO's, default is 15.
        :type limit: int

        :return: list -- Bitcoin unspent transaction outputs.

        >>> from swap.providers.bitcoin.htlc import HTLC
        >>> from swap.utils import sha256
        >>> htlc = HTLC(network="testnet")
        >>> htlc.build_htlc(sha256("Hello Meheret!"), "mgokpSJoX7npmAK1Zj8ze1926CLxYDt1iF", "mkFWGt4hT11XS8dJKzzRFsTrqjjAwZfQAC", 1000)
        >>> htlc.utxos()
        [{'index': 0, 'hash': '9825b68e57c8a924285828dde37869c2eca3bb3784b171353962f0d7e7577da1', 'output_index': 0, 'amount': 10000, 'script': 'a9149418feed4647e156d6663db3e0cef7c050d0386787'}]
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
