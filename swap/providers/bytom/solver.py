#!/usr/bin/env python3

from pybytom.wallet import Wallet
from typing import (
    Optional, List, Tuple
)

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
    :type indexes: list
    :returns: FundSolver -- Bytom fund solver instance.

    >>> from swap.providers.bytom.solver import FundSolver
    >>> sender_xprivate_key = "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"
    >>> fund_solver = FundSolver(xprivate_key=sender_xprivate_key)
    <swap.providers.bytom.solver.FundSolver object at 0x03FCCA60>
    """

    def __init__(self, xprivate_key: str, account: int = 1, change: bool = False,
                 address: int = 1, path: Optional[str] = None, indexes: Optional[List[str]] = None):
        if path is None and not indexes:
            path = config["BIP44"].format(
                account=account, change=(1 if change else 0), address=address
            )

        self._xprivate_key: str = xprivate_key
        self._path: Optional[str] = path
        self._indexes: Optional[List[str]] = indexes

    def solve(self, network: str = config["network"]) -> Tuple[Wallet, Optional[str], Optional[List[str]]]:
        return (
            Wallet(network=network).from_xprivate_key(
                xprivate_key=self._xprivate_key
            ), self._path, self._indexes
        )


class ClaimSolver:
    """
    Bytom Claim solver.

    :param xprivate_key: Bytom sender xprivate key.
    :type xprivate_key: str
    :param secret_key: Secret password/passphrase.
    :type secret_key: str
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
    >>> recipient_xprivate_key = "58dd4094155bbebf2868189231c47e4e0edbd9f74545f843c9537259e1d7a656983aef283d0ccebecc2d33577a9f650b53ac7adff44f48ec839e3346cc22418f"
    >>> bytecode = "02e8032091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"
    >>> claim_solver = ClaimSolver(xprivate_key=recipient_xprivate_key, secret_key="Hello Meheret!", bytecode=bytecode)
    <swap.providers.bytom.solver.ClaimSolver object at 0x03FCCA60>
    """

    def __init__(self, xprivate_key: str, secret_key: str, bytecode: str,
                 account: int = 1, change: bool = False, address: int = 1,
                 path: Optional[str] = None, indexes: Optional[List[str]] = None):
        if path is None and not indexes:
            path = config["BIP44"].format(
                account=account, change=(1 if change else 0), address=address
            )

        self._xprivate_key: str = xprivate_key
        self._secret_key: str = secret_key
        self._path: Optional[str] = path
        self._indexes: Optional[List[str]] = indexes
        self._bytecode: str = bytecode

    def solve(self, network: str = config["network"]) -> Tuple[Wallet, str, Optional[str], Optional[List[str]]]:
        return (
            Wallet(network=network).from_xprivate_key(
                xprivate_key=self._xprivate_key
            ), self._secret_key, self._path, self._indexes
        )

    def witness(self, network: str = config["network"]) -> str:
        return HTLC(network=network).from_bytecode(
            bytecode=self._bytecode
        ).bytecode()


class RefundSolver:
    """
    Bytom Refund solver.

    :param xprivate_key: Bytom sender xprivate key.
    :type xprivate_key: str
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
    >>> sender_xprivate_key = "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"
    >>> bytecode = "02e8032091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"
    >>> refund_solver = RefundSolver(xprivate_key=sender_xprivate_key, bytecode=bytecode)
    <swap.providers.bytom.solver.RefundSolver object at 0x03FCCA60>
    """

    def __init__(self, xprivate_key: str, bytecode: str,
                 account: int = 1, change: bool = False, address: int = 1,
                 path: Optional[str] = None, indexes: Optional[List[str]] = None):
        if path is None and not indexes:
            path = config["BIP44"].format(
                account=account, change=(1 if change else 0), address=address
            )

        self._xprivate_key: str = xprivate_key
        self._path: Optional[str] = path
        self._indexes: Optional[List[str]] = indexes
        self._bytecode: str = bytecode

    def solve(self, network: str = config["network"]) -> Tuple[Wallet, Optional[str], Optional[List[str]]]:
        return (
            Wallet(network=network).from_xprivate_key(
                xprivate_key=self._xprivate_key
            ), self._path, self._indexes
        )

    def witness(self, network: str = config["network"]) -> str:
        return HTLC(network=network).from_bytecode(
            bytecode=self._bytecode
        ).bytecode()
