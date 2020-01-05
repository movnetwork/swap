#!/usr/bin/env python3


from .rpc import build_transaction
from .utils import spend_wallet_action, control_program_action
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


class FundTransaction(Transaction):

    # Initialization fund transaction
    def __init__(self, network="testnet"):
        super().__init__(network)

    def build_transaction(self, guid, locked_asset,
                          contract_program, locked_amount):
        # Actions
        inputs, outputs = list(), list()

        # Input action
        inputs.append(list(spend_wallet_action(
            asset_id=locked_asset,
            amount=locked_amount
        )))
        # Output action
        outputs.append(list(control_program_action(
            asset_id=locked_asset,
            amount=locked_amount,
            control_program=contract_program
        )))

        # Transaction
        tx = dict(
            guid=guid,
            inputs=inputs,
            outputs=outputs,
            fee=bytom["fee"],
            confirmations=bytom["confirmations"]
        )
        # Building transaction
        self.transaction = build_transaction(tx=tx, network=self.network)
        return self
