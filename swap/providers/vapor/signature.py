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
from ..config import vapor as config
from .transaction import Transaction
from .solver import (
    NormalSolver, FundSolver, WithdrawSolver, RefundSolver
)
from .rpc import decode_raw
from .utils import (
    is_network, is_transaction_raw, amount_unit_converter
)


class Signature(Transaction):
    """
    Vapor Signature.

    :param network: Vapor network, defaults to ``mainnet``.
    :type network: str

    :returns: Signature -- Vapor signature instance.

    .. note::
        Vapor has only three networks, ``mainnet``, ``solonet`` and ``testnet``.
    """

    def __init__(self, network: str = config["network"]):

        if not is_network(network=network):
            raise NetworkError(f"Invalid Vapor '{network}' network",
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
        Get Vapor transaction fee.

        :param unit: Vapor unit, default to ``NEU``.
        :type unit: str

        :returns: int, float -- Vapor transaction fee.

        >>> from swap.providers.vapor.signature import Signature
        >>> from swap.providers.vapor.solver import FundSolver
        >>> unsigned_fund_transaction_raw: str = "eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogInZwMXFrOXZqNGphZXpsY25qZGNrZHM0ZmttOGZ3djVrYXdtcXdwbnB2cyIsICJyYXciOiAiMDcwMTAwMDEwMTVmMDE1ZGRmODJjZjdjNzkyNzc4NmE2OTU2OTM3NzQ0ZWU4MjM1NGM0ODFiMGYyMTFhYzUyYTVjMWQ3NDRjNGUzZTc4NjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYzhmOWEyMmEwMTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDIyMDEyMGZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIwMjAxNGEwMDQ4ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjgwYWRlMjA0MDEyMjAwMjAzNGEzZGI1MDMwMWI5NDFiOGVkNDNkY2ZkYmQzMzgxZGYxYjczOWZhNjRhYjc3ZTQyNjRmNzAzYTQ1ZTBiZTMxMDAwMTNlMDAzY2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZlMDk4YTUyNTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDAwIiwgImhhc2giOiAiYTA5ZjMwOTNhYWZmNmM4YzhmMWEzNzJlYWM2ODU3MWNlZWE0OTI4Y2NjOGI5YjU0OTU0ODYzNzU4NDQ3ZGVjMSIsICJ1bnNpZ25lZF9kYXRhcyI6IFt7ImRhdGFzIjogWyJkNzEwNzI1N2VmNWZiZmIwNGZjNDc0N2Q2ODg3ZjIzMGEzMDY3NmVjZDY3MDNhNTgwMTU4NzhiNTRmMWY3YjRmIl0sICJwdWJsaWNfa2V5IjogImZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJ2YXBvcl9mdW5kX3Vuc2lnbmVkIn0"
        >>> signature: Signature = Signature(network="mainnet")
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="58775359b7b3588dcdc1bcf373489fa1272cacc03909f78469657b0208e66e46daedfdd0fd8f8df14e2084c7e8df4701db3062dded1c713e0aae734ac09c4afd")
        >>> signature.sign(transaction_raw=unsigned_fund_transaction_raw, solver=fund_solver)
        >>> signature.fee(unit="NEU")
        449000
        """

        if self._transaction is None:
            raise ValueError("Transaction is none, sign unsigned transaction raw first.")
        if unit not in ["BTM", "mBTM", "NEU"]:
            raise UnitError("Invalid Vapor unit, choose only BTM, mBTM or NEU units.")
        return self._fee if unit == "NEU" else \
            amount_unit_converter(amount=self._fee, unit_from=f"NEU2{unit}")

    def hash(self) -> str:
        """
        Get Vapor signature transaction hash.

        :returns: str -- Vapor signature transaction hash or transaction id.

        >>> from swap.providers.vapor.signature import Signature
        >>> from swap.providers.vapor.solver import WithdrawSolver
        >>> unsigned_withdraw_transaction_raw: str = "eyJmZWUiOiA1MDkwMDAsICJhZGRyZXNzIjogImJtMXF1bDYybnEybDhnbXZ2OWs5dmU0ZTA3bWxtdHhud2d4cHpsZzgzM3BmZjl4M2tjdGx1bDJxNzI3anl5IiwgInJhdyI6ICIwNzAxMDAwMTAxNmIwMTY5ZjdkZjRkMDZhM2ZlM2M4YWM2NDM4ZjI1ZjljOTc3NDRhMTA0NTUzNTc4NTc3NzU1MjZjM2U2Yzc1MmZiNjllYWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGFkZTIwNDAwMDEyMjAwMjBlN2Y0YTk4MTVmM2EzNmM2MTZjNTY2NmI5N2ZiN2ZkYWNkMzcyMGMxMTdkMDc4YzQyOTQ5NGQxYjYxN2ZlN2Q0MDEwMDAxMDEzY2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZiOGE0YzMwNDAxMTYwMDE0ODg3ZWU2NmQ4NGE4MmYyZDg2ODI0YTQ1YmI1MWZkZWEwM2M5MmY0OTAwIiwgImhhc2giOiAiZDFlODRjMzdmNDEwNTZmNGRmMzk4NTIzZjg0ZWNmMDc5Mzc3ZmQ4NWU0NTYxYzEwZWMwMzgxOGNkNGRiN2VjMCIsICJ1bnNpZ25lZF9kYXRhcyI6IFt7ImRhdGFzIjogWyI0NWQxNzQ2YTFlYzA2OTVkM2UwNjA1OWM0MTM4NzIwNDBkMjRmODY0OTlkZGFmYWI0ODE3NzM2OGU1YzcyODgzIl0sICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6IG51bGx9XSwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX3dpdGhkcmF3X3Vuc2lnbmVkIn0"
        >>> bytecode: str = "042918320720fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"
        >>> signature: Signature = Signature(network="mainnet")
        >>> withdraw_solver: WithdrawSolver = WithdrawSolver(xprivate_key="58dd4094155bbebf2868189231c47e4e0edbd9f74545f843c9537259e1d7a656983aef283d0ccebecc2d33577a9f650b53ac7adff44f48ec839e3346cc22418f", secret_key="Hello Meheret!", bytecode=bytecode)
        >>> signature.sign(transaction_raw=unsigned_withdraw_transaction_raw, solver=withdraw_solver)
        >>> signature.hash()
        "904aeda199f05cbb7671e0d9ec95b3091f3c131cef8d634ae17216b9c2fea48c"
        """

        if self._transaction is None:
            raise ValueError("Transaction is none, sign unsigned transaction raw first.")
        return self._transaction["hash"]

    def json(self) -> dict:
        """
        Get Vapor signature transaction json format.

        :returns: dict -- Vapor signature transaction json format.

        >>> from swap.providers.vapor.signature import Signature
        >>> from swap.providers.vapor.solver import FundSolver
        >>> unsigned_fund_transaction_raw: str = "eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogInZwMXFrOXZqNGphZXpsY25qZGNrZHM0ZmttOGZ3djVrYXdtcXdwbnB2cyIsICJyYXciOiAiMDcwMTAwMDEwMTVmMDE1ZGRmODJjZjdjNzkyNzc4NmE2OTU2OTM3NzQ0ZWU4MjM1NGM0ODFiMGYyMTFhYzUyYTVjMWQ3NDRjNGUzZTc4NjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYzhmOWEyMmEwMTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDIyMDEyMGZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIwMjAxNGEwMDQ4ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjgwYWRlMjA0MDEyMjAwMjAzNGEzZGI1MDMwMWI5NDFiOGVkNDNkY2ZkYmQzMzgxZGYxYjczOWZhNjRhYjc3ZTQyNjRmNzAzYTQ1ZTBiZTMxMDAwMTNlMDAzY2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZlMDk4YTUyNTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDAwIiwgImhhc2giOiAiYTA5ZjMwOTNhYWZmNmM4YzhmMWEzNzJlYWM2ODU3MWNlZWE0OTI4Y2NjOGI5YjU0OTU0ODYzNzU4NDQ3ZGVjMSIsICJ1bnNpZ25lZF9kYXRhcyI6IFt7ImRhdGFzIjogWyJkNzEwNzI1N2VmNWZiZmIwNGZjNDc0N2Q2ODg3ZjIzMGEzMDY3NmVjZDY3MDNhNTgwMTU4NzhiNTRmMWY3YjRmIl0sICJwdWJsaWNfa2V5IjogImZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJ2YXBvcl9mdW5kX3Vuc2lnbmVkIn0"
        >>> signature: Signature = Signature(network="mainnet")
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="58775359b7b3588dcdc1bcf373489fa1272cacc03909f78469657b0208e66e46daedfdd0fd8f8df14e2084c7e8df4701db3062dded1c713e0aae734ac09c4afd")
        >>> signature.sign(transaction_raw=unsigned_fund_transaction_raw, solver=fund_solver)
        >>> signature.json()
        {'tx_id': 'a09f3093aaff6c8c8f1a372eac68571ceea4928ccc8b9b54954863758447dec1', 'version': 1, 'size': 279, 'time_range': 0, 'inputs': [{'type': 'spend', 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'asset_definition': {}, 'amount': 88653000, 'control_program': '0014b1592acbb917f13937166c2a9b6ce973296ebb60', 'address': 'vp1qk9vj4jaezlcnjdckds4fkm8fwv5kawmqwpnpvs', 'spent_output_id': 'baa1fa7702447b83ceea10d075534638b4acd93074bb420d3a5399e35c35c8e9', 'input_id': '294506b8df5389141854f6826b625cd7eac43f30fccf6118ae163e34b6b7fc1b', 'witness_arguments': ['fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212']}], 'outputs': [{'type': 'control', 'id': '3e7369a5063743ca88961fe5745860c42e3b949c6baa99df08696063e8066996', 'position': 0, 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'asset_definition': {}, 'amount': 10000000, 'control_program': '002034a3db50301b941b8ed43dcfdbd3381df1b739fa64ab77e4264f703a45e0be31', 'address': 'vp1qxj3ak5psrw2phrk58h8ah5ecrhcmww06vj4h0epxfacr530qhccs4pczgc'}, {'type': 'control', 'id': '0a96063f04da56945b3ffa57a195527e25e40d53b42c3c7a4251896e82946aa3', 'position': 1, 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'asset_definition': {}, 'amount': 78204000, 'control_program': '0014b1592acbb917f13937166c2a9b6ce973296ebb60', 'address': 'vp1qk9vj4jaezlcnjdckds4fkm8fwv5kawmqwpnpvs'}], 'fee': 449000}
        """
        if self._transaction is None:
            raise ValueError("Transaction is none, sign unsigned transaction raw first.")
        return decode_raw(raw=self._transaction["raw"])

    def raw(self) -> str:
        """
        Get Vapor signature transaction raw.

        :returns: str -- Vapor signature transaction raw.

        >>> from swap.providers.vapor.signature import Signature
        >>> from swap.providers.vapor.solver import FundSolver
        >>> unsigned_fund_transaction_raw: str = "eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogInZwMXFrOXZqNGphZXpsY25qZGNrZHM0ZmttOGZ3djVrYXdtcXdwbnB2cyIsICJyYXciOiAiMDcwMTAwMDEwMTVmMDE1ZGRmODJjZjdjNzkyNzc4NmE2OTU2OTM3NzQ0ZWU4MjM1NGM0ODFiMGYyMTFhYzUyYTVjMWQ3NDRjNGUzZTc4NjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYzhmOWEyMmEwMTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDIyMDEyMGZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIwMjAxNGEwMDQ4ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjgwYWRlMjA0MDEyMjAwMjAzNGEzZGI1MDMwMWI5NDFiOGVkNDNkY2ZkYmQzMzgxZGYxYjczOWZhNjRhYjc3ZTQyNjRmNzAzYTQ1ZTBiZTMxMDAwMTNlMDAzY2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZlMDk4YTUyNTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDAwIiwgImhhc2giOiAiYTA5ZjMwOTNhYWZmNmM4YzhmMWEzNzJlYWM2ODU3MWNlZWE0OTI4Y2NjOGI5YjU0OTU0ODYzNzU4NDQ3ZGVjMSIsICJ1bnNpZ25lZF9kYXRhcyI6IFt7ImRhdGFzIjogWyJkNzEwNzI1N2VmNWZiZmIwNGZjNDc0N2Q2ODg3ZjIzMGEzMDY3NmVjZDY3MDNhNTgwMTU4NzhiNTRmMWY3YjRmIl0sICJwdWJsaWNfa2V5IjogImZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJ2YXBvcl9mdW5kX3Vuc2lnbmVkIn0"
        >>> signature: Signature = Signature(network="mainnet")
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="58775359b7b3588dcdc1bcf373489fa1272cacc03909f78469657b0208e66e46daedfdd0fd8f8df14e2084c7e8df4701db3062dded1c713e0aae734ac09c4afd")
        >>> signature.sign(transaction_raw=unsigned_fund_transaction_raw, solver=fund_solver)
        >>> signature.raw()
        "07010001015f015ddf82cf7c7927786a6956937744ee82354c481b0f211ac52a5c1d744c4e3e7866ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffc8f9a22a0101160014b1592acbb917f13937166c2a9b6ce973296ebb60220120fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a11822621202014a0048ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff80ade2040122002034a3db50301b941b8ed43dcfdbd3381df1b739fa64ab77e4264f703a45e0be3100013e003cffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe098a52501160014b1592acbb917f13937166c2a9b6ce973296ebb6000"
        """

        if self._transaction is None:
            raise ValueError("Transaction is none, sign unsigned transaction raw first.")
        return self._transaction["raw"]

    def type(self) -> str:
        """
        Get Vapor signature transaction type.

        :returns: str -- Vapor signature transaction type.

        >>> from swap.providers.vapor.signature import Signature
        >>> from swap.providers.vapor.solver import RefundSolver
        >>> unsigned_refund_transaction_raw: str = "eyJmZWUiOiA1MDkwMDAsICJhZGRyZXNzIjogInZwMXF4ajNhazVwc3J3MnBocms1OGg4YWg1ZWNyaGNtd3cwNnZqNGgwZXB4ZmFjcjUzMHFoY2NzNHBjemdjIiwgImhhc2giOiAiNmQ5NjQyMjIyYmFmYjlkNjk2OGVlMmVlZDk4OGM4MzdiMWRhNTZmY2VjNmZkOTYzMjlmZmY4YzBkNTUxOGY5MiIsICJyYXciOiAiMDcwMTAwMDEwMTZiMDE2OWRmODJjZjdjNzkyNzc4NmE2OTU2OTM3NzQ0ZWU4MjM1NGM0ODFiMGYyMTFhYzUyYTVjMWQ3NDRjNGUzZTc4NjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBhZGUyMDQwMDAxMjIwMDIwMzRhM2RiNTAzMDFiOTQxYjhlZDQzZGNmZGJkMzM4MWRmMWI3MzlmYTY0YWI3N2U0MjY0ZjcwM2E0NWUwYmUzMTAxMDAwMTAxM2UwMDNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmI4YTRjMzA0MDExNjAwMTRiMTU5MmFjYmI5MTdmMTM5MzcxNjZjMmE5YjZjZTk3MzI5NmViYjYwMDAiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiNmIyNGM0NDM4OTY2MWY4YzU3MDE0NmVjNGNjOGQzYWQzZjJkN2YxNjA3MTM2MjBiZTc0MzgwZTQwYmMwNmMwYyJdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiBudWxsfV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJ2YXBvcl9yZWZ1bmRfdW5zaWduZWQifQ"
        >>> bytecode: str = "042918320720fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"
        >>> signature: Signature = Signature(network="mainnet")
        >>> refund_solver: RefundSolver = RefundSolver(xprivate_key="58775359b7b3588dcdc1bcf373489fa1272cacc03909f78469657b0208e66e46daedfdd0fd8f8df14e2084c7e8df4701db3062dded1c713e0aae734ac09c4afd", bytecode=bytecode)
        >>> signature.sign(transaction_raw=unsigned_refund_transaction_raw, solver=refund_solver)
        >>> signature.type()
        "vapor_refund_signed"
        """

        if self._type is None:
            raise ValueError("Type is none, sign unsigned transaction raw first.")
        return self._type

    def sign(self, transaction_raw: str, solver: Union[NormalSolver, FundSolver, WithdrawSolver, RefundSolver]) \
            -> Union["NormalSignature", "FundSignature", "WithdrawSignature", "RefundSignature"]:
        """
        Sign unsigned transaction raw.

        :param transaction_raw: Vapor unsigned transaction raw.
        :type transaction_raw: str
        :param solver: Vapor solver
        :type solver: vapor.solver.NormalSolver, vapor.solver.FundSolver, vapor.solver.WithdrawSolver, vapor.solver.RefundSolver

        :returns: NormalSignature, FundSignature, WithdrawSignature, RefundSignature -- Vapor signature instance.

        >>> from swap.providers.vapor.signature import Signature
        >>> from swap.providers.vapor.solver import FundSolver
        >>> unsigned_fund_transaction_raw: str = "eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogInZwMXFrOXZqNGphZXpsY25qZGNrZHM0ZmttOGZ3djVrYXdtcXdwbnB2cyIsICJyYXciOiAiMDcwMTAwMDEwMTVmMDE1ZGRmODJjZjdjNzkyNzc4NmE2OTU2OTM3NzQ0ZWU4MjM1NGM0ODFiMGYyMTFhYzUyYTVjMWQ3NDRjNGUzZTc4NjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYzhmOWEyMmEwMTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDIyMDEyMGZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIwMjAxNGEwMDQ4ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjgwYWRlMjA0MDEyMjAwMjAzNGEzZGI1MDMwMWI5NDFiOGVkNDNkY2ZkYmQzMzgxZGYxYjczOWZhNjRhYjc3ZTQyNjRmNzAzYTQ1ZTBiZTMxMDAwMTNlMDAzY2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZlMDk4YTUyNTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDAwIiwgImhhc2giOiAiYTA5ZjMwOTNhYWZmNmM4YzhmMWEzNzJlYWM2ODU3MWNlZWE0OTI4Y2NjOGI5YjU0OTU0ODYzNzU4NDQ3ZGVjMSIsICJ1bnNpZ25lZF9kYXRhcyI6IFt7ImRhdGFzIjogWyJkNzEwNzI1N2VmNWZiZmIwNGZjNDc0N2Q2ODg3ZjIzMGEzMDY3NmVjZDY3MDNhNTgwMTU4NzhiNTRmMWY3YjRmIl0sICJwdWJsaWNfa2V5IjogImZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJ2YXBvcl9mdW5kX3Vuc2lnbmVkIn0"
        >>> signature: Signature = Signature(network="mainnet")
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="58775359b7b3588dcdc1bcf373489fa1272cacc03909f78469657b0208e66e46daedfdd0fd8f8df14e2084c7e8df4701db3062dded1c713e0aae734ac09c4afd")
        >>> signature.sign(transaction_raw=unsigned_fund_transaction_raw, solver=fund_solver)
        <swap.providers.vapor.signature.FundSignature object at 0x0409DAF0>
        """

        if not is_transaction_raw(transaction_raw=transaction_raw):
            raise TransactionRawError("Invalid Vapor unsigned transaction raw.")

        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

        self._type = loaded_transaction_raw["type"]
        if loaded_transaction_raw["type"] == "vapor_normal_unsigned":
            return NormalSignature(network=self._network).sign(
                transaction_raw=transaction_raw, solver=solver
            )
        elif loaded_transaction_raw["type"] == "vapor_fund_unsigned":
            return FundSignature(network=self._network).sign(
                transaction_raw=transaction_raw, solver=solver
            )
        elif loaded_transaction_raw["type"] == "vapor_withdraw_unsigned":
            return WithdrawSignature(network=self._network).sign(
                transaction_raw=transaction_raw, solver=solver
            )
        elif loaded_transaction_raw["type"] == "vapor_refund_unsigned":
            return RefundSignature(network=self._network).sign(
                transaction_raw=transaction_raw, solver=solver
            )

    def unsigned_datas(self) -> List[dict]:
        """
        Get Vapor transaction unsigned datas with instruction.

        :returns: list -- Vapor transaction unsigned datas.

        >>> from swap.providers.vapor.signature import Signature
        >>> from swap.providers.vapor.solver import WithdrawSolver
        >>> unsigned_withdraw_transaction_raw: str = "eyJmZWUiOiA1MDkwMDAsICJhZGRyZXNzIjogInZwMXF4ajNhazVwc3J3MnBocms1OGg4YWg1ZWNyaGNtd3cwNnZqNGgwZXB4ZmFjcjUzMHFoY2NzNHBjemdjIiwgInJhdyI6ICIwNzAxMDAwMTAxNmIwMTY5ZGY4MmNmN2M3OTI3Nzg2YTY5NTY5Mzc3NDRlZTgyMzU0YzQ4MWIwZjIxMWFjNTJhNWMxZDc0NGM0ZTNlNzg2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGFkZTIwNDAwMDEyMjAwMjAzNGEzZGI1MDMwMWI5NDFiOGVkNDNkY2ZkYmQzMzgxZGYxYjczOWZhNjRhYjc3ZTQyNjRmNzAzYTQ1ZTBiZTMxMDEwMDAxMDEzZTAwM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYjhhNGMzMDQwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkwMCIsICJoYXNoIjogIjkwNGFlZGExOTlmMDVjYmI3NjcxZTBkOWVjOTViMzA5MWYzYzEzMWNlZjhkNjM0YWUxNzIxNmI5YzJmZWE0OGMiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiM2ExMjNmZDgwOWQzYWQ4NDVhOTJhZDNlNWExZjBjYzEwM2RlNTExYWRmOTVjZjMwMjQwZDkxNjRkNmZmMTk2NCJdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiBudWxsfV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJ2YXBvcl93aXRoZHJhd191bnNpZ25lZCJ9"
        >>> bytecode: str = "042918320720fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"
        >>> signature: Signature = Signature(network="mainnet")
        >>> withdraw_solver: WithdrawSolver = WithdrawSolver(xprivate_key="58dd4094155bbebf2868189231c47e4e0edbd9f74545f843c9537259e1d7a656983aef283d0ccebecc2d33577a9f650b53ac7adff44f48ec839e3346cc22418f", secret_key="Hello Meheret!", bytecode=bytecode)
        >>> signature.sign(transaction_raw=unsigned_withdraw_transaction_raw, solver=withdraw_solver)
        >>> signature.unsigned_datas()
        [{'datas': ['3a123fd809d3ad845a92ad3e5a1f0cc103de511adf95cf30240d9164d6ff1964'], 'network': 'mainnet', 'path': None}]
        """

        if self._transaction is None:
            raise ValueError("Transaction is none, sign unsigned transaction raw first.")
        return self._transaction["unsigned_datas"]

    def signatures(self) -> List[List[str]]:
        """
        Get Vapor transaction signatures(signed datas).

        :returns: list -- Vapor transaction signatures.

        >>> from swap.providers.vapor.signature import Signature
        >>> from swap.providers.vapor.solver import FundSolver
        >>> unsigned_fund_transaction_raw: str = "eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogInZwMXFrOXZqNGphZXpsY25qZGNrZHM0ZmttOGZ3djVrYXdtcXdwbnB2cyIsICJyYXciOiAiMDcwMTAwMDEwMTVmMDE1ZGRmODJjZjdjNzkyNzc4NmE2OTU2OTM3NzQ0ZWU4MjM1NGM0ODFiMGYyMTFhYzUyYTVjMWQ3NDRjNGUzZTc4NjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYzhmOWEyMmEwMTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDIyMDEyMGZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIwMjAxNGEwMDQ4ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjgwYWRlMjA0MDEyMjAwMjAzNGEzZGI1MDMwMWI5NDFiOGVkNDNkY2ZkYmQzMzgxZGYxYjczOWZhNjRhYjc3ZTQyNjRmNzAzYTQ1ZTBiZTMxMDAwMTNlMDAzY2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZlMDk4YTUyNTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDAwIiwgImhhc2giOiAiYTA5ZjMwOTNhYWZmNmM4YzhmMWEzNzJlYWM2ODU3MWNlZWE0OTI4Y2NjOGI5YjU0OTU0ODYzNzU4NDQ3ZGVjMSIsICJ1bnNpZ25lZF9kYXRhcyI6IFt7ImRhdGFzIjogWyJkNzEwNzI1N2VmNWZiZmIwNGZjNDc0N2Q2ODg3ZjIzMGEzMDY3NmVjZDY3MDNhNTgwMTU4NzhiNTRmMWY3YjRmIl0sICJwdWJsaWNfa2V5IjogImZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJ2YXBvcl9mdW5kX3Vuc2lnbmVkIn0"
        >>> signature: Signature = Signature(network="mainnet")
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="58775359b7b3588dcdc1bcf373489fa1272cacc03909f78469657b0208e66e46daedfdd0fd8f8df14e2084c7e8df4701db3062dded1c713e0aae734ac09c4afd")
        >>> signature.sign(transaction_raw=unsigned_fund_transaction_raw, solver=fund_solver)
        >>> signature.signatures()
        [['0d2e4e42fcee863e74195dceab1dfccf368055b171196faa90c53eaa2cea649bb43cc132354edad970b356aae5d628dd0160e787ac174af89ca534d14db71e00']]
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")
        return self._signatures

    def transaction_raw(self) -> str:
        """
        Get Vapor signed transaction raw.

        :returns: str -- Vapor signed transaction raw.

        >>> from swap.providers.vapor.signature import Signature
        >>> from swap.providers.vapor.solver import FundSolver
        >>> unsigned_fund_transaction_raw: str = "eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogInZwMXFrOXZqNGphZXpsY25qZGNrZHM0ZmttOGZ3djVrYXdtcXdwbnB2cyIsICJyYXciOiAiMDcwMTAwMDEwMTVmMDE1ZGRmODJjZjdjNzkyNzc4NmE2OTU2OTM3NzQ0ZWU4MjM1NGM0ODFiMGYyMTFhYzUyYTVjMWQ3NDRjNGUzZTc4NjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYzhmOWEyMmEwMTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDIyMDEyMGZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIwMjAxNGEwMDQ4ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjgwYWRlMjA0MDEyMjAwMjAzNGEzZGI1MDMwMWI5NDFiOGVkNDNkY2ZkYmQzMzgxZGYxYjczOWZhNjRhYjc3ZTQyNjRmNzAzYTQ1ZTBiZTMxMDAwMTNlMDAzY2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZlMDk4YTUyNTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDAwIiwgImhhc2giOiAiYTA5ZjMwOTNhYWZmNmM4YzhmMWEzNzJlYWM2ODU3MWNlZWE0OTI4Y2NjOGI5YjU0OTU0ODYzNzU4NDQ3ZGVjMSIsICJ1bnNpZ25lZF9kYXRhcyI6IFt7ImRhdGFzIjogWyJkNzEwNzI1N2VmNWZiZmIwNGZjNDc0N2Q2ODg3ZjIzMGEzMDY3NmVjZDY3MDNhNTgwMTU4NzhiNTRmMWY3YjRmIl0sICJwdWJsaWNfa2V5IjogImZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJ2YXBvcl9mdW5kX3Vuc2lnbmVkIn0"
        >>> signature: Signature = Signature(network="mainnet")
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="58775359b7b3588dcdc1bcf373489fa1272cacc03909f78469657b0208e66e46daedfdd0fd8f8df14e2084c7e8df4701db3062dded1c713e0aae734ac09c4afd")
        >>> signature.sign(transaction_raw=unsigned_fund_transaction_raw, solver=fund_solver)
        >>> signature.transaction_raw()
        "eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogInZwMXFrOXZqNGphZXpsY25qZGNrZHM0ZmttOGZ3djVrYXdtcXdwbnB2cyIsICJyYXciOiAiMDcwMTAwMDEwMTVmMDE1ZGRmODJjZjdjNzkyNzc4NmE2OTU2OTM3NzQ0ZWU4MjM1NGM0ODFiMGYyMTFhYzUyYTVjMWQ3NDRjNGUzZTc4NjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYzhmOWEyMmEwMTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDIyMDEyMGZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIwMjAxNGEwMDQ4ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjgwYWRlMjA0MDEyMjAwMjAzNGEzZGI1MDMwMWI5NDFiOGVkNDNkY2ZkYmQzMzgxZGYxYjczOWZhNjRhYjc3ZTQyNjRmNzAzYTQ1ZTBiZTMxMDAwMTNlMDAzY2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZlMDk4YTUyNTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDAwIiwgImhhc2giOiAiYTA5ZjMwOTNhYWZmNmM4YzhmMWEzNzJlYWM2ODU3MWNlZWE0OTI4Y2NjOGI5YjU0OTU0ODYzNzU4NDQ3ZGVjMSIsICJ1bnNpZ25lZF9kYXRhcyI6IFt7ImRhdGFzIjogWyJkNzEwNzI1N2VmNWZiZmIwNGZjNDc0N2Q2ODg3ZjIzMGEzMDY3NmVjZDY3MDNhNTgwMTU4NzhiNTRmMWY3YjRmIl0sICJwdWJsaWNfa2V5IjogImZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJzaWduYXR1cmVzIjogW1siMGQyZTRlNDJmY2VlODYzZTc0MTk1ZGNlYWIxZGZjY2YzNjgwNTViMTcxMTk2ZmFhOTBjNTNlYWEyY2VhNjQ5YmI0M2NjMTMyMzU0ZWRhZDk3MGIzNTZhYWU1ZDYyOGRkMDE2MGU3ODdhYzE3NGFmODljYTUzNGQxNGRiNzFlMDAiXV0sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJ2YXBvcl9mdW5kX3NpZ25lZCJ9"
        """

        if self._signed_raw is None:
            raise ValueError("Transaction is none, sign unsigned transaction raw first.")
        return clean_transaction_raw(self._signed_raw)


class NormalSignature(Signature):
    """
    Vapor Normal signature.

    :param network: Vapor network, defaults to ``mainnet``.
    :type network: str

    :returns: NormalSignature -- Vapor normal signature instance.
    """

    def __init__(self, network: str = config["network"]):
        super().__init__(network=network)

    def sign(self, transaction_raw: str, solver: NormalSolver) -> "NormalSignature":
        """
        Sign unsigned normal transaction raw.

        :param transaction_raw: Vapor unsigned normal transaction raw.
        :type transaction_raw: str
        :param solver: Vapor normal solver.
        :type solver: vapor.solver.NormalSolver

        :returns: NormalSignature -- Vapor normal signature instance.

        >>> from swap.providers.vapor.signature import NormalSignature
        >>> from swap.providers.vapor.solver import NormalSolver
        >>> unsigned_normal_transaction_raw: str = "eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcTluZHlseDAyc3lmd2Q3bnBlaGZ4ejRsZGRoenFzdmUyZnU2dmM3IiwgInJhdyI6ICIwNzAxMDAwMjAxNWYwMTVkODJlNjVmOTY0ZDNjMzUzMjU0OGRmZGU5Mzg0NjJmNTY2Yzk1ZDNjOTBlNmEzYTE4MmEwYjNiZGFlNDZhYTc5MGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MDg2ZjIwMzAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAxNWYwMTVkMDcwZDBlYjIyZDMyYjgyZDNkMmYzZmM0YmFmYjdhODVmNTIyOWY3ZmQ4OTA0MmQyZmYzMjU3Mzc1ZTQzZDNlYmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOGY1Zjc0ZjAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDE0NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDAwMTNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmQ4YjhmODUyMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAiaGFzaCI6ICI1MGIzMzZhYjZlMDU1ZDlkNGQ2NWE5ZjIyOTViNTMyNzBhYmQzODE2YzIzYmE0Yzk1NDg0MWYzOTlhYTc3MmQ1IiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbImY3ZDNhYTE4YjI5NWNkYTZmMmIxMTMyYzQyMzE5MzNjYzkyZjNiYWNhNzA1OTc0YzVkZTM3OGY5YjY5NWYwZTIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9LCB7ImRhdGFzIjogWyJjYTYxNWJhMmM3MjllNDYzZmJmNzlhMTE0MTkxNzYyNjFiMWJmNmJlNDQ4MTMzMzVkMmIyNTZlOGE3YmJjZWVlIl0sICJwdWJsaWNfa2V5IjogIjkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieXRvbV9mdW5kX3Vuc2lnbmVkIn0"
        >>> sender_xprivate_key: str = "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"
        >>> normal_solver: NormalSolver = NormalSolver(sender_xprivate_key)
        >>> normal_signature: NormalSignature = NormalSignature("mainnet")
        >>> normal_signature.sign(unsigned_normal_transaction_raw, normal_solver)
        <swap.providers.vapor.signature.NormalSignature object at 0x0409DAF0>
        """

        if not is_transaction_raw(transaction_raw=transaction_raw):
            raise TransactionRawError("Invalid Vapor unsigned transaction raw.")

        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

        if not loaded_transaction_raw["type"] == "vapor_normal_unsigned":
            raise TypeError(f"Invalid Vapor normal unsigned transaction raw type, "
                            f"you can't sign {loaded_transaction_raw['type']} type by using normal signature.")

        # Check parameter instances
        if not isinstance(solver, NormalSolver):
            raise TypeError(f"Solver must be Vapor NormalSolver, not {type(solver).__name__} type.")

        # Set transaction, fee, type and network
        self._fee, self._type, self._network, self._transaction = (
            loaded_transaction_raw["fee"], loaded_transaction_raw["type"],
            loaded_transaction_raw["network"], loaded_transaction_raw
        )

        # Set recipient wallet
        wallet, path, indexes = solver.solve()
        # Clean derivation indexes/path
        wallet.clean_derivation()
        # Sign normal transaction
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
        self._type = "vapor_normal_signed"
        # Encode normal transaction raw
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


class FundSignature(Signature):
    """
    Vapor Fund signature.

    :param network: Vapor network, defaults to ``mainnet``.
    :type network: str

    :returns: FundSignature -- Vapor fund signature instance.
    """

    def __init__(self, network: str = config["network"]):
        super().__init__(network=network)

    def sign(self, transaction_raw: str, solver: FundSolver) -> "FundSignature":
        """
        Sign unsigned fund transaction raw.

        :param transaction_raw: Vapor unsigned fund transaction raw.
        :type transaction_raw: str
        :param solver: Vapor fund solver.
        :type solver: vapor.solver.FundSolver

        :returns: FundSignature -- Vapor fund signature instance.

        >>> from swap.providers.vapor.signature import FundSignature
        >>> from swap.providers.vapor.solver import FundSolver
        >>> unsigned_fund_transaction_raw: str = "eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogInZwMXFrOXZqNGphZXpsY25qZGNrZHM0ZmttOGZ3djVrYXdtcXdwbnB2cyIsICJyYXciOiAiMDcwMTAwMDEwMTVmMDE1ZGRmODJjZjdjNzkyNzc4NmE2OTU2OTM3NzQ0ZWU4MjM1NGM0ODFiMGYyMTFhYzUyYTVjMWQ3NDRjNGUzZTc4NjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYzhmOWEyMmEwMTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDIyMDEyMGZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIwMjAxNGEwMDQ4ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjgwYWRlMjA0MDEyMjAwMjAzNGEzZGI1MDMwMWI5NDFiOGVkNDNkY2ZkYmQzMzgxZGYxYjczOWZhNjRhYjc3ZTQyNjRmNzAzYTQ1ZTBiZTMxMDAwMTNlMDAzY2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZlMDk4YTUyNTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDAwIiwgImhhc2giOiAiYTA5ZjMwOTNhYWZmNmM4YzhmMWEzNzJlYWM2ODU3MWNlZWE0OTI4Y2NjOGI5YjU0OTU0ODYzNzU4NDQ3ZGVjMSIsICJ1bnNpZ25lZF9kYXRhcyI6IFt7ImRhdGFzIjogWyJkNzEwNzI1N2VmNWZiZmIwNGZjNDc0N2Q2ODg3ZjIzMGEzMDY3NmVjZDY3MDNhNTgwMTU4NzhiNTRmMWY3YjRmIl0sICJwdWJsaWNfa2V5IjogImZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJ2YXBvcl9mdW5kX3Vuc2lnbmVkIn0"
        >>> fund_signature: FundSignature = FundSignature(network="mainnet")
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="58775359b7b3588dcdc1bcf373489fa1272cacc03909f78469657b0208e66e46daedfdd0fd8f8df14e2084c7e8df4701db3062dded1c713e0aae734ac09c4afd")
        >>> fund_signature.sign(transaction_raw=unsigned_fund_transaction_raw, solver=fund_solver)
        <swap.providers.vapor.signature.FundSignature object at 0x0409DAF0>
        """

        if not is_transaction_raw(transaction_raw=transaction_raw):
            raise TransactionRawError("Invalid Vapor unsigned transaction raw.")

        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

        if not loaded_transaction_raw["type"] == "vapor_fund_unsigned":
            raise TypeError(f"Invalid Vapor fund unsigned transaction raw type, "
                            f"you can't sign {loaded_transaction_raw['type']} type by using fund signature.")

        # Check parameter instances
        if not isinstance(solver, FundSolver):
            raise TypeError(f"Solver must be Vapor FundSolver, not {type(solver).__name__} type.")

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
        self._type = "vapor_fund_signed"
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
    Vapor Withdraw signature.

    :param network: Vapor network, defaults to ``mainnet``.
    :type network: str

    :returns: WithdrawSignature -- Vapor withdraw signature instance.
    """

    def __init__(self, network: str = config["network"]):
        super().__init__(network=network)

    def sign(self, transaction_raw: str, solver: WithdrawSolver) -> "WithdrawSignature":
        """
        Sign unsigned withdraw transaction raw.

        :param transaction_raw: Vapor unsigned withdraw transaction raw.
        :type transaction_raw: str
        :param solver: Vapor withdraw solver.
        :type solver: vapor.solver.WithdrawSolver

        :returns: WithdrawSignature -- Vapor withdraw signature instance.

        >>> from swap.providers.vapor.signature import WithdrawSignature
        >>> from swap.providers.vapor.solver import WithdrawSolver
        >>> unsigned_withdraw_transaction_raw: str = "eyJmZWUiOiA1MDkwMDAsICJhZGRyZXNzIjogInZwMXF4ajNhazVwc3J3MnBocms1OGg4YWg1ZWNyaGNtd3cwNnZqNGgwZXB4ZmFjcjUzMHFoY2NzNHBjemdjIiwgInJhdyI6ICIwNzAxMDAwMTAxNmIwMTY5ZGY4MmNmN2M3OTI3Nzg2YTY5NTY5Mzc3NDRlZTgyMzU0YzQ4MWIwZjIxMWFjNTJhNWMxZDc0NGM0ZTNlNzg2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGFkZTIwNDAwMDEyMjAwMjAzNGEzZGI1MDMwMWI5NDFiOGVkNDNkY2ZkYmQzMzgxZGYxYjczOWZhNjRhYjc3ZTQyNjRmNzAzYTQ1ZTBiZTMxMDEwMDAxMDEzZTAwM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYjhhNGMzMDQwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkwMCIsICJoYXNoIjogIjkwNGFlZGExOTlmMDVjYmI3NjcxZTBkOWVjOTViMzA5MWYzYzEzMWNlZjhkNjM0YWUxNzIxNmI5YzJmZWE0OGMiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiM2ExMjNmZDgwOWQzYWQ4NDVhOTJhZDNlNWExZjBjYzEwM2RlNTExYWRmOTVjZjMwMjQwZDkxNjRkNmZmMTk2NCJdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiBudWxsfV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJ2YXBvcl93aXRoZHJhd191bnNpZ25lZCJ9"
        >>> bytecode: str = "042918320720fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"
        >>> withdraw_signature: WithdrawSignature = WithdrawSignature(network="mainnet")
        >>> withdraw_solver: WithdrawSolver = WithdrawSolver(xprivate_key="58dd4094155bbebf2868189231c47e4e0edbd9f74545f843c9537259e1d7a656983aef283d0ccebecc2d33577a9f650b53ac7adff44f48ec839e3346cc22418f", secret_key="Hello Meheret!", bytecode=bytecode)
        >>> withdraw_signature.sign(transaction_raw=unsigned_withdraw_transaction_raw, solver=withdraw_solver)
        <swap.providers.vapor.signature.WithdrawSignature object at 0x0409DAF0>
        """

        if not is_transaction_raw(transaction_raw=transaction_raw):
            raise TransactionRawError("Invalid Vapor unsigned transaction raw.")

        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

        if not loaded_transaction_raw["type"] == "vapor_withdraw_unsigned":
            raise TypeError(f"Invalid Vapor withdraw unsigned transaction raw type, "
                            f"you can't sign {loaded_transaction_raw['type']} type by using withdraw signature.")

        # Check parameter instances
        if not isinstance(solver, WithdrawSolver):
            raise TypeError(f"Solver must be Vapor WithdrawSolver, not {type(solver).__name__} type.")

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
        self._type = "vapor_withdraw_signed"
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
    Vapor Refund signature.

    :param network: Vapor network, defaults to ``mainnet``.
    :type network: str

    :returns: RefundSignature -- Vapor withdraw signature instance.
    """

    def __init__(self, network: str = config["network"]):
        super().__init__(network=network)

    def sign(self, transaction_raw: str, solver: RefundSolver) -> "RefundSignature":
        """
        Sign unsigned refund transaction raw.

        :param transaction_raw: Vapor unsigned refund transaction raw.
        :type transaction_raw: str
        :param solver: Vapor refund solver.
        :type solver: vapor.solver.RefundSolver

        :returns: RefundSignature -- Vapor refund signature instance.

        >>> from swap.providers.vapor.signature import RefundSignature
        >>> from swap.providers.vapor.solver import RefundSolver
        >>> unsigned_refund_transaction_raw: str = "eyJmZWUiOiA1MDkwMDAsICJhZGRyZXNzIjogInZwMXF4ajNhazVwc3J3MnBocms1OGg4YWg1ZWNyaGNtd3cwNnZqNGgwZXB4ZmFjcjUzMHFoY2NzNHBjemdjIiwgImhhc2giOiAiNmQ5NjQyMjIyYmFmYjlkNjk2OGVlMmVlZDk4OGM4MzdiMWRhNTZmY2VjNmZkOTYzMjlmZmY4YzBkNTUxOGY5MiIsICJyYXciOiAiMDcwMTAwMDEwMTZiMDE2OWRmODJjZjdjNzkyNzc4NmE2OTU2OTM3NzQ0ZWU4MjM1NGM0ODFiMGYyMTFhYzUyYTVjMWQ3NDRjNGUzZTc4NjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBhZGUyMDQwMDAxMjIwMDIwMzRhM2RiNTAzMDFiOTQxYjhlZDQzZGNmZGJkMzM4MWRmMWI3MzlmYTY0YWI3N2U0MjY0ZjcwM2E0NWUwYmUzMTAxMDAwMTAxM2UwMDNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmI4YTRjMzA0MDExNjAwMTRiMTU5MmFjYmI5MTdmMTM5MzcxNjZjMmE5YjZjZTk3MzI5NmViYjYwMDAiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiNmIyNGM0NDM4OTY2MWY4YzU3MDE0NmVjNGNjOGQzYWQzZjJkN2YxNjA3MTM2MjBiZTc0MzgwZTQwYmMwNmMwYyJdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiBudWxsfV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJ2YXBvcl9yZWZ1bmRfdW5zaWduZWQifQ"
        >>> bytecode: str = "042918320720fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"
        >>> refund_signature: RefundSignature = RefundSignature(network="mainnet")
        >>> refund_solver: RefundSolver = RefundSolver(xprivate_key="58775359b7b3588dcdc1bcf373489fa1272cacc03909f78469657b0208e66e46daedfdd0fd8f8df14e2084c7e8df4701db3062dded1c713e0aae734ac09c4afd", bytecode=bytecode)
        >>> refund_signature.sign(transaction_raw=unsigned_refund_transaction_raw, solver=refund_solver)
        <swap.providers.vapor.signature.RefundSignature object at 0x0409DAF0>
        """

        if not is_transaction_raw(transaction_raw=transaction_raw):
            raise TransactionRawError("Invalid Vapor unsigned transaction raw.")

        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

        if not loaded_transaction_raw["type"] == "vapor_refund_unsigned":
            raise TypeError(f"Invalid Vapor refund unsigned transaction raw type, "
                            f"you can't sign {loaded_transaction_raw['type']} type by using refund signature.")

        # Check parameter instances
        if not isinstance(solver, RefundSolver):
            raise TypeError(f"Solver must be Vapor RefundSolver, not {type(solver).__name__} type.")

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
        self._type = "vapor_refund_signed"
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
