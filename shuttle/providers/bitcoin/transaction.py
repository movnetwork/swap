#!/usr/bin/env python3

from base64 import b64encode
from btcpy.structs.script import ScriptSig, Script, P2pkhScript, P2shScript
from btcpy.structs.transaction import Locktime, MutableTransaction, TxOut, Sequence, TxIn
from btcpy.structs.sig import P2shSolver
from btcpy.setup import setup

import json

from .utils import fee_calculator
from .solver import ClaimSolver, FundSolver, RefundSolver
from .rpc import get_transaction_detail
from .htlc import HTLC
from .wallet import Wallet
from ...utils.exceptions import BalanceError


class Transaction:
    """
    Bitcoin Transaction class.

    :param version: Bitcoin transaction version, defaults to 2.
    :type version: int
    :param network: Bitcoin network, defaults to testnet.
    :type network: str
    :returns:  Transaction -- Bitcoin transaction instance.

    .. note::
        Bitcoin has only two networks, ``mainnet`` and ``testnet``.
    """

    # Initialization transaction
    def __init__(self, version=2, network="testnet"):
        # Transaction build version
        self.version, self.transaction = version, None
        # Bitcoin network
        self.mainnet, self.network = None, network
        if self.network == "mainnet":
            self.mainnet = True
        elif self.network == "testnet":
            self.mainnet = False
        else:
            raise ValueError("invalid network, please choose only mainnet or testnet")
        # Bitcoin fee and type
        self._fee, self._type = 0, None
        # Setting network
        setup(network, strict=True)

    # Transaction fee
    def fee(self):
        """
        Get Bitcoin transaction fee.

        :returns: int -- Bitcoin transaction fee.

        >>> from shuttle.providers.bitcoin.transaction import ClaimTransaction
        >>> from shuttle.providers.bitcoin.wallet import Wallet
        >>> recipient_wallet = Wallet(network="testnet").from_passphrase("meherett")
        >>> claim_transaction = ClaimTransaction(network="testnet")
        >>> claim_transaction.build_transaction("1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", recipient_wallet, 10000)
        >>> claim_transaction.fee()
        576
        """

        return self._fee

    # Transaction hash
    def hash(self):
        """
        Get Bitcoin transaction hash.

        :returns: str -- Bitcoin transaction hash or transaction id.

        >>> from shuttle.providers.bitcoin.htlc import HTLC
        >>> from shuttle.providers.bitcoin.transaction import FundTransaction
        >>> from shuttle.providers.bitcoin.wallet import Wallet
        >>> htlc = HTLC(network="testnet").init("821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e0158", "muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB", "mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q", 1000)
        >>> sender_wallet = Wallet(network="testnet").from_passphrase("meherett")
        >>> fund_transaction = FundTransaction(network="testnet")
        >>> fund_transaction.build_transaction(sender_wallet, htlc, 10000)
        >>> fund_transaction.hash()
        "9cc0524fb8e7b2c5fecaee4eb91d43a3dc5cc18e9906abcb35a5732ff52efcc7"
        """

        # Checking transaction
        if self.transaction is None:
            raise ValueError("transaction script is none, build transaction first.")
        return self.transaction.txid

    # Transaction json format
    def json(self):
        """
        Get Bitcoin transaction json format.

        :returns: dict -- Bitcoin transaction json format.

        >>> from shuttle.providers.bitcoin.transaction import RefundTransaction
        >>> from shuttle.providers.bitcoin.wallet import Wallet
        >>> wallet = Wallet(network="testnet").from_passphrase("meherett")
        >>> refund_transaction = RefundTransaction(network="testnet")
        >>> refund_transaction.build_transaction("1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", wallet, 10000)
        >>> refund_transaction.json()
        {"hex": "02000000012c392217483906f902e73c4bc132864de58153772d79268960998162266634be0100000000ffffffff02e80300000000000017a914971894c58d85981c16c2059d422bcde0b156d04487a6290000000000001976a9146bce65e58a50b97989930e9a4ff1ac1a77515ef188ac00000000", "txid": "9cc0524fb8e7b2c5fecaee4eb91d43a3dc5cc18e9906abcb35a5732ff52efcc7", "hash": "9cc0524fb8e7b2c5fecaee4eb91d43a3dc5cc18e9906abcb35a5732ff52efcc7", "size": 117, "vsize": 117, "version": 2, "locktime": 0, "vin": [{"txid": "be346626628199608926792d775381e54d8632c14b3ce702f90639481722392c", "vout": 1, "scriptSig": {"asm": "", "hex": ""}, "sequence": "4294967295"}], "vout": [{"value": "0.00001000", "n": 0, "scriptPubKey": {"asm": "OP_HASH160 971894c58d85981c16c2059d422bcde0b156d044 OP_EQUAL", "hex": "a914971894c58d85981c16c2059d422bcde0b156d04487", "type": "p2sh", "address": "2N729UBGZB3xjsGFRgKivy4bSjkaJGMVSpB"}}, {"value": "0.00010662", "n": 1, "scriptPubKey": {"asm": "OP_DUP OP_HASH160 6bce65e58a50b97989930e9a4ff1ac1a77515ef1 OP_EQUALVERIFY OP_CHECKSIG", "hex": "76a9146bce65e58a50b97989930e9a4ff1ac1a77515ef188ac", "type": "p2pkh", "address": "mqLyrNDjpENRMZAoDpspH7kR9RtgvhWzYE"}}]}
        """

        # Checking transaction
        if self.transaction is None:
            raise ValueError("transaction script is none, build transaction first.")
        return self.transaction.to_json()

    # Transaction raw
    def raw(self):
        """
        Get Bitcoin transaction raw.

        :returns: str -- Bitcoin transaction raw.

        >>> from shuttle.providers.bitcoin.transaction import ClaimTransaction
        >>> from shuttle.providers.bitcoin.wallet import Wallet
        >>> recipient_wallet = Wallet(network="testnet").from_passphrase("meherett")
        >>> claim_transaction = ClaimTransaction(network="testnet")
        >>> claim_transaction.build_transaction("1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", recipient_wallet, 10000)
        >>> claim_transaction.raw()
        "02000000012c392217483906f902e73c4bc132864de58153772d79268960998162266634be0100000000ffffffff02e80300000000000017a914971894c58d85981c16c2059d422bcde0b156d04487a6290000000000001976a9146bce65e58a50b97989930e9a4ff1ac1a77515ef188ac00000000"
        """

        # Checking transaction
        if self.transaction is None:
            raise ValueError("transaction script is none, build transaction first.")
        return self.transaction.hexlify()

    def type(self):
        """
        Get Bitcoin signature transaction type.

        :returns: str -- Bitcoin signature transaction type.

        >>> from shuttle.providers.bitcoin.transaction import ClaimTransaction
        >>> from shuttle.providers.bitcoin.wallet import Wallet
        >>> recipient_wallet = Wallet(network="testnet").from_passphrase("meherett")
        >>> claim_transaction = ClaimTransaction(network="testnet")
        >>> claim_transaction.build_transaction("1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", recipient_wallet, 10000)
        >>> claim_transaction.type()
        "bitcoin_claim_unsigned"
        """

        # Checking transaction
        if self.transaction is None:
            raise ValueError("transaction script is none, build transaction first.")
        return self._type

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

    :param version: Bitcoin transaction version, defaults to 2.
    :type version: int
    :param network: Bitcoin network, defaults to testnet.
    :type network: str
    :returns: FundTransaction -- Bitcoin fund transaction instance.

    .. warning::
        Do not forget to build transaction after initialize fund transaction.
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
        Build Bitcoin fund transaction.

        :param wallet: Bitcoin sender wallet.
        :type wallet: bitcoin.wallet.Wallet
        :param htlc: Bitcoin hash time lock contract (HTLC).
        :type htlc: bitcoin.htlc.HTLC
        :param amount: Bitcoin amount to fund.
        :type amount: int
        :param locktime: Bitcoin transaction lock time, defaults to 0.
        :type locktime: int
        :returns: FundTransaction -- Bitcoin fund transaction instance.

        >>> from shuttle.providers.bitcoin.htlc import HTLC
        >>> from shuttle.providers.bitcoin.transaction import FundTransaction
        >>> from shuttle.providers.bitcoin.wallet import Wallet
        >>> htlc = HTLC(network="testnet").init("821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e0158", "muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB", "mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q", 1000)
        >>> sender_wallet = Wallet(network="testnet").from_passphrase("meherett")
        >>> fund_transaction = FundTransaction(network="testnet")
        >>> fund_transaction.build_transaction(wallet=sender_wallet, htlc=htlc, amount=10000)
        <shuttle.providers.bitcoin.transaction.FundTransaction object at 0x0409DAF0>
        """

        # Checking parameter instances
        if not isinstance(wallet, Wallet):
            raise TypeError("invalid wallet instance, only takes Bitcoin Wallet class")
        if not isinstance(htlc, HTLC):
            raise TypeError("invalid htlc instance, only takes Bitcoin HTLC class")
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
        inputs, amount = self.inputs(
            utxos=self.unspent,
            previous_transaction_indexes=self.previous_transaction_indexes
        )

        # Calculating Bitcoin fee
        self._fee = fee_calculator(len(inputs), 2)
        if amount < (self.amount + self._fee):
            raise BalanceError("insufficient spend utxos")

        # Building mutable Bitcoin transaction
        self.transaction = MutableTransaction(
            version=self.version,
            ins=inputs,
            outs=[
                # Funding into hash time lock contract script hash
                TxOut(
                    value=self.amount,
                    n=0,
                    script_pubkey=P2shScript.unhexlify(
                        hex_string=self.htlc.hash()
                    )
                ),
                # Controlling amounts when we are funding on htlc script
                TxOut(
                    value=(amount - (self._fee + self.amount)),
                    n=1,
                    script_pubkey=P2pkhScript.unhexlify(
                        hex_string=self.wallet.p2pkh()
                    )
                )
            ], locktime=Locktime(locktime))
        self._type = "bitcoin_fund_unsigned"
        return self

    # Signing fund transaction
    def sign(self, solver):
        """
        Sign Bitcoin fund transaction.

        :param solver: Bitcoin fund solver.
        :type solver: bitcoin.solver.FundSolver
        :returns: FundTransaction -- Bitcoin fund transaction instance.

        >>> from shuttle.providers.bitcoin.htlc import HTLC
        >>> from shuttle.providers.bitcoin.transaction import FundTransaction
        >>> from shuttle.providers.bitcoin.solver import FundSolver
        >>> from shuttle.providers.bitcoin.wallet import Wallet
        >>> htlc = HTLC(network="testnet").init("821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e0158", "muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB", "mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q", 1000)
        >>> sender_wallet = Wallet(network="testnet").from_passphrase("meherett")
        >>> fund_solver = FundSolver("92cbbc5990cb5090326a76feeb321cad01048635afe5756523bbf9f7a75bf38b")
        >>> fund_transaction = FundTransaction(network="testnet")
        >>> fund_transaction.build_transaction(sender_wallet, htlc, 10000)
        >>> fund_transaction.sign(solver=fund_solver)
        <shuttle.providers.bitcoin.transaction.FundTransaction object at 0x0409DAF0>
        """

        # Checking parameter instances
        if not isinstance(solver, FundSolver):
            raise TypeError("invalid solver instance, only takes Bitcoin FundSolver class")
        if not self.unspent or not self.previous_transaction_indexes or not self.transaction:
            raise ValueError("transaction script or unspent is none, build transaction first")

        # Organizing outputs
        outputs = self.outputs(self.unspent, self.previous_transaction_indexes)
        # Signing fund transaction
        self.transaction.spend(outputs, [solver.solve() for _ in outputs])
        self._type = "bitcoin_fund_signed"
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
        Get Bitcoin unsigned fund transaction raw.

        :returns: str -- Bitcoin unsigned fund transaction raw.

        >>> from shuttle.providers.bitcoin.htlc import HTLC
        >>> from shuttle.providers.bitcoin.transaction import FundTransaction
        >>> from shuttle.providers.bitcoin.wallet import Wallet
        >>> htlc = HTLC(network="testnet").init("821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e0158", "muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB", "mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q", 1000)
        >>> sender_wallet = Wallet(network="testnet").from_passphrase("meherett")
        >>> fund_transaction = FundTransaction(network="testnet")
        >>> fund_transaction.build_transaction(sender_wallet, htlc, 10000)
        >>> fund_transaction.unsigned_raw()
        "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTJjMzkyMjE3NDgzOTA2ZjkwMmU3M2M0YmMxMzI4NjRkZTU4MTUzNzcyZDc5MjY4OTYwOTk4MTYyMjY2NjM0YmUwMTAwMDAwMDAwZmZmZmZmZmYwMmU4MDMwMDAwMDAwMDAwMDAxN2E5MTQ5NzE4OTRjNThkODU5ODFjMTZjMjA1OWQ0MjJiY2RlMGIxNTZkMDQ0ODdhNjI5MDAwMDAwMDAwMDAwMTk3NmE5MTQ2YmNlNjVlNThhNTBiOTc5ODk5MzBlOWE0ZmYxYWMxYTc3NTE1ZWYxODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiAxMjM0MCwgIm4iOiAxLCAic2NyaXB0IjogIjc2YTkxNDZiY2U2NWU1OGE1MGI5Nzk4OTkzMGU5YTRmZjFhYzFhNzc1MTVlZjE4OGFjIn1dLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfdW5zaWduZWQifQ"
        """

        # Checking transaction and UTXO
        if not self.transaction or not self.unspent:
            raise ValueError("transaction script or unspent is none, build transaction first")

        outputs = []
        for index, utxo in enumerate(self.unspent):
            if self.previous_transaction_indexes is None or \
                    index in self.previous_transaction_indexes:
                outputs.append(
                    dict(
                        amount=utxo["amount"],
                        n=utxo["output_index"],
                        script=utxo["script"]
                    )
                )

        # Encoding fund transaction raw
        return b64encode(str(json.dumps(dict(
            fee=self._fee,
            raw=self.transaction.hexlify(),
            outputs=outputs,
            network=self.network,
            type="bitcoin_fund_unsigned"
        ))).encode()).decode()


class ClaimTransaction(Transaction):
    """
    Bitcoin ClaimTransaction class.

    :param version: Bitcoin transaction version, defaults to 2.
    :type version: int
    :param network: Bitcoin network, defaults to testnet.
    :type network: str
    :returns:  Transaction -- Bitcoin transaction instance.

    .. warning::
        Do not forget to build transaction after initialize claim transaction.
    """

    # Initialization claim transaction
    def __init__(self, network="testnet", version=2):
        super().__init__(network=network, version=version)
        # Initialization transaction_id, recipient wallet and amount
        self.transaction_id, self.wallet, \
            self.amount = None, None, None
        # Getting transaction detail by id
        self.transaction_detail = None
        # Transaction detail outputs (HTLC and Sender account)
        self.htlc_detail, self.sender_detail = None, None

    # Building claim transaction
    def build_transaction(self, transaction_id, wallet, amount, locktime=0):
        """
        Build Bitcoin claim transaction.

        :param transaction_id: Bitcoin fund transaction id to redeem.
        :type transaction_id: str
        :param wallet: Bitcoin recipient wallet.
        :type wallet: bitcoin.wallet.Wallet
        :param amount: Bitcoin amount to withdraw.
        :type amount: int
        :param locktime: Bitcoin transaction lock time, defaults to 0.
        :type locktime: int
        :returns: ClaimTransaction -- Bitcoin claim transaction instance.

        >>> from shuttle.providers.bitcoin.transaction import ClaimTransaction
        >>> from shuttle.providers.bitcoin.wallet import Wallet
        >>> recipient_wallet = Wallet(network="testnet").from_passphrase("meherett")
        >>> claim_transaction = ClaimTransaction(network="testnet")
        >>> claim_transaction.build_transaction(transaction_id="1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", wallet=recipient_wallet, amount=10000)
        <shuttle.providers.bitcoin.transaction.ClaimTransaction object at 0x0409DAF0>
        """

        # Checking parameter instances
        if not isinstance(transaction_id, str):
            raise TypeError("invalid amount instance, only takes string type")
        if not isinstance(wallet, Wallet):
            raise TypeError("invalid wallet instance, only takes Bitcoin Wallet class")

        # Setting transaction_id and wallet
        self.transaction_id, self.wallet = transaction_id, wallet
        # Getting transaction detail by id
        self.transaction_detail = get_transaction_detail(self.transaction_id)
        # Getting Hash time lock contract output detail
        self.htlc_detail = self.transaction_detail["outputs"][0]
        # Getting HTLC funded amount balance
        htlc_amount = self.htlc_detail["value"]

        # Calculating fee
        self._fee = fee_calculator(1, 1)
        if amount < self._fee:
            raise BalanceError("insufficient spend utxos")
        elif not htlc_amount >= (amount - self._fee):
            raise BalanceError("insufficient spend utxos", f"maximum you can withdraw {htlc_amount}")

        # Building Bitcoin mutable transaction
        self.transaction = MutableTransaction(
            version=self.version,
            ins=[
                TxIn(
                    txid=self.transaction_id,
                    txout=0,
                    script_sig=ScriptSig.empty(),
                    sequence=Sequence.max()
                )
            ],
            outs=[
                TxOut(
                    value=(amount - self._fee),
                    n=0,
                    script_pubkey=P2pkhScript.unhexlify(
                        hex_string=self.wallet.p2pkh()
                    )
                )
            ], locktime=Locktime(locktime))
        self._type = "bitcoin_claim_unsigned"
        return self

    # Signing claim transaction
    def sign(self, solver):
        """
        Sign Bitcoin claim transaction.

        :param solver: Bitcoin claim solver.
        :type solver: bitcoin.solver.ClaimSolver
        :returns: ClaimTransaction -- Bitcoin claim transaction instance.

        >>> from shuttle.providers.bitcoin.transaction import ClaimTransaction
        >>> from shuttle.providers.bitcoin.solver import ClaimSolver
        >>> from shuttle.providers.bitcoin.wallet import Wallet
        >>> recipient_wallet = Wallet(network="testnet").from_passphrase("meherett")
        >>> claim_solver = ClaimSolver(recipient_wallet.private_key(), "Hello Meheret!", "3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb", recipient_wallet.address(), "mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q", 1000)
        >>> claim_transaction = ClaimTransaction(network="testnet")
        >>> claim_transaction.build_transaction("1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", recipient_wallet, 10000)
        >>> claim_transaction.sign(solver=claim_solver)
        <shuttle.providers.bitcoin.transaction.ClaimTransaction object at 0x0409DAF0>
        """

        # Checking parameter instances
        if not isinstance(solver, ClaimSolver):
            raise TypeError("invalid solver instance, only takes Bitcoin ClaimSolver class")
        if self.transaction is None:
            raise ValueError("transaction script is none, build transaction first")

        self.transaction.spend([
            TxOut(
                value=self.htlc_detail["value"],
                n=0,
                script_pubkey=P2shScript.unhexlify(
                    hex_string=self.htlc_detail["script"]
                )
            )
        ], [
            P2shSolver(
                redeem_script=solver.witness(
                    network=self.network
                ),
                redeem_script_solver=solver.solve()
            )
        ])
        self._type = "bitcoin_claim_signed"
        return self

    def unsigned_raw(self):
        """
        Get Bitcoin unsigned claim transaction raw.

        :returns: str -- Bitcoin unsigned claim transaction raw.

        >>> from shuttle.providers.bitcoin.transaction import ClaimTransaction
        >>> from shuttle.providers.bitcoin.wallet import Wallet
        >>> recipient_wallet = Wallet(network="testnet").from_passphrase("meherett")
        >>> claim_transaction = ClaimTransaction(network="testnet")
        >>> claim_transaction.build_transaction("1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", recipient_wallet, 10000)
        >>> claim_transaction.unsigned_raw()
        "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTJjMzkyMjE3NDgzOTA2ZjkwMmU3M2M0YmMxMzI4NjRkZTU4MTUzNzcyZDc5MjY4OTYwOTk4MTYyMjY2NjM0YmUwMTAwMDAwMDAwZmZmZmZmZmYwMmU4MDMwMDAwMDAwMDAwMDAxN2E5MTQ5NzE4OTRjNThkODU5ODFjMTZjMjA1OWQ0MjJiY2RlMGIxNTZkMDQ0ODdhNjI5MDAwMDAwMDAwMDAwMTk3NmE5MTQ2YmNlNjVlNThhNTBiOTc5ODk5MzBlOWE0ZmYxYWMxYTc3NTE1ZWYxODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiAxMjM0MCwgIm4iOiAxLCAic2NyaXB0IjogIjc2YTkxNDZiY2U2NWU1OGE1MGI5Nzk4OTkzMGU5YTRmZjFhYzFhNzc1MTVlZjE4OGFjIn1dLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfdW5zaWduZWQifQ"
        """

        # Checking transaction
        if self.transaction is None:
            raise ValueError("transaction script is none, build transaction first")

        # Encoding claim transaction raw
        return b64encode(str(json.dumps(dict(
            fee=self._fee,
            raw=self.transaction.hexlify(),
            outputs=dict(
                amount=self.htlc_detail["value"],
                n=0,
                script=self.htlc_detail["script"]
            ),
            network=self.network,
            type="bitcoin_claim_unsigned"
        ))).encode()).decode()


class RefundTransaction(Transaction):
    """
    Bitcoin RefundTransaction class.

    :param version: Bitcoin transaction version, defaults to 2.
    :type version: int
    :param network: Bitcoin network, defaults to testnet.
    :type network: str
    :returns:  Transaction -- Bitcoin transaction instance.

    .. warning::
        Do not forget to build transaction after initialize refund transaction.
    """

    # Initialization claim transaction
    def __init__(self, version=2, network="testnet"):
        super().__init__(version=version, network=network)
        # Initialization transaction_id, sender wallet and amount
        self.transaction_id, self.wallet, \
            self.amount = None, None, None
        # Get transaction detail
        self.transaction_detail = None
        # Transaction detail outputs (HTLC and Sender account)
        self.htlc_detail, self.sender_detail = None, None

    # Building transaction
    def build_transaction(self, transaction_id, wallet, amount, locktime=0):
        """
        Build Bitcoin refund transaction.

        :param transaction_id: Bitcoin fund transaction id to redeem.
        :type transaction_id: str
        :param wallet: Bitcoin sender wallet.
        :type wallet: bitcoin.wallet.Wallet
        :param amount: Bitcoin amount to withdraw.
        :type amount: int
        :param locktime: Bitcoin transaction lock time, defaults to 0.
        :type locktime: int
        :returns: RefundTransaction -- Bitcoin refund transaction instance.

        >>> from shuttle.providers.bitcoin.transaction import RefundTransaction
        >>> from shuttle.providers.bitcoin.wallet import Wallet
        >>> sender_wallet = Wallet(network="testnet").from_passphrase("meherett")
        >>> refund_transaction = RefundTransaction(network="testnet")
        >>> refund_transaction.build_transaction(transaction_id="1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", wallet=sender_wallet, amount=10000)
        <shuttle.providers.bitcoin.transaction.RefundTransaction object at 0x0409DAF0>
        """

        # Checking parameter instances
        if not isinstance(transaction_id, str):
            raise TypeError("invalid amount instance, only takes string type")
        if not isinstance(wallet, Wallet):
            raise TypeError("invalid wallet instance, only takes Bitcoin Wallet class")

        # Setting transaction_id and wallet
        self.transaction_id, self.wallet = transaction_id, wallet
        # Getting transaction detail by id
        self.transaction_detail = get_transaction_detail(self.transaction_id)
        # Getting Hash time lock contract output detail
        self.htlc_detail = self.transaction_detail["outputs"][0]
        # Getting HTLC funded amount balance
        htlc_amount = self.htlc_detail["value"]

        # Calculating fee
        self._fee = fee_calculator(1, 1)
        if amount < self._fee:
            raise BalanceError("insufficient spend utxos")
        elif not htlc_amount >= (amount - self._fee):
            raise BalanceError("insufficient spend utxos", f"maximum you can withdraw {htlc_amount}")

        # Building mutable Bitcoin transaction
        self.transaction = MutableTransaction(
            version=self.version,
            ins=[
                TxIn(
                    txid=self.transaction_id,
                    txout=0,
                    script_sig=ScriptSig.empty(),
                    sequence=Sequence.max()
                )
            ],
            outs=[
                TxOut(
                    value=(amount - self._fee),
                    n=0,
                    script_pubkey=P2pkhScript.unhexlify(
                        hex_string=self.wallet.p2pkh()
                    )
                )
            ], locktime=Locktime(locktime))
        self._type = "bitcoin_refund_unsigned"
        return self

    # Signing refund transaction
    def sign(self, solver):
        """
        Sign Bitcoin refund transaction.

        :param solver: Bitcoin refund solver.
        :type solver: bitcoin.solver.RefundSolver
        :returns: RefundTransaction -- Bitcoin refund transaction instance.

        >>> from shuttle.providers.bitcoin.transaction import RefundTransaction
        >>> from shuttle.providers.bitcoin.solver import RefundSolver
        >>> from shuttle.providers.bitcoin.wallet import Wallet
        >>> sender_wallet = Wallet(network="testnet").from_passphrase("meherett1234")
        >>> refund_solver = RefundSolver(sender_wallet.private_key(), "3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb",  "muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB", sender_wallet.address(), 1000)
        >>> refund_transaction = RefundTransaction(network="testnet")
        >>> refund_transaction.build_transaction("1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", sender_wallet, 10000)
        >>> refund_transaction.sign(solver=refund_solver)
        <shuttle.providers.bitcoin.transaction.RefundTransaction object at 0x0409DAF0>
        """

        # Checking parameter instances
        if not isinstance(solver, RefundSolver):
            raise TypeError("invalid solver instance, only takes Bitcoin RefundSolver class")
        if self.transaction is None:
            raise ValueError("transaction script is none, build transaction first")

        self.transaction.spend([
            TxOut(
                value=self.htlc_detail["value"],
                n=0,
                script_pubkey=P2shScript.unhexlify(
                    hex_string=self.htlc_detail["script"]
                )
            )
        ], [
            P2shSolver(
                redeem_script=solver.witness(
                    network=self.network
                ),
                redeem_script_solver=solver.solve()
            )
        ])
        self._type = "bitcoin_refund_signed"
        return self

    def unsigned_raw(self):
        """
        Get Bitcoin unsigned refund transaction raw.

        :returns: str -- Bitcoin unsigned refund transaction raw.

        >>> from shuttle.providers.bitcoin.transaction import RefundTransaction
        >>> from shuttle.providers.bitcoin.wallet import Wallet
        >>> sender_wallet = Wallet(network="testnet").from_passphrase("meherett1234")
        >>> refund_transaction = RefundTransaction(network="testnet")
        >>> refund_transaction.build_transaction("1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", sender_wallet, 10000)
        >>> refund_transaction.unsigned_raw()
        "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTJjMzkyMjE3NDgzOTA2ZjkwMmU3M2M0YmMxMzI4NjRkZTU4MTUzNzcyZDc5MjY4OTYwOTk4MTYyMjY2NjM0YmUwMTAwMDAwMDAwZmZmZmZmZmYwMmU4MDMwMDAwMDAwMDAwMDAxN2E5MTQ5NzE4OTRjNThkODU5ODFjMTZjMjA1OWQ0MjJiY2RlMGIxNTZkMDQ0ODdhNjI5MDAwMDAwMDAwMDAwMTk3NmE5MTQ2YmNlNjVlNThhNTBiOTc5ODk5MzBlOWE0ZmYxYWMxYTc3NTE1ZWYxODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiAxMjM0MCwgIm4iOiAxLCAic2NyaXB0IjogIjc2YTkxNDZiY2U2NWU1OGE1MGI5Nzk4OTkzMGU5YTRmZjFhYzFhNzc1MTVlZjE4OGFjIn1dLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfdW5zaWduZWQifQ"
        """

        # Checking transaction
        if self.transaction is None:
            raise ValueError("transaction script is none, build transaction first")

        # Encoding refund transaction raw
        return b64encode(str(json.dumps(dict(
            fee=self._fee,
            raw=self.transaction.hexlify(),
            outputs=dict(
                value=self.htlc_detail["value"],
                n=0,
                script_pubkey=self.htlc_detail["script"]
            ),
            network=self.network,
            type="bitcoin_refund_unsigned"
        ))).encode()).decode()
