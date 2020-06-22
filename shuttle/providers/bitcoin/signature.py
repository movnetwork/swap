#!/usr/bin/env python3

from base64 import b64encode, b64decode
from btcpy.structs.script import Script, P2shScript
from btcpy.structs.transaction import MutableTransaction, TxOut
from btcpy.structs.sig import P2shSolver
from btcpy.setup import setup

import json

from .solver import FundSolver, ClaimSolver, RefundSolver


# Signature
class Signature:
    """
    Bitcoin Signature class.

    :param version: Bitcoin transaction version, defaults to 2.
    :type version: int
    :param network: Bitcoin network, defaults to testnet.
    :type network: str
    :returns:  Transaction -- Bitcoin transaction instance.

    .. note::
        Bitcoin has only two networks, ``mainnet`` and ``testnet``.
    """

    def __init__(self, network="testnet", version=2):
        # Bitcoin transaction
        self.transaction = None
        # Signed raw, type and fee
        self._signed_raw, self._type, self._fee = None, None, 0

        # Bitcoin setup network
        if network not in ["mainnet", "testnet"]:
            raise ValueError("invalid network, please choose only mainnet or testnet networks")
        self.network, self.version = network, version
        setup(self.network, strict=True)

    # Transaction fee
    def fee(self):
        """
        Get Bitcoin transaction fee.

        :returns: int -- Bitcoin transaction fee.

        >>> from shuttle.providers.bitcoin.signature import Signature
        >>> from shuttle.providers.bitcoin.solver import FundSolver
        >>> bitcoin_fund_unsigned_raw = "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTg4OGJlN2VjMDY1MDk3ZDk1NjY0NzYzZjI3NmQ0MjU1NTJkNzM1ZmIxZDk3NGFlNzhiZjcyMTA2ZGNhMGYzOTEwMTAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQyYmIwMTNjM2U0YmViMDg0MjFkZWRjZjgxNWNiNjVhNWMzODgxNzhiODdiY2RkMGUwMDAwMDAwMDAwMTk3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiA5ODQ5NDYsICJuIjogMSwgInNjcmlwdCI6ICI3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"
        >>> fund_solver = FundSolver(private_key="92cbbc5990cb5090326a76feeb321cad01048635afe5756523bbf9f7a75bf38b")
        >>> signature = Signature(network="testnet")
        >>> signature.sign(bitcoin_fund_unsigned_raw, fund_solver)
        >>> signature.fee()
        678
        """

        return self._fee

    # Transaction hash
    def hash(self):
        """
        Get Bitcoin signature transaction hash.

        :returns: str -- Bitcoin signature transaction hash or transaction id.

        >>> from shuttle.providers.bitcoin.signature import Signature
        >>> from shuttle.providers.bitcoin.solver import FundSolver
        >>> bitcoin_fund_unsigned_raw = "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTg4OGJlN2VjMDY1MDk3ZDk1NjY0NzYzZjI3NmQ0MjU1NTJkNzM1ZmIxZDk3NGFlNzhiZjcyMTA2ZGNhMGYzOTEwMTAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQyYmIwMTNjM2U0YmViMDg0MjFkZWRjZjgxNWNiNjVhNWMzODgxNzhiODdiY2RkMGUwMDAwMDAwMDAwMTk3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiA5ODQ5NDYsICJuIjogMSwgInNjcmlwdCI6ICI3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"
        >>> fund_solver = FundSolver(private_key="92cbbc5990cb5090326a76feeb321cad01048635afe5756523bbf9f7a75bf38b")
        >>> signature = Signature(network="testnet")
        >>> signature.sign(bitcoin_fund_unsigned_raw, fund_solver)
        >>> signature.hash()
        "285ffc86ebece50f208bbfc1e72fb7c99991a3cf4d1b43cf93657838a4ae23ad"
        """

        if self.transaction is None:
            raise ValueError("transaction script is none, sign first")
        return self.transaction.txid

    # Transaction json format
    def json(self):
        """
        Get Bitcoin signature transaction json format.

        :returns: str -- Bitcoin signature transaction json format.

        >>> from shuttle.providers.bitcoin.signature import Signature
        >>> from shuttle.providers.bitcoin.solver import FundSolver
        >>> bitcoin_fund_unsigned_raw = "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTg4OGJlN2VjMDY1MDk3ZDk1NjY0NzYzZjI3NmQ0MjU1NTJkNzM1ZmIxZDk3NGFlNzhiZjcyMTA2ZGNhMGYzOTEwMTAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQyYmIwMTNjM2U0YmViMDg0MjFkZWRjZjgxNWNiNjVhNWMzODgxNzhiODdiY2RkMGUwMDAwMDAwMDAwMTk3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiA5ODQ5NDYsICJuIjogMSwgInNjcmlwdCI6ICI3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"
        >>> fund_solver = FundSolver(private_key="92cbbc5990cb5090326a76feeb321cad01048635afe5756523bbf9f7a75bf38b")
        >>> signature = Signature(network="testnet")
        >>> signature.sign(bitcoin_fund_unsigned_raw, fund_solver)
        >>> signature.json()
        {'hex': '0200000001888be7ec065097d95664763f276d425552d735fb1d974ae78bf72106dca0f391010000006b483045022100c90f072ca3cd1ac446bbc952f007ddd82b930e416cfb7e07b0b56ec5065970b102202dcd28c92d9dfe6a67251602e5075cf21c3ec0bbe43ed0742dbf9cdbfe2d0d80012103c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84ffffffff02102700000000000017a9142bb013c3e4beb08421dedcf815cb65a5c388178b87bcdd0e00000000001976a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac00000000', 'txid': '285ffc86ebece50f208bbfc1e72fb7c99991a3cf4d1b43cf93657838a4ae23ad', 'hash': '285ffc86ebece50f208bbfc1e72fb7c99991a3cf4d1b43cf93657838a4ae23ad', 'size': 224, 'vsize': 224, 'version': 2, 'locktime': 0, 'vin': [{'txid': '91f3a0dc0621f78be74a971dfb35d75255426d273f766456d9975006ece78b88', 'vout': 1, 'scriptSig': {'asm': '3045022100c90f072ca3cd1ac446bbc952f007ddd82b930e416cfb7e07b0b56ec5065970b102202dcd28c92d9dfe6a67251602e5075cf21c3ec0bbe43ed0742dbf9cdbfe2d0d8001 03c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84', 'hex': '483045022100c90f072ca3cd1ac446bbc952f007ddd82b930e416cfb7e07b0b56ec5065970b102202dcd28c92d9dfe6a67251602e5075cf21c3ec0bbe43ed0742dbf9cdbfe2d0d80012103c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84'}, 'sequence': '4294967295'}], 'vout': [{'value': '0.00010000', 'n': 0, 'scriptPubKey': {'asm': 'OP_HASH160 2bb013c3e4beb08421dedcf815cb65a5c388178b OP_EQUAL', 'hex': 'a9142bb013c3e4beb08421dedcf815cb65a5c388178b87', 'type': 'p2sh', 'address': '2MwEDybGC34949zgzWX4M9FHmE3crDSUydP'}}, {'value': '0.00974268', 'n': 1, 'scriptPubKey': {'asm': 'OP_DUP OP_HASH160 64a8390b0b1685fcbf2d4b457118dc8da92d5534 OP_EQUALVERIFY OP_CHECKSIG', 'hex': '76a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac', 'type': 'p2pkh', 'address': 'mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q'}}]}
        """

        if self.transaction is None:
            raise ValueError("transaction script is none, sign first")
        return self.transaction.to_json()

    # Transaction raw
    def raw(self):
        """
        Get Bitcoin signature transaction raw.

        :returns: str -- Bitcoin signature transaction raw.

        >>> from shuttle.providers.bitcoin.signature import Signature
        >>> from shuttle.providers.bitcoin.solver import FundSolver
        >>> bitcoin_fund_unsigned_raw = "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTg4OGJlN2VjMDY1MDk3ZDk1NjY0NzYzZjI3NmQ0MjU1NTJkNzM1ZmIxZDk3NGFlNzhiZjcyMTA2ZGNhMGYzOTEwMTAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQyYmIwMTNjM2U0YmViMDg0MjFkZWRjZjgxNWNiNjVhNWMzODgxNzhiODdiY2RkMGUwMDAwMDAwMDAwMTk3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiA5ODQ5NDYsICJuIjogMSwgInNjcmlwdCI6ICI3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"
        >>> fund_solver = FundSolver(private_key="92cbbc5990cb5090326a76feeb321cad01048635afe5756523bbf9f7a75bf38b")
        >>> signature = Signature(network="testnet")
        >>> signature.sign(bitcoin_fund_unsigned_raw, fund_solver)
        >>> signature.raw()
        "0200000001888be7ec065097d95664763f276d425552d735fb1d974ae78bf72106dca0f391010000006b483045022100c90f072ca3cd1ac446bbc952f007ddd82b930e416cfb7e07b0b56ec5065970b102202dcd28c92d9dfe6a67251602e5075cf21c3ec0bbe43ed0742dbf9cdbfe2d0d80012103c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84ffffffff02102700000000000017a9142bb013c3e4beb08421dedcf815cb65a5c388178b87bcdd0e00000000001976a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac00000000"
        """

        if self.transaction is None:
            raise ValueError("transaction script is none, build transaction first")
        return self.transaction.hexlify()

    def type(self):
        """
        Get Bitcoin signature transaction type.

        :returns: str -- Bitcoin signature transaction type.

        >>> from shuttle.providers.bitcoin.signature import Signature
        >>> from shuttle.providers.bitcoin.solver import FundSolver
        >>> bitcoin_fund_unsigned_raw = "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTg4OGJlN2VjMDY1MDk3ZDk1NjY0NzYzZjI3NmQ0MjU1NTJkNzM1ZmIxZDk3NGFlNzhiZjcyMTA2ZGNhMGYzOTEwMTAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQyYmIwMTNjM2U0YmViMDg0MjFkZWRjZjgxNWNiNjVhNWMzODgxNzhiODdiY2RkMGUwMDAwMDAwMDAwMTk3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiA5ODQ5NDYsICJuIjogMSwgInNjcmlwdCI6ICI3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"
        >>> fund_solver = FundSolver(private_key="92cbbc5990cb5090326a76feeb321cad01048635afe5756523bbf9f7a75bf38b")
        >>> signature = Signature(network="testnet")
        >>> signature.sign(bitcoin_fund_unsigned_raw, fund_solver)
        >>> signature.type()
        "bitcoin_fund_signed"
        """

        if self._type is None:
            raise ValueError("not found type, sign first")
        return self._type

    def sign(self, unsigned_raw, solver):
        """
        Sign unsigned transaction raw.

        :param unsigned_raw: Bitcoin unsigned transaction raw.
        :type unsigned_raw: str
        :param solver: Bitcoin solver
        :type solver: bitcoin.solver.FundSolver, bitcoin.solver.ClaimSolver, bitcoin.solver.RefundSolver
        :returns:  FundSignature, ClaimSignature, RefundSignature -- Bitcoin signature instance.

        >>> from shuttle.providers.bitcoin.signature import Signature
        >>> from shuttle.providers.bitcoin.solver import FundSolver
        >>> bitcoin_fund_unsigned_raw = "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTg4OGJlN2VjMDY1MDk3ZDk1NjY0NzYzZjI3NmQ0MjU1NTJkNzM1ZmIxZDk3NGFlNzhiZjcyMTA2ZGNhMGYzOTEwMTAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQyYmIwMTNjM2U0YmViMDg0MjFkZWRjZjgxNWNiNjVhNWMzODgxNzhiODdiY2RkMGUwMDAwMDAwMDAwMTk3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiA5ODQ5NDYsICJuIjogMSwgInNjcmlwdCI6ICI3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"
        >>> fund_solver = FundSolver(private_key="92cbbc5990cb5090326a76feeb321cad01048635afe5756523bbf9f7a75bf38b")
        >>> signature = Signature(network="testnet")
        >>> signature.sign(unsigned_raw=bitcoin_fund_unsigned_raw, solver=fund_solver)
        <shuttle.providers.bitcoin.signature.FundSignature object at 0x0409DAF0>
        """

        transaction = json.loads(b64decode(
            str(unsigned_raw + "=" * (-len(unsigned_raw) % 4)).encode()).decode())
        if "type" not in transaction:
            raise ValueError("invalid Bitcoin unsigned transaction raw")
        self._type = transaction["type"]
        if transaction["type"] == "bitcoin_fund_unsigned":
            return FundSignature(network=self.network, version=self.version)\
                .sign(unsigned_raw=unsigned_raw, solver=solver)
        elif transaction["type"] == "bitcoin_claim_unsigned":
            return ClaimSignature(network=self.network, version=self.version)\
                .sign(unsigned_raw=unsigned_raw, solver=solver)
        elif transaction["type"] == "bitcoin_refund_unsigned":
            return RefundSignature(network=self.network, version=self.version)\
                .sign(unsigned_raw=unsigned_raw, solver=solver)

    def signed_raw(self):
        """
        Get Bitcoin signed transaction raw.

        :returns: str -- Bitcoin signed transaction raw.

        >>> from shuttle.providers.bitcoin.signature import Signature
        >>> from shuttle.providers.bitcoin.solver import FundSolver
        >>> bitcoin_fund_unsigned_raw = "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTg4OGJlN2VjMDY1MDk3ZDk1NjY0NzYzZjI3NmQ0MjU1NTJkNzM1ZmIxZDk3NGFlNzhiZjcyMTA2ZGNhMGYzOTEwMTAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQyYmIwMTNjM2U0YmViMDg0MjFkZWRjZjgxNWNiNjVhNWMzODgxNzhiODdiY2RkMGUwMDAwMDAwMDAwMTk3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiA5ODQ5NDYsICJuIjogMSwgInNjcmlwdCI6ICI3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"
        >>> fund_solver = FundSolver(private_key="92cbbc5990cb5090326a76feeb321cad01048635afe5756523bbf9f7a75bf38b")
        >>> signature = Signature(network="testnet")
        >>> signature.sign(bitcoin_fund_unsigned_raw, fund_solver)
        >>> signature.signed_raw()
        "eyJyYXciOiAiMDIwMDAwMDAwMTg4OGJlN2VjMDY1MDk3ZDk1NjY0NzYzZjI3NmQ0MjU1NTJkNzM1ZmIxZDk3NGFlNzhiZjcyMTA2ZGNhMGYzOTEwMTAwMDAwMDZiNDgzMDQ1MDIyMTAwYzkwZjA3MmNhM2NkMWFjNDQ2YmJjOTUyZjAwN2RkZDgyYjkzMGU0MTZjZmI3ZTA3YjBiNTZlYzUwNjU5NzBiMTAyMjAyZGNkMjhjOTJkOWRmZTZhNjcyNTE2MDJlNTA3NWNmMjFjM2VjMGJiZTQzZWQwNzQyZGJmOWNkYmZlMmQwZDgwMDEyMTAzYzU2YTYwMDVkNGE4ODkyZDI4Y2MzZjcyNjVlNTY4NWI1NDg2MjdkNTkxMDg5NzNlNDc0YzRlMjZmNjlhNGM4NGZmZmZmZmZmMDIxMDI3MDAwMDAwMDAwMDAwMTdhOTE0MmJiMDEzYzNlNGJlYjA4NDIxZGVkY2Y4MTVjYjY1YTVjMzg4MTc4Yjg3YmNkZDBlMDAwMDAwMDAwMDE5NzZhOTE0NjRhODM5MGIwYjE2ODVmY2JmMmQ0YjQ1NzExOGRjOGRhOTJkNTUzNDg4YWMwMDAwMDAwMCIsICJmZWUiOiA2NzgsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfc2lnbmVkIn0"
        """

        if self._signed_raw is None:
            raise ValueError("there is no signed data, sign first")
        return self._signed_raw


# Fund signature
class FundSignature(Signature):
    """
    Bitcoin FundSignature class.

    :param version: Bitcoin fund signature transaction version, defaults to 2.
    :type version: int
    :param network: Bitcoin network, defaults to testnet.
    :type network: str
    :returns:  FundSignature -- Bitcoin fund signature instance.
    """

    def __init__(self, network="testnet", version=2):
        super().__init__(network=network, version=version)

    def sign(self, unsigned_raw, solver):
        """
        Sign unsigned fund transaction raw.

        :param unsigned_raw: Bitcoin unsigned fund transaction raw.
        :type unsigned_raw: str
        :param solver: Bitcoin fund solver.
        :type solver: bitcoin.solver.FundSolver
        :returns:  FundSignature -- Bitcoin fund signature instance.

        >>> from shuttle.providers.bitcoin.signature import FundSignature
        >>> from shuttle.providers.bitcoin.solver import FundSolver
        >>> bitcoin_fund_unsigned_raw = "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTg4OGJlN2VjMDY1MDk3ZDk1NjY0NzYzZjI3NmQ0MjU1NTJkNzM1ZmIxZDk3NGFlNzhiZjcyMTA2ZGNhMGYzOTEwMTAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQyYmIwMTNjM2U0YmViMDg0MjFkZWRjZjgxNWNiNjVhNWMzODgxNzhiODdiY2RkMGUwMDAwMDAwMDAwMTk3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiA5ODQ5NDYsICJuIjogMSwgInNjcmlwdCI6ICI3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"
        >>> fund_solver = FundSolver("92cbbc5990cb5090326a76feeb321cad01048635afe5756523bbf9f7a75bf38b")
        >>> fund_signature = FundSignature(network="testnet")
        >>> fund_signature.sign(bitcoin_fund_unsigned_raw, fund_solver)
        <shuttle.providers.bitcoin.signature.FundSignature object at 0x0409DAF0>
        """

        # Decoding and loading refund transaction
        fund_transaction = json.loads(b64decode(
            str(unsigned_raw + "=" * (-len(unsigned_raw) % 4)).encode()).decode())
        # Checking refund transaction keys
        for key in ["raw", "outputs", "type", "fee", "network"]:
            if key not in fund_transaction:
                raise ValueError("invalid Bitcoin unsigned fund transaction raw")
        if not fund_transaction["type"] == "bitcoin_fund_unsigned":
            raise TypeError(f"invalid Bitcoin fund unsigned transaction type, "
                            f"you can't sign this {fund_transaction['type']} type by using FundSignature")
        if not isinstance(solver, FundSolver):
            raise TypeError("invalid Bitcoin solver, it's only takes Bitcoin FundSolver class")

        # Setting transaction fee, type, network and transaction
        self._fee, self._type, self.network, self.transaction = (
            fund_transaction["fee"], fund_transaction["type"],
            fund_transaction["network"], MutableTransaction.unhexlify(fund_transaction["raw"])
        )

        # Organizing outputs
        outputs = []
        for output in fund_transaction["outputs"]:
            outputs.append(
                TxOut(
                    value=output["amount"],
                    n=output["n"],
                    script_pubkey=Script.unhexlify(
                        hex_string=output["script"]
                    )
                )
            )
        # Signing fund transaction
        self.transaction.spend(outputs, [solver.solve() for _ in outputs])

        # Encoding fund transaction raw
        self._type = "bitcoin_fund_signed"
        self._signed_raw = b64encode(str(json.dumps(dict(
            raw=self.transaction.hexlify(),
            fee=fund_transaction["fee"],
            network=fund_transaction["network"],
            type=self._type
        ))).encode()).decode()
        return self


# Claim signature
class ClaimSignature(Signature):
    """
    Bitcoin ClaimSignature class.

    :param version: Bitcoin claim signature transaction version, defaults to 2.
    :type version: int
    :param network: Bitcoin network, defaults to testnet.
    :type network: str
    :returns:  ClaimSignature -- Bitcoin claim signature instance.
    """

    def __init__(self, network="testnet", version=2):
        super().__init__(network=network, version=version)

    def sign(self, unsigned_raw, solver):
        """
        Sign unsigned claim transaction raw.

        :param unsigned_raw: Bitcoin unsigned claim transaction raw.
        :type unsigned_raw: str
        :param solver: Bitcoin claim solver.
        :type solver: bitcoin.solver.ClaimSolver
        :returns:  ClaimSignature -- Bitcoin claim signature instance.

        >>> from shuttle.providers.bitcoin.signature import ClaimSignature
        >>> from shuttle.providers.bitcoin.solver import ClaimSolver
        >>> bitcoin_claim_unsigned_raw = "eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTUyYzIzZGM2NDU2N2IxY2ZhZjRkNzc2NjBjNzFjNzUxZjkwZTliYTVjMzc0N2ZhYzFkMDA1MTgwOGVhMGQ2NTEwMDAwMDAwMDAwZmZmZmZmZmYwMTQ4MTEwMDAwMDAwMDAwMDAxOTc2YTkxNDY0YTgzOTBiMGIxNjg1ZmNiZjJkNGI0NTcxMThkYzhkYTkyZDU1MzQ4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsidmFsdWUiOiA1MDAwLCAibiI6IDAsICJzY3JpcHRfcHVia2V5IjogImE5MTQ0MzNlOGVkNTliOWE2N2YwZjE4N2M2M2ViNDUwYjBkNTZlMjU2ZWMyODcifSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fcmVmdW5kX3Vuc2lnbmVkIn0"
        >>> claim_solver = ClaimSolver("6bc3b581f3dea1963f9257ec2a0195969babee3704e6ba7cd2ec535140b9816f", "Hello Meheret!", "3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb",  "muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB", "mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q", 1000)
        >>> claim_signature = ClaimSignature(network="testnet")
        >>> claim_signature.sign(unsigned_raw=bitcoin_claim_unsigned_raw, solver=claim_solver)
        <shuttle.providers.bitcoin.signature.ClaimSignature object at 0x0409DAF0>
        """

        # Decoding and loading claim transaction
        claim_transaction = json.loads(b64decode(
            str(unsigned_raw + "=" * (-len(unsigned_raw) % 4)).encode()).decode())
        # Checking claim transaction keys
        for key in ["raw", "outputs", "type", "fee", "network"]:
            if key not in claim_transaction:
                raise ValueError("invalid Bitcoin unsigned claim transaction raw")
        if not claim_transaction["type"] == "bitcoin_claim_unsigned":
            raise TypeError(f"invalid Bitcoin claim unsigned transaction type, "
                            f"you can't sign this {claim_transaction['type']} type by using ClaimSignature")
        if not isinstance(solver, ClaimSolver):
            raise TypeError("invalid Bitcoin solver, it's only takes Bitcoin ClaimSolver class")

        # Setting transaction fee, type, network and transaction
        self._fee, self._type, self.network, self.transaction = (
            claim_transaction["fee"], claim_transaction["type"],
            claim_transaction["network"], MutableTransaction.unhexlify(claim_transaction["raw"])
        )

        # Signing claim transaction
        self.transaction.spend([
            TxOut(
                value=claim_transaction["outputs"]["amount"],
                n=claim_transaction["outputs"]["n"],
                script_pubkey=P2shScript.unhexlify(
                    hex_string=claim_transaction["outputs"]["script"])
            )
        ], [
            P2shSolver(
                redeem_script=solver.witness(
                    network=claim_transaction["network"]
                ),
                redeem_script_solver=solver.solve()
            )
        ])

        # Encoding refund transaction raw
        self._type = "bitcoin_claim_signed"
        self._signed_raw = b64encode(str(json.dumps(dict(
            raw=self.transaction.hexlify(),
            fee=claim_transaction["fee"],
            network=claim_transaction["network"],
            type=self._type
        ))).encode()).decode()
        return self


# Refund signature
class RefundSignature(Signature):
    """
    Bitcoin RefundSignature class.

    :param version: Bitcoin refund signature transaction version, defaults to 2.
    :type version: int
    :param network: Bitcoin network, defaults to testnet.
    :type network: str
    :returns:  RefundSignature -- Bitcoin claim signature instance.
    """

    def __init__(self, network="testnet", version=2):
        super().__init__(network=network, version=version)

    def sign(self, unsigned_raw, solver):
        """
        Sign unsigned refund transaction raw.

        :param unsigned_raw: Bitcoin unsigned refund transaction raw.
        :type unsigned_raw: str
        :param solver: Bitcoin refund solver.
        :type solver: bitcoin.solver.RefundSolver
        :returns:  RefundSignature -- Bitcoin refund signature instance.

        >>> from shuttle.providers.bitcoin.signature import RefundSignature
        >>> from shuttle.providers.bitcoin.solver import RefundSolver
        >>> bitcoin_refund_unsigned_raw = "eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTUyYzIzZGM2NDU2N2IxY2ZhZjRkNzc2NjBjNzFjNzUxZjkwZTliYTVjMzc0N2ZhYzFkMDA1MTgwOGVhMGQ2NTEwMDAwMDAwMDAwZmZmZmZmZmYwMTQ4MTEwMDAwMDAwMDAwMDAxOTc2YTkxNDY0YTgzOTBiMGIxNjg1ZmNiZjJkNGI0NTcxMThkYzhkYTkyZDU1MzQ4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsidmFsdWUiOiA1MDAwLCAibiI6IDAsICJzY3JpcHRfcHVia2V5IjogImE5MTQ0MzNlOGVkNTliOWE2N2YwZjE4N2M2M2ViNDUwYjBkNTZlMjU2ZWMyODcifSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fcmVmdW5kX3Vuc2lnbmVkIn0"
        >>> refund_solver = RefundSolver("92cbbc5990cb5090326a76feeb321cad01048635afe5756523bbf9f7a75bf38b", "3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb",  "muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB", "mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q", 1000)
        >>> refund_signature = RefundSignature(network="testnet")
        >>> refund_signature.sign(unsigned_raw=bitcoin_refund_unsigned_raw, solver=refund_solver)
        <shuttle.providers.bitcoin.signature.RefundSignature object at 0x0409DAF0>
        """

        # Decoding and loading refund transaction
        refund_transaction = json.loads(b64decode(
            str(unsigned_raw + "=" * (-len(unsigned_raw) % 4)).encode()).decode())
        # Checking refund transaction keys
        for key in ["raw", "outputs", "type", "fee", "network"]:
            if key not in refund_transaction:
                raise ValueError("invalid Bitcoin unsigned refund transaction raw")
        if not refund_transaction["type"] == "bitcoin_refund_unsigned":
            raise TypeError(f"invalid Bitcoin refund unsigned transaction type, "
                            f"you can't sign this {refund_transaction['type']} type by using RefundSignature")
        if not isinstance(solver, RefundSolver):
            raise TypeError("invalid Bitcoin solver, it's only takes Bitcoin RefundSolver class")

        # Setting transaction fee, type, network and transaction
        self._fee, self._type, self.network, self.transaction = (
            refund_transaction["fee"], refund_transaction["type"],
            refund_transaction["network"], MutableTransaction.unhexlify(refund_transaction["raw"])
        )

        # Signing refund transaction
        self.transaction.spend([
            TxOut(
                value=refund_transaction["outputs"]["value"],
                n=refund_transaction["outputs"]["n"],
                script_pubkey=P2shScript.unhexlify(
                    hex_string=refund_transaction["outputs"]["script_pubkey"]
                )
            )
        ], [
            P2shSolver(
                redeem_script=solver.witness(
                    network=refund_transaction["network"]
                ),
                redeem_script_solver=solver.solve()
            )
        ])

        # Encoding refund transaction raw
        self._type = "bitcoin_refund_signed"
        self._signed_raw = b64encode(str(json.dumps(dict(
            raw=self.transaction.hexlify(),
            fee=refund_transaction["fee"],
            network=refund_transaction["network"],
            type=self._type
        ))).encode()).decode()
        return self
