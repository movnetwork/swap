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
    """
    Bitcoin Signature class.

    :param version: bitcoin transaction version, defaults to 2.
    :type version: int
    :param network: bitcoin network, defaults to testnet.
    :type network: str
    :returns:  Transaction -- bitcoin transaction instance.

    .. note::
        Bitcoin has only two networks, ``mainnet`` and ``testnet``.
    """

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
        """
        Get bitcoin signature transaction hash.

        :returns: str -- bitcoin signature transaction hash or transaction id.

        >>> signature.hash()
        "9cc0524fb8e7b2c5fecaee4eb91d43a3dc5cc18e9906abcb35a5732ff52efcc7"
        """

        if self.transaction is None:
            raise ValueError("transaction script is none, sign first")
        return self.transaction.txid

    # Transaction json format
    def json(self):
        """
        Get bitcoin signature transaction json format.

        :returns: str -- bitcoin signature transaction json format.

        >>> signature.json()
        {"hex": "02000000012c392217483906f902e73c4bc132864de58153772d79268960998162266634be0100000000ffffffff02e80300000000000017a914971894c58d85981c16c2059d422bcde0b156d04487a6290000000000001976a9146bce65e58a50b97989930e9a4ff1ac1a77515ef188ac00000000", "txid": "9cc0524fb8e7b2c5fecaee4eb91d43a3dc5cc18e9906abcb35a5732ff52efcc7", "hash": "9cc0524fb8e7b2c5fecaee4eb91d43a3dc5cc18e9906abcb35a5732ff52efcc7", "size": 117, "vsize": 117, "version": 2, "locktime": 0, "vin": [{"txid": "be346626628199608926792d775381e54d8632c14b3ce702f90639481722392c", "vout": 1, "scriptSig": {"asm": "", "hex": ""}, "sequence": "4294967295"}], "vout": [{"value": "0.00001000", "n": 0, "scriptPubKey": {"asm": "OP_HASH160 971894c58d85981c16c2059d422bcde0b156d044 OP_EQUAL", "hex": "a914971894c58d85981c16c2059d422bcde0b156d04487", "type": "p2sh", "address": "2N729UBGZB3xjsGFRgKivy4bSjkaJGMVSpB"}}, {"value": "0.00010662", "n": 1, "scriptPubKey": {"asm": "OP_DUP OP_HASH160 6bce65e58a50b97989930e9a4ff1ac1a77515ef1 OP_EQUALVERIFY OP_CHECKSIG", "hex": "76a9146bce65e58a50b97989930e9a4ff1ac1a77515ef188ac", "type": "p2pkh", "address": "mqLyrNDjpENRMZAoDpspH7kR9RtgvhWzYE"}}]}
        """

        if self.transaction is None:
            raise ValueError("transaction script is none, sign first")
        return self.transaction.to_json()

    # Transaction raw
    def raw(self):
        """
        Get bitcoin signature transaction raw.

        :returns: str -- bitcoin signature transaction raw.

        >>> signature.raw()
        "02000000012c392217483906f902e73c4bc132864de58153772d79268960998162266634be0100000000ffffffff02e80300000000000017a914971894c58d85981c16c2059d422bcde0b156d04487a6290000000000001976a9146bce65e58a50b97989930e9a4ff1ac1a77515ef188ac00000000"
        """

        if self.transaction is None:
            raise ValueError("transaction script is none, build transaction first")
        return self.transaction.hexlify()

    def type(self):
        """
        Get bitcoin signature transaction type.

        :returns: str -- bitcoin signature transaction type.

        >>> signature.type()
        "bitcoin_fund_signed"
        """

        if self.type is None:
            raise ValueError("not found type, sign first")
        return self.type

    def sign(self, unsigned_raw, solver):
        """
        Sign unsigned transaction raw.

        :param unsigned_raw: bitcoin unsigned transaction raw.
        :type unsigned_raw: str
        :param solver: bitcoin solver
        :type solver: bitcoin.solver.FundSolver, bitcoin.solver.ClaimSolver, bitcoin.solver.RefundSolver
        :returns:  FundSignature, ClaimSignature, RefundSignature -- bitcoin signature instance.

        >>> from shuttle.providers.bitcoin.signature import Signature
        >>> signature = Signature()
        >>> signature.sign(bitcoin_claim_unsigned, claim_solver)
        <shuttle.providers.bitcoin.signature.ClaimSignature object at 0x0409DAF0>
        """

        tx_raw = json.loads(b64decode(str(unsigned_raw).encode()).decode())
        if "type" not in tx_raw:
            raise ValueError("invalid unsigned transaction raw")
        self.type = tx_raw["type"]
        if tx_raw["type"] == "bitcoin_fund_unsigned":
            return FundSignature(network=self.network, version=self.version)\
                .sign(unsigned_raw=unsigned_raw, solver=solver)
        elif tx_raw["type"] == "bitcoin_claim_unsigned":
            return ClaimSignature(network=self.network, version=self.version)\
                .sign(unsigned_raw=unsigned_raw, solver=solver)
        elif tx_raw["type"] == "bitcoin_refund_unsigned":
            return RefundSignature(network=self.network, version=self.version)\
                .sign(unsigned_raw=unsigned_raw, solver=solver)

    def signed_raw(self):
        """
        Get bitcoin signed transaction raw.

        :returns: str -- bitcoin signed transaction raw.

        >>> from shuttle.providers.bitcoin.signature import Signature
        >>> signature = Signature()
        >>> signature.sign(bitcoin_refund_unsigned, refund_solver)
        >>> signature.signed_raw()
        "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTJjMzkyMjE3NDgzOTA2ZjkwMmU3M2M0YmMxMzI4NjRkZTU4MTUzNzcyZDc5MjY4OTYwOTk4MTYyMjY2NjM0YmUwMTAwMDAwMDAwZmZmZmZmZmYwMmU4MDMwMDAwMDAwMDAwMDAxN2E5MTQ5NzE4OTRjNThkODU5ODFjMTZjMjA1OWQ0MjJiY2RlMGIxNTZkMDQ0ODdhNjI5MDAwMDAwMDAwMDAwMTk3NmE5MTQ2YmNlNjVlNThhNTBiOTc5ODk5MzBlOWE0ZmYxYWMxYTc3NTE1ZWYxODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiAxMjM0MCwgIm4iOiAxLCAic2NyaXB0IjogIjc2YTkxNDZiY2U2NWU1OGE1MGI5Nzk4OTkzMGU5YTRmZjFhYzFhNzc1MTVlZjE4OGFjIn1dLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfdW5zaWduZWQifQ"
        """

        if self.signed is None:
            raise ValueError("there is no signed data, sign first")
        return self.signed


# Fund signature
class FundSignature(Signature):
    """
    Bitcoin FundSignature class.

    :param version: bitcoin fund signature transaction version, defaults to 2.
    :type version: int
    :param network: bitcoin network, defaults to testnet.
    :type network: str
    :returns:  FundSignature -- bitcoin fund signature instance.

    :fee: Get bitcoin fund signature transaction fee.

    >>> fund_signature.fee
    675
    """

    def __init__(self, network="testnet", version=2):
        super().__init__(network=network, version=version)

    def sign(self, unsigned_raw, solver):
        """
        Sign unsigned fund transaction raw.

        :param unsigned_raw: bitcoin unsigned fund transaction raw.
        :type unsigned_raw: str
        :param solver: bitcoin fund solver.
        :type solver: bitcoin.solver.FundSolver
        :returns:  FundSignature -- bitcoin fund signature instance.

        >>> from shuttle.providers.bitcoin.signature import FundSignature
        >>> fund_signature = FundSignature()
        >>> fund_signature.sign(bitcoin_fund_unsigned, fund_solver)
        <shuttle.providers.bitcoin.signature.FundSignature object at 0x0409DAF0>
        """
        
        tx_raw = json.loads(b64decode(str(unsigned_raw).encode()).decode())
        if "raw" not in tx_raw or "outputs" not in tx_raw or "type" not in tx_raw or "fee" not in tx_raw:
            raise ValueError("invalid unsigned fund transaction raw")
        self.fee = tx_raw["fee"]
        self.type = tx_raw["type"]
        if not self.type == "bitcoin_fund_unsigned":
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
            raw=self.transaction.hexlify(),
            fee=tx_raw["fee"],
            network=tx_raw["network"],
            type="bitcoin_fund_signed"
        ))).encode()).decode()
        return self


# Claim signature
class ClaimSignature(Signature):
    """
    Bitcoin ClaimSignature class.

    :param version: bitcoin claim signature transaction version, defaults to 2.
    :type version: int
    :param network: bitcoin network, defaults to testnet.
    :type network: str
    :returns:  ClaimSignature -- bitcoin claim signature instance.

    :fee: Get bitcoin claim signature transaction fee.

    >>> claim_signature.fee
    675
    """

    def __init__(self, network="testnet", version=2):
        super().__init__(network=network, version=version)

    def sign(self, unsigned_raw, solver):
        """
        Sign unsigned claim transaction raw.

        :param unsigned_raw: bitcoin unsigned claim transaction raw.
        :type unsigned_raw: str
        :param solver: bitcoin claim solver.
        :type solver: bitcoin.solver.ClaimSolver
        :returns:  ClaimSignature -- bitcoin claim signature instance.

        >>> from shuttle.providers.bitcoin.signature import ClaimSignature
        >>> claim_signature = ClaimSignature()
        >>> claim_signature.sign(bitcoin_claim_unsigned, claim_solver)
        <shuttle.providers.bitcoin.signature.ClaimSignature object at 0x0409DAF0>
        """

        tx_raw = json.loads(b64decode(str(unsigned_raw).encode()).decode())
        if "raw" not in tx_raw or "outputs" not in tx_raw or "type" not in tx_raw or \
                "recipient_address" not in tx_raw or "sender_address" not in tx_raw or "fee" not in tx_raw:
            raise ValueError("invalid unsigned claim transaction raw")
        self.fee = tx_raw["fee"]
        self.type = tx_raw["type"]
        if not self.type == "bitcoin_claim_unsigned":
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
            raw=self.transaction.hexlify(),
            fee=tx_raw["fee"],
            network=tx_raw["network"],
            type="bitcoin_claim_signed"
        ))).encode()).decode()
        return self


# Refund signature
class RefundSignature(Signature):
    """
    Bitcoin RefundSignature class.

    :param version: bitcoin refund signature transaction version, defaults to 2.
    :type version: int
    :param network: bitcoin network, defaults to testnet.
    :type network: str
    :returns:  RefundSignature -- bitcoin claim signature instance.

    :fee: Get bitcoin refund signature transaction fee.

    >>> refund_signature.fee
    675
    """

    def __init__(self, network="testnet", version=2):
        super().__init__(network=network, version=version)

    def sign(self, unsigned_raw, solver):
        """
        Sign unsigned refund transaction raw.

        :param unsigned_raw: bitcoin unsigned refund transaction raw.
        :type unsigned_raw: str
        :param solver: bitcoin refund solver.
        :type solver: bitcoin.solver.RefundSolver
        :returns:  RefundSignature -- bitcoin refund signature instance.

        >>> from shuttle.providers.bitcoin.signature import RefundSignature
        >>> refund_signature = RefundSignature()
        >>> refund_signature.sign(bitcoin_refund_unsigned, refund_solver)
        <shuttle.providers.bitcoin.signature.RefundSignature object at 0x0409DAF0>
        """

        tx_raw = json.loads(b64decode(str(unsigned_raw).encode()).decode())
        if "raw" not in tx_raw or "outputs" not in tx_raw or "type" not in tx_raw or \
                "recipient_address" not in tx_raw or "sender_address" not in tx_raw or "fee" not in tx_raw:
            raise ValueError("invalid unsigned refund transaction raw")
        self.fee = tx_raw["fee"]
        self.type = tx_raw["type"]
        if not self.type == "bitcoin_refund_unsigned":
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
            raw=self.transaction.hexlify(),
            fee=tx_raw["fee"],
            network=tx_raw["network"],
            type="bitcoin_refund_signed"
        ))).encode()).decode()
        return self
