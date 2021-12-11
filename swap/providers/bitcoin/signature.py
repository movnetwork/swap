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
    NormalSolver, FundSolver, WithdrawSolver, RefundSolver
)
from .utils import (
    is_transaction_raw, is_network, amount_unit_converter
)


class Signature:
    """
    Bitcoin Signature.

    :param network: Bitcoin network, defaults to ``mainnet``.
    :type network: str
    :param version: Bitcoin transaction version, defaults to ``2``.
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
        self._fee: int = 0

        setup(network, strict=True, force=True)

    def fee(self, unit: str = config["unit"]) -> Union[int, float]:
        """
        Get Bitcoin transaction fee.

        :param unit: Bitcoin unit, default to ``Satoshi``.
        :type unit: str

        :returns: int, float -- Bitcoin transaction fee.

        >>> from swap.providers.bitcoin.signature import Signature
        >>> from swap.providers.bitcoin.solver import FundSolver
        >>> unsigned_fund_transaction_raw: str = "eyJmZWUiOiAxMTIyLCAicmF3IjogIjAyMDAwMDAwMDIzMWZiNzZhMGMzOGQ1NzM4MWIzMTEwZTRmNWVlOWI1MjgxZGNmMmZiZTJmZTI1NjkyNjZiNzUxMDExZDIxMWEyMDEwMDAwMDAwMGZmZmZmZmZmMDgwYjgyZWVjMzMyOTk2YTQyMmFlNGYwODBmNzRlNTNmZDJjYTRmMDcwMTFkNDdjNTkwODUzZTFlMzA1ZmUxMTAxMDAwMDAwMDBmZmZmZmZmZjAyYTA4NjAxMDAwMDAwMDAwMDE3YTkxNGM4Yzc3YTliNDNlZTJiZGYxYTA3YzQ4Njk5ODMzZDc2NjhiZjI2NGM4NzMyOWMwZDAwMDAwMDAwMDAxOTc2YTkxNGUwMGZmMmE2NDBiN2NlMmQzMzY4NjA3MzkxNjk0ODdhNTdmODRiMTU4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IFt7InZhbHVlIjogOTQzMzAsICJ0eF9vdXRwdXRfbiI6IDEsICJzY3JpcHQiOiAiNzZhOTE0ZTAwZmYyYTY0MGI3Y2UyZDMzNjg2MDczOTE2OTQ4N2E1N2Y4NGIxNTg4YWMifSwgeyJ2YWx1ZSI6IDg5ODc0NiwgInR4X291dHB1dF9uIjogMSwgInNjcmlwdCI6ICI3NmE5MTRlMDBmZjJhNjQwYjdjZTJkMzM2ODYwNzM5MTY5NDg3YTU3Zjg0YjE1ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="tprv8ZgxMBicQKsPeMHMJAc6uWGYiGqi1MVM2ybmzXL2TAoDpQe85uyDpdT7mv7Nhdu5rTCBEKLZsd9KyP2LQZJzZTvgVQvENArgU8e6DoYBiXf")
        >>> signature: Signature = Signature(network="testnet")
        >>> signature.sign(transaction_raw=unsigned_fund_transaction_raw, solver=fund_solver)
        >>> signature.fee(unit="Satoshi")
        678
        """

        if self._transaction is None:
            raise ValueError("Transaction is none, sign unsigned transaction raw first.")
        if unit not in ["BTC", "mBTC", "Satoshi"]:
            raise UnitError("Invalid Bitcoin unit, choose only BTC, mBTC or Satoshi units.")
        return self._fee if unit == "Satoshi" else \
            amount_unit_converter(amount=self._fee, unit_from=f"Satoshi2{unit}")

    def hash(self) -> str:
        """
        Get Bitcoin signature transaction hash.

        :returns: str -- Bitcoin signature transaction hash or transaction id.

        >>> from swap.providers.bitcoin.signature import Signature
        >>> from swap.providers.bitcoin.solver import WithdrawSolver
        >>> unsigned_withdraw_transaction_raw: str = "eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTMxZmI3NmEwYzM4ZDU3MzgxYjMxMTBlNGY1ZWU5YjUyODFkY2YyZmJlMmZlMjU2OTI2NmI3NTEwMTFkMjExYTIwMDAwMDAwMDAwZmZmZmZmZmYwMTYwODQwMTAwMDAwMDAwMDAxOTc2YTkxNDBhMGE2NTkwZTZiYTRiNDgxMThkMjFiODY4MTI2MTUyMTllY2U3NmI4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsidmFsdWUiOiAxMDAwMDAsICJ0eF9vdXRwdXRfbiI6IDAsICJzY3JpcHQiOiAiYTkxNGM4Yzc3YTliNDNlZTJiZGYxYTA3YzQ4Njk5ODMzZDc2NjhiZjI2NGM4NyJ9LCAibmV0d29yayI6ICJ0ZXN0bmV0IiwgInR5cGUiOiAiYml0Y29pbl93aXRoZHJhd191bnNpZ25lZCJ9"
        >>> bytecode: str = "63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a9140a0a6590e6ba4b48118d21b86812615219ece76b88ac67040ec4d660b17576a914e00ff2a640b7ce2d336860739169487a57f84b1588ac68"
        >>> withdraw_solver: WithdrawSolver = WithdrawSolver(xprivate_key="tprv8ZgxMBicQKsPf949JcuVFLXPJ5m4VKe33gVX3FYVZYVHr2dChU8K66aEQcPdHpUgACq5GQu81Z4e3QN1vxCrV4pxcUcXHoRTamXBRaPdJhW", secret_key="Hello Meheret!", bytecode=bytecode)
        >>> signature: Signature = Signature(network="testnet")
        >>> signature.sign(transaction_raw=unsigned_withdraw_transaction_raw, solver=withdraw_solver)
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
        >>> unsigned_fund_transaction_raw: str = "eyJmZWUiOiAxMTIyLCAicmF3IjogIjAyMDAwMDAwMDIzMWZiNzZhMGMzOGQ1NzM4MWIzMTEwZTRmNWVlOWI1MjgxZGNmMmZiZTJmZTI1NjkyNjZiNzUxMDExZDIxMWEyMDEwMDAwMDAwMGZmZmZmZmZmMDgwYjgyZWVjMzMyOTk2YTQyMmFlNGYwODBmNzRlNTNmZDJjYTRmMDcwMTFkNDdjNTkwODUzZTFlMzA1ZmUxMTAxMDAwMDAwMDBmZmZmZmZmZjAyYTA4NjAxMDAwMDAwMDAwMDE3YTkxNGM4Yzc3YTliNDNlZTJiZGYxYTA3YzQ4Njk5ODMzZDc2NjhiZjI2NGM4NzMyOWMwZDAwMDAwMDAwMDAxOTc2YTkxNGUwMGZmMmE2NDBiN2NlMmQzMzY4NjA3MzkxNjk0ODdhNTdmODRiMTU4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IFt7InZhbHVlIjogOTQzMzAsICJ0eF9vdXRwdXRfbiI6IDEsICJzY3JpcHQiOiAiNzZhOTE0ZTAwZmYyYTY0MGI3Y2UyZDMzNjg2MDczOTE2OTQ4N2E1N2Y4NGIxNTg4YWMifSwgeyJ2YWx1ZSI6IDg5ODc0NiwgInR4X291dHB1dF9uIjogMSwgInNjcmlwdCI6ICI3NmE5MTRlMDBmZjJhNjQwYjdjZTJkMzM2ODYwNzM5MTY5NDg3YTU3Zjg0YjE1ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="tprv8ZgxMBicQKsPeMHMJAc6uWGYiGqi1MVM2ybmzXL2TAoDpQe85uyDpdT7mv7Nhdu5rTCBEKLZsd9KyP2LQZJzZTvgVQvENArgU8e6DoYBiXf")
        >>> signature: Signature = Signature(network="testnet")
        >>> signature.sign(transaction_raw=unsigned_fund_transaction_raw, solver=fund_solver)
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
        >>> unsigned_refund_transaction_raw: str = "eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTMxZmI3NmEwYzM4ZDU3MzgxYjMxMTBlNGY1ZWU5YjUyODFkY2YyZmJlMmZlMjU2OTI2NmI3NTEwMTFkMjExYTIwMDAwMDAwMDAwZmZmZmZmZmYwMTYwODQwMTAwMDAwMDAwMDAxOTc2YTkxNGUwMGZmMmE2NDBiN2NlMmQzMzY4NjA3MzkxNjk0ODdhNTdmODRiMTU4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsidmFsdWUiOiAxMDAwMDAsICJ0eF9vdXRwdXRfbiI6IDAsICJzY3JpcHQiOiAiYTkxNGM4Yzc3YTliNDNlZTJiZGYxYTA3YzQ4Njk5ODMzZDc2NjhiZjI2NGM4NyJ9LCAibmV0d29yayI6ICJ0ZXN0bmV0IiwgInR5cGUiOiAiYml0Y29pbl9yZWZ1bmRfdW5zaWduZWQifQ"
        >>> bytecode: str = "63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a9140a0a6590e6ba4b48118d21b86812615219ece76b88ac67040ec4d660b17576a914e00ff2a640b7ce2d336860739169487a57f84b1588ac68"
        >>> refund_solver: RefundSolver = RefundSolver(xprivate_key="tprv8ZgxMBicQKsPeMHMJAc6uWGYiGqi1MVM2ybmzXL2TAoDpQe85uyDpdT7mv7Nhdu5rTCBEKLZsd9KyP2LQZJzZTvgVQvENArgU8e6DoYBiXf", bytecode=bytecode, endtime=1624687630)
        >>> signature: Signature = Signature(network="testnet")
        >>> signature.sign(transaction_raw=unsigned_refund_transaction_raw, solver=refund_solver)
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
        >>> unsigned_fund_transaction_raw: str = "eyJmZWUiOiAxMTIyLCAicmF3IjogIjAyMDAwMDAwMDIzMWZiNzZhMGMzOGQ1NzM4MWIzMTEwZTRmNWVlOWI1MjgxZGNmMmZiZTJmZTI1NjkyNjZiNzUxMDExZDIxMWEyMDEwMDAwMDAwMGZmZmZmZmZmMDgwYjgyZWVjMzMyOTk2YTQyMmFlNGYwODBmNzRlNTNmZDJjYTRmMDcwMTFkNDdjNTkwODUzZTFlMzA1ZmUxMTAxMDAwMDAwMDBmZmZmZmZmZjAyYTA4NjAxMDAwMDAwMDAwMDE3YTkxNGM4Yzc3YTliNDNlZTJiZGYxYTA3YzQ4Njk5ODMzZDc2NjhiZjI2NGM4NzMyOWMwZDAwMDAwMDAwMDAxOTc2YTkxNGUwMGZmMmE2NDBiN2NlMmQzMzY4NjA3MzkxNjk0ODdhNTdmODRiMTU4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IFt7InZhbHVlIjogOTQzMzAsICJ0eF9vdXRwdXRfbiI6IDEsICJzY3JpcHQiOiAiNzZhOTE0ZTAwZmYyYTY0MGI3Y2UyZDMzNjg2MDczOTE2OTQ4N2E1N2Y4NGIxNTg4YWMifSwgeyJ2YWx1ZSI6IDg5ODc0NiwgInR4X291dHB1dF9uIjogMSwgInNjcmlwdCI6ICI3NmE5MTRlMDBmZjJhNjQwYjdjZTJkMzM2ODYwNzM5MTY5NDg3YTU3Zjg0YjE1ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="tprv8ZgxMBicQKsPeMHMJAc6uWGYiGqi1MVM2ybmzXL2TAoDpQe85uyDpdT7mv7Nhdu5rTCBEKLZsd9KyP2LQZJzZTvgVQvENArgU8e6DoYBiXf")
        >>> signature: Signature = Signature(network="testnet")
        >>> signature.sign(transaction_raw=unsigned_fund_transaction_raw, solver=fund_solver)
        >>> signature.type()
        "bitcoin_fund_signed"
        """

        if self._type is None:
            raise ValueError("Type is none, sign unsigned transaction raw first.")
        return self._type

    def sign(self, transaction_raw: str, solver: Union[NormalSolver, FundSolver, WithdrawSolver, RefundSolver]) \
            -> Union["NormalSignature", "FundSignature", "WithdrawSignature", "RefundSignature"]:
        """
        Sign unsigned transaction raw.

        :param transaction_raw: Bitcoin unsigned transaction raw.
        :type transaction_raw: str
        :param solver: Bitcoin solver
        :type solver: bitcoin.solver.NormalSolver, bitcoin.solver.FundSolver, bitcoin.solver.WithdrawSolver, bitcoin.solver.RefundSolver

        :returns: NormalSignature, FundSignature, WithdrawSignature, RefundSignature -- Bitcoin signature instance.

        >>> from swap.providers.bitcoin.signature import Signature
        >>> from swap.providers.bitcoin.solver import FundSolver
        >>> unsigned_fund_transaction_raw: str = "eyJmZWUiOiAxMTIyLCAicmF3IjogIjAyMDAwMDAwMDIzMWZiNzZhMGMzOGQ1NzM4MWIzMTEwZTRmNWVlOWI1MjgxZGNmMmZiZTJmZTI1NjkyNjZiNzUxMDExZDIxMWEyMDEwMDAwMDAwMGZmZmZmZmZmMDgwYjgyZWVjMzMyOTk2YTQyMmFlNGYwODBmNzRlNTNmZDJjYTRmMDcwMTFkNDdjNTkwODUzZTFlMzA1ZmUxMTAxMDAwMDAwMDBmZmZmZmZmZjAyYTA4NjAxMDAwMDAwMDAwMDE3YTkxNGM4Yzc3YTliNDNlZTJiZGYxYTA3YzQ4Njk5ODMzZDc2NjhiZjI2NGM4NzMyOWMwZDAwMDAwMDAwMDAxOTc2YTkxNGUwMGZmMmE2NDBiN2NlMmQzMzY4NjA3MzkxNjk0ODdhNTdmODRiMTU4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IFt7InZhbHVlIjogOTQzMzAsICJ0eF9vdXRwdXRfbiI6IDEsICJzY3JpcHQiOiAiNzZhOTE0ZTAwZmYyYTY0MGI3Y2UyZDMzNjg2MDczOTE2OTQ4N2E1N2Y4NGIxNTg4YWMifSwgeyJ2YWx1ZSI6IDg5ODc0NiwgInR4X291dHB1dF9uIjogMSwgInNjcmlwdCI6ICI3NmE5MTRlMDBmZjJhNjQwYjdjZTJkMzM2ODYwNzM5MTY5NDg3YTU3Zjg0YjE1ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="tprv8ZgxMBicQKsPeMHMJAc6uWGYiGqi1MVM2ybmzXL2TAoDpQe85uyDpdT7mv7Nhdu5rTCBEKLZsd9KyP2LQZJzZTvgVQvENArgU8e6DoYBiXf")
        >>> signature: Signature = Signature(network="testnet")
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
        elif loaded_transaction_raw["type"] == "bitcoin_withdraw_unsigned":
            return WithdrawSignature(
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

    def transaction_raw(self) -> str:
        """
        Get Bitcoin transaction raw.

        :returns: str -- Bitcoin transaction raw.

        >>> from swap.providers.bitcoin.signature import Signature
        >>> from swap.providers.bitcoin.solver import FundSolver
        >>> unsigned_fund_transaction_raw: str = "eyJmZWUiOiAxMTIyLCAicmF3IjogIjAyMDAwMDAwMDIzMWZiNzZhMGMzOGQ1NzM4MWIzMTEwZTRmNWVlOWI1MjgxZGNmMmZiZTJmZTI1NjkyNjZiNzUxMDExZDIxMWEyMDEwMDAwMDAwMGZmZmZmZmZmMDgwYjgyZWVjMzMyOTk2YTQyMmFlNGYwODBmNzRlNTNmZDJjYTRmMDcwMTFkNDdjNTkwODUzZTFlMzA1ZmUxMTAxMDAwMDAwMDBmZmZmZmZmZjAyYTA4NjAxMDAwMDAwMDAwMDE3YTkxNGM4Yzc3YTliNDNlZTJiZGYxYTA3YzQ4Njk5ODMzZDc2NjhiZjI2NGM4NzMyOWMwZDAwMDAwMDAwMDAxOTc2YTkxNGUwMGZmMmE2NDBiN2NlMmQzMzY4NjA3MzkxNjk0ODdhNTdmODRiMTU4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IFt7InZhbHVlIjogOTQzMzAsICJ0eF9vdXRwdXRfbiI6IDEsICJzY3JpcHQiOiAiNzZhOTE0ZTAwZmYyYTY0MGI3Y2UyZDMzNjg2MDczOTE2OTQ4N2E1N2Y4NGIxNTg4YWMifSwgeyJ2YWx1ZSI6IDg5ODc0NiwgInR4X291dHB1dF9uIjogMSwgInNjcmlwdCI6ICI3NmE5MTRlMDBmZjJhNjQwYjdjZTJkMzM2ODYwNzM5MTY5NDg3YTU3Zjg0YjE1ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="tprv8ZgxMBicQKsPeMHMJAc6uWGYiGqi1MVM2ybmzXL2TAoDpQe85uyDpdT7mv7Nhdu5rTCBEKLZsd9KyP2LQZJzZTvgVQvENArgU8e6DoYBiXf")
        >>> signature: Signature = Signature(network="testnet")
        >>> signature.sign(transaction_raw=unsigned_fund_transaction_raw, solver=fund_solver)
        >>> signature.transaction_raw()
        "eyJyYXciOiAiMDIwMDAwMDAwMTA4MjVlMDBiYTU5NmFiMTExMjZjZDg5MjAzYjg4MmJjZTYwYTdkYjAxOWU1MTIxNzA1NmM0NzFmNTEwY2ZkODUwMDAwMDAwMDZiNDgzMDQ1MDIyMTAwOWFjNmFmYjY4NzI4ZWVlNTMwNTBlYTdhMzAxYjZmYjgzNmUxM2I3ODJjZDUyYzI5YmUyZjhiMGNjNzFmNDQyNzAyMjA2OTY3MWEwYTNkZjE0ODczY2Y5MjY4ZTQwNTRjNGIxNzdhZmY4ZGE4OTQ2NDE4OTY2NjljZmFmYTRiZTIzYzhhMDEyMTAyMDY1ZThjYjVmYTc2Njk5MDc5ODYwYTQ1MGJkZGQwZTM3ZTBhZDNkYmYyZGRmZDAxZDdiNjAwMjMxZTZjZGU4ZWZmZmZmZmZmMDIxMDI3MDAwMDAwMDAwMDAwMTdhOTE0NDY5NTEyN2IxZDE3YzQ1NGY0YmFlOWM0MWNiOGUzY2RiNWU4OWQyNDg3ZWE1YzAxMDAwMDAwMDAwMDE5NzZhOTE0MzNlY2FiM2Q2N2YwZTJiZGU0M2U1MmY0MWVjMWVjYmRjNzNmMTFmODg4YWMwMDAwMDAwMCIsICJmZWUiOiA2NzgsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfc2lnbmVkIn0"
        """

        if self._signed_raw is None:
            raise ValueError("There is no signed data, sign unsigned transaction raw first.")
        return clean_transaction_raw(self._signed_raw)


class NormalSignature(Signature):
    """
    Bitcoin Normal signature.

    :param network: Bitcoin network, defaults to ``mainnet``.
    :type network: str
    :param version: Bitcoin transaction version, defaults to ``2``.
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

        >>> from swap.providers.bitcoin.signature import NormalSignature
        >>> from swap.providers.bitcoin.solver import NormalSolver
        >>> unsigned_normal_transaction_raw = "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTA4MjVlMDBiYTU5NmFiMTExMjZjZDg5MjAzYjg4MmJjZTYwYTdkYjAxOWU1MTIxNzA1NmM0NzFmNTEwY2ZkODUwMDAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQ0Njk1MTI3YjFkMTdjNDU0ZjRiYWU5YzQxY2I4ZTNjZGI1ZTg5ZDI0ODdlYTVjMDEwMDAwMDAwMDAwMTk3NmE5MTQzM2VjYWIzZDY3ZjBlMmJkZTQzZTUyZjQxZWMxZWNiZGM3M2YxMWY4ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJ2YWx1ZSI6IDEwMDAwMCwgInR4X291dHB1dF9uIjogMCwgInNjcmlwdCI6ICI3NmE5MTQzM2VjYWIzZDY3ZjBlMmJkZTQzZTUyZjQxZWMxZWNiZGM3M2YxMWY4ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"
        >>> normal_solver: NormalSolver = NormalSolver(xprivate_key="tprv8ZgxMBicQKsPeMHMJAc6uWGYiGqi1MVM2ybmzXL2TAoDpQe85uyDpdT7mv7Nhdu5rTCBEKLZsd9KyP2LQZJzZTvgVQvENArgU8e6DoYBiXf")
        >>> normal_signature: NormalSignature = NormalSignature(network="testnet")
        >>> normal_signature.sign(transaction_raw=unsigned_normal_transaction_raw, solver=normal_solver)
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
        self._fee, self._type, self._network, self._transaction = (
            loaded_transaction_raw["fee"], loaded_transaction_raw["type"],
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
            type=self._type
        ))).encode()).decode()
        return self


class FundSignature(Signature):
    """
    Bitcoin Fund signature.

    :param network: Bitcoin network, defaults to ``mainnet``.
    :type network: str
    :param version: Bitcoin transaction version, defaults to ``2``.
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

        >>> from swap.providers.bitcoin.signature import FundSignature
        >>> from swap.providers.bitcoin.solver import FundSolver
        >>> unsigned_fund_transaction_raw: str = "eyJmZWUiOiAxMTIyLCAicmF3IjogIjAyMDAwMDAwMDIzMWZiNzZhMGMzOGQ1NzM4MWIzMTEwZTRmNWVlOWI1MjgxZGNmMmZiZTJmZTI1NjkyNjZiNzUxMDExZDIxMWEyMDEwMDAwMDAwMGZmZmZmZmZmMDgwYjgyZWVjMzMyOTk2YTQyMmFlNGYwODBmNzRlNTNmZDJjYTRmMDcwMTFkNDdjNTkwODUzZTFlMzA1ZmUxMTAxMDAwMDAwMDBmZmZmZmZmZjAyYTA4NjAxMDAwMDAwMDAwMDE3YTkxNGM4Yzc3YTliNDNlZTJiZGYxYTA3YzQ4Njk5ODMzZDc2NjhiZjI2NGM4NzMyOWMwZDAwMDAwMDAwMDAxOTc2YTkxNGUwMGZmMmE2NDBiN2NlMmQzMzY4NjA3MzkxNjk0ODdhNTdmODRiMTU4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IFt7InZhbHVlIjogOTQzMzAsICJ0eF9vdXRwdXRfbiI6IDEsICJzY3JpcHQiOiAiNzZhOTE0ZTAwZmYyYTY0MGI3Y2UyZDMzNjg2MDczOTE2OTQ4N2E1N2Y4NGIxNTg4YWMifSwgeyJ2YWx1ZSI6IDg5ODc0NiwgInR4X291dHB1dF9uIjogMSwgInNjcmlwdCI6ICI3NmE5MTRlMDBmZjJhNjQwYjdjZTJkMzM2ODYwNzM5MTY5NDg3YTU3Zjg0YjE1ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="tprv8ZgxMBicQKsPeMHMJAc6uWGYiGqi1MVM2ybmzXL2TAoDpQe85uyDpdT7mv7Nhdu5rTCBEKLZsd9KyP2LQZJzZTvgVQvENArgU8e6DoYBiXf")
        >>> fund_signature: FundSignature = FundSignature(network="testnet")
        >>> fund_signature.sign(transaction_raw=unsigned_fund_transaction_raw, solver=fund_solver)
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
        self._fee, self._type, self._network, self._transaction = (
            loaded_transaction_raw["fee"], loaded_transaction_raw["type"],
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
            type=self._type
        ))).encode()).decode()
        return self


class WithdrawSignature(Signature):
    """
    Bitcoin Withdraw signature.

    :param network: Bitcoin network, defaults to mainnet.
    :type network: str
    :param version: Bitcoin transaction version, defaults to 2.
    :type version: int

    :returns: WithdrawSignature -- Bitcoin withdraw signature instance.
    """

    def __init__(self, network: str = config["network"], version: int = config["version"]):
        super().__init__(network=network, version=version)

    def sign(self, transaction_raw: str, solver: WithdrawSolver) -> "WithdrawSignature":
        """
        Sign unsigned withdraw transaction raw.

        :param transaction_raw: Bitcoin unsigned withdraw transaction raw.
        :type transaction_raw: str
        :param solver: Bitcoin withdraw solver.
        :type solver: bitcoin.solver.WithdrawSolver

        :returns: WithdrawSignature -- Bitcoin withdraw signature instance.

        >>> from swap.providers.bitcoin.signature import WithdrawSignature
        >>> from swap.providers.bitcoin.solver import WithdrawSolver
        >>> unsigned_withdraw_transaction_raw: str = "eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTMxZmI3NmEwYzM4ZDU3MzgxYjMxMTBlNGY1ZWU5YjUyODFkY2YyZmJlMmZlMjU2OTI2NmI3NTEwMTFkMjExYTIwMDAwMDAwMDAwZmZmZmZmZmYwMTYwODQwMTAwMDAwMDAwMDAxOTc2YTkxNDBhMGE2NTkwZTZiYTRiNDgxMThkMjFiODY4MTI2MTUyMTllY2U3NmI4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsidmFsdWUiOiAxMDAwMDAsICJ0eF9vdXRwdXRfbiI6IDAsICJzY3JpcHQiOiAiYTkxNGM4Yzc3YTliNDNlZTJiZGYxYTA3YzQ4Njk5ODMzZDc2NjhiZjI2NGM4NyJ9LCAibmV0d29yayI6ICJ0ZXN0bmV0IiwgInR5cGUiOiAiYml0Y29pbl93aXRoZHJhd191bnNpZ25lZCJ9"
        >>> bytecode: str = "63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a9140a0a6590e6ba4b48118d21b86812615219ece76b88ac67040ec4d660b17576a914e00ff2a640b7ce2d336860739169487a57f84b1588ac68"
        >>> withdraw_solver: WithdrawSolver = WithdrawSolver(xprivate_key="tprv8ZgxMBicQKsPf949JcuVFLXPJ5m4VKe33gVX3FYVZYVHr2dChU8K66aEQcPdHpUgACq5GQu81Z4e3QN1vxCrV4pxcUcXHoRTamXBRaPdJhW", secret_key="Hello Meheret!", bytecode=bytecode)
        >>> withdraw_signature: WithdrawSignature = WithdrawSignature(network="testnet")
        >>> withdraw_signature.sign(transaction_raw=unsigned_withdraw_transaction_raw, solver=withdraw_solver)
        <swap.providers.bitcoin.signature.WithdrawSignature object at 0x0409DAF0>
        """

        if not is_transaction_raw(transaction_raw=transaction_raw):
            raise TransactionRawError("Invalid Bitcoin unsigned transaction raw.")

        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

        if not loaded_transaction_raw["type"] == "bitcoin_withdraw_unsigned":
            raise TypeError(f"Invalid Bitcoin withdraw unsigned transaction raw type, "
                            f"you can't sign {loaded_transaction_raw['type']} type by using withdraw signature.")

        # Check parameter instances
        if not isinstance(solver, WithdrawSolver):
            raise TypeError(f"Solver must be Bitcoin WithdrawSolver, not {type(solver).__name__} type.")

        # Set transaction fee, type, network and transaction
        self._fee, self._type, self._network, self._transaction = (
            loaded_transaction_raw["fee"], loaded_transaction_raw["type"],
            loaded_transaction_raw["network"], MutableTransaction.unhexlify(loaded_transaction_raw["raw"])
        )

        # Sign withdraw transaction
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

        # Encode withdraw transaction raw
        self._type = "bitcoin_withdraw_signed"
        self._signed_raw = b64encode(str(json.dumps(dict(
            raw=self._transaction.hexlify(),
            fee=self._fee,
            network=self._network,
            type=self._type,
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

        >>> from swap.providers.bitcoin.signature import Signature
        >>> from swap.providers.bitcoin.solver import RefundSolver
        >>> unsigned_refund_transaction_raw: str = "eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTMxZmI3NmEwYzM4ZDU3MzgxYjMxMTBlNGY1ZWU5YjUyODFkY2YyZmJlMmZlMjU2OTI2NmI3NTEwMTFkMjExYTIwMDAwMDAwMDAwZmZmZmZmZmYwMTYwODQwMTAwMDAwMDAwMDAxOTc2YTkxNGUwMGZmMmE2NDBiN2NlMmQzMzY4NjA3MzkxNjk0ODdhNTdmODRiMTU4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsidmFsdWUiOiAxMDAwMDAsICJ0eF9vdXRwdXRfbiI6IDAsICJzY3JpcHQiOiAiYTkxNGM4Yzc3YTliNDNlZTJiZGYxYTA3YzQ4Njk5ODMzZDc2NjhiZjI2NGM4NyJ9LCAibmV0d29yayI6ICJ0ZXN0bmV0IiwgInR5cGUiOiAiYml0Y29pbl9yZWZ1bmRfdW5zaWduZWQifQ"
        >>> bytecode: str = "63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a9140a0a6590e6ba4b48118d21b86812615219ece76b88ac67040ec4d660b17576a914e00ff2a640b7ce2d336860739169487a57f84b1588ac68"
        >>> refund_solver: RefundSolver = RefundSolver(xprivate_key="tprv8ZgxMBicQKsPeMHMJAc6uWGYiGqi1MVM2ybmzXL2TAoDpQe85uyDpdT7mv7Nhdu5rTCBEKLZsd9KyP2LQZJzZTvgVQvENArgU8e6DoYBiXf", bytecode=bytecode, endtime=1624687630)
        >>> refund_signature: RefundSignature = RefundSignature(network="testnet")
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
        self._fee, self._type, self._network, self._transaction = (
            loaded_transaction_raw["fee"], loaded_transaction_raw["type"],
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
        ))).encode()).decode()
        return self
