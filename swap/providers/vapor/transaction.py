#!/usr/bin/env python3

from pybytom.transaction import Transaction as VaporTransaction
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
from ..config import vapor as config
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


class Transaction(VaporTransaction):
    """
    Vapor Transaction.

    :param network: Vapor network, defaults to mainnet.
    :type network: str

    :returns: Transaction -- Vapor transaction instance.

    .. note::
        Vapor has only three networks, ``mainnet``. ``solonet`` and ``mainnet``.
    """

    def __init__(self, network: str = config["network"]):

        if not is_network(network=network):
            raise NetworkError(f"Invalid Vapor '{network}' network",
                               "choose only 'mainnet', 'solonet' or 'testnet' networks.")
        super().__init__(network, vapor=True)

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
        Get Vapor transaction fee.

        :param unit: Vapor unit, default to NEU.
        :type unit: str

        :returns: int, float -- Vapor transaction fee.

        >>> from swap.providers.vapor.transaction import WithdrawTransaction
        >>> withdraw_transaction: WithdrawTransaction = WithdrawTransaction(network="mainnet")
        >>> withdraw_transaction.build_transaction(address="vp1q3plwvmvy4qhjmp5zffzmk50aagpujt6flnf63h", transaction_hash="37b36d7be5dfda0cc5dc3c918705464ff901dc5eadb6f4f049db03a679e02bfe", asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> withdraw_transaction.fee(unit="NEU")
        509000
        """

        if unit not in ["BTM", "mBTM", "NEU"]:
            raise UnitError("Invalid Vapor unit, choose only 'BTM', 'mBTM' or 'NEU' units.")
        return self._fee if unit == "NEU" else \
            amount_unit_converter(amount=self._fee, unit_from=f"NEU2{unit}")

    def hash(self) -> str:
        """
        Get Vapor transaction hash.

        :returns: str -- Vapor transaction id/hash.

       >>> from swap.providers.vapor.htlc import HTLC
        >>> from swap.providers.vapor.transaction import FundTransaction
        >>> htlc: HTLC = HTLC(network="mainnet")
        >>> htlc.build_htlc(secret_hash="3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb", recipient_public_key="3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", sender_public_key="fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212", endblock=120723497)
        >>> fund_transaction: FundTransaction = FundTransaction(network="mainnet")
        >>> fund_transaction.build_transaction(address="vp1qk9vj4jaezlcnjdckds4fkm8fwv5kawmqwpnpvs", htlc=htlc, amount=0.1, asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", unit="BTM")
        >>> fund_transaction.hash()
        "a09f3093aaff6c8c8f1a372eac68571ceea4928ccc8b9b54954863758447dec1"
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")
        return self._transaction["tx"]["hash"]

    def json(self) -> dict:
        """
        Get Vapor transaction json format.

        :returns: dict -- Vapor transaction json format.

        >>> from swap.providers.vapor.transaction import RefundTransaction
        >>> refund_transaction: RefundTransaction = RefundTransaction(network="mainnet")
        >>> refund_transaction.build_transaction(address="vp1qk9vj4jaezlcnjdckds4fkm8fwv5kawmqwpnpvs", transaction_hash="37b36d7be5dfda0cc5dc3c918705464ff901dc5eadb6f4f049db03a679e02bfe", asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> refund_transaction.json()
        {'tx_id': '6d9642222bafb9d6968ee2eed988c837b1da56fcec6fd96329fff8c0d5518f92', 'version': 1, 'size': 181, 'time_range': 0, 'inputs': [{'type': 'spend', 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'asset_definition': {}, 'amount': 10000000, 'control_program': '002034a3db50301b941b8ed43dcfdbd3381df1b739fa64ab77e4264f703a45e0be31', 'address': 'vp1qxj3ak5psrw2phrk58h8ah5ecrhcmww06vj4h0epxfacr530qhccs4pczgc', 'spent_output_id': '144dd8355cae0d9aea6ca3fb1ff685fb7b455b1f9cb0c5992c9035844c664ad1', 'input_id': '576edbd5cf8682fb82eb8fb61ba3d6f25a9490777be607d2e75b2dbcbbceb89e', 'witness_arguments': None}], 'outputs': [{'type': 'control', 'id': 'b6a843f8257fc06ad922a69fa2cfa413277703ffb04512a35799d3c8a2c5d7a2', 'position': 0, 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'asset_definition': {}, 'amount': 9491000, 'control_program': '0014b1592acbb917f13937166c2a9b6ce973296ebb60', 'address': 'vp1qk9vj4jaezlcnjdckds4fkm8fwv5kawmqwpnpvs'}], 'fee': 509000}
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")
        return decode_raw(raw=self._transaction["raw_transaction"])

    def raw(self) -> str:
        """
        Get Vapor transaction raw.

        :returns: str -- Vapor transaction raw.

        >>> from swap.providers.vapor.transaction import WithdrawTransaction
        >>> withdraw_transaction: WithdrawTransaction = WithdrawTransaction(network="mainnet")
        >>> withdraw_transaction.build_transaction(address="vp1q3plwvmvy4qhjmp5zffzmk50aagpujt6flnf63h", transaction_hash="37b36d7be5dfda0cc5dc3c918705464ff901dc5eadb6f4f049db03a679e02bfe", asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> withdraw_transaction.raw()
        "07010001016b0169df82cf7c7927786a6956937744ee82354c481b0f211ac52a5c1d744c4e3e7866ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff80ade204000122002034a3db50301b941b8ed43dcfdbd3381df1b739fa64ab77e4264f703a45e0be31010001013e003cffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffb8a4c30401160014887ee66d84a82f2d86824a45bb51fdea03c92f4900"
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")
        return self._transaction["raw_transaction"]

    def type(self) -> str:
        """
        Get Vapor signature transaction type.

        :returns: str -- Vapor signature transaction type.

        >>> from swap.providers.vapor.transaction import WithdrawTransaction
        >>> withdraw_transaction: WithdrawTransaction = WithdrawTransaction(network="mainnet")
        >>> withdraw_transaction.build_transaction(address="vp1q3plwvmvy4qhjmp5zffzmk50aagpujt6flnf63h", transaction_hash="37b36d7be5dfda0cc5dc3c918705464ff901dc5eadb6f4f049db03a679e02bfe", asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> withdraw_transaction.type()
        "vapor_withdraw_unsigned"
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("transaction script is none, build transaction first.")
        return self._type

    def unsigned_datas(self, detail: bool = False) -> List[dict]:
        """
        Get Vapor transaction unsigned datas(messages) with instruction.

        :param detail: Vapor unsigned datas to see detail, defaults to False.
        :type detail: bool

        :returns: list -- Vapor transaction unsigned datas.

        >>> from swap.providers.vapor.htlc import HTLC
        >>> from swap.providers.vapor.transaction import FundTransaction
        >>> htlc: HTLC = HTLC(network="mainnet")
        >>> htlc.build_htlc(secret_hash="3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb", recipient_public_key="3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", sender_public_key="fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212", endblock=120723497)
        >>> fund_transaction: FundTransaction = FundTransaction(network="mainnet")
        >>> fund_transaction.build_transaction(address="vp1qk9vj4jaezlcnjdckds4fkm8fwv5kawmqwpnpvs", htlc=htlc, amount=0.1, asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", unit="BTM")
        >>> fund_transaction.unsigned_datas()
        [{'datas': ['d7107257ef5fbfb04fc4747d6887f230a30676ecd6703a58015878b54f1f7b4f'], 'public_key': 'fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212', 'network': 'mainnet', 'path': 'm/44/153/1/0/1'}]
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
        Get Vapor transaction signatures(signed datas).

        :returns: list -- Vapor transaction signatures.

        >>> from swap.providers.vapor.htlc import HTLC
        >>> from swap.providers.vapor.transaction import FundTransaction
        >>> from swap.providers.vapor.solver import FundSolver
        >>> htlc: HTLC = HTLC(network="mainnet")
        >>> htlc.build_htlc(secret_hash="3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb", recipient_public_key="3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", sender_public_key="fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212", endblock=120723497)
        >>> fund_transaction: FundTransaction = FundTransaction(network="mainnet")
        >>> fund_transaction.build_transaction(address="vp1qk9vj4jaezlcnjdckds4fkm8fwv5kawmqwpnpvs", htlc=htlc, amount=0.1, asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", unit="BTM")
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="58775359b7b3588dcdc1bcf373489fa1272cacc03909f78469657b0208e66e46daedfdd0fd8f8df14e2084c7e8df4701db3062dded1c713e0aae734ac09c4afd", path="m/44/153/1/0/1")
        >>> fund_transaction.sign(solver=fund_solver)
        >>> fund_transaction.signatures()
        [['0d2e4e42fcee863e74195dceab1dfccf368055b171196faa90c53eaa2cea649bb43cc132354edad970b356aae5d628dd0160e787ac174af89ca534d14db71e00']]
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")
        return self._signatures


class FundTransaction(Transaction):
    """
    Vapor Fund transaction.

    :param network: Vapor network, defaults to ``mainnet``.
    :type network: str

    :returns: FundTransaction -- Vapor fund transaction instance.

    .. warning::
        Do not forget to build transaction after initialize fund transaction.
    """

    def __init__(self, network: str = config["network"]):
        super().__init__(network)

        self._contract_address: Optional[str] = None

    def build_transaction(self, address: str, htlc: HTLC, amount: int, asset: Union[str, AssetNamespace] = config["asset"],
                          unit: str = config["unit"]) -> "FundTransaction":
        """
        Build Vapor fund transaction.

        :param address: Vapor sender wallet address.
        :type address: str
        :param htlc: Vapor Hash Time Lock Contract (HTLC) instance.
        :type htlc: str
        :param amount: Vapor amount to fund.
        :type amount: int, float
        :param asset: Vapor asset id, defaults to ``BTM``.
        :type asset: str, vapor.assets.AssetNamespace
        :param unit: Vapor unit, default to ``NEU``.
        :type unit: str

        :returns: FundTransaction -- Vapor fund transaction instance.

        >>> from swap.providers.vapor.htlc import HTLC
        >>> from swap.providers.vapor.transaction import FundTransaction
        >>> htlc: HTLC = HTLC(network="mainnet")
        >>> htlc.build_htlc(secret_hash="3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb", recipient_public_key="3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", sender_public_key="fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212", endblock=120723497)
        >>> fund_transaction: FundTransaction = FundTransaction(network="mainnet")
        >>> fund_transaction.build_transaction(address="vp1qk9vj4jaezlcnjdckds4fkm8fwv5kawmqwpnpvs", htlc=htlc, amount=0.1, asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", unit="BTM")
        <swap.providers.vapor.transaction.FundTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not is_address(address, self._network):
            raise AddressError(f"Invalid Vapor sender '{address}' {self._network} address.")
        if not isinstance(htlc, HTLC):
            raise TypeError("Invalid Vapor HTLC instance, only takes Vapor HTLC class")
        if unit not in ["BTM", "mBTM", "NEU"]:
            raise UnitError("Invalid Vapor unit, choose only 'BTM', 'mBTM' or 'NEU' units.")

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
                        asset=self._asset, amount=self._amount, address=self._contract_address, vapor=True
                    )
                ]
            ),
            network=self._network
        )

        # Set transaction type
        self._type = "vapor_fund_unsigned"
        return self

    def sign(self, solver: FundSolver) -> "FundTransaction":
        """
        Sign Vapor fund transaction.

        :param solver: Vapor fund solver.
        :type solver: vapor.solver.FundSolver

        :returns: FundTransaction -- Vapor fund transaction instance.

        >>> from swap.providers.vapor.htlc import HTLC
        >>> from swap.providers.vapor.transaction import FundTransaction
        >>> from swap.providers.vapor.solver import FundSolver
        >>> htlc: HTLC = HTLC(network="mainnet")
        >>> htlc.build_htlc(secret_hash="3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb", recipient_public_key="3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", sender_public_key="fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212", endblock=120723497)
        >>> fund_transaction: FundTransaction = FundTransaction(network="mainnet")
        >>> fund_transaction.build_transaction(address="vp1qk9vj4jaezlcnjdckds4fkm8fwv5kawmqwpnpvs", htlc=htlc, amount=0.1, asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", unit="BTM")
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="58775359b7b3588dcdc1bcf373489fa1272cacc03909f78469657b0208e66e46daedfdd0fd8f8df14e2084c7e8df4701db3062dded1c713e0aae734ac09c4afd", path="m/44/153/1/0/1")
        >>> fund_transaction.sign(solver=fund_solver)
        <swap.providers.vapor.transaction.FundTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not isinstance(solver, FundSolver):
            raise TypeError(f"Solver must be Vapor FundSolver, not {type(solver).__name__} type.")

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
        self._type = "vapor_fund_signed"
        return self

    def transaction_raw(self) -> str:
        """
        Get Vapor fund transaction raw.

        :returns: str -- Vapor fund transaction raw.

        >>> from swap.providers.vapor.htlc import HTLC
        >>> from swap.providers.vapor.transaction import FundTransaction
        >>> htlc: HTLC = HTLC(network="mainnet")
        >>> htlc.build_htlc(secret_hash="3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb", recipient_public_key="3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", sender_public_key="fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212", endblock=120723497)
        >>> fund_transaction: FundTransaction = FundTransaction(network="mainnet")
        >>> fund_transaction.build_transaction(address="vp1qk9vj4jaezlcnjdckds4fkm8fwv5kawmqwpnpvs", htlc=htlc, amount=0.1, asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", unit="BTM")
        >>> fund_transaction.transaction_raw()
        "eyJmZWUiOiA0NDkwMDAsICJhZGRyZXNzIjogInZwMXFrOXZqNGphZXpsY25qZGNrZHM0ZmttOGZ3djVrYXdtcXdwbnB2cyIsICJyYXciOiAiMDcwMTAwMDEwMTVmMDE1ZGRmODJjZjdjNzkyNzc4NmE2OTU2OTM3NzQ0ZWU4MjM1NGM0ODFiMGYyMTFhYzUyYTVjMWQ3NDRjNGUzZTc4NjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYzhmOWEyMmEwMTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDIyMDEyMGZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIwMjAxNGEwMDQ4ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjgwYWRlMjA0MDEyMjAwMjAzNGEzZGI1MDMwMWI5NDFiOGVkNDNkY2ZkYmQzMzgxZGYxYjczOWZhNjRhYjc3ZTQyNjRmNzAzYTQ1ZTBiZTMxMDAwMTNlMDAzY2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZlMDk4YTUyNTAxMTYwMDE0YjE1OTJhY2JiOTE3ZjEzOTM3MTY2YzJhOWI2Y2U5NzMyOTZlYmI2MDAwIiwgImhhc2giOiAiYTA5ZjMwOTNhYWZmNmM4YzhmMWEzNzJlYWM2ODU3MWNlZWE0OTI4Y2NjOGI5YjU0OTU0ODYzNzU4NDQ3ZGVjMSIsICJ1bnNpZ25lZF9kYXRhcyI6IFt7ImRhdGFzIjogWyJkNzEwNzI1N2VmNWZiZmIwNGZjNDc0N2Q2ODg3ZjIzMGEzMDY3NmVjZDY3MDNhNTgwMTU4NzhiNTRmMWY3YjRmIl0sICJwdWJsaWNfa2V5IjogImZlNmIzZmQ0NDU4MjkxYjE5NjA1ZDkyODM3YWUxMDYwY2MwMjM3ZTY4MDIyYjJlYjlmYWYwMWExMTgyMjYyMTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJ2YXBvcl9mdW5kX3Vuc2lnbmVkIn0"
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")

        # Encode fund transaction raw
        if self._type == "vapor_fund_signed":
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
    Vapor Withdraw transaction.

    :param network: Vapor network, defaults to ``mainnet``.
    :type network: str

    :returns: WithdrawTransaction -- Vapor withdraw transaction instance.

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
        Build Vapor withdraw transaction.

        :param address: Vapor recipient wallet address.
        :type address: str
        :param transaction_hash: Vapor funded transaction hash/id.
        :type transaction_hash: str
        :param asset: Vapor asset id, defaults to ``BTM``.
        :type asset: str, vapor.assets.AssetNamespace

        :returns: WithdrawTransaction -- Vapor withdraw transaction instance.

        >>> from swap.providers.vapor.transaction import WithdrawTransaction
        >>> withdraw_transaction: WithdrawTransaction = WithdrawTransaction(network="mainnet")
        >>> withdraw_transaction.build_transaction(address="vp1q3plwvmvy4qhjmp5zffzmk50aagpujt6flnf63h", transaction_hash="37b36d7be5dfda0cc5dc3c918705464ff901dc5eadb6f4f049db03a679e02bfe", asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        <swap.providers.vapor.transaction.WithdrawTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not is_address(address, self._network):
            raise AddressError(f"Invalid Vapor recipient '{address}' {self._network} address.")

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
                        asset=self._asset, amount=(self._amount - self._fee), address=self._address, vapor=True
                    )
                ]
            ),
            network=self._network
        )

        # Set transaction type
        self._type = "vapor_withdraw_unsigned"
        return self

    def sign(self, solver: WithdrawSolver) -> "WithdrawTransaction":
        """
        Sign Vapor withdraw transaction.

        :param solver: Vapor withdraw solver.
        :type solver: vapor.solver.WithdrawSolver

        :returns: WithdrawTransaction -- Vapor withdraw transaction instance.

        >>> from swap.providers.vapor.transaction import WithdrawTransaction
        >>> from swap.providers.vapor.solver import WithdrawSolver
        >>> withdraw_transaction: WithdrawTransaction = WithdrawTransaction(network="mainnet")
        >>> withdraw_transaction.build_transaction(address="vp1q3plwvmvy4qhjmp5zffzmk50aagpujt6flnf63h", transaction_hash="37b36d7be5dfda0cc5dc3c918705464ff901dc5eadb6f4f049db03a679e02bfe", asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> bytecode: str = "042918320720fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"
        >>> withdraw_solver: WithdrawSolver = WithdrawSolver(xprivate_key="58dd4094155bbebf2868189231c47e4e0edbd9f74545f843c9537259e1d7a656983aef283d0ccebecc2d33577a9f650b53ac7adff44f48ec839e3346cc22418f", secret_key="Hello Meheret!", bytecode=bytecode)
        >>> withdraw_transaction.sign(solver=withdraw_solver)
        <swap.providers.vapor.transaction.WithdrawTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not isinstance(solver, WithdrawSolver):
            raise TypeError(f"Solver must be Vapor WithdrawSolver, not {type(solver).__name__} type.")

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
        self._type = "vapor_withdraw_signed"
        return self

    def transaction_raw(self) -> str:
        """
        Get Vapor withdraw transaction raw.

        :returns: str -- Vapor withdraw transaction raw.

        >>> from swap.providers.vapor.transaction import WithdrawTransaction
        >>> withdraw_transaction: WithdrawTransaction = WithdrawTransaction(network="mainnet")
        >>> withdraw_transaction.build_transaction(address="vp1q3plwvmvy4qhjmp5zffzmk50aagpujt6flnf63h", transaction_hash="37b36d7be5dfda0cc5dc3c918705464ff901dc5eadb6f4f049db03a679e02bfe", asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> withdraw_transaction.transaction_raw()
        "eyJmZWUiOiA1MDkwMDAsICJhZGRyZXNzIjogInZwMXF4ajNhazVwc3J3MnBocms1OGg4YWg1ZWNyaGNtd3cwNnZqNGgwZXB4ZmFjcjUzMHFoY2NzNHBjemdjIiwgInJhdyI6ICIwNzAxMDAwMTAxNmIwMTY5ZGY4MmNmN2M3OTI3Nzg2YTY5NTY5Mzc3NDRlZTgyMzU0YzQ4MWIwZjIxMWFjNTJhNWMxZDc0NGM0ZTNlNzg2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGFkZTIwNDAwMDEyMjAwMjAzNGEzZGI1MDMwMWI5NDFiOGVkNDNkY2ZkYmQzMzgxZGYxYjczOWZhNjRhYjc3ZTQyNjRmNzAzYTQ1ZTBiZTMxMDEwMDAxMDEzZTAwM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYjhhNGMzMDQwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkwMCIsICJoYXNoIjogIjkwNGFlZGExOTlmMDVjYmI3NjcxZTBkOWVjOTViMzA5MWYzYzEzMWNlZjhkNjM0YWUxNzIxNmI5YzJmZWE0OGMiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiM2ExMjNmZDgwOWQzYWQ4NDVhOTJhZDNlNWExZjBjYzEwM2RlNTExYWRmOTVjZjMwMjQwZDkxNjRkNmZmMTk2NCJdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiBudWxsfV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJ2YXBvcl93aXRoZHJhd191bnNpZ25lZCJ9"
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")

        # Encode withdraw transaction raw
        if self._type == "vapor_withdraw_signed":
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
    Vapor Refund transaction.

    :param network: Vapor network, defaults to ``mainnet``.
    :type network: str

    :returns: RefundTransaction -- Vapor refund transaction instance.

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
        Build Vapor refund transaction.

        :param address: Vapor sender wallet address.
        :type address: str
        :param transaction_hash: Vapor funded transaction hash/id
        :type transaction_hash: str
        :param asset: Vapor asset id, defaults to ``BTM``.
        :type asset: str, vapor.assets.AssetNamespace

        :returns: RefundTransaction -- Vapor refund transaction instance.

        >>> from swap.providers.vapor.transaction import RefundTransaction
        >>> refund_transaction: RefundTransaction = RefundTransaction(network="mainnet")
        >>> refund_transaction.build_transaction(address="vp1qk9vj4jaezlcnjdckds4fkm8fwv5kawmqwpnpvs", transaction_hash="37b36d7be5dfda0cc5dc3c918705464ff901dc5eadb6f4f049db03a679e02bfe", asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        <swap.providers.vapor.transaction.RefundTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not is_address(address, self._network):
            raise AddressError(f"Invalid Vapor sender '{address}' {self._network} address.")

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
                        asset=self._asset, amount=(self._amount - self._fee), address=self._address, vapor=True
                    )
                ]
            ),
            network=self._network
        )

        # Set transaction type
        self._type = "vapor_refund_unsigned"
        return self

    def sign(self, solver: RefundSolver) -> "RefundTransaction":
        """
        Sign Vapor refund transaction.

        :param solver: Vapor refund solver.
        :type solver: vapor.solver.RefundSolver

        :returns: RefundTransaction -- Vapor refund transaction instance.

        >>> from swap.providers.vapor.transaction import RefundTransaction
        >>> from swap.providers.vapor.solver import RefundSolver
        >>> refund_transaction: RefundTransaction = RefundTransaction(network="mainnet")
        >>> refund_transaction.build_transaction(address="vp1qk9vj4jaezlcnjdckds4fkm8fwv5kawmqwpnpvs", transaction_hash="37b36d7be5dfda0cc5dc3c918705464ff901dc5eadb6f4f049db03a679e02bfe", asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> bytecode: str = "042918320720fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"
        >>> refund_solver: RefundSolver = RefundSolver(xprivate_key="58775359b7b3588dcdc1bcf373489fa1272cacc03909f78469657b0208e66e46daedfdd0fd8f8df14e2084c7e8df4701db3062dded1c713e0aae734ac09c4afd", bytecode=bytecode)
        >>> refund_transaction.sign(solver=refund_solver)
        <swap.providers.vapor.transaction.RefundTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not isinstance(solver, RefundSolver):
            raise TypeError(f"Solver must be Vapor RefundSolver, not {type(solver).__name__} type.")

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
        self._type = "vapor_refund_signed"
        return self

    def transaction_raw(self) -> str:
        """
        Get Vapor refund transaction raw.

        :returns: str -- Vapor refund transaction raw.

        >>> from swap.providers.vapor.transaction import RefundTransaction
        >>> refund_transaction: RefundTransaction = RefundTransaction(network="mainnet")
        >>> refund_transaction.build_transaction(address="vp1qk9vj4jaezlcnjdckds4fkm8fwv5kawmqwpnpvs", transaction_hash="37b36d7be5dfda0cc5dc3c918705464ff901dc5eadb6f4f049db03a679e02bfe", asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> refund_transaction.transaction_raw()
        "eyJmZWUiOiA1MDkwMDAsICJhZGRyZXNzIjogInZwMXF4ajNhazVwc3J3MnBocms1OGg4YWg1ZWNyaGNtd3cwNnZqNGgwZXB4ZmFjcjUzMHFoY2NzNHBjemdjIiwgImhhc2giOiAiNmQ5NjQyMjIyYmFmYjlkNjk2OGVlMmVlZDk4OGM4MzdiMWRhNTZmY2VjNmZkOTYzMjlmZmY4YzBkNTUxOGY5MiIsICJyYXciOiAiMDcwMTAwMDEwMTZiMDE2OWRmODJjZjdjNzkyNzc4NmE2OTU2OTM3NzQ0ZWU4MjM1NGM0ODFiMGYyMTFhYzUyYTVjMWQ3NDRjNGUzZTc4NjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBhZGUyMDQwMDAxMjIwMDIwMzRhM2RiNTAzMDFiOTQxYjhlZDQzZGNmZGJkMzM4MWRmMWI3MzlmYTY0YWI3N2U0MjY0ZjcwM2E0NWUwYmUzMTAxMDAwMTAxM2UwMDNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmI4YTRjMzA0MDExNjAwMTRiMTU5MmFjYmI5MTdmMTM5MzcxNjZjMmE5YjZjZTk3MzI5NmViYjYwMDAiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiNmIyNGM0NDM4OTY2MWY4YzU3MDE0NmVjNGNjOGQzYWQzZjJkN2YxNjA3MTM2MjBiZTc0MzgwZTQwYmMwNmMwYyJdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiBudWxsfV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJ2YXBvcl9yZWZ1bmRfdW5zaWduZWQifQ"
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")

        # Encode refund transaction raw
        if self._type == "vapor_refund_signed":
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
