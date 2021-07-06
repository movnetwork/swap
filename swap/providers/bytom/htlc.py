#!/usr/bin/env python3

from pybytom.script import (
    get_script_hash, get_p2wsh_program, get_p2wsh_address
)
from pybytom.script.builder import Builder
from pybytom.wallet.tools import (
    get_address, get_program
)
from pybytom.script.opcode import (
    OP_FALSE, OP_DEPTH, OP_CHECKPREDICATE
)
from pathlib import PurePosixPath
from equity import Equity
from ctypes import c_int64
from typing import (
    Optional, List, Union
)

import os

from ...exceptions import (
    NetworkError, UnitError
)
from ..config import bytom as config
from .assets import AssetNamespace
from .rpc import (
    get_utxos, get_balance
)
from .utils import (
    is_network, amount_unit_converter
)


class HTLC:
    """
    Bytom Hash Time Lock Contract (HTLC).

    :param network: Bytom network, defaults to ``mainnet``.
    :type network: str

    :returns: HTLC -- Bytom HTLC instance.

    .. note::
        Bytom has only three networks, ``mainnet``, ``solonet`` and ``testnet``.
    """

    def __init__(self, network: str = config["network"], contract_address: Optional[str] = None):

        if not is_network(network=network):
            raise NetworkError(f"Invalid Bytom '{network}' network",
                               "choose only 'mainnet', 'solonet' or 'testnet' networks.")
        self._network: str = network
        self._script: Optional[Equity, dict] = None
        self._contract_address: Optional[str] = contract_address
        self.agreements: Optional[dict] = None

    def build_htlc(self, secret_hash: str, recipient_public_key: str, sender_public_key: str,
                   endblock: int, use_script: bool = False) -> "HTLC":
        """
        Build Bytom Hash Time Lock Contract (HTLC).

        :param secret_hash: secret sha-256 hash.
        :type secret_hash: str
        :param recipient_public_key: Bytom recipient public key.
        :type recipient_public_key: str
        :param sender_public_key: Bytom sender public key.
        :type sender_public_key: str
        :param endblock: Bytom expiration block height.
        :type endblock: int
        :param use_script: Initialize HTLC by using script, default to ``False``.
        :type use_script: bool

        :returns: HTLC -- Bytom Hash Time Lock Contract (HTLC) instance.

        >>> from swap.providers.bytom.htlc import HTLC
        >>> from swap.providers.bytom.rpc import get_current_block_height
        >>> from swap.utils import sha256
        >>> htlc: HTLC = HTLC(network="mainnet")
        >>> htlc.build_htlc(secret_hash=sha256("Hello Meheret!"), recipient_public_key="3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", sender_public_key="fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212", endblock=get_current_block_height(plus=100), use_script=False)
        <swap.providers.bytom.htlc.HTLC object at 0x0409DAF0>
        """

        # Checking parameters instances
        if len(secret_hash) != 64:
            raise ValueError("Invalid secret hash, length must be 64")
        if len(recipient_public_key) != 64:
            raise ValueError("Invalid Bytom recipient public key, length must be 64")
        if len(sender_public_key) != 64:
            raise ValueError("Invalid Bytom sender public key, length must be 64")

        if use_script:

            # Get current working directory path (like linux or unix path).
            cwd: str = PurePosixPath(os.path.dirname(os.path.realpath(__file__))).__str__().replace("\\", "/")

            with open(f"{cwd}/contracts/htlc.equity", "r", encoding="utf-8") as htlc_equity_file:
                htlc_script: str = "".join(htlc_equity_file.readlines()[-14:])
                htlc_equity_file.close()

            htlc_agreement: List[str, int] = [
                secret_hash,
                recipient_public_key,
                sender_public_key,
                endblock
            ]
            # Compile HTLC by script
            self._script = Equity(config[self._network]["bytom-core"])\
                .compile_source(htlc_script, htlc_agreement)
        else:
            # Compile HTLC by script binary
            builder: Builder = Builder()
            builder.add_int(endblock)
            builder.add_bytes(bytes.fromhex(sender_public_key))
            builder.add_bytes(bytes.fromhex(recipient_public_key))
            builder.add_bytes(bytes.fromhex(secret_hash))
            builder.add_op(OP_DEPTH)
            builder.add_bytes(bytes.fromhex(config["htlc_script_binary"]))
            builder.add_op(OP_FALSE)
            builder.add_op(OP_CHECKPREDICATE)

            sequence: str = bytes(c_int64(endblock)).rstrip(b'\x00').hex()
            self._script = dict(
                program=builder.hex_digest(),
                opcodes=f"0x{sequence} 0x{sender_public_key} 0x{recipient_public_key} "
                        f"0x{secret_hash} DEPTH 0x{config['htlc_script_binary']} FALSE CHECKPREDICATE"
            )

        self.agreements = {
            "secret_hash": secret_hash,
            "recipient": {
                "public_key": recipient_public_key,
                "address": get_address(
                    program=get_program(public_key=recipient_public_key), network=self._network, vapor=False
                )
            },
            "sender": {
                "public_key": sender_public_key,
                "address": get_address(
                    program=get_program(public_key=sender_public_key), network=self._network, vapor=False
                )
            },
            "endblock": endblock
        }
        return self

    def from_bytecode(self, bytecode: str) -> "HTLC":
        """
        Initialize Bytom Hash Time Lock Contract (HTLC) from bytecode.

        :param bytecode: Bytom bytecode.
        :type bytecode: str

        :returns: HTLC -- Bytom Hash Time Lock Contract (HTLC) instance.

        >>> from swap.providers.bytom.htlc import HTLC
        >>> htlc: HTLC = HTLC(network="testnet")
        >>> bytecode: str = "03285d0a20fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"
        >>> htlc.from_bytecode(bytecode=bytecode)
        <swap.providers.bytom.htlc.HTLC object at 0x0409DAF0>
        """
        
        self._script = dict(program=bytecode)
        return self

    def bytecode(self) -> str:
        """
        Get Bytom Hash Time Lock Contract (HTLC) bytecode.

        :returns: str -- Bytom HTLC bytecode.

        >>> from swap.providers.bytom.htlc import HTLC
        >>> from swap.utils import sha256
        >>> htlc: HTLC = HTLC(network="mainnet")
        >>> htlc.build_htlc(secret_hash=sha256("Hello Meheret!"), recipient_public_key="3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", sender_public_key="fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212", endblock=679208)
        >>> htlc.bytecode()
        "03285d0a20fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"
        """

        if not self._script or "program" not in self._script:
            raise ValueError("HTLC script is None, first build HTLC.")
        return self._script["program"]

    def opcode(self) -> Optional[str]:
        """
        Get Bytom Hash Time Lock Contract (HTLC) OP_Code.

        :returns: str -- Bytom HTLC opcode.

        >>> from swap.providers.bytom.htlc import HTLC
        >>> from swap.utils import sha256
        >>> htlc: HTLC = HTLC(network="mainnet")
        >>> htlc.build_htlc(secret_hash=sha256("Hello Meheret!"), recipient_public_key="3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", sender_public_key="fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212", endblock=679208)
        >>> htlc.opcode()
        "0x285d0a 0xfe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212 0x3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e 0x3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb DEPTH 0x547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac FALSE CHECKPREDICATE"
        """

        if "opcodes" not in self._script:
            if not self._script:
                raise ValueError("HTLC script is None, first build HTLC.")
            return None
        return self._script["opcodes"]

    def hash(self) -> str:
        """
        Get Bytom Hash Time Lock Contract (HTLC) hash.

        :returns: str -- Bytom HTLC hash.

        >>> from swap.providers.bytom.htlc import HTLC
        >>> from swap.utils import sha256
        >>> htlc: HTLC = HTLC(network="mainnet")
        >>> htlc.build_htlc(secret_hash=sha256("Hello Meheret!"), recipient_public_key="3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", sender_public_key="fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212", endblock=679208)
        >>> htlc.hash()
        "e7f4a9815f3a36c616c5666b97fb7fdacd3720c117d078c429494d1b617fe7d4"
        """

        if not self._script or "program" not in self._script:
            raise ValueError("HTLC script is None, first build HTLC.")
        return get_script_hash(bytecode=self.bytecode())

    def contract_address(self) -> str:
        """
        Get Bytom Hash Time Lock Contract (HTLC) address.

        :returns: str -- Bytom HTLC address.

        >>> from swap.providers.bytom.htlc import HTLC
        >>> from swap.utils import sha256
        >>> htlc: HTLC = HTLC(network="mainnet")
        >>> htlc.build_htlc(secret_hash=sha256("Hello Meheret!"), recipient_public_key="3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", sender_public_key="fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212", endblock=679208)
        >>> htlc.contract_address()
        "bm1qul62nq2l8gmvv9k9ve4e07mlmtxnwgxpzlg833pff9x3kctlul2q727jyy"
        """

        if self._contract_address:
            return self._contract_address
        if not self._script or "program" not in self._script:
            raise ValueError("HTLC script is None, first build HTLC.")
        return get_p2wsh_address(script_hash=self.hash(), network=self._network, vapor=False)

    def balance(self, asset: Union[str, AssetNamespace] = config["asset"],
                unit: str = config["unit"]) -> Union[int, float]:
        """
        Get Bytom HTLC balance.

        :param asset: Bytom asset id, defaults to ``BTM``.
        :type asset: str, bytom.assets.AssetNamespace, bytom.assets.AssetNamespace
        :param unit: Bytom unit, default to ``NEU``.
        :type unit: str

        :return: int, float -- Bytom HTLC balance.

        >>> from swap.providers.bytom.htlc import HTLC
        >>> from swap.utils import sha256
        >>> htlc: HTLC = HTLC(network="mainnet")
        >>> htlc.build_htlc(secret_hash=sha256("Hello Meheret!"), recipient_public_key="3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", sender_public_key="fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212", endblock=679208)
        >>> htlc.balance(asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", unit="BTM")
        0.1
        """

        if unit not in ["BTM", "mBTM", "NEU"]:
            raise UnitError("Invalid Bytom unit, choose only BTM, mBTM or NEU units.")
        
        _balance: int = get_balance(
            address=self.contract_address(),
            asset=(str(asset.ID) if isinstance(asset, AssetNamespace) else asset),
            network=self._network
        )
        return _balance if unit == "NEU" else \
            amount_unit_converter(amount=_balance, unit_from=f"NEU2{unit}")

    def utxos(self, asset: Union[str, AssetNamespace] = config["asset"], limit: int = 15) -> list:
        """
        Get Bytom HTLC unspent transaction output (UTXO's).

        :param asset: Bytom asset id, defaults to ``BTM``.
        :type asset: str, bytom.assets.AssetNamespace
        :param limit: Limit of UTXO's, default is ``15``.
        :type limit: int

        :return: list -- Bytom unspent transaction outputs.

        >>> from swap.providers.bytom.htlc import HTLC
        >>> from swap.utils import sha256
        >>> htlc: HTLC = HTLC(network="mainnet")
        >>> htlc.build_htlc(secret_hash=sha256("Hello Meheret!"), recipient_public_key="3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", sender_public_key="fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212", endblock=679208)
        >>> htlc.utxos(asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        [{'hash': '1aaf7df33c1d41bc6108c93d8b6da6af1d7f68632f54516408a03ff86494a1f0', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 10000000}]
        """

        return get_utxos(
            program=get_p2wsh_program(script_hash=self.hash()),
            asset=(str(asset.ID) if isinstance(asset, AssetNamespace) else asset),
            limit=limit
        )
