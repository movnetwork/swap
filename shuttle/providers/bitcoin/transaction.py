#!/usr/bin/env python3

from base64 import b64encode, b64decode
from btcpy.structs.address import Address
from btcpy.structs.script import ScriptSig, Script, P2pkhScript, P2shScript
from btcpy.structs.transaction import Locktime, MutableTransaction, TxOut, Sequence, TxIn
from btcpy.structs.sig import P2pkhSolver, P2shSolver
from btcpy.setup import setup

import json

from .utils import double_sha256, fee_calculator
from .solver import ClaimSolver, FundSolver, RefundSolver
from .rpc import get_transaction_detail
from .htlc import HTLC
from .wallet import Wallet


class Transaction:
    # Initialization transaction
    def __init__(self, version=2, network="testnet"):
        # Transaction build version
        self.version = version
        # Transaction
        self.transaction = None
        # Bitcoin network
        self.network = network
        # Setting testnet
        setup(network, strict=True)

    # Building transaction
    def build_transaction(self, previous_transaction_inputs: list, transaction_outputs: list, locktime=0):
        # Building mutable bitcoin transaction
        self.transaction = MutableTransaction(version=self.version, ins=previous_transaction_inputs,
                                              outs=transaction_outputs, locktime=Locktime(locktime))
        return self

    # Signing transaction using private keys
    def sign(self, previous_transaction_outputs: list, solver: list):
        self.transaction.spend(previous_transaction_outputs, solver)
        return self

    # Transaction hash
    def hash(self):
        if self.transaction is None:
            raise ValueError("Transaction script is none, Please build transaction first.")
        return self.transaction.txid

    # Transaction json format
    def json(self):
        if self.transaction is None:
            raise ValueError("Transaction script is none, Please build transaction first.")
        return self.transaction.to_json()

    # Transaction raw
    def raw(self):
        if self.transaction is None:
            raise ValueError("Transaction script is none, Please build transaction first.")
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

    def __init__(self, wallet: Wallet, htlc: HTLC, amount: int, network="testnet", version=2):
        super().__init__(network=network, version=version)
        # Bitcoin sender wallet
        assert isinstance(wallet, Wallet), "Invalid Bitcoin Wallet!"
        self.wallet = wallet
        # Bitcoin sender hash time lock contract
        assert isinstance(htlc, HTLC), "Invalid Bitcoin HTLC script!"
        self.htlc = htlc
        # Bitcoin sender fund amount
        self.amount = amount
        # Bitcoin sender unspent transactions
        self.unspent = self.wallet.unspent()
        # Get previous transaction indexes using funding amount
        self.previous_transaction_indexes = self.get_previous_transaction_indexes()

    # Building transaction
    def build_transaction(self, locktime=0, **kwargs):
        inputs, amount = self.inputs(self.unspent, self.previous_transaction_indexes)
        # Building mutable bitcoin transaction
        self.transaction = MutableTransaction(
            version=self.version, ins=inputs,
            outs=[
                # Funding into hash time lock contract script hash
                TxOut(value=self.amount, n=0,
                      script_pubkey=P2shScript.unhexlify(self.htlc.hash())),
                # Controlling amounts when we are funding on htlc script.
                TxOut(value=amount - (fee_calculator(len(inputs), 2) + self.amount), n=1,
                      script_pubkey=P2pkhScript.unhexlify(self.wallet.p2pkh()))
            ], locktime=Locktime(locktime))
        return self

    # Signing transaction using private keys
    def sign(self, solver: FundSolver, **kwargs):
        if not isinstance(solver, FundSolver):
            raise Exception("Solver error")
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
        if self.transaction is None:
            raise ValueError("Transaction script is none, Please build transaction first.")
        for index, utxo in enumerate(self.unspent):
            if self.previous_transaction_indexes is None or index in self.previous_transaction_indexes:
                outputs.append(dict(amount=utxo["amount"],
                               n=utxo["output_index"], script=utxo["script"]))
        return b64encode(str(json.dumps(dict(
            raw=self.transaction.hexlify(), outputs=outputs, type="fund_unsigned"
        ))).encode()).decode()


class ClaimTransaction(Transaction):

    def __init__(self, htlc_hash, wallet: Wallet, network="testnet", version=2):
        super().__init__(network=network, version=version)
        # Bitcoin sender wallet
        assert isinstance(wallet, Wallet), "Invalid Bitcoin Wallet!"
        self.wallet = wallet
        self.htlc_transaction_id = htlc_hash
        self.htlc_transaction_detail = get_transaction_detail(self.htlc_transaction_id)
        mainnet = True if self.network == "mainnet" else False
        if "outputs" not in self.htlc_transaction_detail:
            raise Exception("Not found HTLC in this %s hash" % self.htlc_transaction_id)

        self.htlc = self.htlc_transaction_detail["outputs"][0]
        self.htlc_value = self.htlc["value"]  # Funded amount
        self.htlc_script = P2shScript.unhexlify(self.htlc["script"])
        self.htlc_address = self.htlc_script.address(mainnet=mainnet)
        self.sender_script = P2pkhScript.unhexlify(self.htlc_transaction_detail["outputs"][1]["script"])
        self.sender_address = self.sender_script.address(mainnet=mainnet)

    # Building transaction
    def build_transaction(self, locktime=0, **kwargs):
        # Building mutable bitcoin transaction
        self.transaction = MutableTransaction(
            version=self.version,
            ins=[
                TxIn(txid=self.htlc_transaction_id, txout=0,
                     script_sig=ScriptSig.empty(), sequence=Sequence.max())
            ],
            outs=[
                TxOut(value=self.htlc_value - fee_calculator(1, 1), n=0,
                      script_pubkey=P2pkhScript.unhexlify(self.wallet.p2pkh()))
            ], locktime=Locktime(locktime))
        return self

    # Signing transaction using private keys
    def sign(self, solver: ClaimSolver, **kwargs):
        if not isinstance(solver, ClaimSolver):
            raise Exception("Invalid solver error, only take claim solver.")
        htlc = HTLC(self.network).init(
            secret_hash=double_sha256(solver.secret),
            recipient_address=str(self.wallet.address()),
            sender_address=str(self.sender_address),
            sequence=solver.sequence
        )
        self.transaction.spend([
            TxOut(value=self.htlc_value, n=0, script_pubkey=self.htlc_script)
        ], [
            P2shSolver(htlc.script, solver.solve())
        ])
        return self

    def unsigned_raw(self):
        if self.transaction is None:
            raise ValueError("Transaction script is none, Please build transaction first.")
        outputs = [dict(amount=self.htlc_value, n=0, script=self.htlc["script"])]
        return b64encode(str(json.dumps(dict(
            raw=self.transaction.hexlify(), outputs=outputs, type="claim_unsigned",
            recipient=str(self.wallet.address()), sender=str(self.sender_address)
        ))).encode()).decode()


class RefundTransaction(Transaction):

    def __init__(self, htlc_hash, wallet: Wallet, network="testnet", version=2):
        super().__init__(network=network, version=version)
        # Bitcoin sender wallet
        assert isinstance(wallet, Wallet), "Invalid Bitcoin Wallet!"
        self.wallet = wallet
        self.htlc_transaction_id = htlc_hash
        self.htlc_transaction_detail = get_transaction_detail(self.htlc_transaction_id)
        mainnet = True if self.network == "mainnet" else False
        if "outputs" not in self.htlc_transaction_detail:
            raise Exception("Not found HTLC in this %s hash" % self.htlc_transaction_id)

        self.htlc = self.htlc_transaction_detail["outputs"][0]
        self.htlc_value = self.htlc["value"]  # Funded amount
        self.htlc_script = P2shScript.unhexlify(self.htlc["script"])
        self.htlc_address = self.htlc_script.address(mainnet=mainnet)
        self.sender_script = P2pkhScript.unhexlify(self.htlc_transaction_detail["outputs"][1]["script"])
        self.sender_address = self.sender_script.address(mainnet=mainnet)

    # Building transaction
    def build_transaction(self, locktime=0, **kwargs):
        # Building mutable bitcoin transaction
        self.transaction = MutableTransaction(
            version=self.version,
            ins=[
                TxIn(txid=self.htlc_transaction_id, txout=0,
                     script_sig=ScriptSig.empty(), sequence=Sequence.max())
            ],
            outs=[
                TxOut(value=self.htlc_value - fee_calculator(1, 1), n=0,
                      script_pubkey=P2pkhScript.unhexlify(self.wallet.p2pkh()))
            ], locktime=Locktime(locktime))
        return self

    # Signing transaction using private keys
    def sign(self, solver: RefundSolver, **kwargs):
        if not isinstance(solver, RefundSolver):
            raise Exception("Solver error")
        htlc = HTLC(self.network).init(
            secret_hash=double_sha256(solver.secret),
            recipient_address=str(self.wallet.address()),
            sender_address=str(self.sender_address),
            sequence=solver.sequence
        )
        self.transaction.spend([
            TxOut(value=self.htlc_value, n=0, script_pubkey=self.htlc_script)
        ], [
            P2shSolver(htlc.script, solver.solve())
        ])
        return self

    def unsigned_raw(self):
        if self.transaction is None:
            raise ValueError("Transaction script is none, Please build transaction first.")
        outputs = [dict(amount=self.htlc_value, n=0, script=self.htlc["script"])]
        return b64encode(str(json.dumps(dict(
            raw=self.transaction.hexlify(), outputs=outputs, type="refund_unsigned",
            recipient=str(self.wallet.address()), sender=str(self.sender_address)
        ))).encode()).decode()
