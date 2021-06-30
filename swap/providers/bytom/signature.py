#!/usr/bin/env python3

from base64 import (
    b64encode, b64decode
)
from typing import (
    Optional, Union, List
)

import json

from ...utils import clean_transaction_raw
from ...exceptions import (
    TransactionRawError, NetworkError, UnitError
)
from ..config import bytom as config
from .transaction import Transaction
from .solver import (
    FundSolver, WithdrawSolver, RefundSolver
)
from .rpc import decode_raw
from .utils import (
    is_network, is_transaction_raw, amount_unit_converter
)


class Signature(Transaction):
    """
    Bytom Signature.

    :param network: Bytom network, defaults to mainnet.
    :type network: str

    :returns: Signature -- Bytom signature instance.

    .. note::
        Bytom has only three networks, ``mainnet``, ``solonet`` and ``testnet``.
    """

    def __init__(self, network: str = config["network"]):

        if not is_network(network=network):
            raise NetworkError(f"Invalid Bytom '{network}' network",
                               "choose only 'mainnet', 'solonet' or 'testnet' networks.")

        self._network: str = network
        self._address: Optional[str] = None
        self._transaction: Optional[dict] = None
        self._type: Optional[str] = None
        self._confirmations: int = config["confirmations"]
        self._signed_raw: Optional[str] = None
        self._fee: int = 0

        super().__init__(network)

    def fee(self, unit: str = config["unit"]) -> Union[int, float]:
        """
        Get Bytom transaction fee.

        :param unit: Bytom unit, default to ``NEU``.
        :type unit: str

        :returns: int, float -- Bytom transaction fee.

        >>> from swap.providers.bytom.signature import Signature
        >>> from swap.providers.bytom.solver import FundSolver
        >>> unsigned_fund_transaction_raw: str = "eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogImJtMXFrOXZqNGphZXpsY25qZGNrZHM0ZmttOGZ3djVrYXdtcTlxcnVmeCIsICJyYXciOiAiMDcwMTAwMDEwMTVmMDE1ZGY3ZGY0ZDA2YTNmZTNjOGFjNjQzOGYyNWY5Yzk3NzQ0YTEwNDU1MzU3ODU3Nzc1NTI2YzNlNmM3NTJmYjY5ZWFmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOThhM2IxNWEwMTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDIyMDEyMGZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIwMjAxNDhmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBhZGUyMDQwMTIyMDAyMGU3ZjRhOTgxNWYzYTM2YzYxNmM1NjY2Yjk3ZmI3ZmRhY2QzNzIwYzExN2QwNzhjNDI5NDk0ZDFiNjE3ZmU3ZDQwMDAxM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYjBjMmIzNTUwMTE2MDAxNGIxNTkyYWNiYjkxN2YxMzkzNzE2NmMyYTliNmNlOTczMjk2ZWJiNjAwMCIsICJoYXNoIjogImEzMDc4YWYwODEwYzY4YTdiYjZmMmY0MmNkNjdkY2U5ZGVhM2Q3NzAyOGNhMGM1MjcyMjRlNDUyNDAzOGFiYzQiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiZjQyYTJiNmUxNTU4NWI4OGRhOGIzNDIzN2M3YTZmZDgzYWYxMmVlNjk3MTgxM2Q2NmNmNzk0YTYzZWJjYzE2ZiJdLCAicHVibGljX2tleSI6ICJmZTZiM2ZkNDQ1ODI5MWIxOTYwNWQ5MjgzN2FlMTA2MGNjMDIzN2U2ODAyMmIyZWI5ZmFmMDFhMTE4MjI2MjEyIiwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogIm0vNDQvMTUzLzEvMC8xIn1dLCAic2lnbmF0dXJlcyI6IFtdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInR5cGUiOiAiYnl0b21fZnVuZF91bnNpZ25lZCJ9"
        >>> signature: Signature = Signature(network="mainnet")
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="58775359b7b3588dcdc1bcf373489fa1272cacc03909f78469657b0208e66e46daedfdd0fd8f8df14e2084c7e8df4701db3062dded1c713e0aae734ac09c4afd")
        >>> signature.sign(transaction_raw=unsigned_fund_transaction_raw, solver=fund_solver)
        >>> signature.fee(unit="NEU")
        449000
        """

        if self._transaction is None:
            raise ValueError("Transaction is none, sign unsigned transaction raw first.")
        if unit not in ["BTM", "mBTM", "NEU"]:
            raise UnitError("Invalid Bytom unit, choose only BTM, mBTM or NEU units.")
        return self._fee if unit == "NEU" else \
            amount_unit_converter(amount=self._fee, unit_from=f"NEU2{unit}")

    def hash(self) -> str:
        """
        Get Bytom signature transaction hash.

        :returns: str -- Bytom signature transaction hash or transaction id.

        >>> from swap.providers.bytom.signature import Signature
        >>> from swap.providers.bytom.solver import WithdrawSolver
        >>> unsigned_withdraw_transaction_raw: str = "eyJmZWUiOiA1MDkwMDAsICJhZGRyZXNzIjogImJtMXF1bDYybnEybDhnbXZ2OWs5dmU0ZTA3bWxtdHhud2d4cHpsZzgzM3BmZjl4M2tjdGx1bDJxNzI3anl5IiwgInJhdyI6ICIwNzAxMDAwMTAxNmIwMTY5ZjdkZjRkMDZhM2ZlM2M4YWM2NDM4ZjI1ZjljOTc3NDRhMTA0NTUzNTc4NTc3NzU1MjZjM2U2Yzc1MmZiNjllYWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGFkZTIwNDAwMDEyMjAwMjBlN2Y0YTk4MTVmM2EzNmM2MTZjNTY2NmI5N2ZiN2ZkYWNkMzcyMGMxMTdkMDc4YzQyOTQ5NGQxYjYxN2ZlN2Q0MDEwMDAxMDEzY2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZiOGE0YzMwNDAxMTYwMDE0ODg3ZWU2NmQ4NGE4MmYyZDg2ODI0YTQ1YmI1MWZkZWEwM2M5MmY0OTAwIiwgImhhc2giOiAiZDFlODRjMzdmNDEwNTZmNGRmMzk4NTIzZjg0ZWNmMDc5Mzc3ZmQ4NWU0NTYxYzEwZWMwMzgxOGNkNGRiN2VjMCIsICJ1bnNpZ25lZF9kYXRhcyI6IFt7ImRhdGFzIjogWyI0NWQxNzQ2YTFlYzA2OTVkM2UwNjA1OWM0MTM4NzIwNDBkMjRmODY0OTlkZGFmYWI0ODE3NzM2OGU1YzcyODgzIl0sICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6IG51bGx9XSwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX3dpdGhkcmF3X3Vuc2lnbmVkIn0"
        >>> bytecode: str = "03285d0a20fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"
        >>> signature: Signature = Signature(network="mainnet")
        >>> withdraw_solver: WithdrawSolver = WithdrawSolver(xprivate_key="58dd4094155bbebf2868189231c47e4e0edbd9f74545f843c9537259e1d7a656983aef283d0ccebecc2d33577a9f650b53ac7adff44f48ec839e3346cc22418f", secret_key="Hello Meheret!", bytecode=bytecode)
        >>> signature.sign(transaction_raw=unsigned_withdraw_transaction_raw, solver=withdraw_solver)
        >>> signature.hash()
        "d1e84c37f41056f4df398523f84ecf079377fd85e4561c10ec03818cd4db7ec0"
        """

        if self._transaction is None:
            raise ValueError("Transaction is none, sign unsigned transaction raw first.")
        return self._transaction["hash"]

    def json(self) -> dict:
        """
        Get Bytom signature transaction json format.

        :returns: dict -- Bytom signature transaction json format.

        >>> from swap.providers.bytom.signature import Signature
        >>> from swap.providers.bytom.solver import FundSolver
        >>> unsigned_fund_transaction_raw: str = "eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogImJtMXFrOXZqNGphZXpsY25qZGNrZHM0ZmttOGZ3djVrYXdtcTlxcnVmeCIsICJyYXciOiAiMDcwMTAwMDEwMTVmMDE1ZGY3ZGY0ZDA2YTNmZTNjOGFjNjQzOGYyNWY5Yzk3NzQ0YTEwNDU1MzU3ODU3Nzc1NTI2YzNlNmM3NTJmYjY5ZWFmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOThhM2IxNWEwMTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDIyMDEyMGZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIwMjAxNDhmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBhZGUyMDQwMTIyMDAyMGU3ZjRhOTgxNWYzYTM2YzYxNmM1NjY2Yjk3ZmI3ZmRhY2QzNzIwYzExN2QwNzhjNDI5NDk0ZDFiNjE3ZmU3ZDQwMDAxM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYjBjMmIzNTUwMTE2MDAxNGIxNTkyYWNiYjkxN2YxMzkzNzE2NmMyYTliNmNlOTczMjk2ZWJiNjAwMCIsICJoYXNoIjogImEzMDc4YWYwODEwYzY4YTdiYjZmMmY0MmNkNjdkY2U5ZGVhM2Q3NzAyOGNhMGM1MjcyMjRlNDUyNDAzOGFiYzQiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiZjQyYTJiNmUxNTU4NWI4OGRhOGIzNDIzN2M3YTZmZDgzYWYxMmVlNjk3MTgxM2Q2NmNmNzk0YTYzZWJjYzE2ZiJdLCAicHVibGljX2tleSI6ICJmZTZiM2ZkNDQ1ODI5MWIxOTYwNWQ5MjgzN2FlMTA2MGNjMDIzN2U2ODAyMmIyZWI5ZmFmMDFhMTE4MjI2MjEyIiwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogIm0vNDQvMTUzLzEvMC8xIn1dLCAic2lnbmF0dXJlcyI6IFtdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInR5cGUiOiAiYnl0b21fZnVuZF91bnNpZ25lZCJ9"
        >>> signature: Signature = Signature(network="mainnet")
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="58775359b7b3588dcdc1bcf373489fa1272cacc03909f78469657b0208e66e46daedfdd0fd8f8df14e2084c7e8df4701db3062dded1c713e0aae734ac09c4afd")
        >>> signature.sign(transaction_raw=unsigned_fund_transaction_raw, solver=fund_solver)
        >>> signature.json()
        {"tx_id": "a3078af0810c68a7bb6f2f42cd67dce9dea3d77028ca0c527224e4524038abc4", "version": 1, "size": 275, "time_range": 0, "inputs": [{"type": "spend", "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "asset_definition": {}, "amount": 189551000, "control_program": "0014b1592acbb917f13937166c2a9b6ce973296ebb60", "address": "bm1qk9vj4jaezlcnjdckds4fkm8fwv5kawmq9qrufx", "spent_output_id": "dd12e69d28a3e581b8b4501f9979ad39ba1e6b7e2163fe112a54a81fc2e8d6e3", "input_id": "e55412ce943b72860ea06f7bc4c7ca4d9913b3dd736f8915279741c9a8c3bb2d", "witness_arguments": ["fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212"], "sign_data": "f42a2b6e15585b88da8b34237c7a6fd83af12ee6971813d66cf794a63ebcc16f"}], "outputs": [{"type": "control", "id": "ecbd05faf0c2bec7706fb1d5230768d86eddc4d65fae2e4b0f995e6aa278c278", "position": 0, "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "asset_definition": {}, "amount": 10000000, "control_program": "0020e7f4a9815f3a36c616c5666b97fb7fdacd3720c117d078c429494d1b617fe7d4", "address": "bm1qul62nq2l8gmvv9k9ve4e07mlmtxnwgxpzlg833pff9x3kctlul2q727jyy"}, {"type": "control", "id": "9b13259cf0ddfebeb6f616e1f5f52a7372b20bd3d7ba694cdbc5490cdc675538", "position": 1, "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "asset_definition": {}, "amount": 179102000, "control_program": "0014b1592acbb917f13937166c2a9b6ce973296ebb60", "address": "bm1qk9vj4jaezlcnjdckds4fkm8fwv5kawmq9qrufx"}], "fee": 449000}
        """
        if self._transaction is None:
            raise ValueError("Transaction is none, sign unsigned transaction raw first.")
        return decode_raw(raw=self._transaction["raw"])

    def raw(self) -> str:
        """
        Get Bytom signature transaction raw.

        :returns: str -- Bytom signature transaction raw.

        >>> from swap.providers.bytom.signature import Signature
        >>> from swap.providers.bytom.solver import FundSolver
        >>> unsigned_fund_transaction_raw: str = "eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogImJtMXFrOXZqNGphZXpsY25qZGNrZHM0ZmttOGZ3djVrYXdtcTlxcnVmeCIsICJyYXciOiAiMDcwMTAwMDEwMTVmMDE1ZGY3ZGY0ZDA2YTNmZTNjOGFjNjQzOGYyNWY5Yzk3NzQ0YTEwNDU1MzU3ODU3Nzc1NTI2YzNlNmM3NTJmYjY5ZWFmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOThhM2IxNWEwMTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDIyMDEyMGZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIwMjAxNDhmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBhZGUyMDQwMTIyMDAyMGU3ZjRhOTgxNWYzYTM2YzYxNmM1NjY2Yjk3ZmI3ZmRhY2QzNzIwYzExN2QwNzhjNDI5NDk0ZDFiNjE3ZmU3ZDQwMDAxM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYjBjMmIzNTUwMTE2MDAxNGIxNTkyYWNiYjkxN2YxMzkzNzE2NmMyYTliNmNlOTczMjk2ZWJiNjAwMCIsICJoYXNoIjogImEzMDc4YWYwODEwYzY4YTdiYjZmMmY0MmNkNjdkY2U5ZGVhM2Q3NzAyOGNhMGM1MjcyMjRlNDUyNDAzOGFiYzQiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiZjQyYTJiNmUxNTU4NWI4OGRhOGIzNDIzN2M3YTZmZDgzYWYxMmVlNjk3MTgxM2Q2NmNmNzk0YTYzZWJjYzE2ZiJdLCAicHVibGljX2tleSI6ICJmZTZiM2ZkNDQ1ODI5MWIxOTYwNWQ5MjgzN2FlMTA2MGNjMDIzN2U2ODAyMmIyZWI5ZmFmMDFhMTE4MjI2MjEyIiwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogIm0vNDQvMTUzLzEvMC8xIn1dLCAic2lnbmF0dXJlcyI6IFtdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInR5cGUiOiAiYnl0b21fZnVuZF91bnNpZ25lZCJ9"
        >>> signature: Signature = Signature(network="mainnet")
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="58775359b7b3588dcdc1bcf373489fa1272cacc03909f78469657b0208e66e46daedfdd0fd8f8df14e2084c7e8df4701db3062dded1c713e0aae734ac09c4afd")
        >>> signature.sign(transaction_raw=unsigned_fund_transaction_raw, solver=fund_solver)
        >>> signature.raw()
        "07010001015f015df7df4d06a3fe3c8ac6438f25f9c97744a10455357857775526c3e6c752fb69eaffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff98a3b15a0101160014b1592acbb917f13937166c2a9b6ce973296ebb60220120fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212020148ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff80ade20401220020e7f4a9815f3a36c616c5666b97fb7fdacd3720c117d078c429494d1b617fe7d400013cffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffb0c2b35501160014b1592acbb917f13937166c2a9b6ce973296ebb6000"
        """

        if self._transaction is None:
            raise ValueError("Transaction is none, sign unsigned transaction raw first.")
        return self._transaction["raw"]

    def type(self) -> str:
        """
        Get Bytom signature transaction type.

        :returns: str -- Bytom signature transaction type.

        >>> from swap.providers.bytom.signature import Signature
        >>> from swap.providers.bytom.solver import RefundSolver
        >>> unsigned_refund_transaction_raw: str = "eyJmZWUiOiA1MDkwMDAsICJhZGRyZXNzIjogImJtMXF1bDYybnEybDhnbXZ2OWs5dmU0ZTA3bWxtdHhud2d4cHpsZzgzM3BmZjl4M2tjdGx1bDJxNzI3anl5IiwgImhhc2giOiAiMTcyMmFhOTMwZjZmOTNiNGM4Nzc4OGVhNTVmNDkwNTVmMjZmODY4MjFiY2QxMWE2NGQ0MmJjYjllM2I4YTk2ZCIsICJyYXciOiAiMDcwMTAwMDEwMTZiMDE2OWY3ZGY0ZDA2YTNmZTNjOGFjNjQzOGYyNWY5Yzk3NzQ0YTEwNDU1MzU3ODU3Nzc1NTI2YzNlNmM3NTJmYjY5ZWFmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBhZGUyMDQwMDAxMjIwMDIwZTdmNGE5ODE1ZjNhMzZjNjE2YzU2NjZiOTdmYjdmZGFjZDM3MjBjMTE3ZDA3OGM0Mjk0OTRkMWI2MTdmZTdkNDAxMDAwMTAxM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYjhhNGMzMDQwMTE2MDAxNGIxNTkyYWNiYjkxN2YxMzkzNzE2NmMyYTliNmNlOTczMjk2ZWJiNjAwMCIsICJ1bnNpZ25lZF9kYXRhcyI6IFt7ImRhdGFzIjogWyJjYzc4YzFmYjY0OGY4ODI2ZTRkZDRmODVmODg1YWM3NTg2NmMwMjMzYjBhZjY1ODE3NTNkODU4MzA0YjhlMDRiIl0sICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6IG51bGx9XSwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX3JlZnVuZF91bnNpZ25lZCJ9"
        >>> bytecode: str = "03285d0a20fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"
        >>> signature: Signature = Signature(network="mainnet")
        >>> refund_solver: RefundSolver = RefundSolver(xprivate_key="58775359b7b3588dcdc1bcf373489fa1272cacc03909f78469657b0208e66e46daedfdd0fd8f8df14e2084c7e8df4701db3062dded1c713e0aae734ac09c4afd", bytecode=bytecode)
        >>> signature.sign(transaction_raw=unsigned_refund_transaction_raw, solver=refund_solver)
        >>> signature.type()
        "bytom_refund_signed"
        """

        if self._type is None:
            raise ValueError("Type is none, sign unsigned transaction raw first.")
        return self._type

    def sign(self, transaction_raw: str, solver: Union[FundSolver, WithdrawSolver, RefundSolver]) \
            -> Union["FundSignature", "WithdrawSignature", "RefundSignature"]:
        """
        Sign unsigned transaction raw.

        :param transaction_raw: Bytom unsigned transaction raw.
        :type transaction_raw: str
        :param solver: Bytom solver
        :type solver: bytom.solver.NormalSolver, bytom.solver.FundSolver, bytom.solver.WithdrawSolver, bytom.solver.RefundSolver

        :returns: FundSignature, WithdrawSignature, RefundSignature -- Bytom signature instance.

        >>> from swap.providers.bytom.signature import Signature
        >>> from swap.providers.bytom.solver import FundSolver
        >>> unsigned_fund_transaction_raw: str = "eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogImJtMXFrOXZqNGphZXpsY25qZGNrZHM0ZmttOGZ3djVrYXdtcTlxcnVmeCIsICJyYXciOiAiMDcwMTAwMDEwMTVmMDE1ZGY3ZGY0ZDA2YTNmZTNjOGFjNjQzOGYyNWY5Yzk3NzQ0YTEwNDU1MzU3ODU3Nzc1NTI2YzNlNmM3NTJmYjY5ZWFmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOThhM2IxNWEwMTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDIyMDEyMGZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIwMjAxNDhmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBhZGUyMDQwMTIyMDAyMGU3ZjRhOTgxNWYzYTM2YzYxNmM1NjY2Yjk3ZmI3ZmRhY2QzNzIwYzExN2QwNzhjNDI5NDk0ZDFiNjE3ZmU3ZDQwMDAxM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYjBjMmIzNTUwMTE2MDAxNGIxNTkyYWNiYjkxN2YxMzkzNzE2NmMyYTliNmNlOTczMjk2ZWJiNjAwMCIsICJoYXNoIjogImEzMDc4YWYwODEwYzY4YTdiYjZmMmY0MmNkNjdkY2U5ZGVhM2Q3NzAyOGNhMGM1MjcyMjRlNDUyNDAzOGFiYzQiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiZjQyYTJiNmUxNTU4NWI4OGRhOGIzNDIzN2M3YTZmZDgzYWYxMmVlNjk3MTgxM2Q2NmNmNzk0YTYzZWJjYzE2ZiJdLCAicHVibGljX2tleSI6ICJmZTZiM2ZkNDQ1ODI5MWIxOTYwNWQ5MjgzN2FlMTA2MGNjMDIzN2U2ODAyMmIyZWI5ZmFmMDFhMTE4MjI2MjEyIiwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogIm0vNDQvMTUzLzEvMC8xIn1dLCAic2lnbmF0dXJlcyI6IFtdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInR5cGUiOiAiYnl0b21fZnVuZF91bnNpZ25lZCJ9"
        >>> signature: Signature = Signature(network="mainnet")
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="58775359b7b3588dcdc1bcf373489fa1272cacc03909f78469657b0208e66e46daedfdd0fd8f8df14e2084c7e8df4701db3062dded1c713e0aae734ac09c4afd")
        >>> signature.sign(transaction_raw=unsigned_fund_transaction_raw, solver=fund_solver)
        <swap.providers.bytom.signature.FundSignature object at 0x0409DAF0>
        """

        if not is_transaction_raw(transaction_raw=transaction_raw):
            raise TransactionRawError("Invalid Bytom unsigned transaction raw.")

        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

        self._type = loaded_transaction_raw["type"]
        if loaded_transaction_raw["type"] == "bytom_fund_unsigned":
            return FundSignature(network=self._network).sign(
                transaction_raw=transaction_raw, solver=solver
            )
        elif loaded_transaction_raw["type"] == "bytom_withdraw_unsigned":
            return WithdrawSignature(network=self._network).sign(
                transaction_raw=transaction_raw, solver=solver
            )
        elif loaded_transaction_raw["type"] == "bytom_refund_unsigned":
            return RefundSignature(network=self._network).sign(
                transaction_raw=transaction_raw, solver=solver
            )

    def unsigned_datas(self) -> List[dict]:
        """
        Get Bytom transaction unsigned datas with instruction.

        :returns: list -- Bytom transaction unsigned datas.

        >>> from swap.providers.bytom.signature import Signature
        >>> from swap.providers.bytom.solver import WithdrawSolver
        >>> unsigned_withdraw_transaction_raw: str = "eyJmZWUiOiA1MDkwMDAsICJhZGRyZXNzIjogImJtMXF1bDYybnEybDhnbXZ2OWs5dmU0ZTA3bWxtdHhud2d4cHpsZzgzM3BmZjl4M2tjdGx1bDJxNzI3anl5IiwgInJhdyI6ICIwNzAxMDAwMTAxNmIwMTY5ZjdkZjRkMDZhM2ZlM2M4YWM2NDM4ZjI1ZjljOTc3NDRhMTA0NTUzNTc4NTc3NzU1MjZjM2U2Yzc1MmZiNjllYWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGFkZTIwNDAwMDEyMjAwMjBlN2Y0YTk4MTVmM2EzNmM2MTZjNTY2NmI5N2ZiN2ZkYWNkMzcyMGMxMTdkMDc4YzQyOTQ5NGQxYjYxN2ZlN2Q0MDEwMDAxMDEzY2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZiOGE0YzMwNDAxMTYwMDE0ODg3ZWU2NmQ4NGE4MmYyZDg2ODI0YTQ1YmI1MWZkZWEwM2M5MmY0OTAwIiwgImhhc2giOiAiZDFlODRjMzdmNDEwNTZmNGRmMzk4NTIzZjg0ZWNmMDc5Mzc3ZmQ4NWU0NTYxYzEwZWMwMzgxOGNkNGRiN2VjMCIsICJ1bnNpZ25lZF9kYXRhcyI6IFt7ImRhdGFzIjogWyI0NWQxNzQ2YTFlYzA2OTVkM2UwNjA1OWM0MTM4NzIwNDBkMjRmODY0OTlkZGFmYWI0ODE3NzM2OGU1YzcyODgzIl0sICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6IG51bGx9XSwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX3dpdGhkcmF3X3Vuc2lnbmVkIn0"
        >>> bytecode: str = "03285d0a20fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"
        >>> signature: Signature = Signature(network="mainnet")
        >>> withdraw_solver: WithdrawSolver = WithdrawSolver(xprivate_key="58dd4094155bbebf2868189231c47e4e0edbd9f74545f843c9537259e1d7a656983aef283d0ccebecc2d33577a9f650b53ac7adff44f48ec839e3346cc22418f", secret_key="Hello Meheret!", bytecode=bytecode)
        >>> signature.sign(transaction_raw=unsigned_withdraw_transaction_raw, solver=withdraw_solver)
        >>> signature.unsigned_datas()
        [{"datas": ["45d1746a1ec0695d3e06059c413872040d24f86499ddafab48177368e5c72883"], "network": "mainnet", "path": null}]
        """

        if self._transaction is None:
            raise ValueError("Transaction is none, sign unsigned transaction raw first.")
        return self._transaction["unsigned_datas"]

    def signatures(self) -> List[List[str]]:
        """
        Get Bytom transaction signatures(signed datas).

        :returns: list -- Bytom transaction signatures.

        >>> from swap.providers.bytom.signature import Signature
        >>> from swap.providers.bytom.solver import FundSolver
        >>> unsigned_fund_transaction_raw: str = "eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogImJtMXFrOXZqNGphZXpsY25qZGNrZHM0ZmttOGZ3djVrYXdtcTlxcnVmeCIsICJyYXciOiAiMDcwMTAwMDEwMTVmMDE1ZGY3ZGY0ZDA2YTNmZTNjOGFjNjQzOGYyNWY5Yzk3NzQ0YTEwNDU1MzU3ODU3Nzc1NTI2YzNlNmM3NTJmYjY5ZWFmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOThhM2IxNWEwMTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDIyMDEyMGZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIwMjAxNDhmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBhZGUyMDQwMTIyMDAyMGU3ZjRhOTgxNWYzYTM2YzYxNmM1NjY2Yjk3ZmI3ZmRhY2QzNzIwYzExN2QwNzhjNDI5NDk0ZDFiNjE3ZmU3ZDQwMDAxM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYjBjMmIzNTUwMTE2MDAxNGIxNTkyYWNiYjkxN2YxMzkzNzE2NmMyYTliNmNlOTczMjk2ZWJiNjAwMCIsICJoYXNoIjogImEzMDc4YWYwODEwYzY4YTdiYjZmMmY0MmNkNjdkY2U5ZGVhM2Q3NzAyOGNhMGM1MjcyMjRlNDUyNDAzOGFiYzQiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiZjQyYTJiNmUxNTU4NWI4OGRhOGIzNDIzN2M3YTZmZDgzYWYxMmVlNjk3MTgxM2Q2NmNmNzk0YTYzZWJjYzE2ZiJdLCAicHVibGljX2tleSI6ICJmZTZiM2ZkNDQ1ODI5MWIxOTYwNWQ5MjgzN2FlMTA2MGNjMDIzN2U2ODAyMmIyZWI5ZmFmMDFhMTE4MjI2MjEyIiwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogIm0vNDQvMTUzLzEvMC8xIn1dLCAic2lnbmF0dXJlcyI6IFtdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInR5cGUiOiAiYnl0b21fZnVuZF91bnNpZ25lZCJ9"
        >>> signature: Signature = Signature(network="mainnet")
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="58775359b7b3588dcdc1bcf373489fa1272cacc03909f78469657b0208e66e46daedfdd0fd8f8df14e2084c7e8df4701db3062dded1c713e0aae734ac09c4afd")
        >>> signature.sign(transaction_raw=unsigned_fund_transaction_raw, solver=fund_solver)
        >>> signature.signatures()
        [["b82e97abc4b70f7ffe7f783254c63e61436d6a7ad15da89b1fb791f91d1d6aa0bab7ff86328eabd2959f5475dde443e613ce7dfe70411be5b469b02069164a06"]]
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")
        return self._signatures

    def transaction_raw(self) -> str:
        """
        Get Bytom signed transaction raw.

        :returns: str -- Bytom signed transaction raw.

        >>> from swap.providers.bytom.signature import Signature
        >>> from swap.providers.bytom.solver import FundSolver
        >>> unsigned_fund_transaction_raw: str = "eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogImJtMXFrOXZqNGphZXpsY25qZGNrZHM0ZmttOGZ3djVrYXdtcTlxcnVmeCIsICJyYXciOiAiMDcwMTAwMDEwMTVmMDE1ZGY3ZGY0ZDA2YTNmZTNjOGFjNjQzOGYyNWY5Yzk3NzQ0YTEwNDU1MzU3ODU3Nzc1NTI2YzNlNmM3NTJmYjY5ZWFmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOThhM2IxNWEwMTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDIyMDEyMGZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIwMjAxNDhmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBhZGUyMDQwMTIyMDAyMGU3ZjRhOTgxNWYzYTM2YzYxNmM1NjY2Yjk3ZmI3ZmRhY2QzNzIwYzExN2QwNzhjNDI5NDk0ZDFiNjE3ZmU3ZDQwMDAxM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYjBjMmIzNTUwMTE2MDAxNGIxNTkyYWNiYjkxN2YxMzkzNzE2NmMyYTliNmNlOTczMjk2ZWJiNjAwMCIsICJoYXNoIjogImEzMDc4YWYwODEwYzY4YTdiYjZmMmY0MmNkNjdkY2U5ZGVhM2Q3NzAyOGNhMGM1MjcyMjRlNDUyNDAzOGFiYzQiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiZjQyYTJiNmUxNTU4NWI4OGRhOGIzNDIzN2M3YTZmZDgzYWYxMmVlNjk3MTgxM2Q2NmNmNzk0YTYzZWJjYzE2ZiJdLCAicHVibGljX2tleSI6ICJmZTZiM2ZkNDQ1ODI5MWIxOTYwNWQ5MjgzN2FlMTA2MGNjMDIzN2U2ODAyMmIyZWI5ZmFmMDFhMTE4MjI2MjEyIiwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogIm0vNDQvMTUzLzEvMC8xIn1dLCAic2lnbmF0dXJlcyI6IFtdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInR5cGUiOiAiYnl0b21fZnVuZF91bnNpZ25lZCJ9"
        >>> signature: Signature = Signature(network="mainnet")
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="58775359b7b3588dcdc1bcf373489fa1272cacc03909f78469657b0208e66e46daedfdd0fd8f8df14e2084c7e8df4701db3062dded1c713e0aae734ac09c4afd")
        >>> signature.sign(transaction_raw=unsigned_fund_transaction_raw, solver=fund_solver)
        >>> signature.transaction_raw()
        "eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogImJtMXFrOXZqNGphZXpsY25qZGNrZHM0ZmttOGZ3djVrYXdtcTlxcnVmeCIsICJyYXciOiAiMDcwMTAwMDEwMTVmMDE1ZGY3ZGY0ZDA2YTNmZTNjOGFjNjQzOGYyNWY5Yzk3NzQ0YTEwNDU1MzU3ODU3Nzc1NTI2YzNlNmM3NTJmYjY5ZWFmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOThhM2IxNWEwMTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDIyMDEyMGZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIwMjAxNDhmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBhZGUyMDQwMTIyMDAyMGU3ZjRhOTgxNWYzYTM2YzYxNmM1NjY2Yjk3ZmI3ZmRhY2QzNzIwYzExN2QwNzhjNDI5NDk0ZDFiNjE3ZmU3ZDQwMDAxM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYjBjMmIzNTUwMTE2MDAxNGIxNTkyYWNiYjkxN2YxMzkzNzE2NmMyYTliNmNlOTczMjk2ZWJiNjAwMCIsICJoYXNoIjogImEzMDc4YWYwODEwYzY4YTdiYjZmMmY0MmNkNjdkY2U5ZGVhM2Q3NzAyOGNhMGM1MjcyMjRlNDUyNDAzOGFiYzQiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiZjQyYTJiNmUxNTU4NWI4OGRhOGIzNDIzN2M3YTZmZDgzYWYxMmVlNjk3MTgxM2Q2NmNmNzk0YTYzZWJjYzE2ZiJdLCAicHVibGljX2tleSI6ICJmZTZiM2ZkNDQ1ODI5MWIxOTYwNWQ5MjgzN2FlMTA2MGNjMDIzN2U2ODAyMmIyZWI5ZmFmMDFhMTE4MjI2MjEyIiwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogIm0vNDQvMTUzLzEvMC8xIn1dLCAic2lnbmF0dXJlcyI6IFtbImI4MmU5N2FiYzRiNzBmN2ZmZTdmNzgzMjU0YzYzZTYxNDM2ZDZhN2FkMTVkYTg5YjFmYjc5MWY5MWQxZDZhYTBiYWI3ZmY4NjMyOGVhYmQyOTU5ZjU0NzVkZGU0NDNlNjEzY2U3ZGZlNzA0MTFiZTViNDY5YjAyMDY5MTY0YTA2Il1dLCAibmV0d29yayI6ICJtYWlubmV0IiwgInR5cGUiOiAiYnl0b21fZnVuZF9zaWduZWQifQ"
        """

        if self._signed_raw is None:
            raise ValueError("Transaction is none, sign unsigned transaction raw first.")
        return clean_transaction_raw(self._signed_raw)


class FundSignature(Signature):
    """
    Bytom Fund signature.

    :param network: Bytom network, defaults to ``mainnet``.
    :type network: str

    :returns: FundSignature -- Bytom fund signature instance.
    """

    def __init__(self, network: str = config["network"]):
        super().__init__(network=network)

    def sign(self, transaction_raw: str, solver: FundSolver) -> "FundSignature":
        """
        Sign unsigned fund transaction raw.

        :param transaction_raw: Bytom unsigned fund transaction raw.
        :type transaction_raw: str
        :param solver: Bytom fund solver.
        :type solver: bytom.solver.FundSolver

        :returns: FundSignature -- Bytom fund signature instance.

        >>> from swap.providers.bytom.signature import FundSignature
        >>> from swap.providers.bytom.solver import FundSolver
        >>> unsigned_fund_transaction_raw: str = "eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogImJtMXFrOXZqNGphZXpsY25qZGNrZHM0ZmttOGZ3djVrYXdtcTlxcnVmeCIsICJyYXciOiAiMDcwMTAwMDEwMTVmMDE1ZGY3ZGY0ZDA2YTNmZTNjOGFjNjQzOGYyNWY5Yzk3NzQ0YTEwNDU1MzU3ODU3Nzc1NTI2YzNlNmM3NTJmYjY5ZWFmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOThhM2IxNWEwMTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDIyMDEyMGZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIwMjAxNDhmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBhZGUyMDQwMTIyMDAyMGU3ZjRhOTgxNWYzYTM2YzYxNmM1NjY2Yjk3ZmI3ZmRhY2QzNzIwYzExN2QwNzhjNDI5NDk0ZDFiNjE3ZmU3ZDQwMDAxM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYjBjMmIzNTUwMTE2MDAxNGIxNTkyYWNiYjkxN2YxMzkzNzE2NmMyYTliNmNlOTczMjk2ZWJiNjAwMCIsICJoYXNoIjogImEzMDc4YWYwODEwYzY4YTdiYjZmMmY0MmNkNjdkY2U5ZGVhM2Q3NzAyOGNhMGM1MjcyMjRlNDUyNDAzOGFiYzQiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiZjQyYTJiNmUxNTU4NWI4OGRhOGIzNDIzN2M3YTZmZDgzYWYxMmVlNjk3MTgxM2Q2NmNmNzk0YTYzZWJjYzE2ZiJdLCAicHVibGljX2tleSI6ICJmZTZiM2ZkNDQ1ODI5MWIxOTYwNWQ5MjgzN2FlMTA2MGNjMDIzN2U2ODAyMmIyZWI5ZmFmMDFhMTE4MjI2MjEyIiwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogIm0vNDQvMTUzLzEvMC8xIn1dLCAic2lnbmF0dXJlcyI6IFtdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInR5cGUiOiAiYnl0b21fZnVuZF91bnNpZ25lZCJ9"
        >>> fund_signature: FundSignature = FundSignature(network="mainnet")
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="58775359b7b3588dcdc1bcf373489fa1272cacc03909f78469657b0208e66e46daedfdd0fd8f8df14e2084c7e8df4701db3062dded1c713e0aae734ac09c4afd")
        >>> fund_signature.sign(transaction_raw=unsigned_fund_transaction_raw, solver=fund_solver)
        <swap.providers.bytom.signature.FundSignature object at 0x0409DAF0>
        """

        if not is_transaction_raw(transaction_raw=transaction_raw):
            raise TransactionRawError("Invalid Bytom unsigned transaction raw.")

        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

        if not loaded_transaction_raw["type"] == "bytom_fund_unsigned":
            raise TypeError(f"Invalid Bytom fund unsigned transaction raw type, "
                            f"you can't sign {loaded_transaction_raw['type']} type by using fund signature.")

        # Check parameter instances
        if not isinstance(solver, FundSolver):
            raise TypeError(f"Solver must be Bytom FundSolver, not {type(solver).__name__} type.")

        # Set transaction, fee, type and network
        self._fee, self._type, self._network, self._transaction = (
            loaded_transaction_raw["fee"], loaded_transaction_raw["type"],
            loaded_transaction_raw["network"], loaded_transaction_raw
        )

        # Set recipient wallet
        wallet, path, indexes = solver.solve()
        # Clean derivation indexes/path
        wallet.clean_derivation()
        # Sign fund transaction
        for unsigned in self.unsigned_datas():
            signed_data = list()
            unsigned_datas = unsigned["datas"]
            if unsigned["path"]:
                wallet.from_path(unsigned["path"])
            elif path:
                wallet.from_path(path)
            elif indexes:
                wallet.from_indexes(indexes)
            for unsigned_data in unsigned_datas:
                signed_data.append(wallet.sign(unsigned_data))
            self._signatures.append(signed_data)
            wallet.clean_derivation()

        # Set transaction type
        self._type = "bytom_fund_signed"
        # Encode fund transaction raw
        self._signed_raw = b64encode(str(json.dumps(dict(
            fee=self._fee,
            address=self._transaction["address"],
            raw=self.raw(),
            hash=self.hash(),
            unsigned_datas=self.unsigned_datas(),
            signatures=self.signatures(),
            network=self._network,
            type=self._type,
        ))).encode()).decode()
        return self


class WithdrawSignature(Signature):
    """
    Bytom Withdraw signature.

    :param network: Bytom network, defaults to ``mainnet``.
    :type network: str

    :returns: WithdrawSignature -- Bytom withdraw signature instance.
    """

    def __init__(self, network: str = config["network"]):
        super().__init__(network=network)

    def sign(self, transaction_raw: str, solver: WithdrawSolver) -> "WithdrawSignature":
        """
        Sign unsigned withdraw transaction raw.

        :param transaction_raw: Bytom unsigned withdraw transaction raw.
        :type transaction_raw: str
        :param solver: Bytom withdraw solver.
        :type solver: bytom.solver.WithdrawSolver

        :returns: WithdrawSignature -- Bytom withdraw signature instance.

        >>> from swap.providers.bytom.signature import WithdrawSignature
        >>> from swap.providers.bytom.solver import WithdrawSolver
        >>> unsigned_withdraw_transaction_raw: str = "eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcTNwbHd2bXZ5NHFoam1wNXpmZnptazUwYWFncHVqdDZmNWplODVwIiwgInJhdyI6ICIwNzAxMDAwMjAxNWYwMTVkMzA1YTI4ZDhkMzRiNDBjNjU5MzY4MTBmOWU5YzFmOGJjOWM3OTNlYzJlNzJjNzBmOTIwM2ZiYmViMGE1NmRiOWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGFkZTIwNDAxMDExNjAwMTQwZTQzYTkyYTllOGFjYTc4OGViMTU1MWMzMTY0NDhjMmUzZjc4MjE1MDEwMDAxNWQwMTViMTM4ODFmMzI3ZTJiZTBkNWMwMGYzODU2MGYxYzI5NDg2Y2RhZjI1NWMwOWMwMWVlZTFhMWViYWEzNzgzZGRkOWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDAwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkyMjAxMjAzZTBhMzc3YWU0YWZhMDMxZDQ1NTE1OTlkOWJiN2Q1YjI3ZjQ3MzZkNzdmNzhjYWM0ZDQ3NmYwZmZiYTVhZTNlMDIwMTNhZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjkwNGUwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkwMDAxM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjBkZWUxMDQwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkwMCIsICJoYXNoIjogImQ1NDRhZDJkMDhmOWRkYTMzYjc4OTUzYzc0ZWVkZTljOWViNWQ4MDgzNTY5NTMxMGIyNDJkNTc5NmNmYjkxZDYiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiNTE3MjI5MGE5ODU4YTRhMDdjNjAzYzc0MWY2ZmQ4ZTg2NzE1YThhNDQ3MGViMjM3ZDBhMmQ4MzI1YzE3MDZiNyJdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiBudWxsfSwgeyJkYXRhcyI6IFsiZTQxYWI5NjQ3MDFmMjBhMjM0NzMzNDBiMTFkNWNiY2ZiYTlhMzczY2VkZjI4NGY4MDljMGM2MWNlN2Q3MTVkYSJdLCAicHVibGljX2tleSI6ICIzZTBhMzc3YWU0YWZhMDMxZDQ1NTE1OTlkOWJiN2Q1YjI3ZjQ3MzZkNzdmNzhjYWM0ZDQ3NmYwZmZiYTVhZTNlIiwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogIm0vNDQvMTUzLzEvMC8xIn1dLCAic2lnbmF0dXJlcyI6IFtdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInR5cGUiOiAiYnl0b21fY2xhaW1fdW5zaWduZWQifQ"
        >>> bytecode: str = "03285d0a20fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"
        >>> withdraw_signature: WithdrawSignature = WithdrawSignature(network="mainnet")
        >>> withdraw_solver: WithdrawSolver = WithdrawSolver(xprivate_key="58dd4094155bbebf2868189231c47e4e0edbd9f74545f843c9537259e1d7a656983aef283d0ccebecc2d33577a9f650b53ac7adff44f48ec839e3346cc22418f", secret_key="Hello Meheret!", bytecode=bytecode)
        >>> withdraw_signature.sign(transaction_raw=unsigned_withdraw_transaction_raw, solver=withdraw_solver)
        <swap.providers.bytom.signature.WithdrawSignature object at 0x0409DAF0>
        """

        if not is_transaction_raw(transaction_raw=transaction_raw):
            raise TransactionRawError("Invalid Bytom unsigned transaction raw.")

        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

        if not loaded_transaction_raw["type"] == "bytom_withdraw_unsigned":
            raise TypeError(f"Invalid Bytom withdraw unsigned transaction raw type, "
                            f"you can't sign {loaded_transaction_raw['type']} type by using withdraw signature.")

        # Check parameter instances
        if not isinstance(solver, WithdrawSolver):
            raise TypeError(f"Solver must be Bytom WithdrawSolver, not {type(solver).__name__} type.")

        # Set transaction, fee, type and network
        self._fee, self._type, self._network, self._transaction = (
            loaded_transaction_raw["fee"], loaded_transaction_raw["type"],
            loaded_transaction_raw["network"], loaded_transaction_raw
        )

        # Set recipient wallet
        wallet, secret, path, indexes = solver.solve()
        # Clean derivation indexes/path
        wallet.clean_derivation()
        # Sign withdraw transaction
        for index, unsigned in enumerate(self.unsigned_datas()):
            signed_data = list()
            unsigned_datas = unsigned["datas"]
            if unsigned["path"]:
                wallet.from_path(unsigned["path"])
            elif path:
                wallet.from_path(path)
            elif indexes:
                wallet.from_indexes(indexes)
            for unsigned_data in unsigned_datas:
                signed_data.append(bytearray(secret.encode()).hex())
                signed_data.append(wallet.sign(unsigned_data))
                signed_data.append(str("00"))
                signed_data.append(solver.witness(self._network))
            self._signatures.append(signed_data)
            wallet.clean_derivation()

        # Set transaction type
        self._type = "bytom_withdraw_signed"
        # Encode withdraw transaction raw
        self._signed_raw = b64encode(str(json.dumps(dict(
            fee=self._fee,
            address=self._transaction["address"],
            raw=self.raw(),
            hash=self.hash(),
            unsigned_datas=self.unsigned_datas(),
            signatures=self.signatures(),
            network=self._network,
            type=self._type
        ))).encode()).decode()
        return self


class RefundSignature(Signature):
    """
    Bytom Refund signature.

    :param network: Bytom network, defaults to ``mainnet``.
    :type network: str

    :returns: RefundSignature -- Bytom withdraw signature instance.
    """

    def __init__(self, network: str = config["network"]):
        super().__init__(network=network)

    def sign(self, transaction_raw: str, solver: RefundSolver) -> "RefundSignature":
        """
        Sign unsigned refund transaction raw.

        :param transaction_raw: Bytom unsigned refund transaction raw.
        :type transaction_raw: str
        :param solver: Bytom refund solver.
        :type solver: bytom.solver.RefundSolver
        
        :returns: RefundSignature -- Bytom refund signature instance.

        >>> from swap.providers.bytom.signature import RefundSignature
        >>> from swap.providers.bytom.solver import RefundSolver
        >>> unsigned_refund_transaction_raw: str = "eyJmZWUiOiA1MDkwMDAsICJhZGRyZXNzIjogImJtMXF1bDYybnEybDhnbXZ2OWs5dmU0ZTA3bWxtdHhud2d4cHpsZzgzM3BmZjl4M2tjdGx1bDJxNzI3anl5IiwgImhhc2giOiAiMTcyMmFhOTMwZjZmOTNiNGM4Nzc4OGVhNTVmNDkwNTVmMjZmODY4MjFiY2QxMWE2NGQ0MmJjYjllM2I4YTk2ZCIsICJyYXciOiAiMDcwMTAwMDEwMTZiMDE2OWY3ZGY0ZDA2YTNmZTNjOGFjNjQzOGYyNWY5Yzk3NzQ0YTEwNDU1MzU3ODU3Nzc1NTI2YzNlNmM3NTJmYjY5ZWFmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBhZGUyMDQwMDAxMjIwMDIwZTdmNGE5ODE1ZjNhMzZjNjE2YzU2NjZiOTdmYjdmZGFjZDM3MjBjMTE3ZDA3OGM0Mjk0OTRkMWI2MTdmZTdkNDAxMDAwMTAxM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYjhhNGMzMDQwMTE2MDAxNGIxNTkyYWNiYjkxN2YxMzkzNzE2NmMyYTliNmNlOTczMjk2ZWJiNjAwMCIsICJ1bnNpZ25lZF9kYXRhcyI6IFt7ImRhdGFzIjogWyJjYzc4YzFmYjY0OGY4ODI2ZTRkZDRmODVmODg1YWM3NTg2NmMwMjMzYjBhZjY1ODE3NTNkODU4MzA0YjhlMDRiIl0sICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6IG51bGx9XSwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX3JlZnVuZF91bnNpZ25lZCJ9"
        >>> bytecode: str = "03285d0a20fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"
        >>> refund_signature: RefundSignature = RefundSignature(network="mainnet")
        >>> refund_solver: RefundSolver = RefundSolver(xprivate_key="58775359b7b3588dcdc1bcf373489fa1272cacc03909f78469657b0208e66e46daedfdd0fd8f8df14e2084c7e8df4701db3062dded1c713e0aae734ac09c4afd", bytecode=bytecode)
        >>> refund_signature.sign(transaction_raw=unsigned_refund_transaction_raw, solver=refund_solver)
        <swap.providers.bytom.signature.RefundSignature object at 0x0409DAF0>
        """

        if not is_transaction_raw(transaction_raw=transaction_raw):
            raise TransactionRawError("Invalid Bytom unsigned transaction raw.")

        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

        if not loaded_transaction_raw["type"] == "bytom_refund_unsigned":
            raise TypeError(f"Invalid Bytom refund unsigned transaction raw type, "
                            f"you can't sign {loaded_transaction_raw['type']} type by using refund signature.")

        # Check parameter instances
        if not isinstance(solver, RefundSolver):
            raise TypeError(f"Solver must be Bytom RefundSolver, not {type(solver).__name__} type.")

        # Set transaction, fee, type and network
        self._fee, self._type, self._network, self._transaction = (
            loaded_transaction_raw["fee"], loaded_transaction_raw["type"],
            loaded_transaction_raw["network"], loaded_transaction_raw
        )

        # Set recipient wallet
        wallet, path, indexes = solver.solve()
        # Clean derivation indexes/path
        wallet.clean_derivation()
        # Sign refund transaction
        for index, unsigned in enumerate(self.unsigned_datas()):
            signed_data = list()
            unsigned_datas = unsigned["datas"]
            if unsigned["path"]:
                wallet.from_path(unsigned["path"])
            elif path:
                wallet.from_path(path)
            elif indexes:
                wallet.from_indexes(indexes)
            for unsigned_data in unsigned_datas:
                signed_data.append(wallet.sign(unsigned_data))
                signed_data.append(str("01"))
                signed_data.append(solver.witness(self._network))
            self._signatures.append(signed_data)
            wallet.clean_derivation()

        # Encode refund transaction raw
        self._type = "bytom_refund_signed"
        self._signed_raw = b64encode(str(json.dumps(dict(
            fee=self._fee,
            address=self._transaction["address"],
            raw=self.raw(),
            hash=self.hash(),
            unsigned_datas=self.unsigned_datas(),
            signatures=self.signatures(),
            network=self._network,
            type=self._type
        ))).encode()).decode()
        return self
