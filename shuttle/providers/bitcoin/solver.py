#!/usr/bin/env python3

from btcpy.structs.crypto import PrivateKey
from btcpy.structs.sig import P2pkhSolver, \
    IfElseSolver, HashlockSolver, Branch, RelativeTimelockSolver
from btcpy.structs.transaction import Sequence

from ..config import bitcoin

# Bitcoin config
bitcoin = bitcoin()


# Fund HTLC Solver
class FundSolver:
    """
    Bitcoin FundSolver class.

    :param private_key: bitcoin sender private key.
    :type private_key: str
    :param compressed: bitcoin network, defaults to False.
    :type compressed: bool
    :returns:  FundSolver -- bitcoin fund solver instance.

    >>> from shuttle.providers.bitcoin.solver import FundSolver
    >>> fund_solver = FundSolver(sender_private_key)
    <shuttle.providers.bitcoin.solver.FundSolver object at 0x03FCCA60>
    """

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
    """
    Bitcoin ClaimSolver class.

    :param secret: secret key.
    :type secret: str
    :param private_key: bitcoin sender private key.
    :type private_key: str
    :param sequence: bitcoin sequence number of expiration block, defaults to bitcoin config sequence (15).
    :type sequence: int
    :param compressed: bitcoin network, defaults to False.
    :type compressed: bool
    :returns:  ClaimSolver -- bitcoin claim solver instance.

    >>> from shuttle.providers.bitcoin.solver import ClaimSolver
    >>> claim_solver = ClaimSolver("Hello Meheret!", recipient_private_key)
    <shuttle.providers.bitcoin.solver.ClaimSolver object at 0x03FCCA60>
    """

    # Initialization claiming on hash time lock contract (HTLC)
    def __init__(self, secret, private_key,
                 sequence=bitcoin["sequence"], compressed=False):
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
    """
    Bitcoin RefundSolver class.

    :param secret: secret key.
    :type secret: str
    :param private_key: bitcoin sender private key.
    :type private_key: str
    :param sequence: bitcoin sequence number of expiration block, defaults to bitcoin config sequence (15).
    :type sequence: int
    :param compressed: bitcoin network, defaults to False.
    :type compressed: bool
    :returns:  RefundSolver -- bitcoin refund solver instance.

    >>> from shuttle.providers.bitcoin.solver import RefundSolver
    >>> refund_solver = RefundSolver("Hello Meheret!", sender_private_key)
    <shuttle.providers.bitcoin.solver.RefundSolver object at 0x03FCCA60>
    """

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
