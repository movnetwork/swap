#!/usr/bin/env python3

from pybytom.wallet import Wallet


# Fund HTLC Solver
class FundSolver:
    """
    Bytom FundSolver class.

    :param xprivate_key: Bytom sender xprivate key.
    :type xprivate_key: str
    :param account: Bytom derivation account, defaults to 1.
    :type account: int
    :param change: Bytom derivation change, defaults to False.
    :type change: bool
    :param address: Bytom derivation address, defaults to 1.
    :type address: int
    :param path: Bytom derivation path, defaults to None.
    :type path: str
    :param indexes: Bytom derivation indexes, defaults to None.
    :type indexes: list
    :returns:  FundSolver -- Bytom fund solver instance.

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

        # Initialization Bytom wallet
        self.wallet = Wallet()
        # XPrivate key of sender to sign signature
        self.xprivate_key = xprivate_key
        # Setting derivation key
        self.path, self.indexes = path, indexes

    # Signature solve
    def solve(self):
        return self.wallet\
            .from_xprivate_key(xprivate_key=self.xprivate_key)


# Claim HTLC Solver
class ClaimSolver:
    """
    Bytom ClaimSolver class.

    :param secret: secret key.
    :type secret: str
    :param xprivate_key: Bytom sender xprivate key.
    :type xprivate_key: str
    :param account: Bytom derivation account, defaults to 1.
    :type account: int
    :param change: Bytom derivation change, defaults to False.
    :type change: bool
    :param address: Bytom derivation address, defaults to 1.
    :type address: int
    :param path: Bytom derivation path, defaults to None.
    :type path: str
    :param indexes: Bytom derivation indexes, defaults to None.
    :type indexes: list
    :returns:  ClaimSolver -- Bytom claim solver instance.

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

        # Initialization Bytom wallet
        self.wallet = Wallet()
        # Secret key to unlock HTLC
        self.secret = secret.encode()
        # XPrivate key of recipient to sign signature
        self.xprivate_key = xprivate_key
        # Setting derivation key
        self.path, self.indexes = path, indexes

    # Signature solve
    def solve(self):
        return self.wallet.from_xprivate_key(
            xprivate_key=self.xprivate_key)


# Refund HTLC Solver
class RefundSolver:
    """
    Bytom RefundSolver class.

    :param xprivate_key: Bytom sender xprivate key.
    :type xprivate_key: str
    :param account: Bytom derivation account, defaults to 1.
    :type account: int
    :param change: Bytom derivation change, defaults to False.
    :type change: bool
    :param address: Bytom derivation address, defaults to 1.
    :type address: int
    :param path: Bytom derivation path, defaults to None.
    :type path: str
    :param indexes: Bytom derivation indexes, defaults to None.
    :type indexes: list
    :returns:  RefundSolver -- Bytom refund solver instance.

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

        # Initialization Bytom wallet
        self.wallet = Wallet()
        # XPrivate key of recipient to sign signature
        self.xprivate_key = xprivate_key
        # Setting derivation key
        self.path, self.indexes = path, indexes

    # Signature solve
    def solve(self):
        return self.wallet.from_xprivate_key(
            xprivate_key=self.xprivate_key)

