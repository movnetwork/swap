#!/usr/bin/env python3

from btmhdw import BytomHDWallet, sign
from base64 import b64encode, b64decode

import json

from .rpc import build_transaction, decode_tx_raw
from .utils import spend_wallet_action, control_program_action, \
    find_contract_utxo_id, spend_utxo_action, control_address_action
from .solver import FundSolver, ClaimSolver, RefundSolver
from .htlc import HTLC
from .wallet import Wallet
from ..config import bytom

# Bytom configuration
bytom = bytom()


class Transaction:
    """
    Bytom Transaction class.

    :param network: bytom network, defaults to testnet.
    :type network: str
    :param guid: bytom blockcenter guid, defaults to None.
    :type guid: str
    :param inputs: bytom transaction inputs, defaults to None.
    :type inputs: list
    :param outputs: bytom transaction outputs, defaults to None.
    :type outputs: list
    :param tx: bytom transaction, defaults to None.
    :type tx: dict
    :returns:  Transaction -- bytom transaction instance.

    .. note::
        Bytom has only three networks, ``mainnet``. ``solonet`` and ``testnet``.
    """

    # Initialization transaction
    def __init__(self, network="testnet",
                 guid=None, inputs=None, outputs=None, tx=None):
        # Transaction
        self.transaction = tx
        # Bytom network
        self.network = network
        # Input and Output actions
        self.inputs, self.outputs = inputs, outputs
        # Blockcenter GUID
        self.guid = guid
        # Bytom fee
        self.fee = bytom["fee"]
        # Signed datas
        self.signatures = list()

    # Building bytom transaction
    def build_transaction(self, *args, **kwargs):

        if not self.guid and not self.inputs or not self.outputs:
            raise ValueError("transaction fail | GUID, Inputs or Outputs are none.")

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
        """
        Get bytom transaction hash.

        :returns: str -- bytom transaction hash or transaction id.

        >>> transaction.hash()
        "2993414225f65390220730d0c1a356c14e91bca76db112d37366df93e364a492"
        """

        if self.transaction is None:
            raise ValueError("transaction is none, build transaction first.")
        return self.transaction["tx"]["hash"]

    # Transaction json
    def json(self):
        """
        Get bytom transaction json format.

        :returns: dict -- bytom transaction json format.

        >>> transaction.json()
        {"hash": "2993414225f65390220730d0c1a356c14e91bca76db112d37366df93e364a492", "status_fail": false, "size": 379, "submission_timestamp": 0, "memo": "", "inputs": [{"script": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 2450000000, "type": "spend"}], "outputs": [{"utxo_id": "5edccebe497893c289121f9e365fdeb34c97008b9eb5a9960fe9541e7923aabc", "script": "01642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0", "address": "smart contract", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 1000, "type": "control"}, {"utxo_id": "f8cfbb692db1963be88b09c314adcc9e19d91c6c019aa556fb7cb76ba8ffa1fa", "script": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 2439999000, "type": "control"}], "fee": 10000000, "balances": [{"asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": "-10001000"}], "types": ["ordinary"]}
        """
        if self.transaction is None:
            raise ValueError("transaction is none, build transaction first.")
        return decode_tx_raw(tx_raw=self.transaction["raw_transaction"])

    # Transaction raw
    def raw(self):
        """
        Get bytom transaction raw.

        :returns: str -- bytom transaction raw.

        >>> transaction.raw()
        "070100010160015e7f2d7ecec3f61d30d0b2968973a3ac8448f0599ea20dce883b48c903c4d6e87fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8091a0900901011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a22012091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e20201ad01ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe80701880101642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c000013dffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff98dcbd8b09011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a00"
        """

        if self.transaction is None:
            raise ValueError("transaction is none, build transaction first.")
        return self.transaction["raw_transaction"]

    def unsigned(self, detail=False):
        unsigned_datas = list()
        if self.transaction is None:
            raise ValueError("transaction is none, build transaction first.")
        bytom_hd_wallet = BytomHDWallet()
        for signing_instruction in self.transaction["signing_instructions"]:
            unsigned_data = dict(datas=signing_instruction["sign_data"])
            if "pubkey" in signing_instruction and signing_instruction["pubkey"]:
                unsigned_data.setdefault("public_key", signing_instruction["pubkey"])
                if detail:
                    program = bytom_hd_wallet.program(public=signing_instruction["pubkey"])
                    address = bytom_hd_wallet.address(program=program, network=self.network)
                    unsigned_data.setdefault("program", program)
                    unsigned_data.setdefault("address", address)
                else:
                    unsigned_data.setdefault("network", self.network)
            else:
                if detail:
                    unsigned_data.setdefault("public_key", None)
                    unsigned_data.setdefault("program", None)
                    unsigned_data.setdefault("address", None)
                else:
                    unsigned_data.setdefault("network", self.network)
            if "derivation_path" in signing_instruction and signing_instruction["derivation_path"]:
                path = bytom_hd_wallet.get_path(indexes=signing_instruction["derivation_path"])
                if detail:
                    unsigned_data.setdefault("indexes", signing_instruction["derivation_path"])
                unsigned_data.setdefault("path", path)
            else:
                if detail:
                    unsigned_data.setdefault("indexes", None)
                unsigned_data.setdefault("path", None)
            # Append unsigned datas
            unsigned_datas.append(unsigned_data)
        # Returning
        return unsigned_datas

    # # Signing message
    # def sign(self, xprivate_key):
    #     for unsigned in self.unsigned():
    #         signed_data = list()
    #         unsigned_datas = unsigned["datas"]
    #         for unsigned_data in unsigned_datas:
    #             signed_data.append(
    #                 sign(xprivate=xprivate_key,
    #                      message=unsigned_data))
    #         self.signatures.append(signed_data)
    #     return self


class FundTransaction(Transaction):
    """
    Bytom FundTransaction class.

    :param network: bytom network, defaults to testnet.
    :type network: str
    :returns: FundTransaction -- bytom fund transaction instance.

    .. warning::
        Do not forget to build transaction after initialize fund transaction.

    :fee: Get bytom fund transaction fee.

    >>> fund_transaction.fee
    10000000

    :signatures: Get bytom fund transaction signature data.

    >>> fund_transaction.signatures
    [...]
    """

    # Initialization fund transaction
    def __init__(self, network="testnet"):
        super().__init__(network)

    def build_transaction(self, wallet, htlc, amount, asset=bytom["BTM_asset"]):
        """
        Build bytom fund transaction.

        :param wallet: bytom sender wallet.
        :type wallet: bytom.wallet.Wallet
        :param htlc: bytom hash time lock contract (HTLC).
        :type htlc: bytom.htlc.HTLC
        :param amount: bytom amount to fund.
        :type amount: int
        :param asset: bytom asset id, defaults to BTM asset.
        :type asset: str
        :returns: FundTransaction -- bytom fund transaction instance.

        >>> from shuttle.providers.bytom.transaction import FundTransaction
        >>> fund_transaction = FundTransaction(network="testnet")
        >>> fund_transaction.build_transaction(sender_wallet, htlc, 10000)
        <shuttle.providers.bytom.transaction.FundTransaction object at 0x0409DAF0>
        """

        # Checking build transaction arguments instance
        if not isinstance(wallet, Wallet):
            raise TypeError("invalid wallet instance, only takes bytom Wallet class")
        if not isinstance(htlc, HTLC):
            raise TypeError("invalid htlc instance, only takes bytom HTLC class")
        if not isinstance(amount, int):
            raise TypeError("invalid amount instance, only takes integer type")
        if not isinstance(asset, str):
            raise TypeError("invalid asset instance, only takes string type")
        # Setting wallet GUID
        self.guid = wallet.guid()
        # Actions
        inputs, outputs = list(), list()
        # Input action
        inputs.append(
            spend_wallet_action(
                asset=asset,
                amount=amount
            )
        )
        # Output action
        outputs.append(
            control_program_action(
                asset=asset,
                amount=amount,
                control_program=htlc.bytecode()
            )
        )
        # Transaction
        tx = dict(
            guid=self.guid,
            inputs=inputs,
            outputs=outputs,
            fee=bytom["fee"],
            confirmations=bytom["confirmations"]
        )
        # Building transaction
        self.transaction = build_transaction(tx=tx, network=self.network)
        return self

    # Signing transaction using xprivate keys
    def sign(self, solver):
        """
        Sign bytom fund transaction.

        :param solver: bytom fund solver.
        :type solver: bytom.solver.FundSolver
        :returns: FundTransaction -- bytom fund transaction instance.

        >>> from shuttle.providers.bytom.transaction import FundTransaction
        >>> fund_transaction = FundTransaction(network="testnet")
        >>> fund_transaction.build_transaction(sender_wallet, htlc, 10000)
        >>> fund_transaction.sign(fund_solver)
        <shuttle.providers.bytom.transaction.FundTransaction object at 0x0409DAF0>
        """

        if not isinstance(solver, FundSolver):
            raise TypeError("Solver must be FundSolver format.")
        wallet = solver.solve()
        wallet.indexes = list()
        for unsigned in self.unsigned(detail=True):
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
            wallet.indexes = list()
        return self

    def unsigned_raw(self):
        """
        Get bytom unsigned fund transaction raw.

        :returns: str -- bytom unsigned fund transaction raw.

        >>> from shuttle.providers.bytom.transaction import FundTransaction
        >>> fund_transaction = FundTransaction(network="testnet")
        >>> fund_transaction.build_transaction(sender_wallet, htlc, 10000)
        >>> fund_transaction.unsigned_raw()
        "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTJjMzkyMjE3NDgzOTA2ZjkwMmU3M2M0YmMxMzI4NjRkZTU4MTUzNzcyZDc5MjY4OTYwOTk4MTYyMjY2NjM0YmUwMTAwMDAwMDAwZmZmZmZmZmYwMmU4MDMwMDAwMDAwMDAwMDAxN2E5MTQ5NzE4OTRjNThkODU5ODFjMTZjMjA1OWQ0MjJiY2RlMGIxNTZkMDQ0ODdhNjI5MDAwMDAwMDAwMDAwMTk3NmE5MTQ2YmNlNjVlNThhNTBiOTc5ODk5MzBlOWE0ZmYxYWMxYTc3NTE1ZWYxODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiAxMjM0MCwgIm4iOiAxLCAic2NyaXB0IjogIjc2YTkxNDZiY2U2NWU1OGE1MGI5Nzk4OTkzMGU5YTRmZjFhYzFhNzc1MTVlZjE4OGFjIn1dLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfdW5zaWduZWQifQ"
        """

        if not self.transaction:
            raise ValueError("transaction script is none, build transaction first")

        return b64encode(str(json.dumps(dict(
            fee=self.fee,
            guid=self.guid,
            unsigned=self.unsigned(detail=False),
            hash=self.transaction["tx"]["hash"],
            raw=self.transaction["raw_transaction"],
            signatures=list(),
            network=self.network,
            type="bytom_fund_unsigned"
        ))).encode()).decode()


class ClaimTransaction(Transaction):
    """
    Bytom ClaimTransaction class.

    :param network: bytom network, defaults to testnet.
    :type network: str
    :returns: ClaimTransaction -- bytom claim transaction instance.

    .. warning::
        Do not forget to build transaction after initialize claim transaction.

    :fee: Get bytom claim transaction fee.

    >>> claim_transaction.fee
    10000000

    :signatures: Get bytom fund transaction signature data.

    >>> claim_transaction.signatures
    [...]
    """

    # Initialization claim transaction
    def __init__(self, network="testnet"):
        super().__init__(network)

        # Init secret key
        self.secret = None

    def build_transaction(self, wallet, amount, asset=bytom["BTM_asset"],
                          transaction_id=None, utxo_id=None, secret=None):
        """
        Build bytom claim transaction.

        :param wallet: bytom recipient wallet.
        :type wallet: bytom.wallet.Wallet
        :param amount: bytom amount to withdraw.
        :type amount: int
        :param asset: bytom asset id, defaults to BTM asset.
        :type asset: str
        :param transaction_id: bytom fund transaction id to redeem, default to None.
        :type transaction_id: str
        :param utxo_id: bytom htlc utxo id, default to None..
        :type utxo_id: str
        :param secret: secret key.
        :type secret: str
        :returns: ClaimTransaction -- bytom claim transaction instance.

        >>> from shuttle.providers.bytom.transaction import ClaimTransaction
        >>> claim_transaction = ClaimTransaction(network="testnet")
        >>> claim_transaction.build_transaction(fund_transaction_id, recipient_wallet, 10000)
        <shuttle.providers.bytom.transaction.ClaimTransaction object at 0x0409DAF0>
        """

        # Checking transaction and utxo id
        if not transaction_id and not utxo_id:
            raise ValueError("transaction or utxo id are required")

        # Checking build transaction arguments instance
        if transaction_id and not isinstance(transaction_id, str):
            raise TypeError("invalid transaction id instance, only takes bytom string type")
        if utxo_id and not isinstance(utxo_id, str):
            raise TypeError("invalid utxo id instance, only takes bytom string type")
        if not isinstance(wallet, Wallet):
            raise TypeError("invalid wallet instance, only takes bytom Wallet class")
        if not isinstance(amount, int):
            raise TypeError("invalid asset instance, only takes integer type")
        if not isinstance(asset, str):
            raise TypeError("invalid amount instance, only takes string type")
        if secret is not None and not isinstance(secret, str):
            raise TypeError("invalid secret instance, only takes string type")

        if transaction_id:
            # Finding htlc utxo id.
            utxo_id = find_contract_utxo_id(
                tx_id=transaction_id, network=self.network)
            if utxo_id is None:
                raise ValueError("invalid transaction id, there is no smart contact")

        # Setting wallet GUID
        self.guid = wallet.guid()
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
                asset=asset,
                amount=amount,
                address=wallet.address()
            )
        )
        # Transaction
        tx = dict(
            guid=self.guid,
            inputs=inputs,
            outputs=outputs,
            fee=bytom["fee"],
            confirmations=bytom["confirmations"]
        )
        # Building transaction
        self.transaction = build_transaction(tx=tx, network=self.network)
        self.secret = secret
        return self

    # Signing transaction using private keys
    def sign(self, solver):
        """
        Sign bytom claim transaction.

        :param solver: bytom claim solver.
        :type solver: bytom.solver.ClaimSolver
        :returns: ClaimTransaction -- bytom claim transaction instance.

        >>> from shuttle.providers.bytom.transaction import ClaimTransaction
        >>> claim_transaction = ClaimTransaction(network="testnet")
        >>> claim_transaction.build_transaction(fund_transaction_id, recipient_wallet, 10000)
        >>> claim_transaction.sign(claim_solver)
        <shuttle.providers.bytom.transaction.ClaimTransaction object at 0x0409DAF0>
        """

        if not isinstance(solver, ClaimSolver):
            raise TypeError("solver must be ClaimSolver format.")
        wallet = solver.solve()
        wallet.indexes = list()
        for index, unsigned in enumerate(self.unsigned(detail=True)):
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
            wallet.indexes = list()
        return self

    def unsigned_raw(self):
        """
        Get bytom unsigned claim transaction raw.

        :returns: str -- bytom unsigned claim transaction raw.

        >>> from shuttle.providers.bytom.transaction import ClaimTransaction
        >>> claim_transaction = ClaimTransaction(network="testnet")
        >>> claim_transaction.build_transaction(fund_transaction_id, recipient_wallet, 10000)
        >>> claim_transaction.unsigned_raw()
        "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTJjMzkyMjE3NDgzOTA2ZjkwMmU3M2M0YmMxMzI4NjRkZTU4MTUzNzcyZDc5MjY4OTYwOTk4MTYyMjY2NjM0YmUwMTAwMDAwMDAwZmZmZmZmZmYwMmU4MDMwMDAwMDAwMDAwMDAxN2E5MTQ5NzE4OTRjNThkODU5ODFjMTZjMjA1OWQ0MjJiY2RlMGIxNTZkMDQ0ODdhNjI5MDAwMDAwMDAwMDAwMTk3NmE5MTQ2YmNlNjVlNThhNTBiOTc5ODk5MzBlOWE0ZmYxYWMxYTc3NTE1ZWYxODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiAxMjM0MCwgIm4iOiAxLCAic2NyaXB0IjogIjc2YTkxNDZiY2U2NWU1OGE1MGI5Nzk4OTkzMGU5YTRmZjFhYzFhNzc1MTVlZjE4OGFjIn1dLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfdW5zaWduZWQifQ"
        """

        if not self.transaction:
            raise ValueError("transaction script is none, build transaction first")

        return b64encode(str(json.dumps(dict(
            fee=self.fee,
            guid=self.guid,
            unsigned=self.unsigned(detail=False),
            hash=self.transaction["tx"]["hash"],
            raw=self.transaction["raw_transaction"],
            secret=self.secret,
            network=self.network,
            signatures=list(),
            type="bytom_claim_unsigned"
        ))).encode()).decode()


class RefundTransaction(Transaction):
    """
    Bytom RefundTransaction class.

    :param network: bytom network, defaults to testnet.
    :type network: str
    :returns: RefundTransaction -- bytom refund transaction instance.

    .. warning::
        Do not forget to build transaction after initialize refund transaction.

    :fee: Get bytom refund transaction fee.

    >>> refund_transaction.fee
    10000000

    :signatures: Get bytom refund transaction signature data.

    >>> refund_transaction.signatures
    [...]
    """

    # Initialization fund transaction
    def __init__(self, network="testnet"):
        super().__init__(network)

    def build_transaction(self, wallet, amount, asset=bytom["BTM_asset"],
                          transaction_id=None, utxo_id=None):
        """
        Build bytom refund transaction.

        :param wallet: bytom sender wallet.
        :type wallet: bytom.wallet.Wallet
        :param amount: bytom amount to withdraw.
        :type amount: int
        :param asset: bytom asset id, defaults to BTM asset.
        :type asset: str
        :param transaction_id: bytom fund transaction id to redeem, defaults to None.
        :type transaction_id: str
        :param utxo_id: bytom htlc utxo id, default to None..
        :type utxo_id: str
        :returns: RefundTransaction -- bytom refund transaction instance.

        >>> from shuttle.providers.bytom.transaction import RefundTransaction
        >>> refund_transaction = RefundTransaction(network="testnet")
        >>> refund_transaction.build_transaction(fund_transaction_id, sender_wallet, 10000)
        <shuttle.providers.bytom.transaction.RefundTransaction object at 0x0409DAF0>
        """

        # Checking transaction and utxo id
        if not transaction_id and not utxo_id:
            raise ValueError("transaction or utxo id are required")

        # Checking build transaction arguments instance
        if transaction_id and not isinstance(transaction_id, str):
            raise TypeError("invalid transaction id instance, only takes bytom string type")
        if utxo_id and not isinstance(utxo_id, str):
            raise TypeError("invalid utxo id instance, only takes bytom string type")
        if not isinstance(wallet, Wallet):
            raise TypeError("invalid wallet instance, only takes bytom Wallet class")
        if not isinstance(amount, int):
            raise TypeError("invalid asset instance, only takes integer type")
        if not isinstance(asset, str):
            raise TypeError("invalid amount instance, only takes string type")

        if transaction_id:
            # Finding htlc utxo id.
            utxo_id = find_contract_utxo_id(
                tx_id=transaction_id, network=self.network)
            if utxo_id is None:
                raise ValueError("invalid transaction id, there is no smart contact")

        # Setting wallet GUID
        self.guid = wallet.guid()
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
                asset=asset,
                amount=amount,
                address=wallet.address()
            )
        )
        # Transaction
        tx = dict(
            guid=self.guid,
            inputs=inputs,
            outputs=outputs,
            fee=bytom["fee"],
            confirmations=bytom["confirmations"]
        )
        # Building transaction
        self.transaction = build_transaction(tx=tx, network=self.network)
        return self

    # Signing transaction using private keys
    def sign(self, solver):
        """
        Sign bytom refund transaction.

        :param solver: bytom refund solver.
        :type solver: bytom.solver.RefundSolver
        :returns: RefundTransaction -- bytom refund transaction instance.

        >>> from shuttle.providers.bytom.transaction import RefundTransaction
        >>> refund_transaction = RefundTransaction(network="testnet")
        >>> refund_transaction.build_transaction(fund_transaction_id, sender_wallet, 10000)
        >>> refund_transaction.sign(refund_solver)
        <shuttle.providers.bytom.transaction.RefundTransaction object at 0x0409DAF0>
        """

        if not isinstance(solver, RefundSolver):
            raise TypeError("solver must be RefundSolver format.")
        wallet = solver.solve()
        wallet.indexes = list()
        for index, unsigned in enumerate(self.unsigned(detail=True)):
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
            wallet.indexes = list()
        return self

    def unsigned_raw(self):
        """
        Get bytom unsigned refund transaction raw.

        :returns: str -- bytom unsigned refund transaction raw.

        >>> from shuttle.providers.bytom.transaction import RefundTransaction
        >>> refund_transaction = RefundTransaction(network="testnet")
        >>> refund_transaction.build_transaction(fund_transaction_id, sender_wallet, 10000)
        >>> refund_transaction.unsigned_raw()
        "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTJjMzkyMjE3NDgzOTA2ZjkwMmU3M2M0YmMxMzI4NjRkZTU4MTUzNzcyZDc5MjY4OTYwOTk4MTYyMjY2NjM0YmUwMTAwMDAwMDAwZmZmZmZmZmYwMmU4MDMwMDAwMDAwMDAwMDAxN2E5MTQ5NzE4OTRjNThkODU5ODFjMTZjMjA1OWQ0MjJiY2RlMGIxNTZkMDQ0ODdhNjI5MDAwMDAwMDAwMDAwMTk3NmE5MTQ2YmNlNjVlNThhNTBiOTc5ODk5MzBlOWE0ZmYxYWMxYTc3NTE1ZWYxODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiAxMjM0MCwgIm4iOiAxLCAic2NyaXB0IjogIjc2YTkxNDZiY2U2NWU1OGE1MGI5Nzk4OTkzMGU5YTRmZjFhYzFhNzc1MTVlZjE4OGFjIn1dLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfdW5zaWduZWQifQ"
        """

        if not self.transaction:
            raise ValueError("transaction script is none, build transaction first")

        return b64encode(str(json.dumps(dict(
            fee=self.fee,
            guid=self.guid,
            unsigned=self.unsigned(detail=False),
            hash=self.transaction["tx"]["hash"],
            raw=self.transaction["raw_transaction"],
            signatures=list(),
            network=self.network,
            type="bytom_refund_unsigned"
        ))).encode()).decode()
