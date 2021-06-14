#!/usr/bin/env python3

from eth_wallet import Wallet


# Fund HTLC Solver
class FundSolver:
    """
    Ethereum FundSolver class.

    :param private_key: ethereum sender private key.
    :type private_key: str
    :returns:  FundSolver -- ethereum fund solver instance.

    >>> from shuttle.providers.ethereum.solver import FundSolver
    >>> fund_solver = FundSolver(sender_private_key)
    <shuttle.providers.ethereum.solver.FundSolver object at 0x03FCCA60>
    """

    # Initialization funding on hash time lock contract (HTLC)
    def __init__(self, private_key):

        # Initialization ethereum wallet
        self.wallet = Wallet()
        # Private key of sender to sign signature
        self.private_key = private_key

    # Signature solve
    def solve(self):
        return self.wallet\
            .from_private_key(private_key=self.private_key)


# Claim HTLC Solver
class ClaimSolver:
    """
    Ethereum ClaimSolver class.

    :param secret: secret key.
    :type secret: str
    :param private_key: ethereum sender private key.
    :type private_key: str
    :returns:  ClaimSolver -- ethereum claim solver instance.

    >>> from shuttle.providers.ethereum.solver import ClaimSolver
    >>> claim_solver = ClaimSolver("Hello Meheret!", recipient_private_key)
    <shuttle.providers.ethereum.solver.ClaimSolver object at 0x03FCCA60>
    """

    # Initialization claiming on hash time lock contract (HTLC)
    def __init__(self, secret, private_key):

        # Initialization ethereum wallet
        self.wallet = Wallet()
        # Secret key to unlock HTLC
        self.secret = secret.encode()
        # Private key of recipient to sign signature
        self.private_key = private_key

    # Signature solve
    def solve(self):
        return self.wallet\
            .from_private_key(private_key=self.private_key)


# Refund HTLC Solver
class RefundSolver:
    """
    Ethereum RefundSolver class.

    :param private_key: ethereum sender private key.
    :type private_key: str
    :returns:  RefundSolver -- ethereum refund solver instance.

    >>> from shuttle.providers.ethereum.solver import RefundSolver
    >>> refund_solver = RefundSolver(sender_private_key)
    <shuttle.providers.ethereum.solver.RefundSolver object at 0x03FCCA60>
    """

    # Initialization claiming on hash time lock contract (HTLC)
    def __init__(self, private_key):

        # Initialization ethereum wallet
        self.wallet = Wallet()
        # Private key of recipient to sign signature
        self.private_key = private_key

    # Signature solve
    def solve(self):
        return self.wallet\
            .from_private_key(private_key=self.private_key)
