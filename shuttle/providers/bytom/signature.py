#!/usr/bin/env python3

from base64 import b64encode, b64decode

import json

from .solver import ClaimSolver, FundSolver, RefundSolver
from .transaction import Transaction
from .rpc import decode_tx_raw


# Signature
class Signature(Transaction):
    """
    Bytom Signature class.

    :param network: bytom network, defaults to testnet.
    :type network: str
    :returns:  Transaction -- bytom transaction instance.

    .. note::
        Bytom has only three networks, ``mainnet``, ``solonet`` and ``testnet``.
    """

    def __init__(self, network="testnet"):
        super().__init__(network)
        # Signed and type
        self.signed, self.type = None, None

    # Transaction hash
    def hash(self):
        """
        Get bytom signature transaction hash.

        :returns: str -- bytom signature transaction hash or transaction id.

        >>> signature.hash()
        "2993414225f65390220730d0c1a356c14e91bca76db112d37366df93e364a492"
        """

        if self.transaction is None:
            raise ValueError("transaction is none, build transaction first.")
        return self.transaction["hash"]

    # Transaction json
    def json(self):
        """
        Get bytom signature transaction json format.

        :returns: dict -- bytom signature transaction json format.

        >>> signature.json()
        {"hash": "2993414225f65390220730d0c1a356c14e91bca76db112d37366df93e364a492", "status_fail": false, "size": 379, "submission_timestamp": 0, "memo": "", "inputs": [{"script": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 2450000000, "type": "spend"}], "outputs": [{"utxo_id": "5edccebe497893c289121f9e365fdeb34c97008b9eb5a9960fe9541e7923aabc", "script": "01642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0", "address": "smart contract", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 1000, "type": "control"}, {"utxo_id": "f8cfbb692db1963be88b09c314adcc9e19d91c6c019aa556fb7cb76ba8ffa1fa", "script": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 2439999000, "type": "control"}], "fee": 10000000, "balances": [{"asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": "-10001000"}], "types": ["ordinary"]}
        """
        if self.transaction is None:
            raise ValueError("transaction is none, build transaction first.")
        return decode_tx_raw(tx_raw=self.transaction["raw"])

    # Transaction raw
    def raw(self):
        """
        Get bytom signature transaction raw.

        :returns: str -- bytom signature transaction raw.

        >>> signature.raw()
        "070100010160015e7f2d7ecec3f61d30d0b2968973a3ac8448f0599ea20dce883b48c903c4d6e87fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8091a0900901011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a22012091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e20201ad01ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe80701880101642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c000013dffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff98dcbd8b09011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a00"
        """

        if self.transaction is None:
            raise ValueError("transaction is none, build transaction first.")
        return self.transaction["raw"]

    def type(self):
        """
        Get bytom signature transaction type.

        :returns: str -- bytom signature transaction type.

        >>> signature.type()
        "bytom_fund_signed"
        """

        if self.type is None:
            raise ValueError("not found type, sign first")
        return self.type

    def sign(self, unsigned_raw, solver):
        """
        Sign unsigned transaction raw.

        :param unsigned_raw: bytom unsigned transaction raw.
        :type unsigned_raw: str
        :param solver: bytom solver
        :type solver: bytom.solver.FundSolver, bytom.solver.ClaimSolver, bytom.solver.RefundSolver
        :returns:  FundSignature, ClaimSignature, RefundSignature -- bytom signature instance.

        >>> from shuttle.providers.bytom.signature import Signature
        >>> signature = Signature()
        >>> signature.sign(bytom_claim_unsigned, claim_solver)
        <shuttle.providers.bytom.signature.ClaimSignature object at 0x0409DAF0>
        """

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

    def unsigned(self, raw=False):
        if self.transaction is None:
            raise ValueError("transaction is none, build transaction first.")
        return self.transaction["unsigned"]

    def signed_raw(self):
        """
        Get bytom signed transaction raw.

        :returns: str -- bytom signed transaction raw.

        >>> from shuttle.providers.bytom.signature import Signature
        >>> signature = Signature()
        >>> signature.sign(bytom_refund_unsigned, refund_solver)
        >>> signature.signed_raw()
        "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTJjMzkyMjE3NDgzOTA2ZjkwMmU3M2M0YmMxMzI4NjRkZTU4MTUzNzcyZDc5MjY4OTYwOTk4MTYyMjY2NjM0YmUwMTAwMDAwMDAwZmZmZmZmZmYwMmU4MDMwMDAwMDAwMDAwMDAxN2E5MTQ5NzE4OTRjNThkODU5ODFjMTZjMjA1OWQ0MjJiY2RlMGIxNTZkMDQ0ODdhNjI5MDAwMDAwMDAwMDAwMTk3NmE5MTQ2YmNlNjVlNThhNTBiOTc5ODk5MzBlOWE0ZmYxYWMxYTc3NTE1ZWYxODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiAxMjM0MCwgIm4iOiAxLCAic2NyaXB0IjogIjc2YTkxNDZiY2U2NWU1OGE1MGI5Nzk4OTkzMGU5YTRmZjFhYzFhNzc1MTVlZjE4OGFjIn1dLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfdW5zaWduZWQifQ"
        """

        if self.signed is None:
            raise ValueError("there is no signed data, sign first")
        return self.signed


# Fund signature
class FundSignature(Signature):
    """
    Bytom FundSignature class.

    :param network: bytom network, defaults to testnet.
    :type network: str
    :returns:  FundSignature -- bytom fund signature instance.

    :fee: Get bytom fund signature transaction fee.

    >>> fund_signature.fee
    10000000
    """

    def __init__(self, network="testnet"):
        super().__init__(network=network)

    def sign(self, unsigned_raw, solver):
        """
        Sign unsigned fund transaction raw.

        :param unsigned_raw: bytom unsigned fund transaction raw.
        :type unsigned_raw: str
        :param solver: bytom fund solver.
        :type solver: bytom.solver.FundSolver
        :returns:  FundSignature -- bytom fund signature instance.

        >>> from shuttle.providers.bytom.signature import FundSignature
        >>> fund_signature = FundSignature()
        >>> fund_signature.sign(bytom_fund_unsigned, fund_solver)
        <shuttle.providers.bytom.signature.FundSignature object at 0x0409DAF0>
        """
        
        tx_raw = json.loads(b64decode(str(unsigned_raw).encode()).decode())
        if "raw" not in tx_raw or "type" not in tx_raw or "fee" not in tx_raw:
            raise ValueError("invalid unsigned bytom fund transaction raw")
        self.fee, self.type, self.transaction = tx_raw["fee"], tx_raw["type"], tx_raw
        if not self.type == "bytom_fund_unsigned":
            raise TypeError("can't sign this %s transaction using bytom FundSignature" % tx_raw["type"])
        wallet = solver.solve()
        wallet._indexes = list()
        for unsigned in self.unsigned():
            signed_data = list()
            unsigned_datas = unsigned["datas"]
            if unsigned["path"]:
                wallet.from_path(unsigned["path"])
            elif solver.path:
                wallet.from_path(solver.path)
            elif solver.indexes:
                wallet.from_indexes(solver.indexes)
            for unsigned_data in unsigned_datas:
                signed_data.append(wallet.sign(unsigned_data))
            self.signatures.append(signed_data)
            wallet._indexes = list()
        self.signed = b64encode(str(json.dumps(dict(
            fee=self.fee,
            guid=self.transaction["guid"],
            raw=self.raw(),
            hash=self.hash(),
            unsigned=self.unsigned(),
            network=self.network,
            signatures=self.signatures,
            type="bytom_fund_signed"
        ))).encode()).decode()
        return self


# Claim signature
class ClaimSignature(Signature):
    """
    Bytom ClaimSignature class.

    :param network: bytom network, defaults to testnet.
    :type network: str
    :returns:  ClaimSignature -- bytom claim signature instance.

    :fee: Get bytom claim signature transaction fee.

    >>> claim_signature.fee
    10000000
    """

    def __init__(self, network="testnet"):
        super().__init__(network=network)

    def sign(self, unsigned_raw, solver):
        """
        Sign unsigned claim transaction raw.

        :param unsigned_raw: bytom unsigned claim transaction raw.
        :type unsigned_raw: str
        :param solver: bytom claim solver.
        :type solver: bytom.solver.ClaimSolver
        :returns:  ClaimSignature -- bytom claim signature instance.

        >>> from shuttle.providers.bytom.signature import ClaimSignature
        >>> claim_signature = ClaimSignature()
        >>> claim_signature.sign(bytom_claim_unsigned, claim_solver)
        <shuttle.providers.bytom.signature.ClaimSignature object at 0x0409DAF0>
        """
        
        tx_raw = json.loads(b64decode(str(unsigned_raw).encode()).decode())
        if "raw" not in tx_raw or "type" not in tx_raw or "fee" not in tx_raw:
            raise ValueError("invalid unsigned bytom fund transaction raw")
        self.fee, self.type, self.transaction = tx_raw["fee"], tx_raw["type"], tx_raw
        if not self.type == "bytom_claim_unsigned":
            raise TypeError("can't sign this %s transaction using bytom FundSignature" % tx_raw["type"])
        wallet = solver.solve()
        wallet._indexes = list()
        for index, unsigned in enumerate(self.unsigned()):
            signed_data = list()
            unsigned_datas = unsigned["datas"]
            if unsigned["path"]:
                wallet.from_path(unsigned["path"])
            elif solver.path:
                wallet.from_path(solver.path)
            elif solver.indexes:
                wallet.from_indexes(solver.indexes)
            for unsigned_data in unsigned_datas:
                if index == 0:
                    signed_data.append(bytearray(solver.secret).hex())
                    signed_data.append(wallet.sign(unsigned_data))
                    signed_data.append(str())
                else:
                    signed_data.append(wallet.sign(unsigned_data))
            self.signatures.append(signed_data)
            wallet._indexes = list()
        self.signed = b64encode(str(json.dumps(dict(
            fee=self.fee,
            guid=self.transaction["guid"],
            raw=self.raw(),
            hash=self.hash(),
            unsigned=self.unsigned(),
            network=self.network,
            signatures=self.signatures,
            type="bytom_claim_signed"
        ))).encode()).decode()
        return self


# Refund signature
class RefundSignature(Signature):
    """
    Bytom RefundSignature class.

    :param network: bytom network, defaults to testnet.
    :type network: str
    :returns:  RefundSignature -- bytom claim signature instance.

    :fee: Get bytom refund signature transaction fee.

    >>> refund_signature.fee
    10000000
    """

    def __init__(self, network="testnet"):
        super().__init__(network=network)

    def sign(self, unsigned_raw, solver):
        """
        Sign unsigned refund transaction raw.

        :param unsigned_raw: bytom unsigned refund transaction raw.
        :type unsigned_raw: str
        :param solver: bytom refund solver.
        :type solver: bytom.solver.RefundSolver
        :returns:  RefundSignature -- bytom refund signature instance.

        >>> from shuttle.providers.bytom.signature import RefundSignature
        >>> refund_signature = RefundSignature()
        >>> refund_signature.sign(bytom_refund_unsigned, refund_solver)
        <shuttle.providers.bytom.signature.RefundSignature object at 0x0409DAF0>
        """
        
        tx_raw = json.loads(b64decode(str(unsigned_raw).encode()).decode())
        if "raw" not in tx_raw or "type" not in tx_raw or "fee" not in tx_raw:
            raise ValueError("invalid unsigned bytom fund transaction raw")
        self.fee, self.type, self.transaction = tx_raw["fee"], tx_raw["type"], tx_raw
        if not self.type == "bytom_refund_unsigned":
            raise TypeError("can't sign this %s transaction using bytom FundSignature" % tx_raw["type"])
        wallet = solver.solve()
        wallet._indexes = list()
        for index, unsigned in enumerate(self.unsigned()):
            signed_data = list()
            unsigned_datas = unsigned["datas"]
            if unsigned["path"]:
                wallet.from_path(unsigned["path"])
            elif solver.path:
                wallet.from_path(solver.path)
            elif solver.indexes:
                wallet.from_indexes(solver.indexes)
            for unsigned_data in unsigned_datas:
                if index == 0:
                    signed_data.append(wallet.sign(unsigned_data))
                    signed_data.append(str("01"))
                else:
                    signed_data.append(wallet.sign(unsigned_data))
            self.signatures.append(signed_data)
            wallet._indexes = list()
        self.signed = b64encode(str(json.dumps(dict(
            fee=self.fee,
            guid=self.transaction["guid"],
            raw=self.raw(),
            hash=self.hash(),
            unsigned=self.unsigned(),
            network=self.network,
            signatures=self.signatures,
            type="bytom_refund_signed"
        ))).encode()).decode()
        return self
