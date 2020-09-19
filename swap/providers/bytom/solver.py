#!/usr/bin/env python3

from pybytom.wallet import Wallet
from typing import Optional, List, Tuple

from ...utils import sha256
from ..config import bytom
from .htlc import HTLC

# Bytom config
config = bytom()


class FundSolver:
    """
    Bytom Fund solver.

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
    :type indexes: List[str]
    :returns:  FundSolver -- Bytom fund solver instance.

    >>> from swap.providers.bytom.solver import FundSolver
    >>> fund_solver = FundSolver(xprivate_key="205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
    <swap.providers.bytom.solver.FundSolver object at 0x03FCCA60>
    """

    def __init__(self, xprivate_key: str, account: int = 1, change: bool = False,
                 address: int = 1, path: Optional[str] = None, indexes: Optional[List[str]] = None):

        if not path and not indexes:
            path = config["BIP44"].format(
                account=account, change=(1 if change else 0), address=address
            )

        # Set Bytom xprivate key and path/indexes
        self._xprivate_key: str = xprivate_key
        self._path: Optional[str] = path
        self._indexes: Optional[List[str]] = indexes

    def solve(self) -> Tuple[Wallet, Optional[str], Optional[List[str]]]:
        return (
            Wallet().from_xprivate_key(xprivate_key=self._xprivate_key),
            self._path, self._indexes
        )


class ClaimSolver:
    """
    Bytom Claim solver.

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

    >>> from swap.providers.bytom.solver import ClaimSolver
    >>> from swap.utils import sha256
    >>> recipient_xprivate_key = "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"
    >>> claim_solver = ClaimSolver(xprivate_key=recipient_xprivate_key, secret="Hello Meheret!", secret_hash=sha256("Hello Meheret!".encode()).hex(), recipient_public="3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", sender_public="91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2", sequence=1000)
    <swap.providers.bytom.solver.ClaimSolver object at 0x03FCCA60>
    """

    def __init__(self, xprivate_key: str, secret: str, secret_hash: Optional[str] = None,
                 recipient_public: Optional[str] = None, sender_public: Optional[str] = None,
                 sequence: int = config["sequence"], bytecode: Optional[str] = None,
                 account: int = 1, change: bool = False, address: int = 1,
                 path: Optional[str] = None, indexes: Optional[List[str]] = None):

        if not path and not indexes:
            path = config["BIP44"].format(
                account=account, change=(1 if change else 0), address=address
            )

        # Set Bytom xprivate key, secret and path/indexes
        self._xprivate_key: str = xprivate_key
        self._secret: str = secret
        self._path: Optional[str] = path
        self._indexes: Optional[List[str]] = indexes

        # Set witnesses from bytecode or HTLC agreements
        self._bytecode, self._htlc_agreements = bytecode, [
            secret_hash,  # Secret password/passphrase
            recipient_public,  # Bitcoin recipient public key
            sender_public,  # Bitcoin sender public key
            sequence  # Sequence/Expiration block
        ]

    def solve(self) -> Tuple[Wallet, str, Optional[str], Optional[List[str]]]:
        return (
            Wallet().from_xprivate_key(xprivate_key=self._xprivate_key),
            self._secret, self._path, self._indexes
        )

    def witness(self, network: str = config["network"], use_script: bool = False) -> str:
        if self._bytecode:
            return HTLC(network=network).from_bytecode(
                bytecode=self._bytecode
            ).bytecode()
        return HTLC(network=network).init(
            secret_hash=self._htlc_agreements[0],
            recipient_public=self._htlc_agreements[1],
            sender_public=self._htlc_agreements[2],
            sequence=self._htlc_agreements[3],
            use_script=use_script
        ).bytecode()


class RefundSolver:
    """
    Bytom Refund solver.

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

    >>> from swap.providers.bytom.solver import RefundSolver
    >>> from swap.utils import sha256
    >>> sender_xprivate_key = "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"
    >>> refund_solver = RefundSolver(xprivate_key=sender_xprivate_key, secret_hash=sha256("Hello Meheret!".encode()).hex(), recipient_public="3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", sender_public="91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2", sequence=1000)
    <swap.providers.bytom.solver.RefundSolver object at 0x03FCCA60>
    """

    def __init__(self, xprivate_key: str, secret_hash: Optional[str] = None,
                 recipient_public: Optional[str] = None, sender_public: Optional[str] = None,
                 sequence: int = config["sequence"], bytecode: Optional[str] = None,
                 account: int = 1, change: bool = False, address: int = 1,
                 path: Optional[str] = None, indexes: Optional[List[str]] = None):

        if not path and not indexes:
            path = config["BIP44"].format(
                account=account, change=(1 if change else 0), address=address
            )

        # Set Bytom xprivate key, secret and path/indexes
        self._xprivate_key: str = xprivate_key
        self._path: Optional[str] = path
        self._indexes: Optional[List[str]] = indexes

        # Set witnesses from bytecode or HTLC agreements
        self._bytecode, self._htlc_agreements = bytecode, [
            secret_hash,  # Secret password/passphrase
            recipient_public,  # Bitcoin recipient public key
            sender_public,  # Bitcoin sender public key
            sequence  # Sequence/Expiration block
        ]

    def solve(self) -> Tuple[Wallet, Optional[str], Optional[List[str]]]:
        return (
            Wallet().from_xprivate_key(xprivate_key=self._xprivate_key),
            self._path, self._indexes
        )

    def witness(self, network: str = config["network"], use_script: bool = False) -> str:
        if self._bytecode:
            return HTLC(network=network).from_bytecode(
                bytecode=self._bytecode
            ).bytecode()
        return HTLC(network=network).init(
            secret_hash=self._htlc_agreements[0],
            recipient_public=self._htlc_agreements[1],
            sender_public=self._htlc_agreements[2],
            sequence=self._htlc_agreements[3],
            use_script=use_script
        ).bytecode()
