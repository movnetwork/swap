#!/usr/bin/env python3

from base64 import b64encode, b64decode
from btcpy.structs.address import Address
from btcpy.structs.script import ScriptSig, Script, P2pkhScript, P2shScript
from btcpy.structs.transaction import Locktime, MutableTransaction, TxOut, Sequence, TxIn
from btcpy.structs.sig import P2shSolver
from btcpy.setup import setup

import json

from .utils import double_sha256, fee_calculator
from .solver import ClaimSolver, FundSolver, RefundSolver
from .rpc import get_transaction_detail
from .htlc import HTLC
from .wallet import Wallet
from ...utils.exceptions import BalanceError, NotFoundError


class Transaction:
    """
    Bitcoin Transaction class.

    :param version: bitcoin transaction version, defaults to 2.
    :type version: int
    :param network: bitcoin network, defaults to testnet.
    :type network: str
    :returns:  Transaction -- bitcoin transaction instance.

    .. note::
        Bitcoin has only two networks, ``mainnet`` and ``testnet``.
    """

    # Initialization transaction
    def __init__(self, version=2, network="testnet"):
        # Transaction build version
        self.version = version
        # Transaction
        self.transaction = None
        # Bitcoin network
        self.mainnet = None
        self.network = network
        if self.network == "mainnet":
            self.mainnet = True
        elif self.network == "testnet":
            self.mainnet = False
        else:
            raise ValueError("invalid network, only mainnet or testnet")
        # Bitcoin fee
        self.fee = int()
        # Setting testnet
        setup(network, strict=True)

    # Transaction hash
    def hash(self):
        """
        Get bitcoin transaction hash.

        :returns: str -- bitcoin transaction hash or transaction id.

        >>> transaction.hash()
        "9cc0524fb8e7b2c5fecaee4eb91d43a3dc5cc18e9906abcb35a5732ff52efcc7"
        """

        if self.transaction is None:
            raise ValueError("transaction script is none, build transaction first.")
        return self.transaction.txid

    # Transaction json format
    def json(self):
        """
        Get bitcoin transaction json format.

        :returns: dict -- bitcoin transaction json format.

        >>> transaction.json()
        {"hex": "02000000012c392217483906f902e73c4bc132864de58153772d79268960998162266634be0100000000ffffffff02e80300000000000017a914971894c58d85981c16c2059d422bcde0b156d04487a6290000000000001976a9146bce65e58a50b97989930e9a4ff1ac1a77515ef188ac00000000", "txid": "9cc0524fb8e7b2c5fecaee4eb91d43a3dc5cc18e9906abcb35a5732ff52efcc7", "hash": "9cc0524fb8e7b2c5fecaee4eb91d43a3dc5cc18e9906abcb35a5732ff52efcc7", "size": 117, "vsize": 117, "version": 2, "locktime": 0, "vin": [{"txid": "be346626628199608926792d775381e54d8632c14b3ce702f90639481722392c", "vout": 1, "scriptSig": {"asm": "", "hex": ""}, "sequence": "4294967295"}], "vout": [{"value": "0.00001000", "n": 0, "scriptPubKey": {"asm": "OP_HASH160 971894c58d85981c16c2059d422bcde0b156d044 OP_EQUAL", "hex": "a914971894c58d85981c16c2059d422bcde0b156d04487", "type": "p2sh", "address": "2N729UBGZB3xjsGFRgKivy4bSjkaJGMVSpB"}}, {"value": "0.00010662", "n": 1, "scriptPubKey": {"asm": "OP_DUP OP_HASH160 6bce65e58a50b97989930e9a4ff1ac1a77515ef1 OP_EQUALVERIFY OP_CHECKSIG", "hex": "76a9146bce65e58a50b97989930e9a4ff1ac1a77515ef188ac", "type": "p2pkh", "address": "mqLyrNDjpENRMZAoDpspH7kR9RtgvhWzYE"}}]}
        """

        if self.transaction is None:
            raise ValueError("transaction script is none, build transaction first.")
        return self.transaction.to_json()

    # Transaction raw
    def raw(self):
        """
        Get bitcoin transaction raw.

        :returns: str -- bitcoin transaction raw.

        >>> transaction.raw()
        "02000000012c392217483906f902e73c4bc132864de58153772d79268960998162266634be0100000000ffffffff02e80300000000000017a914971894c58d85981c16c2059d422bcde0b156d04487a6290000000000001976a9146bce65e58a50b97989930e9a4ff1ac1a77515ef188ac00000000"
        """

        if self.transaction is None:
            raise ValueError("transaction script is none, build transaction first.")
        return self.transaction.hexlify()

    @staticmethod
    def inputs(utxos, previous_transaction_indexes=None):
        inputs, amount = list(), int()
        for index, utxo in enumerate(utxos):
            if previous_transaction_indexes is None or index in previous_transaction_indexes:
                amount += utxo["amount"]
                inputs.append(
                    TxIn(txid=utxo["hash"], txout=utxo["output_index"],
                         script_sig=ScriptSig.empty(), sequence=Sequence.max()))
        return inputs, amount

    @staticmethod
    def outputs(utxos, previous_transaction_indexes=None):
        outputs = list()
        for index, utxo in enumerate(utxos):
            if previous_transaction_indexes is None or index in previous_transaction_indexes:
                outputs.append(
                    TxOut(value=utxo["amount"], n=utxo["output_index"],
                          script_pubkey=Script.unhexlify(utxo["script"])))
        return outputs


class FundTransaction(Transaction):
    """
    Bitcoin FundTransaction class.

    :param version: bitcoin transaction version, defaults to 2.
    :type version: int
    :param network: bitcoin network, defaults to testnet.
    :type network: str
    :returns: FundTransaction -- bitcoin fund transaction instance.

    .. warning::
        Do not forget to build transaction after initialize fund transaction.

    :fee: Get bitcoin fund transaction fee.

    >>> fund_transaction.fee
    675
    """

    # Initialization fund transaction
    def __init__(self, version=2, network="testnet"):
        super().__init__(version=version, network=network)
        # Initialization wallet, htlc, amount and unspent
        self.wallet, self.htlc, self.amount, self.unspent = None, None, None, None
        # Getting previous transaction indexes using funding amount
        self.previous_transaction_indexes = None

    # Building transaction
    def build_transaction(self, wallet, htlc, amount, locktime=0):
        """
        Build bitcoin fund transaction.

        :param wallet: bitcoin sender wallet.
        :type wallet: bitcoin.wallet.Wallet
        :param htlc: bitcoin hash time lock contract (HTLC).
        :type htlc: bitcoin.htlc.HTLC
        :param amount: bitcoin amount to fund.
        :type amount: int
        :param locktime: bitcoin transaction lock time, defaults to 0.
        :type locktime: int
        :returns: FundTransaction -- bitcoin fund transaction instance.

        >>> from shuttle.providers.bitcoin.transaction import FundTransaction
        >>> fund_transaction = FundTransaction(network="testnet")
        >>> fund_transaction.build_transaction(sender_wallet, htlc, 10000)
        <shuttle.providers.bitcoin.transaction.FundTransaction object at 0x0409DAF0>
        """

        # Checking build transaction arguments instance
        if not isinstance(wallet, Wallet):
            raise TypeError("invalid wallet instance, only takes bitcoin Wallet class")
        if not isinstance(htlc, HTLC):
            raise TypeError("invalid htlc instance, only takes bitcoin HTLC class")
        if not isinstance(amount, int):
            raise TypeError("invalid amount instance, only takes integer type")
        # Setting wallet, htlc, amount and unspent
        self.wallet, self.htlc, self.amount = wallet, htlc, amount
        # Getting unspent transaction output
        self.unspent = self.wallet.unspent()
        # Setting previous transaction indexes
        self.previous_transaction_indexes = \
            self.get_previous_transaction_indexes(amount=self.amount)
        # Getting transaction inputs and amount
        inputs, amount = self.inputs(self.unspent, self.previous_transaction_indexes)
        # Calculating bitcoin fee
        self.fee = fee_calculator(len(inputs), 2)
        if amount < (self.amount + self.fee):
            raise BalanceError("insufficient spend utxos")
        # Building mutable bitcoin transaction
        self.transaction = MutableTransaction(
            version=self.version, ins=inputs,
            outs=[
                # Funding into hash time lock contract script hash
                TxOut(value=self.amount, n=0,
                      script_pubkey=P2shScript.unhexlify(self.htlc.hash())),
                # Controlling amounts when we are funding on htlc script.
                TxOut(value=amount - (self.fee + self.amount), n=1,
                      script_pubkey=P2pkhScript.unhexlify(self.wallet.p2pkh()))
            ], locktime=Locktime(locktime))
        return self

    # Signing transaction using fund solver
    def sign(self, solver):
        """
        Sign bitcoin fund transaction.

        :param solver: bitcoin fund solver.
        :type solver: bitcoin.solver.FundSolver
        :returns: FundTransaction -- bitcoin fund transaction instance.

        >>> from shuttle.providers.bitcoin.transaction import FundTransaction
        >>> fund_transaction = FundTransaction(network="testnet")
        >>> fund_transaction.build_transaction(sender_wallet, htlc, 10000)
        >>> fund_transaction.sign(fund_solver)
        <shuttle.providers.bitcoin.transaction.FundTransaction object at 0x0409DAF0>
        """

        if not isinstance(solver, FundSolver):
            raise TypeError("invalid solver instance, only takes bitcoin FundSolver class")
        if not self.unspent or not self.previous_transaction_indexes or not self.transaction:
            raise ValueError("transaction script or unspent is none, build transaction first")
        outputs = self.outputs(self.unspent, self.previous_transaction_indexes)
        self.transaction.spend(outputs, [solver.solve() for _ in outputs])
        return self

    # Automatically analysis previous transaction indexes using fund amount
    def get_previous_transaction_indexes(self, amount=None):
        if amount is None:
            amount = self.amount
        temp_amount = int()
        previous_transaction_indexes = list()
        for index, unspent in enumerate(self.unspent):
            temp_amount += unspent["amount"]
            if temp_amount > (amount + fee_calculator((index + 1), 2)):
                previous_transaction_indexes.append(index)
                break
            previous_transaction_indexes.append(index)
        return previous_transaction_indexes

    def unsigned_raw(self):
        """
        Get bitcoin unsigned fund transaction raw.

        :returns: str -- bitcoin unsigned fund transaction raw.

        >>> from shuttle.providers.bitcoin.transaction import FundTransaction
        >>> fund_transaction = FundTransaction(network="testnet")
        >>> fund_transaction.build_transaction(sender_wallet, htlc, 10000)
        >>> fund_transaction.unsigned_raw()
        "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTJjMzkyMjE3NDgzOTA2ZjkwMmU3M2M0YmMxMzI4NjRkZTU4MTUzNzcyZDc5MjY4OTYwOTk4MTYyMjY2NjM0YmUwMTAwMDAwMDAwZmZmZmZmZmYwMmU4MDMwMDAwMDAwMDAwMDAxN2E5MTQ5NzE4OTRjNThkODU5ODFjMTZjMjA1OWQ0MjJiY2RlMGIxNTZkMDQ0ODdhNjI5MDAwMDAwMDAwMDAwMTk3NmE5MTQ2YmNlNjVlNThhNTBiOTc5ODk5MzBlOWE0ZmYxYWMxYTc3NTE1ZWYxODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiAxMjM0MCwgIm4iOiAxLCAic2NyaXB0IjogIjc2YTkxNDZiY2U2NWU1OGE1MGI5Nzk4OTkzMGU5YTRmZjFhYzFhNzc1MTVlZjE4OGFjIn1dLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfdW5zaWduZWQifQ"
        """
        outputs = list()
        if not self.transaction or not self.unspent:
            raise ValueError("transaction script or unspent is none, build transaction first")
        for index, utxo in enumerate(self.unspent):
            if self.previous_transaction_indexes is None or index in self.previous_transaction_indexes:
                outputs.append(dict(amount=utxo["amount"],
                               n=utxo["output_index"], script=utxo["script"]))
        return b64encode(str(json.dumps(dict(
            fee=self.fee,
            raw=self.transaction.hexlify(),
            outputs=outputs,
            network=self.network,
            type="bitcoin_fund_unsigned"
        ))).encode()).decode()


class ClaimTransaction(Transaction):
    """
    Bitcoin ClaimTransaction class.

    :param version: bitcoin transaction version, defaults to 2.
    :type version: int
    :param network: bitcoin network, defaults to testnet.
    :type network: str
    :returns:  Transaction -- bitcoin transaction instance.

    .. warning::
        Do not forget to build transaction after initialize claim transaction.

    :fee: Get bitcoin claim transaction fee.

    >>> claim_transaction.fee
    675
    """

    # Initialization claim transaction
    def __init__(self, network="testnet", version=2):
        super().__init__(network=network, version=version)
        # Initialization transaction_id, wallet, secret and amount
        self.transaction_id, self.wallet, self.amount, self.secret = \
            None, None, None, None
        # Getting transaction detail by id
        self.transaction_detail = None
        # Transaction detail outputs (HTLC and Sender account)
        self.htlc = None
        self.sender_account = None

    # Building transaction
    def build_transaction(self, transaction_id, wallet, amount, secret=None, locktime=0):
        """
        Build bitcoin claim transaction.

        :param transaction_id: bitcoin fund transaction id to redeem.
        :type transaction_id: str
        :param wallet: bitcoin recipient wallet.
        :type wallet: bitcoin.wallet.Wallet
        :param amount: bitcoin amount to withdraw.
        :type amount: int
        :param secret: secret key.
        :type secret: str
        :param locktime: bitcoin transaction lock time, defaults to 0.
        :type locktime: int
        :returns: ClaimTransaction -- bitcoin claim transaction instance.

        >>> from shuttle.providers.bitcoin.transaction import ClaimTransaction
        >>> claim_transaction = ClaimTransaction(network="testnet")
        >>> claim_transaction.build_transaction(fund_transaction_id, recipient_wallet, 10000)
        <shuttle.providers.bitcoin.transaction.ClaimTransaction object at 0x0409DAF0>
        """

        # Checking build transaction arguments instance
        if not isinstance(transaction_id, str):
            raise TypeError("invalid amount instance, only takes string type")
        if not isinstance(wallet, Wallet):
            raise TypeError("invalid wallet instance, only takes bitcoin Wallet class")
        if secret is not None and not isinstance(secret, str):
            raise TypeError("invalid secret instance, only takes string type")
        # Setting transaction_id and wallet
        self.transaction_id, self.wallet, self.secret = transaction_id, wallet, secret
        # Getting transaction detail by id
        self.transaction_detail = get_transaction_detail(self.transaction_id)
        # Checking transaction outputs
        if "outputs" not in self.transaction_detail:
            raise NotFoundError("not found htlc in this %s hash" % self.transaction_id)
        # Hash time lock contract output
        self.htlc = self.transaction_detail["outputs"][0]
        # Sender account output
        sender_address = P2pkhScript.unhexlify(
            self.transaction_detail["outputs"][1]["script"]).address(mainnet=self.mainnet)
        self.sender_account = Wallet(network=self.network).from_address(str(sender_address))
        # HTLC info's
        htlc_amount = self.htlc["value"]
        htlc_script = P2shScript.unhexlify(self.htlc["script"])
        htlc_address = htlc_script.address(mainnet=self.mainnet)
        # Calculating fee
        self.fee = fee_calculator(1, 1)
        if amount < self.fee:
            raise BalanceError("insufficient spend utxos")
        elif not htlc_amount >= (amount - self.fee):
            raise BalanceError("insufficient spend utxos", "maximum withdraw %d" % htlc_amount)
        # Building mutable bitcoin transaction
        self.transaction = MutableTransaction(
            version=self.version,
            ins=[
                TxIn(txid=self.transaction_id, txout=0,
                     script_sig=ScriptSig.empty(), sequence=Sequence.max())
            ],
            outs=[
                TxOut(value=(amount - self.fee), n=0,
                      script_pubkey=P2pkhScript.unhexlify(self.wallet.p2pkh()))
            ], locktime=Locktime(locktime))
        return self

    # Signing transaction using private keys
    def sign(self, solver):
        """
        Sign bitcoin claim transaction.

        :param solver: bitcoin claim solver.
        :type solver: bitcoin.solver.ClaimSolver
        :returns: ClaimTransaction -- bitcoin claim transaction instance.

        >>> from shuttle.providers.bitcoin.transaction import ClaimTransaction
        >>> claim_transaction = ClaimTransaction(network="testnet")
        >>> claim_transaction.build_transaction(fund_transaction_id, recipient_wallet, 10000)
        >>> claim_transaction.sign(claim_solver)
        <shuttle.providers.bitcoin.transaction.ClaimTransaction object at 0x0409DAF0>
        """

        if not isinstance(solver, ClaimSolver):
            raise TypeError("invalid solver instance, only takes bitcoin ClaimSolver class")
        if self.transaction is None:
            raise ValueError("transaction script is none, build transaction first")
        htlc = HTLC(self.network).init(
            secret_hash=double_sha256(solver.secret),
            recipient_address=str(self.wallet.address()),
            sender_address=str(self.sender_account.address()),
            sequence=solver.sequence
        )
        self.transaction.spend([
            TxOut(value=self.htlc["value"], n=0,
                  script_pubkey=P2shScript.unhexlify(self.htlc["script"]))
        ], [
            P2shSolver(htlc.script, solver.solve())
        ])
        return self

    def unsigned_raw(self):
        """
        Get bitcoin unsigned claim transaction raw.

        :returns: str -- bitcoin unsigned claim transaction raw.

        >>> from shuttle.providers.bitcoin.transaction import ClaimTransaction
        >>> claim_transaction = ClaimTransaction(network="testnet")
        >>> claim_transaction.build_transaction(fund_transaction_id, recipient_wallet, 10000)
        >>> claim_transaction.unsigned_raw()
        "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTJjMzkyMjE3NDgzOTA2ZjkwMmU3M2M0YmMxMzI4NjRkZTU4MTUzNzcyZDc5MjY4OTYwOTk4MTYyMjY2NjM0YmUwMTAwMDAwMDAwZmZmZmZmZmYwMmU4MDMwMDAwMDAwMDAwMDAxN2E5MTQ5NzE4OTRjNThkODU5ODFjMTZjMjA1OWQ0MjJiY2RlMGIxNTZkMDQ0ODdhNjI5MDAwMDAwMDAwMDAwMTk3NmE5MTQ2YmNlNjVlNThhNTBiOTc5ODk5MzBlOWE0ZmYxYWMxYTc3NTE1ZWYxODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiAxMjM0MCwgIm4iOiAxLCAic2NyaXB0IjogIjc2YTkxNDZiY2U2NWU1OGE1MGI5Nzk4OTkzMGU5YTRmZjFhYzFhNzc1MTVlZjE4OGFjIn1dLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfdW5zaWduZWQifQ"
        """
        if self.transaction is None:
            raise ValueError("transaction script is none, build transaction first")
        outputs = [dict(amount=self.htlc["value"], n=0, script=self.htlc["script"])]
        return b64encode(str(json.dumps(dict(
            fee=self.fee,
            raw=self.transaction.hexlify(),
            outputs=outputs,
            recipient_address=str(self.wallet.address()),
            sender_address=str(self.sender_account.address()),
            secret=self.secret,
            network=self.network,
            type="bitcoin_claim_unsigned"
        ))).encode()).decode()


class RefundTransaction(Transaction):
    """
    Bitcoin RefundTransaction class.

    :param version: bitcoin transaction version, defaults to 2.
    :type version: int
    :param network: bitcoin network, defaults to testnet.
    :type network: str
    :returns:  Transaction -- bitcoin transaction instance.

    .. warning::
        Do not forget to build transaction after initialize refund transaction.

    :fee: Get bitcoin refund transaction fee.

    >>> refund_transaction.fee
    675
    """

    # Initialization claim transaction
    def __init__(self, version=2, network="testnet"):
        super().__init__(version=version, network=network)
        # Initialization transaction_id, wallet and amount
        self.transaction_id, self.wallet, self.amount, self.secret = \
            None, None, None, None
        # Getting transaction detail by id
        self.transaction_detail = None
        # Transaction detail outputs (HTLC and Sender account)
        self.htlc = None
        self.sender_account = None

    # Building transaction
    def build_transaction(self, transaction_id, wallet, amount, secret=None, locktime=0):
        """
        Build bitcoin refund transaction.

        :param transaction_id: bitcoin fund transaction id to redeem.
        :type transaction_id: str
        :param wallet: bitcoin sender wallet.
        :type wallet: bitcoin.wallet.Wallet
        :param amount: bitcoin amount to withdraw.
        :type amount: int
        :param secret: secret passphrase.
        :type secret: str
        :param locktime: bitcoin transaction lock time, defaults to 0.
        :type locktime: int
        :returns: RefundTransaction -- bitcoin refund transaction instance.

        >>> from shuttle.providers.bitcoin.transaction import RefundTransaction
        >>> refund_transaction = RefundTransaction(network="testnet")
        >>> refund_transaction.build_transaction(fund_transaction_id, sender_wallet, 10000)
        <shuttle.providers.bitcoin.transaction.RefundTransaction object at 0x0409DAF0>
        """

        # Checking build transaction arguments instance
        if not isinstance(transaction_id, str):
            raise TypeError("invalid amount instance, only takes string type")
        if not isinstance(wallet, Wallet):
            raise TypeError("invalid wallet instance, only takes bitcoin Wallet class")
        if secret is not None and not isinstance(secret, str):
            raise TypeError("invalid secret instance, only takes string type")
        # Setting transaction_id and wallet
        self.transaction_id, self.wallet, self.secret = transaction_id, wallet, secret
        # Getting transaction detail by id
        self.transaction_detail = get_transaction_detail(self.transaction_id)
        # Checking transaction outputs
        if "outputs" not in self.transaction_detail:
            raise NotFoundError("not found htlc in this %s hash" % self.transaction_id)
        # Hash time lock contract output
        self.htlc = self.transaction_detail["outputs"][0]
        # Sender account output
        sender_address = P2pkhScript.unhexlify(
            self.transaction_detail["outputs"][1]["script"]).address(mainnet=self.mainnet)
        self.sender_account = Wallet(network=self.network).from_address(str(sender_address))
        # HTLC info's
        htlc_amount = self.htlc["value"]
        htlc_script = P2shScript.unhexlify(self.htlc["script"])
        htlc_address = htlc_script.address(mainnet=self.mainnet)
        # Calculating fee
        self.fee = fee_calculator(1, 1)
        if amount < self.fee:
            raise BalanceError("insufficient spend utxos")
        elif not htlc_amount >= (amount - self.fee):
            raise BalanceError("insufficient spend utxos", "maximum withdraw %d" % htlc_amount)
        # Building mutable bitcoin transaction
        self.transaction = MutableTransaction(
            version=self.version,
            ins=[
                TxIn(txid=self.transaction_id, txout=0,
                     script_sig=ScriptSig.empty(), sequence=Sequence.max())
            ],
            outs=[
                TxOut(value=(amount - self.fee), n=0,
                      script_pubkey=P2pkhScript.unhexlify(self.wallet.p2pkh()))
            ], locktime=Locktime(locktime))
        return self

    # Signing transaction using private keys
    def sign(self, solver):
        """
        Sign bitcoin refund transaction.

        :param solver: bitcoin refund solver.
        :type solver: bitcoin.solver.RefundSolver
        :returns: RefundTransaction -- bitcoin refund transaction instance.

        >>> from shuttle.providers.bitcoin.transaction import RefundTransaction
        >>> refund_transaction = RefundTransaction(network="testnet")
        >>> refund_transaction.build_transaction(fund_transaction_id, sender_wallet, 10000)
        >>> refund_transaction.sign(refund_solver)
        <shuttle.providers.bitcoin.transaction.RefundTransaction object at 0x0409DAF0>
        """
        if not isinstance(solver, RefundSolver):
            raise TypeError("invalid solver instance, only takes bitcoin RefundSolver class")
        if self.transaction is None:
            raise ValueError("transaction script is none, build transaction first")
        htlc = HTLC(self.network).init(
            secret_hash=double_sha256(solver.secret),
            recipient_address=str(self.wallet.address()),
            sender_address=str(self.sender_account.address()),
            sequence=solver.sequence
        )
        self.transaction.spend([
            TxOut(value=self.htlc["value"], n=0,
                  script_pubkey=P2shScript.unhexlify(self.htlc["script"]))
        ], [
            P2shSolver(htlc.script, solver.solve())
        ])
        return self

    def unsigned_raw(self):
        """
        Get bitcoin unsigned refund transaction raw.

        :returns: str -- bitcoin unsigned refund transaction raw.

        >>> from shuttle.providers.bitcoin.transaction import RefundTransaction
        >>> refund_transaction = RefundTransaction(network="testnet")
        >>> refund_transaction.build_transaction(fund_transaction_id, sender_wallet, 10000)
        >>> refund_transaction.unsigned_raw()
        "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTJjMzkyMjE3NDgzOTA2ZjkwMmU3M2M0YmMxMzI4NjRkZTU4MTUzNzcyZDc5MjY4OTYwOTk4MTYyMjY2NjM0YmUwMTAwMDAwMDAwZmZmZmZmZmYwMmU4MDMwMDAwMDAwMDAwMDAxN2E5MTQ5NzE4OTRjNThkODU5ODFjMTZjMjA1OWQ0MjJiY2RlMGIxNTZkMDQ0ODdhNjI5MDAwMDAwMDAwMDAwMTk3NmE5MTQ2YmNlNjVlNThhNTBiOTc5ODk5MzBlOWE0ZmYxYWMxYTc3NTE1ZWYxODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiAxMjM0MCwgIm4iOiAxLCAic2NyaXB0IjogIjc2YTkxNDZiY2U2NWU1OGE1MGI5Nzk4OTkzMGU5YTRmZjFhYzFhNzc1MTVlZjE4OGFjIn1dLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfdW5zaWduZWQifQ"
        """
        if self.transaction is None:
            raise ValueError("transaction script is none, build transaction first")
        outputs = [dict(amount=self.htlc["value"], n=0, script=self.htlc["script"])]
        return b64encode(str(json.dumps(dict(
            fee=self.fee,
            raw=self.transaction.hexlify(),
            outputs=outputs,
            recipient_address=str(self.wallet.address()),
            sender_address=str(self.sender_account.address()),
            secret=self.secret,
            network=self.network,
            type="bitcoin_refund_unsigned"
        ))).encode()).decode()
