#!/usr/bin/env python3

from pybytom.transaction.tools import find_p2wsh_utxo
from pybytom.wallet.tools import indexes_to_path, get_program, get_address
from pybytom.rpc import list_address
from pybytom.script import p2wsh_program
from base64 import b64encode

import json

from .rpc import build_transaction, decode_tx_raw
from .utils import spend_wallet_action, \
    control_program_action, spend_utxo_action, control_address_action
from .solver import FundSolver, ClaimSolver, RefundSolver
from .htlc import HTLC
from .wallet import Wallet
from ..config import bytom

# Bytom configuration
bytom = bytom()


class Transaction:
    """
    Bytom Transaction class.

    :param network: Bytom network, defaults to testnet.
    :type network: str
    :param guid: Bytom blockcenter guid, defaults to None.
    :type guid: str
    :param inputs: Bytom transaction inputs, defaults to None.
    :type inputs: list
    :param outputs: Bytom transaction outputs, defaults to None.
    :type outputs: list
    :param tx: Bytom transaction, defaults to None.
    :type tx: dict
    :returns:  Transaction -- Bytom transaction instance.

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
        # Bytom fee and type
        self._fee, self._type = bytom["fee"], None
        # Signed datas
        self._signatures = []

    # Building Bytom transaction
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

    # Transaction fee
    def fee(self):
        """
        Get Bitcoin transaction fee.

        :returns: int -- Bitcoin transaction fee.

        >>> from shuttle.providers.bytom.transaction import ClaimTransaction
        >>> from shuttle.providers.bytom.wallet import Wallet
        >>> recipient_wallet = Wallet(network="testnet").from_mnemonic("hint excuse upgrade sleep easily deputy erase cluster section other ugly limit")
        >>> claim_transaction = ClaimTransaction(network="testnet")
        >>> claim_transaction.build_transaction("1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", recipient_wallet, 10000, "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> claim_transaction.fee()
        10000000
        """

        return self._fee

    # Transaction hash
    def hash(self):
        """
        Get Bytom transaction hash.

        :returns: str -- Bytom transaction hash or transaction id.

        >>> from shuttle.providers.bytom.htlc import HTLC
        >>> from shuttle.providers.bytom.transaction import FundTransaction
        >>> from shuttle.providers.bytom.wallet import Wallet
        >>> htlc = HTLC(network="testnet").init("821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e0158", "3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2", 1000)
        >>> sender_wallet = Wallet(network="testnet").from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> fund_transaction = FundTransaction(network="testnet")
        >>> fund_transaction.build_transaction(sender_wallet, htlc, 10000)
        >>> fund_transaction.hash()
        "2993414225f65390220730d0c1a356c14e91bca76db112d37366df93e364a492"
        """

        # Checking transaction
        if self.transaction is None:
            raise ValueError("transaction is none, build transaction first.")
        return self.transaction["tx"]["hash"]

    # Transaction json
    def json(self):
        """
        Get Bytom transaction json format.

        :returns: dict -- Bytom transaction json format.

        >>> from shuttle.providers.bytom.transaction import RefundTransaction
        >>> from shuttle.providers.bytom.wallet import Wallet
        >>> sender_wallet = Wallet(network="testnet").from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> refund_transaction = RefundTransaction(network="testnet")
        >>> refund_transaction.build_transaction("481c00212c552fbdf537fcc88c1006a69bdd3130f593965f6ff4f91818a1c6e1", sender_wallet, 10000, "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> refund_transaction.json()
        {"hash": "2993414225f65390220730d0c1a356c14e91bca76db112d37366df93e364a492", "status_fail": false, "size": 379, "submission_timestamp": 0, "memo": "", "inputs": [{"script": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 2450000000, "type": "spend"}], "outputs": [{"utxo_id": "5edccebe497893c289121f9e365fdeb34c97008b9eb5a9960fe9541e7923aabc", "script": "01642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0", "address": "smart contract", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 1000, "type": "control"}, {"utxo_id": "f8cfbb692db1963be88b09c314adcc9e19d91c6c019aa556fb7cb76ba8ffa1fa", "script": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 2439999000, "type": "control"}], "fee": 10000000, "balances": [{"asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": "-10001000"}], "types": ["ordinary"]}
        """

        # Checking transaction
        if self.transaction is None:
            raise ValueError("transaction is none, build transaction first.")
        return decode_tx_raw(tx_raw=self.transaction["raw_transaction"])

    # Transaction raw
    def raw(self):
        """
        Get Bytom transaction raw.

        :returns: str -- Bytom transaction raw.

        >>> from shuttle.providers.bytom.transaction import ClaimTransaction
        >>> from shuttle.providers.bytom.wallet import Wallet
        >>> recipient_wallet = Wallet(network="testnet").from_mnemonic("hint excuse upgrade sleep easily deputy erase cluster section other ugly limit")
        >>> claim_transaction = ClaimTransaction(network="testnet")
        >>> claim_transaction.build_transaction("1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", recipient_wallet, 10000, "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> claim_transaction.raw()
        "070100010160015e7f2d7ecec3f61d30d0b2968973a3ac8448f0599ea20dce883b48c903c4d6e87fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8091a0900901011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a22012091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e20201ad01ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe80701880101642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c000013dffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff98dcbd8b09011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a00"
        """

        # Checking transaction
        if self.transaction is None:
            raise ValueError("transaction is none, build transaction first.")
        return self.transaction["raw_transaction"]
    
    def type(self):
        """
        Get Bitcoin signature transaction type.

        :returns: str -- Bitcoin signature transaction type.

        >>> from shuttle.providers.bytom.transaction import ClaimTransaction
        >>> from shuttle.providers.bytom.wallet import Wallet
        >>> recipient_wallet = Wallet(network="testnet").from_mnemonic("hint excuse upgrade sleep easily deputy erase cluster section other ugly limit")
        >>> claim_transaction = ClaimTransaction(network="testnet")
        >>> claim_transaction.build_transaction("1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", recipient_wallet, 10000, "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> claim_transaction.type()
        "bitcoin_claim_unsigned"
        """

        # Checking transaction
        if self.transaction is None:
            raise ValueError("transaction script is none, build transaction first.")
        return self._type

    def unsigned_datas(self, detail=False):
        """
        Get Bytom transaction unsigned datas with instruction.

        :param detail: Bytom unsigned datas to see detail, defaults to False.
        :type detail: bool
        :returns: list -- Bytom transaction unsigned datas.

        >>> from shuttle.providers.bytom.htlc import HTLC
        >>> from shuttle.providers.bytom.transaction import FundTransaction
        >>> from shuttle.providers.bytom.wallet import Wallet
        >>> htlc = HTLC(network="testnet").init("821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e0158", "3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2", 1000)
        >>> sender_wallet = Wallet(network="testnet").from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> fund_transaction = FundTransaction(network="testnet")
        >>> fund_transaction.build_transaction(sender_wallet, htlc, 10000)
        >>> fund_transaction.unsigned_datas()
        [{'datas': ['38601bf7ce08dab921916f2c723acca0451d8904649bbec16c2076f1455dd1a2'], 'public_key': '91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2', 'network': 'mainnet', 'path': 'm/44/153/1/0/1'}]
        """

        # Checking transaction
        if self.transaction is None:
            raise ValueError("transaction is none, build transaction first.")

        unsigned_datas = []
        for signing_instruction in self.transaction["signing_instructions"]:
            unsigned_data = dict(datas=signing_instruction["sign_data"])
            if "pubkey" in signing_instruction and signing_instruction["pubkey"]:
                unsigned_data.setdefault("public_key", signing_instruction["pubkey"])
                if detail:
                    program = get_program(public_key=signing_instruction["pubkey"])
                    address = get_address(program=program, network=self.network)
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
                path = indexes_to_path(indexes=signing_instruction["derivation_path"])
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

    # Transaction signed datas
    def signatures(self):
        """
        Get Bytom transaction signatures(signed datas).

        :returns: list -- Bytom transaction signatures.

        >>> from shuttle.providers.bytom.htlc import HTLC
        >>> from shuttle.providers.bytom.transaction import FundTransaction
        >>> from shuttle.providers.bytom.solver import FundSolver
        >>> from shuttle.providers.bytom.wallet import Wallet
        >>> htlc = HTLC(network="testnet").init("821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e0158", "3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2", 1000)
        >>> sender_wallet = Wallet(network="testnet").from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> fund_solver = FundSolver("205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
        >>> fund_transaction = FundTransaction(network="testnet")
        >>> fund_transaction.build_transaction(sender_wallet, htlc, 10000)
        >>> fund_transaction.sign(solver=fund_solver)
        >>> fund_transaction.signatures()
        [['8ca69a01def05118866681bc7008971efcff40895285297e0d6bd791220a36d6ef85a11abc48438de21f0256c4f82752b66eb58100ce6b213e1af14cc130ec0e']]
        """

        # Checking transaction
        if self.transaction is None:
            raise ValueError("transaction is none, build transaction first.")
        return self._signatures


class FundTransaction(Transaction):
    """
    Bytom FundTransaction class.

    :param network: Bytom network, defaults to testnet.
    :type network: str
    :returns: FundTransaction -- Bytom fund transaction instance.

    .. warning::
        Do not forget to build transaction after initialize fund transaction.
    """

    # Initialization fund transaction
    def __init__(self, network="testnet"):
        super().__init__(network)

    def build_transaction(self, wallet, htlc, amount, asset=bytom["BTM_asset"]):
        """
        Build Bytom fund transaction.

        :param wallet: Bytom sender wallet.
        :type wallet: bytom.wallet.Wallet
        :param htlc: Bytom hash time lock contract (HTLC).
        :type htlc: bytom.htlc.HTLC
        :param amount: Bytom amount to fund.
        :type amount: int
        :param asset: Bytom asset id, defaults to BTM asset.
        :type asset: str
        :returns: FundTransaction -- Bytom fund transaction instance.

        >>> from shuttle.providers.bytom.htlc import HTLC
        >>> from shuttle.providers.bytom.transaction import FundTransaction
        >>> from shuttle.providers.bytom.wallet import Wallet
        >>> htlc = HTLC(network="testnet").init("821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e0158", "3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2", 1000)
        >>> sender_wallet = Wallet(network="testnet").from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> fund_transaction = FundTransaction(network="testnet")
        >>> fund_transaction.build_transaction(wallet=sender_wallet, htlc=htlc, amount=10000)
        <shuttle.providers.bytom.transaction.FundTransaction object at 0x0409DAF0>
        """

        # Checking parameter instances
        if not isinstance(wallet, Wallet):
            raise TypeError("invalid wallet instance, only takes Bytom Wallet class")
        if not isinstance(htlc, HTLC):
            raise TypeError("invalid htlc instance, only takes Bytom HTLC class")
        if not isinstance(amount, int):
            raise TypeError("invalid amount instance, only takes integer type")
        if not isinstance(asset, str):
            raise TypeError("invalid asset instance, only takes string type")

        # Setting wallet GUID
        self.guid, inputs, outputs = wallet.guid(), list(), list()

        # Building input actions
        inputs.append(
            spend_wallet_action(
                asset=asset,
                amount=amount
            )
        )
        # Building output actions
        outputs.append(
            control_program_action(
                asset=asset,
                amount=amount,
                control_program=p2wsh_program(  # Changing script hash to P2WSH
                    script_hash=htlc.hash()
                )
            )
        )
        # Blockcenter transaction
        tx = dict(
            guid=self.guid,
            inputs=inputs,
            outputs=outputs,
            fee=bytom["fee"],
            confirmations=bytom["confirmations"]
        )
        # Building transaction
        self.transaction = build_transaction(tx=tx, network=self.network)
        self._type = "bytom_fund_unsigned"
        return self

    # Signing transaction using xprivate keys
    def sign(self, solver):
        """
        Sign Bytom fund transaction.

        :param solver: Bytom fund solver.
        :type solver: bytom.solver.FundSolver
        :returns: FundTransaction -- Bytom fund transaction instance.

        >>> from shuttle.providers.bytom.htlc import HTLC
        >>> from shuttle.providers.bytom.transaction import FundTransaction
        >>> from shuttle.providers.bytom.solver import FundSolver
        >>> from shuttle.providers.bytom.wallet import Wallet
        >>> htlc = HTLC(network="testnet").init("821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e0158", "3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2", 1000)
        >>> sender_wallet = Wallet(network="testnet").from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> fund_solver = FundSolver("205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
        >>> fund_transaction = FundTransaction(network="testnet")
        >>> fund_transaction.build_transaction(sender_wallet, htlc, 10000)
        >>> fund_transaction.sign(solver=fund_solver)
        <shuttle.providers.bytom.transaction.FundTransaction object at 0x0409DAF0>
        """

        # Checking parameter instances
        if not isinstance(solver, FundSolver):
            raise TypeError("Solver must be FundSolver format.")

        # Setting sender wallet
        wallet = solver.solve()
        wallet.clean_derivation()  # Cleaning any derivation indexes/path
        # Signing refund transaction
        for unsigned in self.unsigned_datas(detail=True):
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
            self._signatures.append(signed_data)
            wallet.clean_derivation()
        self._type = "bytom_fund_signed"
        return self

    def unsigned_raw(self):
        """
        Get Bytom unsigned fund transaction raw.

        :returns: str -- Bytom unsigned fund transaction raw.

        >>> from shuttle.providers.bytom.htlc import HTLC
        >>> from shuttle.providers.bytom.transaction import FundTransaction
        >>> from shuttle.providers.bytom.wallet import Wallet
        >>> htlc = HTLC(network="testnet").init("821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e0158", "3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2", 1000)
        >>> sender_wallet = Wallet(network="testnet").from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> fund_transaction = FundTransaction(network="testnet")
        >>> fund_transaction.build_transaction(sender_wallet, htlc, 10000)
        >>> fund_transaction.unsigned_raw()
        "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTJjMzkyMjE3NDgzOTA2ZjkwMmU3M2M0YmMxMzI4NjRkZTU4MTUzNzcyZDc5MjY4OTYwOTk4MTYyMjY2NjM0YmUwMTAwMDAwMDAwZmZmZmZmZmYwMmU4MDMwMDAwMDAwMDAwMDAxN2E5MTQ5NzE4OTRjNThkODU5ODFjMTZjMjA1OWQ0MjJiY2RlMGIxNTZkMDQ0ODdhNjI5MDAwMDAwMDAwMDAwMTk3NmE5MTQ2YmNlNjVlNThhNTBiOTc5ODk5MzBlOWE0ZmYxYWMxYTc3NTE1ZWYxODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiAxMjM0MCwgIm4iOiAxLCAic2NyaXB0IjogIjc2YTkxNDZiY2U2NWU1OGE1MGI5Nzk4OTkzMGU5YTRmZjFhYzFhNzc1MTVlZjE4OGFjIn1dLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfdW5zaWduZWQifQ"
        """

        # Checking transaction
        if not self.transaction:
            raise ValueError("transaction script is none, build transaction first")

        # Encoding claim transaction raw and return
        return b64encode(str(json.dumps(dict(
            fee=self.fee(),
            guid=self.guid,
            unsigned_datas=self.unsigned_datas(detail=False),
            hash=self.hash(),
            raw=self.raw(),
            signatures=[],
            network=self.network,
            type="bytom_fund_unsigned"
        ))).encode()).decode()


class ClaimTransaction(Transaction):
    """
    Bytom ClaimTransaction class.

    :param network: Bytom network, defaults to testnet.
    :type network: str
    :returns: ClaimTransaction -- Bytom claim transaction instance.

    .. warning::
        Do not forget to build transaction after initialize claim transaction.
    """

    # Initialization claim transaction
    def __init__(self, network="testnet"):
        super().__init__(network)

    def build_transaction(self, transaction_id, wallet, amount, asset=bytom["BTM_asset"]):
        """
        Build Bytom claim transaction.

        :param transaction_id: Bytom fund transaction id to redeem.
        :type transaction_id: str
        :param wallet: Bytom recipient wallet.
        :type wallet: bytom.wallet.Wallet
        :param amount: Bytom amount to withdraw.
        :type amount: int
        :param asset: Bytom asset id, defaults to BTM asset.
        :type asset: str
        :returns: ClaimTransaction -- Bytom claim transaction instance.

        >>> from shuttle.providers.bytom.transaction import ClaimTransaction
        >>> from shuttle.providers.bytom.wallet import Wallet
        >>> recipient_wallet = Wallet(network="testnet").from_mnemonic("hint excuse upgrade sleep easily deputy erase cluster section other ugly limit")
        >>> claim_transaction = ClaimTransaction(network="testnet")
        >>> claim_transaction.build_transaction(transaction_id="1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", wallet=recipient_wallet, amount=10000, asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        <shuttle.providers.bytom.transaction.ClaimTransaction object at 0x0409DAF0>
        """

        # Checking parameter instances
        if not isinstance(transaction_id, str):
            raise TypeError("invalid transaction id instance, only takes Bytom string type")
        if not isinstance(wallet, Wallet):
            raise TypeError("invalid wallet instance, only takes Bytom Wallet class")
        if not isinstance(amount, int):
            raise TypeError("invalid asset instance, only takes integer type")
        if not isinstance(asset, str):
            raise TypeError("invalid amount instance, only takes string type")

        # Finding htlc utxo id.
        utxo_id = find_p2wsh_utxo(
            transaction_id=transaction_id,
            network=self.network
        )
        if utxo_id is None:
            raise ValueError("invalid transaction id, there is no pay to witness script hash")
        if not wallet.guid():
            raise ValueError("can't find recipient wallet guid from wallet")
        elif not isinstance(wallet.guid(), str):
            raise TypeError("invalid recipient guid type, only takes string type")

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
                address=wallet.address() if wallet.address() else list_address(
                    guid=wallet.guid(), limit=1, network=self.network
                )["result"]["data"][0]["address"]
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
        self._type = "bytom_claim_unsigned"
        return self

    # Signing transaction using private keys
    def sign(self, solver):
        """
        Sign Bytom claim transaction.

        :param solver: Bytom claim solver.
        :type solver: bytom.solver.ClaimSolver
        :returns: ClaimTransaction -- Bytom claim transaction instance.

        >>> from shuttle.providers.bytom.transaction import ClaimTransaction
        >>> from shuttle.providers.bytom.solver import ClaimSolver
        >>> from shuttle.providers.bytom.wallet import Wallet
        >>> recipient_wallet = Wallet(network="testnet").from_mnemonic("hint excuse upgrade sleep easily deputy erase cluster section other ugly limit")
        >>> claim_solver = ClaimSolver(recipient_wallet.xprivate_key(), "Hello Meheret!", "3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb", recipient_wallet.public_key(), "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2", 1000)
        >>> claim_transaction = ClaimTransaction(network="testnet")
        >>> claim_transaction.build_transaction("1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", recipient_wallet, 10000, "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> claim_transaction.sign(solver=claim_solver)
        <shuttle.providers.bytom.transaction.ClaimTransaction object at 0x0409DAF0>
        """

        # Checking parameter instances
        if not isinstance(solver, ClaimSolver):
            raise TypeError("solver must be ClaimSolver format.")

        # Setting recipient wallet
        wallet = solver.solve()
        wallet.clean_derivation()  # Cleaning any derivation indexes/path
        # Signing claim transaction
        for index, unsigned in enumerate(self.unsigned_datas(detail=True)):
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
                    signed_data.append(bytearray(solver.secret.encode()).hex())
                    signed_data.append(wallet.sign(unsigned_data))
                    signed_data.append(str("00"))
                    signed_data.append(solver.witness(self.network, False))
                else:
                    signed_data.append(wallet.sign(unsigned_data))
            self._signatures.append(signed_data)
            wallet.clean_derivation()
        self._type = "bytom_claim_signed"
        return self

    def unsigned_raw(self):
        """
        Get Bytom unsigned claim transaction raw.

        :returns: str -- Bytom unsigned claim transaction raw.

        >>> from shuttle.providers.bytom.transaction import ClaimTransaction
        >>> from shuttle.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="testnet").from_mnemonic("hint excuse upgrade sleep easily deputy erase cluster section other ugly limit")
        >>> claim_transaction = ClaimTransaction(network="testnet")
        >>> claim_transaction.build_transaction("1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", wallet, 10000, "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> claim_transaction.unsigned_raw()
        "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTJjMzkyMjE3NDgzOTA2ZjkwMmU3M2M0YmMxMzI4NjRkZTU4MTUzNzcyZDc5MjY4OTYwOTk4MTYyMjY2NjM0YmUwMTAwMDAwMDAwZmZmZmZmZmYwMmU4MDMwMDAwMDAwMDAwMDAxN2E5MTQ5NzE4OTRjNThkODU5ODFjMTZjMjA1OWQ0MjJiY2RlMGIxNTZkMDQ0ODdhNjI5MDAwMDAwMDAwMDAwMTk3NmE5MTQ2YmNlNjVlNThhNTBiOTc5ODk5MzBlOWE0ZmYxYWMxYTc3NTE1ZWYxODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiAxMjM0MCwgIm4iOiAxLCAic2NyaXB0IjogIjc2YTkxNDZiY2U2NWU1OGE1MGI5Nzk4OTkzMGU5YTRmZjFhYzFhNzc1MTVlZjE4OGFjIn1dLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfdW5zaWduZWQifQ"
        """

        # Checking transaction
        if not self.transaction:
            raise ValueError("transaction script is none, build transaction first")

        # Encoding claim transaction raw and return
        return b64encode(str(json.dumps(dict(
            fee=self.fee(),
            guid=self.guid,
            unsigned_datas=self.unsigned_datas(detail=False),
            hash=self.hash(),
            raw=self.raw(),
            network=self.network,
            signatures=[],
            type="bytom_claim_unsigned"
        ))).encode()).decode()


class RefundTransaction(Transaction):
    """
    Bytom RefundTransaction class.

    :param network: Bytom network, defaults to testnet.
    :type network: str
    :returns: RefundTransaction -- Bytom refund transaction instance.

    .. warning::
        Do not forget to build transaction after initialize refund transaction.
    """

    # Initialization fund transaction
    def __init__(self, network="testnet"):
        super().__init__(network)

    def build_transaction(self, transaction_id, wallet, amount, asset=bytom["BTM_asset"]):
        """
        Build Bytom refund transaction.

        :param transaction_id: Bytom fund transaction id to redeem.
        :type transaction_id: str
        :param wallet: Bytom sender wallet.
        :type wallet: bytom.wallet.Wallet
        :param amount: Bytom amount to withdraw.
        :type amount: int
        :param asset: Bytom asset id, defaults to BTM asset.
        :type asset: str
        :returns: RefundTransaction -- Bytom refund transaction instance.

        >>> from shuttle.providers.bytom.transaction import RefundTransaction
        >>> from shuttle.providers.bytom.wallet import Wallet
        >>> sender_wallet = Wallet(network="testnet").from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> refund_transaction = RefundTransaction(network="testnet")
        >>> refund_transaction.build_transaction(transaction_id="481c00212c552fbdf537fcc88c1006a69bdd3130f593965f6ff4f91818a1c6e1", wallet=sender_wallet, amount=10000, asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        <shuttle.providers.bytom.transaction.RefundTransaction object at 0x0409DAF0>
        """

        # Checking parameter instances
        if not isinstance(transaction_id, str):
            raise TypeError("invalid transaction id instance, only takes Bytom string type")
        if not isinstance(wallet, Wallet):
            raise TypeError("invalid wallet instance, only takes Bytom Wallet class")
        if not isinstance(amount, int):
            raise TypeError("invalid asset instance, only takes integer type")
        if not isinstance(asset, str):
            raise TypeError("invalid amount instance, only takes string type")

        # Finding htlc utxo id.
        utxo_id = find_p2wsh_utxo(
            transaction_id=transaction_id, network=self.network)
        if utxo_id is None:
            raise ValueError("invalid transaction id, there is no smart contact")
        if not wallet.guid():
            raise ValueError("can't find sender wallet guid from wallet")
        elif not isinstance(wallet.guid(), str):
            raise TypeError("invalid sender guid type, only takes string type")

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
                address=wallet.address() if wallet.address() else list_address(
                    guid=wallet.guid(), limit=1, network=self.network
                )["result"]["data"][0]["address"]
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
        self._type = "bytom_refund_unsigned"
        return self

    # Signing transaction using private keys
    def sign(self, solver):
        """
        Sign Bytom refund transaction.

        :param solver: Bytom refund solver.
        :type solver: bytom.solver.RefundSolver
        :returns: RefundTransaction -- Bytom refund transaction instance.

        >>> from shuttle.providers.bytom.transaction import RefundTransaction
        >>> from shuttle.providers.bytom.solver import RefundSolver
        >>> from shuttle.providers.bytom.wallet import Wallet
        >>> sender_wallet = Wallet(network="testnet").from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> refund_solver = RefundSolver(wallet.xprivate_key(), "3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb", "3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", wallet.public_key(), 1000)
        >>> refund_transaction = RefundTransaction(network="testnet")
        >>> refund_transaction.build_transaction("481c00212c552fbdf537fcc88c1006a69bdd3130f593965f6ff4f91818a1c6e1", sender_wallet, 10000, "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> refund_transaction.sign(solver=refund_solver)
        <shuttle.providers.bytom.transaction.RefundTransaction object at 0x0409DAF0>
        """

        # Checking parameter instances
        if not isinstance(solver, RefundSolver):
            raise TypeError("solver must be RefundSolver format.")

        # Setting recipient wallet
        wallet = solver.solve()
        wallet.clean_derivation()  # Cleaning any derivation indexes/path
        # Signing claim transaction
        for index, unsigned in enumerate(self.unsigned_datas(detail=True)):
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
                    signed_data.append(solver.witness(self.network, False))
                else:
                    signed_data.append(wallet.sign(unsigned_data))
            self._signatures.append(signed_data)
            wallet.clean_derivation()
        self._type = "bytom_refund_signed"
        return self

    def unsigned_raw(self):
        """
        Get Bytom unsigned refund transaction raw.

        :returns: str -- Bytom unsigned refund transaction raw.

        >>> from shuttle.providers.bytom.transaction import RefundTransaction
        >>> from shuttle.providers.bytom.wallet import Wallet
        >>> sender_wallet = Wallet(network="testnet").from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> refund_transaction = RefundTransaction(network="testnet")
        >>> refund_transaction.build_transaction("481c00212c552fbdf537fcc88c1006a69bdd3130f593965f6ff4f91818a1c6e1", sender_wallet, 10000, "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> refund_transaction.unsigned_raw()
        "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTJjMzkyMjE3NDgzOTA2ZjkwMmU3M2M0YmMxMzI4NjRkZTU4MTUzNzcyZDc5MjY4OTYwOTk4MTYyMjY2NjM0YmUwMTAwMDAwMDAwZmZmZmZmZmYwMmU4MDMwMDAwMDAwMDAwMDAxN2E5MTQ5NzE4OTRjNThkODU5ODFjMTZjMjA1OWQ0MjJiY2RlMGIxNTZkMDQ0ODdhNjI5MDAwMDAwMDAwMDAwMTk3NmE5MTQ2YmNlNjVlNThhNTBiOTc5ODk5MzBlOWE0ZmYxYWMxYTc3NTE1ZWYxODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiAxMjM0MCwgIm4iOiAxLCAic2NyaXB0IjogIjc2YTkxNDZiY2U2NWU1OGE1MGI5Nzk4OTkzMGU5YTRmZjFhYzFhNzc1MTVlZjE4OGFjIn1dLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfdW5zaWduZWQifQ"
        """

        # Checking transaction
        if not self.transaction:
            raise ValueError("transaction script is none, build transaction first")

        # Encoding claim transaction raw and return
        return b64encode(str(json.dumps(dict(
            fee=self.fee(),
            guid=self.guid,
            unsigned_datas=self.unsigned_datas(detail=False),
            hash=self.hash(),
            raw=self.raw(),
            signatures=[],
            network=self.network,
            type="bytom_refund_unsigned"
        ))).encode()).decode()
