#!/usr/bin/env python3

from btcpy.structs.script import (
    Script, ScriptBuilder, P2shScript, IfElseScript, Hashlock256Script, RelativeTimelockScript
)
from btcpy.structs.transaction import Sequence
from typing import Optional, TypeVar, Union
from binascii import unhexlify

import hashlib

from ...exceptions import (
    AddressError, NetworkError
)
from ..config import bitcoin
from .utils import (
    get_address_hash, is_address, is_network
)

# Bitcoin config
config = bitcoin()
# Type Var HTLC class
_HTLC = TypeVar("_HTLC", bound="HTLC")


class HTLC:
    """
    Bitcoin Hash Time Lock Contract (HTLC) class.

    :param network: Bitcoin network, defaults to testnet.
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
                   sender_address: str, sequence: int = config["sequence"]) -> _HTLC:
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
        >>> htlc.build_htlc(secret_hash=sha256("Hello Meheret!"), recipient_address="muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB", sender_address="mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q", sequence=1000)
        <swap.providers.bitcoin.htlc.HTLC object at 0x0409DAF0>
        """

        # Check parameter instances
        if len(secret_hash) != 64:
            raise ValueError("Invalid secret hash, length must be 64.")
        if not is_address(recipient_address, self._network):
            raise AddressError(f"Invalid Bitcoin recipient '{recipient_address}' {self._network} address.")
        if not is_address(sender_address, self._network):
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

    def from_opcode(self, opcode: str) -> _HTLC:
        """
        Initiate Bitcoin Hash Time Lock Contract (HTLC) from opcode script.

        :param opcode: Bitcoin opcode script.
        :type opcode: str
        :returns: HTLC -- Bitcoin Hash Time Lock Contract (HTLC) instance.

        >>> from swap.providers.bitcoin.htlc import HTLC
        >>> htlc = HTLC(network="testnet")
        >>> htlc_opcode_script = "OP_IF OP_HASH256 821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e0158 OP_EQUALVERIFY OP_DUP OP_HASH160 98f879fb7f8b4951dee9bc8a0327b792fbe332b8 OP_EQUALVERIFY OP_CHECKSIG OP_ELSE e803 OP_CHECKSEQUENCEVERIFY OP_DROP OP_DUP OP_HASH160 64a8390b0b1685fcbf2d4b457118dc8da92d5534 OP_EQUALVERIFY OP_CHECKSIG OP_ENDIF"        >>> htlc.from_opcode(opcode=htlc_opcode_script)
        <swap.providers.bitcoin.htlc.HTLC object at 0x0409DAF0>
        """

        bytecode = Script.compile(opcode)
        self._script = ScriptBuilder.identify(bytecode)
        return self

    def from_bytecode(self, bytecode: str) -> _HTLC:
        """
        Initialize Bitcoin Hash Time Lock Contract (HTLC) from bytecode.

        :param bytecode: Bitcoin bytecode.
        :type bytecode: str
        :returns: HTLC -- Bitcoin Hash Time Lock Contract (HTLC) instance.

        >>> from swap.providers.bitcoin.htlc import HTLC
        >>> htlc = HTLC(network="testnet")
        >>> bytecode = "63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac6702e803b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68"
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
        >>> htlc.build_htlc(sha256("Hello Meheret!"), "muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB", "mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q", 1000)
        >>> htlc.bytecode()
        "63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac6702e803b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68"
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
        >>> htlc.build_htlc(sha256("Hello Meheret!"), "muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB", "mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q", 1000)
        >>> htlc.opcode()
        "OP_IF OP_HASH256 821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e0158 OP_EQUALVERIFY OP_DUP OP_HASH160 98f879fb7f8b4951dee9bc8a0327b792fbe332b8 OP_EQUALVERIFY OP_CHECKSIG OP_ELSE e803 OP_CHECKSEQUENCEVERIFY OP_DROP OP_DUP OP_HASH160 64a8390b0b1685fcbf2d4b457118dc8da92d5534 OP_EQUALVERIFY OP_CHECKSIG OP_ENDIF"
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
        >>> htlc.build_htlc(sha256("Hello Meheret!"), "muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB", "mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q", 1000)
        >>> htlc.hash()
        "a9142bb013c3e4beb08421dedcf815cb65a5c388178b87"
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
        >>> htlc.build_htlc(sha256("Hello Meheret!"), "muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB", "mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q", 1000)
        >>> htlc.address()
        "2MwEDybGC34949zgzWX4M9FHmE3crDSUydP"
        """

        if self._script is None:
            raise ValueError("HTLC script is None, first build HTLC.")
        return str(P2shScript(self._script.p2sh_hash()).address(
            mainnet=(True if self._network == "mainnet" else False)
        ))
