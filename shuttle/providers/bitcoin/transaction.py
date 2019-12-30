#!/usr/bin/env python3
from btcpy.structs.address import Address
from btcpy.structs.script import ScriptSig, Script, P2pkhScript, P2shScript
from btcpy.structs.transaction import Locktime, MutableTransaction, TxOut, Sequence, TxIn
from btcpy.structs.sig import P2pkhSolver
from btcpy.setup import setup

from .utils import is_address, fee_calculator
from .solver import ClaimSolver
from .rpc import get_unspent_transactions
from .htlc import HTLC
from .wallet import Wallet


class Transaction:
    # Initialization transaction
    def __init__(self, version=2, network="testnet"):
        # Transaction build version
        self.version = version
        # Transaction
        self.transaction = None
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

    def __init__(self, wallet: Wallet, htlc: HTLC, amount: int, version=2):
        super().__init__(version)
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
    def sign(self, solver, **kwargs):
        outputs = self.outputs(self.unspent, self.previous_transaction_indexes)
        self.transaction.spend(outputs, [solver for output in outputs])
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
