#!/usr/bin/env python3
from btcpy.structs.crypto import PrivateKey
from btcpy.structs.sig import P2pkhSolver, P2shSolver, IfElseSolver, HashlockSolver, Branch, RelativeTimelockSolver
from btcpy.structs.transaction import Sequence

from .htlc import HTLC


class FundSolver:

    def __init__(self, private_key):
        self.private_key = PrivateKey.unhexlify(private_key)

    def solve(self):
        return P2pkhSolver(self.private_key,
                           compressed=False)


class ClaimSolver:

    def __init__(self, htlc_script, secret, private_key):
        if not isinstance(htlc_script, HTLC):
            raise Exception("HTLC Error!")
        self.htlc_script = htlc_script.htlc_script
        self.secret = secret.encode()
        self.private_key = PrivateKey.unhexlify(private_key)

    def solve(self):
        return P2shSolver(
            self.htlc_script,
            IfElseSolver(
                Branch.IF,
                HashlockSolver(
                    self.secret,
                    P2pkhSolver(self.private_key,
                                compressed=False)
                )
            )
        )


class RefundSolver:

    def __init__(self, htlc_script, sequence, private_key):
        if not isinstance(htlc_script, HTLC):
            raise Exception("HTLC Error!")
        self.htlc_script = htlc_script.htlc_script
        self.sequence = sequence
        self.private_key = PrivateKey.unhexlify(private_key)

    def solve(self):
        return P2shSolver(
            self.htlc_script,
            IfElseSolver(
                Branch.ELSE,
                RelativeTimelockSolver(
                    Sequence(self.sequence),
                    P2pkhSolver(self.private_key,
                                compressed=False)
                )
            )
        )
