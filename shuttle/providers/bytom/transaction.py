#!/usr/bin/env python3


from .rpc import build_transaction
from ..config import bytom

# Bytom configuration
bytom = bytom()


class Transaction:

    # Initialization transaction
    def __init__(self, network="testnet", guid=None, inputs=None, outputs=None):
        # Transaction
        self.transaction = None
        # Bitcoin network
        self.network = network
        # Input and Output actions
        self.inputs, self.outputs = inputs, outputs
        # GUID
        self.guid = guid

    # Building bytom transaction
    def build_transaction(self, *args, **kwargs):

        if not self.guid and not self.inputs or not self.outputs:
            raise ValueError("Transaction fail | GUID, Inputs or Outputs are none.")

        # Transaction
        tx = dict(
            guid=self.guid,
            inputs=self.inputs,
            outputs=self.outputs,
            fee=bytom["fee"],
            confirmations=bytom["confirmations"]
        )
        # Building transaction
        self.transaction = build_transaction(tx=tx, network=self.network)
        return self

    # Getting transaction raw
    def raw(self):
        if self.transaction is None and "raw_transaction" not in self.transaction:
            raise ValueError("Transaction is none, Please build transaction first.")
        return self.transaction["raw_transaction"]

