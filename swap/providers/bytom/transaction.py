#!/usr/bin/env python3

from pybytom.transaction import Transaction as BytomTransaction
from pybytom.transaction.tools import find_p2wsh_utxo
from pybytom.transaction.actions import (
    spend_wallet, spend_utxo, control_address, control_program
)
from pybytom.wallet.tools import (
    indexes_to_path, get_program, get_address
)
from pybytom.utils import is_network
from pybytom.script import p2wsh_program
from base64 import b64encode
from typing import Optional

import json

from ...utils.exceptions import NetworkError
from ..config import bytom
from .rpc import (
    build_transaction, decode_transaction_raw
)
from .solver import (
    FundSolver, ClaimSolver, RefundSolver
)
from .utils import amount_converter
from .wallet import Wallet
from .htlc import HTLC

# Bytom config
config = bytom()


class Transaction(BytomTransaction):
    """
    Bytom Transaction class.

    :param network: Bytom network, defaults to mainnet.
    :type network: str
    :returns:  Transaction -- Bytom transaction instance.

    .. note::
        Bytom has only three networks, ``mainnet``. ``solonet`` and ``mainnet``.
    """

    def __init__(self, network: str = config["network"]):

        if not is_network(network=network):
            raise NetworkError(f"Invalid '{network}' network/type",
                               "choose only 'mainnet', 'solonet' or 'testnet' networks.")
        super().__init__(network)

        self._network:         str = network
        self._address:         Optional[str] = None
        self._transaction:     Optional[dict] = None
        self._type:            Optional[str] = None
        self._fee:             int = config["fee"]
        self._confirmations:   int = config["confirmations"]

    def fee(self) -> int:
        """
        Get Bitcoin transaction fee.

        :returns: int -- Bitcoin transaction fee.

        >>> from swap.providers.bytom.transaction import ClaimTransaction
        >>> from swap.providers.bytom.wallet import Wallet
        >>> recipient_wallet = Wallet(network="mainnet").from_mnemonic("hint excuse upgrade sleep easily deputy erase cluster section other ugly limit")
        >>> claim_transaction = ClaimTransaction(network="mainnet")
        >>> claim_transaction.build_transaction("1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", recipient_wallet, 10000, "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> claim_transaction.fee()
        10000000
        """

        return self._fee

    def hash(self) -> str:
        """
        Get Bytom transaction hash.

        :returns: str -- Bytom transaction hash or transaction id.

        >>> from swap.providers.bytom.htlc import HTLC
        >>> from swap.providers.bytom.transaction import FundTransaction
        >>> from swap.providers.bytom.wallet import Wallet
        >>> htlc = HTLC(network="mainnet").init("821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e0158", "3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2", 1000)
        >>> sender_wallet = Wallet(network="mainnet").from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> fund_transaction = FundTransaction(network="mainnet")
        >>> fund_transaction.build_transaction(sender_wallet, htlc, 10000)
        >>> fund_transaction.hash()
        "2993414225f65390220730d0c1a356c14e91bca76db112d37366df93e364a492"
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("transaction is none, build transaction first.")
        return self._transaction["tx"]["hash"]

    def json(self) -> dict:
        """
        Get Bytom transaction json format.

        :returns: dict -- Bytom transaction json format.

        >>> from swap.providers.bytom.transaction import RefundTransaction
        >>> from swap.providers.bytom.wallet import Wallet
        >>> sender_wallet = Wallet(network="mainnet").from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> refund_transaction = RefundTransaction(network="mainnet")
        >>> refund_transaction.build_transaction("481c00212c552fbdf537fcc88c1006a69bdd3130f593965f6ff4f91818a1c6e1", sender_wallet, 10000, "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> refund_transaction.json()
        {"hash": "2993414225f65390220730d0c1a356c14e91bca76db112d37366df93e364a492", "status_fail": false, "size": 379, "submission_timestamp": 0, "memo": "", "inputs": [{"script": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 2450000000, "type": "spend"}], "outputs": [{"utxo_id": "5edccebe497893c289121f9e365fdeb34c97008b9eb5a9960fe9541e7923aabc", "script": "01642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0", "address": "smart contract", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 1000, "type": "control"}, {"utxo_id": "f8cfbb692db1963be88b09c314adcc9e19d91c6c019aa556fb7cb76ba8ffa1fa", "script": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 2439999000, "type": "control"}], "fee": 10000000, "balances": [{"asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": "-10001000"}], "types": ["ordinary"]}
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("transaction is none, build transaction first.")
        return decode_transaction_raw(transaction_raw=self._transaction["raw_transaction"])

    def raw(self) -> str:
        """
        Get Bytom transaction raw.

        :returns: str -- Bytom transaction raw.

        >>> from swap.providers.bytom.transaction import ClaimTransaction
        >>> from swap.providers.bytom.wallet import Wallet
        >>> recipient_wallet = Wallet(network="mainnet").from_mnemonic("hint excuse upgrade sleep easily deputy erase cluster section other ugly limit")
        >>> claim_transaction = ClaimTransaction(network="mainnet")
        >>> claim_transaction.build_transaction("1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", recipient_wallet, 10000, "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> claim_transaction.raw()
        "070100010160015e7f2d7ecec3f61d30d0b2968973a3ac8448f0599ea20dce883b48c903c4d6e87fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8091a0900901011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a22012091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e20201ad01ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe80701880101642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c000013dffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff98dcbd8b09011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a00"
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("transaction is none, build transaction first.")
        return self._transaction["raw_transaction"]
    
    def type(self):
        """
        Get Bitcoin signature transaction type.

        :returns: str -- Bitcoin signature transaction type.

        >>> from swap.providers.bytom.transaction import ClaimTransaction
        >>> from swap.providers.bytom.wallet import Wallet
        >>> recipient_wallet = Wallet(network="mainnet").from_mnemonic("hint excuse upgrade sleep easily deputy erase cluster section other ugly limit")
        >>> claim_transaction = ClaimTransaction(network="mainnet")
        >>> claim_transaction.build_transaction("1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", recipient_wallet, 10000, "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> claim_transaction.type()
        "bitcoin_claim_unsigned"
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("transaction script is none, build transaction first.")
        return self._type

    def unsigned_datas(self, detail: bool = False) -> list:
        """
        Get Bytom transaction unsigned datas with instruction.

        :param detail: Bytom unsigned datas to see detail, defaults to False.
        :type detail: bool
        :returns: list -- Bytom transaction unsigned datas.

        >>> from swap.providers.bytom.htlc import HTLC
        >>> from swap.providers.bytom.transaction import FundTransaction
        >>> from swap.providers.bytom.wallet import Wallet
        >>> htlc = HTLC(network="mainnet").init("821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e0158", "3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2", 1000)
        >>> sender_wallet = Wallet(network="mainnet").from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> fund_transaction = FundTransaction(network="mainnet")
        >>> fund_transaction.build_transaction(sender_wallet, htlc, 10000)
        >>> fund_transaction.unsigned_datas()
        [{'datas': ['38601bf7ce08dab921916f2c723acca0451d8904649bbec16c2076f1455dd1a2'], 'public_key': '91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2', 'network': 'mainnet', 'path': 'm/44/153/1/0/1'}]
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("transaction is none, build transaction first.")

        unsigned_datas: list = []
        for signing_instruction in self._transaction["signing_instructions"]:
            unsigned_data = dict(datas=signing_instruction["sign_data"])
            if "pubkey" in signing_instruction and signing_instruction["pubkey"]:
                unsigned_data.setdefault("public_key", signing_instruction["pubkey"])
                if detail:
                    program = get_program(public_key=signing_instruction["pubkey"])
                    address = get_address(program=program, network=self._network)
                    unsigned_data.setdefault("program", program)
                    unsigned_data.setdefault("address", address)
                else:
                    unsigned_data.setdefault("network", self._network)
            else:
                if detail:
                    unsigned_data.setdefault("public_key", None)
                    unsigned_data.setdefault("program", None)
                    unsigned_data.setdefault("address", None)
                else:
                    unsigned_data.setdefault("network", self._network)
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

        return unsigned_datas

    def sign(self, *args, **kwargs):
        # Not implemented
        pass

    def signatures(self):
        """
        Get Bytom transaction signatures(signed datas).

        :returns: list -- Bytom transaction signatures.

        >>> from swap.providers.bytom.htlc import HTLC
        >>> from swap.providers.bytom.transaction import FundTransaction
        >>> from swap.providers.bytom.solver import FundSolver
        >>> from swap.providers.bytom.wallet import Wallet
        >>> htlc = HTLC(network="mainnet").init("821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e0158", "3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2", 1000)
        >>> sender_wallet = Wallet(network="mainnet").from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> fund_solver = FundSolver("205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
        >>> fund_transaction = FundTransaction(network="mainnet")
        >>> fund_transaction.build_transaction(sender_wallet, htlc, 10000)
        >>> fund_transaction.sign(solver=fund_solver)
        >>> fund_transaction.signatures()
        [['8ca69a01def05118866681bc7008971efcff40895285297e0d6bd791220a36d6ef85a11abc48438de21f0256c4f82752b66eb58100ce6b213e1af14cc130ec0e']]
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("transaction is none, build transaction first.")
        return self._signatures


class FundTransaction(Transaction):
    """
    Bytom FundTransaction class.

    :param network: Bytom network, defaults to mainnet.
    :type network: str
    :returns: FundTransaction -- Bytom fund transaction instance.

    .. warning::
        Do not forget to build transaction after initialize fund transaction.
    """

    # Initialize fund transaction
    def __init__(self, network="mainnet"):
        super().__init__(network)

    def build_transaction(self, address: str, htlc: HTLC, amount: int, asset: str = config["asset"]):
        """
        Build Bytom fund transaction.

        :param address: Bytom sender wallet address.
        :type address: str
        :param htlc: Bytom hash time lock contract (HTLC).
        :type htlc: bytom.htlc.HTLC
        :param amount: Bytom amount to fund.
        :type amount: int
        :param asset: Bytom asset id, defaults to BTM asset.
        :type asset: str
        :returns: FundTransaction -- Bytom fund transaction instance.

        >>> from swap.providers.bytom.htlc import HTLC
        >>> from swap.providers.bytom.transaction import FundTransaction
        >>> from swap.providers.bytom.wallet import Wallet
        >>> htlc = HTLC(network="mainnet").init("821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e0158", "3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2", 1000)
        >>> sender_wallet = Wallet(network="mainnet").from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> fund_transaction = FundTransaction(network="mainnet")
        >>> fund_transaction.build_transaction(address=sender_wallet.address(), htlc=htlc, amount=10000)
        <swap.providers.bytom.transaction.FundTransaction object at 0x0409DAF0>
        """

        # Set address, fee and confirmations
        self._address, self._fee, self._confirmations = (
            address, config["fee"], config["confirmations"]
        )

        # Build transaction
        self._transaction = build_transaction(
            address=self._address,
            transaction=dict(
                fee=str(amount_converter(self._fee, "NEU2BTM")),
                confirmations=self._confirmations,
                inputs=[
                    spend_wallet(
                        asset=asset,
                        amount=amount
                    )
                ],
                outputs=[
                    control_program(
                        asset=asset,
                        amount=amount,
                        program=p2wsh_program(  # Change script hash to P2WSH
                            script_hash=htlc.hash()
                        )
                    )
                ]
            ),
            network=self._network
        )

        # Set transaction type
        self._type = "bytom_fund_unsigned"
        return self

    def sign(self, solver: FundSolver):
        """
        Sign Bytom fund transaction.

        :param solver: Bytom fund solver.
        :type solver: bytom.solver.FundSolver
        :returns: FundTransaction -- Bytom fund transaction instance.

        >>> from swap.providers.bytom.htlc import HTLC
        >>> from swap.providers.bytom.transaction import FundTransaction
        >>> from swap.providers.bytom.solver import FundSolver
        >>> from swap.providers.bytom.wallet import Wallet
        >>> htlc = HTLC(network="mainnet").init("821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e0158", "3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2", 1000)
        >>> sender_wallet = Wallet(network="mainnet").from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> fund_solver = FundSolver("205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
        >>> fund_transaction = FundTransaction(network="mainnet")
        >>> fund_transaction.build_transaction(sender_wallet, htlc, 10000)
        >>> fund_transaction.sign(solver=fund_solver)
        <swap.providers.bytom.transaction.FundTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not isinstance(solver, FundSolver):
            raise TypeError(f"solver must be FundSolver, not '{type(solver)}' type.")

        # Setting sender wallet
        wallet, path, indexes = solver.solve()
        # Clean derivation indexes/path
        wallet.clean_derivation()
        # Signing refund transaction
        for unsigned in self.unsigned_datas(detail=True):
            signed_data = []
            unsigned_datas = unsigned["datas"]
            if unsigned["path"]:
                wallet.from_path(unsigned["path"])
            elif path:
                wallet.from_path(path)
            elif indexes:
                wallet.from_indexes(indexes)
            for unsigned_data in unsigned_datas:
                signed_data.append(wallet.sign(unsigned_data))
            self._signatures.append(signed_data)
            wallet.clean_derivation()

        # Set transaction type
        self._type = "bytom_fund_signed"
        return self

    def unsigned_raw(self) -> str:
        """
        Get Bytom unsigned fund swap transaction raw.

        :returns: str -- Bytom unsigned fund transaction raw.

        >>> from swap.providers.bytom.htlc import HTLC
        >>> from swap.providers.bytom.transaction import FundTransaction
        >>> from swap.providers.bytom.wallet import Wallet
        >>> htlc = HTLC(network="mainnet").init("821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e0158", "3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2", 1000)
        >>> sender_wallet = Wallet(network="mainnet").from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> fund_transaction = FundTransaction(network="mainnet")
        >>> fund_transaction.build_transaction(sender_wallet, htlc, 10000)
        >>> fund_transaction.unsigned_raw()
        "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTJjMzkyMjE3NDgzOTA2ZjkwMmU3M2M0YmMxMzI4NjRkZTU4MTUzNzcyZDc5MjY4OTYwOTk4MTYyMjY2NjM0YmUwMTAwMDAwMDAwZmZmZmZmZmYwMmU4MDMwMDAwMDAwMDAwMDAxN2E5MTQ5NzE4OTRjNThkODU5ODFjMTZjMjA1OWQ0MjJiY2RlMGIxNTZkMDQ0ODdhNjI5MDAwMDAwMDAwMDAwMTk3NmE5MTQ2YmNlNjVlNThhNTBiOTc5ODk5MzBlOWE0ZmYxYWMxYTc3NTE1ZWYxODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiAxMjM0MCwgIm4iOiAxLCAic2NyaXB0IjogIjc2YTkxNDZiY2U2NWU1OGE1MGI5Nzk4OTkzMGU5YTRmZjFhYzFhNzc1MTVlZjE4OGFjIn1dLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfdW5zaWduZWQifQ"
        """

        # Check transaction
        if not self._transaction:
            raise ValueError("transaction script is none, build transaction first")

        # Encode claim transaction raw and return
        return b64encode(str(json.dumps(dict(
            fee=self.fee(),
            address=self._address,
            unsigned_datas=self.unsigned_datas(detail=False),
            hash=self.hash(),
            raw=self.raw(),
            signatures=[],
            network=self._network,
            type="bytom_fund_unsigned"
        ))).encode()).decode()


class ClaimTransaction(Transaction):
    """
    Bytom ClaimTransaction class.

    :param network: Bytom network, defaults to mainnet.
    :type network: str
    :returns: ClaimTransaction -- Bytom claim transaction instance.

    .. warning::
        Do not forget to build transaction after initialize claim transaction.
    """

    # Initialize claim transaction
    def __init__(self, network="mainnet"):
        super().__init__(network)

    def build_transaction(self, transaction_id: str, address: str, amount: int, asset: str = config["asset"]):
        """
        Build Bytom claim transaction.

        :param transaction_id: Bytom fund transaction id to redeem.
        :type transaction_id: str
        :param address: Bytom recipient wallet address.
        :type address: str
        :param amount: Bytom amount to withdraw.
        :type amount: int
        :param asset: Bytom asset id, defaults to BTM asset.
        :type asset: str
        :returns: ClaimTransaction -- Bytom claim transaction instance.

        >>> from swap.providers.bytom.transaction import ClaimTransaction
        >>> from swap.providers.bytom.wallet import Wallet
        >>> recipient_wallet = Wallet(network="mainnet").from_mnemonic("hint excuse upgrade sleep easily deputy erase cluster section other ugly limit")
        >>> claim_transaction = ClaimTransaction(network="mainnet")
        >>> claim_transaction.build_transaction(transaction_id="1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", address=recipient_wallet.address(), amount=10000, asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        <swap.providers.bytom.transaction.ClaimTransaction object at 0x0409DAF0>
        """

        # Find HTLC UTXO id.
        htlc_utxo_id = find_p2wsh_utxo(
            transaction_id=transaction_id,
            network=self._network
        )
        if htlc_utxo_id is None:
            raise ValueError("Invalid transaction id, there is no pay to witness script hash (P2WSH).")

        # Set address, fee and confirmations
        self._address, self._fee, self._confirmations = (
            address, config["fee"], config["confirmations"]
        )

        # Build transaction
        self._transaction = build_transaction(
            address=self._address,
            transaction=dict(
                fee=str(amount_converter(self._fee, "NEU2BTM")),
                confirmations=self._confirmations,
                inputs=[
                    spend_utxo(
                        utxo=htlc_utxo_id
                    )
                ],
                outputs=[
                    control_address(
                        asset=asset,
                        amount=amount,
                        address=self._address
                    )
                ]
            ),
            network=self._network
        )

        # Set transaction type
        self._type = "bytom_claim_unsigned"
        return self

    def sign(self, solver: ClaimSolver):
        """
        Sign Bytom claim transaction.

        :param solver: Bytom claim solver.
        :type solver: bytom.solver.ClaimSolver
        :returns: ClaimTransaction -- Bytom claim transaction instance.

        >>> from swap.providers.bytom.transaction import ClaimTransaction
        >>> from swap.providers.bytom.solver import ClaimSolver
        >>> from swap.providers.bytom.wallet import Wallet
        >>> recipient_wallet = Wallet(network="mainnet").from_mnemonic("hint excuse upgrade sleep easily deputy erase cluster section other ugly limit")
        >>> claim_solver = ClaimSolver(recipient_wallet.xprivate_key(), "Hello Meheret!", "3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb", recipient_wallet.public_key(), "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2", 1000)
        >>> claim_transaction = ClaimTransaction(network="mainnet")
        >>> claim_transaction.build_transaction("1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", recipient_wallet, 10000, "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> claim_transaction.sign(solver=claim_solver)
        <swap.providers.bytom.transaction.ClaimTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not isinstance(solver, ClaimSolver):
            raise TypeError(f"solver must be ClaimSolver, not '{type(solver)}' type.")

        # Set recipient wallet
        wallet, secret, path, indexes = solver.solve()
        # Clean derivation indexes/path
        wallet.clean_derivation()
        # Sign claim transaction
        for index, unsigned in enumerate(self.unsigned_datas(detail=True)):
            signed_data = []
            unsigned_datas = unsigned["datas"]
            if unsigned["path"]:
                wallet.from_path(unsigned["path"])
            elif path:
                wallet.from_path(path)
            elif indexes:
                wallet.from_indexes(indexes)
            for unsigned_data in unsigned_datas:
                if index == 0:
                    signed_data.append(bytearray(secret.encode()).hex())
                    signed_data.append(wallet.sign(unsigned_data))
                    signed_data.append(str("00"))
                    signed_data.append(solver.witness(self._network, False))
                else:
                    signed_data.append(wallet.sign(unsigned_data))
            self._signatures.append(signed_data)
            wallet.clean_derivation()

        # Set transaction type
        self._type = "bytom_claim_signed"
        return self

    def unsigned_raw(self) -> str:
        """
        Get Bytom unsigned claim swap transaction raw.

        :returns: str -- Bytom unsigned claim transaction raw.

        >>> from swap.providers.bytom.transaction import ClaimTransaction
        >>> from swap.providers.bytom.wallet import Wallet
        >>> wallet = Wallet(network="mainnet").from_mnemonic("hint excuse upgrade sleep easily deputy erase cluster section other ugly limit")
        >>> claim_transaction = ClaimTransaction(network="mainnet")
        >>> claim_transaction.build_transaction("1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", wallet, 10000, "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> claim_transaction.unsigned_raw()
        "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTJjMzkyMjE3NDgzOTA2ZjkwMmU3M2M0YmMxMzI4NjRkZTU4MTUzNzcyZDc5MjY4OTYwOTk4MTYyMjY2NjM0YmUwMTAwMDAwMDAwZmZmZmZmZmYwMmU4MDMwMDAwMDAwMDAwMDAxN2E5MTQ5NzE4OTRjNThkODU5ODFjMTZjMjA1OWQ0MjJiY2RlMGIxNTZkMDQ0ODdhNjI5MDAwMDAwMDAwMDAwMTk3NmE5MTQ2YmNlNjVlNThhNTBiOTc5ODk5MzBlOWE0ZmYxYWMxYTc3NTE1ZWYxODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiAxMjM0MCwgIm4iOiAxLCAic2NyaXB0IjogIjc2YTkxNDZiY2U2NWU1OGE1MGI5Nzk4OTkzMGU5YTRmZjFhYzFhNzc1MTVlZjE4OGFjIn1dLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfdW5zaWduZWQifQ"
        """

        # Check transaction
        if not self._transaction:
            raise ValueError("transaction script is none, build transaction first")

        # Encode claim transaction raw and return
        return b64encode(str(json.dumps(dict(
            fee=self.fee(),
            address=self._address,
            unsigned_datas=self.unsigned_datas(detail=False),
            hash=self.hash(),
            raw=self.raw(),
            network=self._network,
            signatures=[],
            type="bytom_claim_unsigned"
        ))).encode()).decode()


class RefundTransaction(Transaction):
    """
    Bytom RefundTransaction class.

    :param network: Bytom network, defaults to mainnet.
    :type network: str
    :returns: RefundTransaction -- Bytom refund transaction instance.

    .. warning::
        Do not forget to build transaction after initialize refund transaction.
    """

    # Initialize fund transaction
    def __init__(self, network="mainnet"):
        super().__init__(network)

    def build_transaction(self, transaction_id: str, address: str, amount: int, asset: str = config["asset"]):
        """
        Build Bytom refund transaction.

        :param transaction_id: Bytom fund transaction id to redeem.
        :type transaction_id: str
        :param address: Bytom sender wallet address.
        :type address: str
        :param amount: Bytom amount to withdraw.
        :type amount: int
        :param asset: Bytom asset id, defaults to BTM asset.
        :type asset: str
        :returns: RefundTransaction -- Bytom refund transaction instance.

        >>> from swap.providers.bytom.transaction import RefundTransaction
        >>> from swap.providers.bytom.wallet import Wallet
        >>> sender_wallet = Wallet(network="mainnet").from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> refund_transaction = RefundTransaction(network="mainnet")
        >>> refund_transaction.build_transaction(transaction_id="481c00212c552fbdf537fcc88c1006a69bdd3130f593965f6ff4f91818a1c6e1", address=sender_wallet.address(), amount=10000, asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        <swap.providers.bytom.transaction.RefundTransaction object at 0x0409DAF0>
        """

        # Find HTLC UTXO id.
        htlc_utxo_id = find_p2wsh_utxo(
            transaction_id=transaction_id,
            network=self._network
        )
        if htlc_utxo_id is None:
            raise ValueError("Invalid transaction id, there is no pay to witness script hash (P2WSH).")

        # Set address, fee and confirmations
        self._address, self._fee, self._confirmations = (
            address, config["fee"], config["confirmations"]
        )

        # Build transaction
        self._transaction = build_transaction(
            address=self._address,
            transaction=dict(
                fee=str(amount_converter(self._fee, "NEU2BTM")),
                confirmations=self._confirmations,
                inputs=[
                    spend_utxo(
                        utxo=htlc_utxo_id
                    )
                ],
                outputs=[
                    control_address(
                        asset=asset,
                        amount=amount,
                        address=self._address
                    )
                ]
            ),
            network=self._network
        )

        # Set transaction type
        self._type = "bytom_refund_unsigned"
        return self

    # Signing transaction using private keys
    def sign(self, solver: RefundSolver):
        """
        Sign Bytom refund transaction.

        :param solver: Bytom refund solver.
        :type solver: bytom.solver.RefundSolver
        :returns: RefundTransaction -- Bytom refund transaction instance.

        >>> from swap.providers.bytom.transaction import RefundTransaction
        >>> from swap.providers.bytom.solver import RefundSolver
        >>> from swap.providers.bytom.wallet import Wallet
        >>> sender_wallet = Wallet(network="mainnet").from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> refund_solver = RefundSolver(wallet.xprivate_key(), "3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb", "3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", wallet.public_key(), 1000)
        >>> refund_transaction = RefundTransaction(network="mainnet")
        >>> refund_transaction.build_transaction("481c00212c552fbdf537fcc88c1006a69bdd3130f593965f6ff4f91818a1c6e1", sender_wallet, 10000, "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> refund_transaction.sign(solver=refund_solver)
        <swap.providers.bytom.transaction.RefundTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not isinstance(solver, RefundSolver):
            raise TypeError(f"solver must be RefundSolver, not '{type(solver)}' type.")

        # Set recipient wallet
        wallet, path, indexes = solver.solve()
        # Clean derivation indexes/path
        wallet.clean_derivation() 
        # Sign claim transaction
        for index, unsigned in enumerate(self.unsigned_datas(detail=True)):
            signed_data = []
            unsigned_datas = unsigned["datas"]
            if unsigned["path"]:
                wallet.from_path(unsigned["path"])
            elif path:
                wallet.from_path(path)
            elif indexes:
                wallet.from_indexes(indexes)
            for unsigned_data in unsigned_datas:
                if index == 0:
                    signed_data.append(wallet.sign(unsigned_data))
                    signed_data.append(str("01"))
                    signed_data.append(solver.witness(self._network, False))
                else:
                    signed_data.append(wallet.sign(unsigned_data))
            self._signatures.append(signed_data)
            wallet.clean_derivation()

        # Set transaction type
        self._type = "bytom_refund_signed"
        return self

    def unsigned_raw(self) -> str:
        """
        Get Bytom unsigned refund swap transaction raw.

        :returns: str -- Bytom unsigned refund transaction raw.

        >>> from swap.providers.bytom.transaction import RefundTransaction
        >>> from swap.providers.bytom.wallet import Wallet
        >>> sender_wallet = Wallet(network="mainnet").from_mnemonic("indicate warm sock mistake code spot acid ribbon sing over taxi toast")
        >>> refund_transaction = RefundTransaction(network="mainnet")
        >>> refund_transaction.build_transaction("481c00212c552fbdf537fcc88c1006a69bdd3130f593965f6ff4f91818a1c6e1", sender_wallet, 10000, "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> refund_transaction.unsigned_raw()
        "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTJjMzkyMjE3NDgzOTA2ZjkwMmU3M2M0YmMxMzI4NjRkZTU4MTUzNzcyZDc5MjY4OTYwOTk4MTYyMjY2NjM0YmUwMTAwMDAwMDAwZmZmZmZmZmYwMmU4MDMwMDAwMDAwMDAwMDAxN2E5MTQ5NzE4OTRjNThkODU5ODFjMTZjMjA1OWQ0MjJiY2RlMGIxNTZkMDQ0ODdhNjI5MDAwMDAwMDAwMDAwMTk3NmE5MTQ2YmNlNjVlNThhNTBiOTc5ODk5MzBlOWE0ZmYxYWMxYTc3NTE1ZWYxODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiAxMjM0MCwgIm4iOiAxLCAic2NyaXB0IjogIjc2YTkxNDZiY2U2NWU1OGE1MGI5Nzk4OTkzMGU5YTRmZjFhYzFhNzc1MTVlZjE4OGFjIn1dLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfdW5zaWduZWQifQ"
        """

        # Check transaction
        if not self._transaction:
            raise ValueError("transaction script is none, build transaction first")

        # Encode claim transaction raw and return
        return b64encode(str(json.dumps(dict(
            fee=self.fee(),
            address=self._address,
            unsigned_datas=self.unsigned_datas(detail=False),
            hash=self.hash(),
            raw=self.raw(),
            signatures=[],
            network=self._network,
            type="bytom_refund_unsigned"
        ))).encode()).decode()
