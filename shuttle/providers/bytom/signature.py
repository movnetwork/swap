#!/usr/bin/env python3

from base64 import b64encode, b64decode

import json

from .solver import ClaimSolver, FundSolver, RefundSolver
from .transaction import Transaction


# Signature
class Signature(Transaction):

    def __init__(self, network="testnet"):
        super().__init__(network)
        # Signed and type
        self.signed, self.type = None, None

    def type(self):
        if self.type is None:
            raise ValueError("not found type, sign first")
        return self.type

    def sign(self, unsigned_raw, solver):
        tx_raw = json.loads(b64decode(str(unsigned_raw).encode()).decode())
        if "type" not in tx_raw:
            raise ValueError("invalid unsigned transaction raw")
        self.type = tx_raw["type"]
        if tx_raw["type"] == "bytom_fund_unsigned":
            return FundSignature(network=self.network)\
                .sign(unsigned_raw=unsigned_raw, solver=solver)
        elif tx_raw["type"] == "bytom_claim_unsigned":
            return ClaimSignature(network=self.network)\
                .sign(unsigned_raw=unsigned_raw, solver=solver)
        elif tx_raw["type"] == "bytom_refund_unsigned":
            return RefundSignature(network=self.network)\
                .sign(unsigned_raw=unsigned_raw, solver=solver)

    def signed_raw(self):
        if self.signed is None:
            raise ValueError("there is no signed data, sign first")
        return self.signed


# Fund signature
class FundSignature(Signature):

    def __init__(self, network="testnet"):
        super().__init__(network=network)

    def sign(self, unsigned_raw, solver: FundSolver):
        tx_raw = json.loads(b64decode(str(unsigned_raw).encode()).decode())
        if "tx" not in tx_raw or "type" not in tx_raw or "fee" not in tx_raw:
            raise ValueError("invalid unsigned bytom fund transaction raw")
        self.fee, self.type, self.transaction = tx_raw["fee"], tx_raw["type"], tx_raw["tx"]
        if not self.type == "bytom_fund_unsigned":
            raise TypeError("can't sign this %s transaction using bytom FundSignature" % tx_raw["type"])
        wallet = solver.solve()
        for unsigned in self.unsigned():
            signed_data = list()
            unsigned_datas = unsigned["datas"]
            for unsigned_data in unsigned_datas:
                signed_data.append(wallet.sign(unsigned_data))
            self.signatures.append(signed_data)
        self.signed = b64encode(str(json.dumps(dict(
            raw=self.raw(),
            signatures=self.signatures,
            type="bytom_fund_signed"
        ))).encode()).decode()
        return self


# Claim signature
class ClaimSignature(Signature):

    def __init__(self, network="testnet"):
        super().__init__(network=network)

    def sign(self, unsigned_raw, solver: ClaimSolver):
        tx_raw = json.loads(b64decode(str(unsigned_raw).encode()).decode())
        if "tx" not in tx_raw or "type" not in tx_raw or "fee" not in tx_raw:
            raise ValueError("invalid unsigned bytom fund transaction raw")
        self.fee, self.type, self.transaction = tx_raw["fee"], tx_raw["type"], tx_raw["tx"]
        if not self.type == "bytom_claim_unsigned":
            raise TypeError("can't sign this %s transaction using bytom FundSignature" % tx_raw["type"])
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
        self.signed = b64encode(str(json.dumps(dict(
            raw=self.raw(),
            signatures=self.signatures,
            type="bytom_claim_signed"
        ))).encode()).decode()
        return self


# Refund signature
class RefundSignature(Signature):

    def __init__(self, network="testnet"):
        super().__init__(network=network)

    def sign(self, unsigned_raw, solver: RefundSolver):
        tx_raw = json.loads(b64decode(str(unsigned_raw).encode()).decode())
        if "tx" not in tx_raw or "type" not in tx_raw or "fee" not in tx_raw:
            raise ValueError("invalid unsigned bytom fund transaction raw")
        self.fee, self.type, self.transaction = tx_raw["fee"], tx_raw["type"], tx_raw["tx"]
        if not self.type == "bytom_refund_unsigned":
            raise TypeError("can't sign this %s transaction using bytom FundSignature" % tx_raw["type"])
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
        self.signed = b64encode(str(json.dumps(dict(
            raw=self.raw(),
            signatures=self.signatures,
            type="bytom_refund_signed"
        ))).encode()).decode()
        return self
