#!/usr/bin/env python3
from btcpy.structs.script import ScriptSig, Script
from btcpy.structs.transaction import Locktime, MutableTransaction, TxIn, Sequence, TxOut
from btcpy.structs.sig import P2pkhSolver

from .utils import is_address
from .rpc import get_unspent_transactions


def list_previous_transaction(address, limit=50, network="testnet"):
    assert is_address(address, network), "Invalid %s address!"
    previous_transactions = list()
    unspent_transactions = get_unspent_transactions(address, network, limit=limit)
    for index, unspent_transaction in enumerate(unspent_transactions):
        previous_transactions.append(dict(
            index=index,
            hash=unspent_transaction["tx_hash"],
            output_index=unspent_transaction["tx_output_n"],
            balance=unspent_transaction["value"],
            script=unspent_transaction["script"]
        ))
    return previous_transactions


def build_previous_transaction_inputs(address, previous_indexes=None, network="testnet"):
    assert is_address(address, network), "Invalid %s address!"
    if previous_indexes is not None:
        assert isinstance(previous_indexes, list), "Previous indexes must be list format."
    previous_transaction_inputs = list()
    unspent_transactions = get_unspent_transactions(address, network)
    for index, unspent_transaction in enumerate(unspent_transactions):
        if previous_indexes is None or index in previous_indexes:
            previous_transaction_inputs.append(
                TxIn(txid=unspent_transaction["tx_hash"], txout=unspent_transaction["tx_output_n"],
                     script_sig=ScriptSig.empty(), sequence=Sequence.max()))
    return previous_transaction_inputs


def build_previous_transaction_outputs(address, previous_indexes=None, network="testnet"):
    assert is_address(address, network), "Invalid %s address!"
    if previous_indexes is not None:
        assert isinstance(previous_indexes, list), "Previous indexes must be list format."
    previous_transaction_outputs = list()
    unspent_transactions = get_unspent_transactions(address, network)
    for index, unspent_transaction in enumerate(unspent_transactions):
        if previous_indexes is None or index in previous_indexes:
            previous_transaction_outputs.append(
                TxOut(value=unspent_transaction["value"], n=unspent_transaction["tx_output_n"],
                      script_pubkey=Script.unhexlify(unspent_transaction["script"])))
    return previous_transaction_outputs


class Transaction:
    # Initialization transaction
    def __init__(self, version=1):
        # Transaction build version
        self.version = version
        # Transaction
        self.transaction = None

    # Building transaction
    def build_transaction(self, previous_transaction_inputs: list, transaction_outputs: list, locktime=0):
        # Building mutable bitcoin transaction
        self.transaction = MutableTransaction(version=self.version, ins=previous_transaction_inputs,
                                              outs=transaction_outputs, locktime=Locktime(locktime))
        return self

    # Signing transaction using private keys
    def sign(self, previous_transaction_outputs: list, private_keys: list):
        private_keys_solver = [P2pkhSolver(private_key) for private_key in private_keys]
        self.transaction.spend(previous_transaction_outputs, private_keys_solver)
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
