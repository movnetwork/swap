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
    BalanceError, AddressError, NetworkError, SymbolError
)
from ..config import bitcoin as config
from .utils import (
    fee_calculator, is_address, is_network, _get_previous_transaction_indexes,
    _build_inputs, _build_outputs, get_address_hash, amount_converter, get_address_type
)
from .solver import (
    FundSolver, ClaimSolver, RefundSolver
)
from .rpc import (
    get_transaction, get_utxos, find_p2sh_utxo
)


class Transaction:
    """
    Bitcoin Transaction.

    :param network: Bitcoin network, defaults to testnet.
    :type network: str
    :param version: Bitcoin transaction version, defaults to 2.
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
        self._version: int = version
        self._transaction: Optional[MutableTransaction] = None
        self._fee: int = 0
        self._type: Optional[str] = None
        self._address: Optional[str] = None
        self._amount: int = 0

        setup(network, strict=True, force=True)

    def fee(self, symbol: str = config["symbol"]) -> Union[int, float]:
        """
        Get Bitcoin transaction fee.

        :param symbol: Bitcoin symbol, default to SATOSHI.
        :type symbol: str

        :returns: int, float -- Bitcoin transaction fee.

        >>> from swap.providers.bitcoin.transaction import ClaimTransaction
        >>> claim_transaction = ClaimTransaction("testnet")
        >>> claim_transaction.build_transaction("mgokpSJoX7npmAK1Zj8ze1926CLxYDt1iF", "1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", 10000)
        >>> claim_transaction.fee(symbol="SATOSHI")
        576
        """

        if symbol not in ["BTC", "mBTC", "SATOSHI"]:
            raise SymbolError("Invalid Bitcoin symbol, choose only BTC, mBTC or SATOSHI symbols.")
        return self._fee if symbol == "SATOSHI" else \
            amount_converter(amount=self._fee, symbol=f"SATOSHI2{symbol}")

    def hash(self) -> str:
        """
        Get Bitcoin transaction hash.

        :returns: str -- Bitcoin transaction id/hash.

        >>> from swap.providers.bitcoin.transaction import FundTransaction
        >>> fund_transaction = FundTransaction("testnet")
        >>> fund_transaction.build_transaction("mkFWGt4hT11XS8dJKzzRFsTrqjjAwZfQAC", "2N6kHwQy6Ph5EdKNgzGrcW2WhGHKGfmP5ae", 10000)
        >>> fund_transaction.hash()
        "9cc0524fb8e7b2c5fecaee4eb91d43a3dc5cc18e9906abcb35a5732ff52efcc7"
        """

        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first..")
        return self._transaction.txid

    def json(self) -> dict:
        """
        Get Bitcoin transaction json format.

        :returns: dict -- Bitcoin transaction json format.

        >>> from swap.providers.bitcoin.transaction import RefundTransaction
        >>> refund_transaction = RefundTransaction("testnet")
        >>> refund_transaction.build_transaction("mkFWGt4hT11XS8dJKzzRFsTrqjjAwZfQAC", "1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", 10000)
        >>> refund_transaction.json()
        {"hex": "02000000012c392217483906f902e73c4bc132864de58153772d79268960998162266634be0100000000ffffffff02e80300000000000017a914971894c58d85981c16c2059d422bcde0b156d04487a6290000000000001976a9146bce65e58a50b97989930e9a4ff1ac1a77515ef188ac00000000", "txid": "9cc0524fb8e7b2c5fecaee4eb91d43a3dc5cc18e9906abcb35a5732ff52efcc7", "hash": "9cc0524fb8e7b2c5fecaee4eb91d43a3dc5cc18e9906abcb35a5732ff52efcc7", "size": 117, "vsize": 117, "version": 2, "locktime": 0, "vin": [{"txid": "be346626628199608926792d775381e54d8632c14b3ce702f90639481722392c", "vout": 1, "scriptSig": {"asm": "", "hex": ""}, "sequence": "4294967295"}], "vout": [{"value": "0.00001000", "n": 0, "scriptPubKey": {"asm": "OP_HASH160 971894c58d85981c16c2059d422bcde0b156d044 OP_EQUAL", "hex": "a914971894c58d85981c16c2059d422bcde0b156d04487", "type": "p2sh", "address": "2N729UBGZB3xjsGFRgKivy4bSjkaJGMVSpB"}}, {"value": "0.00010662", "n": 1, "scriptPubKey": {"asm": "OP_DUP OP_HASH160 6bce65e58a50b97989930e9a4ff1ac1a77515ef1 OP_EQUALVERIFY OP_CHECKSIG", "hex": "76a9146bce65e58a50b97989930e9a4ff1ac1a77515ef188ac", "type": "p2pkh", "address": "mqLyrNDjpENRMZAoDpspH7kR9RtgvhWzYE"}}]}
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first..")
        return self._transaction.to_json()

    def raw(self) -> str:
        """
        Get Bitcoin main transaction raw.

        :returns: str -- Bitcoin transaction raw.

        >>> from swap.providers.bitcoin.transaction import ClaimTransaction
        >>> claim_transaction = ClaimTransaction("testnet")
        >>> claim_transaction.build_transaction("mgokpSJoX7npmAK1Zj8ze1926CLxYDt1iF", "1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", 10000)
        >>> claim_transaction.raw()
        "02000000012c392217483906f902e73c4bc132864de58153772d79268960998162266634be0100000000ffffffff02e80300000000000017a914971894c58d85981c16c2059d422bcde0b156d04487a6290000000000001976a9146bce65e58a50b97989930e9a4ff1ac1a77515ef188ac00000000"
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first..")
        return self._transaction.hexlify()

    def type(self) -> str:
        """
        Get Bitcoin signature transaction type.

        :returns: str -- Bitcoin signature transaction type.

        >>> from swap.providers.bitcoin.transaction import ClaimTransaction
        >>> claim_transaction = ClaimTransaction("testnet")
        >>> claim_transaction.build_transaction("mgokpSJoX7npmAK1Zj8ze1926CLxYDt1iF", "1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", 10000)
        >>> claim_transaction.type()
        "bitcoin_claim_unsigned"
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first..")
        return self._type


class FundTransaction(Transaction):
    """
    Bitcoin Fund transaction.

    :param network: Bitcoin network, defaults to testnet.
    :type network: str
    :param version: Bitcoin transaction version, defaults to 2.
    :type version: int

    :returns: FundTransaction -- Bitcoin fund transaction instance.

    .. warning::
        Do not forget to build transaction after initialize fund transaction.
    """

    def __init__(self, network: str = config["network"], version: int = config["version"]):
        super().__init__(network=network, version=version)

        self._htlc_address: Optional[str] = None
        self._utxos: Optional[list] = None
        self._previous_transaction_indexes: Optional[list] = None
        self._interest: Optional[int] = None

    def build_transaction(self, address: str, htlc_address: str,
                          amount: int, locktime: int = config["locktime"], **kwargs) -> "FundTransaction":
        """
        Build Bitcoin fund transaction.

        :param address: Bitcoin sender address.
        :type address: str
        :param htlc_address: Bitcoin Hash Time Lock Contract (HTLC) address.
        :type htlc_address: str
        :param amount: Bitcoin amount to fund.
        :type amount: int
        :param locktime: Bitcoin transaction lock time, defaults to 0.
        :type locktime: int

        :returns: FundTransaction -- Bitcoin fund transaction instance.

        >>> from swap.providers.bitcoin.transaction import FundTransaction
        >>> fund_transaction = FundTransaction("testnet")
        >>> fund_transaction.build_transaction(address="mkFWGt4hT11XS8dJKzzRFsTrqjjAwZfQAC", htlc_address="2N6kHwQy6Ph5EdKNgzGrcW2WhGHKGfmP5ae", amount=10000)
        <swap.providers.bitcoin.transaction.FundTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not is_address(address, self._network):
            raise AddressError(f"Invalid Bitcoin sender '{address}' {self._network} address.")
        if not is_address(htlc_address, self._network) and get_address_type(htlc_address) == "p2sh":
            raise AddressError(f"Invalid Bitcoin HTLC '{htlc_address}' {self._network} address.")

        self._address, self._htlc_address, self._amount = (
            address, htlc_address, amount
        )
        # Get Sender UTXO's
        self._utxos = get_utxos(
            address=self._address, network=self._network
        )

        if "options" in kwargs.keys():
            options: dict = kwargs.get("options")
            if "address" in options and "percent" in options:
                self._interest = int((self._amount * options["percent"]) / 100)
            if "fee" in options:
                self._amount = (self._amount + fee_calculator(1, 2)) if options["fee"] else self._amount
            if "interest" in options and self._interest:
                self._amount = (self._amount + (self._interest / 2)) if options["interest"] else self._amount

        # Get previous transaction indexes
        self._previous_transaction_indexes, max_amount = _get_previous_transaction_indexes(
            utxos=self._utxos, amount=(
                self._amount if not self._interest else (self._amount + (
                    self._interest if not kwargs["options"]["interest"] else (self._interest / 2)))
            ), transaction_output=(2 if not self._interest else 3)
        )
        # Build transaction inputs
        inputs, amount = _build_inputs(
            utxos=self._utxos, previous_transaction_indexes=self._previous_transaction_indexes
        )

        # Calculate the fee
        self._fee = fee_calculator(len(inputs), (
            2 if not self._interest else 3
        ))
        if amount < ((self._amount + self._fee) if not self._interest else (self._amount + self._fee + (
                self._interest if not kwargs["options"]["interest"] else (self._interest / 2)))):
            raise BalanceError("Insufficient spend UTXO's", "you don't have enough amount.")

        outputs: list = [TxOut(
            value=int(self._amount), n=0,
            script_pubkey=get_address_hash(
                address=self._htlc_address, script=True
            )
        ), TxOut(
            value=int(amount - ((self._amount + self._fee) if not self._interest else (self._amount + self._fee + (
                self._interest if not kwargs["options"]["interest"] else (self._interest / 2))))), n=1,
            script_pubkey=get_address_hash(
                address=self._address, script=True
            )
        )]
        if self._interest:
            outputs.append(TxOut(
                value=int(
                    self._interest if not kwargs["options"]["interest"] else (self._interest / 2)
                ), n=2, script_pubkey=get_address_hash(
                    address=kwargs["options"]["address"], script=True
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

        >>> from swap.providers.bitcoin.transaction import FundTransaction
        >>> from swap.providers.bitcoin.solver import FundSolver
        >>> from swap.providers.bitcoin.wallet import Wallet, DEFAULT_PATH
        >>> sender_wallet = Wallet("testnet").from_entropy("72fee73846f2d1a5807dc8c953bf79f1").from_path(DEFAULT_PATH)
        >>> fund_solver = FundSolver(sender_wallet.root_xprivate_key())
        >>> fund_transaction = FundTransaction("testnet").build_transaction(sender_wallet.address(), "2N6kHwQy6Ph5EdKNgzGrcW2WhGHKGfmP5ae", 10000)
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

        >>> from swap.providers.bitcoin.transaction import FundTransaction
        >>> fund_transaction = FundTransaction("testnet")
        >>> fund_transaction.build_transaction("mkFWGt4hT11XS8dJKzzRFsTrqjjAwZfQAC", "2N6kHwQy6Ph5EdKNgzGrcW2WhGHKGfmP5ae", 10000)
        >>> fund_transaction.transaction_raw()
        "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTJjMzkyMjE3NDgzOTA2ZjkwMmU3M2M0YmMxMzI4NjRkZTU4MTUzNzcyZDc5MjY4OTYwOTk4MTYyMjY2NjM0YmUwMTAwMDAwMDAwZmZmZmZmZmYwMmU4MDMwMDAwMDAwMDAwMDAxN2E5MTQ5NzE4OTRjNThkODU5ODFjMTZjMjA1OWQ0MjJiY2RlMGIxNTZkMDQ0ODdhNjI5MDAwMDAwMDAwMDAwMTk3NmE5MTQ2YmNlNjVlNThhNTBiOTc5ODk5MzBlOWE0ZmYxYWMxYTc3NTE1ZWYxODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiAxMjM0MCwgIm4iOiAxLCAic2NyaXB0IjogIjc2YTkxNDZiY2U2NWU1OGE1MGI5Nzk4OTkzMGU5YTRmZjFhYzFhNzc1MTVlZjE4OGFjIn1dLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfdW5zaWduZWQifQ"
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
                type=self._type
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
            type=self._type
        ))).encode()).decode())


class ClaimTransaction(Transaction):
    """
    Bitcoin Claim transaction.

    :param network: Bitcoin network, defaults to testnet.
    :type network: str
    :param version: Bitcoin transaction version, defaults to 2.
    :type version: int

    :returns: ClaimTransaction -- Bitcoin claim transaction instance.

    .. warning::
        Do not forget to build transaction after initialize claim transaction.
    """

    def __init__(self, network: str = config["network"], version: int = config["version"]):
        super().__init__(network=network, version=version)

        self._transaction_id: Optional[str] = None
        self._transaction_detail: Optional[dict] = None
        self._htlc_utxo: Optional[dict] = None

    def build_transaction(self, address: str, transaction_id: str,
                          amount: Optional[int] = None, max_amount: bool = config["max_amount"],
                          locktime: int = config["locktime"], **kwargs) -> "ClaimTransaction":
        """
        Build Bitcoin claim transaction.

        :param address: Bitcoin recipient address.
        :type address: str
        :param transaction_id: Bitcoin fund transaction id to redeem.
        :type transaction_id: str
        :param amount: Bitcoin amount to withdraw, default to None.
        :type amount: int
        :param max_amount: Bitcoin maximum amount to withdraw, default to True.
        :type max_amount: bool
        :param locktime: Bitcoin transaction lock time, defaults to 0.
        :type locktime: int

        :returns: ClaimTransaction -- Bitcoin claim transaction instance.

        >>> from swap.providers.bitcoin.transaction import ClaimTransaction
        >>> claim_transaction = ClaimTransaction("testnet")
        >>> claim_transaction.build_transaction(address="mgokpSJoX7npmAK1Zj8ze1926CLxYDt1iF", transaction_id="1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", amount=10000)
        <swap.providers.bitcoin.transaction.ClaimTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not is_address(address, self._network):
            raise AddressError(f"Invalid Bitcoin recipient '{address}' {self._network} address.")

        self._address, self._transaction_id, = address, transaction_id
        # Get transaction
        self._transaction_detail = get_transaction(
            transaction_id=self._transaction_id, network=self._network
        )
        # Find HTLC UTXO
        self._htlc_utxo = find_p2sh_utxo(transaction=self._transaction_detail)
        if self._htlc_utxo is None:
            raise ValueError("Invalid transaction id, there is no pay to script hash (P2SH) address.")

        if max_amount:
            self._amount = self._htlc_utxo["value"]
        elif amount is None:
            raise ValueError("Amount is None, Set SATOSHI amount or set maximum amount true.")
        else:
            self._amount = amount

        interest: Optional[int] = None
        if "options" in kwargs.keys():
            options: dict = kwargs.get("options")
            for transaction_output in self._transaction_detail["outputs"]:
                if transaction_output["script"] == get_address_hash(
                        address=options["address"], script=True).hexlify():
                    interest = transaction_output["value"]
        # Calculate the fee
        self._fee = fee_calculator(1, ((
            1 if self._htlc_utxo["value"] == self._amount else 2
        ) if not interest else (
            2 if self._htlc_utxo["value"] == self._amount else 3
        )))

        if self._amount < self._fee:
            raise BalanceError("Insufficient spend UTXO's", "you don't have enough amount.")
        elif self._htlc_utxo["value"] < self._amount:
            raise BalanceError("Insufficient spend UTXO's",
                               f"maximum you can withdraw {self._htlc_utxo['value']} SATOSHI amount.")

        outputs: list = [TxOut(
            value=(
                (self._amount - self._fee) if not interest else (self._amount - (self._fee + interest))
            ), n=0, script_pubkey=get_address_hash(
                address=self._address, script=True
            )
        )]
        if self._htlc_utxo["value"] != self._amount:
            outputs.append(TxOut(
                value=(
                    self._htlc_utxo["value"] - self._amount
                ), n=len(outputs), script_pubkey=P2shScript.unhexlify(
                    self._htlc_utxo["script"]
                )
            ))
        if interest:
            options: dict = kwargs.get("options")
            outputs.append(TxOut(
                value=interest, n=len(outputs), script_pubkey=get_address_hash(
                    address=options["address"], script=True
                )
            ))

        # Build mutable transaction
        self._transaction = MutableTransaction(
            version=self._version,
            ins=[TxIn(
                txid=self._transaction_id,
                txout=0, script_sig=ScriptSig.empty(),
                sequence=Sequence.max()
            )],
            outs=outputs,
            locktime=Locktime(locktime)
        )

        # Set transaction type
        self._type = "bitcoin_claim_unsigned"
        return self

    def sign(self, solver: ClaimSolver) -> "ClaimTransaction":
        """
        Sign Bitcoin claim transaction.

        :param solver: Bitcoin claim solver.
        :type solver: bitcoin.solver.ClaimSolver

        :returns: ClaimTransaction -- Bitcoin claim transaction instance.

        >>> from swap.providers.bitcoin.transaction import ClaimTransaction
        >>> from swap.providers.bitcoin.solver import ClaimSolver
        >>> from swap.providers.bitcoin.wallet import Wallet, DEFAULT_PATH
        >>> recipient_wallet = Wallet("testnet").from_mnemonic("6bc9e3bae5945876931963c2b3a3b040").from_path(DEFAULT_PATH)
        >>> bytecode = "63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a9140e259e08f2ec9fc99a92b6f66fdfcb3c7914fd6888ac6702e803b27576a91433ecab3d67f0e2bde43e52f41ec1ecbdc73f11f888ac68"
        >>> claim_solver = ClaimSolver(recipient_wallet.root_xprivate_key(), "Hello Meheret!", bytecode)
        >>> claim_transaction = ClaimTransaction("testnet")
        >>> claim_transaction.build_transaction(recipient_wallet.address(), "1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", 10000)
        >>> claim_transaction.sign(solver=claim_solver)
        <swap.providers.bitcoin.transaction.ClaimTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not isinstance(solver, ClaimSolver):
            raise TypeError(f"Solver must be Bitcoin ClaimSolver, not {type(solver).__name__} type.")
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")

        self._transaction.spend([
            TxOut(
                value=self._htlc_utxo["value"],
                n=0,
                script_pubkey=P2shScript.unhexlify(
                    hex_string=self._htlc_utxo["script"]
                )
            )
        ], [
            P2shSolver(
                redeem_script=solver.witness(
                    network=self._network
                ),
                redeem_script_solver=solver.solve(
                    network=self._network
                )
            )
        ])

        # Set transaction type
        self._type = "bitcoin_claim_signed"
        return self

    def transaction_raw(self) -> str:
        """
        Get Bitcoin claim transaction raw.

        :returns: str -- Bitcoin claim transaction raw.

        >>> from swap.providers.bitcoin.transaction import ClaimTransaction
        >>> claim_transaction = ClaimTransaction("testnet")
        >>> claim_transaction.build_transaction("mgokpSJoX7npmAK1Zj8ze1926CLxYDt1iF", "1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", 10000)
        >>> claim_transaction.transaction_raw()
        "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTJjMzkyMjE3NDgzOTA2ZjkwMmU3M2M0YmMxMzI4NjRkZTU4MTUzNzcyZDc5MjY4OTYwOTk4MTYyMjY2NjM0YmUwMTAwMDAwMDAwZmZmZmZmZmYwMmU4MDMwMDAwMDAwMDAwMDAxN2E5MTQ5NzE4OTRjNThkODU5ODFjMTZjMjA1OWQ0MjJiY2RlMGIxNTZkMDQ0ODdhNjI5MDAwMDAwMDAwMDAwMTk3NmE5MTQ2YmNlNjVlNThhNTBiOTc5ODk5MzBlOWE0ZmYxYWMxYTc3NTE1ZWYxODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiAxMjM0MCwgIm4iOiAxLCAic2NyaXB0IjogIjc2YTkxNDZiY2U2NWU1OGE1MGI5Nzk4OTkzMGU5YTRmZjFhYzFhNzc1MTVlZjE4OGFjIn1dLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfdW5zaWduZWQifQ"
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")

        # Encode claim transaction raw
        if self._type == "bitcoin_claim_signed":
            return clean_transaction_raw(b64encode(str(json.dumps(dict(
                raw=self._transaction.hexlify(),
                fee=self._fee,
                network=self._network,
                type=self._type
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
            type=self._type
        ))).encode()).decode())


class RefundTransaction(Transaction):
    """
    Bitcoin Refund transaction.

    :param network: Bitcoin network, defaults to testnet.
    :type network: str
    :param version: Bitcoin transaction version, defaults to 2.
    :type version: int

    :returns: RefundTransaction -- Bitcoin refund transaction instance.

    .. warning::
        Do not forget to build transaction after initialize refund transaction.
    """

    def __init__(self, network: str = config["network"], version: int = config["version"]):
        super().__init__(network=network, version=version)

        self._transaction_id: Optional[str] = None
        self._transaction_detail: Optional[list] = None
        self._htlc_utxo: Optional[dict] = None

    def build_transaction(self, address: str, transaction_id: str,
                          amount: Optional[int] = None, max_amount: bool = config["max_amount"],
                          locktime: int = config["locktime"], **kwargs) -> "RefundTransaction":
        """
        Build Bitcoin refund transaction.

        :param address: Bitcoin sender address.
        :type address: str
        :param transaction_id: Bitcoin fund transaction id to redeem.
        :type transaction_id: str
        :param amount: Bitcoin amount to withdraw, default to None.
        :type amount: int
        :param max_amount: Bitcoin maximum amount to withdraw, default to True.
        :type max_amount: bool
        :param locktime: Bitcoin transaction lock time, defaults to 0.
        :type locktime: int

        :returns: RefundTransaction -- Bitcoin refund transaction instance.

        >>> from swap.providers.bitcoin.transaction import RefundTransaction
        >>> refund_transaction = RefundTransaction("testnet")
        >>> refund_transaction.build_transaction(address="mkFWGt4hT11XS8dJKzzRFsTrqjjAwZfQAC", transaction_id="1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", amount=10000)
        <swap.providers.bitcoin.transaction.RefundTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not is_address(address, self._network):
            raise AddressError(f"Invalid Bitcoin sender '{address}' {self._network} address.")

        self._address, self._transaction_id, = address, transaction_id
        # Get transaction
        self._transaction_detail = get_transaction(
            transaction_id=self._transaction_id, network=self._network
        )
        # Find HTLC UTXO
        self._htlc_utxo = find_p2sh_utxo(transaction=self._transaction_detail)
        if self._htlc_utxo is None:
            raise ValueError("Invalid transaction id, there is no pay to script hash (P2SH) address.")

        if max_amount:
            self._amount = self._htlc_utxo["value"]
        elif amount is None:
            raise ValueError("Amount is None, Set SATOSHI amount or set maximum amount true.")
        else:
            self._amount = amount

        interest: Optional[int] = None
        if "options" in kwargs.keys():
            options: dict = kwargs.get("options")
            for transaction_output in self._transaction_detail["outputs"]:
                if transaction_output["script"] == get_address_hash(
                        address=options["address"], script=True).hexlify():
                    interest = transaction_output["value"]

        # Calculate the fee
        self._fee = fee_calculator(1, ((
           1 if self._htlc_utxo["value"] == self._amount else 2
       ) if not interest else (
            2 if self._htlc_utxo["value"] == self._amount else 3
        )))

        if self._amount < self._fee:
            raise BalanceError("Insufficient spend UTXO's", "you don't have enough amount.")
        elif self._htlc_utxo["value"] < self._amount:
            raise BalanceError("Insufficient spend UTXO's",
                               f"maximum you can refund {self._htlc_utxo['value']} SATOSHI amount.")

        outputs: list = [TxOut(
            value=(
                (self._amount - self._fee) if not interest else (self._amount - (self._fee + interest))
            ), n=0, script_pubkey=get_address_hash(
                address=self._address, script=True
            )
        )]
        if self._htlc_utxo["value"] != self._amount:
            outputs.append(TxOut(
                value=(
                        self._htlc_utxo["value"] - self._amount
                ), n=len(outputs), script_pubkey=P2shScript.unhexlify(
                    self._htlc_utxo["script"]
                )
            ))
        if interest:
            options: dict = kwargs.get("options")
            outputs.append(TxOut(
                value=interest, n=len(outputs), script_pubkey=get_address_hash(
                    address=options["address"], script=True
                )
            ))

        # Build mutable transaction
        self._transaction = MutableTransaction(
            version=self._version,
            ins=[TxIn(
                txid=self._transaction_id,
                txout=0, script_sig=ScriptSig.empty(),
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
        >>> from swap.providers.bitcoin.solver import RefundSolver
        >>> from swap.providers.bitcoin.wallet import Wallet, DEFAULT_PATH
        >>> sender_wallet = Wallet("testnet").from_entropy("72fee73846f2d1a5807dc8c953bf79f1").from_path(DEFAULT_PATH)
        >>> bytecode = "63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a9140e259e08f2ec9fc99a92b6f66fdfcb3c7914fd6888ac6702e803b27576a91433ecab3d67f0e2bde43e52f41ec1ecbdc73f11f888ac68"
        >>> refund_solver = RefundSolver(sender_wallet.root_xprivate_key(), bytecode, sequence=1000)
        >>> refund_transaction = RefundTransaction("testnet")
        >>> refund_transaction.build_transaction(sender_wallet.address(), "1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", 10000)
        >>> refund_transaction.sign(solver=refund_solver)
        <swap.providers.bitcoin.transaction.RefundTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not isinstance(solver, RefundSolver):
            raise TypeError(f"Solver must be Bitcoin RefundSolver, not {type(solver).__name__} type.")
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")

        self._transaction.spend([
            TxOut(
                value=self._htlc_utxo["value"],
                n=0,
                script_pubkey=P2shScript.unhexlify(
                    hex_string=self._htlc_utxo["script"]
                )
            )
        ], [
            P2shSolver(
                redeem_script=solver.witness(
                    network=self._network
                ),
                redeem_script_solver=solver.solve(
                    network=self._network
                )
            )
        ])

        # Set transaction type
        self._type = "bitcoin_refund_signed"
        return self

    def transaction_raw(self) -> str:
        """
        Get Bitcoin refund transaction raw.

        :returns: str -- Bitcoin refund transaction raw.

        >>> from swap.providers.bitcoin.transaction import RefundTransaction
        >>> refund_transaction = RefundTransaction("testnet")
        >>> refund_transaction.build_transaction("mkFWGt4hT11XS8dJKzzRFsTrqjjAwZfQAC", "1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", 10000)
        >>> refund_transaction.transaction_raw()
        "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTJjMzkyMjE3NDgzOTA2ZjkwMmU3M2M0YmMxMzI4NjRkZTU4MTUzNzcyZDc5MjY4OTYwOTk4MTYyMjY2NjM0YmUwMTAwMDAwMDAwZmZmZmZmZmYwMmU4MDMwMDAwMDAwMDAwMDAxN2E5MTQ5NzE4OTRjNThkODU5ODFjMTZjMjA1OWQ0MjJiY2RlMGIxNTZkMDQ0ODdhNjI5MDAwMDAwMDAwMDAwMTk3NmE5MTQ2YmNlNjVlNThhNTBiOTc5ODk5MzBlOWE0ZmYxYWMxYTc3NTE1ZWYxODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiAxMjM0MCwgIm4iOiAxLCAic2NyaXB0IjogIjc2YTkxNDZiY2U2NWU1OGE1MGI5Nzk4OTkzMGU5YTRmZjFhYzFhNzc1MTVlZjE4OGFjIn1dLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfdW5zaWduZWQifQ"
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
                type=self._type
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
            type=self._type
        ))).encode()).decode())
