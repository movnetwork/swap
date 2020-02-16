#!/usr/bin/env python3

from equity import Equity

from ..config import bytom

# Bytom configuration
bytom = bytom()

# Hash Time Lock Contract (HTLC) Script
HTLC_SCRIPT = """
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


# Hash Time Lock Contract
class HTLC:
    """
    Bytom Hash Time Lock Contract (HTLC) class.

    :param network: bytom network, defaults to testnet.
    :type network: str
    :returns:  HTLC -- bytom HTLC instance.

    .. note::
        Bytom has only three networks, ``mainnet``, ``solonet`` and ``testnet``.
    """

    # Initialization
    def __init__(self, network="testnet"):
        # Bytom network.
        self.network = network
        # Initializing equity
        self.equity = None

    # Initialize new HTLC Contract script
    def init(self, secret_hash, recipient_public, sender_public, sequence=bytom["sequence"]):
        """
        Initialize bytom Hash Time Lock Contract (HTLC).

        :param secret_hash: secret sha-256 hash.
        :type secret_hash: hash
        :param recipient_public: bytom recipient public key.
        :type recipient_public: str
        :param sender_public: bytom sender public key.
        :type sender_public: int
        :param sequence: bytom sequence number of expiration block, defaults to bytom config sequence (15).
        :type sequence: int
        :returns: HTLC -- bytom Hash Time Lock Contract (HTLC) instance.

        >>> from shuttle.providers.bytom.htlc import HTLC
        >>> htlc = HTLC(network="testnet")
        >>> htlc.init(secret_hash, recipient_public_key, sender_public_key, 100)
        <shuttle.providers.bytom.htlc.HTLC object at 0x0409DAF0>
        """

        # HTLC agreements
        HTLC_ARGS = [
            secret_hash,  # secret_hash: Hash
            recipient_public,  # recipient: PublicKey
            sender_public,  # sender: PublicKey
            sequence,  # sequence: Integer
        ]
        # Compiling HTLC contract
        self.equity = Equity(bytom[self.network]["bytom"])\
            .compile_source(HTLC_SCRIPT, HTLC_ARGS)
        return self

    # Bytecode HTLC script
    def bytecode(self):
        """
        Get bytom htlc bytecode.

        :returns: str -- bytom Hash Time Lock Contract (HTLC) bytecode.

        >>> from shuttle.providers.bytom.htlc import HTLC
        >>> htlc = HTLC(network="testnet")
        >>> htlc.init(secret_hash, recipient_public_key, sender_public_key, 100)
        >>> htlc.bytecode()
        "01642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"
        """

        if self.equity and "program" not in self.equity:
            raise ValueError("htlc script is none, initialization htlc first")
        return self.equity["program"]

    # OP Code of HTLC script
    def opcode(self):
        """
        Get bytom htlc opcode.

        :returns: str -- bytom Hash Time Lock Contract (HTLC) opcode.

        >>> from shuttle.providers.bytom.htlc import HTLC
        >>> htlc = HTLC(network="testnet")
        >>> htlc.init(secret_hash, recipient_public_key, sender_public_key, 100)
        >>> htlc.opcode()
        "0x64 0x91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2 0xac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01 0x2b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff DEPTH 0x547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac FALSE CHECKPREDICATE"
        """

        if self.equity and "opcodes" not in self.equity:
            raise ValueError("htlc script is none, initialization htlc first")
        return self.equity["opcodes"]
