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
    >>> fund_solver = FundSolver(xprivate_key="205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
    <shuttle.providers.bytom.solver.FundSolver object at 0x03FCCA60>
    """

    def __init__(self, xprivate_key,
                 account=1, change=False, address=1, path=None, indexes=None):
        # Checking parameter instances
        if not isinstance(xprivate_key, str):
            raise TypeError("xprivate key must be string format")
        # Checking path and indexes
        if not path and not indexes:
            path = f"m/44/153/{account}/{1 if change else 0}/{address}"

        # Setting Bytom private key
        self.xprivate_key = xprivate_key
        # Setting Bytom derivation key
        self.path, self.indexes = path, indexes

    # Signature solve
    def solve(self):
        return Wallet().from_xprivate_key(
            xprivate_key=self.xprivate_key
        )


# Claim HTLC Solver
class ClaimSolver:
    """
    Bytom ClaimSolver class.

    :param xprivate_key: Bytom sender xprivate key.
    :type xprivate_key: str
    :param secret: Secret password/passphrase.
    :type secret: str
    :param secret_hash: Secret password/passphrase hash, defaults to None.
    :type secret_hash: str
    :param recipient_public: Bytom recipient public key, defaults to None.
    :type recipient_public: str
    :param sender_public: Bytom sender public key, defaults to None.
    :type sender_public: str
    :param sequence: Bytom sequence number(expiration block), defaults to 1000.
    :type sequence: int
    :param bytecode: Bytom witness HTLC bytecode, defaults to None.
    :type bytecode: str
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
    >>> from shuttle.utils import sha256
    >>> recipient_xprivate_key = "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"
    >>> claim_solver = ClaimSolver(xprivate_key=recipient_xprivate_key, secret="Hello Meheret!", secret_hash=sha256("Hello Meheret!".encode()).hex(), recipient_public="3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", sender_public="91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2", sequence=1000)
    <shuttle.providers.bytom.solver.ClaimSolver object at 0x03FCCA60>
    """

    def __init__(self, xprivate_key, secret, secret_hash=None, recipient_public=None,
                 sender_public=None, sequence=bytom["sequence"], bytecode=None,
                 account=1, change=False, address=1, path=None, indexes=None):
        # Checking parameter instances
        if not isinstance(xprivate_key, str):
            raise TypeError("recipient xprivate key must be string format")
        if not isinstance(secret, str):
            raise TypeError("secret must be string format")
        if bytecode is None:
            if not isinstance(secret_hash, str):
                raise TypeError("secret hash must be string format")
            if len(secret_hash) != 64:
                raise ValueError("invalid secret hash, length must be 64")
            if not isinstance(recipient_public, str):
                raise TypeError("recipient public key must be string format")
            if len(recipient_public) != 64:
                raise ValueError("invalid recipient public key, length must be 64")
            if not isinstance(sender_public, str):
                raise TypeError("sender public key must be string format")
            if len(sender_public) != 64:
                raise ValueError("invalid sender public key, length must be 64")
            if not isinstance(sequence, int):
                raise TypeError("sequence must be integer format")
        else:
            if not isinstance(bytecode, str):
                raise TypeError("bytecode must be string format")

        # Checking path and indexes
        if not path and not indexes:
            path = f"m/44/153/{account}/{1 if change else 0}/{address}"
        # Setting Bytom xprivate key and secret password/passphrase
        self.xprivate_key, self.secret = xprivate_key, secret
        # Setting derivation key
        self.path, self.indexes = path, indexes
        # Setting witness from bytecode or HTLC
        self.bytecode, self.htlc_args = bytecode, [
            secret_hash,  # Secret password/passphrase
            recipient_public,  # Bitcoin recipient public key
            sender_public,  # Bitcoin sender public key
            sequence  # Sequence/Expiration block
        ]

    # Signature solve
    def solve(self):
        return Wallet().from_xprivate_key(
            xprivate_key=self.xprivate_key
        )

    # HTLC witnesses bytecode
    def witness(self, network=bytom["network"], use_script=False):
        if self.bytecode:
            return HTLC(network=network).from_bytecode(
                bytecode=self.bytecode
            ).bytecode()
        return HTLC(network=network).init(
            secret_hash=self.htlc_args[0],
            recipient_public=self.htlc_args[1],
            sender_public=self.htlc_args[2],
            sequence=self.htlc_args[3],
            use_script=use_script
        ).bytecode()


# Refund HTLC Solver
class RefundSolver:
    """
    Bytom RefundSolver class.

    :param xprivate_key: Bytom sender xprivate key.
    :type xprivate_key: str
    :param secret_hash: Secret password/passphrase hash, defaults to None.
    :type secret_hash: str
    :param recipient_public: Bytom recipient public key, defaults to None.
    :type recipient_public: str
    :param sender_public: Bytom sender public key, defaults to None.
    :type sender_public: str
    :param sequence: Bytom sequence number(expiration block), defaults to 1000.
    :type sequence: int
    :param bytecode: Bytom witness HTLC bytecode, defaults to None.
    :type bytecode: str
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
    >>> from shuttle.utils import sha256
    >>> sender_xprivate_key = "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"
    >>> refund_solver = RefundSolver(xprivate_key=sender_xprivate_key, secret_hash=sha256("Hello Meheret!".encode()).hex(), recipient_public="3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", sender_public="91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2", sequence=1000)
    <shuttle.providers.bytom.solver.RefundSolver object at 0x03FCCA60>
    """

    def __init__(self, xprivate_key, secret_hash=None, recipient_public=None,
                 sender_public=None, sequence=bytom["sequence"], bytecode=None,
                 account=1, change=False, address=1, path=None, indexes=None):
        # Checking parameter instances
        if not isinstance(xprivate_key, str):
            raise TypeError("recipient xprivate key must be string format")
        if bytecode is None:
            if not isinstance(secret_hash, str):
                raise TypeError("secret hash must be string format")
            if len(secret_hash) != 64:
                raise ValueError("invalid secret hash, length must be 64.")
            if not isinstance(recipient_public, str):
                raise TypeError("recipient public key must be string format")
            if len(recipient_public) != 64:
                raise ValueError("invalid recipient public key, length must be 64.")
            if not isinstance(sender_public, str):
                raise TypeError("sender public key must be string format")
            if len(sender_public) != 64:
                raise ValueError("invalid sender public key, length must be 64.")
            if not isinstance(sequence, int):
                raise TypeError("sequence must be integer format")
        else:
            if not isinstance(bytecode, str):
                raise TypeError("bytecode must be string format")

        # Checking path and indexes
        if not path and not indexes:
            path = f"m/44/153/{account}/{1 if change else 0}/{address}"
        # Setting Bytom xprivate key
        self.xprivate_key = xprivate_key
        # Setting derivation key
        self.path, self.indexes = path, indexes
        # Setting witness from bytecode or HTLC
        self.bytecode, self.htlc_args = bytecode, [
            secret_hash,  # Secret password/passphrase
            recipient_public,  # Bytom recipient public key
            sender_public,  # Bytom sender public key
            sequence  # Sequence/Expiration block
        ]

    # Signature solve
    def solve(self):
        return Wallet().from_xprivate_key(
            xprivate_key=self.xprivate_key
        )

    # HTLC witnesses bytecode
    def witness(self, network=bytom["network"], use_script=False):
        if self.bytecode:
            return HTLC(network=network).from_bytecode(
                bytecode=self.bytecode
            ).bytecode()
        return HTLC(network=network).init(
            secret_hash=self.htlc_args[0],
            recipient_public=self.htlc_args[1],
            sender_public=self.htlc_args[2],
            sequence=self.htlc_args[3],
            use_script=use_script
        ).bytecode()
