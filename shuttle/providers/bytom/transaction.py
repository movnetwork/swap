#!/usr/bin/env python3

from btmhdw import BytomHDWallet, sign, verify

from .rpc import build_transaction, decode_raw_transaction
from .utils import spend_wallet_action, control_program_action, spend_utxo_action, control_address_action
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
        if self.transaction is None:
            raise ValueError("Transaction is none, Please build transaction first.")
        elif "msg" in self.transaction:
            raise ValueError(self.transaction["msg"])
        return self.transaction["raw_transaction"]

    # Getting transaction json
    def json(self):
        if self.transaction is None:
            raise ValueError("Transaction is none, Please build transaction first.")
        elif "msg" in self.transaction:
            raise ValueError(self.transaction["msg"])
        return decode_raw_transaction(self.transaction["raw_transaction"])

    def unsigned(self):
        unsigned_datas = list()
        if self.transaction is None:
            raise ValueError("Transaction is none, Please build transaction first.")
        elif "msg" in self.transaction:
            raise ValueError(self.transaction["msg"])
        bytom_hd_wallet = BytomHDWallet()
        for signing_instruction in self.transaction["signing_instructions"]:
            unsigned_data = dict(unsigned=signing_instruction["sign_data"])
            if "pubkey" in signing_instruction and signing_instruction["pubkey"]:
                program = bytom_hd_wallet.program(public=signing_instruction["pubkey"])
                address = bytom_hd_wallet.address(program=program, network=self.network)
                unsigned_data.setdefault("public_key", signing_instruction["pubkey"])
                unsigned_data.setdefault("program", program)
                unsigned_data.setdefault("address", address)
            else:
                unsigned_data.setdefault("public_key", None)
                unsigned_data.setdefault("program", None)
                unsigned_data.setdefault("address", None)
            if "derivation_path" in signing_instruction and signing_instruction["derivation_path"]:
                path = bytom_hd_wallet.get_path(indexes=signing_instruction["derivation_path"])
                unsigned_data.setdefault("indexes", signing_instruction["derivation_path"])
                unsigned_data.setdefault("path", path)
            else:
                unsigned_data.setdefault("indexes", None)
                unsigned_data.setdefault("path", None)
            # Append unsigned datas
            unsigned_datas.append(unsigned_data)
        # Returning
        return unsigned_datas

    # Signing message
    def sign(self, xprivate_key, message):
        return sign(xprivate=xprivate_key, message=message)

    # Verifying signed message.
    def verify(self, xpublic_key, message, signature):
        return verify(xpublic=xpublic_key, message=message, signature=signature)


class FundTransaction(Transaction):

    # Initialization fund transaction
    def __init__(self, network="testnet"):
        super().__init__(network)

    def build_transaction(self, guid, locked_asset,
                          contract_program, locked_amount):
        # Actions
        inputs, outputs = list(), list()

        # Input action
        inputs.append(
            spend_wallet_action(
                asset=locked_asset,
                amount=locked_amount
            )
        )
        # Output action
        outputs.append(
            control_program_action(
                asset=locked_asset,
                amount=locked_amount,
                control_program=contract_program
            )
        )

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

    def sign(self, wallet: BytomHDWallet, **kwargs):
        pass

    def verify(self, wallet: BytomHDWallet, **kwargs):
        pass


class ClaimTransaction(Transaction):

    # Initialization fund transaction
    def __init__(self, network="testnet"):
        super().__init__(network)

    def build_transaction(self, guid, utxo_id, contract_asset,
                          contract_amount, receiver_address):
        # Actions
        inputs, outputs = list(), list()

        # Input action
        inputs.append(
            spend_utxo_action(
                utxo=utxo_id
            )
        )
        # Output action
        outputs.append(
            control_address_action(
                asset=contract_asset,
                amount=contract_amount,
                address=receiver_address
            )
        )

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


class RefundTransaction(Transaction):

    # Initialization fund transaction
    def __init__(self, network="testnet"):
        super().__init__(network)

    def build_transaction(self, guid, utxo_id, contract_asset,
                          contract_amount, sender_address):
        # Actions
        inputs, outputs = list(), list()

        # Input action
        inputs.append(
            spend_utxo_action(
                utxo=utxo_id
            )
        )
        # Output action
        outputs.append(
            control_address_action(
                asset=contract_asset,
                amount=contract_amount,
                address=sender_address
            )
        )

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
