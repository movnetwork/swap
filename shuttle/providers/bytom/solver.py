#!/usr/bin/env python3

from pybytom.wallet import Wallet

from ...utils import sha256
from ..config import bytom
from .htlc import HTLC

# Bytom configuration
bytom = bytom()


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

    def __init__(self, xprivate_key, account=1,
                 change=False, address=1, path=None, indexes=None):
        # Checking path and indexes
        if not path and not indexes:
            path = f"m/44/153/{account}/{1 if change else 0}/{address}"

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

    :param xprivate_key: Bytom sender xprivate key.
    :type xprivate_key: str
    :param secret: secret key.
    :type secret: str
    :param recipient_public: Bytom recipient public key.
    :type recipient_public: str
    :param sender_public: Bytom sender public key.
    :type sender_public: str
    :param sequence: Bytom sequence number(expiration block), defaults to Bytom config sequence.
    :type sequence: int
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

    def __init__(self, xprivate_key, secret, recipient_public, sender_public,
                 sequence=bytom["sequence"], account=1, change=False, address=1, path=None, indexes=None):
        # Checking path and indexes
        if not path and not indexes:
            path = f"m/44/153/{account}/{1 if change else 0}/{address}"

        # Initialization Bytom wallet
        self.wallet = Wallet()
        # XPrivate key of recipient to sign signature
        self.xprivate_key = xprivate_key
        # Secret key to unlock HTLC
        self.secret = secret.encode()
        # Setting derivation key
        self.path, self.indexes = path, indexes
        # HTLC witness agreements
        self.htlc_args = [
            sha256(self.secret).hex(),
            recipient_public,
            sender_public,
            sequence
        ]

    # Signature solve
    def solve(self):
        return self.wallet.from_xprivate_key(
            xprivate_key=self.xprivate_key)

    # HTLC witnesses bytecode
    def witness(self, network=bytom["network"], use_script=False):
        return HTLC(network=network).init(
            secret_hash=self.htlc_args[0], recipient_public=self.htlc_args[1],
            sender_public=self.htlc_args[2], sequence=self.htlc_args[3], use_script=use_script
        ).bytecode()


# Refund HTLC Solver
class RefundSolver:
    """
    Bytom RefundSolver class.

    :param xprivate_key: Bytom sender xprivate key.
    :type xprivate_key: str
    :param secret: secret key.
    :type secret: str
    :param recipient_public: Bytom recipient public key.
    :type recipient_public: str
    :param sender_public: Bytom sender public key.
    :type sender_public: str
    :param sequence: Bytom sequence number(expiration block), defaults to Bytom config sequence.
    :type sequence: int
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

    def __init__(self, xprivate_key, secret, recipient_public, sender_public,
                 sequence=bytom["sequence"], account=1, change=False, address=1, path=None, indexes=None):
        # Checking path and indexes
        if not path and not indexes:
            path = f"m/44/153/{account}/{1 if change else 0}/{address}"

        # Initialization Bytom wallet
        self.wallet = Wallet()
        # XPrivate key of recipient to sign signature
        self.xprivate_key = xprivate_key
        # Secret key to unlock HTLC
        self.secret = secret.encode()
        # Setting derivation key
        self.path, self.indexes = path, indexes
        # HTLC witness agreements
        self.htlc_args = [
            sha256(self.secret).hex(),
            recipient_public,
            sender_public,
            sequence
        ]

    # Signature solve
    def solve(self):
        return self.wallet.from_xprivate_key(
            xprivate_key=self.xprivate_key)

    # HTLC witnesses bytecode
    def witness(self, network=bytom["network"], use_script=False):
        return HTLC(network=network).init(
            secret_hash=self.htlc_args[0], recipient_public=self.htlc_args[1],
            sender_public=self.htlc_args[2], sequence=self.htlc_args[3], use_script=use_script
        ).bytecode()
