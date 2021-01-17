#!/usr/bin/env python3

from base64 import b64encode, b64decode
from btcpy.structs.script import (
    Script, P2shScript
)
from btcpy.structs.transaction import (
    MutableTransaction, TxOut
)
from btcpy.structs.sig import P2shSolver
from btcpy.setup import setup
from typing import (
    Optional, Union
)

import json

from ...utils import clean_transaction_raw
from ...exceptions import (
    TransactionRawError, NetworkError, UnitError
)
from ..config import bitcoin as config
from .solver import (
    NormalSolver, FundSolver, ClaimSolver, RefundSolver
)
from .utils import (
    is_transaction_raw, is_network, amount_unit_converter
)


class Signature:
    """
    Bitcoin Signature.

    :param network: Bitcoin network, defaults to mainnet.
    :type network: str
    :param version: Bitcoin transaction version, defaults to 2.
    :type version: int

    :returns: Signature -- Bitcoin signature instance.

    .. note::
        Bitcoin has only two networks, ``mainnet`` and ``testnet``.
    """

    def __init__(self, network: str = config["network"], version: int = config["version"]):
        
        if not is_network(network=network):
            raise NetworkError(f"Invalid Bitcoin '{network}' network",
                               "choose only 'mainnet' or 'testnet' networks.")

        self._network: str = network
        self._mainnet: bool = True if network == "mainnet" else False
        self._version: int = version
        self._transaction: Optional[MutableTransaction] = None
        self._type: Optional[str] = None
        self._signed_raw: Optional[str] = None
        self._datas: dict = {}
        self._fee: int = 0

        setup(network, strict=True, force=True)

    def fee(self, unit: str = config["unit"]) -> Union[int, float]:
        """
        Get Bitcoin transaction fee.

        :param unit: Bitcoin unit, default to SATOSHI.
        :type unit: str

        :returns: int, float -- Bitcoin transaction fee.

        >>> from swap.providers.bitcoin.signature import Signature
        >>> from swap.providers.bitcoin.solver import FundSolver
        >>> unsigned_fund_transaction_raw = "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTA4MjVlMDBiYTU5NmFiMTExMjZjZDg5MjAzYjg4MmJjZTYwYTdkYjAxOWU1MTIxNzA1NmM0NzFmNTEwY2ZkODUwMDAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQ0Njk1MTI3YjFkMTdjNDU0ZjRiYWU5YzQxY2I4ZTNjZGI1ZTg5ZDI0ODdlYTVjMDEwMDAwMDAwMDAwMTk3NmE5MTQzM2VjYWIzZDY3ZjBlMmJkZTQzZTUyZjQxZWMxZWNiZGM3M2YxMWY4ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJ2YWx1ZSI6IDEwMDAwMCwgInR4X291dHB1dF9uIjogMCwgInNjcmlwdCI6ICI3NmE5MTQzM2VjYWIzZDY3ZjBlMmJkZTQzZTUyZjQxZWMxZWNiZGM3M2YxMWY4ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"
        >>> sender_root_xprivate_key = "xprv9s21ZrQH143K3XihXQBN8Uar2WBtrjSzK2oRDEGQ25pA2kKAADoQXaiiVXht163ZTrdtTXfM4GqNRE9gWQHky25BpvBQuuhNCM3SKwWTPNJ"
        >>> fund_solver = FundSolver(sender_root_xprivate_key)
        >>> signature = Signature("testnet")
        >>> signature.sign(unsigned_fund_transaction_raw, fund_solver)
        >>> signature.fee(unit="SATOSHI")
        678
        """

        if self._transaction is None:
            raise ValueError("Transaction is none, sign unsigned transaction raw first.")
        if unit not in ["BTC", "mBTC", "SATOSHI"]:
            raise UnitError("Invalid Bitcoin unit, choose only BTC, mBTC or SATOSHI units.")
        return self._fee if unit == "SATOSHI" else \
            amount_unit_converter(amount=self._fee, unit_from=f"SATOSHI2{unit}")

    def hash(self) -> str:
        """
        Get Bitcoin signature transaction hash.

        :returns: str -- Bitcoin signature transaction hash or transaction id.

        >>> from swap.providers.bitcoin.signature import Signature
        >>> from swap.providers.bitcoin.solver import ClaimSolver
        >>> unsigned_claim_transaction_raw = "eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTE4MjNmMzlhOGM1ZjZmMjc4NDVkZDEzYTY1ZTAzZmUyZWY1MTA4ZDIzNWU3YTM2ZWRiNmViMjY3YjA0NTljNWEwMDAwMDAwMDAwZmZmZmZmZmYwMWQwMjQwMDAwMDAwMDAwMDAxOTc2YTkxNDBlMjU5ZTA4ZjJlYzlmYzk5YTkyYjZmNjZmZGZjYjNjNzkxNGZkNjg4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsidmFsdWUiOiAxMDAwMCwgInR4X291dHB1dF9uIjogMCwgInNjcmlwdCI6ICJhOTE0OTQxOGZlZWQ0NjQ3ZTE1NmQ2NjYzZGIzZTBjZWY3YzA1MGQwMzg2Nzg3In0sICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX2NsYWltX3Vuc2lnbmVkIn0"
        >>> recipient_root_xprivate_key = "xprv9s21ZrQH143K4Kpce43z5guPyxLrFoc2i8aQAq835Zzp4Rt7i6nZaMCnVSDyHT6MnmJJGKHMrCUqaYpGojrug1ZN5qQDdShQffmkyv5xyUR"
        >>> bytecode = "63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a9140e259e08f2ec9fc99a92b6f66fdfcb3c7914fd6888ac6702e803b27576a91433ecab3d67f0e2bde43e52f41ec1ecbdc73f11f888ac68"
        >>> claim_solver = ClaimSolver(recipient_root_xprivate_key, "Hello Meheret!", bytecode)
        >>> signature = Signature("testnet")
        >>> signature.sign(unsigned_claim_transaction_raw, claim_solver)
        >>> signature.hash()
        "29c7ac0ec049687e1b952cefdaf2f1f52957e6f42f35826af21ec6bd3edf60ce"
        """

        if self._transaction is None:
            raise ValueError("Transaction is none, sign unsigned transaction raw first.")
        return self._transaction.txid

    def json(self) -> dict:
        """
        Get Bitcoin signature transaction json format.

        :returns: str -- Bitcoin signature transaction json format.

        >>> from swap.providers.bitcoin.signature import Signature
        >>> from swap.providers.bitcoin.solver import FundSolver
        >>> unsigned_fund_transaction_raw = "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTA4MjVlMDBiYTU5NmFiMTExMjZjZDg5MjAzYjg4MmJjZTYwYTdkYjAxOWU1MTIxNzA1NmM0NzFmNTEwY2ZkODUwMDAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQ0Njk1MTI3YjFkMTdjNDU0ZjRiYWU5YzQxY2I4ZTNjZGI1ZTg5ZDI0ODdlYTVjMDEwMDAwMDAwMDAwMTk3NmE5MTQzM2VjYWIzZDY3ZjBlMmJkZTQzZTUyZjQxZWMxZWNiZGM3M2YxMWY4ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJ2YWx1ZSI6IDEwMDAwMCwgInR4X291dHB1dF9uIjogMCwgInNjcmlwdCI6ICI3NmE5MTQzM2VjYWIzZDY3ZjBlMmJkZTQzZTUyZjQxZWMxZWNiZGM3M2YxMWY4ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"
        >>> sender_root_xprivate_key = "xprv9s21ZrQH143K3XihXQBN8Uar2WBtrjSzK2oRDEGQ25pA2kKAADoQXaiiVXht163ZTrdtTXfM4GqNRE9gWQHky25BpvBQuuhNCM3SKwWTPNJ"
        >>> fund_solver = FundSolver(sender_root_xprivate_key)
        >>> signature = Signature("testnet")
        >>> signature.sign(unsigned_fund_transaction_raw, fund_solver)
        >>> signature.json()
        {"hex": "02000000010825e00ba596ab11126cd89203b882bce60a7db019e51217056c471f510cfd85000000006b4830450221009ac6afb68728eee53050ea7a301b6fb836e13b782cd52c29be2f8b0cc71f4427022069671a0a3df14873cf9268e4054c4b177aff8da894641896669cfafa4be23c8a012102065e8cb5fa76699079860a450bddd0e37e0ad3dbf2ddfd01d7b600231e6cde8effffffff02102700000000000017a9144695127b1d17c454f4bae9c41cb8e3cdb5e89d2487ea5c0100000000001976a91433ecab3d67f0e2bde43e52f41ec1ecbdc73f11f888ac00000000", "txid": "29c7ac0ec049687e1b952cefdaf2f1f52957e6f42f35826af21ec6bd3edf60ce", "hash": "29c7ac0ec049687e1b952cefdaf2f1f52957e6f42f35826af21ec6bd3edf60ce", "size": 224, "vsize": 224, "version": 2, "locktime": 0, "vin": [{"txid": "85fd0c511f476c051712e519b07d0ae6bc82b80392d86c1211ab96a50be02508", "vout": 0, "scriptSig": {"asm": "30450221009ac6afb68728eee53050ea7a301b6fb836e13b782cd52c29be2f8b0cc71f4427022069671a0a3df14873cf9268e4054c4b177aff8da894641896669cfafa4be23c8a01 02065e8cb5fa76699079860a450bddd0e37e0ad3dbf2ddfd01d7b600231e6cde8e", "hex": "4830450221009ac6afb68728eee53050ea7a301b6fb836e13b782cd52c29be2f8b0cc71f4427022069671a0a3df14873cf9268e4054c4b177aff8da894641896669cfafa4be23c8a012102065e8cb5fa76699079860a450bddd0e37e0ad3dbf2ddfd01d7b600231e6cde8e"}, "sequence": "4294967295"}], "vout": [{"value": "0.00010000", "n": 0, "scriptPubKey": {"asm": "OP_HASH160 4695127b1d17c454f4bae9c41cb8e3cdb5e89d24 OP_EQUAL", "hex": "a9144695127b1d17c454f4bae9c41cb8e3cdb5e89d2487", "type": "p2sh", "address": "2MygRsRs6En1RCj8a88FfsK1QBeissBTswL"}}, {"value": "0.00089322", "n": 1, "scriptPubKey": {"asm": "OP_DUP OP_HASH160 33ecab3d67f0e2bde43e52f41ec1ecbdc73f11f8 OP_EQUALVERIFY OP_CHECKSIG", "hex": "76a91433ecab3d67f0e2bde43e52f41ec1ecbdc73f11f888ac", "type": "p2pkh", "address": "mkFWGt4hT11XS8dJKzzRFsTrqjjAwZfQAC"}}]}
        """

        if self._transaction is None:
            raise ValueError("Transaction is none, sign unsigned transaction raw first.")
        return self._transaction.to_json()

    def raw(self) -> str:
        """
        Get Bitcoin main transaction raw.

        :returns: str -- Bitcoin signature transaction raw.

        >>> from swap.providers.bitcoin.signature import Signature
        >>> from swap.providers.bitcoin.solver import RefundSolver
        >>> unsigned_refund_transaction_raw = "eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTE4MjNmMzlhOGM1ZjZmMjc4NDVkZDEzYTY1ZTAzZmUyZWY1MTA4ZDIzNWU3YTM2ZWRiNmViMjY3YjA0NTljNWEwMDAwMDAwMDAwZmZmZmZmZmYwMWQwMjQwMDAwMDAwMDAwMDAxOTc2YTkxNDMzZWNhYjNkNjdmMGUyYmRlNDNlNTJmNDFlYzFlY2JkYzczZjExZjg4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsidmFsdWUiOiAxMDAwMCwgInR4X291dHB1dF9uIjogMCwgInNjcmlwdCI6ICJhOTE0OTQxOGZlZWQ0NjQ3ZTE1NmQ2NjYzZGIzZTBjZWY3YzA1MGQwMzg2Nzg3In0sICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX3JlZnVuZF91bnNpZ25lZCJ9"
        >>> sender_root_xprivate_key = "xprv9s21ZrQH143K3XihXQBN8Uar2WBtrjSzK2oRDEGQ25pA2kKAADoQXaiiVXht163ZTrdtTXfM4GqNRE9gWQHky25BpvBQuuhNCM3SKwWTPNJ"
        >>> bytecode = "63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a9140e259e08f2ec9fc99a92b6f66fdfcb3c7914fd6888ac6702e803b27576a91433ecab3d67f0e2bde43e52f41ec1ecbdc73f11f888ac68"
        >>> refund_solver = RefundSolver(sender_root_xprivate_key, bytecode, 1000)
        >>> signature = Signature("testnet")
        >>> signature.sign(unsigned_refund_transaction_raw, refund_solver)
        >>> signature.raw()
        "02000000011823f39a8c5f6f27845dd13a65e03fe2ef5108d235e7a36edb6eb267b0459c5a00000000ca47304402207b7a2d1486258f0e59ae5d16fc0e369d45017a1016c85082ed362f36596970950220537c8762a5e03fef76bcfaacd451c36cde3d25bebe85d8e33a3fec5625b34183012102065e8cb5fa76699079860a450bddd0e37e0ad3dbf2ddfd01d7b600231e6cde8e004c5d63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a914acf8419eecab574c494febbe03fd07fdae7bf2f488ac6702e803b27576a9141d0f671c26a3ef7a865d1eda0fbd085e98adcc2388ac68e803000001d0240000000000001976a91433ecab3d67f0e2bde43e52f41ec1ecbdc73f11f888ac00000000"
        """

        if self._transaction is None:
            raise ValueError("Transaction is none, sign unsigned transaction raw first.")
        return self._transaction.hexlify()

    def type(self) -> str:
        """
        Get Bitcoin signature transaction type.

        :returns: str -- Bitcoin signature transaction type.

        >>> from swap.providers.bitcoin.signature import Signature
        >>> from swap.providers.bitcoin.solver import FundSolver
        >>> unsigned_fund_transaction_raw = "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTA4MjVlMDBiYTU5NmFiMTExMjZjZDg5MjAzYjg4MmJjZTYwYTdkYjAxOWU1MTIxNzA1NmM0NzFmNTEwY2ZkODUwMDAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQ0Njk1MTI3YjFkMTdjNDU0ZjRiYWU5YzQxY2I4ZTNjZGI1ZTg5ZDI0ODdlYTVjMDEwMDAwMDAwMDAwMTk3NmE5MTQzM2VjYWIzZDY3ZjBlMmJkZTQzZTUyZjQxZWMxZWNiZGM3M2YxMWY4ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJ2YWx1ZSI6IDEwMDAwMCwgInR4X291dHB1dF9uIjogMCwgInNjcmlwdCI6ICI3NmE5MTQzM2VjYWIzZDY3ZjBlMmJkZTQzZTUyZjQxZWMxZWNiZGM3M2YxMWY4ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"
        >>> sender_root_xprivate_key = "xprv9s21ZrQH143K3XihXQBN8Uar2WBtrjSzK2oRDEGQ25pA2kKAADoQXaiiVXht163ZTrdtTXfM4GqNRE9gWQHky25BpvBQuuhNCM3SKwWTPNJ"
        >>> fund_solver = FundSolver(sender_root_xprivate_key)
        >>> signature = Signature("testnet")
        >>> signature.sign(unsigned_fund_transaction_raw, fund_solver)
        >>> signature.type()
        "bitcoin_fund_signed"
        """

        if self._type is None:
            raise ValueError("Type is none, sign unsigned transaction raw first.")
        return self._type

    def sign(self, transaction_raw: str, solver: Union[NormalSolver, FundSolver, ClaimSolver, RefundSolver]) \
            -> Union["NormalSignature", "FundSignature", "ClaimSignature", "RefundSignature"]:
        """
        Sign unsigned transaction raw.

        :param transaction_raw: Bitcoin unsigned transaction raw.
        :type transaction_raw: str
        :param solver: Bitcoin solver
        :type solver: bitcoin.solver.NormalSolver, bitcoin.solver.FundSolver, bitcoin.solver.ClaimSolver, bitcoin.solver.RefundSolver

        :returns: NormalSignature, ClaimSignature, RefundSignature -- Bitcoin signature instance.

        >>> from swap.providers.bitcoin.signature import Signature
        >>> from swap.providers.bitcoin.solver import FundSolver
        >>> unsigned_fund_transaction_raw = "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTA4MjVlMDBiYTU5NmFiMTExMjZjZDg5MjAzYjg4MmJjZTYwYTdkYjAxOWU1MTIxNzA1NmM0NzFmNTEwY2ZkODUwMDAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQ0Njk1MTI3YjFkMTdjNDU0ZjRiYWU5YzQxY2I4ZTNjZGI1ZTg5ZDI0ODdlYTVjMDEwMDAwMDAwMDAwMTk3NmE5MTQzM2VjYWIzZDY3ZjBlMmJkZTQzZTUyZjQxZWMxZWNiZGM3M2YxMWY4ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJ2YWx1ZSI6IDEwMDAwMCwgInR4X291dHB1dF9uIjogMCwgInNjcmlwdCI6ICI3NmE5MTQzM2VjYWIzZDY3ZjBlMmJkZTQzZTUyZjQxZWMxZWNiZGM3M2YxMWY4ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"
        >>> sender_root_xprivate_key = "xprv9s21ZrQH143K3XihXQBN8Uar2WBtrjSzK2oRDEGQ25pA2kKAADoQXaiiVXht163ZTrdtTXfM4GqNRE9gWQHky25BpvBQuuhNCM3SKwWTPNJ"
        >>> fund_solver = FundSolver(sender_root_xprivate_key)
        >>> signature = Signature("testnet")
        >>> signature.sign(transaction_raw=unsigned_fund_transaction_raw, solver=fund_solver)
        <swap.providers.bitcoin.signature.FundSignature object at 0x0409DAF0>
        """

        if not is_transaction_raw(transaction_raw=transaction_raw):
            raise TransactionRawError("Invalid Bitcoin unsigned transaction raw.")

        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

        self._type = loaded_transaction_raw["type"]
        if loaded_transaction_raw["type"] == "bitcoin_normal_unsigned":
            return NormalSignature(
                network=self._network, version=self._version
            ).sign(
                transaction_raw=transaction_raw, solver=solver
            )
        elif loaded_transaction_raw["type"] == "bitcoin_fund_unsigned":
            return FundSignature(
                network=self._network, version=self._version
            ).sign(
                transaction_raw=transaction_raw, solver=solver
            )
        elif loaded_transaction_raw["type"] == "bitcoin_claim_unsigned":
            return ClaimSignature(
                network=self._network, version=self._version
            ).sign(
                transaction_raw=transaction_raw, solver=solver
            )
        elif loaded_transaction_raw["type"] == "bitcoin_refund_unsigned":
            return RefundSignature(
                network=self._network, version=self._version
            ).sign(
                transaction_raw=transaction_raw, solver=solver
            )

    def datas(self) -> dict:
        return self._datas

    def transaction_raw(self) -> str:
        """
        Get Bitcoin transaction raw.

        :returns: str -- Bitcoin transaction raw.

        >>> from swap.providers.bitcoin.signature import Signature
        >>> from swap.providers.bitcoin.solver import FundSolver
        >>> unsigned_fund_transaction_raw = "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTA4MjVlMDBiYTU5NmFiMTExMjZjZDg5MjAzYjg4MmJjZTYwYTdkYjAxOWU1MTIxNzA1NmM0NzFmNTEwY2ZkODUwMDAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQ0Njk1MTI3YjFkMTdjNDU0ZjRiYWU5YzQxY2I4ZTNjZGI1ZTg5ZDI0ODdlYTVjMDEwMDAwMDAwMDAwMTk3NmE5MTQzM2VjYWIzZDY3ZjBlMmJkZTQzZTUyZjQxZWMxZWNiZGM3M2YxMWY4ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJ2YWx1ZSI6IDEwMDAwMCwgInR4X291dHB1dF9uIjogMCwgInNjcmlwdCI6ICI3NmE5MTQzM2VjYWIzZDY3ZjBlMmJkZTQzZTUyZjQxZWMxZWNiZGM3M2YxMWY4ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"
        >>> sender_root_xprivate_key = "xprv9s21ZrQH143K3XihXQBN8Uar2WBtrjSzK2oRDEGQ25pA2kKAADoQXaiiVXht163ZTrdtTXfM4GqNRE9gWQHky25BpvBQuuhNCM3SKwWTPNJ"
        >>> fund_solver = FundSolver(sender_root_xprivate_key)
        >>> signature = Signature("testnet")
        >>> signature.sign(unsigned_fund_transaction_raw, fund_solver)
        >>> signature.transaction_raw()
        "eyJyYXciOiAiMDIwMDAwMDAwMTA4MjVlMDBiYTU5NmFiMTExMjZjZDg5MjAzYjg4MmJjZTYwYTdkYjAxOWU1MTIxNzA1NmM0NzFmNTEwY2ZkODUwMDAwMDAwMDZiNDgzMDQ1MDIyMTAwOWFjNmFmYjY4NzI4ZWVlNTMwNTBlYTdhMzAxYjZmYjgzNmUxM2I3ODJjZDUyYzI5YmUyZjhiMGNjNzFmNDQyNzAyMjA2OTY3MWEwYTNkZjE0ODczY2Y5MjY4ZTQwNTRjNGIxNzdhZmY4ZGE4OTQ2NDE4OTY2NjljZmFmYTRiZTIzYzhhMDEyMTAyMDY1ZThjYjVmYTc2Njk5MDc5ODYwYTQ1MGJkZGQwZTM3ZTBhZDNkYmYyZGRmZDAxZDdiNjAwMjMxZTZjZGU4ZWZmZmZmZmZmMDIxMDI3MDAwMDAwMDAwMDAwMTdhOTE0NDY5NTEyN2IxZDE3YzQ1NGY0YmFlOWM0MWNiOGUzY2RiNWU4OWQyNDg3ZWE1YzAxMDAwMDAwMDAwMDE5NzZhOTE0MzNlY2FiM2Q2N2YwZTJiZGU0M2U1MmY0MWVjMWVjYmRjNzNmMTFmODg4YWMwMDAwMDAwMCIsICJmZWUiOiA2NzgsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfc2lnbmVkIn0"
        """

        if self._signed_raw is None:
            raise ValueError("There is no signed data, sign unsigned transaction raw first.")
        return clean_transaction_raw(self._signed_raw)


class NormalSignature(Signature):
    """
    Bitcoin Normal signature.

    :param network: Bitcoin network, defaults to mainnet.
    :type network: str
    :param version: Bitcoin transaction version, defaults to 2.
    :type version: int

    :returns: NormalSignature -- Bitcoin normal signature instance.
    """

    def __init__(self, network: str = config["network"], version: int = config["version"]):
        super().__init__(network=network, version=version)

    def sign(self, transaction_raw: str, solver: NormalSolver) -> "NormalSignature":
        """
        Sign unsigned normal transaction raw.

        :param transaction_raw: Bitcoin unsigned normal transaction raw.
        :type transaction_raw: str
        :param solver: Bitcoin normal solver.
        :type solver: bitcoin.solver.NormalSolver

        :returns: NormalSignature -- Bitcoin normal signature instance.

        >>> from swap.providers.bitcoin.signature import Signature
        >>> from swap.providers.bitcoin.solver import NormalSolver
        >>> unsigned_normal_transaction_raw = "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTA4MjVlMDBiYTU5NmFiMTExMjZjZDg5MjAzYjg4MmJjZTYwYTdkYjAxOWU1MTIxNzA1NmM0NzFmNTEwY2ZkODUwMDAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQ0Njk1MTI3YjFkMTdjNDU0ZjRiYWU5YzQxY2I4ZTNjZGI1ZTg5ZDI0ODdlYTVjMDEwMDAwMDAwMDAwMTk3NmE5MTQzM2VjYWIzZDY3ZjBlMmJkZTQzZTUyZjQxZWMxZWNiZGM3M2YxMWY4ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJ2YWx1ZSI6IDEwMDAwMCwgInR4X291dHB1dF9uIjogMCwgInNjcmlwdCI6ICI3NmE5MTQzM2VjYWIzZDY3ZjBlMmJkZTQzZTUyZjQxZWMxZWNiZGM3M2YxMWY4ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"
        >>> sender_root_xprivate_key = "xprv9s21ZrQH143K3XihXQBN8Uar2WBtrjSzK2oRDEGQ25pA2kKAADoQXaiiVXht163ZTrdtTXfM4GqNRE9gWQHky25BpvBQuuhNCM3SKwWTPNJ"
        >>> normal_solver = NormalSolver(sender_root_xprivate_key)
        >>> normal_signature = NormalSignature("testnet")
        >>> normal_signature.sign(unsigned_normal_transaction_raw, normal_solver)
        <swap.providers.bitcoin.signature.NormalSignature object at 0x0409DAF0>
        """

        if not is_transaction_raw(transaction_raw=transaction_raw):
            raise TransactionRawError("Invalid Bitcoin unsigned transaction raw.")

        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

        if not loaded_transaction_raw["type"] == "bitcoin_normal_unsigned":
            raise TypeError(f"Invalid Bitcoin normal unsigned transaction raw type, "
                            f"you can't sign {loaded_transaction_raw['type']} type by using normal signature.")

        # Check parameter instances
        if not isinstance(solver, NormalSolver):
            raise TypeError(f"Solver must be Bitcoin NormalSolver, not {type(solver).__name__} type.")

        # Set transaction fee, type, network and transaction
        self._fee, self._type, self._datas, self._network, self._transaction = (
            loaded_transaction_raw["fee"], loaded_transaction_raw["type"], loaded_transaction_raw["datas"],
            loaded_transaction_raw["network"], MutableTransaction.unhexlify(loaded_transaction_raw["raw"])
        )

        # Organize outputs
        outputs = []
        for output in loaded_transaction_raw["outputs"]:
            outputs.append(TxOut(
                value=output["value"],
                n=output["tx_output_n"],
                script_pubkey=Script.unhexlify(
                    hex_string=output["script"]
                )
            ))

        # Sign normal transaction
        self._transaction.spend(
            txouts=outputs,
            solvers=[solver.solve(network=self._network) for _ in outputs]
        )

        # Encode normal transaction raw
        self._type = "bitcoin_normal_signed"
        self._signed_raw = b64encode(str(json.dumps(dict(
            raw=self._transaction.hexlify(),
            fee=self._fee,
            network=self._network,
            type=self._type,
            datas=self._datas
        ))).encode()).decode()
        return self


class FundSignature(Signature):
    """
    Bitcoin Fund signature.

    :param network: Bitcoin network, defaults to mainnet.
    :type network: str
    :param version: Bitcoin transaction version, defaults to 2.
    :type version: int

    :returns: FundSignature -- Bitcoin fund signature instance.
    """

    def __init__(self, network: str = config["network"], version: int = config["version"]):
        super().__init__(network=network, version=version)

    def sign(self, transaction_raw: str, solver: FundSolver) -> "FundSignature":
        """
        Sign unsigned fund transaction raw.

        :param transaction_raw: Bitcoin unsigned fund transaction raw.
        :type transaction_raw: str
        :param solver: Bitcoin fund solver.
        :type solver: bitcoin.solver.FundSolver

        :returns: FundSignature -- Bitcoin fund signature instance.

        >>> from swap.providers.bitcoin.signature import Signature
        >>> from swap.providers.bitcoin.solver import FundSolver
        >>> unsigned_fund_transaction_raw = "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTA4MjVlMDBiYTU5NmFiMTExMjZjZDg5MjAzYjg4MmJjZTYwYTdkYjAxOWU1MTIxNzA1NmM0NzFmNTEwY2ZkODUwMDAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQ0Njk1MTI3YjFkMTdjNDU0ZjRiYWU5YzQxY2I4ZTNjZGI1ZTg5ZDI0ODdlYTVjMDEwMDAwMDAwMDAwMTk3NmE5MTQzM2VjYWIzZDY3ZjBlMmJkZTQzZTUyZjQxZWMxZWNiZGM3M2YxMWY4ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJ2YWx1ZSI6IDEwMDAwMCwgInR4X291dHB1dF9uIjogMCwgInNjcmlwdCI6ICI3NmE5MTQzM2VjYWIzZDY3ZjBlMmJkZTQzZTUyZjQxZWMxZWNiZGM3M2YxMWY4ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"
        >>> sender_root_xprivate_key = "xprv9s21ZrQH143K3XihXQBN8Uar2WBtrjSzK2oRDEGQ25pA2kKAADoQXaiiVXht163ZTrdtTXfM4GqNRE9gWQHky25BpvBQuuhNCM3SKwWTPNJ"
        >>> fund_solver = FundSolver(sender_root_xprivate_key)
        >>> fund_signature = FundSignature("testnet")
        >>> fund_signature.sign(unsigned_fund_transaction_raw, fund_solver)
        <swap.providers.bitcoin.signature.FundSignature object at 0x0409DAF0>
        """

        if not is_transaction_raw(transaction_raw=transaction_raw):
            raise TransactionRawError("Invalid Bitcoin unsigned transaction raw.")

        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

        if not loaded_transaction_raw["type"] == "bitcoin_fund_unsigned":
            raise TypeError(f"Invalid Bitcoin fund unsigned transaction raw type, "
                            f"you can't sign {loaded_transaction_raw['type']} type by using fund signature.")

        # Check parameter instances
        if not isinstance(solver, FundSolver):
            raise TypeError(f"Solver must be Bitcoin FundSolver, not {type(solver).__name__} type.")

        # Set transaction fee, type, network and transaction
        self._fee, self._type, self._datas, self._network, self._transaction = (
            loaded_transaction_raw["fee"], loaded_transaction_raw["type"], loaded_transaction_raw["datas"],
            loaded_transaction_raw["network"], MutableTransaction.unhexlify(loaded_transaction_raw["raw"])
        )

        # Organize outputs
        outputs = []
        for output in loaded_transaction_raw["outputs"]:
            outputs.append(TxOut(
                value=output["value"],
                n=output["tx_output_n"],
                script_pubkey=Script.unhexlify(
                    hex_string=output["script"]
                )
            ))

        # Sign fund transaction
        self._transaction.spend(
            txouts=outputs,
            solvers=[solver.solve(network=self._network) for _ in outputs]
        )

        # Encode fund transaction raw
        self._type = "bitcoin_fund_signed"
        self._signed_raw = b64encode(str(json.dumps(dict(
            raw=self._transaction.hexlify(),
            fee=self._fee,
            network=self._network,
            type=self._type,
            datas=self._datas
        ))).encode()).decode()
        return self


class ClaimSignature(Signature):
    """
    Bitcoin Claim signature.

    :param network: Bitcoin network, defaults to mainnet.
    :type network: str
    :param version: Bitcoin transaction version, defaults to 2.
    :type version: int

    :returns: ClaimSignature -- Bitcoin claim signature instance.
    """

    def __init__(self, network: str = config["network"], version: int = config["version"]):
        super().__init__(network=network, version=version)

    def sign(self, transaction_raw: str, solver: ClaimSolver) -> "ClaimSignature":
        """
        Sign unsigned claim transaction raw.

        :param transaction_raw: Bitcoin unsigned claim transaction raw.
        :type transaction_raw: str
        :param solver: Bitcoin claim solver.
        :type solver: bitcoin.solver.ClaimSolver

        :returns: ClaimSignature -- Bitcoin claim signature instance.

        >>> from swap.providers.bitcoin.signature import ClaimSignature
        >>> from swap.providers.bitcoin.solver import ClaimSolver
        >>> unsigned_claim_transaction_raw = "eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTE4MjNmMzlhOGM1ZjZmMjc4NDVkZDEzYTY1ZTAzZmUyZWY1MTA4ZDIzNWU3YTM2ZWRiNmViMjY3YjA0NTljNWEwMDAwMDAwMDAwZmZmZmZmZmYwMWQwMjQwMDAwMDAwMDAwMDAxOTc2YTkxNDBlMjU5ZTA4ZjJlYzlmYzk5YTkyYjZmNjZmZGZjYjNjNzkxNGZkNjg4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsidmFsdWUiOiAxMDAwMCwgInR4X291dHB1dF9uIjogMCwgInNjcmlwdCI6ICJhOTE0OTQxOGZlZWQ0NjQ3ZTE1NmQ2NjYzZGIzZTBjZWY3YzA1MGQwMzg2Nzg3In0sICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX2NsYWltX3Vuc2lnbmVkIn0"
        >>> recipient_root_xprivate_key = "xprv9s21ZrQH143K4Kpce43z5guPyxLrFoc2i8aQAq835Zzp4Rt7i6nZaMCnVSDyHT6MnmJJGKHMrCUqaYpGojrug1ZN5qQDdShQffmkyv5xyUR"
        >>> bytecode = "63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a9140e259e08f2ec9fc99a92b6f66fdfcb3c7914fd6888ac6702e803b27576a91433ecab3d67f0e2bde43e52f41ec1ecbdc73f11f888ac68"
        >>> claim_solver = ClaimSolver(recipient_root_xprivate_key, "Hello Meheret!", bytecode)
        >>> claim_signature = ClaimSignature("testnet")
        >>> claim_signature.sign(transaction_raw=unsigned_claim_transaction_raw, solver=claim_solver)
        <swap.providers.bitcoin.signature.ClaimSignature object at 0x0409DAF0>
        """

        if not is_transaction_raw(transaction_raw=transaction_raw):
            raise TransactionRawError("Invalid Bitcoin unsigned transaction raw.")

        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

        if not loaded_transaction_raw["type"] == "bitcoin_claim_unsigned":
            raise TypeError(f"Invalid Bitcoin claim unsigned transaction raw type, "
                            f"you can't sign {loaded_transaction_raw['type']} type by using claim signature.")

        # Check parameter instances
        if not isinstance(solver, ClaimSolver):
            raise TypeError(f"Solver must be Bitcoin ClaimSolver, not {type(solver).__name__} type.")

        # Set transaction fee, type, network and transaction
        self._fee, self._type, self._datas, self._network, self._transaction = (
            loaded_transaction_raw["fee"], loaded_transaction_raw["type"], loaded_transaction_raw["datas"],
            loaded_transaction_raw["network"], MutableTransaction.unhexlify(loaded_transaction_raw["raw"])
        )

        # Sign claim transaction
        self._transaction.spend([TxOut(
            value=loaded_transaction_raw["outputs"]["value"],
            n=loaded_transaction_raw["outputs"]["tx_output_n"],
            script_pubkey=P2shScript.unhexlify(
                hex_string=loaded_transaction_raw["outputs"]["script"]
            )
        )], [P2shSolver(
            redeem_script=solver.witness(
                network=self._network
            ),
            redeem_script_solver=solver.solve(
                network=self._network
            )
        )])

        # Encode claim transaction raw
        self._type = "bitcoin_claim_signed"
        self._signed_raw = b64encode(str(json.dumps(dict(
            raw=self._transaction.hexlify(),
            fee=self._fee,
            network=self._network,
            type=self._type,
            datas=self._datas
        ))).encode()).decode()
        return self


class RefundSignature(Signature):
    """
    Bitcoin Refund signature.

    :param network: Bitcoin network, defaults to mainnet.
    :type network: str
    :param version: Bitcoin transaction version, defaults to 2.
    :type version: int

    :returns: RefundSignature -- Bitcoin refund signature instance.
    """

    def __init__(self, network: str = config["network"], version: int = config["version"]):
        super().__init__(network=network, version=version)

    def sign(self, transaction_raw: str, solver: RefundSolver) -> "RefundSignature":
        """
        Sign unsigned refund transaction raw.

        :param transaction_raw: Bitcoin unsigned refund transaction raw.
        :type transaction_raw: str
        :param solver: Bitcoin refund solver.
        :type solver: bitcoin.solver.RefundSolver
        :returns:  RefundSignature -- Bitcoin refund signature instance.

        >>> from swap.providers.bitcoin.signature import RefundSignature
        >>> from swap.providers.bitcoin.solver import RefundSolver
        >>> unsigned_refund_transaction_raw = "eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTE4MjNmMzlhOGM1ZjZmMjc4NDVkZDEzYTY1ZTAzZmUyZWY1MTA4ZDIzNWU3YTM2ZWRiNmViMjY3YjA0NTljNWEwMDAwMDAwMDAwZmZmZmZmZmYwMWQwMjQwMDAwMDAwMDAwMDAxOTc2YTkxNDMzZWNhYjNkNjdmMGUyYmRlNDNlNTJmNDFlYzFlY2JkYzczZjExZjg4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsidmFsdWUiOiAxMDAwMCwgInR4X291dHB1dF9uIjogMCwgInNjcmlwdCI6ICJhOTE0OTQxOGZlZWQ0NjQ3ZTE1NmQ2NjYzZGIzZTBjZWY3YzA1MGQwMzg2Nzg3In0sICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX3JlZnVuZF91bnNpZ25lZCJ9"
        >>> sender_root_xprivate_key = "xprv9s21ZrQH143K3XihXQBN8Uar2WBtrjSzK2oRDEGQ25pA2kKAADoQXaiiVXht163ZTrdtTXfM4GqNRE9gWQHky25BpvBQuuhNCM3SKwWTPNJ"
        >>> bytecode = "63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a9140e259e08f2ec9fc99a92b6f66fdfcb3c7914fd6888ac6702e803b27576a91433ecab3d67f0e2bde43e52f41ec1ecbdc73f11f888ac68"
        >>> refund_solver = RefundSolver(sender_root_xprivate_key, bytecode, 1000)
        >>> refund_signature = RefundSignature("testnet")
        >>> refund_signature.sign(transaction_raw=unsigned_refund_transaction_raw, solver=refund_solver)
        <swap.providers.bitcoin.signature.RefundSignature object at 0x0409DAF0>
        """

        if not is_transaction_raw(transaction_raw=transaction_raw):
            raise TransactionRawError("Invalid Bitcoin unsigned transaction raw.")

        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

        if not loaded_transaction_raw["type"] == "bitcoin_refund_unsigned":
            raise TypeError(f"Invalid Bitcoin refund unsigned transaction raw type, "
                            f"you can't sign {loaded_transaction_raw['type']} type by using refund signature.")

        # Check parameter instances
        if not isinstance(solver, RefundSolver):
            raise TypeError(f"Solver must be Bitcoin RefundSolver, not {type(solver).__name__} type.")

        # Set transaction fee, type, network and transaction
        self._fee, self._type, self._datas, self._network, self._transaction = (
            loaded_transaction_raw["fee"], loaded_transaction_raw["type"], loaded_transaction_raw["datas"],
            loaded_transaction_raw["network"], MutableTransaction.unhexlify(loaded_transaction_raw["raw"])
        )

        # Sign refund transaction
        self._transaction.spend([TxOut(
            value=loaded_transaction_raw["outputs"]["value"],
            n=loaded_transaction_raw["outputs"]["tx_output_n"],
            script_pubkey=P2shScript.unhexlify(
                hex_string=loaded_transaction_raw["outputs"]["script"]
            )
        )], [P2shSolver(
            redeem_script=solver.witness(
                network=self._network
            ),
            redeem_script_solver=solver.solve(
                network=self._network
            )
        )])

        # Encode refund transaction raw
        self._type = "bitcoin_refund_signed"
        self._signed_raw = b64encode(str(json.dumps(dict(
            raw=self._transaction.hexlify(),
            fee=self._fee,
            network=self._network,
            type=self._type,
            datas=self._datas
        ))).encode()).decode()
        return self
