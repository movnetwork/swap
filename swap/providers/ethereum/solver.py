#!/usr/bin/env python3

from typing import Optional

from ..config import ethereum as config
from .wallet import Wallet


class FundSolver:
    """
    Ethereum Fund solver.

    :param xprivate_key: Ethereum sender xprivate key.
    :type xprivate_key: str
    :param account: Ethereum derivation account, defaults to 0.
    :type account: int
    :param change: Ethereum derivation change, defaults to False.
    :type change: bool
    :param address: Ethereum derivation address, defaults to 0.
    :type address: int
    :param path: Ethereum derivation path, defaults to None.
    :type path: str

    :returns: FundSolver -- Ethereum fund solver instance.

    >>> from swap.providers.ethereum.solver import FundSolver
    >>> sender_root_xprivate_key: str = "xprv9s21ZrQH143K3XihXQBN8Uar2WBtrjSzK2oRDEGQ25pA2kKAADoQXaiiVXht163ZTrdtTXfM4GqNRE9gWQHky25BpvBQuuhNCM3SKwWTPNJ"
    >>> fund_solver: FundSolver = FundSolver(xprivate_key=sender_root_xprivate_key)
    <swap.providers.ethereum.solver.FundSolver object at 0x03FCCA60>
    """

    def __init__(self, xprivate_key: str, account: int = 0,
                 change: bool = False, address: int = 0, path: Optional[str] = None):
        if path is None:
            path = config["bip44_path"].format(
                account=account, change=(1 if change else 0), address=address
            )

        self._xprivate_key: str = xprivate_key
        self._path: Optional[str] = path

    def solve(self, network: str = config["network"]) -> Wallet:
        return Wallet(network=network).from_root_xprivate_key(
            xprivate_key=self._xprivate_key
        ).from_path(path=self._path)


class WithdrawSolver:
    """
    Ethereum Withdraw solver.

    :param xprivate_key: Ethereum sender xprivate key.
    :type xprivate_key: str
    :param account: Ethereum derivation account, defaults to 0.
    :type account: int
    :param change: Ethereum derivation change, defaults to False.
    :type change: bool
    :param address: Ethereum derivation address, defaults to 0.
    :type address: int
    :param path: Ethereum derivation path, defaults to None.
    :type path: str

    :returns: WithdrawSolver -- Ethereum withdraw solver instance.

    >>> from swap.providers.ethereum.solver import WithdrawSolver
    >>> recipient_root_xprivate_key: str = "xprv9s21ZrQH143K3XihXQBN8Uar2WBtrjSzK2oRDEGQ25pA2kKAADoQXaiiVXht163ZTrdtTXfM4GqNRE9gWQHky25BpvBQuuhNCM3SKwWTPNJ"
    >>> withdraw_solver: WithdrawSolver = WithdrawSolver(xprivate_key=recipient_root_xprivate_key)
    <swap.providers.ethereum.solver.WithdrawSolver object at 0x03FCCA60>
    """

    def __init__(self, xprivate_key: str, account: int = 0,
                 change: bool = False, address: int = 0, path: Optional[str] = None):
        if path is None:
            path = config["bip44_path"].format(
                account=account, change=(1 if change else 0), address=address
            )

        self._xprivate_key: str = xprivate_key
        self._path: Optional[str] = path

    def solve(self, network: str = config["network"]) -> Wallet:
        return Wallet(network=network).from_root_xprivate_key(
            xprivate_key=self._xprivate_key
        ).from_path(path=self._path)


class RefundSolver:
    """
    Ethereum Refund solver.

    :param xprivate_key: Ethereum sender xprivate key.
    :type xprivate_key: str
    :param account: Ethereum derivation account, defaults to 0.
    :type account: int
    :param change: Ethereum derivation change, defaults to False.
    :type change: bool
    :param address: Ethereum derivation address, defaults to 0.
    :type address: int
    :param path: Ethereum derivation path, defaults to None.
    :type path: str

    :returns: RefundSolver -- Ethereum refund solver instance.

    >>> from swap.providers.ethereum.solver import RefundSolver
    >>> sender_root_xprivate_key: str = "xprv9s21ZrQH143K3XihXQBN8Uar2WBtrjSzK2oRDEGQ25pA2kKAADoQXaiiVXht163ZTrdtTXfM4GqNRE9gWQHky25BpvBQuuhNCM3SKwWTPNJ"
    >>> refund_solver: RefundSolver = RefundSolver(xprivate_key=sender_root_xprivate_key)
    <swap.providers.ethereum.solver.RefundSolver object at 0x03FCCA60>
    """

    def __init__(self, xprivate_key: str, account: int = 0,
                 change: bool = False, address: int = 0, path: Optional[str] = None):
        if path is None:
            path = config["bip44_path"].format(
                account=account, change=(1 if change else 0), address=address
            )

        self._xprivate_key: str = xprivate_key
        self._path: Optional[str] = path

    def solve(self, network: str = config["network"]) -> Wallet:
        return Wallet(network=network).from_root_xprivate_key(
            xprivate_key=self._xprivate_key
        ).from_path(path=self._path)
