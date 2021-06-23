#!/usr/bin/env python3

from base64 import b64encode, b64decode
from eth_account.datastructures import SignedTransaction
from web3.types import Wei
from typing import (
    Optional, Union
)

import json

from ...utils import clean_transaction_raw
from ...exceptions import (
    TransactionRawError, UnitError
)
from ..config import xinfin as config
from .transaction import Transaction
from .solver import (
    FundSolver, WithdrawSolver, RefundSolver
)
from .wallet import Wallet
from .utils import (
    is_transaction_raw, amount_unit_converter
)


class Signature(Transaction):
    """
    XinFin Signature.

    :param network: XinFin network, defaults to ``mainnet``.
    :type network: str
    :param provider: XinFin network provider, defaults to ``http``.
    :type provider: str
    :param token: Infura API endpoint token, defaults to ``4414fea5f7454211956b1627621450b4``.
    :type token: str

    :returns: Signature -- XinFin signature instance.

    .. note::
        XinFin has only two networks, ``mainnet`` and ``testnet``.
    """

    def __init__(self, network: str = config["network"], provider: str = config["provider"],
                 token: Optional[str] = None):
        super().__init__(
            network=network, provider=provider, token=token
        )

        self._signed_raw: Optional[str] = None

    def fee(self, unit: str = config["unit"]) -> Union[Wei, int, float]:
        """
        Get XinFin signature fee.

        :param unit: XinFin unit, default to ``Wie``.
        :type unit: str

        :returns: Wei, int, float -- XinFin signature fee.

        >>> from swap.providers.xinfin.signature import Signature
        >>> from swap.providers.xinfin.solver import FundSolver
        >>> signature: Signature = Signature(network="mainnet")
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="xprv9s21ZrQH143K3Y3pdbkbjreZQ9RVmqTLhRgf86uZyCJk2ou36YdUJt5frjwihGWmV1fQEDioiGZXWXUbHLy3kQf5xmhvhp8dZ2tfn6tgGUj")
        >>> signature.sign(transaction_raw="eyJmZWUiOiAxMzg0NDgsICJ0cmFuc2FjdGlvbiI6IHsiY2hhaW5JZCI6IDEzMzcsICJmcm9tIjogIjB4NjllMDRmZTE2YzlBNkE4MzA3NkIzYzJkYzRiNEJjMjFiNWQ5QTIwQyIsICJ2YWx1ZSI6IDMwMDAwMDAwMDAwMDAwMDAwMDAsICJub25jZSI6IDEsICJnYXMiOiAxMzg0NDgsICJnYXNQcmljZSI6IDIwMDAwMDAwMDAwLCAidG8iOiAiMHhlYUVhQzgxZGE1RTM4NkU4Q2E0RGUxZTY0ZDQwYTEwRTQ2OEE1YjQwIiwgImRhdGEiOiAiMHhmNGZkMzA2MjNhMjZkYTgyZWFkMTVhODA1MzNhMDI2OTY2NTZiMTRiNWRiZmQ4NGViMTQ3OTBmMmUxYmU1ZTllNDU4MjBlZWIwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDBkNzdlMGQyZWVmOTA1Y2ZiMzljM2M0Yjk1MmVkMjc4ZDU4Zjk2ZTFmMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwNjllMDRmZTE2YzlhNmE4MzA3NmIzYzJkYzRiNGJjMjFiNWQ5YTIwYzAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwNjBjZTRiNzIifSwgInNpZ25hdHVyZSI6IG51bGwsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJldGhlcmV1bV9mdW5kX3Vuc2lnbmVkIn0", solver=fund_solver)
        >>> signature.fee(unit="Wei")
        1532774
        """

        # Check transaction
        if not self._transaction:
            raise ValueError("Transaction is none, build transaction first.")

        if unit not in ["XDC", "Gwei", "Wei"]:
            raise UnitError(f"Invalid XinFin '{unit}' unit", "choose only 'XDC', 'Gwei' or 'Wei' units.")
        return self._fee if unit == "Wei" else \
            amount_unit_converter(amount=self._fee, unit=f"Wei2{unit}")

    def hash(self) -> Optional[str]:
        """
        Get XinFin signature has.

        :returns: str -- XinFin signature hash.

        >>> from swap.providers.xinfin.signature import Signature
        >>> from swap.providers.xinfin.solver import FundSolver
        >>> signature: Signature = Signature(network="mainnet")
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="xprv9s21ZrQH143K3Y3pdbkbjreZQ9RVmqTLhRgf86uZyCJk2ou36YdUJt5frjwihGWmV1fQEDioiGZXWXUbHLy3kQf5xmhvhp8dZ2tfn6tgGUj")
        >>> signature.sign(transaction_raw="eyJmZWUiOiAxMzg0NDgsICJ0cmFuc2FjdGlvbiI6IHsiY2hhaW5JZCI6IDEzMzcsICJmcm9tIjogIjB4NjllMDRmZTE2YzlBNkE4MzA3NkIzYzJkYzRiNEJjMjFiNWQ5QTIwQyIsICJ2YWx1ZSI6IDMwMDAwMDAwMDAwMDAwMDAwMDAsICJub25jZSI6IDEsICJnYXMiOiAxMzg0NDgsICJnYXNQcmljZSI6IDIwMDAwMDAwMDAwLCAidG8iOiAiMHhlYUVhQzgxZGE1RTM4NkU4Q2E0RGUxZTY0ZDQwYTEwRTQ2OEE1YjQwIiwgImRhdGEiOiAiMHhmNGZkMzA2MjNhMjZkYTgyZWFkMTVhODA1MzNhMDI2OTY2NTZiMTRiNWRiZmQ4NGViMTQ3OTBmMmUxYmU1ZTllNDU4MjBlZWIwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDBkNzdlMGQyZWVmOTA1Y2ZiMzljM2M0Yjk1MmVkMjc4ZDU4Zjk2ZTFmMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwNjllMDRmZTE2YzlhNmE4MzA3NmIzYzJkYzRiNGJjMjFiNWQ5YTIwYzAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwNjBjZTRiNzIifSwgInNpZ25hdHVyZSI6IG51bGwsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJldGhlcmV1bV9mdW5kX3Vuc2lnbmVkIn0", solver=fund_solver)
        >>> signature.hash()
        "0xe87b1aefec9fecbb7699e16d101e757e4825db157eb94d2e71ecfaf17fd3d75d"
        """

        # Check transaction
        if not self._transaction:
            raise ValueError("Transaction is none, build transaction first.")

        return self._signature["hash"] if self._signature else None

    def json(self) -> dict:
        """
        Get XinFin signature json.

        :returns: dict -- XinFin signature json.

        >>> from swap.providers.xinfin.signature import Signature
        >>> from swap.providers.xinfin.solver import FundSolver
        >>> signature: Signature = Signature(network="mainnet")
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="xprv9s21ZrQH143K3Y3pdbkbjreZQ9RVmqTLhRgf86uZyCJk2ou36YdUJt5frjwihGWmV1fQEDioiGZXWXUbHLy3kQf5xmhvhp8dZ2tfn6tgGUj")
        >>> signature.sign(transaction_raw="eyJmZWUiOiAxMzg0NDgsICJ0cmFuc2FjdGlvbiI6IHsiY2hhaW5JZCI6IDEzMzcsICJmcm9tIjogIjB4NjllMDRmZTE2YzlBNkE4MzA3NkIzYzJkYzRiNEJjMjFiNWQ5QTIwQyIsICJ2YWx1ZSI6IDMwMDAwMDAwMDAwMDAwMDAwMDAsICJub25jZSI6IDEsICJnYXMiOiAxMzg0NDgsICJnYXNQcmljZSI6IDIwMDAwMDAwMDAwLCAidG8iOiAiMHhlYUVhQzgxZGE1RTM4NkU4Q2E0RGUxZTY0ZDQwYTEwRTQ2OEE1YjQwIiwgImRhdGEiOiAiMHhmNGZkMzA2MjNhMjZkYTgyZWFkMTVhODA1MzNhMDI2OTY2NTZiMTRiNWRiZmQ4NGViMTQ3OTBmMmUxYmU1ZTllNDU4MjBlZWIwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDBkNzdlMGQyZWVmOTA1Y2ZiMzljM2M0Yjk1MmVkMjc4ZDU4Zjk2ZTFmMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwNjllMDRmZTE2YzlhNmE4MzA3NmIzYzJkYzRiNGJjMjFiNWQ5YTIwYzAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwNjBjZTRiNzIifSwgInNpZ25hdHVyZSI6IG51bGwsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJldGhlcmV1bV9mdW5kX3Vuc2lnbmVkIn0", solver=fund_solver)
        >>> signature.json()
        {'chainId': 1337, 'from': 'xdc69e04fe16c9A6A83076B3c2dc4b4Bc21b5d9A20C', 'value': 3000000000000000000, 'nonce': 1, 'gas': 138448, 'gasPrice': 20000000000, 'to': '0xeaEaC81da5E386E8Ca4De1e64d40a10E468A5b40', 'data': '0xf4fd30623a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb000000000000000000000000d77e0d2eef905cfb39c3c4b952ed278d58f96e1f00000000000000000000000069e04fe16c9a6a83076b3c2dc4b4bc21b5d9a20c0000000000000000000000000000000000000000000000000000000060ce4b72'}
        """

        # Check transaction
        if not self._transaction:
            raise ValueError("Transaction is none, build transaction first.")

        return self._transaction

    def raw(self) -> Optional[str]:
        """
        Get XinFin signature raw.

        :returns: str -- XinFin signature raw.

        >>> from swap.providers.xinfin.signature import Signature
        >>> from swap.providers.xinfin.solver import FundSolver
        >>> signature: Signature = Signature(network="mainnet")
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="xprv9s21ZrQH143K3Y3pdbkbjreZQ9RVmqTLhRgf86uZyCJk2ou36YdUJt5frjwihGWmV1fQEDioiGZXWXUbHLy3kQf5xmhvhp8dZ2tfn6tgGUj")
        >>> signature.sign(transaction_raw="eyJmZWUiOiAxMzg0NDgsICJ0cmFuc2FjdGlvbiI6IHsiY2hhaW5JZCI6IDEzMzcsICJmcm9tIjogIjB4NjllMDRmZTE2YzlBNkE4MzA3NkIzYzJkYzRiNEJjMjFiNWQ5QTIwQyIsICJ2YWx1ZSI6IDMwMDAwMDAwMDAwMDAwMDAwMDAsICJub25jZSI6IDEsICJnYXMiOiAxMzg0NDgsICJnYXNQcmljZSI6IDIwMDAwMDAwMDAwLCAidG8iOiAiMHhlYUVhQzgxZGE1RTM4NkU4Q2E0RGUxZTY0ZDQwYTEwRTQ2OEE1YjQwIiwgImRhdGEiOiAiMHhmNGZkMzA2MjNhMjZkYTgyZWFkMTVhODA1MzNhMDI2OTY2NTZiMTRiNWRiZmQ4NGViMTQ3OTBmMmUxYmU1ZTllNDU4MjBlZWIwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDBkNzdlMGQyZWVmOTA1Y2ZiMzljM2M0Yjk1MmVkMjc4ZDU4Zjk2ZTFmMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwNjllMDRmZTE2YzlhNmE4MzA3NmIzYzJkYzRiNGJjMjFiNWQ5YTIwYzAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwNjBjZTRiNzIifSwgInNpZ25hdHVyZSI6IG51bGwsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJldGhlcmV1bV9mdW5kX3Vuc2lnbmVkIn0", solver=fund_solver)
        >>> signature.raw()
        "0xf8f4018504a817c80083021cd094eaeac81da5e386e8ca4de1e64d40a10e468a5b408829a2241af62c0000b884f4fd30623a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb000000000000000000000000d77e0d2eef905cfb39c3c4b952ed278d58f96e1f00000000000000000000000069e04fe16c9a6a83076b3c2dc4b4bc21b5d9a20c0000000000000000000000000000000000000000000000000000000060ce4b72820a95a06dcfc6e385cbcad6b093d0a2351f516c61d94368fd80d94f48bf5663070ee57da0570c837b594577469516b29b9902cc7df978641deaa87e5f6576afcf30589ef2"
        """

        # Check transaction
        if not self._transaction:
            raise ValueError("Transaction is none, build transaction first.")

        return self._signature["rawTransaction"] if self._signature else None

    def type(self) -> str:
        """
        Get XinFin signature type.

        :returns: str -- XinFin signature type.

        >>> from swap.providers.xinfin.signature import Signature
        >>> from swap.providers.xinfin.solver import FundSolver
        >>> signature: Signature = Signature(network="mainnet")
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="xprv9s21ZrQH143K3Y3pdbkbjreZQ9RVmqTLhRgf86uZyCJk2ou36YdUJt5frjwihGWmV1fQEDioiGZXWXUbHLy3kQf5xmhvhp8dZ2tfn6tgGUj")
        >>> signature.sign(transaction_raw="eyJmZWUiOiAxMzg0NDgsICJ0cmFuc2FjdGlvbiI6IHsiY2hhaW5JZCI6IDEzMzcsICJmcm9tIjogIjB4NjllMDRmZTE2YzlBNkE4MzA3NkIzYzJkYzRiNEJjMjFiNWQ5QTIwQyIsICJ2YWx1ZSI6IDMwMDAwMDAwMDAwMDAwMDAwMDAsICJub25jZSI6IDEsICJnYXMiOiAxMzg0NDgsICJnYXNQcmljZSI6IDIwMDAwMDAwMDAwLCAidG8iOiAiMHhlYUVhQzgxZGE1RTM4NkU4Q2E0RGUxZTY0ZDQwYTEwRTQ2OEE1YjQwIiwgImRhdGEiOiAiMHhmNGZkMzA2MjNhMjZkYTgyZWFkMTVhODA1MzNhMDI2OTY2NTZiMTRiNWRiZmQ4NGViMTQ3OTBmMmUxYmU1ZTllNDU4MjBlZWIwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDBkNzdlMGQyZWVmOTA1Y2ZiMzljM2M0Yjk1MmVkMjc4ZDU4Zjk2ZTFmMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwNjllMDRmZTE2YzlhNmE4MzA3NmIzYzJkYzRiNGJjMjFiNWQ5YTIwYzAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwNjBjZTRiNzIifSwgInNpZ25hdHVyZSI6IG51bGwsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJldGhlcmV1bV9mdW5kX3Vuc2lnbmVkIn0", solver=fund_solver)
        >>> signature.type()
        "xinfin_fund_signed"
        """

        # Check transaction
        if not self._transaction:
            raise ValueError("Transaction is none, build transaction first.")

        return self._type

    def sign(self, transaction_raw: str, solver: Union[FundSolver, WithdrawSolver, RefundSolver]) -> \
            Union["FundSignature", "WithdrawSignature", "RefundSignature"]:
        """
        Sign XinFin unsigned transaction raw.

        :param transaction_raw: XinFin unsigned transaction raw.
        :type transaction_raw: str
        :param solver: XinFin solver.
        :type solver: xinfin.solver.FundSolver, xinfin.solver.WithdrawSolver, xinfin.solver.RefundSolver

        :returns: FundSignature, WithdrawSignature, RefundSignature -- XinFin signature instance.

        >>> from swap.providers.xinfin.signature import Signature
        >>> from swap.providers.xinfin.solver import FundSolver
        >>> signature: Signature = Signature(network="mainnet")
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="xprv9s21ZrQH143K3Y3pdbkbjreZQ9RVmqTLhRgf86uZyCJk2ou36YdUJt5frjwihGWmV1fQEDioiGZXWXUbHLy3kQf5xmhvhp8dZ2tfn6tgGUj")
        >>> signature.sign(transaction_raw="eyJmZWUiOiAxMzg0NDgsICJ0cmFuc2FjdGlvbiI6IHsiY2hhaW5JZCI6IDEzMzcsICJmcm9tIjogIjB4NjllMDRmZTE2YzlBNkE4MzA3NkIzYzJkYzRiNEJjMjFiNWQ5QTIwQyIsICJ2YWx1ZSI6IDMwMDAwMDAwMDAwMDAwMDAwMDAsICJub25jZSI6IDEsICJnYXMiOiAxMzg0NDgsICJnYXNQcmljZSI6IDIwMDAwMDAwMDAwLCAidG8iOiAiMHhlYUVhQzgxZGE1RTM4NkU4Q2E0RGUxZTY0ZDQwYTEwRTQ2OEE1YjQwIiwgImRhdGEiOiAiMHhmNGZkMzA2MjNhMjZkYTgyZWFkMTVhODA1MzNhMDI2OTY2NTZiMTRiNWRiZmQ4NGViMTQ3OTBmMmUxYmU1ZTllNDU4MjBlZWIwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDBkNzdlMGQyZWVmOTA1Y2ZiMzljM2M0Yjk1MmVkMjc4ZDU4Zjk2ZTFmMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwNjllMDRmZTE2YzlhNmE4MzA3NmIzYzJkYzRiNGJjMjFiNWQ5YTIwYzAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwNjBjZTRiNzIifSwgInNpZ25hdHVyZSI6IG51bGwsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJldGhlcmV1bV9mdW5kX3Vuc2lnbmVkIn0", solver=fund_solver)
        <swap.providers.xinfin.signature.FundSignature object at 0x0409DAF0>
        """

        if not is_transaction_raw(transaction_raw=transaction_raw):
            raise TransactionRawError("Invalid Bytom unsigned transaction raw.")

        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

        self._type = loaded_transaction_raw["type"]
        if loaded_transaction_raw["type"] == "xinfin_fund_unsigned":
            return FundSignature(network=self._network).sign(
                transaction_raw=transaction_raw, solver=solver
            )
        elif loaded_transaction_raw["type"] == "xinfin_withdraw_unsigned":
            return WithdrawSignature(network=self._network).sign(
                transaction_raw=transaction_raw, solver=solver
            )
        elif loaded_transaction_raw["type"] == "xinfin_refund_unsigned":
            return RefundSignature(network=self._network).sign(
                transaction_raw=transaction_raw, solver=solver
            )

    def signature(self) -> dict:
        """
        Get XinFin signature.

        :returns: dict -- XinFin signature.

        >>> from swap.providers.xinfin.signature import Signature
        >>> from swap.providers.xinfin.solver import FundSolver
        >>> signature: Signature = Signature(network="mainnet")
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="xprv9s21ZrQH143K3Y3pdbkbjreZQ9RVmqTLhRgf86uZyCJk2ou36YdUJt5frjwihGWmV1fQEDioiGZXWXUbHLy3kQf5xmhvhp8dZ2tfn6tgGUj")
        >>> signature.sign(transaction_raw="eyJmZWUiOiAxMzg0NDgsICJ0cmFuc2FjdGlvbiI6IHsiY2hhaW5JZCI6IDEzMzcsICJmcm9tIjogIjB4NjllMDRmZTE2YzlBNkE4MzA3NkIzYzJkYzRiNEJjMjFiNWQ5QTIwQyIsICJ2YWx1ZSI6IDMwMDAwMDAwMDAwMDAwMDAwMDAsICJub25jZSI6IDEsICJnYXMiOiAxMzg0NDgsICJnYXNQcmljZSI6IDIwMDAwMDAwMDAwLCAidG8iOiAiMHhlYUVhQzgxZGE1RTM4NkU4Q2E0RGUxZTY0ZDQwYTEwRTQ2OEE1YjQwIiwgImRhdGEiOiAiMHhmNGZkMzA2MjNhMjZkYTgyZWFkMTVhODA1MzNhMDI2OTY2NTZiMTRiNWRiZmQ4NGViMTQ3OTBmMmUxYmU1ZTllNDU4MjBlZWIwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDBkNzdlMGQyZWVmOTA1Y2ZiMzljM2M0Yjk1MmVkMjc4ZDU4Zjk2ZTFmMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwNjllMDRmZTE2YzlhNmE4MzA3NmIzYzJkYzRiNGJjMjFiNWQ5YTIwYzAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwNjBjZTRiNzIifSwgInNpZ25hdHVyZSI6IG51bGwsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJldGhlcmV1bV9mdW5kX3Vuc2lnbmVkIn0", solver=fund_solver)
        >>> signature.signature()
        {'hash': '0xe87b1aefec9fecbb7699e16d101e757e4825db157eb94d2e71ecfaf17fd3d75d', 'rawTransaction': '0xf8f4018504a817c80083021cd094eaeac81da5e386e8ca4de1e64d40a10e468a5b408829a2241af62c0000b884f4fd30623a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb000000000000000000000000d77e0d2eef905cfb39c3c4b952ed278d58f96e1f00000000000000000000000069e04fe16c9a6a83076b3c2dc4b4bc21b5d9a20c0000000000000000000000000000000000000000000000000000000060ce4b72820a95a06dcfc6e385cbcad6b093d0a2351f516c61d94368fd80d94f48bf5663070ee57da0570c837b594577469516b29b9902cc7df978641deaa87e5f6576afcf30589ef2', 'r': 49669210517760089961057755545670916457545361634072315135726343721882166945149, 's': 39373327445767756604614462296774202164268870502915897592346222361951457550066, 'v': 2709}
        """

        # Check transaction
        if not self._transaction:
            raise ValueError("Transaction is none, build transaction first.")

        return self._signature

    def transaction_raw(self) -> str:
        """
        Get XinFin signed transaction raw.

        :returns: str -- XinFin signed transaction raw.

        >>> from swap.providers.xinfin.signature import Signature
        >>> from swap.providers.xinfin.solver import FundSolver
        >>> signature: Signature = Signature(network="mainnet")
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="xprv9s21ZrQH143K3Y3pdbkbjreZQ9RVmqTLhRgf86uZyCJk2ou36YdUJt5frjwihGWmV1fQEDioiGZXWXUbHLy3kQf5xmhvhp8dZ2tfn6tgGUj")
        >>> signature.sign(transaction_raw="eyJmZWUiOiAxMzg0NDgsICJ0cmFuc2FjdGlvbiI6IHsiY2hhaW5JZCI6IDEzMzcsICJmcm9tIjogIjB4NjllMDRmZTE2YzlBNkE4MzA3NkIzYzJkYzRiNEJjMjFiNWQ5QTIwQyIsICJ2YWx1ZSI6IDMwMDAwMDAwMDAwMDAwMDAwMDAsICJub25jZSI6IDEsICJnYXMiOiAxMzg0NDgsICJnYXNQcmljZSI6IDIwMDAwMDAwMDAwLCAidG8iOiAiMHhlYUVhQzgxZGE1RTM4NkU4Q2E0RGUxZTY0ZDQwYTEwRTQ2OEE1YjQwIiwgImRhdGEiOiAiMHhmNGZkMzA2MjNhMjZkYTgyZWFkMTVhODA1MzNhMDI2OTY2NTZiMTRiNWRiZmQ4NGViMTQ3OTBmMmUxYmU1ZTllNDU4MjBlZWIwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDBkNzdlMGQyZWVmOTA1Y2ZiMzljM2M0Yjk1MmVkMjc4ZDU4Zjk2ZTFmMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwNjllMDRmZTE2YzlhNmE4MzA3NmIzYzJkYzRiNGJjMjFiNWQ5YTIwYzAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwNjBjZTRiNzIifSwgInNpZ25hdHVyZSI6IG51bGwsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJldGhlcmV1bV9mdW5kX3Vuc2lnbmVkIn0", solver=fund_solver)
        >>> signature.transaction_raw()
        "eyJmZWUiOiAxMzg0NDgsICJ0cmFuc2FjdGlvbiI6IHsiY2hhaW5JZCI6IDEzMzcsICJmcm9tIjogIjB4NjllMDRmZTE2YzlBNkE4MzA3NkIzYzJkYzRiNEJjMjFiNWQ5QTIwQyIsICJ2YWx1ZSI6IDMwMDAwMDAwMDAwMDAwMDAwMDAsICJub25jZSI6IDEsICJnYXMiOiAxMzg0NDgsICJnYXNQcmljZSI6IDIwMDAwMDAwMDAwLCAidG8iOiAiMHhlYUVhQzgxZGE1RTM4NkU4Q2E0RGUxZTY0ZDQwYTEwRTQ2OEE1YjQwIiwgImRhdGEiOiAiMHhmNGZkMzA2MjNhMjZkYTgyZWFkMTVhODA1MzNhMDI2OTY2NTZiMTRiNWRiZmQ4NGViMTQ3OTBmMmUxYmU1ZTllNDU4MjBlZWIwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDBkNzdlMGQyZWVmOTA1Y2ZiMzljM2M0Yjk1MmVkMjc4ZDU4Zjk2ZTFmMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwNjllMDRmZTE2YzlhNmE4MzA3NmIzYzJkYzRiNGJjMjFiNWQ5YTIwYzAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwNjBjZTRiNzIifSwgInNpZ25hdHVyZSI6IHsiaGFzaCI6ICIweGU4N2IxYWVmZWM5ZmVjYmI3Njk5ZTE2ZDEwMWU3NTdlNDgyNWRiMTU3ZWI5NGQyZTcxZWNmYWYxN2ZkM2Q3NWQiLCAicmF3VHJhbnNhY3Rpb24iOiAiMHhmOGY0MDE4NTA0YTgxN2M4MDA4MzAyMWNkMDk0ZWFlYWM4MWRhNWUzODZlOGNhNGRlMWU2NGQ0MGExMGU0NjhhNWI0MDg4MjlhMjI0MWFmNjJjMDAwMGI4ODRmNGZkMzA2MjNhMjZkYTgyZWFkMTVhODA1MzNhMDI2OTY2NTZiMTRiNWRiZmQ4NGViMTQ3OTBmMmUxYmU1ZTllNDU4MjBlZWIwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDBkNzdlMGQyZWVmOTA1Y2ZiMzljM2M0Yjk1MmVkMjc4ZDU4Zjk2ZTFmMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwNjllMDRmZTE2YzlhNmE4MzA3NmIzYzJkYzRiNGJjMjFiNWQ5YTIwYzAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwNjBjZTRiNzI4MjBhOTVhMDZkY2ZjNmUzODVjYmNhZDZiMDkzZDBhMjM1MWY1MTZjNjFkOTQzNjhmZDgwZDk0ZjQ4YmY1NjYzMDcwZWU1N2RhMDU3MGM4MzdiNTk0NTc3NDY5NTE2YjI5Yjk5MDJjYzdkZjk3ODY0MWRlYWE4N2U1ZjY1NzZhZmNmMzA1ODllZjIiLCAiciI6IDQ5NjY5MjEwNTE3NzYwMDg5OTYxMDU3NzU1NTQ1NjcwOTE2NDU3NTQ1MzYxNjM0MDcyMzE1MTM1NzI2MzQzNzIxODgyMTY2OTQ1MTQ5LCAicyI6IDM5MzczMzI3NDQ1NzY3NzU2NjA0NjE0NDYyMjk2Nzc0MjAyMTY0MjY4ODcwNTAyOTE1ODk3NTkyMzQ2MjIyMzYxOTUxNDU3NTUwMDY2LCAidiI6IDI3MDl9LCAibmV0d29yayI6ICJ0ZXN0bmV0IiwgInR5cGUiOiAiZXRoZXJldW1fZnVuZF9zaWduZWQifQ"
        """

        if self._signed_raw is None:
            raise ValueError("Transaction is none, sign unsigned transaction raw first.")
        return clean_transaction_raw(self._signed_raw)


class FundSignature(Signature):
    """
    XinFin Fund signature.

    :param network: XinFin network, defaults to ``mainnet``.
    :type network: str
    :param provider: XinFin network provider, defaults to ``http``.
    :type provider: str
    :param token: Infura API endpoint token, defaults to ``4414fea5f7454211956b1627621450b4``.
    :type token: str

    :returns: FundSignature -- XinFin fund signature instance.

    .. note::
        XinFin has only two networks, ``mainnet`` and ``testnet``.
    """

    def __init__(self, network: str = config["network"], provider: str = config["provider"],
                 token: Optional[str] = None):
        super().__init__(
            network=network, provider=provider, token=token
        )

    def sign(self, transaction_raw: str, solver: FundSolver) -> "FundSignature":
        """
        Sign XinFin unsigned fund transaction raw.

        :param transaction_raw: XinFin unsigned fund transaction raw.
        :type transaction_raw: str
        :param solver: XinFin solver.
        :type solver: xinfin.solver.FundSolver

        :returns: FundSignature -- XinFin fund signature instance.

        >>> from swap.providers.xinfin.signature import FundSignature
        >>> from swap.providers.xinfin.solver import FundSolver
        >>> fund_signature: FundSignature = FundSignature(network="mainnet")
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="xprv9s21ZrQH143K3Y3pdbkbjreZQ9RVmqTLhRgf86uZyCJk2ou36YdUJt5frjwihGWmV1fQEDioiGZXWXUbHLy3kQf5xmhvhp8dZ2tfn6tgGUj")
        >>> fund_signature.sign(transaction_raw="eyJmZWUiOiAxMzg0NDgsICJ0cmFuc2FjdGlvbiI6IHsiY2hhaW5JZCI6IDEzMzcsICJmcm9tIjogIjB4NjllMDRmZTE2YzlBNkE4MzA3NkIzYzJkYzRiNEJjMjFiNWQ5QTIwQyIsICJ2YWx1ZSI6IDMwMDAwMDAwMDAwMDAwMDAwMDAsICJub25jZSI6IDEsICJnYXMiOiAxMzg0NDgsICJnYXNQcmljZSI6IDIwMDAwMDAwMDAwLCAidG8iOiAiMHhlYUVhQzgxZGE1RTM4NkU4Q2E0RGUxZTY0ZDQwYTEwRTQ2OEE1YjQwIiwgImRhdGEiOiAiMHhmNGZkMzA2MjNhMjZkYTgyZWFkMTVhODA1MzNhMDI2OTY2NTZiMTRiNWRiZmQ4NGViMTQ3OTBmMmUxYmU1ZTllNDU4MjBlZWIwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDBkNzdlMGQyZWVmOTA1Y2ZiMzljM2M0Yjk1MmVkMjc4ZDU4Zjk2ZTFmMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwNjllMDRmZTE2YzlhNmE4MzA3NmIzYzJkYzRiNGJjMjFiNWQ5YTIwYzAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwNjBjZTRiNzIifSwgInNpZ25hdHVyZSI6IG51bGwsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJldGhlcmV1bV9mdW5kX3Vuc2lnbmVkIn0", solver=fund_solver)
        <swap.providers.xinfin.signature.FundSignature object at 0x0409DAF0>
        """

        # Check parameter instances
        if not is_transaction_raw(transaction_raw=transaction_raw):
            raise TransactionRawError("Invalid XinFin unsigned transaction raw.")

        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

        if not loaded_transaction_raw["type"] == "xinfin_fund_unsigned":
            raise TypeError(f"Invalid XinFin fund unsigned transaction raw type, "
                            f"you can't sign '{loaded_transaction_raw['type']}' type by using fund signature.")

        # Check parameter instances
        if not isinstance(solver, FundSolver):
            raise TypeError(f"Solver must be XinFin FundSolver, not '{type(solver).__name__}' type.")

        # Set transaction, fee, type and network
        self._fee, self._type, self._network, self._transaction = (
            loaded_transaction_raw["fee"], loaded_transaction_raw["type"],
            loaded_transaction_raw["network"], loaded_transaction_raw["transaction"]
        )

        wallet: Wallet = solver.solve()
        signed_fund_transaction: SignedTransaction = self.web3.eth.account.sign_transaction(
            transaction_dict=self._transaction,
            private_key=wallet.private_key()
        )

        self._signature = dict(
            hash=signed_fund_transaction["hash"].hex(),
            rawTransaction=signed_fund_transaction["rawTransaction"].hex(),
            r=signed_fund_transaction["r"],
            s=signed_fund_transaction["s"],
            v=signed_fund_transaction["v"]
        )
        self._type = "xinfin_fund_signed"

        self._signed_raw = b64encode(str(json.dumps(dict(
            fee=self._fee,
            transaction=self._transaction,
            signature=self._signature,
            network=self._network,
            type=self._type
        ))).encode()).decode()
        return self


class WithdrawSignature(Signature):
    """
    XinFin Withdraw signature.

    :param network: XinFin network, defaults to ``mainnet``.
    :type network: str
    :param provider: XinFin network provider, defaults to ``http``.
    :type provider: str
    :param token: Infura API endpoint token, defaults to ``4414fea5f7454211956b1627621450b4``.
    :type token: str

    :returns: WithdrawSignature -- XinFin withdraw signature instance.

    .. note::
        XinFin has only two networks, ``mainnet`` and ``testnet``.
    """

    def __init__(self, network: str = config["network"], provider: str = config["provider"],
                 token: Optional[str] = None):
        super().__init__(
            network=network, provider=provider, token=token
        )

    def sign(self, transaction_raw: str, solver: WithdrawSolver) -> "WithdrawSignature":
        """
        Sign XinFin unsigned withdraw transaction raw.

        :param transaction_raw: XinFin unsigned withdraw transaction raw.
        :type transaction_raw: str
        :param solver: XinFin withdraw solver.
        :type solver: xinfin.solver.WithdrawSolver

        :returns: WithdrawSignature -- XinFin withdraw signature instance.

        >>> from swap.providers.xinfin.signature import WithdrawSignature
        >>> from swap.providers.xinfin.solver import WithdrawSolver
        >>> withdraw_signature: WithdrawSignature = WithdrawSignature(network="mainnet")
        >>> withdraw_solver: WithdrawSolver = WithdrawSolver(xprivate_key="xprv9s21ZrQH143K3Y3pdbkbjreZQ9RVmqTLhRgf86uZyCJk2ou36YdUJt5frjwihGWmV1fQEDioiGZXWXUbHLy3kQf5xmhvhp8dZ2tfn6tgGUj")
        >>> withdraw_signature.sign(transaction_raw="eyJmZWUiOiAxMzg0NDgsICJ0cmFuc2FjdGlvbiI6IHsiY2hhaW5JZCI6IDEzMzcsICJmcm9tIjogIjB4NjllMDRmZTE2YzlBNkE4MzA3NkIzYzJkYzRiNEJjMjFiNWQ5QTIwQyIsICJ2YWx1ZSI6IDMwMDAwMDAwMDAwMDAwMDAwMDAsICJub25jZSI6IDEsICJnYXMiOiAxMzg0NDgsICJnYXNQcmljZSI6IDIwMDAwMDAwMDAwLCAidG8iOiAiMHhlYUVhQzgxZGE1RTM4NkU4Q2E0RGUxZTY0ZDQwYTEwRTQ2OEE1YjQwIiwgImRhdGEiOiAiMHhmNGZkMzA2MjNhMjZkYTgyZWFkMTVhODA1MzNhMDI2OTY2NTZiMTRiNWRiZmQ4NGViMTQ3OTBmMmUxYmU1ZTllNDU4MjBlZWIwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDBkNzdlMGQyZWVmOTA1Y2ZiMzljM2M0Yjk1MmVkMjc4ZDU4Zjk2ZTFmMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwNjllMDRmZTE2YzlhNmE4MzA3NmIzYzJkYzRiNGJjMjFiNWQ5YTIwYzAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwNjBjZTRiNzIifSwgInNpZ25hdHVyZSI6IG51bGwsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJldGhlcmV1bV9mdW5kX3Vuc2lnbmVkIn0", solver=withdraw_solver)
        <swap.providers.xinfin.signature.WithdrawSignature object at 0x0409DAF0>
        """

        # Check parameter instances
        if not is_transaction_raw(transaction_raw=transaction_raw):
            raise TransactionRawError("Invalid XinFin unsigned transaction raw.")

        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

        if not loaded_transaction_raw["type"] == "xinfin_withdraw_unsigned":
            raise TypeError(f"Invalid XinFin withdraw unsigned transaction raw type, "
                            f"you can't sign '{loaded_transaction_raw['type']}' type by using withdraw signature.")

        # Check parameter instances
        if not isinstance(solver, WithdrawSolver):
            raise TypeError(f"Solver must be XinFin WithdrawSolver, not '{type(solver).__name__}' type.")

        # Set transaction, fee, type and network
        self._fee, self._type, self._network, self._transaction = (
            loaded_transaction_raw["fee"], loaded_transaction_raw["type"],
            loaded_transaction_raw["network"], loaded_transaction_raw["transaction"]
        )

        wallet: Wallet = solver.solve()
        signed_fund_transaction: SignedTransaction = self.web3.eth.account.sign_transaction(
            transaction_dict=self._transaction,
            private_key=wallet.private_key()
        )

        self._signature = dict(
            hash=signed_fund_transaction["hash"].hex(),
            rawTransaction=signed_fund_transaction["rawTransaction"].hex(),
            r=signed_fund_transaction["r"],
            s=signed_fund_transaction["s"],
            v=signed_fund_transaction["v"]
        )
        self._type = "xinfin_withdraw_signed"

        self._signed_raw = b64encode(str(json.dumps(dict(
            fee=self._fee,
            transaction=self._transaction,
            signature=self._signature,
            network=self._network,
            type=self._type
        ))).encode()).decode()
        return self


class RefundSignature(Signature):
    """
    XinFin Refund signature.

    :param network: XinFin network, defaults to ``mainnet``.
    :type network: str
    :param provider: XinFin network provider, defaults to ``http``.
    :type provider: str
    :param token: Infura API endpoint token, defaults to ``4414fea5f7454211956b1627621450b4``.
    :type token: str

    :returns: RefundSignature -- XinFin refund signature instance.

    .. note::
        XinFin has only two networks, ``mainnet`` and ``testnet``.
    """

    def __init__(self, network: str = config["network"], provider: str = config["provider"],
                 token: Optional[str] = None):
        super().__init__(
            network=network, provider=provider, token=token
        )

    def sign(self, transaction_raw: str, solver: RefundSolver) -> "RefundSignature":
        """
        Sign XinFin unsigned refund transaction raw.

        :param transaction_raw: XinFin unsigned refund transaction raw.
        :type transaction_raw: str
        :param solver: XinFin refund solver.
        :type solver: xinfin.solver.RefundSolver

        :returns: RefundSignature -- XinFin refund signature instance.

        >>> from swap.providers.xinfin.signature import RefundSignature
        >>> from swap.providers.xinfin.solver import RefundSolver
        >>> refund_signature: RefundSignature = RefundSignature(network="mainnet")
        >>> refund_solver: RefundSolver = RefundSolver(xprivate_key="xprv9s21ZrQH143K3Y3pdbkbjreZQ9RVmqTLhRgf86uZyCJk2ou36YdUJt5frjwihGWmV1fQEDioiGZXWXUbHLy3kQf5xmhvhp8dZ2tfn6tgGUj")
        >>> refund_signature.sign(transaction_raw="eyJmZWUiOiAxMzg0NDgsICJ0cmFuc2FjdGlvbiI6IHsiY2hhaW5JZCI6IDEzMzcsICJmcm9tIjogIjB4NjllMDRmZTE2YzlBNkE4MzA3NkIzYzJkYzRiNEJjMjFiNWQ5QTIwQyIsICJ2YWx1ZSI6IDMwMDAwMDAwMDAwMDAwMDAwMDAsICJub25jZSI6IDEsICJnYXMiOiAxMzg0NDgsICJnYXNQcmljZSI6IDIwMDAwMDAwMDAwLCAidG8iOiAiMHhlYUVhQzgxZGE1RTM4NkU4Q2E0RGUxZTY0ZDQwYTEwRTQ2OEE1YjQwIiwgImRhdGEiOiAiMHhmNGZkMzA2MjNhMjZkYTgyZWFkMTVhODA1MzNhMDI2OTY2NTZiMTRiNWRiZmQ4NGViMTQ3OTBmMmUxYmU1ZTllNDU4MjBlZWIwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDBkNzdlMGQyZWVmOTA1Y2ZiMzljM2M0Yjk1MmVkMjc4ZDU4Zjk2ZTFmMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwNjllMDRmZTE2YzlhNmE4MzA3NmIzYzJkYzRiNGJjMjFiNWQ5YTIwYzAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwNjBjZTRiNzIifSwgInNpZ25hdHVyZSI6IG51bGwsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJldGhlcmV1bV9mdW5kX3Vuc2lnbmVkIn0", solver=refund_solver)
        <swap.providers.xinfin.signature.RefundSignature object at 0x0409DAF0>
        """

        # Check parameter instances
        if not is_transaction_raw(transaction_raw=transaction_raw):
            raise TransactionRawError("Invalid XinFin unsigned transaction raw.")

        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

        if not loaded_transaction_raw["type"] == "xinfin_refund_unsigned":
            raise TypeError(f"Invalid XinFin refund unsigned transaction raw type, "
                            f"you can't sign '{loaded_transaction_raw['type']}' type by using refund signature.")

        # Check parameter instances
        if not isinstance(solver, RefundSolver):
            raise TypeError(f"Solver must be XinFin RefundSolver, not '{type(solver).__name__}' type.")

        # Set transaction, fee, type and network
        self._fee, self._type, self._network, self._transaction = (
            loaded_transaction_raw["fee"], loaded_transaction_raw["type"],
            loaded_transaction_raw["network"], loaded_transaction_raw["transaction"]
        )

        wallet: Wallet = solver.solve()
        signed_fund_transaction: SignedTransaction = self.web3.eth.account.sign_transaction(
            transaction_dict=self._transaction,
            private_key=wallet.private_key()
        )

        self._signature = dict(
            hash=signed_fund_transaction["hash"].hex(),
            rawTransaction=signed_fund_transaction["rawTransaction"].hex(),
            r=signed_fund_transaction["r"],
            s=signed_fund_transaction["s"],
            v=signed_fund_transaction["v"]
        )
        self._type = "xinfin_refund_signed"

        self._signed_raw = b64encode(str(json.dumps(dict(
            fee=self._fee,
            transaction=self._transaction,
            signature=self._signature,
            network=self._network,
            type=self._type
        ))).encode()).decode()
        return self
