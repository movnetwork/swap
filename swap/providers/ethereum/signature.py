#!/usr/bin/env python3

from base64 import b64encode, b64decode
from binascii import hexlify, unhexlify

import json

from .rpc import get_web3
from .solver import FundSolver


# Signature
class Signature:
    """
    Ethereum Signature class.

    :param network: ethereum network, defaults to ropsten.
    :type network: str
    :returns:  Transaction -- ethereum transaction instance.

    .. note::
        Ethereum has only two networks, ``mainnet`` and ``ropsten``.
    """

    def __init__(self, network="ropsten"):
        # Ethereum network
        self.network = network
        # Transaction
        self.transaction = None
        # Ethereum fee
        self.fee = int()
        # Signed and type
        self.signature, self.type = None, None

        self.web3, self.signed = None, None

    # Transaction hash
    def hash(self):
        """
        Get ethereum transaction hash.

        :returns: str -- ethereum transaction hash or transaction id.

        >>> transaction.hash()
        "2993414225f65390220730d0c1a356c14e91bca76db112d37366df93e364a492"
        """

        return self.signature["hash"]\
            if "hash" in self.signature else None

    # Transaction json
    def json(self):
        """
        Get ethereum transaction json format.

        :returns: dict -- ethereum transaction json format.

        >>> transaction.json()
        {'gas': 134320, 'gasPrice': 20000000000, 'chainId': 1337, 'from': '0x053929E43A1eF27E3822E7fb193527edE04C415B', 'nonce': 15, 'value': 100, 'to': '0x9f77B9f27e8Bc8ad0b58FBf99aeA28feEC7eC50b', 'data': '0x335ef5bd00000000000000000000000031aa61a5d8756c84ebdf0f34e01cab90514f2a573a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb000000000000000000000000000000000000000000000000000000005ea55961'}
        """
        if self.transaction is None:
            raise ValueError("transaction is none, build transaction first.")
        return self.transaction

    # Transaction raw
    def raw(self):
        """
        Get ethereum transaction raw.

        :returns: str -- ethereum transaction raw.

        >>> transaction.raw()
        "f8cc0f8504a817c80083020cb0949f77b9f27e8bc8ad0b58fbf99aea28feec7ec50b64b864335ef5bd00000000000000000000000031aa61a5d8756c84ebdf0f34e01cab90514f2a573a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb000000000000000000000000000000000000000000000000000000005ea55961820a95a08bae7e0a7481d11518f7771fedc6f25ab5cc85bc24a0767573ce60e52a090c8da04d6efaafedc5096ecc998cdbca5b3ea4fc6b009b44a8041b8c71be5520c3a356"
        """

        return self.signature["rawTransaction"]\
            if "rawTransaction" in self.signature else None

    def sign(self, unsigned_raw, solver):
        """
        Sign unsigned transaction raw.

        :param unsigned_raw: ethereum unsigned transaction raw.
        :type unsigned_raw: str
        :param solver: ethereum solver
        :type solver: ethereum.solver.FundSolver, ethereum.solver.ClaimSolver, ethereum.solver.RefundSolver
        :returns:  FundSignature, ClaimSignature, RefundSignature -- ethereum signature instance.

        >>> from shuttle.providers.ethereum.signature import Signature
        >>> signature = Signature()
        >>> signature.sign(ethereum_claim_unsigned, claim_solver)
        <shuttle.providers.ethereum.signature.ClaimSignature object at 0x0409DAF0>
        """

        tx_raw = json.loads(b64decode(str(unsigned_raw).encode()).decode())
        if "type" not in tx_raw:
            raise ValueError("invalid unsigned transaction raw")
        if tx_raw["type"] == "ethereum_fund_unsigned":
            return FundSignature(network=self.network)\
                .sign(unsigned_raw=unsigned_raw, solver=solver)
        # elif tx_raw["type"] == "ethereum_claim_unsigned":
        #     return ClaimSignature(network=self.network, version=self.version)\
        #         .sign(unsigned_raw=unsigned_raw, solver=solver)
        # elif tx_raw["type"] == "ethereum_refund_unsigned":
        #     return RefundSignature(network=self.network, version=self.version)\
        #         .sign(unsigned_raw=unsigned_raw, solver=solver)

    def signed_raw(self):
        """
        Get ethereum signed transaction raw.

        :returns: str -- ethereum signed transaction raw.

        >>> from shuttle.providers.ethereum.signature import Signature
        >>> signature = Signature()
        >>> signature.sign(ethereum_refund_unsigned, refund_solver)
        >>> signature.signed_raw()
        "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTJjMzkyMjE3NDgzOTA2ZjkwMmU3M2M0YmMxMzI4NjRkZTU4MTUzNzcyZDc5MjY4OTYwOTk4MTYyMjY2NjM0YmUwMTAwMDAwMDAwZmZmZmZmZmYwMmU4MDMwMDAwMDAwMDAwMDAxN2E5MTQ5NzE4OTRjNThkODU5ODFjMTZjMjA1OWQ0MjJiY2RlMGIxNTZkMDQ0ODdhNjI5MDAwMDAwMDAwMDAwMTk3NmE5MTQ2YmNlNjVlNThhNTBiOTc5ODk5MzBlOWE0ZmYxYWMxYTc3NTE1ZWYxODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiAxMjM0MCwgIm4iOiAxLCAic2NyaXB0IjogIjc2YTkxNDZiY2U2NWU1OGE1MGI5Nzk4OTkzMGU5YTRmZjFhYzFhNzc1MTVlZjE4OGFjIn1dLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfdW5zaWduZWQifQ"
        """

        if self.signed is None:
            raise ValueError("there is no signed data, sign first")
        return self.signed


# Fund signature
class FundSignature(Signature):
    """
    Ethereum FundSignature class.

    :param network: ethereum network, defaults to ropsten.
    :type network: str
    :returns:  FundSignature -- ethereum fund signature instance.

    :fee: Get ethereum fund signature transaction fee.

    >>> fund_signature.fee
    300000000
    """

    def __init__(self, network="ropsten"):
        super().__init__(network=network)

    def sign(self, unsigned_raw, solver):
        """
        Sign unsigned fund transaction raw.

        :param unsigned_raw: ethereum unsigned fund transaction raw.
        :type unsigned_raw: str
        :param solver: ethereum fund solver.
        :type solver: ethereum.solver.FundSolver
        :returns:  FundSignature -- ethereum fund signature instance.

        >>> from shuttle.providers.ethereum.signature import FundSignature
        >>> fund_signature = FundSignature()
        >>> fund_signature.sign(ethereum_fund_unsigned, fund_solver)
        <shuttle.providers.ethereum.signature.FundSignature object at 0x0409DAF0>
        """

        tx_raw = json.loads(b64decode(str(unsigned_raw).encode()).decode())
        if "tx" not in tx_raw or "network" not in tx_raw or "type" not in tx_raw or "fee" not in tx_raw:
            raise ValueError("invalid unsigned fund transaction raw")
        self.fee = tx_raw["fee"]
        self.type = tx_raw["type"]
        if not self.type == "ethereum_fund_unsigned":
            raise TypeError("can't sign this %s transaction using FundSignature" % tx_raw["type"])
        if not isinstance(solver, FundSolver):
            raise TypeError("invalid solver instance, only takes ethereum FundSolver class")
        # Initializing web3
        self.network = tx_raw["network"]
        _, _, self.web3 = get_web3(network=self.network)
        account = self.web3.eth.account.privateKeyToAccount(solver.solve().private_key())
        self.transaction = tx_raw["tx"]
        signature = account.signTransaction(self.transaction)
        self.signature = dict(
            rawTransaction=hexlify(signature.rawTransaction).decode(),
            hash=hexlify(signature.hash).decode(),
            r=str(signature.r), s=str(signature.s), v=str(signature.v)
        )
        self.signed = b64encode(str(json.dumps(dict(
            fee=self.fee,
            network=self.network,
            signature=self.signature,
            type="ethereum_fund_signed"
        ))).encode()).decode()
        return self
