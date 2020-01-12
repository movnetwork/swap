#!/usr/bin/env python3

from btmhdw import BytomHDWallet


# Fund HTLC Solver
class FundSolver:

    # Initialization funding on hash time lock contract (HTLC)
    def __init__(self, xprivate_key):
        # Initialization bytom wallet
        self.bytomHDWallet = BytomHDWallet()
        # XPrivate key of sender to sign signature
        self.xprivate_key = xprivate_key

    # Signature solve
    def solve(self):
        return self.bytomHDWallet\
            .master_key_from_xprivate(xprivate=self.xprivate_key)


# Claim HTLC Solver
class ClaimSolver:

    # Initialization claiming on hash time lock contract (HTLC)
    def __init__(self, secret, xprivate_key):
        # Initialization bytom wallet
        self.bytomHDWallet = BytomHDWallet()
        # Secret key to unlock HTLC
        self.secret = secret.encode()
        # XPrivate key of recipient to sign signature
        self.xprivate_key = xprivate_key

    # Signature solve
    def solve(self):
        return self.bytomHDWallet.master_key_from_xprivate(
            xprivate=self.xprivate_key), self.secret


# Refund HTLC Solver
class RefundSolver:

    # Initialization claiming on hash time lock contract (HTLC)
    def __init__(self, xprivate_key):
        # Initialization bytom wallet
        self.bytomHDWallet = BytomHDWallet()
        # XPrivate key of recipient to sign signature
        self.xprivate_key = xprivate_key

    # Signature solve
    def solve(self):
        return self.bytomHDWallet.master_key_from_xprivate(
            xprivate=self.xprivate_key)

