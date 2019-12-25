#!/usr/bin/env python3

from btcpy.structs.transaction import Locktime, MutableTransaction
from btcpy.structs.sig import P2pkhSolver


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
