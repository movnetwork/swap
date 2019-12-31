#!/usr/bin/env python3

from btcpy.structs.crypto import PrivateKey
from btcpy.structs.sig import P2pkhSolver, \
    IfElseSolver, HashlockSolver, Branch, RelativeTimelockSolver
from btcpy.structs.transaction import Sequence


# Fund HTLC Solver
class FundSolver:

    # Initialization funding on hash time lock contract (HTLC)
    def __init__(self, private_key, compressed=False):
        # Public key compression
        self.compressed = compressed
        # Private key of sender to sign signature
        self.private_key = PrivateKey.unhexlify(private_key)

    # Signature solve
    def solve(self):
        return P2pkhSolver(self.private_key, compressed=self.compressed)


# Claim HTLC Solver
class ClaimSolver:

    # Initialization claiming on hash time lock contract (HTLC)
    def __init__(self, secret, private_key, sequence=5, compressed=False):
        # Public key compression
        self.compressed = compressed
        # Secret key to unlock HTLC
        self.secret = secret.encode()
        # Private key of recipient to sign signature
        self.private_key = PrivateKey.unhexlify(private_key)
        # Sequence number of expiration block
        self.sequence = sequence

    # Signature solve
    def solve(self):
        return IfElseSolver(
            Branch.IF,
            HashlockSolver(
                self.secret,
                P2pkhSolver(self.private_key, compressed=self.compressed)
            )
        )


# Refund HTLC Solver
class RefundSolver:

    # Initialization refunding on hash time lock contract (HTLC)
    def __init__(self, secret, private_key, sequence=5, compressed=False):
        # Public key compression
        self.compressed = compressed
        # Secret key to unlock HTLC
        self.secret = secret.encode()
        # Private key of recipient to sign signature
        self.private_key = PrivateKey.unhexlify(private_key)
        # Sequence number of expiration block
        self.sequence = sequence

    def solve(self):
        return IfElseSolver(
            Branch.ELSE,
            RelativeTimelockSolver(
                Sequence(self.sequence),
                P2pkhSolver(self.private_key, compressed=self.compressed)
            )
        )
