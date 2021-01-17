#!/usr/bin/env python3

from pybytom.transaction import Transaction as BytomTransaction
from pybytom.transaction.actions import (
    spend_wallet, spend_utxo, control_address
)
from pybytom.wallet.tools import (
    indexes_to_path, get_program, get_address
)
from base64 import b64encode
from typing import (
    Optional, Union, List
)

import json

from ...utils import clean_transaction_raw
from ...exceptions import (
    AddressError, NetworkError, BalanceError, UnitError
)
from ..config import bytom as config
from .assets import AssetNamespace
from .rpc import (
    estimate_transaction_fee, build_transaction, find_p2wsh_utxo, decode_raw, get_transaction, get_balance
)
from .solver import (
    NormalSolver, FundSolver, ClaimSolver, RefundSolver
)
from .utils import (
    amount_unit_converter, is_network, is_address, get_address_type
)


class Transaction(BytomTransaction):
    """
    Bytom Transaction.

    :param network: Bytom network, defaults to mainnet.
    :type network: str

    :returns: Transaction -- Bytom transaction instance.

    .. note::
        Bytom has only three networks, ``mainnet``. ``solonet`` and ``mainnet``.
    """

    def __init__(self, network: str = config["network"]):

        if not is_network(network=network):
            raise NetworkError(f"Invalid Bytom '{network}' network",
                               "choose only 'mainnet', 'solonet' or 'testnet' networks.")
        super().__init__(network, vapor=False)

        self._network: str = network
        self._address: Optional[str] = None
        self._asset: Optional[str] = None
        self._transaction: Optional[dict] = None
        self._type: Optional[str] = None
        self._confirmations: int = config["confirmations"]
        self._datas: dict = {}
        self._interest: int = 0
        self._amount: int = 0
        self._fee: int = 0

    def fee(self, unit: str = config["unit"]) -> Union[int, float]:
        """
        Get Bytom transaction fee.

        :param unit: Bytom unit, default to NEU.
        :type unit: str

        :returns: int, float -- Bytom transaction fee.

        >>> from swap.providers.bytom.transaction import ClaimTransaction
        >>> claim_transaction = ClaimTransaction("mainnet")
        >>> claim_transaction.build_transaction("bm1q3plwvmvy4qhjmp5zffzmk50aagpujt6f5je85p", "1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", 10000000, False, "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> claim_transaction.fee(unit="NEU")
        10000000
        """

        if unit not in ["BTM", "mBTM", "NEU"]:
            raise UnitError("Invalid Bytom unit, choose only 'BTM', 'mBTM' or 'NEU' units.")
        return self._fee if unit == "NEU" else \
            amount_unit_converter(amount=self._fee, unit_from=f"NEU2{unit}")

    def hash(self) -> str:
        """
        Get Bytom transaction hash.

        :returns: str -- Bytom transaction id/hash.

        >>> from swap.providers.bytom.transaction import FundTransaction
        >>> fund_transaction = FundTransaction("mainnet")
        >>> fund_transaction.build_transaction("bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "bm1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07q3yf5q8", 10000000, "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> fund_transaction.hash()
        "2993414225f65390220730d0c1a356c14e91bca76db112d37366df93e364a492"
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")
        return self._transaction["tx"]["hash"]

    def json(self) -> dict:
        """
        Get Bytom transaction json format.

        :returns: dict -- Bytom transaction json format.

        >>> from swap.providers.bytom.transaction import RefundTransaction
        >>> refund_transaction = RefundTransaction("mainnet")
        >>> refund_transaction.build_transaction("bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "481c00212c552fbdf537fcc88c1006a69bdd3130f593965f6ff4f91818a1c6e1", 10000000, False, "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> refund_transaction.json()
        {"hash": "2993414225f65390220730d0c1a356c14e91bca76db112d37366df93e364a492", "status_fail": false, "size": 379, "submission_timestamp": 0, "memo": "", "inputs": [{"script": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 2450000000, "type": "spend"}], "outputs": [{"utxo_id": "5edccebe497893c289121f9e365fdeb34c97008b9eb5a9960fe9541e7923aabc", "script": "01642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0", "address": "smart contract", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 1000, "type": "control"}, {"utxo_id": "f8cfbb692db1963be88b09c314adcc9e19d91c6c019aa556fb7cb76ba8ffa1fa", "script": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 2439999000, "type": "control"}], "fee": 10000000, "balances": [{"asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": "-10001000"}], "types": ["ordinary"]}
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")
        return decode_raw(raw=self._transaction["raw_transaction"])

    def raw(self) -> str:
        """
        Get Bytom transaction raw.

        :returns: str -- Bytom transaction raw.

        >>> from swap.providers.bytom.transaction import ClaimTransaction
        >>> claim_transaction = ClaimTransaction("mainnet")
        >>> claim_transaction.build_transaction("bm1q3plwvmvy4qhjmp5zffzmk50aagpujt6f5je85p", "1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", 10000000, False, "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> claim_transaction.raw()
        "070100010160015e7f2d7ecec3f61d30d0b2968973a3ac8448f0599ea20dce883b48c903c4d6e87fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8091a0900901011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a22012091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e20201ad01ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe80701880101642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c000013dffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff98dcbd8b09011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a00"
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")
        return self._transaction["raw_transaction"]

    def type(self) -> str:
        """
        Get Bitcoin signature transaction type.

        :returns: str -- Bitcoin signature transaction type.

        >>> from swap.providers.bytom.transaction import ClaimTransaction
        >>> claim_transaction = ClaimTransaction("mainnet")
        >>> claim_transaction.build_transaction("bm1q3plwvmvy4qhjmp5zffzmk50aagpujt6f5je85p", "1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", 10000000, False, "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> claim_transaction.type()
        "bitcoin_claim_unsigned"
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("transaction script is none, build transaction first.")
        return self._type

    def unsigned_datas(self, detail: bool = False) -> List[dict]:
        """
        Get Bytom transaction unsigned datas(messages) with instruction.

        :param detail: Bytom unsigned datas to see detail, defaults to False.
        :type detail: bool

        :returns: list -- Bytom transaction unsigned datas.

        >>> from swap.providers.bytom.transaction import FundTransaction
        >>> from swap.providers.bytom.solver import FundSolver
        >>> from swap.providers.bytom.wallet import Wallet, DEFAULT_PATH
        >>> sender_wallet = Wallet("mainnet").from_entropy("72fee73846f2d1a5807dc8c953bf79f1").from_path(DEFAULT_PATH)
        >>> fund_solver = FundSolver(sender_wallet.xprivate_key())
        >>> fund_transaction = FundTransaction("mainnet")
        >>> fund_transaction.build_transaction(sender_wallet.address(), "bm1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07q3yf5q8", 10000000, "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> fund_transaction.unsigned_datas(solver=fund_solver)
        [{'datas': ['38601bf7ce08dab921916f2c723acca0451d8904649bbec16c2076f1455dd1a2'], 'public_key': '91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2', 'network': 'mainnet', 'path': 'm/44/153/1/0/1'}]
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")

        unsigned_datas: List[dict] = []
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

    def signatures(self) -> List[List[str]]:
        """
        Get Bytom transaction signatures(signed datas).

        :returns: list -- Bytom transaction signatures.

        >>> from swap.providers.bytom.transaction import FundTransaction
        >>> from swap.providers.bytom.solver import FundSolver
        >>> from swap.providers.bytom.wallet import Wallet, DEFAULT_PATH
        >>> sender_wallet = Wallet("mainnet").from_entropy("72fee73846f2d1a5807dc8c953bf79f1").from_path(DEFAULT_PATH)
        >>> fund_solver = FundSolver(sender_wallet.xprivate_key())
        >>> fund_transaction = FundTransaction("mainnet")
        >>> fund_transaction.build_transaction(sender_wallet.address(), "bm1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07q3yf5q8", 10000000, "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> fund_transaction.sign(solver=fund_solver)
        >>> fund_transaction.signatures()
        [['8ca69a01def05118866681bc7008971efcff40895285297e0d6bd791220a36d6ef85a11abc48438de21f0256c4f82752b66eb58100ce6b213e1af14cc130ec0e']]
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")
        return self._signatures

    def datas(self) -> dict:
        return self._datas


class NormalTransaction(Transaction):
    """
    Bytom Normal transaction.

    :param network: Bytom network, defaults to mainnet.
    :type network: str

    :returns: NormalTransaction -- Bytom normal transaction instance.

    .. warning::
        Do not forget to build transaction after initialize normal transaction.
    """

    def __init__(self, network: str = config["network"]):
        super().__init__(network)

    def build_transaction(self, address: str, recipients: dict,
                          asset: Union[str, AssetNamespace] = config["asset"], fee: Optional[Union[int, float]] = None,
                          unit: str = config["unit"], **kwargs) -> "NormalTransaction":
        """
        Build Bytom normal transaction.

        :param address: Bytom sender wallet address.
        :type address: str
        :param recipients: Recipients Bytom address and amount.
        :type recipients: dict
        :param asset: Bytom asset id, defaults to BTM asset.
        :type asset: str, bytom.assets.AssetNamespace
        :param fee: Bytom custom fee, defaults to None.
        :type fee: int, float
        :param unit: Bytom unit, default to NEU.
        :type unit: str

        :returns: NormalTransaction -- Bytom normal transaction instance.

        >>> from swap.providers.bytom.transaction import NormalTransaction
        >>> normal_transaction = NormalTransaction("mainnet")
        >>> normal_transaction.build_transaction(address="bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", recipients={"bm1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07q3yf5q8": 10000000}, asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        <swap.providers.bytom.transaction.NormalTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not is_address(address, self._network):
            raise AddressError(f"Invalid Bytom sender '{address}' {self._network} address.")
        if unit not in ["BTM", "mBTM", "NEU"]:
            raise UnitError("Invalid Bytom unit, choose only 'BTM', 'mBTM' or 'NEU' units.")

        # Set address, fee and confirmations
        self._address, self._asset, self._confirmations, inputs, outputs, self._amount = (
            address, (str(asset.ID) if isinstance(asset, AssetNamespace) else asset),
            config["confirmations"], [], [], (
                sum(recipients.values()) if unit == "NEU" else
                amount_unit_converter(
                    amount=sum(recipients.values()), unit_from=f"{unit}2NEU"
                )
            )
        )

        if "options" in kwargs.keys():
            options: dict = kwargs.get("options")
            if "address" in options and "percent" in options:
                self._interest = int((self._amount * options["percent"]) / 100)

        maximum_amount: int = get_balance(self._address, self._asset)
        if maximum_amount < self._amount:
            raise BalanceError(
                "Insufficient spend UTXO's", f"you don't have enough amount. "
                f"You can spend maximum {maximum_amount} NEU sum of recipients amounts."
            )

        if fee is None:
            # Estimating transaction fee
            self._fee = estimate_transaction_fee(
                address=self._address, asset=self._asset,
                amount=(self._amount if not self._interest else (self._amount + self._interest)),
                confirmations=self._confirmations, network=self._network
            )
        else:
            self._fee = (
                fee if unit == "NEU" else
                amount_unit_converter(
                    amount=fee, unit_from=f"{unit}2NEU"
                )
            )

        fi: int = (self._fee if not self._interest else (self._fee + self._interest))
        if maximum_amount < (self._amount + fi):
            raise BalanceError(
                f"You don't have enough amount to pay {fi} NEU fee",
                f"you can spend maximum {maximum_amount - fi} NEU amount."
            )

        # Outputs action
        for _address, _amount in recipients.items():
            if not is_address(_address, self._network):
                raise AddressError(f"Invalid Bytom recipients '{_address}' {self._network} address.")
            outputs.append(control_address(
                asset=self._asset, address=_address, amount=_amount, vapor=False
            ))

        if self._interest:
            outputs.append(control_address(
                asset=self._asset, amount=self._interest,
                address=kwargs["options"]["address"], vapor=False
            ))

        # Build transaction
        self._transaction = build_transaction(
            address=self._address,
            transaction=dict(
                fee=str(amount_unit_converter(
                    amount=self._fee, unit_from="NEU2BTM"
                )),
                confirmations=self._confirmations,
                inputs=[spend_wallet(
                    asset=self._asset, amount=self._amount
                )],
                outputs=outputs
            ),
            network=self._network
        )

        # Set transaction type
        self._type = "bytom_normal_unsigned"
        return self

    def sign(self, solver: NormalSolver) -> "NormalTransaction":
        """
        Sign Bytom normal transaction.

        :param solver: Bytom normal solver.
        :type solver: bytom.solver.NormalSolver

        :returns: NormalTransaction -- Bytom normal transaction instance.

        >>> from swap.providers.bytom.transaction import NormalTransaction
        >>> from swap.providers.bytom.solver import NormalSolver
        >>> from swap.providers.bytom.wallet import Wallet, DEFAULT_PATH
        >>> sender_wallet = Wallet("mainnet").from_entropy("72fee73846f2d1a5807dc8c953bf79f1").from_path(DEFAULT_PATH)
        >>> normal_solver = NormalSolver(sender_wallet.xprivate_key())
        >>> normal_transaction = NormalTransaction("mainnet")
        >>> normal_transaction.build_transaction(sender_wallet.address(), {"bm1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07q3yf5q8": 10000000}, "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> normal_transaction.sign(solver=normal_solver)
        <swap.providers.bytom.transaction.NormalTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not isinstance(solver, NormalSolver):
            raise TypeError(f"Solver must be Bytom NormalSolver, not {type(solver).__name__} type.")

        # Setting sender wallet
        wallet, path, indexes = solver.solve()
        # Clean derivation indexes/path
        wallet.clean_derivation()
        # Signing normal transaction
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
        self._type = "bytom_normal_signed"
        return self

    def transaction_raw(self) -> str:
        """
        Get Bytom normal transaction raw.

        :returns: str -- Bytom normal transaction raw.

        >>> from swap.providers.bytom.transaction import NormalTransaction
        >>> normal_transaction = NormalTransaction("mainnet")
        >>> normal_transaction.build_transaction("bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", {"bm1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07q3yf5q8": 10000000}, "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> normal_transaction.transaction_raw()
        "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTJjMzkyMjE3NDgzOTA2ZjkwMmU3M2M0YmMxMzI4NjRkZTU4MTUzNzcyZDc5MjY4OTYwOTk4MTYyMjY2NjM0YmUwMTAwMDAwMDAwZmZmZmZmZmYwMmU4MDMwMDAwMDAwMDAwMDAxN2E5MTQ5NzE4OTRjNThkODU5ODFjMTZjMjA1OWQ0MjJiY2RlMGIxNTZkMDQ0ODdhNjI5MDAwMDAwMDAwMDAwMTk3NmE5MTQ2YmNlNjVlNThhNTBiOTc5ODk5MzBlOWE0ZmYxYWMxYTc3NTE1ZWYxODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiAxMjM0MCwgIm4iOiAxLCAic2NyaXB0IjogIjc2YTkxNDZiY2U2NWU1OGE1MGI5Nzk4OTkzMGU5YTRmZjFhYzFhNzc1MTVlZjE4OGFjIn1dLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfdW5zaWduZWQifQ"
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")

        # Encode normal transaction raw
        if self._type == "bytom_normal_signed":
            return clean_transaction_raw(b64encode(str(json.dumps(dict(
                fee=self._fee,
                address=self._address,
                raw=self.raw(),
                hash=self.hash(),
                unsigned_datas=self.unsigned_datas(
                    detail=False
                ),
                signatures=self.signatures(),
                network=self._network,
                type=self._type,
                datas=self._datas
            ))).encode()).decode())
        return clean_transaction_raw(b64encode(str(json.dumps(dict(
            fee=self._fee,
            address=self._address,
            raw=self.raw(),
            hash=self.hash(),
            unsigned_datas=self.unsigned_datas(
                detail=False
            ),
            signatures=[],
            network=self._network,
            type=self._type,
            datas=self._datas
        ))).encode()).decode())


class FundTransaction(Transaction):
    """
    Bytom Fund transaction.

    :param network: Bytom network, defaults to mainnet.
    :type network: str

    :returns: FundTransaction -- Bytom fund transaction instance.

    .. warning::
        Do not forget to build transaction after initialize fund transaction.
    """

    def __init__(self, network: str = config["network"]):
        super().__init__(network)

        self._htlc_address: Optional[str] = None

    def build_transaction(self, address: str, htlc_address: str, amount: Optional[Union[int, float]] = None,
                          max_amount: bool = False, asset: Union[str, AssetNamespace] = config["asset"],
                          fee: Optional[Union[int, float]] = None, unit: str = config["unit"], **kwargs) -> "FundTransaction":
        """
        Build Bytom fund transaction.

        :param address: Bytom sender wallet address.
        :type address: str
        :param htlc_address: Bytom Hash Time Lock Contract (HTLC) address.
        :type htlc_address: str
        :param amount: Bytom amount to fund, default to None.
        :type amount: int, float
        :param max_amount: Bytom maximum amount to fund, default to False.
        :type max_amount: bool
        :param asset: Bytom asset id, defaults to BTM asset.
        :type asset: str, bytom.assets.AssetNamespace
        :param fee: Bytom custom fee, defaults to None.
        :type fee: int, float
        :param unit: Bytom unit, default to NEU.
        :type unit: str

        :returns: FundTransaction -- Bytom fund transaction instance.

        >>> from swap.providers.bytom.transaction import FundTransaction
        >>> fund_transaction = FundTransaction("mainnet")
        >>> fund_transaction.build_transaction(address="bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", htlc_address="bm1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07q3yf5q8", amount=10000000, asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        <swap.providers.bytom.transaction.FundTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not is_address(address, self._network):
            raise AddressError(f"Invalid Bytom sender '{address}' {self._network} address.")
        if not is_address(htlc_address, self._network) or get_address_type(htlc_address) != "p2wsh":
            raise AddressError(f"Invalid Bytom HTLC '{htlc_address}' {self._network} P2WSH address.")
        if unit not in ["BTM", "mBTM", "NEU"]:
            raise UnitError("Invalid Bytom unit, choose only 'BTM', 'mBTM' or 'NEU' units.")

        # Set address, fee and confirmations
        self._address, self._asset, self._htlc_address, self._confirmations = (
            address, (str(asset.ID) if isinstance(asset, AssetNamespace) else asset),
            htlc_address, config["confirmations"]
        )

        maximum_amount: int = get_balance(
            address=self._address, asset=self._asset, network=self._network
        )
        if max_amount:
            self._amount = maximum_amount
        elif amount is None:
            raise ValueError("Amount is None, Set amount or maximum amount set true.")
        else:
            self._amount = (
                amount if unit == "NEU" else
                amount_unit_converter(
                    amount=amount, unit_from=f"{unit}2NEU"
                )
            )
        if maximum_amount < self._amount:
            raise BalanceError(
                "Insufficient spend UTXO's", f"you don't have enough amount. "
                f"You can fund minimum {449001} / maximum {maximum_amount} NEU amount."
            )

        temp_amount: int = self._amount
        if "options" in kwargs.keys():
            options: dict = kwargs.get("options")
            if "address" in options and "percent" in options:
                self._interest += int((self._amount * options["percent"]) / 100)
                temp_amount += self._interest
            if "fee" in options and options["fee"]:
                temp_amount += int(449000 + 60000)

        if fee is not None:
            self._fee = (
                fee if unit == "NEU" else
                amount_unit_converter(
                    amount=fee, unit_from=f"{unit}2NEU"
                )
            )
        elif max_amount or maximum_amount < temp_amount:
            max_amount = True
            self._fee = estimate_transaction_fee(
                address=self._address,
                amount=maximum_amount,
                asset=self._asset,
                confirmations=self._confirmations,
                network=self._network
            )
        else:
            max_amount = False
            if "options" in kwargs.keys():
                options: dict = kwargs.get("options")
                if "fee" in options and options["fee"]:
                    self._amount += int(449000 + 60000)
                if self._interest and "interest" in options and options["interest"]:
                    self._amount += int(self._interest / 2)

            self._fee = estimate_transaction_fee(
                address=self._address,
                amount=int(
                    self._amount if not self._interest else (self._amount + (
                        self._interest if not kwargs["options"]["interest"] else (self._interest / 2)))
                ),
                asset=self._asset,
                confirmations=self._confirmations,
                network=self._network
            )

        fi: int = int(self._fee if not self._interest else (self._fee + (
            self._interest if not kwargs["options"]["interest"] else (self._interest / 2))))
        outputs: list = [control_address(
            asset=self._asset, amount=(self._amount - fi),
            address=self._htlc_address, vapor=False
        )]
        if self._interest:
            outputs.append(control_address(
                asset=self._asset, amount=int(
                    self._interest if not kwargs["options"]["interest"] else (self._interest / 2)
                ), address=kwargs["options"]["address"], vapor=False
            ))
        if self._amount < self._fee:
            raise BalanceError(
                "Insufficient spend UTXO's", f"you don't have enough amount. "
                f"You can fund minimum {449001} NEU amount."
            )

        self._datas.setdefault("address", self._address)
        self._datas.setdefault("htlc_address", self._htlc_address)
        self._datas.setdefault("amount", (self._amount - fi))
        # Build transaction
        self._transaction = build_transaction(
            address=self._address,
            transaction=dict(
                fee=str(amount_unit_converter(
                    amount=self._fee, unit_from="NEU2BTM"
                )),
                confirmations=self._confirmations,
                inputs=[spend_wallet(
                    asset=self._asset,
                    amount=(maximum_amount if max_amount else int(
                        self._amount if not self._interest else (self._amount + (
                            self._interest if not kwargs["options"]["interest"] else (self._interest / 2)))
                    ))
                )],
                outputs=outputs
            ),
            network=self._network
        )

        # Set transaction type
        self._type = "bytom_fund_unsigned"
        return self

    def sign(self, solver: FundSolver) -> "FundTransaction":
        """
        Sign Bytom fund transaction.

        :param solver: Bytom fund solver.
        :type solver: bytom.solver.FundSolver

        :returns: FundTransaction -- Bytom fund transaction instance.

        >>> from swap.providers.bytom.transaction import FundTransaction
        >>> from swap.providers.bytom.solver import FundSolver
        >>> from swap.providers.bytom.wallet import Wallet, DEFAULT_PATH
        >>> sender_wallet = Wallet("mainnet").from_entropy("72fee73846f2d1a5807dc8c953bf79f1").from_path(DEFAULT_PATH)
        >>> fund_solver = FundSolver(sender_wallet.xprivate_key())
        >>> fund_transaction = FundTransaction("mainnet")
        >>> fund_transaction.build_transaction(sender_wallet.address(), "bm1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07q3yf5q8", 10000000, "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> fund_transaction.sign(solver=fund_solver)
        <swap.providers.bytom.transaction.FundTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not isinstance(solver, FundSolver):
            raise TypeError(f"Solver must be Bytom FundSolver, not {type(solver).__name__} type.")

        # Setting sender wallet
        wallet, path, indexes = solver.solve()
        # Clean derivation indexes/path
        wallet.clean_derivation()
        # Signing fund transaction
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

    def transaction_raw(self) -> str:
        """
        Get Bytom fund transaction raw.

        :returns: str -- Bytom fund transaction raw.

        >>> from swap.providers.bytom.transaction import FundTransaction
        >>> fund_transaction = FundTransaction("mainnet")
        >>> fund_transaction.build_transaction("bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "bm1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07q3yf5q8", 10000000, "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> fund_transaction.transaction_raw()
        "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTJjMzkyMjE3NDgzOTA2ZjkwMmU3M2M0YmMxMzI4NjRkZTU4MTUzNzcyZDc5MjY4OTYwOTk4MTYyMjY2NjM0YmUwMTAwMDAwMDAwZmZmZmZmZmYwMmU4MDMwMDAwMDAwMDAwMDAxN2E5MTQ5NzE4OTRjNThkODU5ODFjMTZjMjA1OWQ0MjJiY2RlMGIxNTZkMDQ0ODdhNjI5MDAwMDAwMDAwMDAwMTk3NmE5MTQ2YmNlNjVlNThhNTBiOTc5ODk5MzBlOWE0ZmYxYWMxYTc3NTE1ZWYxODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiAxMjM0MCwgIm4iOiAxLCAic2NyaXB0IjogIjc2YTkxNDZiY2U2NWU1OGE1MGI5Nzk4OTkzMGU5YTRmZjFhYzFhNzc1MTVlZjE4OGFjIn1dLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfdW5zaWduZWQifQ"
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")

        # Encode fund transaction raw
        if self._type == "bytom_fund_signed":
            return clean_transaction_raw(b64encode(str(json.dumps(dict(
                fee=self._fee,
                address=self._address,
                raw=self.raw(),
                hash=self.hash(),
                unsigned_datas=self.unsigned_datas(
                    detail=False
                ),
                signatures=self.signatures(),
                network=self._network,
                type=self._type,
                datas=self._datas
            ))).encode()).decode())
        return clean_transaction_raw(b64encode(str(json.dumps(dict(
            fee=self._fee,
            address=self._address,
            raw=self.raw(),
            hash=self.hash(),
            unsigned_datas=self.unsigned_datas(
                detail=False
            ),
            signatures=[],
            network=self._network,
            type=self._type,
            datas=self._datas
        ))).encode()).decode())


class ClaimTransaction(Transaction):
    """
    Bytom Claim transaction.

    :param network: Bytom network, defaults to mainnet.
    :type network: str

    :returns: ClaimTransaction -- Bytom claim transaction instance.

    .. warning::
        Do not forget to build transaction after initialize claim transaction.
    """

    def __init__(self, network: str = config["network"]):
        super().__init__(network)

        self._transaction_id: Optional[str] = None
        self._transaction_detail: Optional[dict] = None
        self._htlc_utxo: Optional[dict] = None

    def build_transaction(self, address: str, transaction_id: str, amount: Optional[Union[int, float]] = None,
                          max_amount: bool = config["max_amount"], asset: Union[str, AssetNamespace] = config["asset"],
                          fee: Optional[Union[int, float]] = None, unit: str = config["unit"], **kwargs) -> "ClaimTransaction":
        """
        Build Bytom claim transaction.

        :param address: Bytom recipient wallet address.
        :type address: str
        :param transaction_id: Bytom fund transaction id to redeem.
        :type transaction_id: str
        :param amount: Bytom amount to withdraw, default to None.
        :type amount: int, float
        :param max_amount: Bytom maximum amount to withdraw, default to True.
        :type max_amount: bool
        :param asset: Bytom asset id, defaults to BTM asset.
        :type asset: str, bytom.assets.AssetNamespace
        :param fee: Bytom custom fee, defaults to None.
        :type fee: int, float
        :param unit: Bytom unit, default to NEU.
        :type unit: str

        :returns: ClaimTransaction -- Bytom claim transaction instance.

        >>> from swap.providers.bytom.transaction import ClaimTransaction
        >>> claim_transaction = ClaimTransaction("mainnet")
        >>> claim_transaction.build_transaction(address="bm1q3plwvmvy4qhjmp5zffzmk50aagpujt6f5je85p", transaction_id="1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", max_amount=True, asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        <swap.providers.bytom.transaction.ClaimTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not is_address(address, self._network):
            raise AddressError(f"Invalid Bytom recipient '{address}' {self._network} address.")
        if unit not in ["BTM", "mBTM", "NEU"]:
            raise UnitError("Invalid Bytom unit, choose only 'BTM', 'mBTM' or 'NEU' units.")

        # Set address, asset, confirmations and transaction_id
        self._address, self._asset, self._confirmations, self._transaction_id = (
            address, (str(asset.ID) if isinstance(asset, AssetNamespace) else asset),
            config["confirmations"], transaction_id
        )
        # Get transaction
        self._transaction_detail = get_transaction(
            transaction_id=self._transaction_id, network=self._network
        )
        # Find HTLC UTXO
        self._htlc_utxo = find_p2wsh_utxo(transaction=self._transaction_detail)
        if self._htlc_utxo is None:
            raise ValueError("Invalid transaction id, there is no pay to witness script hash (P2WSH) address.")

        if max_amount:
            self._amount = self._htlc_utxo["amount"]
        elif amount is None:
            raise ValueError("Amount is None, Set amount or maximum amount set true.")
        else:
            self._amount = (
                amount if unit == "NEU" else
                amount_unit_converter(
                    amount=amount, unit_from=f"{unit}2NEU"
                )
            )

        if "options" in kwargs.keys():
            options: dict = kwargs.get("options")
            for transaction_output in self._transaction_detail["outputs"]:
                if transaction_output["address"] == options["address"]:
                    self._interest = transaction_output["amount"]

        if fee is None:
            # Estimating transaction fee
            self._fee = estimate_transaction_fee(
                address=self._htlc_utxo["address"], amount=self._amount, asset=self._asset,
                confirmations=self._confirmations, network=self._network
            ) + 60000
        else:
            self._fee = (
                fee if unit == "NEU" else
                amount_unit_converter(
                    amount=fee, unit_from=f"{unit}2NEU"
                )
            )

        if self._amount < self._fee:
            raise BalanceError("Insufficient spend UTXO's",
                               f"minimum you can withdraw {self._fee + 1} NEU amount.")
        if self._htlc_utxo["amount"] < self._amount:
            raise BalanceError("Insufficient spend UTXO's",
                               f"maximum you can withdraw {self._htlc_utxo['amount']} NEU amount.")

        _amount = (self._amount - self._fee) if not self._interest else (self._amount - (self._fee + self._interest))
        outputs: list = [control_address(
            asset=self._asset, amount=_amount,
            address=self._address, vapor=False
        )]
        if self._interest:
            outputs.append(control_address(
                asset=self._asset, amount=self._interest,
                address=kwargs["options"]["address"], vapor=False
            ))

        self._datas.setdefault("address", self._address)
        self._datas.setdefault("htlc_address", self._htlc_utxo["address"])
        self._datas.setdefault("amount", _amount)
        # Build transaction
        self._transaction = build_transaction(
            address=self._htlc_utxo["address"],
            transaction=dict(
                fee=str(amount_unit_converter(
                    amount=self._fee, unit_from="NEU2BTM"
                )),
                confirmations=self._confirmations,
                inputs=[spend_utxo(
                    utxo=self._htlc_utxo["id"]
                )],
                outputs=outputs
            ),
            network=self._network
        )

        # Set transaction type
        self._type = "bytom_claim_unsigned"
        return self

    def sign(self, solver: ClaimSolver) -> "ClaimTransaction":
        """
        Sign Bytom claim transaction.

        :param solver: Bytom claim solver.
        :type solver: bytom.solver.ClaimSolver

        :returns: ClaimTransaction -- Bytom claim transaction instance.

        >>> from swap.providers.bytom.transaction import ClaimTransaction
        >>> from swap.providers.bytom.solver import ClaimSolver
        >>> from swap.providers.bytom.wallet import Wallet, DEFAULT_PATH
        >>> recipient_wallet = Wallet("mainnet").from_entropy("6bc9e3bae5945876931963c2b3a3b040").from_path(DEFAULT_PATH)
        >>> bytecode = "02e8032091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"
        >>> claim_solver = ClaimSolver(recipient_wallet.xprivate_key(), "Hello Meheret!", bytecode=bytecode)
        >>> claim_transaction = ClaimTransaction("mainnet")
        >>> claim_transaction.build_transaction(recipient_wallet.address(), "1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", 10000000, False, "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> claim_transaction.sign(solver=claim_solver)
        <swap.providers.bytom.transaction.ClaimTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not isinstance(solver, ClaimSolver):
            raise TypeError(f"Solver must be Bytom ClaimSolver, not {type(solver).__name__} type.")

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
                signed_data.append(bytearray(secret.encode()).hex())
                signed_data.append(wallet.sign(unsigned_data))
                signed_data.append(str("00"))
                signed_data.append(solver.witness(self._network))
            self._signatures.append(signed_data)
            wallet.clean_derivation()

        # Set transaction type
        self._type = "bytom_claim_signed"
        return self

    def transaction_raw(self) -> str:
        """
        Get Bytom claim transaction raw.

        :returns: str -- Bytom claim transaction raw.

        >>> from swap.providers.bytom.transaction import ClaimTransaction
        >>> claim_transaction = ClaimTransaction("mainnet")
        >>> claim_transaction.build_transaction("bm1q3plwvmvy4qhjmp5zffzmk50aagpujt6f5je85p", "1006a6f537fcc4888c65f6ff4f91818a1c6e19bdd3130f59391c00212c552fbd", 10000000, False, "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> claim_transaction.transaction_raw()
        "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTJjMzkyMjE3NDgzOTA2ZjkwMmU3M2M0YmMxMzI4NjRkZTU4MTUzNzcyZDc5MjY4OTYwOTk4MTYyMjY2NjM0YmUwMTAwMDAwMDAwZmZmZmZmZmYwMmU4MDMwMDAwMDAwMDAwMDAxN2E5MTQ5NzE4OTRjNThkODU5ODFjMTZjMjA1OWQ0MjJiY2RlMGIxNTZkMDQ0ODdhNjI5MDAwMDAwMDAwMDAwMTk3NmE5MTQ2YmNlNjVlNThhNTBiOTc5ODk5MzBlOWE0ZmYxYWMxYTc3NTE1ZWYxODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiAxMjM0MCwgIm4iOiAxLCAic2NyaXB0IjogIjc2YTkxNDZiY2U2NWU1OGE1MGI5Nzk4OTkzMGU5YTRmZjFhYzFhNzc1MTVlZjE4OGFjIn1dLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfdW5zaWduZWQifQ"
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")

        # Encode claim transaction raw
        if self._type == "bytom_claim_signed":
            return clean_transaction_raw(b64encode(str(json.dumps(dict(
                fee=self._fee,
                address=self._htlc_utxo["address"],
                raw=self.raw(),
                hash=self.hash(),
                unsigned_datas=self.unsigned_datas(
                    detail=False
                ),
                signatures=self.signatures(),
                network=self._network,
                type=self._type,
                datas=self._datas
            ))).encode()).decode())
        return clean_transaction_raw(b64encode(str(json.dumps(dict(
            fee=self._fee,
            address=self._htlc_utxo["address"],
            raw=self.raw(),
            hash=self.hash(),
            unsigned_datas=self.unsigned_datas(
                detail=False
            ),
            signatures=[],
            network=self._network,
            type=self._type,
            datas=self._datas
        ))).encode()).decode())


class RefundTransaction(Transaction):
    """
    Bytom Refund transaction.

    :param network: Bytom network, defaults to mainnet.
    :type network: str

    :returns: RefundTransaction -- Bytom refund transaction instance.

    .. warning::
        Do not forget to build transaction after initialize refund transaction.
    """

    def __init__(self, network: str = config["network"]):
        super().__init__(network)

        self._transaction_id: Optional[str] = None
        self._transaction_detail: Optional[dict] = None
        self._htlc_utxo: Optional[dict] = None

    def build_transaction(self, address: str, transaction_id: str, amount: Optional[Union[int, float]] = None,
                          max_amount: bool = config["max_amount"], asset: Union[str, AssetNamespace] = config["asset"],
                          fee: Optional[Union[int, float]] = None, unit: str = config["unit"], **kwargs) -> "RefundTransaction":
        """
        Build Bytom refund transaction.

        :param address: Bytom sender wallet address.
        :type address: str
        :param transaction_id: Bytom fund transaction id to redeem.
        :type transaction_id: str
        :param amount: Bytom amount to withdraw, default to None.
        :type amount: int, float
        :param max_amount: Bytom maximum amount to withdraw, default to True.
        :type max_amount: bool
        :param asset: Bytom asset id, defaults to BTM asset.
        :type asset: str, bytom.assets.AssetNamespace
        :param fee: Bytom custom fee, defaults to None.
        :type fee: int, float
        :param unit: Bytom unit, default to NEU.
        :type unit: str

        :returns: RefundTransaction -- Bytom refund transaction instance.

        >>> from swap.providers.bytom.transaction import RefundTransaction
        >>> refund_transaction = RefundTransaction("mainnet")
        >>> refund_transaction.build_transaction(address="bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", transaction_id="481c00212c552fbdf537fcc88c1006a69bdd3130f593965f6ff4f91818a1c6e1", max_amount=True, asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        <swap.providers.bytom.transaction.RefundTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not is_address(address, self._network):
            raise AddressError(f"Invalid Bytom sender '{address}' {self._network} address.")
        if unit not in ["BTM", "mBTM", "NEU"]:
            raise UnitError("Invalid Bytom unit, choose only 'BTM', 'mBTM' or 'NEU' units.")

        # Set address, fee, confirmations and transaction_id
        self._address, self._asset, self._confirmations, self._transaction_id = (
            address, (str(asset.ID) if isinstance(asset, AssetNamespace) else asset),
            config["confirmations"], transaction_id
        )
        # Get transaction
        self._transaction_detail = get_transaction(
            transaction_id=self._transaction_id, network=self._network
        )
        # Find HTLC UTXO
        self._htlc_utxo = find_p2wsh_utxo(transaction=self._transaction_detail)
        if self._htlc_utxo is None:
            raise ValueError("Invalid transaction id, there is no pay to witness script hash (P2WSH) address.")

        if max_amount:
            self._amount = self._htlc_utxo["amount"]
        elif amount is None:
            raise ValueError("Amount is None, Set amount or maximum amount set true.")
        else:
            self._amount = (
                amount if unit == "NEU" else
                amount_unit_converter(
                    amount=amount, unit_from=f"{unit}2NEU"
                )
            )

        if "options" in kwargs.keys():
            options: dict = kwargs.get("options")
            for transaction_output in self._transaction_detail["outputs"]:
                if transaction_output["address"] == options["address"]:
                    self._interest = transaction_output["amount"]

        if fee is None:
            # Estimating transaction fee
            self._fee = estimate_transaction_fee(
                address=self._htlc_utxo["address"], amount=self._amount, asset=self._asset,
                confirmations=self._confirmations, network=self._network
            ) + 60000
        else:
            self._fee = (
                fee if unit == "NEU" else
                amount_unit_converter(
                    amount=fee, unit_from=f"{unit}2NEU"
                )
            )

        if self._amount < self._fee:
            raise BalanceError("Insufficient spend UTXO's",
                               f"minimum you can refund {self._fee + 1} NEU amount.")
        if self._htlc_utxo["amount"] < self._amount:
            raise BalanceError("Insufficient spend UTXO's",
                               f"maximum you can refund {self._htlc_utxo['amount']} NEU amount.")

        _amount = (self._amount - self._fee) if not self._interest else (self._amount - (self._fee + self._interest))
        outputs: list = [control_address(
            asset=self._asset, amount=_amount,
            address=self._address, vapor=False
        )]
        if self._interest:
            outputs.append(control_address(
                asset=self._asset, amount=self._interest,
                address=kwargs["options"]["address"], vapor=False
            ))

        self._datas.setdefault("address", self._address)
        self._datas.setdefault("htlc_address", self._htlc_utxo["address"])
        self._datas.setdefault("amount", _amount)
        # Build transaction
        self._transaction = build_transaction(
            address=self._htlc_utxo["address"],
            transaction=dict(
                fee=str(amount_unit_converter(
                    amount=self._fee, unit_from="NEU2BTM"
                )),
                confirmations=self._confirmations,
                inputs=[spend_utxo(
                    utxo=self._htlc_utxo["id"]
                )],
                outputs=outputs
            ),
            network=self._network
        )

        # Set transaction type
        self._type = "bytom_refund_unsigned"
        return self

    def sign(self, solver: RefundSolver) -> "RefundTransaction":
        """
        Sign Bytom refund transaction.

        :param solver: Bytom refund solver.
        :type solver: bytom.solver.RefundSolver

        :returns: RefundTransaction -- Bytom refund transaction instance.

        >>> from swap.providers.bytom.transaction import RefundTransaction
        >>> from swap.providers.bytom.solver import RefundSolver
        >>> from swap.providers.bytom.wallet import Wallet, DEFAULT_PATH
        >>> sender_wallet = Wallet("mainnet").from_entropy("72fee73846f2d1a5807dc8c953bf79f1").from_path(DEFAULT_PATH)
        >>> bytecode = "02e8032091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"
        >>> refund_solver = RefundSolver(sender_wallet.xprivate_key(), bytecode=bytecode)
        >>> refund_transaction = RefundTransaction("mainnet")
        >>> refund_transaction.build_transaction(sender_wallet.address(), "481c00212c552fbdf537fcc88c1006a69bdd3130f593965f6ff4f91818a1c6e1", 10000000, False, "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> refund_transaction.sign(solver=refund_solver)
        <swap.providers.bytom.transaction.RefundTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not isinstance(solver, RefundSolver):
            raise TypeError(f"Solver must be Bytom RefundSolver, not {type(solver).__name__} type.")

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
                signed_data.append(wallet.sign(unsigned_data))
                signed_data.append(str("01"))
                signed_data.append(solver.witness(self._network))
            self._signatures.append(signed_data)
            wallet.clean_derivation()

        # Set transaction type
        self._type = "bytom_refund_signed"
        return self

    def transaction_raw(self) -> str:
        """
        Get Bytom refund transaction raw.

        :returns: str -- Bytom refund transaction raw.

        >>> from swap.providers.bytom.transaction import RefundTransaction
        >>> refund_transaction = RefundTransaction("mainnet")
        >>> refund_transaction.build_transaction("bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "481c00212c552fbdf537fcc88c1006a69bdd3130f593965f6ff4f91818a1c6e1", 10000000, False, "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
        >>> refund_transaction.transaction_raw()
        "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTJjMzkyMjE3NDgzOTA2ZjkwMmU3M2M0YmMxMzI4NjRkZTU4MTUzNzcyZDc5MjY4OTYwOTk4MTYyMjY2NjM0YmUwMTAwMDAwMDAwZmZmZmZmZmYwMmU4MDMwMDAwMDAwMDAwMDAxN2E5MTQ5NzE4OTRjNThkODU5ODFjMTZjMjA1OWQ0MjJiY2RlMGIxNTZkMDQ0ODdhNjI5MDAwMDAwMDAwMDAwMTk3NmE5MTQ2YmNlNjVlNThhNTBiOTc5ODk5MzBlOWE0ZmYxYWMxYTc3NTE1ZWYxODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiAxMjM0MCwgIm4iOiAxLCAic2NyaXB0IjogIjc2YTkxNDZiY2U2NWU1OGE1MGI5Nzk4OTkzMGU5YTRmZjFhYzFhNzc1MTVlZjE4OGFjIn1dLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfdW5zaWduZWQifQ"
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")

        # Encode refund transaction raw
        if self._type == "bytom_refund_signed":
            return clean_transaction_raw(b64encode(str(json.dumps(dict(
                fee=self._fee,
                address=self._htlc_utxo["address"],
                raw=self.raw(),
                hash=self.hash(),
                unsigned_datas=self.unsigned_datas(
                    detail=False
                ),
                signatures=self.signatures(),
                network=self._network,
                type=self._type,
                datas=self._datas
            ))).encode()).decode())
        return clean_transaction_raw(b64encode(str(json.dumps(dict(
            fee=self._fee,
            address=self._htlc_utxo["address"],
            hash=self.hash(),
            raw=self.raw(),
            unsigned_datas=self.unsigned_datas(
                detail=False
            ),
            signatures=[],
            network=self._network,
            type=self._type,
            datas=self._datas
        ))).encode()).decode())
