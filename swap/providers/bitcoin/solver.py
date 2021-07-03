#!/usr/bin/env python3

from btcpy.structs.crypto import PrivateKey
from btcpy.structs.sig import (
    P2pkhSolver, IfElseSolver, HashlockSolver, Branch, AbsoluteTimelockSolver
)
from btcpy.structs.script import (
    ScriptBuilder, IfElseScript
)
from btcpy.structs.transaction import Locktime
from typing import Optional, Union

from ..config import bitcoin as config
from .wallet import Wallet
from .htlc import HTLC


class FundSolver:
    """
    Bitcoin Fund solver.

    :param xprivate_key: Bitcoin sender root xprivate key.
    :type xprivate_key: str
    :param account: Bitcoin derivation account, defaults to ``0``.
    :type account: int
    :param change: Bitcoin derivation change, defaults to ``False``.
    :type change: bool
    :param address: Bitcoin derivation address, defaults to ``0``.
    :type address: int
    :param path: Bitcoin derivation path, defaults to ``None``.
    :type path: str
    :param strict: Strict for must be root xprivate key, default to ``True``.
    :type strict: bool

    :returns: FundSolver -- Bitcoin fund solver instance.

    >>> from swap.providers.bitcoin.solver import FundSolver
    >>> sender_xprivate_key: str = "tprv8ZgxMBicQKsPeMHMJAc6uWGYiGqi1MVM2ybmzXL2TAoDpQe85uyDpdT7mv7Nhdu5rTCBEKLZsd9KyP2LQZJzZTvgVQvENArgU8e6DoYBiXf"
    >>> fund_solver: FundSolver = FundSolver(xprivate_key=sender_xprivate_key, path="m/44'/1'/0'/0/0")
    <swap.providers.bitcoin.solver.FundSolver object at 0x03FCCA60>
    """

    def __init__(self, xprivate_key: str, account: int = 0, change: bool = False, address: int = 0,
                 path: Optional[str] = None, strict: bool = True):

        self._xprivate_key: str = xprivate_key
        self._strict: bool = strict
        self._path: Optional[str] = path

        self._account: int = account
        self._change: bool = change
        self._address: int = address

    def solve(self, network: str = config["network"]) -> P2pkhSolver:

        if self._path is None:
            self._path = config["bip44_path"].format(
                account=self._account, change=(1 if self._change else 0), address=self._address
            )

        return P2pkhSolver(
            privk=PrivateKey.unhexlify(
                hexa=Wallet(network=network).from_root_xprivate_key(
                    xprivate_key=self._xprivate_key, strict=self._strict
                ).from_path(
                    path=self._path
                ).private_key()
            )
        )


class WithdrawSolver:
    """
    Bitcoin Withdraw solver.

    :param xprivate_key: Bitcoin recipient root xprivate key.
    :type xprivate_key: str
    :param secret_key: Secret password/passphrase.
    :type secret_key: str
    :param bytecode: Bitcoin witness HTLC bytecode.
    :type bytecode: str
    :param account: Bitcoin derivation account, defaults to ``0``.
    :type account: int
    :param change: Bitcoin derivation change, defaults to ``False``.
    :type change: bool
    :param address: Bitcoin derivation address, defaults to ``0``.
    :type address: int
    :param path: Bitcoin derivation path, defaults to ``None``.
    :type path: str
    :param strict: Strict for must be root xprivate key, default to ``True``.
    :type strict: bool

    :returns: WithdrawSolver -- Bitcoin withdraw solver instance.

    >>> from swap.providers.bitcoin.solver import WithdrawSolver
    >>> recipient_xprivate_key: str = "tprv8ZgxMBicQKsPf949JcuVFLXPJ5m4VKe33gVX3FYVZYVHr2dChU8K66aEQcPdHpUgACq5GQu81Z4e3QN1vxCrV4pxcUcXHoRTamXBRaPdJhW"
    >>> bytecode: str = "63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a9140e259e08f2ec9fc99a92b6f66fdfcb3c7914fd6888ac6702e803b27576a91433ecab3d67f0e2bde43e52f41ec1ecbdc73f11f888ac68"
    >>> withdraw_solver: WithdrawSolver = WithdrawSolver(xprivate_key=recipient_xprivate_key, secret_key="Hello Meheret!", bytecode=bytecode, path="m/44'/1'/0'/0/0")
    <swap.providers.bitcoin.solver.WithdrawSolver object at 0x03FCCA60>
    """

    def __init__(self, xprivate_key: str, secret_key: str, bytecode: str, account: int = 0,
                 change: bool = False, address: int = 0, path: Optional[str] = None, strict: bool = True):

        self._xprivate_key: str = xprivate_key
        self._strict: bool = strict
        self._secret_key: str = secret_key
        self._path: Optional[str] = path
        self._bytecode: str = bytecode

        self._account: int = account
        self._change: bool = change
        self._address: int = address

    def solve(self, network: str = config["network"]) -> IfElseSolver:

        if self._path is None:
            self._path = config["bip44_path"].format(
                account=self._account, change=(1 if self._change else 0), address=self._address
            )

        return IfElseSolver(
            branch=Branch.IF,
            inner_solver=HashlockSolver(
                preimage=self._secret_key.encode(),
                inner_solver=P2pkhSolver(
                    privk=PrivateKey.unhexlify(
                        hexa=Wallet(network=network).from_root_xprivate_key(
                            xprivate_key=self._xprivate_key, strict=self._strict
                        ).from_path(
                            path=self._path
                        ).private_key()
                    )
                )
            )
        )

    def witness(self, network: str = config["network"]) -> Union[IfElseScript, ScriptBuilder]:
        return HTLC(network=network).from_bytecode(
            bytecode=self._bytecode
        ).script


class RefundSolver:
    """
    Bitcoin Refund solver.

    :param xprivate_key: Bitcoin sender root xprivate key.
    :type xprivate_key: str
    :param bytecode: Bitcoin witness HTLC bytecode..
    :type bytecode: str
    :param endtime: Bitcoin witness expiration block timestamp.
    :type endtime: int
    :param account: Bitcoin derivation account, defaults to ``0``.
    :type account: int
    :param change: Bitcoin derivation change, defaults to ``False``.
    :type change: bool
    :param address: Bitcoin derivation address, defaults to ``0``.
    :type address: int
    :param path: Bitcoin derivation path, defaults to ``None``.
    :type path: str
    :param strict: Strict for must be root xprivate key, default to ``True``.
    :type strict: bool

    :returns: RefundSolver -- Bitcoin refund solver instance.

    >>> from swap.providers.bitcoin.solver import RefundSolver
    >>> sender_xprivate_key: str = "tprv8ZgxMBicQKsPeMHMJAc6uWGYiGqi1MVM2ybmzXL2TAoDpQe85uyDpdT7mv7Nhdu5rTCBEKLZsd9KyP2LQZJzZTvgVQvENArgU8e6DoYBiXf"
    >>> bytecode: str = "63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a9140e259e08f2ec9fc99a92b6f66fdfcb3c7914fd6888ac6702e803b27576a91433ecab3d67f0e2bde43e52f41ec1ecbdc73f11f888ac68"
    >>> refund_solver: RefundSolver = RefundSolver(xprivate_key=sender_xprivate_key, bytecode=bytecode, endtime=1000, path="m/44'/1'/0'/0/0")
    <swap.providers.bitcoin.solver.RefundSolver object at 0x03FCCA60>
    """

    def __init__(self, xprivate_key: str, bytecode: str, endtime: int, account: int = 0,
                 change: bool = False, address: int = 0, path: Optional[str] = None, strict: bool = True):

        self._xprivate_key: str = xprivate_key
        self._strict: bool = strict
        self._endtime: int = endtime
        self._path: Optional[str] = path
        self._bytecode: str = bytecode

        self._account: int = account
        self._change: bool = change
        self._address: int = address

    def solve(self, network: str = config["network"]) -> IfElseSolver:

        if self._path is None:
            self._path = config["bip44_path"].format(
                account=self._account, change=(1 if self._change else 0), address=self._address
            )

        return IfElseSolver(
            branch=Branch.ELSE,
            inner_solver=AbsoluteTimelockSolver(
                locktime=Locktime(
                    n=self._endtime
                ),
                inner_solver=P2pkhSolver(
                    privk=PrivateKey.unhexlify(
                        hexa=Wallet(network=network).from_root_xprivate_key(
                            xprivate_key=self._xprivate_key, strict=self._strict
                        ).from_path(
                            path=self._path
                        ).private_key()
                    )
                )
            )
        )

    def witness(self, network: str = config["network"]) -> Union[IfElseScript, ScriptBuilder]:
        return HTLC(network=network).from_bytecode(
            bytecode=self._bytecode
        ).script
