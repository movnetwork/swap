#!/usr/bin/env python3

from binascii import unhexlify
from btcpy.structs.script import (
    Script, ScriptBuilder, P2shScript, IfElseScript
)
from btcpy.structs.transaction import Locktime
from datetime import datetime
from typing import (
    Optional, Union
)

import hashlib
import sys
import os

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

    def __init__(self, network: str = config["network"], contract_address: Optional[str] = None):

        if not is_network(network=network):
            raise NetworkError(f"Invalid Bitcoin '{network}' network",
                               "choose only 'mainnet' or 'testnet' networks.")
        self._network: str = network
        self._script: Optional[IfElseScript, ScriptBuilder] = None
        self._contract_address: Optional[str] = contract_address
        self.agreements: Optional[dict] = None

    @property
    def script(self) -> Union[ScriptBuilder]:
        return self._script

    def build_htlc(self, secret_hash: str, recipient_address: str, sender_address: str, endtime: int) -> "HTLC":
        """
        Build Bitcoin Hash Time Lock Contract (HTLC).

        :param secret_hash: secret sha-256 hash.
        :type secret_hash: str
        :param recipient_address: Bitcoin recipient address.
        :type recipient_address: str
        :param sender_address: Bitcoin sender address.
        :type sender_address: str
        :param endtime: Expiration block time (Seconds).
        :type endtime: int

        :returns: HTLC -- Bitcoin Hash Time Lock Contract (HTLC) instance.

        >>> from swap.providers.bitcoin.htlc import HTLC
        >>> from swap.utils import sha256
        >>> htlc: HTLC = HTLC(network="testnet")
        >>> htlc.build_htlc(secret_hash=sha256("Hello Meheret!"), recipient_address="mgS3WMHp9nvdUPeDJxr5iCF2P5HuFZSR3V", sender_address="n1wgm6kkzMcNfAtJmes8YhpvtDzdNhDY5a", endtime=1624687630)
        <swap.providers.bitcoin.htlc.HTLC object at 0x0409DAF0>
        """

        # Check parameter instances
        if len(secret_hash) != 64:
            raise ValueError("Invalid secret hash, length must be 64.")
        if not is_address(address=recipient_address, network=self._network):
            raise AddressError(f"Invalid Bitcoin recipient '{recipient_address}' {self._network} address.")
        if not is_address(address=sender_address, network=self._network):
            raise AddressError(f"Invalid Bitcoin sender '{sender_address}' {self._network} address.")

        # Get current working directory path (like linux or unix path).
        cwd: str = os.path.dirname(sys.modules[__package__].__file__)

        with open(f"{cwd}/contracts/htlc.script", "r", encoding="utf-8") as htlc_script:
            htlc_opcode: str = htlc_script.readlines()[-1]  # HTLC OP_Code script
            htlc_script.close()

        build_htlc_opcode: str = htlc_opcode.format(
            secret_hash=hashlib.sha256(unhexlify(secret_hash)).hexdigest(),
            recipient_address_hash=get_address_hash(
                address=recipient_address, script=False
            ),
            sender_address_hash=get_address_hash(
                address=sender_address, script=False
            ),
            endtime=Locktime(n=endtime).for_script().hexlify()[2:]
        )

        self.agreements = {
            "secret_hash": secret_hash,
            "recipient_address": recipient_address,
            "sender_address": sender_address,
            "endtime": {
                "datetime": str(datetime.fromtimestamp(endtime)),
                "timestamp": endtime
            }
        }
        bytecode: str = Script.compile(build_htlc_opcode)
        self._script = ScriptBuilder.identify(bytecode)
        return self

    def from_opcode(self, opcode: str) -> "HTLC":
        """
        Initiate Bitcoin Hash Time Lock Contract (HTLC) from opcode script.

        :param opcode: Bitcoin opcode script.
        :type opcode: str

        :returns: HTLC -- Bitcoin Hash Time Lock Contract (HTLC) instance.

        >>> from swap.providers.bitcoin.htlc import HTLC
        >>> htlc: HTLC = HTLC(network="testnet")
        >>> opcode: str = "OP_IF OP_HASH256 821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e0158 OP_EQUALVERIFY OP_DUP OP_HASH160 0a0a6590e6ba4b48118d21b86812615219ece76b OP_EQUALVERIFY OP_CHECKSIG OP_ELSE 0ec4d660 OP_CHECKLOCKTIMEVERIFY OP_DROP OP_DUP OP_HASH160 e00ff2a640b7ce2d336860739169487a57f84b15 OP_EQUALVERIFY OP_CHECKSIG OP_ENDIF"
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
        >>> htlc: HTLC = HTLC(network="testnet")
        >>> bytecode: str = "63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a9140a0a6590e6ba4b48118d21b86812615219ece76b88ac67040ec4d660b17576a914e00ff2a640b7ce2d336860739169487a57f84b1588ac68"
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
        >>> htlc: HTLC = HTLC(network="testnet")
        >>> htlc.build_htlc(sha256("Hello Meheret!"), "mgS3WMHp9nvdUPeDJxr5iCF2P5HuFZSR3V", "n1wgm6kkzMcNfAtJmes8YhpvtDzdNhDY5a", 1624687630)
        >>> htlc.bytecode()
        "63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a9140a0a6590e6ba4b48118d21b86812615219ece76b88ac67040ec4d660b17576a914e00ff2a640b7ce2d336860739169487a57f84b1588ac68"
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
        >>> htlc: HTLC = HTLC(network="testnet")
        >>> htlc.build_htlc(sha256("Hello Meheret!"), "mgS3WMHp9nvdUPeDJxr5iCF2P5HuFZSR3V", "n1wgm6kkzMcNfAtJmes8YhpvtDzdNhDY5a", 1624687630)
        >>> htlc.opcode()
        "OP_IF OP_HASH256 821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e0158 OP_EQUALVERIFY OP_DUP OP_HASH160 0a0a6590e6ba4b48118d21b86812615219ece76b OP_EQUALVERIFY OP_CHECKSIG OP_ELSE 0ec4d660 OP_CHECKLOCKTIMEVERIFY OP_DROP OP_DUP OP_HASH160 e00ff2a640b7ce2d336860739169487a57f84b15 OP_EQUALVERIFY OP_CHECKSIG OP_ENDIF"
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
        >>> htlc: HTLC = HTLC(network="testnet")
        >>> htlc.build_htlc(sha256("Hello Meheret!"), "mgS3WMHp9nvdUPeDJxr5iCF2P5HuFZSR3V", "n1wgm6kkzMcNfAtJmes8YhpvtDzdNhDY5a", 1624687630)
        >>> htlc.hash()
        "a914c8c77a9b43ee2bdf1a07c48699833d7668bf264c87"
        """

        if self._script is None:
            raise ValueError("HTLC script is None, first build HTLC.")
        return str(P2shScript(self._script.p2sh_hash()).hexlify())

    def contract_address(self) -> str:
        """
        Get Bitcoin Hash Time Lock Contract (HTLC) address.

        :returns: str -- Bitcoin HTLC address.

        >>> from swap.providers.bitcoin.htlc import HTLC
        >>> from swap.utils import sha256
        >>> htlc: HTLC = HTLC(network="testnet")
        >>> htlc.build_htlc(sha256("Hello Meheret!"), "mgS3WMHp9nvdUPeDJxr5iCF2P5HuFZSR3V", "n1wgm6kkzMcNfAtJmes8YhpvtDzdNhDY5a", 1624687630)
        >>> htlc.contract_address()
        "2NBYr6gvh4ujsRwKKjDrrRr2vGonazzX6Z6"
        """

        if self._contract_address:
            return self._contract_address
        if self._script is None:
            raise ValueError("HTLC script is None, first build HTLC.")
        return str(P2shScript(self._script.p2sh_hash()).address(
            mainnet=(True if self._network == "mainnet" else False)
        ))

    def balance(self, unit: str = config["unit"]) -> Union[int, float]:
        """
        Get Bitcoin HTLC balance.

        :param unit: Bitcoin unit, default to Satoshi.
        :type unit: str

        :return: int, float -- Bitcoin wallet balance.

        >>> from swap.providers.bitcoin.htlc import HTLC
        >>> from swap.utils import sha256
        >>> htlc: HTLC = HTLC(network="testnet")
        >>> htlc.build_htlc(sha256("Hello Meheret!"), "mgS3WMHp9nvdUPeDJxr5iCF2P5HuFZSR3V", "n1wgm6kkzMcNfAtJmes8YhpvtDzdNhDY5a", 1624687630)
        >>> htlc.balance(unit="BTC")
        0.001
        """

        if unit not in ["BTC", "mBTC", "Satoshi"]:
            raise UnitError("Invalid Bitcoin unit, choose only 'BTC', 'mBTC' or 'Satoshi' units.")
        _balance: int = get_balance(address=self.contract_address(), network=self._network)
        return _balance if unit == "Satoshi" else \
            amount_unit_converter(amount=_balance, unit_from=f"Satoshi2{unit}")

    def utxos(self, limit: int = 15) -> list:
        """
        Get Bitcoin HTLC unspent transaction output (UTXO's).

        :param limit: Limit of UTXO's, default is 15.
        :type limit: int

        :return: list -- Bitcoin unspent transaction outputs.

        >>> from swap.providers.bitcoin.htlc import HTLC
        >>> from swap.utils import sha256
        >>> htlc: HTLC = HTLC(network="testnet")
        >>> htlc.build_htlc(sha256("Hello Meheret!"), "mgS3WMHp9nvdUPeDJxr5iCF2P5HuFZSR3V", "n1wgm6kkzMcNfAtJmes8YhpvtDzdNhDY5a", 1624687630)
        >>> htlc.utxos()
        [{'index': 0, 'hash': 'a211d21110756b266925fee2fbf2dc81529beef5e410311b38578dc3a076fb31', 'output_index': 0, 'amount': 100000, 'script': 'a914c8c77a9b43ee2bdf1a07c48699833d7668bf264c87'}]
        """

        utxos = list()
        _utxos = get_utxos(
            address=self.contract_address(), network=self._network, limit=limit
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
