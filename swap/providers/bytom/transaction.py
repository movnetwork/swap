#!/usr/bin/env python3

from pybytom.transaction import Transaction as BytomTransaction
from pybytom.transaction.actions import (
    spend_wallet, spend_utxo, control_address
)
from pybytom.wallet.tools import (
    indexes_to_path, get_program, get_address
)
from base64 import b64encode
from typing import (
    Optional, Union, List
)

import json

from ...utils import clean_transaction_raw
from ...exceptions import (
    AddressError, NetworkError, UnitError
)
from ..config import bytom as config
from .assets import AssetNamespace
from .htlc import HTLC
from .rpc import (
    estimate_transaction_fee, build_transaction, find_p2wsh_utxo, decode_raw, get_transaction
)
from .solver import (
    FundSolver, WithdrawSolver, RefundSolver
)
from .utils import (
    amount_unit_converter, is_network, is_address
)


class Transaction(BytomTransaction):
    """
    Bytom Transaction.

    :param network: Bytom network, defaults to mainnet.
    :type network: str

    :returns: Transaction -- Bytom transaction instance.

    .. note::
        Bytom has only three networks, ``mainnet``. ``solonet`` and ``mainnet``.
    """

    def __init__(self, network: str = config["network"]):

        if not is_network(network=network):
            raise NetworkError(f"Invalid Bytom '{network}' network",
                               "choose only 'mainnet', 'solonet' or 'testnet' networks.")
        super().__init__(network, vapor=False)

        self._network: str = network
        self._address: Optional[str] = None
        self._asset: Optional[str] = None
        self._transaction: Optional[dict] = None
        self._type: Optional[str] = None
        self._confirmations: int = config["confirmations"]
        self._amount: int = 0
        self._fee: int = 0

    def fee(self, unit: str = config["unit"]) -> Union[int, float]:
        """
        Get Bytom transaction fee.

        :param unit: Bytom unit, default to NEU.
        :type unit: str

        :returns: int, float -- Bytom transaction fee.

        >>> from swap.providers.bytom.transaction import WithdrawTransaction
        >>> withdraw_transaction: WithdrawTransaction = WithdrawTransaction(network="mainnet")
        >>> withdraw_transaction.build_transaction(address="bm1q3plwvmvy4qhjmp5zffzmk50aagpujt6f5je85p", transaction_hash="59b1e43b57cba1afa5834eb9886e4a9fba031c9880ce7ae29d32c36f6b47496f", asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> withdraw_transaction.fee(unit="NEU")
        509000
        """

        if unit not in ["BTM", "mBTM", "NEU"]:
            raise UnitError("Invalid Bytom unit, choose only 'BTM', 'mBTM' or 'NEU' units.")
        return self._fee if unit == "NEU" else \
            amount_unit_converter(amount=self._fee, unit_from=f"NEU2{unit}")

    def hash(self) -> str:
        """
        Get Bytom transaction hash.

        :returns: str -- Bytom transaction id/hash.

       >>> from swap.providers.bytom.htlc import HTLC
        >>> from swap.providers.bytom.transaction import FundTransaction
        >>> htlc: HTLC = HTLC(network="mainnet")
        >>> htlc.build_htlc(secret_hash="3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb", recipient_public_key="3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", sender_public_key="fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212", endblock=679208)
        >>> fund_transaction: FundTransaction = FundTransaction(network="mainnet")
        >>> fund_transaction.build_transaction(address="bm1qk9vj4jaezlcnjdckds4fkm8fwv5kawmq9qrufx", htlc=htlc, amount=0.1, asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", unit="BTM")
        >>> fund_transaction.hash()
        "a3078af0810c68a7bb6f2f42cd67dce9dea3d77028ca0c527224e4524038abc4"
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")
        return self._transaction["tx"]["hash"]

    def json(self) -> dict:
        """
        Get Bytom transaction json format.

        :returns: dict -- Bytom transaction json format.

        >>> from swap.providers.bytom.transaction import RefundTransaction
        >>> refund_transaction: RefundTransaction = RefundTransaction(network="mainnet")
        >>> refund_transaction.build_transaction(address="bm1qk9vj4jaezlcnjdckds4fkm8fwv5kawmq9qrufx", transaction_hash="59b1e43b57cba1afa5834eb9886e4a9fba031c9880ce7ae29d32c36f6b47496f", asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> refund_transaction.json()
        {"tx_id": "1722aa930f6f93b4c87788ea55f49055f26f86821bcd11a64d42bcb9e3b8a96d", "version": 1, "size": 179, "time_range": 0, "inputs": [{"type": "spend", "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "asset_definition": {}, "amount": 10000000, "control_program": "0020e7f4a9815f3a36c616c5666b97fb7fdacd3720c117d078c429494d1b617fe7d4", "address": "bm1qul62nq2l8gmvv9k9ve4e07mlmtxnwgxpzlg833pff9x3kctlul2q727jyy", "spent_output_id": "1aaf7df33c1d41bc6108c93d8b6da6af1d7f68632f54516408a03ff86494a1f0", "input_id": "6ccb3abb96d713fcaf27548ed76dadc695259fb7570b38ab9cde23f7ec261d60", "witness_arguments": null, "sign_data": "cc78c1fb648f8826e4dd4f85f885ac75866c0233b0af6581753d858304b8e04b"}], "outputs": [{"type": "control", "id": "6f831e2f958252a20b8d5aa9242c7bda229cb0e35bd2101978ea7df6cd7cc728", "position": 0, "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "asset_definition": {}, "amount": 9491000, "control_program": "0014b1592acbb917f13937166c2a9b6ce973296ebb60", "address": "bm1qk9vj4jaezlcnjdckds4fkm8fwv5kawmq9qrufx"}], "fee": 509000}
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")
        return decode_raw(raw=self._transaction["raw_transaction"])

    def raw(self) -> str:
        """
        Get Bytom transaction raw.

        :returns: str -- Bytom transaction raw.

        >>> from swap.providers.bytom.transaction import WithdrawTransaction
        >>> withdraw_transaction: WithdrawTransaction = WithdrawTransaction(network="mainnet")
        >>> withdraw_transaction.build_transaction(address="bm1q3plwvmvy4qhjmp5zffzmk50aagpujt6f5je85p", transaction_hash="59b1e43b57cba1afa5834eb9886e4a9fba031c9880ce7ae29d32c36f6b47496f", asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> withdraw_transaction.raw()
        "07010001016b0169f7df4d06a3fe3c8ac6438f25f9c97744a10455357857775526c3e6c752fb69eaffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff80ade2040001220020e7f4a9815f3a36c616c5666b97fb7fdacd3720c117d078c429494d1b617fe7d4010001013cffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffb8a4c30401160014887ee66d84a82f2d86824a45bb51fdea03c92f4900"
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")
        return self._transaction["raw_transaction"]

    def type(self) -> str:
        """
        Get Bytom signature transaction type.

        :returns: str -- Bytom signature transaction type.

        >>> from swap.providers.bytom.transaction import WithdrawTransaction
        >>> withdraw_transaction: WithdrawTransaction = WithdrawTransaction(network="mainnet")
        >>> withdraw_transaction.build_transaction(address="bm1q3plwvmvy4qhjmp5zffzmk50aagpujt6f5je85p", transaction_hash="59b1e43b57cba1afa5834eb9886e4a9fba031c9880ce7ae29d32c36f6b47496f", asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> withdraw_transaction.type()
        "bytom_withdraw_unsigned"
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("transaction script is none, build transaction first.")
        return self._type

    def unsigned_datas(self, detail: bool = False) -> List[dict]:
        """
        Get Bytom transaction unsigned datas(messages) with instruction.

        :param detail: Bytom unsigned datas to see detail, defaults to False.
        :type detail: bool

        :returns: list -- Bytom transaction unsigned datas.

        >>> from swap.providers.bytom.htlc import HTLC
        >>> from swap.providers.bytom.transaction import FundTransaction
        >>> htlc: HTLC = HTLC(network="mainnet")
        >>> htlc.build_htlc(secret_hash="3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb", recipient_public_key="3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", sender_public_key="fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212", endblock=679208)
        >>> fund_transaction: FundTransaction = FundTransaction(network="mainnet")
        >>> fund_transaction.build_transaction(address="bm1qk9vj4jaezlcnjdckds4fkm8fwv5kawmq9qrufx", htlc=htlc, amount=0.1, asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", unit="BTM")
        >>> fund_transaction.unsigned_datas()
        [{"datas": ["f42a2b6e15585b88da8b34237c7a6fd83af12ee6971813d66cf794a63ebcc16f"], "public_key": "fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212", "network": "mainnet", "path": "m/44/153/1/0/1"}]
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")

        unsigned_datas: List[dict] = []
        for signing_instruction in self._transaction["signing_instructions"]:
            unsigned_data = dict(datas=signing_instruction["sign_data"])
            if "pubkey" in signing_instruction and signing_instruction["pubkey"]:
                unsigned_data.setdefault("public_key", signing_instruction["pubkey"])
                if detail:
                    program = get_program(public_key=signing_instruction["pubkey"])
                    address = get_address(program=program, network=self._network)
                    unsigned_data.setdefault("program", program)
                    unsigned_data.setdefault("address", address)
                else:
                    unsigned_data.setdefault("network", self._network)
            else:
                if detail:
                    unsigned_data.setdefault("public_key", None)
                    unsigned_data.setdefault("program", None)
                    unsigned_data.setdefault("address", None)
                else:
                    unsigned_data.setdefault("network", self._network)
            if "derivation_path" in signing_instruction and signing_instruction["derivation_path"]:
                path = indexes_to_path(indexes=signing_instruction["derivation_path"])
                if detail:
                    unsigned_data.setdefault("indexes", signing_instruction["derivation_path"])
                unsigned_data.setdefault("path", path)
            else:
                if detail:
                    unsigned_data.setdefault("indexes", None)
                unsigned_data.setdefault("path", None)
            # Append unsigned datas
            unsigned_datas.append(unsigned_data)

        return unsigned_datas

    def signatures(self) -> List[List[str]]:
        """
        Get Bytom transaction signatures(signed datas).

        :returns: list -- Bytom transaction signatures.

        >>> from swap.providers.bytom.htlc import HTLC
        >>> from swap.providers.bytom.transaction import FundTransaction
        >>> from swap.providers.bytom.solver import FundSolver
        >>> htlc: HTLC = HTLC(network="mainnet")
        >>> htlc.build_htlc(secret_hash="3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb", recipient_public_key="3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", sender_public_key="fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212", endblock=679208)
        >>> fund_transaction: FundTransaction = FundTransaction(network="mainnet")
        >>> fund_transaction.build_transaction(address="bm1qk9vj4jaezlcnjdckds4fkm8fwv5kawmq9qrufx", htlc=htlc, amount=0.1, asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", unit="BTM")
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="58775359b7b3588dcdc1bcf373489fa1272cacc03909f78469657b0208e66e46daedfdd0fd8f8df14e2084c7e8df4701db3062dded1c713e0aae734ac09c4afd", path="m/44/153/1/0/1")
        >>> fund_transaction.sign(solver=fund_solver)
        >>> fund_transaction.signatures()
        [['b82e97abc4b70f7ffe7f783254c63e61436d6a7ad15da89b1fb791f91d1d6aa0bab7ff86328eabd2959f5475dde443e613ce7dfe70411be5b469b02069164a06']]
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")
        return self._signatures


class FundTransaction(Transaction):
    """
    Bytom Fund transaction.

    :param network: Bytom network, defaults to ``mainnet``.
    :type network: str

    :returns: FundTransaction -- Bytom fund transaction instance.

    .. warning::
        Do not forget to build transaction after initialize fund transaction.
    """

    def __init__(self, network: str = config["network"]):
        super().__init__(network)

        self._contract_address: Optional[str] = None

    def build_transaction(self, address: str, htlc: HTLC, amount: int, asset: Union[str, AssetNamespace] = config["asset"],
                          unit: str = config["unit"]) -> "FundTransaction":
        """
        Build Bytom fund transaction.

        :param address: Bytom sender wallet address.
        :type address: str
        :param htlc: Bytom Hash Time Lock Contract (HTLC) instance.
        :type htlc: str
        :param amount: Bytom amount to fund.
        :type amount: int, float
        :param asset: Bytom asset id, defaults to ``BTM``.
        :type asset: str, bytom.assets.AssetNamespace
        :param unit: Bytom unit, default to ``NEU``.
        :type unit: str

        :returns: FundTransaction -- Bytom fund transaction instance.

        >>> from swap.providers.bytom.htlc import HTLC
        >>> from swap.providers.bytom.transaction import FundTransaction
        >>> htlc: HTLC = HTLC(network="mainnet")
        >>> htlc.build_htlc(secret_hash="3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb", recipient_public_key="3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", sender_public_key="fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212", endblock=679208)
        >>> fund_transaction: FundTransaction = FundTransaction(network="mainnet")
        >>> fund_transaction.build_transaction(address="bm1qk9vj4jaezlcnjdckds4fkm8fwv5kawmq9qrufx", htlc=htlc, amount=0.1, asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", unit="BTM")
        <swap.providers.bytom.transaction.FundTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not is_address(address, self._network):
            raise AddressError(f"Invalid Bytom sender '{address}' {self._network} address.")
        if not isinstance(htlc, HTLC):
            raise TypeError("Invalid Bytom HTLC instance, only takes Bytom HTLC class")
        if unit not in ["BTM", "mBTM", "NEU"]:
            raise UnitError("Invalid Bytom unit, choose only 'BTM', 'mBTM' or 'NEU' units.")

        # Set address, fee and confirmations
        self._address, self._asset, self._contract_address, self._confirmations, self._amount = (
            address, (str(asset.ID) if isinstance(asset, AssetNamespace) else asset),
            htlc.contract_address(), config["confirmations"], (
                amount if unit == "NEU" else amount_unit_converter(
                    amount=amount, unit_from=f"{unit}2NEU"
                )
            )
        )

        self._fee = estimate_transaction_fee(
            address=self._address,
            amount=self._amount,
            asset=self._asset,
            confirmations=self._confirmations,
            network=self._network
        )

        # Build transaction
        self._transaction = build_transaction(
            address=self._address,
            transaction=dict(
                fee=str(amount_unit_converter(
                    amount=self._fee, unit_from="NEU2BTM"
                )),
                confirmations=self._confirmations,
                inputs=[
                    spend_wallet(
                        asset=self._asset, amount=self._amount
                    )
                ],
                outputs=[
                    control_address(
                        asset=self._asset, amount=self._amount, address=self._contract_address, vapor=False
                    )
                ]
            ),
            network=self._network
        )

        # Set transaction type
        self._type = "bytom_fund_unsigned"
        return self

    def sign(self, solver: FundSolver) -> "FundTransaction":
        """
        Sign Bytom fund transaction.

        :param solver: Bytom fund solver.
        :type solver: bytom.solver.FundSolver

        :returns: FundTransaction -- Bytom fund transaction instance.

        >>> from swap.providers.bytom.htlc import HTLC
        >>> from swap.providers.bytom.transaction import FundTransaction
        >>> from swap.providers.bytom.solver import FundSolver
        >>> htlc: HTLC = HTLC(network="mainnet")
        >>> htlc.build_htlc(secret_hash="3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb", recipient_public_key="3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", sender_public_key="fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212", endblock=679208)
        >>> fund_transaction: FundTransaction = FundTransaction(network="mainnet")
        >>> fund_transaction.build_transaction(address="bm1qk9vj4jaezlcnjdckds4fkm8fwv5kawmq9qrufx", htlc=htlc, amount=0.1, asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", unit="BTM")
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="58775359b7b3588dcdc1bcf373489fa1272cacc03909f78469657b0208e66e46daedfdd0fd8f8df14e2084c7e8df4701db3062dded1c713e0aae734ac09c4afd", path="m/44/153/1/0/1")
        >>> fund_transaction.sign(solver=fund_solver)
        <swap.providers.bytom.transaction.FundTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not isinstance(solver, FundSolver):
            raise TypeError(f"Solver must be Bytom FundSolver, not {type(solver).__name__} type.")

        # Setting sender wallet
        wallet, path, indexes = solver.solve()
        # Clean derivation indexes/path
        wallet.clean_derivation()
        # Signing fund transaction
        for unsigned in self.unsigned_datas(detail=True):
            signed_data = []
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
        return self

    def transaction_raw(self) -> str:
        """
        Get Bytom fund transaction raw.

        :returns: str -- Bytom fund transaction raw.

        >>> from swap.providers.bytom.htlc import HTLC
        >>> from swap.providers.bytom.transaction import FundTransaction
        >>> htlc: HTLC = HTLC(network="mainnet")
        >>> htlc.build_htlc(secret_hash="3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb", recipient_public_key="3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", sender_public_key="fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212", endblock=679208)
        >>> fund_transaction: FundTransaction = FundTransaction(network="mainnet")
        >>> fund_transaction.build_transaction(address="bm1qk9vj4jaezlcnjdckds4fkm8fwv5kawmq9qrufx", htlc=htlc, amount=0.1, asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", unit="BTM")
        >>> fund_transaction.transaction_raw()
        "eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogImJtMXFrOXZqNGphZXpsY25qZGNrZHM0ZmttOGZ3djVrYXdtcTlxcnVmeCIsICJyYXciOiAiMDcwMTAwMDEwMTVmMDE1ZGY3ZGY0ZDA2YTNmZTNjOGFjNjQzOGYyNWY5Yzk3NzQ0YTEwNDU1MzU3ODU3Nzc1NTI2YzNlNmM3NTJmYjY5ZWFmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOThhM2IxNWEwMTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDIyMDEyMGZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIwMjAxNDhmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBhZGUyMDQwMTIyMDAyMGU3ZjRhOTgxNWYzYTM2YzYxNmM1NjY2Yjk3ZmI3ZmRhY2QzNzIwYzExN2QwNzhjNDI5NDk0ZDFiNjE3ZmU3ZDQwMDAxM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYjBjMmIzNTUwMTE2MDAxNGIxNTkyYWNiYjkxN2YxMzkzNzE2NmMyYTliNmNlOTczMjk2ZWJiNjAwMCIsICJoYXNoIjogImEzMDc4YWYwODEwYzY4YTdiYjZmMmY0MmNkNjdkY2U5ZGVhM2Q3NzAyOGNhMGM1MjcyMjRlNDUyNDAzOGFiYzQiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiZjQyYTJiNmUxNTU4NWI4OGRhOGIzNDIzN2M3YTZmZDgzYWYxMmVlNjk3MTgxM2Q2NmNmNzk0YTYzZWJjYzE2ZiJdLCAicHVibGljX2tleSI6ICJmZTZiM2ZkNDQ1ODI5MWIxOTYwNWQ5MjgzN2FlMTA2MGNjMDIzN2U2ODAyMmIyZWI5ZmFmMDFhMTE4MjI2MjEyIiwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogIm0vNDQvMTUzLzEvMC8xIn1dLCAic2lnbmF0dXJlcyI6IFtdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInR5cGUiOiAiYnl0b21fZnVuZF91bnNpZ25lZCJ9"
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")

        # Encode fund transaction raw
        if self._type == "bytom_fund_signed":
            return clean_transaction_raw(b64encode(str(json.dumps(dict(
                fee=self._fee,
                address=self._address,
                raw=self.raw(),
                hash=self.hash(),
                unsigned_datas=self.unsigned_datas(
                    detail=False
                ),
                signatures=self.signatures(),
                network=self._network,
                type=self._type,
            ))).encode()).decode())
        return clean_transaction_raw(b64encode(str(json.dumps(dict(
            fee=self._fee,
            address=self._address,
            raw=self.raw(),
            hash=self.hash(),
            unsigned_datas=self.unsigned_datas(
                detail=False
            ),
            signatures=[],
            network=self._network,
            type=self._type,
        ))).encode()).decode())


class WithdrawTransaction(Transaction):
    """
    Bytom Withdraw transaction.

    :param network: Bytom network, defaults to ``mainnet``.
    :type network: str

    :returns: WithdrawTransaction -- Bytom withdraw transaction instance.

    .. warning::
        Do not forget to build transaction after initialize withdraw transaction.
    """

    def __init__(self, network: str = config["network"]):
        super().__init__(network)

        self._transaction_hash: Optional[str] = None
        self._transaction_detail: Optional[dict] = None
        self._htlc_utxo: Optional[dict] = None

    def build_transaction(self, address: str, transaction_hash: str,
                          asset: Union[str, AssetNamespace] = config["asset"]) -> "WithdrawTransaction":
        """
        Build Bytom withdraw transaction.

        :param address: Bytom recipient wallet address.
        :type address: str
        :param transaction_hash: Bytom funded transaction hash/id.
        :type transaction_hash: str
        :param asset: Bytom asset id, defaults to ``BTM``.
        :type asset: str, bytom.assets.AssetNamespace

        :returns: WithdrawTransaction -- Bytom withdraw transaction instance.

        >>> from swap.providers.bytom.transaction import WithdrawTransaction
        >>> withdraw_transaction: WithdrawTransaction = WithdrawTransaction(network="mainnet")
        >>> withdraw_transaction.build_transaction(address="bm1q3plwvmvy4qhjmp5zffzmk50aagpujt6f5je85p", transaction_hash="59b1e43b57cba1afa5834eb9886e4a9fba031c9880ce7ae29d32c36f6b47496f", asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        <swap.providers.bytom.transaction.WithdrawTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not is_address(address, self._network):
            raise AddressError(f"Invalid Bytom recipient '{address}' {self._network} address.")

        # Set address, asset, confirmations and transaction_hash
        self._address, self._asset, self._confirmations, self._transaction_hash = (
            address, (str(asset.ID) if isinstance(asset, AssetNamespace) else asset),
            config["confirmations"], transaction_hash
        )
        # Get transaction
        self._transaction_detail = get_transaction(
            transaction_hash=self._transaction_hash, network=self._network
        )
        # Find HTLC UTXO
        self._htlc_utxo: dict = find_p2wsh_utxo(transaction=self._transaction_detail)
        if self._htlc_utxo is None:
            raise ValueError("Invalid transaction id, there is no pay to witness script hash (P2WSH) address.")

        self._amount = self._htlc_utxo["amount"]

        # Estimating transaction fee
        self._fee = estimate_transaction_fee(
            address=self._htlc_utxo["address"], amount=self._amount, asset=self._asset,
            confirmations=self._confirmations, network=self._network
        ) + 60000

        # Build transaction
        self._transaction = build_transaction(
            address=self._htlc_utxo["address"],
            transaction=dict(
                fee=str(amount_unit_converter(
                    amount=self._fee, unit_from="NEU2BTM"
                )),
                confirmations=self._confirmations,
                inputs=[
                    spend_utxo(
                        utxo=self._htlc_utxo["id"]
                    )
                ],
                outputs=[
                    control_address(
                        asset=self._asset, amount=(self._amount - self._fee), address=self._address, vapor=False
                    )
                ]
            ),
            network=self._network
        )

        # Set transaction type
        self._type = "bytom_withdraw_unsigned"
        return self

    def sign(self, solver: WithdrawSolver) -> "WithdrawTransaction":
        """
        Sign Bytom withdraw transaction.

        :param solver: Bytom withdraw solver.
        :type solver: bytom.solver.WithdrawSolver

        :returns: WithdrawTransaction -- Bytom withdraw transaction instance.

        >>> from swap.providers.bytom.transaction import WithdrawTransaction
        >>> from swap.providers.bytom.solver import WithdrawSolver
        >>> withdraw_transaction: WithdrawTransaction = WithdrawTransaction(network="mainnet")
        >>> withdraw_transaction.build_transaction(address="bm1q3plwvmvy4qhjmp5zffzmk50aagpujt6f5je85p", transaction_hash="59b1e43b57cba1afa5834eb9886e4a9fba031c9880ce7ae29d32c36f6b47496f", asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> bytecode: str = "03285d0a20fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"
        >>> withdraw_solver: WithdrawSolver = WithdrawSolver(xprivate_key="58dd4094155bbebf2868189231c47e4e0edbd9f74545f843c9537259e1d7a656983aef283d0ccebecc2d33577a9f650b53ac7adff44f48ec839e3346cc22418f", secret_key="Hello Meheret!", bytecode=bytecode)
        >>> withdraw_transaction.sign(solver=withdraw_solver)
        <swap.providers.bytom.transaction.WithdrawTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not isinstance(solver, WithdrawSolver):
            raise TypeError(f"Solver must be Bytom WithdrawSolver, not {type(solver).__name__} type.")

        # Set recipient wallet
        wallet, secret, path, indexes = solver.solve()
        # Clean derivation indexes/path
        wallet.clean_derivation()
        # Sign withdraw transaction
        for index, unsigned in enumerate(self.unsigned_datas(detail=True)):
            signed_data = []
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
        return self

    def transaction_raw(self) -> str:
        """
        Get Bytom withdraw transaction raw.

        :returns: str -- Bytom withdraw transaction raw.

        >>> from swap.providers.bytom.transaction import WithdrawTransaction
        >>> withdraw_transaction: WithdrawTransaction = WithdrawTransaction(network="mainnet")
        >>> withdraw_transaction.build_transaction(address="bm1q3plwvmvy4qhjmp5zffzmk50aagpujt6f5je85p", transaction_hash="59b1e43b57cba1afa5834eb9886e4a9fba031c9880ce7ae29d32c36f6b47496f", asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> withdraw_transaction.transaction_raw()
        "eyJmZWUiOiA1MDkwMDAsICJhZGRyZXNzIjogImJtMXF1bDYybnEybDhnbXZ2OWs5dmU0ZTA3bWxtdHhud2d4cHpsZzgzM3BmZjl4M2tjdGx1bDJxNzI3anl5IiwgInJhdyI6ICIwNzAxMDAwMTAxNmIwMTY5ZjdkZjRkMDZhM2ZlM2M4YWM2NDM4ZjI1ZjljOTc3NDRhMTA0NTUzNTc4NTc3NzU1MjZjM2U2Yzc1MmZiNjllYWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGFkZTIwNDAwMDEyMjAwMjBlN2Y0YTk4MTVmM2EzNmM2MTZjNTY2NmI5N2ZiN2ZkYWNkMzcyMGMxMTdkMDc4YzQyOTQ5NGQxYjYxN2ZlN2Q0MDEwMDAxMDEzY2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZiOGE0YzMwNDAxMTYwMDE0ODg3ZWU2NmQ4NGE4MmYyZDg2ODI0YTQ1YmI1MWZkZWEwM2M5MmY0OTAwIiwgImhhc2giOiAiZDFlODRjMzdmNDEwNTZmNGRmMzk4NTIzZjg0ZWNmMDc5Mzc3ZmQ4NWU0NTYxYzEwZWMwMzgxOGNkNGRiN2VjMCIsICJ1bnNpZ25lZF9kYXRhcyI6IFt7ImRhdGFzIjogWyI0NWQxNzQ2YTFlYzA2OTVkM2UwNjA1OWM0MTM4NzIwNDBkMjRmODY0OTlkZGFmYWI0ODE3NzM2OGU1YzcyODgzIl0sICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6IG51bGx9XSwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX3dpdGhkcmF3X3Vuc2lnbmVkIn0"
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")

        # Encode withdraw transaction raw
        if self._type == "bytom_withdraw_signed":
            return clean_transaction_raw(b64encode(str(json.dumps(dict(
                fee=self._fee,
                address=self._htlc_utxo["address"],
                raw=self.raw(),
                hash=self.hash(),
                unsigned_datas=self.unsigned_datas(
                    detail=False
                ),
                signatures=self.signatures(),
                network=self._network,
                type=self._type
            ))).encode()).decode())
        return clean_transaction_raw(b64encode(str(json.dumps(dict(
            fee=self._fee,
            address=self._htlc_utxo["address"],
            raw=self.raw(),
            hash=self.hash(),
            unsigned_datas=self.unsigned_datas(
                detail=False
            ),
            signatures=[],
            network=self._network,
            type=self._type
        ))).encode()).decode())


class RefundTransaction(Transaction):
    """
    Bytom Refund transaction.

    :param network: Bytom network, defaults to ``mainnet``.
    :type network: str

    :returns: RefundTransaction -- Bytom refund transaction instance.

    .. warning::
        Do not forget to build transaction after initialize refund transaction.
    """

    def __init__(self, network: str = config["network"]):
        super().__init__(network)

        self._transaction_hash: Optional[str] = None
        self._transaction_detail: Optional[dict] = None
        self._htlc_utxo: Optional[dict] = None

    def build_transaction(self, address: str, transaction_hash: str,
                          asset: Union[str, AssetNamespace] = config["asset"]) -> "RefundTransaction":
        """
        Build Bytom refund transaction.

        :param address: Bytom sender wallet address.
        :type address: str
        :param transaction_hash: Bytom funded transaction hash/id
        :type transaction_hash: str
        :param asset: Bytom asset id, defaults to ``BTM``.
        :type asset: str, bytom.assets.AssetNamespace

        :returns: RefundTransaction -- Bytom refund transaction instance.

        >>> from swap.providers.bytom.transaction import RefundTransaction
        >>> refund_transaction: RefundTransaction = RefundTransaction(network="mainnet")
        >>> refund_transaction.build_transaction(address="bm1qk9vj4jaezlcnjdckds4fkm8fwv5kawmq9qrufx", transaction_hash="59b1e43b57cba1afa5834eb9886e4a9fba031c9880ce7ae29d32c36f6b47496f", asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        <swap.providers.bytom.transaction.RefundTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not is_address(address, self._network):
            raise AddressError(f"Invalid Bytom sender '{address}' {self._network} address.")

        # Set address, fee, confirmations and transaction_hash
        self._address, self._asset, self._confirmations, self._transaction_hash = (
            address, (str(asset.ID) if isinstance(asset, AssetNamespace) else asset),
            config["confirmations"], transaction_hash
        )
        # Get transaction
        self._transaction_detail = get_transaction(
            transaction_hash=self._transaction_hash, network=self._network
        )
        # Find HTLC UTXO
        self._htlc_utxo = find_p2wsh_utxo(transaction=self._transaction_detail)
        if self._htlc_utxo is None:
            raise ValueError("Invalid transaction id, there is no pay to witness script hash (P2WSH) address.")

        self._amount = self._htlc_utxo["amount"]

        # Estimating transaction fee
        self._fee = estimate_transaction_fee(
            address=self._htlc_utxo["address"], amount=self._amount, asset=self._asset,
            confirmations=self._confirmations, network=self._network
        ) + 60000

        # Build transaction
        self._transaction = build_transaction(
            address=self._htlc_utxo["address"],
            transaction=dict(
                fee=str(amount_unit_converter(
                    amount=self._fee, unit_from="NEU2BTM"
                )),
                confirmations=self._confirmations,
                inputs=[
                    spend_utxo(
                        utxo=self._htlc_utxo["id"]
                    )
                ],
                outputs=[
                    control_address(
                        asset=self._asset, amount=(self._amount - self._fee), address=self._address, vapor=False
                    )
                ]
            ),
            network=self._network
        )

        # Set transaction type
        self._type = "bytom_refund_unsigned"
        return self

    def sign(self, solver: RefundSolver) -> "RefundTransaction":
        """
        Sign Bytom refund transaction.

        :param solver: Bytom refund solver.
        :type solver: bytom.solver.RefundSolver

        :returns: RefundTransaction -- Bytom refund transaction instance.

        >>> from swap.providers.bytom.transaction import RefundTransaction
        >>> from swap.providers.bytom.solver import RefundSolver
        >>> refund_transaction: RefundTransaction = RefundTransaction(network="mainnet")
        >>> refund_transaction.build_transaction(address="bm1qk9vj4jaezlcnjdckds4fkm8fwv5kawmq9qrufx", transaction_hash="59b1e43b57cba1afa5834eb9886e4a9fba031c9880ce7ae29d32c36f6b47496f", asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> bytecode: str = "03285d0a20fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"
        >>> refund_solver: RefundSolver = RefundSolver(xprivate_key="58775359b7b3588dcdc1bcf373489fa1272cacc03909f78469657b0208e66e46daedfdd0fd8f8df14e2084c7e8df4701db3062dded1c713e0aae734ac09c4afd", bytecode=bytecode)
        >>> refund_transaction.sign(solver=refund_solver)
        <swap.providers.bytom.transaction.RefundTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not isinstance(solver, RefundSolver):
            raise TypeError(f"Solver must be Bytom RefundSolver, not {type(solver).__name__} type.")

        # Set recipient wallet
        wallet, path, indexes = solver.solve()
        # Clean derivation indexes/path
        wallet.clean_derivation()
        # Sign withdraw transaction
        for index, unsigned in enumerate(self.unsigned_datas(detail=True)):
            signed_data = []
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

        # Set transaction type
        self._type = "bytom_refund_signed"
        return self

    def transaction_raw(self) -> str:
        """
        Get Bytom refund transaction raw.

        :returns: str -- Bytom refund transaction raw.

        >>> from swap.providers.bytom.transaction import RefundTransaction
        >>> refund_transaction: RefundTransaction = RefundTransaction(network="mainnet")
        >>> refund_transaction.build_transaction(address="bm1qk9vj4jaezlcnjdckds4fkm8fwv5kawmq9qrufx", transaction_hash="59b1e43b57cba1afa5834eb9886e4a9fba031c9880ce7ae29d32c36f6b47496f", asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> refund_transaction.transaction_raw()
        "eyJmZWUiOiA1MDkwMDAsICJhZGRyZXNzIjogImJtMXF1bDYybnEybDhnbXZ2OWs5dmU0ZTA3bWxtdHhud2d4cHpsZzgzM3BmZjl4M2tjdGx1bDJxNzI3anl5IiwgImhhc2giOiAiMTcyMmFhOTMwZjZmOTNiNGM4Nzc4OGVhNTVmNDkwNTVmMjZmODY4MjFiY2QxMWE2NGQ0MmJjYjllM2I4YTk2ZCIsICJyYXciOiAiMDcwMTAwMDEwMTZiMDE2OWY3ZGY0ZDA2YTNmZTNjOGFjNjQzOGYyNWY5Yzk3NzQ0YTEwNDU1MzU3ODU3Nzc1NTI2YzNlNmM3NTJmYjY5ZWFmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBhZGUyMDQwMDAxMjIwMDIwZTdmNGE5ODE1ZjNhMzZjNjE2YzU2NjZiOTdmYjdmZGFjZDM3MjBjMTE3ZDA3OGM0Mjk0OTRkMWI2MTdmZTdkNDAxMDAwMTAxM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYjhhNGMzMDQwMTE2MDAxNGIxNTkyYWNiYjkxN2YxMzkzNzE2NmMyYTliNmNlOTczMjk2ZWJiNjAwMCIsICJ1bnNpZ25lZF9kYXRhcyI6IFt7ImRhdGFzIjogWyJjYzc4YzFmYjY0OGY4ODI2ZTRkZDRmODVmODg1YWM3NTg2NmMwMjMzYjBhZjY1ODE3NTNkODU4MzA0YjhlMDRiIl0sICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6IG51bGx9XSwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX3JlZnVuZF91bnNpZ25lZCJ9"
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")

        # Encode refund transaction raw
        if self._type == "bytom_refund_signed":
            return clean_transaction_raw(b64encode(str(json.dumps(dict(
                fee=self._fee,
                address=self._htlc_utxo["address"],
                raw=self.raw(),
                hash=self.hash(),
                unsigned_datas=self.unsigned_datas(
                    detail=False
                ),
                signatures=self.signatures(),
                network=self._network,
                type=self._type
            ))).encode()).decode())
        return clean_transaction_raw(b64encode(str(json.dumps(dict(
            fee=self._fee,
            address=self._htlc_utxo["address"],
            hash=self.hash(),
            raw=self.raw(),
            unsigned_datas=self.unsigned_datas(
                detail=False
            ),
            signatures=[],
            network=self._network,
            type=self._type
        ))).encode()).decode())
