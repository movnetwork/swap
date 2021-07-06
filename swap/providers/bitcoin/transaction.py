#!/usr/bin/env python3

from base64 import b64encode
from btcpy.structs.script import (
    ScriptSig, P2shScript
)
from btcpy.structs.transaction import (
    Locktime, MutableTransaction, TxOut, Sequence, TxIn
)
from btcpy.structs.sig import P2shSolver
from btcpy.setup import setup
from typing import (
    Optional, Union
)

import json

from ...utils import clean_transaction_raw
from ...exceptions import (
    BalanceError, AddressError, NetworkError, UnitError
)
from ..config import bitcoin as config
from .htlc import HTLC
from .utils import (
    fee_calculator, is_address, is_network, _get_previous_transaction_indexes,
    _build_inputs, _build_outputs, get_address_hash, amount_unit_converter
)
from .solver import (
    FundSolver, WithdrawSolver, RefundSolver
)
from .rpc import (
    get_transaction, get_utxos, find_p2sh_utxo
)


class Transaction:
    """
    Bitcoin Transaction.

    :param network: Bitcoin network, defaults to ``mainnet``.
    :type network: str
    :param version: Bitcoin transaction version, defaults to ``2``.
    :type version: int

    :returns: Transaction -- Bitcoin transaction instance.

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
        self._address: Optional[str] = None
        self._datas: dict = {}
        self._amount: int = 0
        self._fee: int = 0

        setup(network, strict=True, force=True)

    def fee(self, unit: str = config["unit"]) -> Union[int, float]:
        """
        Get Bitcoin transaction fee.

        :param unit: Bitcoin unit, default to ``Satoshi``.
        :type unit: str

        :returns: int, float -- Bitcoin transaction fee.

        >>> from swap.providers.bitcoin.transaction import WithdrawTransaction
        >>> withdraw_transaction = WithdrawTransaction("testnet")
        >>> withdraw_transaction.build_transaction("mgS3WMHp9nvdUPeDJxr5iCF2P5HuFZSR3V", "a211d21110756b266925fee2fbf2dc81529beef5e410311b38578dc3a076fb31")
        >>> withdraw_transaction.fee(unit="Satoshi")
        576
        """

        if unit not in ["BTC", "mBTC", "Satoshi"]:
            raise UnitError("Invalid Bitcoin unit, choose only 'BTC', 'mBTC' or 'Satoshi' units.")
        return self._fee if unit == "Satoshi" else \
            amount_unit_converter(amount=self._fee, unit_from=f"Satoshi2{unit}")

    def hash(self) -> str:
        """
        Get Bitcoin transaction hash.

        :returns: str -- Bitcoin transaction id/hash.

        >>> from swap.providers.bitcoin.htlc import HTLC
        >>> from swap.providers.bitcoin.transaction import FundTransaction
        >>> from swap.utils import sha256
        >>> htlc: HTLC = HTLC(network="testnet")
        >>> htlc.build_htlc(secret_hash=sha256("Hello Meheret!"), recipient_address="mgS3WMHp9nvdUPeDJxr5iCF2P5HuFZSR3V", sender_address="n1wgm6kkzMcNfAtJmes8YhpvtDzdNhDY5a", endtime=1624687630)
        >>> fund_transaction: FundTransaction = FundTransaction(network="testnet")
        >>> fund_transaction.build_transaction(address="n1wgm6kkzMcNfAtJmes8YhpvtDzdNhDY5a", htlc=htlc, amount=0.001, unit="BTC")
        >>> fund_transaction.hash()
        "9cc0524fb8e7b2c5fecaee4eb91d43a3dc5cc18e9906abcb35a5732ff52efcc7"
        """

        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")
        return self._transaction.txid

    def json(self) -> dict:
        """
        Get Bitcoin transaction json format.

        :returns: dict -- Bitcoin transaction json format.

        >>> from swap.providers.bitcoin.transaction import RefundTransaction
        >>> refund_transaction: RefundTransaction = RefundTransaction(network="testnet")
        >>> refund_transaction.build_transaction(address="n1wgm6kkzMcNfAtJmes8YhpvtDzdNhDY5a", transaction_hash="a211d21110756b266925fee2fbf2dc81529beef5e410311b38578dc3a076fb31")
        >>> refund_transaction.json()
        {"hex": "02000000012c392217483906f902e73c4bc132864de58153772d79268960998162266634be0100000000ffffffff02e80300000000000017a914971894c58d85981c16c2059d422bcde0b156d04487a6290000000000001976a9146bce65e58a50b97989930e9a4ff1ac1a77515ef188ac00000000", "txid": "9cc0524fb8e7b2c5fecaee4eb91d43a3dc5cc18e9906abcb35a5732ff52efcc7", "hash": "9cc0524fb8e7b2c5fecaee4eb91d43a3dc5cc18e9906abcb35a5732ff52efcc7", "size": 117, "vsize": 117, "version": 2, "locktime": 0, "vin": [{"txid": "be346626628199608926792d775381e54d8632c14b3ce702f90639481722392c", "vout": 1, "scriptSig": {"asm": "", "hex": ""}, "sequence": "4294967295"}], "vout": [{"value": "0.00001000", "n": 0, "scriptPubKey": {"asm": "OP_HASH160 971894c58d85981c16c2059d422bcde0b156d044 OP_EQUAL", "hex": "a914971894c58d85981c16c2059d422bcde0b156d04487", "type": "p2sh", "address": "2N729UBGZB3xjsGFRgKivy4bSjkaJGMVSpB"}}, {"value": "0.00010662", "n": 1, "scriptPubKey": {"asm": "OP_DUP OP_HASH160 6bce65e58a50b97989930e9a4ff1ac1a77515ef1 OP_EQUALVERIFY OP_CHECKSIG", "hex": "76a9146bce65e58a50b97989930e9a4ff1ac1a77515ef188ac", "type": "p2pkh", "address": "mqLyrNDjpENRMZAoDpspH7kR9RtgvhWzYE"}}]}
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")
        return self._transaction.to_json()

    def raw(self) -> str:
        """
        Get Bitcoin main transaction raw.

        :returns: str -- Bitcoin transaction raw.

        >>> from swap.providers.bitcoin.transaction import WithdrawTransaction
        >>> withdraw_transaction: WithdrawTransaction = WithdrawTransaction("testnet")
        >>> withdraw_transaction.build_transaction(address="mgS3WMHp9nvdUPeDJxr5iCF2P5HuFZSR3V", transaction_hash="a211d21110756b266925fee2fbf2dc81529beef5e410311b38578dc3a076fb31")
        >>> withdraw_transaction.raw()
        "02000000012c392217483906f902e73c4bc132864de58153772d79268960998162266634be0100000000ffffffff02e80300000000000017a914971894c58d85981c16c2059d422bcde0b156d04487a6290000000000001976a9146bce65e58a50b97989930e9a4ff1ac1a77515ef188ac00000000"
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")
        return self._transaction.hexlify()

    def type(self) -> str:
        """
        Get Bitcoin signature transaction type.

        :returns: str -- Bitcoin signature transaction type.

        >>> from swap.providers.bitcoin.transaction import WithdrawTransaction
        >>> withdraw_transaction: WithdrawTransaction = WithdrawTransaction(network="testnet")
        >>> withdraw_transaction.build_transaction(address="mgS3WMHp9nvdUPeDJxr5iCF2P5HuFZSR3V", transaction_hash="a211d21110756b266925fee2fbf2dc81529beef5e410311b38578dc3a076fb31")
        >>> withdraw_transaction.type()
        "bitcoin_withdraw_unsigned"
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")
        return self._type

    def datas(self) -> dict:
        return self._datas


class FundTransaction(Transaction):
    """
    Bitcoin Fund transaction.

    :param network: Bitcoin network, defaults to ``mainnet``.
    :type network: str
    :param version: Bitcoin transaction version, defaults to ``2``.
    :type version: int

    :returns: FundTransaction -- Bitcoin fund transaction instance.

    .. warning::
        Do not forget to build transaction after initialize fund transaction.
    """

    def __init__(self, network: str = config["network"], version: int = config["version"]):
        super().__init__(network=network, version=version)

        self._htlc: Optional[HTLC] = None
        self._utxos: Optional[list] = None
        self._previous_transaction_indexes: Optional[list] = None
        self._interest: Optional[int] = None

    def build_transaction(self, address: str, htlc: HTLC, amount: Optional[Union[int, float]],
                          unit: str = config["unit"], locktime: int = config["locktime"]) -> "FundTransaction":
        """
        Build Bitcoin fund transaction.

        :param address: Bitcoin sender address.
        :type address: str
        :param htlc: Bitcoin HTLC instance.
        :type htlc: bitcoin.htlc.HTLC
        :param amount: Bitcoin amount, default to ``None``.
        :type amount: int, float
        :param unit: Bitcoin unit, default to ``Satoshi``.
        :type unit: str
        :param locktime: Bitcoin transaction lock time, defaults to ``0``.
        :type locktime: int

        :returns: FundTransaction -- Bitcoin fund transaction instance.

        >>> from swap.providers.bitcoin.htlc import HTLC
        >>> from swap.providers.bitcoin.transaction import FundTransaction
        >>> from swap.utils import sha256
        >>> htlc: HTLC = HTLC(network="testnet")
        >>> htlc.build_htlc(secret_hash=sha256("Hello Meheret!"), recipient_address="mgS3WMHp9nvdUPeDJxr5iCF2P5HuFZSR3V", sender_address="n1wgm6kkzMcNfAtJmes8YhpvtDzdNhDY5a", endtime=1624687630)
        >>> fund_transaction: FundTransaction = FundTransaction(network="testnet")
        >>> fund_transaction.build_transaction(address="n1wgm6kkzMcNfAtJmes8YhpvtDzdNhDY5a", htlc=htlc, amount=0.001, unit="BTC")
        <swap.providers.bitcoin.transaction.FundTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not is_address(address, self._network):
            raise AddressError(f"Invalid Bitcoin sender '{address}' {self._network} address.")
        if not isinstance(htlc, HTLC):
            raise TypeError("Invalid Bitcoin HTLC instance, only takes xinfin HTLC class")
        if htlc.agreements and address != htlc.agreements["sender_address"]:
            raise AddressError(f"Wrong Bitcoin sender '{address}' address",
                               "address must be equal with HTLC agreements sender address.")
        if unit not in ["BTC", "mBTC", "Satoshi"]:
            raise UnitError("Invalid Bitcoin unit, choose only 'BTC', 'mBTC' or 'Satoshi' units.")

        self._address, self._htlc, self._amount = (
            address, htlc, (
                amount if unit == "Satoshi" else
                amount_unit_converter(
                    amount=amount, unit_from=f"{unit}2Satoshi"
                )
            )
        )

        # Get Sender UTXO's
        self._utxos = get_utxos(
            address=self._address, network=self._network
        )
        # Get previous transaction indexes
        self._previous_transaction_indexes, max_amount = _get_previous_transaction_indexes(
            utxos=self._utxos, amount=self._amount, transaction_output=2
        )
        # Build transaction inputs
        inputs, amount = _build_inputs(
            utxos=self._utxos, previous_transaction_indexes=self._previous_transaction_indexes
        )
        # Calculate the fee
        self._fee = fee_calculator(len(inputs), 2)

        if amount < (self._amount + self._fee):
            raise BalanceError(
                "Insufficient spend UTXO's",
                f"You don't have enough amount to pay '{self._fee}' Satoshi fee."
            )

        return_amount: int = int(amount - (self._amount + self._fee))
        outputs: list = [TxOut(
            value=self._amount, n=0,
            script_pubkey=get_address_hash(
                address=self._htlc.contract_address(), script=True
            )
        )]
        if return_amount != 0:
            outputs.append(TxOut(
                value=return_amount, n=len(outputs),
                script_pubkey=get_address_hash(
                    address=self._address, script=True
                )
            ))

        # Build mutable transaction
        self._transaction = MutableTransaction(
            version=self._version, ins=inputs, outs=outputs, locktime=Locktime(locktime)
        )
        # Set transaction type
        self._type = "bitcoin_fund_unsigned"
        return self

    def sign(self, solver: FundSolver) -> "FundTransaction":
        """
        Sign Bitcoin fund transaction.

        :param solver: Bitcoin fund solver.
        :type solver: bitcoin.solver.FundSolver

        :returns: FundTransaction -- Bitcoin fund transaction instance.

        >>> from swap.providers.bitcoin.htlc import HTLC
        >>> from swap.providers.bitcoin.transaction import FundTransaction
        >>> from swap.providers.bitcoin.solver import FundSolver
        >>> from swap.utils import sha256
        >>> htlc: HTLC = HTLC(network="testnet")
        >>> htlc.build_htlc(secret_hash=sha256("Hello Meheret!"), recipient_address="mgS3WMHp9nvdUPeDJxr5iCF2P5HuFZSR3V", sender_address="n1wgm6kkzMcNfAtJmes8YhpvtDzdNhDY5a", endtime=1624687630)
        >>> fund_transaction: FundTransaction = FundTransaction(network="testnet")
        >>> fund_transaction.build_transaction(address="n1wgm6kkzMcNfAtJmes8YhpvtDzdNhDY5a", htlc=htlc, amount=0.001, unit="BTC")
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="tprv8ZgxMBicQKsPeMHMJAc6uWGYiGqi1MVM2ybmzXL2TAoDpQe85uyDpdT7mv7Nhdu5rTCBEKLZsd9KyP2LQZJzZTvgVQvENArgU8e6DoYBiXf")
        >>> fund_transaction.sign(solver=fund_solver)
        <swap.providers.bitcoin.transaction.FundTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not isinstance(solver, FundSolver):
            raise TypeError(f"Solver must be Bitcoin FundSolver, not {type(solver).__name__} type.")
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")

        # Organize outputs
        outputs = _build_outputs(
            utxos=self._utxos, previous_transaction_indexes=self._previous_transaction_indexes
        )
        # Sign fund transaction
        self._transaction.spend(
            txouts=outputs,
            solvers=[solver.solve(network=self._network) for _ in outputs]
        )

        # Set transaction type
        self._type = "bitcoin_fund_signed"
        return self

    def transaction_raw(self) -> str:
        """
        Get Bitcoin fund transaction raw.

        :returns: str -- Bitcoin fund transaction raw.

        >>> from swap.providers.bitcoin.htlc import HTLC
        >>> from swap.providers.bitcoin.transaction import FundTransaction
        >>> from swap.utils import sha256
        >>> htlc: HTLC = HTLC(network="testnet")
        >>> htlc.build_htlc(secret_hash=sha256("Hello Meheret!"), recipient_address="mgS3WMHp9nvdUPeDJxr5iCF2P5HuFZSR3V", sender_address="n1wgm6kkzMcNfAtJmes8YhpvtDzdNhDY5a", endtime=1624687630)
        >>> fund_transaction: FundTransaction = FundTransaction(network="testnet")
        >>> fund_transaction.build_transaction(address="n1wgm6kkzMcNfAtJmes8YhpvtDzdNhDY5a", htlc=htlc, amount=0.001, unit="BTC")
        >>> fund_transaction.transaction_raw()
        "eyJmZWUiOiAxMTIyLCAicmF3IjogIjAyMDAwMDAwMDIzMWZiNzZhMGMzOGQ1NzM4MWIzMTEwZTRmNWVlOWI1MjgxZGNmMmZiZTJmZTI1NjkyNjZiNzUxMDExZDIxMWEyMDEwMDAwMDAwMGZmZmZmZmZmMDgwYjgyZWVjMzMyOTk2YTQyMmFlNGYwODBmNzRlNTNmZDJjYTRmMDcwMTFkNDdjNTkwODUzZTFlMzA1ZmUxMTAxMDAwMDAwMDBmZmZmZmZmZjAyYTA4NjAxMDAwMDAwMDAwMDE3YTkxNGM4Yzc3YTliNDNlZTJiZGYxYTA3YzQ4Njk5ODMzZDc2NjhiZjI2NGM4NzMyOWMwZDAwMDAwMDAwMDAxOTc2YTkxNGUwMGZmMmE2NDBiN2NlMmQzMzY4NjA3MzkxNjk0ODdhNTdmODRiMTU4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IFt7InZhbHVlIjogOTQzMzAsICJ0eF9vdXRwdXRfbiI6IDEsICJzY3JpcHQiOiAiNzZhOTE0ZTAwZmYyYTY0MGI3Y2UyZDMzNjg2MDczOTE2OTQ4N2E1N2Y4NGIxNTg4YWMifSwgeyJ2YWx1ZSI6IDg5ODc0NiwgInR4X291dHB1dF9uIjogMSwgInNjcmlwdCI6ICI3NmE5MTRlMDBmZjJhNjQwYjdjZTJkMzM2ODYwNzM5MTY5NDg3YTU3Zjg0YjE1ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"
        """

        # Check parameter instances
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")

        # Encode fund transaction raw
        if self._type == "bitcoin_fund_signed":
            return clean_transaction_raw(b64encode(str(json.dumps(dict(
                raw=self._transaction.hexlify(),
                fee=self._fee,
                network=self._network,
                type=self._type,
            ))).encode()).decode())
        return clean_transaction_raw(b64encode(str(json.dumps(dict(
            fee=self._fee,
            raw=self._transaction.hexlify(),
            outputs=_build_outputs(
                utxos=self._utxos,
                previous_transaction_indexes=self._previous_transaction_indexes,
                only_dict=True
            ),
            network=self._network,
            type=self._type,
        ))).encode()).decode())


class WithdrawTransaction(Transaction):
    """
    Bitcoin Withdraw transaction.

    :param network: Bitcoin network, defaults to ``mainnet``.
    :type network: str
    :param version: Bitcoin transaction version, defaults to ``2``.
    :type version: int

    :returns: WithdrawTransaction -- Bitcoin withdraw transaction instance.

    .. warning::
        Do not forget to build transaction after initialize withdraw transaction.
    """

    def __init__(self, network: str = config["network"], version: int = config["version"]):
        super().__init__(network=network, version=version)

        self._transaction_hash: Optional[str] = None
        self._transaction_detail: Optional[dict] = None
        self._htlc_utxo: Optional[dict] = None
        self._interest: Optional[int] = None

    def build_transaction(self, address: str, transaction_hash: str,
                          locktime: int = config["locktime"]) -> "WithdrawTransaction":
        """
        Build Bitcoin withdraw transaction.

        :param address: Bitcoin recipient address.
        :type address: str
        :param transaction_hash: Bitcoin funded transaction hash/id.
        :type transaction_hash: str
        :param locktime: Bitcoin transaction lock time, defaults to ``0``.
        :type locktime: int

        :returns: WithdrawTransaction -- Bitcoin withdraw transaction instance.

        >>> from swap.providers.bitcoin.transaction import WithdrawTransaction
        >>> withdraw_transaction: WithdrawTransaction = WithdrawTransaction("testnet")
        >>> withdraw_transaction.build_transaction(address="mgS3WMHp9nvdUPeDJxr5iCF2P5HuFZSR3V", transaction_hash="a211d21110756b266925fee2fbf2dc81529beef5e410311b38578dc3a076fb31")
        <swap.providers.bitcoin.transaction.WithdrawTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not is_address(address, self._network):
            raise AddressError(f"Invalid Bitcoin recipient '{address}' {self._network} address.")

        # Set address and transaction hash
        self._address, self._transaction_hash, = address, transaction_hash
        # Get transaction
        self._transaction_detail = get_transaction(
            transaction_hash=self._transaction_hash, network=self._network
        )
        # Find HTLC UTXO
        self._htlc_utxo = find_p2sh_utxo(transaction=self._transaction_detail)

        if self._htlc_utxo is None:
            raise ValueError("Invalid transaction hash, there is no pay to script hash (P2SH) address.")

        self._amount = self._htlc_utxo["value"]
        # Calculate the fee
        self._fee = fee_calculator(1, 1)

        outputs: list = [TxOut(
            value=(self._amount - self._fee), n=0, script_pubkey=get_address_hash(
                address=self._address, script=True
            )
        )]
        # Build mutable transaction
        self._transaction = MutableTransaction(
            version=self._version,
            ins=[TxIn(
                txid=self._transaction_hash,
                txout=self._htlc_utxo["position"],
                script_sig=ScriptSig.empty(),
                sequence=Sequence.max()
            )],
            outs=outputs,
            locktime=Locktime(locktime)
        )

        # Set transaction type
        self._type = "bitcoin_withdraw_unsigned"
        return self

    def sign(self, solver: WithdrawSolver) -> "WithdrawTransaction":
        """
        Sign Bitcoin withdraw transaction.

        :param solver: Bitcoin withdraw solver.
        :type solver: bitcoin.solver.WithdrawSolver

        :returns: WithdrawTransaction -- Bitcoin withdraw transaction instance.

        >>> from swap.providers.bitcoin.transaction import WithdrawTransaction
        >>> from swap.providers.bitcoin.solver import WithdrawSolver
        >>> withdraw_transaction: WithdrawTransaction = WithdrawTransaction("testnet")
        >>> withdraw_transaction.build_transaction(address="mgS3WMHp9nvdUPeDJxr5iCF2P5HuFZSR3V", transaction_hash="a211d21110756b266925fee2fbf2dc81529beef5e410311b38578dc3a076fb31")
        >>> bytecode: str = "63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a9140a0a6590e6ba4b48118d21b86812615219ece76b88ac67040ec4d660b17576a914e00ff2a640b7ce2d336860739169487a57f84b1588ac68"
        >>> withdraw_solver: WithdrawSolver = WithdrawSolver(xprivate_key="tprv8ZgxMBicQKsPf949JcuVFLXPJ5m4VKe33gVX3FYVZYVHr2dChU8K66aEQcPdHpUgACq5GQu81Z4e3QN1vxCrV4pxcUcXHoRTamXBRaPdJhW", secret_key="Hello Meheret!", bytecode=bytecode)
        >>> withdraw_transaction.sign(solver=withdraw_solver)
        <swap.providers.bitcoin.transaction.WithdrawTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not isinstance(solver, WithdrawSolver):
            raise TypeError(f"Solver must be Bitcoin WithdrawSolver, not {type(solver).__name__} type.")
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")

        self._transaction.spend([TxOut(
            value=self._htlc_utxo["value"],
            n=0,
            script_pubkey=P2shScript.unhexlify(
                hex_string=self._htlc_utxo["script"]
            )
        )], [P2shSolver(
            redeem_script=solver.witness(
                network=self._network
            ),
            redeem_script_solver=solver.solve(
                network=self._network
            )
        )])

        # Set transaction type
        self._type = "bitcoin_withdraw_signed"
        return self

    def transaction_raw(self) -> str:
        """
        Get Bitcoin withdraw transaction raw.

        :returns: str -- Bitcoin withdraw transaction raw.

        >>> from swap.providers.bitcoin.transaction import WithdrawTransaction
        >>> withdraw_transaction: WithdrawTransaction = WithdrawTransaction("testnet")
        >>> withdraw_transaction.build_transaction(address="mgS3WMHp9nvdUPeDJxr5iCF2P5HuFZSR3V", transaction_hash="a211d21110756b266925fee2fbf2dc81529beef5e410311b38578dc3a076fb31")
        >>> withdraw_transaction.transaction_raw()
        "eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTMxZmI3NmEwYzM4ZDU3MzgxYjMxMTBlNGY1ZWU5YjUyODFkY2YyZmJlMmZlMjU2OTI2NmI3NTEwMTFkMjExYTIwMDAwMDAwMDAwZmZmZmZmZmYwMTYwODQwMTAwMDAwMDAwMDAxOTc2YTkxNDBhMGE2NTkwZTZiYTRiNDgxMThkMjFiODY4MTI2MTUyMTllY2U3NmI4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsidmFsdWUiOiAxMDAwMDAsICJ0eF9vdXRwdXRfbiI6IDAsICJzY3JpcHQiOiAiYTkxNGM4Yzc3YTliNDNlZTJiZGYxYTA3YzQ4Njk5ODMzZDc2NjhiZjI2NGM4NyJ9LCAibmV0d29yayI6ICJ0ZXN0bmV0IiwgInR5cGUiOiAiYml0Y29pbl93aXRoZHJhd191bnNpZ25lZCJ9"
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")

        # Encode withdraw transaction raw
        if self._type == "bitcoin_withdraw_signed":
            return clean_transaction_raw(b64encode(str(json.dumps(dict(
                raw=self._transaction.hexlify(),
                fee=self._fee,
                network=self._network,
                type=self._type,
            ))).encode()).decode())
        return clean_transaction_raw(b64encode(str(json.dumps(dict(
            fee=self._fee,
            raw=self._transaction.hexlify(),
            outputs=dict(
                value=self._htlc_utxo["value"],
                tx_output_n=0,
                script=self._htlc_utxo["script"]
            ),
            network=self._network,
            type=self._type,
        ))).encode()).decode())


class RefundTransaction(Transaction):
    """
    Bitcoin Refund transaction.

    :param network: Bitcoin network, defaults to ``mainnet``.
    :type network: str
    :param version: Bitcoin transaction version, defaults to ``2``.
    :type version: int

    :returns: RefundTransaction -- Bitcoin refund transaction instance.

    .. warning::
        Do not forget to build transaction after initialize refund transaction.
    """

    def __init__(self, network: str = config["network"], version: int = config["version"]):
        super().__init__(network=network, version=version)

        self._transaction_hash: Optional[str] = None
        self._transaction_detail: Optional[dict] = None
        self._htlc_utxo: Optional[dict] = None
        self._interest: Optional[int] = None

    def build_transaction(self, address: str, transaction_hash: str,
                          locktime: int = config["locktime"]) -> "RefundTransaction":
        """
        Build Bitcoin refund transaction.

        :param address: Bitcoin sender address.
        :type address: str
        :param transaction_hash: Bitcoin funded transaction hash/id.
        :type transaction_hash: str
        :param locktime: Bitcoin transaction lock time, defaults to ``0``.
        :type locktime: int

        :returns: RefundTransaction -- Bitcoin refund transaction instance.

        >>> from swap.providers.bitcoin.transaction import RefundTransaction
        >>> refund_transaction: RefundTransaction = RefundTransaction("testnet")
        >>> refund_transaction.build_transaction(address="n1wgm6kkzMcNfAtJmes8YhpvtDzdNhDY5a", transaction_hash="a211d21110756b266925fee2fbf2dc81529beef5e410311b38578dc3a076fb31")
        <swap.providers.bitcoin.transaction.RefundTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not is_address(address, self._network):
            raise AddressError(f"Invalid Bitcoin sender '{address}' {self._network} address.")

        # Set address and transaction_hash
        self._address, self._transaction_hash, = address, transaction_hash
        # Get transaction
        self._transaction_detail = get_transaction(
            transaction_hash=self._transaction_hash, network=self._network
        )
        # Find HTLC UTXO
        self._htlc_utxo = find_p2sh_utxo(transaction=self._transaction_detail)

        if self._htlc_utxo is None:
            raise ValueError("Invalid transaction id, there is no pay to script hash (P2SH) address.")

        self._amount = self._htlc_utxo["value"]
        # Calculate the fee
        self._fee = fee_calculator(1, 1)

        outputs: list = [TxOut(
            value=(self._amount - self._fee), n=0, script_pubkey=get_address_hash(
                address=self._address, script=True
            )
        )]
        # Build mutable transaction
        self._transaction = MutableTransaction(
            version=self._version,
            ins=[TxIn(
                txid=self._transaction_hash,
                txout=self._htlc_utxo["position"],
                script_sig=ScriptSig.empty(),
                sequence=Sequence.max()
            )],
            outs=outputs,
            locktime=Locktime(locktime)
        )

        # Set transaction type
        self._type = "bitcoin_refund_unsigned"
        return self

    def sign(self, solver: RefundSolver) -> "RefundTransaction":
        """
        Sign Bitcoin refund transaction.

        :param solver: Bitcoin refund solver.
        :type solver: bitcoin.solver.RefundSolver

        :returns: RefundTransaction -- Bitcoin refund transaction instance.

        >>> from swap.providers.bitcoin.transaction import RefundTransaction
        >>> refund_transaction: RefundTransaction = RefundTransaction("testnet")
        >>> refund_transaction.build_transaction(address="n1wgm6kkzMcNfAtJmes8YhpvtDzdNhDY5a", transaction_hash="a211d21110756b266925fee2fbf2dc81529beef5e410311b38578dc3a076fb31")
        >>> bytecode: str = "63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a9140a0a6590e6ba4b48118d21b86812615219ece76b88ac67040ec4d660b17576a914e00ff2a640b7ce2d336860739169487a57f84b1588ac68"
        >>> refund_solver: RefundSolver = RefundSolver(xprivate_key="tprv8ZgxMBicQKsPeMHMJAc6uWGYiGqi1MVM2ybmzXL2TAoDpQe85uyDpdT7mv7Nhdu5rTCBEKLZsd9KyP2LQZJzZTvgVQvENArgU8e6DoYBiXf", bytecode=bytecode, endtime=1624687630)
        >>> refund_transaction.sign(solver=refund_solver)
        <swap.providers.bitcoin.transaction.RefundTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not isinstance(solver, RefundSolver):
            raise TypeError(f"Solver must be Bitcoin RefundSolver, not {type(solver).__name__} type.")
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")

        self._transaction.spend([TxOut(
            value=self._htlc_utxo["value"],
            n=0,
            script_pubkey=P2shScript.unhexlify(
                hex_string=self._htlc_utxo["script"]
            )
        )], [P2shSolver(
            redeem_script=solver.witness(
                network=self._network
            ),
            redeem_script_solver=solver.solve(
                network=self._network
            )
        )])

        # Set transaction type
        self._type = "bitcoin_refund_signed"
        return self

    def transaction_raw(self) -> str:
        """
        Get Bitcoin refund transaction raw.

        :returns: str -- Bitcoin refund transaction raw.

        >>> from swap.providers.bitcoin.transaction import RefundTransaction
        >>> refund_transaction: RefundTransaction = RefundTransaction("testnet")
        >>> refund_transaction.build_transaction(address="n1wgm6kkzMcNfAtJmes8YhpvtDzdNhDY5a", transaction_hash="a211d21110756b266925fee2fbf2dc81529beef5e410311b38578dc3a076fb31")
        >>> refund_transaction.transaction_raw()
        "eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTMxZmI3NmEwYzM4ZDU3MzgxYjMxMTBlNGY1ZWU5YjUyODFkY2YyZmJlMmZlMjU2OTI2NmI3NTEwMTFkMjExYTIwMDAwMDAwMDAwZmZmZmZmZmYwMTYwODQwMTAwMDAwMDAwMDAxOTc2YTkxNGUwMGZmMmE2NDBiN2NlMmQzMzY4NjA3MzkxNjk0ODdhNTdmODRiMTU4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsidmFsdWUiOiAxMDAwMDAsICJ0eF9vdXRwdXRfbiI6IDAsICJzY3JpcHQiOiAiYTkxNGM4Yzc3YTliNDNlZTJiZGYxYTA3YzQ4Njk5ODMzZDc2NjhiZjI2NGM4NyJ9LCAibmV0d29yayI6ICJ0ZXN0bmV0IiwgInR5cGUiOiAiYml0Y29pbl9yZWZ1bmRfdW5zaWduZWQifQ=="
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")

        # Encode refund transaction raw
        if self._type == "bitcoin_refund_signed":
            return clean_transaction_raw(b64encode(str(json.dumps(dict(
                raw=self._transaction.hexlify(),
                fee=self._fee,
                network=self._network,
                type=self._type,
            ))).encode()).decode())
        return clean_transaction_raw(b64encode(str(json.dumps(dict(
            fee=self._fee,
            raw=self._transaction.hexlify(),
            outputs=dict(
                value=self._htlc_utxo["value"],
                tx_output_n=0,
                script=self._htlc_utxo["script"]
            ),
            network=self._network,
            type=self._type,
        ))).encode()).decode())
