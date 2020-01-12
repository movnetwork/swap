#!/usr/bin/env python3

from btmhdw import BytomHDWallet, sign

from .rpc import build_transaction
from .utils import spend_wallet_action, control_program_action, spend_utxo_action, control_address_action
from .solver import FundSolver, ClaimSolver, RefundSolver
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
        # Blockcenter GUID
        self.guid = guid
        # Signed datas
        self.signatures = list()

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

    # Transaction hash
    def hash(self):
        if self.transaction is None:
            raise ValueError("Transaction is none, Please build transaction first.")
        return self.transaction["tx"]["hash"]

    # Transaction raw
    def raw(self):
        if self.transaction is None:
            raise ValueError("Transaction is none, Please build transaction first.")
        return self.transaction["raw_transaction"]

    # Transaction json
    def json(self):
        if self.transaction is None:
            raise ValueError("Transaction is none, Please build transaction first.")
        return self.transaction["tx"]

    def unsigned(self):
        unsigned_datas = list()
        if self.transaction is None:
            raise ValueError("Transaction is none, Please build transaction first.")
        bytom_hd_wallet = BytomHDWallet()
        for signing_instruction in self.transaction["signing_instructions"]:
            unsigned_data = dict(datas=signing_instruction["sign_data"])
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
    def sign(self, xprivate_key):
        for unsigned in self.unsigned():
            signed_data = list()
            unsigned_datas = unsigned["datas"]
            for unsigned_data in unsigned_datas:
                signed_data.append(
                    sign(xprivate=xprivate_key,
                         message=unsigned_data))
            self.signatures.append(signed_data)
        return self


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

    # Signing transaction using xprivate keys
    def sign(self, solver: FundSolver, **kwargs):
        if not isinstance(solver, FundSolver):
            raise TypeError("Solver must be FundSolver format.")
        wallet = solver.solve()
        for unsigned in self.unsigned():
            signed_data = list()
            unsigned_datas = unsigned["datas"]
            for unsigned_data in unsigned_datas:
                signed_data.append(wallet.sign(unsigned_data))
            self.signatures.append(signed_data)
        return self


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

    # Signing transaction using private keys
    def sign(self, solver: ClaimSolver, **kwargs):
        if not isinstance(solver, ClaimSolver):
            raise TypeError("Solver must be ClaimSolver format.")
        wallet, secret = solver.solve()
        for index, unsigned in enumerate(self.unsigned()):
            signed_data = list()
            unsigned_datas = unsigned["datas"]
            for unsigned_data in unsigned_datas:
                if index == 0:
                    signed_data.append(bytearray(secret).hex())
                    signed_data.append(wallet.sign(unsigned_data))
                    signed_data.append(str())
                else:
                    signed_data.append(wallet.sign(unsigned_data))
            self.signatures.append(signed_data)
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

    # Signing transaction using private keys
    def sign(self, solver: RefundSolver, **kwargs):
        if not isinstance(solver, RefundSolver):
            raise TypeError("Solver must be ClaimSolver format.")
        wallet = solver.solve()
        for index, unsigned in enumerate(self.unsigned()):
            signed_data = list()
            unsigned_datas = unsigned["datas"]
            for unsigned_data in unsigned_datas:
                if index == 0:
                    signed_data.append(wallet.sign(unsigned_data))
                    signed_data.append(str("01"))
                else:
                    signed_data.append(wallet.sign(unsigned_data))
            self.signatures.append(signed_data)
        return self
