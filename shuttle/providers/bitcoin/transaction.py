#!/usr/bin/env python3

from base64 import b64encode, b64decode
from btcpy.structs.address import Address
from btcpy.structs.script import ScriptSig, Script, P2pkhScript, P2shScript
from btcpy.structs.transaction import Locktime, MutableTransaction, TxOut, Sequence, TxIn
from btcpy.structs.sig import P2shSolver
from btcpy.setup import setup

import json

from .utils import double_sha256, fee_calculator
from .solver import ClaimSolver, FundSolver, RefundSolver
from .rpc import get_transaction_detail
from .htlc import HTLC
from .wallet import Wallet
from ...utils.exceptions import BalanceError, NotFoundError


class Transaction:
    # Initialization transaction
    def __init__(self, version=2, network="testnet"):
        # Transaction build version
        self.version = version
        # Transaction
        self.transaction = None
        # Bitcoin network
        self.mainnet = None
        self.network = network
        if self.network == "mainnet":
            self.mainnet = True
        elif self.network == "testnet":
            self.mainnet = False
        else:
            raise ValueError("invalid network, only mainnet or testnet")
        # Bitcoin fee
        self.fee = int()
        # Setting testnet
        setup(network, strict=True)

    # Transaction hash
    def hash(self):
        if self.transaction is None:
            raise ValueError("transaction script is none, Please build transaction first.")
        return self.transaction.txid

    # Transaction json format
    def json(self):
        if self.transaction is None:
            raise ValueError("transaction script is none, Please build transaction first.")
        return self.transaction.to_json()

    # Transaction raw
    def raw(self):
        if self.transaction is None:
            raise ValueError("transaction script is none, Please build transaction first.")
        return self.transaction.hexlify()

    @staticmethod
    def inputs(utxos, previous_transaction_indexes=None):
        inputs, amount = list(), int()
        for index, utxo in enumerate(utxos):
            if previous_transaction_indexes is None or index in previous_transaction_indexes:
                amount += utxo["amount"]
                inputs.append(
                    TxIn(txid=utxo["hash"], txout=utxo["output_index"],
                         script_sig=ScriptSig.empty(), sequence=Sequence.max()))
        return inputs, amount

    @staticmethod
    def outputs(utxos, previous_transaction_indexes=None):
        outputs = list()
        for index, utxo in enumerate(utxos):
            if previous_transaction_indexes is None or index in previous_transaction_indexes:
                outputs.append(
                    TxOut(value=utxo["amount"], n=utxo["output_index"],
                          script_pubkey=Script.unhexlify(utxo["script"])))
        return outputs


class FundTransaction(Transaction):

    # Initialization fund transaction
    def __init__(self, version=2, network="testnet"):
        super().__init__(version=version, network=network)
        # Initialization wallet, htlc, amount and unspent
        self.wallet, self.htlc, self.amount, self.unspent = None, None, None, None
        # Getting previous transaction indexes using funding amount
        self.previous_transaction_indexes = None

    # Building transaction
    def build_transaction(self, wallet: Wallet, htlc: HTLC, amount: int, locktime=0):
        # Checking build transaction arguments instance
        if not isinstance(wallet, Wallet):
            raise TypeError("invalid wallet instance, only takes bitcoin Wallet class")
        if not isinstance(htlc, HTLC):
            raise TypeError("invalid htlc instance, only takes bitcoin HTLC class")
        if not isinstance(amount, int):
            raise TypeError("invalid amount instance, only takes integer type")
        # Setting wallet, htlc, amount and unspent
        self.wallet, self.htlc, self.amount = wallet, htlc, amount
        # Getting unspent transaction output
        self.unspent = self.wallet.unspent()
        # Setting previous transaction indexes
        self.previous_transaction_indexes = \
            self.get_previous_transaction_indexes(amount=self.amount)
        # Getting transaction inputs and amount
        inputs, amount = self.inputs(self.unspent, self.previous_transaction_indexes)
        # Calculating bitcoin fee
        self.fee = fee_calculator(len(inputs), 2)
        if amount < (self.amount + self.fee):
            raise BalanceError("insufficient spend utxos")
        # Building mutable bitcoin transaction
        self.transaction = MutableTransaction(
            version=self.version, ins=inputs,
            outs=[
                # Funding into hash time lock contract script hash
                TxOut(value=self.amount, n=0,
                      script_pubkey=P2shScript.unhexlify(self.htlc.hash())),
                # Controlling amounts when we are funding on htlc script.
                TxOut(value=amount - (self.fee + self.amount), n=1,
                      script_pubkey=P2pkhScript.unhexlify(self.wallet.p2pkh()))
            ], locktime=Locktime(locktime))
        return self

    # Signing transaction using fund solver
    def sign(self, solver: FundSolver):
        if not isinstance(solver, FundSolver):
            raise TypeError("invalid solver instance, only takes bitcoin FundSolver class")
        if not self.unspent or not self.previous_transaction_indexes or not self.transaction:
            raise ValueError("transaction script or unspent is none, build transaction first")
        outputs = self.outputs(self.unspent, self.previous_transaction_indexes)
        self.transaction.spend(outputs, [solver.solve() for _ in outputs])
        return self

    # Automatically analysis previous transaction indexes using fund amount
    def get_previous_transaction_indexes(self, amount=None):
        if amount is None:
            amount = self.amount
        temp_amount = int()
        previous_transaction_indexes = list()
        for index, unspent in enumerate(self.unspent):
            temp_amount += unspent["amount"]
            if temp_amount > (amount + fee_calculator((index + 1), 2)):
                previous_transaction_indexes.append(index)
                break
            previous_transaction_indexes.append(index)
        return previous_transaction_indexes

    def unsigned_raw(self):
        outputs = list()
        if not self.transaction or not self.unspent:
            raise ValueError("transaction script or unspent is none, build transaction first")
        for index, utxo in enumerate(self.unspent):
            if self.previous_transaction_indexes is None or index in self.previous_transaction_indexes:
                outputs.append(dict(amount=utxo["amount"],
                               n=utxo["output_index"], script=utxo["script"]))
        return b64encode(str(json.dumps(dict(
            fee=self.fee,
            raw=self.transaction.hexlify(),
            outputs=outputs,
            type="fund_unsigned"
        ))).encode()).decode()


class ClaimTransaction(Transaction):

    # Initialization claim transaction
    def __init__(self, network="testnet", version=2):
        super().__init__(network=network, version=version)
        # Initialization transaction_id, wallet and amount
        self.transaction_id, self.wallet, self.amount = None, None, None
        # Getting transaction detail by id
        self.transaction_detail = None
        # Transaction detail outputs (HTLC and Sender account)
        self.htlc = None
        self.sender_account: Wallet = None

    # Building transaction
    def build_transaction(self, transaction_id: str, wallet: Wallet, amount: int, locktime=0):
        # Checking build transaction arguments instance
        if not isinstance(transaction_id, str):
            raise TypeError("invalid amount instance, only takes string type")
        if not isinstance(wallet, Wallet):
            raise TypeError("invalid wallet instance, only takes bitcoin Wallet class")
        # Setting transaction_id and wallet
        self.transaction_id, self.wallet = transaction_id, wallet
        # Getting transaction detail by id
        self.transaction_detail = get_transaction_detail(self.transaction_id)
        # Checking transaction outputs
        if "outputs" not in self.transaction_detail:
            raise NotFoundError("not found htlc in this %s hash" % self.transaction_id)
        # Hash time lock contract output
        self.htlc = self.transaction_detail["outputs"][0]
        # Sender account output
        sender_address = P2pkhScript.unhexlify(
            self.transaction_detail["outputs"][1]["script"]).address(mainnet=self.mainnet)
        self.sender_account = Wallet(network=self.network).from_address(str(sender_address))
        # HTLC info's
        htlc_amount = self.htlc["value"]
        htlc_script = P2shScript.unhexlify(self.htlc["script"])
        htlc_address = htlc_script.address(mainnet=self.mainnet)
        # Calculating fee
        self.fee = fee_calculator(1, 1)
        if amount < self.fee:
            raise BalanceError("insufficient spend utxos")
        elif not htlc_amount >= (amount - self.fee):
            raise BalanceError("insufficient spend utxos", "maximum withdraw %d" % htlc_amount)
        # Building mutable bitcoin transaction
        self.transaction = MutableTransaction(
            version=self.version,
            ins=[
                TxIn(txid=self.transaction_id, txout=0,
                     script_sig=ScriptSig.empty(), sequence=Sequence.max())
            ],
            outs=[
                TxOut(value=(amount - self.fee), n=0,
                      script_pubkey=P2pkhScript.unhexlify(self.wallet.p2pkh()))
            ], locktime=Locktime(locktime))
        return self

    # Signing transaction using private keys
    def sign(self, solver: ClaimSolver):
        if not isinstance(solver, ClaimSolver):
            raise TypeError("invalid solver instance, only takes bitcoin ClaimSolver class")
        if self.transaction is None:
            raise ValueError("transaction script is none, build transaction first")
        htlc = HTLC(self.network).init(
            secret_hash=double_sha256(solver.secret),
            recipient_address=str(self.wallet.address()),
            sender_address=str(self.sender_account.address()),
            sequence=solver.sequence
        )
        self.transaction.spend([
            TxOut(value=self.htlc["value"], n=0,
                  script_pubkey=P2shScript.unhexlify(self.htlc["script"]))
        ], [
            P2shSolver(htlc.script, solver.solve())
        ])
        return self

    def unsigned_raw(self):
        if self.transaction is None:
            raise ValueError("transaction script is none, build transaction first")
        outputs = [dict(amount=self.htlc["value"], n=0, script=self.htlc["script"])]
        return b64encode(str(json.dumps(dict(
            fee=self.fee,
            raw=self.transaction.hexlify(),
            outputs=outputs,
            recipient_address=str(self.wallet.address()),
            sender_address=str(self.sender_account.address()),
            type="claim_unsigned"
        ))).encode()).decode()


class RefundTransaction(Transaction):

    # Initialization claim transaction
    def __init__(self, version=2, network="testnet"):
        super().__init__(version=version, network=network)
        # Initialization transaction_id, wallet and amount
        self.transaction_id, self.wallet, self.amount = None, None, None
        # Getting transaction detail by id
        self.transaction_detail = None
        # Transaction detail outputs (HTLC and Sender account)
        self.htlc = None
        self.sender_account: Wallet = None

    # Building transaction
    def build_transaction(self, transaction_id: str, wallet: Wallet, amount: int, locktime=0):
        # Checking build transaction arguments instance
        if not isinstance(transaction_id, str):
            raise TypeError("invalid amount instance, only takes string type")
        if not isinstance(wallet, Wallet):
            raise TypeError("invalid wallet instance, only takes bitcoin Wallet class")
        # Setting transaction_id and wallet
        self.transaction_id, self.wallet = transaction_id, wallet
        # Getting transaction detail by id
        self.transaction_detail = get_transaction_detail(self.transaction_id)
        # Checking transaction outputs
        if "outputs" not in self.transaction_detail:
            raise NotFoundError("not found htlc in this %s hash" % self.transaction_id)
        # Hash time lock contract output
        self.htlc = self.transaction_detail["outputs"][0]
        # Sender account output
        sender_address = P2pkhScript.unhexlify(
            self.transaction_detail["outputs"][1]["script"]).address(mainnet=self.mainnet)
        self.sender_account = Wallet(network=self.network).from_address(str(sender_address))
        # HTLC info's
        htlc_amount = self.htlc["value"]
        htlc_script = P2shScript.unhexlify(self.htlc["script"])
        htlc_address = htlc_script.address(mainnet=self.mainnet)
        # Calculating fee
        self.fee = fee_calculator(1, 1)
        if amount < self.fee:
            raise BalanceError("insufficient spend utxos")
        elif not htlc_amount >= (amount - self.fee):
            raise BalanceError("insufficient spend utxos", "maximum withdraw %d" % htlc_amount)
        # Building mutable bitcoin transaction
        self.transaction = MutableTransaction(
            version=self.version,
            ins=[
                TxIn(txid=self.transaction_id, txout=0,
                     script_sig=ScriptSig.empty(), sequence=Sequence.max())
            ],
            outs=[
                TxOut(value=(amount - self.fee), n=0,
                      script_pubkey=P2pkhScript.unhexlify(self.wallet.p2pkh()))
            ], locktime=Locktime(locktime))
        return self

    # Signing transaction using private keys
    def sign(self, solver: RefundSolver):
        if not isinstance(solver, RefundSolver):
            raise TypeError("invalid solver instance, only takes bitcoin RefundSolver class")
        if self.transaction is None:
            raise ValueError("transaction script is none, build transaction first")
        htlc = HTLC(self.network).init(
            secret_hash=double_sha256(solver.secret),
            recipient_address=str(self.wallet.address()),
            sender_address=str(self.sender_account.address()),
            sequence=solver.sequence
        )
        self.transaction.spend([
            TxOut(value=self.htlc["value"], n=0,
                  script_pubkey=P2shScript.unhexlify(self.htlc["script"]))
        ], [
            P2shSolver(htlc.script, solver.solve())
        ])
        return self

    def unsigned_raw(self):
        if self.transaction is None:
            raise ValueError("transaction script is none, build transaction first")
        outputs = [dict(amount=self.htlc["value"], n=0, script=self.htlc["script"])]
        return b64encode(str(json.dumps(dict(
            fee=self.fee,
            raw=self.transaction.hexlify(),
            outputs=outputs,
            recipient_address=str(self.wallet.address()),
            sender_address=str(self.sender_account.address()),
            type="refund_unsigned"
        ))).encode()).decode()
