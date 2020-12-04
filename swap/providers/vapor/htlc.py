#!/usr/bin/env python3

from pybytom.script import (
    get_script_hash, get_p2wsh_program, get_p2wsh_address
)
from pybytom.script.builder import Builder
from pybytom.script.opcode import (
    OP_FALSE, OP_DEPTH, OP_CHECKPREDICATE
)
from equity import Equity
from ctypes import c_int64
from typing import (
    Optional, List
)

from ...exceptions import NetworkError
from ..config import vapor as config
from .rpc import (
    get_utxos, get_balance
)
from .utils import is_network


# Equity smart contract -> Hash Time Lock Contract (HTLC) Script
HTLC_SCRIPT: str = """
contract HTLC (
  secret_hash: Hash,
  recipient: PublicKey,
  sender: PublicKey,
  sequence: Integer
) locks valueAmount of valueAsset {
  clause claim(preimage: String, sig: Signature) {
    verify sha256(preimage) == secret_hash
    verify checkTxSig(recipient, sig)
    unlock valueAmount of valueAsset
  }
  clause refund(sig: Signature) {
    verify above(sequence)
    verify checkTxSig(sender, sig)
    unlock valueAmount of valueAsset
  }
}
"""

# Equity smart contract -> Hash Time Lock Contract (HTLC) Script Binary
HTLC_SCRIPT_BINARY: str = "547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac"


class HTLC:
    """
    Vapor Hash Time Lock Contract (HTLC).

    :param network: Vapor network, defaults to mainnet.
    :type network: str

    :returns: HTLC -- Vapor HTLC instance.

    .. note::
        Vapor has only three networks, ``mainnet``, ``solonet`` and ``testnet``.
    """

    def __init__(self, network: str = config["network"]):

        if not is_network(network=network):
            raise NetworkError(f"Invalid Vapor '{network}' network",
                               "choose only 'mainnet', 'solonet' or 'testnet' networks.")
        self._network: str = network
        self._script: Optional[Equity, dict] = None

    def build_htlc(self, secret_hash: str, recipient_public_key: str, sender_public_key: str,
                   sequence: int = config["sequence"], use_script: bool = False) -> "HTLC":
        """
        Build Vapor Hash Time Lock Contract (HTLC).

        :param secret_hash: secret sha-256 hash.
        :type secret_hash: str
        :param recipient_public_key: Vapor recipient public key.
        :type recipient_public_key: str
        :param sender_public_key: Vapor sender public key.
        :type sender_public_key: str
        :param sequence: Vapor sequence number(expiration block), defaults to Vapor config sequence.
        :type sequence: int
        :param use_script: Initialize HTLC by using script, default to False.
        :type use_script: bool

        :returns: HTLC -- Vapor Hash Time Lock Contract (HTLC) instance.

        >>> from swap.providers.vapor.htlc import HTLC
        >>> from swap.utils import sha256
        >>> htlc = HTLC(network="mainnet")
        >>> htlc.build_htlc(secret_hash=sha256("Hello Meheret!"), recipient_public_key="3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", sender_public_key="91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2", sequence=1000, use_script=False)
        <swap.providers.vapor.htlc.HTLC object at 0x0409DAF0>
        """

        # Checking parameters instances
        if len(secret_hash) != 64:
            raise ValueError("Invalid secret hash, length must be 64")
        if len(recipient_public_key) != 64:
            raise ValueError("Invalid Bitcoin recipient public key, length must be 64")
        if len(sender_public_key) != 64:
            raise ValueError("Invalid Bitcoin sender public key, length must be 64")

        if use_script:
            HTLC_AGREEMENTS: List[str, int] = [
                secret_hash,
                recipient_public_key,
                sender_public_key,
                sequence
            ]
            # Compile HTLC by script
            self._script = Equity(
                url=config[self._network]["vapor-core"], timeout=config["sequence"]
            ).compile_source(HTLC_SCRIPT, HTLC_AGREEMENTS)
        else:
            # Compile HTLC by script binary
            builder: Builder = Builder()
            builder.add_int(sequence)
            builder.add_bytes(bytes.fromhex(sender_public_key))
            builder.add_bytes(bytes.fromhex(recipient_public_key))
            builder.add_bytes(bytes.fromhex(secret_hash))
            builder.add_op(OP_DEPTH)
            builder.add_bytes(bytes.fromhex(HTLC_SCRIPT_BINARY))
            builder.add_op(OP_FALSE)
            builder.add_op(OP_CHECKPREDICATE)

            SEQUENCE = bytes(c_int64(sequence)).rstrip(b'\x00').hex()
            self._script = dict(
                program=builder.hex_digest(),
                opcodes=f"0x{SEQUENCE} 0x{sender_public_key} 0x{recipient_public_key} "
                        f"0x{secret_hash} DEPTH 0x{HTLC_SCRIPT_BINARY} FALSE CHECKPREDICATE"
            )
        return self

    def from_bytecode(self, bytecode: str) -> "HTLC":
        """
        Initialize Vapor Hash Time Lock Contract (HTLC) from bytecode.

        :param bytecode: Vapor bytecode.
        :type bytecode: str

        :returns: HTLC -- Vapor Hash Time Lock Contract (HTLC) instance.

        >>> from swap.providers.vapor.htlc import HTLC
        >>> htlc = HTLC(network="testnet")
        >>> bytecode = "02e8032091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"
        >>> htlc.from_bytecode(bytecode=bytecode)
        <swap.providers.bitcoin.htlc.HTLC object at 0x0409DAF0>
        """
        
        self._script = dict(program=bytecode)
        return self

    def bytecode(self) -> str:
        """
        Get Vapor Hash Time Lock Contract (HTLC) bytecode.

        :returns: str -- Vapor HTLC bytecode.

        >>> from swap.providers.vapor.htlc import HTLC
        >>> from swap.utils import sha256
        >>> htlc = HTLC(network="mainnet")
        >>> htlc.build_htlc(sha256("Hello Meheret!"), "3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2", 1000, False)
        >>> htlc.bytecode()
        "02e8032091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"
        """

        if not self._script or "program" not in self._script:
            raise ValueError("HTLC script is None, first build HTLC.")
        return self._script["program"]

    def opcode(self) -> Optional[str]:
        """
        Get Vapor Hash Time Lock Contract (HTLC) OP_Code.

        :returns: str -- Vapor HTLC opcode.

        >>> from swap.providers.vapor.htlc import HTLC
        >>> from swap.utils import sha256
        >>> htlc = HTLC(network="mainnet")
        >>> htlc.build_htlc(sha256("Hello Meheret!"), "3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2", 1000, False)
        >>> htlc.opcode()
        "0xe803 0x91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2 0x3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e 0x3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb DEPTH 0x547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac FALSE CHECKPREDICATE"
        """

        if "opcodes" not in self._script:
            if not self._script:
                raise ValueError("HTLC script is None, first build HTLC.")
            return None
        return self._script["opcodes"]

    def hash(self) -> str:
        """
        Get Vapor Hash Time Lock Contract (HTLC) hash.

        :returns: str -- Vapor HTLC hash.

        >>> from swap.providers.vapor.htlc import HTLC
        >>> from swap.utils import sha256
        >>> htlc = HTLC(network="mainnet")
        >>> htlc.build_htlc(sha256("Hello Meheret!"), "3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2", 1000, False)
        >>> htlc.hash()
        "4f8f0e88d0a44b3d884b07b6dd4536518ffcbb596a91ca0e6b2f37e96463bbfc"
        """

        if not self._script or "program" not in self._script:
            raise ValueError("HTLC script is None, first build HTLC.")
        return get_script_hash(bytecode=self.bytecode())

    def address(self) -> str:
        """
        Get Vapor Hash Time Lock Contract (HTLC) address.

        :returns: str -- Vapor HTLC address.

        >>> from swap.providers.vapor.htlc import HTLC
        >>> from swap.utils import sha256
        >>> htlc = HTLC(network="mainnet")
        >>> htlc.build_htlc(sha256("Hello Meheret!"), "3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2", 1000, False)
        >>> htlc.address()
        "vp1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07qcyvk37"
        """

        if not self._script or "program" not in self._script:
            raise ValueError("HTLC script is None, first build HTLC.")
        return get_p2wsh_address(script_hash=self.hash(), network=self._network, vapor=True)
    
    def balance(self, asset: str = config["asset"]) -> int:
        """
        Get Vapor HTLC balance.

        :param asset: Vapor asset id, defaults to BTM asset.
        :type asset: str

        :return: int -- Vapor HTLC balance (NEU amount).

        >>> from swap.providers.vapor.htlc import HTLC
        >>> from swap.utils import sha256
        >>> htlc = HTLC(network="mainnet")
        >>> htlc.build_htlc(sha256("Hello Meheret!"), "3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2", 1000, False)
        >>> htlc.balance(asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        30000
        """

        return get_balance(address=self.address(), asset=asset, network=self._network)

    def utxos(self, asset: str = config["asset"], limit: int = 15) -> list:
        """
        Get Vapor HTLC unspent transaction output (UTXO's).

        :param asset: Vapor asset id, defaults to BTM asset.
        :type asset: str
        :param limit: Limit of UTXO's, default is 15.
        :type limit: int

        :return: list -- Vapor unspent transaction outputs.

        >>> from swap.providers.vapor.htlc import HTLC
        >>> from swap.utils import sha256
        >>> htlc = HTLC(network="mainnet")
        >>> htlc.build_htlc(sha256("Hello Meheret!"), "3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2", 1000, False)
        >>> htlc.utxos(asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        [{'hash': '8a0d861767240a284ebed0320b11b81253727ecdac0c80bc6a88127327c0d8a1', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 10000}, {'hash': '76c9ec09f4990122337b1cb9925abc5c5de115065cb1eea7adb7b5fdeb2c6e1e', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 10000}, {'hash': '2637748a967aa5428008aa57159b9795f3aff63b81c72df0575041e7df1efe01', 'asset': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'amount': 10000}]
        """

        return get_utxos(program=get_p2wsh_program(script_hash=self.hash()), asset=asset, limit=limit)
