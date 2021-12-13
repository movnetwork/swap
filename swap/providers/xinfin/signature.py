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
    NormalSolver, FundSolver, WithdrawSolver, RefundSolver
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
    :param xrc20: Signature XRC20 token, default to ``False``.
    :type xrc20: bool
    :param provider: XinFin network provider, defaults to ``http``.
    :type provider: str

    :returns: Signature -- XinFin signature instance.

    .. note::
        XinFin has only two networks, ``mainnet``, ``apothem`` and ``testnet``.
    """

    def __init__(self, network: str = config["network"], xrc20: bool = False, provider: str = config["provider"]):
        super().__init__(
            network=network, xrc20=xrc20, provider=provider
        )

        self._signed_raw: Optional[str] = None

    def fee(self, unit: str = config["unit"]) -> Union[Wei, int, float]:
        """
        Get XinFin signature fee.

        :param unit: XinFin unit, default to ``Wie``.
        :type unit: str

        :returns: Wei, int, float -- XinFin signature fee.

        >>> from swap.providers.xinfin.signature import Signature
        >>> from swap.providers.xinfin.solver import WithdrawSolver
        >>> signature: Signature = Signature(network="testnet")
        >>> withdraw_solver: WithdrawSolver = WithdrawSolver(xprivate_key="xprv9s21ZrQH143K4Kpce43z5guPyxLrFoc2i8aQAq835Zzp4Rt7i6nZaMCnVSDyHT6MnmJJGKHMrCUqaYpGojrug1ZN5qQDdShQffmkyv5xyUR", account=0, change=False, address=0)
        >>> signature.sign(transaction_raw="eyJmZWUiOiA4MjY4OSwgInR5cGUiOiAieGluZmluX3dpdGhkcmF3X3Vuc2lnbmVkIiwgInRyYW5zYWN0aW9uIjogeyJjaGFpbklkIjogMTMzNywgImZyb20iOiAiMHhmOEQ0MzgwNjI2MENGYzZjQzc5ZkI0MDhCQTE4OTcwNTQ2NjdGODFDIiwgInZhbHVlIjogMCwgIm5vbmNlIjogMCwgImdhcyI6IDgyNjg5LCAiZ2FzUHJpY2UiOiAyMDAwMDAwMDAwMCwgInRvIjogIjB4ZEUwNmIxMGM2Nzc2NWM4QzBiOUY2NEUwZUY0MjNiNDVFYjg2YjhlNyIsICJkYXRhIjogIjB4MDZhNTM2NjUxOTA5NTc1YzQzNmEwZWFiZTZjYWE3MmQ0ZmViMmM0YWVjZWVmNTg2ZmU5NGNhODJmMzZjZTljMjBlZmRhNGI0MDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDA0MDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMGU0ODY1NmM2YzZmMjA0ZDY1Njg2NTcyNjU3NDIxMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwIn0sICJzaWduYXR1cmUiOiBudWxsLCAibmV0d29yayI6ICJ0ZXN0bmV0In0", solver=withdraw_solver)
        >>> signature.fee(unit="Wei")
        82689
        """

        # Check transaction
        if not self._transaction:
            raise ValueError("Transaction is none, build transaction first.")

        if unit not in ["XDC", "Gwei", "Wei"]:
            raise UnitError(f"Invalid XinFin '{unit}' unit", "choose only 'XDC', 'Gwei' or 'Wei' units.")
        return self._fee if unit == "Wei" else \
            amount_unit_converter(amount=self._fee, unit_from=f"Wei2{unit}")

    def hash(self) -> Optional[str]:
        """
        Get XinFin signature has.

        :returns: str -- XinFin signature hash.

        >>> from swap.providers.xinfin.signature import Signature
        >>> from swap.providers.xinfin.solver import RefundSolver
        >>> signature: Signature = Signature(network="testnet")
        >>> refund_solver: RefundSolver = RefundSolver(xprivate_key="xprv9s21ZrQH143K3Y3pdbkbjreZQ9RVmqTLhRgf86uZyCJk2ou36YdUJt5frjwihGWmV1fQEDioiGZXWXUbHLy3kQf5xmhvhp8dZ2tfn6tgGUj", account=0, change=False, address=0)
        >>> signature.sign(transaction_raw="eyJmZWUiOiA1OTIzMiwgInR5cGUiOiAieGluZmluX3JlZnVuZF91bnNpZ25lZCIsICJ0cmFuc2FjdGlvbiI6IHsiY2hhaW5JZCI6IDEzMzcsICJmcm9tIjogIjB4MjIyNGNhQTIyMzVERjhEYTNEMjAxNmQyQUIxMTM3RDJkNTQ4QTIzMiIsICJ2YWx1ZSI6IDAsICJub25jZSI6IDIsICJnYXMiOiA1OTIzMiwgImdhc1ByaWNlIjogMjAwMDAwMDAwMDAsICJ0byI6ICIweGRFMDZiMTBjNjc3NjVjOEMwYjlGNjRFMGVGNDIzYjQ1RWI4NmI4ZTciLCAiZGF0YSI6ICIweDcyNDlmYmI2MTkwOTU3NWM0MzZhMGVhYmU2Y2FhNzJkNGZlYjJjNGFlY2VlZjU4NmZlOTRjYTgyZjM2Y2U5YzIwZWZkYTRiNCJ9LCAic2lnbmF0dXJlIjogbnVsbCwgIm5ldHdvcmsiOiAidGVzdG5ldCJ9", solver=refund_solver)
        >>> signature.hash()
        "0x90449ab8e3736feae4980554bb129b408f88d0003e569022cf8e00817cc2a7d9"
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
        >>> signature: Signature = Signature(network="testnet")
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="xprv9s21ZrQH143K3Y3pdbkbjreZQ9RVmqTLhRgf86uZyCJk2ou36YdUJt5frjwihGWmV1fQEDioiGZXWXUbHLy3kQf5xmhvhp8dZ2tfn6tgGUj", account=0, change=False, address=0)
        >>> signature.sign(transaction_raw="eyJmZWUiOiAxMzg0NDgsICJ0cmFuc2FjdGlvbiI6IHsiY2hhaW5JZCI6IDEzMzcsICJmcm9tIjogIjB4NjllMDRmZTE2YzlBNkE4MzA3NkIzYzJkYzRiNEJjMjFiNWQ5QTIwQyIsICJ2YWx1ZSI6IDMwMDAwMDAwMDAwMDAwMDAwMDAsICJub25jZSI6IDEsICJnYXMiOiAxMzg0NDgsICJnYXNQcmljZSI6IDIwMDAwMDAwMDAwLCAidG8iOiAiMHhlYUVhQzgxZGE1RTM4NkU4Q2E0RGUxZTY0ZDQwYTEwRTQ2OEE1YjQwIiwgImRhdGEiOiAiMHhmNGZkMzA2MjNhMjZkYTgyZWFkMTVhODA1MzNhMDI2OTY2NTZiMTRiNWRiZmQ4NGViMTQ3OTBmMmUxYmU1ZTllNDU4MjBlZWIwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDBkNzdlMGQyZWVmOTA1Y2ZiMzljM2M0Yjk1MmVkMjc4ZDU4Zjk2ZTFmMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwNjllMDRmZTE2YzlhNmE4MzA3NmIzYzJkYzRiNGJjMjFiNWQ5YTIwYzAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwNjBjZTRiNzIifSwgInNpZ25hdHVyZSI6IG51bGwsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJldGhlcmV1bV9mdW5kX3Vuc2lnbmVkIn0", solver=fund_solver)
        >>> signature.json()
        {'chainId': 1337, 'from': '0x2224caA2235DF8Da3D2016d2AB1137D2d548A232', 'value': 1000000000000000000, 'nonce': 2, 'gas': 138448, 'gasPrice': 20000000000, 'to': '0xdE06b10c67765c8C0b9F64E0eF423b45Eb86b8e7', 'data': '0xf4fd30623a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb000000000000000000000000f8d43806260cfc6cc79fb408ba1897054667f81c0000000000000000000000002224caa2235df8da3d2016d2ab1137d2d548a2320000000000000000000000000000000000000000000000000000000060e006c3'}
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
        >>> from swap.providers.xinfin.solver import WithdrawSolver
        >>> signature: Signature = Signature(network="testnet")
        >>> withdraw_solver: WithdrawSolver = WithdrawSolver(xprivate_key="xprv9s21ZrQH143K4Kpce43z5guPyxLrFoc2i8aQAq835Zzp4Rt7i6nZaMCnVSDyHT6MnmJJGKHMrCUqaYpGojrug1ZN5qQDdShQffmkyv5xyUR", account=0, change=False, address=0)
        >>> signature.sign(transaction_raw="eyJmZWUiOiA4MjY4OSwgInR5cGUiOiAieGluZmluX3dpdGhkcmF3X3Vuc2lnbmVkIiwgInRyYW5zYWN0aW9uIjogeyJjaGFpbklkIjogMTMzNywgImZyb20iOiAiMHhmOEQ0MzgwNjI2MENGYzZjQzc5ZkI0MDhCQTE4OTcwNTQ2NjdGODFDIiwgInZhbHVlIjogMCwgIm5vbmNlIjogMCwgImdhcyI6IDgyNjg5LCAiZ2FzUHJpY2UiOiAyMDAwMDAwMDAwMCwgInRvIjogIjB4ZEUwNmIxMGM2Nzc2NWM4QzBiOUY2NEUwZUY0MjNiNDVFYjg2YjhlNyIsICJkYXRhIjogIjB4MDZhNTM2NjUxOTA5NTc1YzQzNmEwZWFiZTZjYWE3MmQ0ZmViMmM0YWVjZWVmNTg2ZmU5NGNhODJmMzZjZTljMjBlZmRhNGI0MDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDA0MDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMGU0ODY1NmM2YzZmMjA0ZDY1Njg2NTcyNjU3NDIxMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwIn0sICJzaWduYXR1cmUiOiBudWxsLCAibmV0d29yayI6ICJ0ZXN0bmV0In0", solver=withdraw_solver)
        >>> signature.raw()
        "0xf8ec808504a817c8008301430194de06b10c67765c8c0b9f64e0ef423b45eb86b8e780b88406a536651909575c436a0eabe6caa72d4feb2c4aeceef586fe94ca82f36ce9c20efda4b40000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000000e48656c6c6f204d65686572657421000000000000000000000000000000000000820a95a0ffc24cf0a8abaf98bec5096ba0822833d4509d31ebcb4a3a0e6ba0530ec90156a0184a9b41949b199ec5c7a7c269c1c47d24fb05ca60adf7c5ec617a06e1047384"
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
        >>> signature: Signature = Signature(network="testnet")
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="xprv9s21ZrQH143K3Y3pdbkbjreZQ9RVmqTLhRgf86uZyCJk2ou36YdUJt5frjwihGWmV1fQEDioiGZXWXUbHLy3kQf5xmhvhp8dZ2tfn6tgGUj", account=0, change=False, address=0)
        >>> signature.sign(transaction_raw="eyJmZWUiOiAxMzg0NDgsICJ0eXBlIjogInhpbmZpbl9mdW5kX3Vuc2lnbmVkIiwgInRyYW5zYWN0aW9uIjogeyJjaGFpbklkIjogMTMzNywgImZyb20iOiAiMHgyMjI0Y2FBMjIzNURGOERhM0QyMDE2ZDJBQjExMzdEMmQ1NDhBMjMyIiwgInZhbHVlIjogMTAwMDAwMDAwMDAwMDAwMDAwMCwgIm5vbmNlIjogMiwgImdhcyI6IDEzODQ0OCwgImdhc1ByaWNlIjogMjAwMDAwMDAwMDAsICJ0byI6ICIweGRFMDZiMTBjNjc3NjVjOEMwYjlGNjRFMGVGNDIzYjQ1RWI4NmI4ZTciLCAiZGF0YSI6ICIweGY0ZmQzMDYyM2EyNmRhODJlYWQxNWE4MDUzM2EwMjY5NjY1NmIxNGI1ZGJmZDg0ZWIxNDc5MGYyZTFiZTVlOWU0NTgyMGVlYjAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMGY4ZDQzODA2MjYwY2ZjNmNjNzlmYjQwOGJhMTg5NzA1NDY2N2Y4MWMwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAyMjI0Y2FhMjIzNWRmOGRhM2QyMDE2ZDJhYjExMzdkMmQ1NDhhMjMyMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDA2MGUwMDZjMyJ9LCAic2lnbmF0dXJlIjogbnVsbCwgIm5ldHdvcmsiOiAidGVzdG5ldCJ9", solver=fund_solver)
        >>> signature.type()
        "xinfin_fund_signed"
        """

        # Check transaction
        if not self._transaction:
            raise ValueError("Transaction is none, build transaction first.")

        return self._type

    def sign(self, transaction_raw: str, solver: Union[NormalSolver, FundSolver, WithdrawSolver, RefundSolver]) -> \
            Union["NormalSignature", "FundSignature", "WithdrawSignature", "RefundSignature"]:
        """
        Sign XinFin unsigned transaction raw.

        :param transaction_raw: XinFin unsigned transaction raw.
        :type transaction_raw: str
        :param solver: XinFin solver.
        :type solver: xinfin.solver.NormalSolver, xinfin.solver.FundSolver, xinfin.solver.WithdrawSolver, xinfin.solver.RefundSolver

        :returns: NormalSignature, FundSignature, WithdrawSignature, RefundSignature -- XinFin signature instance.

        >>> from swap.providers.xinfin.signature import Signature
        >>> from swap.providers.xinfin.solver import FundSolver
        >>> signature: Signature = Signature(network="testnet")
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="xprv9s21ZrQH143K3Y3pdbkbjreZQ9RVmqTLhRgf86uZyCJk2ou36YdUJt5frjwihGWmV1fQEDioiGZXWXUbHLy3kQf5xmhvhp8dZ2tfn6tgGUj", account=0, change=False, address=0)
        >>> signature.sign(transaction_raw="eyJmZWUiOiAxMzg0NDgsICJ0eXBlIjogInhpbmZpbl9mdW5kX3Vuc2lnbmVkIiwgInRyYW5zYWN0aW9uIjogeyJjaGFpbklkIjogMTMzNywgImZyb20iOiAiMHgyMjI0Y2FBMjIzNURGOERhM0QyMDE2ZDJBQjExMzdEMmQ1NDhBMjMyIiwgInZhbHVlIjogMTAwMDAwMDAwMDAwMDAwMDAwMCwgIm5vbmNlIjogMiwgImdhcyI6IDEzODQ0OCwgImdhc1ByaWNlIjogMjAwMDAwMDAwMDAsICJ0byI6ICIweGRFMDZiMTBjNjc3NjVjOEMwYjlGNjRFMGVGNDIzYjQ1RWI4NmI4ZTciLCAiZGF0YSI6ICIweGY0ZmQzMDYyM2EyNmRhODJlYWQxNWE4MDUzM2EwMjY5NjY1NmIxNGI1ZGJmZDg0ZWIxNDc5MGYyZTFiZTVlOWU0NTgyMGVlYjAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMGY4ZDQzODA2MjYwY2ZjNmNjNzlmYjQwOGJhMTg5NzA1NDY2N2Y4MWMwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAyMjI0Y2FhMjIzNWRmOGRhM2QyMDE2ZDJhYjExMzdkMmQ1NDhhMjMyMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDA2MGUwMDZjMyJ9LCAic2lnbmF0dXJlIjogbnVsbCwgIm5ldHdvcmsiOiAidGVzdG5ldCJ9", solver=fund_solver)
        <swap.providers.xinfin.signature.FundSignature object at 0x0409DAF0>
        """

        if not is_transaction_raw(transaction_raw=transaction_raw):
            raise TransactionRawError("Invalid Bytom unsigned transaction raw.")

        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

        self._type = loaded_transaction_raw["type"]
        if loaded_transaction_raw["type"] == "xinfin_normal_unsigned":
            return NormalSignature(network=self._network, xrc20=False).sign(
                transaction_raw=transaction_raw, solver=solver
            )
        elif loaded_transaction_raw["type"] == "xinfin_xrc20_normal_unsigned":
            return NormalSignature(network=self._network, xrc20=True).sign(
                transaction_raw=transaction_raw, solver=solver
            )
        elif loaded_transaction_raw["type"] == "xinfin_fund_unsigned":
            return FundSignature(network=self._network, xrc20=False).sign(
                transaction_raw=transaction_raw, solver=solver
            )
        elif loaded_transaction_raw["type"] == "xinfin_xrc20_fund_unsigned":
            return FundSignature(network=self._network, xrc20=True).sign(
                transaction_raw=transaction_raw, solver=solver
            )
        elif loaded_transaction_raw["type"] == "xinfin_withdraw_unsigned":
            return WithdrawSignature(network=self._network, xrc20=False).sign(
                transaction_raw=transaction_raw, solver=solver
            )
        elif loaded_transaction_raw["type"] == "xinfin_xrc20_withdraw_unsigned":
            return WithdrawSignature(network=self._network, xrc20=True).sign(
                transaction_raw=transaction_raw, solver=solver
            )
        elif loaded_transaction_raw["type"] == "xinfin_refund_unsigned":
            return RefundSignature(network=self._network, xrc20=False).sign(
                transaction_raw=transaction_raw, solver=solver
            )
        elif loaded_transaction_raw["type"] == "xinfin_xrc20_refund_unsigned":
            return RefundSignature(network=self._network, xrc20=True).sign(
                transaction_raw=transaction_raw, solver=solver
            )

    def signature(self) -> dict:
        """
        Get XinFin signature.

        :returns: dict -- XinFin signature.

        >>> from swap.providers.xinfin.signature import Signature
        >>> from swap.providers.xinfin.solver import WithdrawSolver
        >>> signature: Signature = Signature(network="testnet")
        >>> withdraw_solver: WithdrawSolver = WithdrawSolver(xprivate_key="xprv9s21ZrQH143K4Kpce43z5guPyxLrFoc2i8aQAq835Zzp4Rt7i6nZaMCnVSDyHT6MnmJJGKHMrCUqaYpGojrug1ZN5qQDdShQffmkyv5xyUR", account=0, change=False, address=0)
        >>> signature.sign(transaction_raw="eyJmZWUiOiA4MjY4OSwgInR5cGUiOiAieGluZmluX3dpdGhkcmF3X3Vuc2lnbmVkIiwgInRyYW5zYWN0aW9uIjogeyJjaGFpbklkIjogMTMzNywgImZyb20iOiAiMHhmOEQ0MzgwNjI2MENGYzZjQzc5ZkI0MDhCQTE4OTcwNTQ2NjdGODFDIiwgInZhbHVlIjogMCwgIm5vbmNlIjogMCwgImdhcyI6IDgyNjg5LCAiZ2FzUHJpY2UiOiAyMDAwMDAwMDAwMCwgInRvIjogIjB4ZEUwNmIxMGM2Nzc2NWM4QzBiOUY2NEUwZUY0MjNiNDVFYjg2YjhlNyIsICJkYXRhIjogIjB4MDZhNTM2NjUxOTA5NTc1YzQzNmEwZWFiZTZjYWE3MmQ0ZmViMmM0YWVjZWVmNTg2ZmU5NGNhODJmMzZjZTljMjBlZmRhNGI0MDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDA0MDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMGU0ODY1NmM2YzZmMjA0ZDY1Njg2NTcyNjU3NDIxMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwIn0sICJzaWduYXR1cmUiOiBudWxsLCAibmV0d29yayI6ICJ0ZXN0bmV0In0", solver=withdraw_solver)
        >>> signature.signature()
        {'hash': '0xe8e8738c791385738661573ad4de63dd81b77d240b6138ca476ea8cdcbb29a21', 'rawTransaction': '0xf8ec808504a817c8008301430194de06b10c67765c8c0b9f64e0ef423b45eb86b8e780b88406a536651909575c436a0eabe6caa72d4feb2c4aeceef586fe94ca82f36ce9c20efda4b40000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000000e48656c6c6f204d65686572657421000000000000000000000000000000000000820a95a0ffc24cf0a8abaf98bec5096ba0822833d4509d31ebcb4a3a0e6ba0530ec90156a0184a9b41949b199ec5c7a7c269c1c47d24fb05ca60adf7c5ec617a06e1047384', 'r': 115683075740172584287236173170973052486872064110718784013746063807450268107094, 's': 10987326587522303302152973055763806493281157878637620947188858604750528344964, 'v': 2709}
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
        >>> signature: Signature = Signature(network="testnet")
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="xprv9s21ZrQH143K3Y3pdbkbjreZQ9RVmqTLhRgf86uZyCJk2ou36YdUJt5frjwihGWmV1fQEDioiGZXWXUbHLy3kQf5xmhvhp8dZ2tfn6tgGUj", account=0, change=False, address=0)
        >>> signature.sign(transaction_raw="eyJmZWUiOiAxMzg0NDgsICJ0eXBlIjogInhpbmZpbl9mdW5kX3Vuc2lnbmVkIiwgInRyYW5zYWN0aW9uIjogeyJjaGFpbklkIjogMTMzNywgImZyb20iOiAiMHgyMjI0Y2FBMjIzNURGOERhM0QyMDE2ZDJBQjExMzdEMmQ1NDhBMjMyIiwgInZhbHVlIjogMTAwMDAwMDAwMDAwMDAwMDAwMCwgIm5vbmNlIjogMiwgImdhcyI6IDEzODQ0OCwgImdhc1ByaWNlIjogMjAwMDAwMDAwMDAsICJ0byI6ICIweGRFMDZiMTBjNjc3NjVjOEMwYjlGNjRFMGVGNDIzYjQ1RWI4NmI4ZTciLCAiZGF0YSI6ICIweGY0ZmQzMDYyM2EyNmRhODJlYWQxNWE4MDUzM2EwMjY5NjY1NmIxNGI1ZGJmZDg0ZWIxNDc5MGYyZTFiZTVlOWU0NTgyMGVlYjAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMGY4ZDQzODA2MjYwY2ZjNmNjNzlmYjQwOGJhMTg5NzA1NDY2N2Y4MWMwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAyMjI0Y2FhMjIzNWRmOGRhM2QyMDE2ZDJhYjExMzdkMmQ1NDhhMjMyMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDA2MGUwMDZjMyJ9LCAic2lnbmF0dXJlIjogbnVsbCwgIm5ldHdvcmsiOiAidGVzdG5ldCJ9", solver=fund_solver)
        >>> signature.transaction_raw()
        "eyJmZWUiOiAxMzg0NDgsICJ0eXBlIjogInhpbmZpbl9mdW5kX3NpZ25lZCIsICJ0cmFuc2FjdGlvbiI6IHsiY2hhaW5JZCI6IDEzMzcsICJmcm9tIjogIjB4MjIyNGNhQTIyMzVERjhEYTNEMjAxNmQyQUIxMTM3RDJkNTQ4QTIzMiIsICJ2YWx1ZSI6IDEwMDAwMDAwMDAwMDAwMDAwMDAsICJub25jZSI6IDIsICJnYXMiOiAxMzg0NDgsICJnYXNQcmljZSI6IDIwMDAwMDAwMDAwLCAidG8iOiAiMHhkRTA2YjEwYzY3NzY1YzhDMGI5RjY0RTBlRjQyM2I0NUViODZiOGU3IiwgImRhdGEiOiAiMHhmNGZkMzA2MjNhMjZkYTgyZWFkMTVhODA1MzNhMDI2OTY2NTZiMTRiNWRiZmQ4NGViMTQ3OTBmMmUxYmU1ZTllNDU4MjBlZWIwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDBmOGQ0MzgwNjI2MGNmYzZjYzc5ZmI0MDhiYTE4OTcwNTQ2NjdmODFjMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMjIyNGNhYTIyMzVkZjhkYTNkMjAxNmQyYWIxMTM3ZDJkNTQ4YTIzMjAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwNjBlMDA2YzMifSwgInNpZ25hdHVyZSI6IHsiaGFzaCI6ICIweDcwZTNhYjZjZDhiMDZiMDliYjc4M2Y0ZjkyNzlmMGM0OGM3MGIyZjk0MjQ0NmU4OWIyN2EyZGQyZWJjNTMwNDgiLCAicmF3VHJhbnNhY3Rpb24iOiAiMHhmOGY0MDI4NTA0YTgxN2M4MDA4MzAyMWNkMDk0ZGUwNmIxMGM2Nzc2NWM4YzBiOWY2NGUwZWY0MjNiNDVlYjg2YjhlNzg4MGRlMGI2YjNhNzY0MDAwMGI4ODRmNGZkMzA2MjNhMjZkYTgyZWFkMTVhODA1MzNhMDI2OTY2NTZiMTRiNWRiZmQ4NGViMTQ3OTBmMmUxYmU1ZTllNDU4MjBlZWIwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDBmOGQ0MzgwNjI2MGNmYzZjYzc5ZmI0MDhiYTE4OTcwNTQ2NjdmODFjMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMjIyNGNhYTIyMzVkZjhkYTNkMjAxNmQyYWIxMTM3ZDJkNTQ4YTIzMjAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwNjBlMDA2YzM4MjBhOTVhMDk4Yjg0YWRjNWVmMWNiMTZlYzFjZjE2MTAzMDlmNGM4OTAwYjU3ZGYzOTMwZDRjOTI3OWI0ZjJlZmE2NDc2OTVhMDQ2MWQ4YzA4MWVmMGUzNjJkZjA5MjNjZjcwMzAzMTFjMDg5YzVkYjA1ZmQ5N2Y2MzgwNDI1ZDAwODYzMWZlYWUiLCAiciI6IDY5MDc3MTY5NTE0OTkyNDY2NDQyOTgxMzAwMzk0OTkzNDQ5NDgzMDExOTkwMzg1ODU5NzE3ODAyOTk1MzUyNzIzMjkyNzg1MjQzNzk3LCAicyI6IDMxNzE0MTA0NDI5MTMzODA4NzY2ODgyNzkwNDAyOTIyODA1Mzg0NzA5Mzk4MDEyOTMyOTcxOTc5MDIyODg3NDMyMjk1MTUxNjk3NTgyLCAidiI6IDI3MDl9LCAibmV0d29yayI6ICJ0ZXN0bmV0In0"
        """

        if self._signed_raw is None:
            raise ValueError("Transaction is none, sign unsigned transaction raw first.")
        return clean_transaction_raw(self._signed_raw)


class NormalSignature(Signature):
    """
    XinFin Normal signature.

    :param network: XinFin network, defaults to ``mainnet``.
    :type network: str
    :param xrc20: Normal signature XRC20 token, default to ``False``.
    :type xrc20: bool
    :param provider: XinFin network provider, defaults to ``http``.
    :type provider: str

    :returns: NormalSignature -- XinFin normal signature instance.

    .. note::
        XinFin has only five networks, ``mainnet``, ``ropsten``, ``kovan``, ``rinkeby`` and ``testnet``.
    """

    def __init__(self, network: str = config["network"], xrc20: bool = False, provider: str = config["provider"]):
        super().__init__(
            network=network, xrc20=xrc20, provider=provider
        )

    def sign(self, transaction_raw: str, solver: NormalSolver) -> "NormalSignature":
        """
        Sign XinFin unsigned normal transaction raw.

        :param transaction_raw: XinFin unsigned normal transaction raw.
        :type transaction_raw: str
        :param solver: XinFin solver.
        :type solver: xinfin.solver.NormalSolver

        :returns: NormalSignature -- XinFin normal signature instance.

        >>> from swap.providers.xinfin.signature import NormalSignature
        >>> from swap.providers.xinfin.solver import NormalSolver
        >>> normal_signature: NormalSignature = NormalSignature(network="mainnet")
        >>> normal_solver: NormalSolver = NormalSolver(xprivate_key="xprv9s21ZrQH143K3Y3pdbkbjreZQ9RVmqTLhRgf86uZyCJk2ou36YdUJt5frjwihGWmV1fQEDioiGZXWXUbHLy3kQf5xmhvhp8dZ2tfn6tgGUj")
        >>> normal_signature.sign(transaction_raw="eyJmZWUiOiAxMzg0NDgsICJ0cmFuc2FjdGlvbiI6IHsiY2hhaW5JZCI6IDEzMzcsICJmcm9tIjogIjB4NjllMDRmZTE2YzlBNkE4MzA3NkIzYzJkYzRiNEJjMjFiNWQ5QTIwQyIsICJ2YWx1ZSI6IDMwMDAwMDAwMDAwMDAwMDAwMDAsICJub25jZSI6IDEsICJnYXMiOiAxMzg0NDgsICJnYXNQcmljZSI6IDIwMDAwMDAwMDAwLCAidG8iOiAiMHhlYUVhQzgxZGE1RTM4NkU4Q2E0RGUxZTY0ZDQwYTEwRTQ2OEE1YjQwIiwgImRhdGEiOiAiMHhmNGZkMzA2MjNhMjZkYTgyZWFkMTVhODA1MzNhMDI2OTY2NTZiMTRiNWRiZmQ4NGViMTQ3OTBmMmUxYmU1ZTllNDU4MjBlZWIwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDBkNzdlMGQyZWVmOTA1Y2ZiMzljM2M0Yjk1MmVkMjc4ZDU4Zjk2ZTFmMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwNjllMDRmZTE2YzlhNmE4MzA3NmIzYzJkYzRiNGJjMjFiNWQ5YTIwYzAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwNjBjZTRiNzIifSwgInNpZ25hdHVyZSI6IG51bGwsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJldGhlcmV1bV9mdW5kX3Vuc2lnbmVkIn0", solver=normal_solver)
        <swap.providers.xinfin.signature.NormalSignature object at 0x0409DAF0>
        """

        # Check parameter instances
        if not is_transaction_raw(transaction_raw=transaction_raw):
            raise TransactionRawError("Invalid XinFin unsigned transaction raw.")

        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

        if loaded_transaction_raw["type"] not in ["xinfin_normal_unsigned", "xinfin_xrc20_normal_unsigned"]:
            raise TypeError(f"Invalid XinFin normal unsigned transaction raw type, "
                            f"you can't sign '{loaded_transaction_raw['type']}' type by using normal signature.")

        # Check parameter instances
        if not isinstance(solver, NormalSolver):
            raise TypeError(f"Solver must be XinFin NormalSolver, not '{type(solver).__name__}' type.")

        # Set transaction, fee, type and network
        self._fee, self._type, self._network, self._transaction = (
            loaded_transaction_raw["fee"], loaded_transaction_raw["type"],
            loaded_transaction_raw["network"], loaded_transaction_raw["transaction"]
        )

        wallet: Wallet = solver.solve()
        signed_normal_transaction: SignedTransaction = self.web3.eth.account.sign_transaction(
            transaction_dict=self._transaction,
            private_key=wallet.private_key()
        )

        self._signature = dict(
            hash=signed_normal_transaction["hash"].hex(),
            rawTransaction=signed_normal_transaction["rawTransaction"].hex(),
            r=signed_normal_transaction["r"],
            s=signed_normal_transaction["s"],
            v=signed_normal_transaction["v"]
        )
        self._type = "xinfin_xrc20_normal_signed" if self._xrc20 else "xinfin_normal_signed"

        self._signed_raw = b64encode(str(json.dumps(dict(
            fee=self._fee,
            type=self._type,
            transaction=self._transaction,
            signature=self._signature,
            network=self._network,
            xrc20=self._xrc20
        ))).encode()).decode()
        return self


class FundSignature(Signature):
    """
    XinFin Fund signature.

    :param network: XinFin network, defaults to ``mainnet``.
    :type network: str
    :param xrc20: Fund signature XRC20 token, default to ``False``.
    :type xrc20: bool
    :param provider: XinFin network provider, defaults to ``http``.
    :type provider: str

    :returns: FundSignature -- XinFin fund signature instance.

    .. note::
        XinFin has only two networks, ``mainnet``, ``apothem`` and ``testnet``.
    """

    def __init__(self, network: str = config["network"], xrc20: bool = False, provider: str = config["provider"]):
        super().__init__(
            network=network, xrc20=xrc20, provider=provider
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
        >>> fund_signature: FundSignature = FundSignature(network="testnet")
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="xprv9s21ZrQH143K3Y3pdbkbjreZQ9RVmqTLhRgf86uZyCJk2ou36YdUJt5frjwihGWmV1fQEDioiGZXWXUbHLy3kQf5xmhvhp8dZ2tfn6tgGUj", account=0, change=False, address=0)
        >>> fund_signature.sign(transaction_raw="eyJmZWUiOiAxMzg0NDgsICJ0eXBlIjogInhpbmZpbl9mdW5kX3Vuc2lnbmVkIiwgInRyYW5zYWN0aW9uIjogeyJjaGFpbklkIjogMTMzNywgImZyb20iOiAiMHgyMjI0Y2FBMjIzNURGOERhM0QyMDE2ZDJBQjExMzdEMmQ1NDhBMjMyIiwgInZhbHVlIjogMTAwMDAwMDAwMDAwMDAwMDAwMCwgIm5vbmNlIjogMiwgImdhcyI6IDEzODQ0OCwgImdhc1ByaWNlIjogMjAwMDAwMDAwMDAsICJ0byI6ICIweGRFMDZiMTBjNjc3NjVjOEMwYjlGNjRFMGVGNDIzYjQ1RWI4NmI4ZTciLCAiZGF0YSI6ICIweGY0ZmQzMDYyM2EyNmRhODJlYWQxNWE4MDUzM2EwMjY5NjY1NmIxNGI1ZGJmZDg0ZWIxNDc5MGYyZTFiZTVlOWU0NTgyMGVlYjAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMGY4ZDQzODA2MjYwY2ZjNmNjNzlmYjQwOGJhMTg5NzA1NDY2N2Y4MWMwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAyMjI0Y2FhMjIzNWRmOGRhM2QyMDE2ZDJhYjExMzdkMmQ1NDhhMjMyMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDA2MGUwMDZjMyJ9LCAic2lnbmF0dXJlIjogbnVsbCwgIm5ldHdvcmsiOiAidGVzdG5ldCJ9", solver=fund_solver)
        <swap.providers.xinfin.signature.FundSignature object at 0x0409DAF0>
        """

        # Check parameter instances
        if not is_transaction_raw(transaction_raw=transaction_raw):
            raise TransactionRawError("Invalid XinFin unsigned transaction raw.")

        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

        if loaded_transaction_raw["type"] not in ["xinfin_fund_unsigned", "xinfin_xrc20_fund_unsigned"]:
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
        self._type = "xinfin_xrc20_fund_signed" if self._xrc20 else "xinfin_fund_signed"

        self._signed_raw = b64encode(str(json.dumps(dict(
            fee=self._fee,
            type=self._type,
            transaction=self._transaction,
            signature=self._signature,
            network=self._network,
            xrc20=self._xrc20
        ))).encode()).decode()
        return self


class WithdrawSignature(Signature):
    """
    XinFin Withdraw signature.

    :param network: XinFin network, defaults to ``mainnet``.
    :type network: str
    :param xrc20: Fund signature XRC20 token, default to ``False``.
    :type xrc20: bool
    :param provider: XinFin network provider, defaults to ``http``.
    :type provider: str

    :returns: WithdrawSignature -- XinFin withdraw signature instance.

    .. note::
        XinFin has only two networks, ``mainnet``, ``apothem`` and ``testnet``.
    """

    def __init__(self, network: str = config["network"], xrc20: bool = False, provider: str = config["provider"]):
        super().__init__(
            network=network, xrc20=xrc20, provider=provider
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
        >>> withdraw_signature: WithdrawSignature = WithdrawSignature(network="testnet")
        >>> withdraw_solver: WithdrawSolver = WithdrawSolver(xprivate_key="xprv9s21ZrQH143K4Kpce43z5guPyxLrFoc2i8aQAq835Zzp4Rt7i6nZaMCnVSDyHT6MnmJJGKHMrCUqaYpGojrug1ZN5qQDdShQffmkyv5xyUR", account=0, change=False, address=0)
        >>> withdraw_signature.sign(transaction_raw="eyJmZWUiOiA4MjY4OSwgInR5cGUiOiAieGluZmluX3dpdGhkcmF3X3Vuc2lnbmVkIiwgInRyYW5zYWN0aW9uIjogeyJjaGFpbklkIjogMTMzNywgImZyb20iOiAiMHhmOEQ0MzgwNjI2MENGYzZjQzc5ZkI0MDhCQTE4OTcwNTQ2NjdGODFDIiwgInZhbHVlIjogMCwgIm5vbmNlIjogMCwgImdhcyI6IDgyNjg5LCAiZ2FzUHJpY2UiOiAyMDAwMDAwMDAwMCwgInRvIjogIjB4ZEUwNmIxMGM2Nzc2NWM4QzBiOUY2NEUwZUY0MjNiNDVFYjg2YjhlNyIsICJkYXRhIjogIjB4MDZhNTM2NjUxOTA5NTc1YzQzNmEwZWFiZTZjYWE3MmQ0ZmViMmM0YWVjZWVmNTg2ZmU5NGNhODJmMzZjZTljMjBlZmRhNGI0MDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDA0MDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMGU0ODY1NmM2YzZmMjA0ZDY1Njg2NTcyNjU3NDIxMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwIn0sICJzaWduYXR1cmUiOiBudWxsLCAibmV0d29yayI6ICJ0ZXN0bmV0In0", solver=withdraw_solver)
        <swap.providers.xinfin.signature.WithdrawSignature object at 0x0409DAF0>
        """

        # Check parameter instances
        if not is_transaction_raw(transaction_raw=transaction_raw):
            raise TransactionRawError("Invalid XinFin unsigned transaction raw.")

        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

        if loaded_transaction_raw["type"] not in ["xinfin_withdraw_unsigned", "xinfin_xrc20_withdraw_unsigned"]:
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
        self._type = "xinfin_xrc20_withdraw_signed" if self._xrc20 else "xinfin_withdraw_signed"

        self._signed_raw = b64encode(str(json.dumps(dict(
            fee=self._fee,
            type=self._type,
            transaction=self._transaction,
            signature=self._signature,
            network=self._network,
            xrc20=self._xrc20
        ))).encode()).decode()
        return self


class RefundSignature(Signature):
    """
    XinFin Refund signature.

    :param network: XinFin network, defaults to ``mainnet``.
    :type network: str
    :param xrc20: Fund signature XRC20 token, default to ``False``.
    :type xrc20: bool
    :param provider: XinFin network provider, defaults to ``http``.
    :type provider: str

    :returns: RefundSignature -- XinFin refund signature instance.

    .. note::
        XinFin has only two networks, ``mainnet``, ``apothem`` and ``testnet``.
    """

    def __init__(self, network: str = config["network"], xrc20: bool = False, provider: str = config["provider"]):
        super().__init__(
            network=network, xrc20=xrc20, provider=provider
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
        >>> refund_signature: RefundSignature = RefundSignature(network="testnet")
        >>> refund_solver: RefundSolver = RefundSolver(xprivate_key="xprv9s21ZrQH143K3Y3pdbkbjreZQ9RVmqTLhRgf86uZyCJk2ou36YdUJt5frjwihGWmV1fQEDioiGZXWXUbHLy3kQf5xmhvhp8dZ2tfn6tgGUj", account=0, change=False, address=0)
        >>> refund_signature.sign(transaction_raw="eyJmZWUiOiA1OTIzMiwgInR5cGUiOiAieGluZmluX3JlZnVuZF91bnNpZ25lZCIsICJ0cmFuc2FjdGlvbiI6IHsiY2hhaW5JZCI6IDEzMzcsICJmcm9tIjogIjB4MjIyNGNhQTIyMzVERjhEYTNEMjAxNmQyQUIxMTM3RDJkNTQ4QTIzMiIsICJ2YWx1ZSI6IDAsICJub25jZSI6IDIsICJnYXMiOiA1OTIzMiwgImdhc1ByaWNlIjogMjAwMDAwMDAwMDAsICJ0byI6ICIweGRFMDZiMTBjNjc3NjVjOEMwYjlGNjRFMGVGNDIzYjQ1RWI4NmI4ZTciLCAiZGF0YSI6ICIweDcyNDlmYmI2MTkwOTU3NWM0MzZhMGVhYmU2Y2FhNzJkNGZlYjJjNGFlY2VlZjU4NmZlOTRjYTgyZjM2Y2U5YzIwZWZkYTRiNCJ9LCAic2lnbmF0dXJlIjogbnVsbCwgIm5ldHdvcmsiOiAidGVzdG5ldCJ9", solver=refund_solver)
        <swap.providers.xinfin.signature.RefundSignature object at 0x0409DAF0>
        """

        # Check parameter instances
        if not is_transaction_raw(transaction_raw=transaction_raw):
            raise TransactionRawError("Invalid XinFin unsigned transaction raw.")

        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

        if loaded_transaction_raw["type"] not in ["xinfin_refund_unsigned", "xinfin_xrc20_refund_unsigned"]:
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
        self._type = "xinfin_xrc20_refund_signed" if self._xrc20 else "xinfin_refund_signed"

        self._signed_raw = b64encode(str(json.dumps(dict(
            fee=self._fee,
            type=self._type,
            transaction=self._transaction,
            signature=self._signature,
            network=self._network,
            xrc20=self._xrc20
        ))).encode()).decode()
        return self
