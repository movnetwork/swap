#!/usr/bin/env python3

from base64 import b64encode, b64decode
from btcpy.structs.script import Script, P2shScript
from btcpy.structs.transaction import MutableTransaction, TxOut
from btcpy.structs.sig import P2shSolver

import json

from .utils import double_sha256
from .solver import ClaimSolver, FundSolver, RefundSolver
from .htlc import HTLC


# Signature
class Signature:

    def __init__(self, network="testnet", version=2):
        # Transaction build version
        self.version = version
        # Bitcoin network
        self.network = network
        # Transaction
        self.transaction = None
        # Bitcoin fee
        self.fee = int()
        # Signed and type
        self.signed, self.type = None, None

    # Transaction hash
    def hash(self):
        if self.transaction is None:
            raise ValueError("transaction script is none, sign first")
        return self.transaction.txid

    # Transaction raw
    def raw(self):
        if self.transaction is None:
            raise ValueError("transaction script is none, build transaction first")
        return self.transaction.hexlify()

    # Transaction json format
    def json(self):
        if self.transaction is None:
            raise ValueError("transaction script is none, sign first")
        return self.transaction.to_json()

    def type(self):
        if self.type is None:
            raise ValueError("not found type, sign first")
        return self.type

    def sign(self, unsigned_raw, solver):
        tx_raw = json.loads(b64decode(str(unsigned_raw).encode()).decode())
        if "type" not in tx_raw:
            raise ValueError("invalid unsigned transaction raw")
        self.type = tx_raw["type"]
        if tx_raw["type"] == "fund_unsigned":
            return FundSignature(network=self.network, version=self.version)\
                .sign(unsigned_raw=unsigned_raw, solver=solver)
        elif tx_raw["type"] == "claim_unsigned":
            return ClaimSignature(network=self.network, version=self.version)\
                .sign(unsigned_raw=unsigned_raw, solver=solver)
        elif tx_raw["type"] == "refund_unsigned":
            return RefundSignature(network=self.network, version=self.version)\
                .sign(unsigned_raw=unsigned_raw, solver=solver)

    def signed_raw(self):
        if self.signed is None:
            raise ValueError("there is no signed data, sign first")
        return self.signed


# Fund signature
class FundSignature(Signature):

    def __init__(self, network="testnet", version=2):
        super().__init__(network=network, version=version)

    def sign(self, unsigned_raw, solver: FundSolver):
        tx_raw = json.loads(b64decode(str(unsigned_raw).encode()).decode())
        if "raw" not in tx_raw or "outputs" not in tx_raw or "type" not in tx_raw or "fee" not in tx_raw:
            raise ValueError("invalid unsigned fund transaction raw")
        self.fee = tx_raw["fee"]
        self.type = tx_raw["type"]
        if not self.type == "fund_unsigned":
            raise TypeError("can't sign this %s transaction using FundSignature" % tx_raw["type"])
        if not isinstance(solver, FundSolver):
            raise TypeError("invalid solver instance, only takes bitcoin FundSolver class")
        self.transaction = MutableTransaction.unhexlify(tx_raw["raw"])
        outputs = list()
        for output in tx_raw["outputs"]:
            outputs.append(
                TxOut(value=output["amount"], n=output["n"],
                      script_pubkey=Script.unhexlify(output["script"])))
        self.transaction.spend(outputs, [solver.solve() for _ in outputs])
        self.signed = b64encode(str(json.dumps(dict(
            raw=self.transaction.hexlify(), type="fund_signed"
        ))).encode()).decode()
        return self


# Claim signature
class ClaimSignature(Signature):

    def __init__(self, network="testnet", version=2):
        super().__init__(network=network, version=version)

    def sign(self, unsigned_raw, solver: ClaimSolver):
        tx_raw = json.loads(b64decode(str(unsigned_raw).encode()).decode())
        if "raw" not in tx_raw or "outputs" not in tx_raw or "type" not in tx_raw or \
                "recipient_address" not in tx_raw or "sender_address" not in tx_raw or "fee" not in tx_raw:
            raise ValueError("invalid unsigned claim transaction raw")
        self.fee = tx_raw["fee"]
        self.type = tx_raw["type"]
        if not self.type == "claim_unsigned":
            raise TypeError("can't sign this %s transaction using ClaimSignature" % tx_raw["type"])
        if not isinstance(solver, ClaimSolver):
            raise TypeError("invalid solver instance, only takes bitcoin ClaimSolver class")
        htlc = HTLC(network=self.network).init(
            secret_hash=double_sha256(solver.secret),
            recipient_address=tx_raw["recipient_address"],
            sender_address=tx_raw["sender_address"],
            sequence=solver.sequence
        )
        output = TxOut(value=tx_raw["outputs"][0]["amount"], n=tx_raw["outputs"][0]["n"],
                       script_pubkey=P2shScript.unhexlify(tx_raw["outputs"][0]["script"]))
        self.transaction = MutableTransaction.unhexlify(tx_raw["raw"])
        self.transaction.spend([output], [
            P2shSolver(htlc.script, solver.solve())
        ])
        self.signed = b64encode(str(json.dumps(dict(
            raw=self.transaction.hexlify(), type="claim_signed"
        ))).encode()).decode()
        return self


# Refund signature
class RefundSignature(Signature):

    def __init__(self, network="testnet", version=2):
        super().__init__(network=network, version=version)

    def sign(self, unsigned_raw, solver: RefundSolver):
        tx_raw = json.loads(b64decode(str(unsigned_raw).encode()).decode())
        if "raw" not in tx_raw or "outputs" not in tx_raw or "type" not in tx_raw or \
                "recipient_address" not in tx_raw or "sender_address" not in tx_raw or "fee" not in tx_raw:
            raise ValueError("invalid unsigned refund transaction raw")
        self.fee = tx_raw["fee"]
        self.type = tx_raw["type"]
        if not self.type == "refund_unsigned":
            raise TypeError("can't sign this %s transaction using RefundSignature" % tx_raw["type"])
        if not isinstance(solver, RefundSolver):
            raise Exception("invalid solver error, only refund solver")
        htlc = HTLC(network=self.network).init(
            secret_hash=double_sha256(solver.secret),
            recipient_address=tx_raw["recipient_address"],
            sender_address=tx_raw["sender_address"],
            sequence=solver.sequence
        )
        output = TxOut(value=tx_raw["outputs"][0]["amount"], n=tx_raw["outputs"][0]["n"],
                       script_pubkey=P2shScript.unhexlify(tx_raw["outputs"][0]["script"]))
        self.transaction = MutableTransaction.unhexlify(tx_raw["raw"])
        self.transaction.spend([output], [
            P2shSolver(htlc.script, solver.solve())
        ])
        self.signed = b64encode(str(json.dumps(dict(
            raw=self.transaction.hexlify(), type="refund_signed"
        ))).encode()).decode()
        return self
