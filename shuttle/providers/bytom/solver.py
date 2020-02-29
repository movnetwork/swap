#!/usr/bin/env python3

from btmhdw import BytomHDWallet


# Fund HTLC Solver
class FundSolver:
    """
    Bytom FundSolver class.

    :param xprivate_key: bytom sender xprivate key.
    :type xprivate_key: str
    :param account: bytom derivation account, defaults to 1.
    :type account: int
    :param change: bytom derivation change, defaults to False.
    :type change: bool
    :param address: bytom derivation address, defaults to 1.
    :type address: int
    :param path: bytom derivation path, defaults to None.
    :type path: str
    :param indexes: bytom derivation indexes, defaults to None.
    :type indexes: list
    :returns:  FundSolver -- bytom fund solver instance.

    >>> from shuttle.providers.bytom.solver import FundSolver
    >>> fund_solver = FundSolver(sender_xprivate_key)
    <shuttle.providers.bytom.solver.FundSolver object at 0x03FCCA60>
    """

    # Initialization funding on hash time lock contract (HTLC)
    def __init__(self, xprivate_key, account=1,
                 change=False, address=1, path=None, indexes=None):
        # Checking path and indexes
        if not path and not indexes:
            path = "m/44/153/{}/{}/{}".format(
                account, 1 if change else 0, address)

        # Initialization bytom wallet
        self.bytomHDWallet = BytomHDWallet()
        # XPrivate key of sender to sign signature
        self.xprivate_key = xprivate_key
        # Setting derivation key
        self.path, self.indexes = path, indexes

    # Signature solve
    def solve(self):
        return self.bytomHDWallet\
            .master_key_from_xprivate(xprivate=self.xprivate_key)


# Claim HTLC Solver
class ClaimSolver:
    """
    Bytom ClaimSolver class.

    :param secret: secret key.
    :type secret: str
    :param xprivate_key: bytom sender xprivate key.
    :type xprivate_key: str
    :param account: bytom derivation account, defaults to 1.
    :type account: int
    :param change: bytom derivation change, defaults to False.
    :type change: bool
    :param address: bytom derivation address, defaults to 1.
    :type address: int
    :param path: bytom derivation path, defaults to None.
    :type path: str
    :param indexes: bytom derivation indexes, defaults to None.
    :type indexes: list
    :returns:  ClaimSolver -- bytom claim solver instance.

    >>> from shuttle.providers.bytom.solver import ClaimSolver
    >>> claim_solver = ClaimSolver("Hello Meheret!", recipient_xprivate_key)
    <shuttle.providers.bytom.solver.ClaimSolver object at 0x03FCCA60>
    """

    # Initialization claiming on hash time lock contract (HTLC)
    def __init__(self, secret, xprivate_key, account=1,
                 change=False, address=1, path=None, indexes=None):
        # Checking path and indexes
        if not path and not indexes:
            path = "m/44/153/{}/{}/{}".format(
                account, 1 if change else 0, address)

        # Initialization bytom wallet
        self.bytomHDWallet = BytomHDWallet()
        # Secret key to unlock HTLC
        self.secret = secret.encode()
        # XPrivate key of recipient to sign signature
        self.xprivate_key = xprivate_key
        # Setting derivation key
        self.path, self.indexes = path, indexes

    # Signature solve
    def solve(self):
        return self.bytomHDWallet.master_key_from_xprivate(
            xprivate=self.xprivate_key)


# Refund HTLC Solver
class RefundSolver:
    """
    Bytom RefundSolver class.

    :param xprivate_key: bytom sender xprivate key.
    :type xprivate_key: str
    :param account: bytom derivation account, defaults to 1.
    :type account: int
    :param change: bytom derivation change, defaults to False.
    :type change: bool
    :param address: bytom derivation address, defaults to 1.
    :type address: int
    :param path: bytom derivation path, defaults to None.
    :type path: str
    :param indexes: bytom derivation indexes, defaults to None.
    :type indexes: list
    :returns:  RefundSolver -- bytom refund solver instance.

    >>> from shuttle.providers.bytom.solver import RefundSolver
    >>> refund_solver = RefundSolver(sender_xprivate_key)
    <shuttle.providers.bytom.solver.RefundSolver object at 0x03FCCA60>
    """

    # Initialization claiming on hash time lock contract (HTLC)
    def __init__(self, xprivate_key, account=1,
                 change=False, address=1, path=None, indexes=None):
        # Checking path and indexes
        if not path and not indexes:
            path = "m/44/153/{}/{}/{}".format(
                account, 1 if change else 0, address)

        # Initialization bytom wallet
        self.bytomHDWallet = BytomHDWallet()
        # XPrivate key of recipient to sign signature
        self.xprivate_key = xprivate_key
        # Setting derivation key
        self.path, self.indexes = path, indexes

    # Signature solve
    def solve(self):
        return self.bytomHDWallet.master_key_from_xprivate(
            xprivate=self.xprivate_key)

