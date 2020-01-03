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

    # Initialization
    def __init__(self, network="testnet"):
        # Bitcoin network.
        self.network = network
        # Bitcoin network boolean..
        self.testnet = True if network == "testnet" else False
        # Initializing equity
        self.equity = None

    # Initialize new HTLC Contract script
    def init(self, secret_hash, recipient_public, sender_public, sequence=100):

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
        if self.equity and "program" not in self.equity:
            raise ValueError("HTLC script is none, Please initialization htlc first.")
        return self.equity["program"]

    # OP Code of HTLC script
    def opcode(self):
        if self.equity and "opcodes" not in self.equity:
            raise ValueError("HTLC script is none, Please initialization htlc first.")
        return self.equity["opcodes"]
