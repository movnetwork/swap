#!/usr/bin/env python3

from binascii import unhexlify
from eth_account.datastructures import SignedTransaction
from web3.datastructures import AttributeDict
from web3.contract import Contract
from web3 import Web3
from web3.types import Wei
from typing import (
    Optional, Union
)
from base64 import b64encode

import json
import sys
import os

from ...exceptions import (
    AddressError, NetworkError, UnitError
)
from ...utils import clean_transaction_raw
from ..config import xinfin as config
from .wallet import Wallet
from .htlc import HTLC
from .rpc import (
    get_web3, get_transaction_receipt
)
from .utils import (
    _AttributeDict, is_network, is_address, to_checksum_address, amount_unit_converter
)
from .solver import (
    NormalSolver, FundSolver, WithdrawSolver, RefundSolver
)


class Transaction:
    """
    XinFin Transaction.

    :param network: XinFin network, defaults to ``mainnet``.
    :type network: str
    :param xrc20: Transaction XRC20 token, default to ``False``.
    :type xrc20: bool
    :param provider: XinFin network provider, defaults to ``http``.
    :type provider: str

    :returns: Transaction -- XinFin transaction instance.

    .. note::
        XinFin has only three networks, ``mainnet``, ``apothem`` and ``testnet``.
    """

    def __init__(self, network: str = config["network"], xrc20: bool = False, provider: str = config["provider"]):

        # Check parameter instances
        if not is_network(network=network):
            raise NetworkError(f"Invalid XinFin '{network}' network",
                               "choose only 'mainnet', 'apothem' or 'testnet' networks.")

        self._xrc20: bool = xrc20
        self._network: str = network
        self.web3: Web3 = get_web3(
            network=network, provider=provider
        )

        self._transaction: Optional[dict] = None
        self._signature: Optional[dict] = None
        self._type: Optional[str] = None
        self._fee: Optional[Wei] = None

    def fee(self, unit: str = config["unit"]) -> Union[Wei, int, float]:
        """
        Get XinFin transaction fee.

        :param unit: XinFin unit, default to ``Wei``.
        :type unit: str

        :returns: Wei, int, float -- XinFin transaction fee.

        >>> from swap.providers.xinfin.htlc import HTLC
        >>> from swap.providers.xinfin.transaction import FundTransaction
        >>> from swap.utils import sha256, get_current_timestamp
        >>> htlc: HTLC = HTLC(contract_address="xdcdE06b10c67765c8C0b9F64E0eF423b45Eb86b8e7", network="testnet")
        >>> htlc.build_htlc(secret_hash=sha256("Hello Meheret!"), recipient_address="xdcf8D43806260CFc6cC79fB408BA1897054667F81C", sender_address="xdc2224caA2235DF8Da3D2016d2AB1137D2d548A232", endtime=get_current_timestamp(plus=3600))
        >>> fund_transaction: FundTransaction = FundTransaction(network="testnet")
        >>> fund_transaction.build_transaction(address="xdc2224caA2235DF8Da3D2016d2AB1137D2d548A232", htlc=htlc, amount=3, unit="XDC")
        >>> fund_transaction.fee(unit="Wei")
        138436
        """

        # Check transaction
        if not self._transaction:
            raise ValueError("Transaction is none, build transaction first.")

        if unit not in ["XDC", "Gwei", "Wei"]:
            raise UnitError(f"Invalid XinFin '{unit}' unit", "choose only 'XDC', 'Gwei' or 'Wei' units.")
        return self._fee if unit == "Wei" else \
            amount_unit_converter(amount=self._fee, unit_from=f"Wei2{unit}")

    def hash(self) -> Optional[str]:
        """
        Get XinFin transaction hash.

        :returns: str -- XinFin transaction hash.

        >>> from swap.providers.xinfin.transaction import WithdrawTransaction
        >>> from swap.providers.xinfin.solver import WithdrawSolver
        >>> withdraw_transaction: WithdrawTransaction = WithdrawTransaction(network="testnet")
        >>> withdraw_transaction.build_transaction(transaction_hash="0x0d4c93546aa3e5e476455931a63f1a97a2624e3b516e3fd8e3a582cb20aaeef9", secret_key="Hello Meheret!", address="xdcf8D43806260CFc6cC79fB408BA1897054667F81C", contract_address="xdcdE06b10c67765c8C0b9F64E0eF423b45Eb86b8e7")
        >>> withdraw_solver: WithdrawSolver = WithdrawSolver(xprivate_key="xprv9s21ZrQH143K4Kpce43z5guPyxLrFoc2i8aQAq835Zzp4Rt7i6nZaMCnVSDyHT6MnmJJGKHMrCUqaYpGojrug1ZN5qQDdShQffmkyv5xyUR", path="m/44'/550'/0'/0/0")
        >>> withdraw_transaction.sign(solver=withdraw_solver)
        >>> withdraw_transaction.hash()
        "0xe8e8738c791385738661573ad4de63dd81b77d240b6138ca476ea8cdcbb29a21"
        """

        # Check transaction
        if not self._transaction:
            raise ValueError("Transaction is none, build transaction first.")

        return self._signature["hash"] if self._signature else None

    def json(self) -> dict:
        """
        Get XinFin transaction fee.

        :returns: Wei, int, float -- XinFin transaction fee.

        >>> from swap.providers.xinfin.htlc import HTLC
        >>> from swap.providers.xinfin.transaction import FundTransaction
        >>> from swap.utils import sha256, get_current_timestamp
        >>> htlc: HTLC = HTLC(contract_address="xdcdE06b10c67765c8C0b9F64E0eF423b45Eb86b8e7", network="testnet")
        >>> htlc.build_htlc(secret_hash=sha256("Hello Meheret!"), recipient_address="xdcf8D43806260CFc6cC79fB408BA1897054667F81C", sender_address="xdc2224caA2235DF8Da3D2016d2AB1137D2d548A232", endtime=get_current_timestamp(plus=3600))
        >>> fund_transaction: FundTransaction = FundTransaction(network="testnet")
        >>> fund_transaction.build_transaction(address="xdc2224caA2235DF8Da3D2016d2AB1137D2d548A232", htlc=htlc, amount=3, unit="XDC")
        >>> fund_transaction.json()
        {'chainId': 1337, 'from': '0x2224caA2235DF8Da3D2016d2AB1137D2d548A232', 'value': 3000000000000000000, 'nonce': 2, 'gas': 138436, 'gasPrice': 20000000000, 'to': '0xdE06b10c67765c8C0b9F64E0eF423b45Eb86b8e7', 'data': '0xf4fd30623a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb000000000000000000000000f8d43806260cfc6cc79fb408ba1897054667f81c0000000000000000000000002224caa2235df8da3d2016d2ab1137d2d548a2320000000000000000000000000000000000000000000000000000000060e000d3'}
        """

        # Check transaction
        if not self._transaction:
            raise ValueError("Transaction is none, build transaction first.")

        return self._transaction

    def raw(self) -> Optional[str]:
        """
        Get XinFin transaction hash.

        :returns: str -- XinFin transaction hash.

        >>> from swap.providers.xinfin.transaction import RefundTransaction
        >>> from swap.providers.xinfin.solver import RefundSolver
        >>> refund_transaction: RefundTransaction = RefundTransaction(network="testnet")
        >>> refund_transaction.build_transaction(transaction_hash="0x0d4c93546aa3e5e476455931a63f1a97a2624e3b516e3fd8e3a582cb20aaeef9", address="xdc2224caA2235DF8Da3D2016d2AB1137D2d548A232", contract_address="xdcdE06b10c67765c8C0b9F64E0eF423b45Eb86b8e7")
        >>> refund_solver: RefundSolver = RefundSolver(xprivate_key="xprv9s21ZrQH143K3Y3pdbkbjreZQ9RVmqTLhRgf86uZyCJk2ou36YdUJt5frjwihGWmV1fQEDioiGZXWXUbHLy3kQf5xmhvhp8dZ2tfn6tgGUj", path="m/44'/550'/0'/0/0")
        >>> refund_transaction.sign(solver=refund_solver)
        >>> refund_transaction.hash()
        "0xf88a028504a817c80082e76094de06b10c67765c8c0b9f64e0ef423b45eb86b8e780a47249fbb61909575c436a0eabe6caa72d4feb2c4aeceef586fe94ca82f36ce9c20efda4b4820a95a05ed63e467fb541b728dc7253ea4f9c4f2ada130ef78ffaba8de9c5e92536ce42a034ba97172cb8726cdfbaba14b10a817a0c4c4bccc6d8f2a27fc1711752ed2ab2"
        """

        # Check transaction
        if not self._transaction:
            raise ValueError("Transaction is none, build transaction first.")

        return self._signature["rawTransaction"] if self._signature else None

    def type(self) -> str:
        """
        Get XinFin transaction hash.

        :returns: str -- XinFin transaction hash.

        >>> from swap.providers.xinfin.transaction import WithdrawTransaction
        >>> from swap.providers.xinfin.solver import WithdrawSolver
        >>> withdraw_transaction: WithdrawTransaction = WithdrawTransaction(network="testnet")
        >>> withdraw_transaction.build_transaction(transaction_hash="0x0d4c93546aa3e5e476455931a63f1a97a2624e3b516e3fd8e3a582cb20aaeef9", secret_key="Hello Meheret!", address="xdcf8D43806260CFc6cC79fB408BA1897054667F81C", contract_address="xdcdE06b10c67765c8C0b9F64E0eF423b45Eb86b8e7")
        >>> withdraw_transaction.type()
        "xinfin_withdraw_unsigned"
        """

        # Check transaction
        if not self._transaction:
            raise ValueError("Transaction is none, build transaction first.")

        return self._type

    def signature(self) -> dict:
        """
        Get XinFin transaction hash.

        :returns: str -- XinFin transaction hash.

        >>> from swap.providers.xinfin.transaction import RefundTransaction
        >>> from swap.providers.xinfin.solver import RefundSolver
        >>> refund_transaction: RefundTransaction = RefundTransaction(network="testnet")
        >>> refund_transaction.build_transaction(transaction_hash="0x0d4c93546aa3e5e476455931a63f1a97a2624e3b516e3fd8e3a582cb20aaeef9", address="xdc2224caA2235DF8Da3D2016d2AB1137D2d548A232", contract_address="xdcdE06b10c67765c8C0b9F64E0eF423b45Eb86b8e7")
        >>> refund_solver: RefundSolver = RefundSolver(xprivate_key="xprv9s21ZrQH143K3Y3pdbkbjreZQ9RVmqTLhRgf86uZyCJk2ou36YdUJt5frjwihGWmV1fQEDioiGZXWXUbHLy3kQf5xmhvhp8dZ2tfn6tgGUj", path="m/44'/550'/0'/0/0")
        >>> refund_transaction.sign(solver=refund_solver)
        >>> refund_transaction.signature()
        {'hash': '0x90449ab8e3736feae4980554bb129b408f88d0003e569022cf8e00817cc2a7d9', 'rawTransaction': '0xf88a028504a817c80082e76094de06b10c67765c8c0b9f64e0ef423b45eb86b8e780a47249fbb61909575c436a0eabe6caa72d4feb2c4aeceef586fe94ca82f36ce9c20efda4b4820a95a05ed63e467fb541b728dc7253ea4f9c4f2ada130ef78ffaba8de9c5e92536ce42a034ba97172cb8726cdfbaba14b10a817a0c4c4bccc6d8f2a27fc1711752ed2ab2', 'r': 42895942847608608192932856733711858695420995837709512084644654454168196927042, 's': 23849944468865388317715121201379699989753020274517556595896033163737398323890, 'v': 2709}
        """

        # Check transaction
        if not self._transaction:
            raise ValueError("Transaction is none, build transaction first.")

        return self._signature

    def transaction_raw(self) -> str:
        """
        Get XinFin fund transaction raw.

        :returns: str -- XinFin fund transaction raw.

        >>> from swap.providers.xinfin.htlc import HTLC
        >>> from swap.providers.xinfin.transaction import FundTransaction
        >>> from swap.utils import sha256, get_current_timestamp
        >>> htlc: HTLC = HTLC(contract_address="xdcdE06b10c67765c8C0b9F64E0eF423b45Eb86b8e7", network="testnet")
        >>> htlc.build_htlc(secret_hash=sha256("Hello Meheret!"), recipient_address="xdcf8D43806260CFc6cC79fB408BA1897054667F81C", sender_address="xdc2224caA2235DF8Da3D2016d2AB1137D2d548A232", endtime=get_current_timestamp(plus=3600))
        >>> fund_transaction: FundTransaction = FundTransaction(network="testnet")
        >>> fund_transaction.build_transaction(address="xdc2224caA2235DF8Da3D2016d2AB1137D2d548A232", htlc=htlc, amount=3, unit="XDC")
        >>> fund_transaction.transaction_raw()
        "eyJmZWUiOiAxMzg0MzYsICJ0eXBlIjogInhpbmZpbl9mdW5kX3Vuc2lnbmVkIiwgInRyYW5zYWN0aW9uIjogeyJjaGFpbklkIjogMTMzNywgImZyb20iOiAiMHgyMjI0Y2FBMjIzNURGOERhM0QyMDE2ZDJBQjExMzdEMmQ1NDhBMjMyIiwgInZhbHVlIjogMzAwMDAwMDAwMDAwMDAwMDAwMCwgIm5vbmNlIjogMiwgImdhcyI6IDEzODQzNiwgImdhc1ByaWNlIjogMjAwMDAwMDAwMDAsICJ0byI6ICIweGRFMDZiMTBjNjc3NjVjOEMwYjlGNjRFMGVGNDIzYjQ1RWI4NmI4ZTciLCAiZGF0YSI6ICIweGY0ZmQzMDYyM2EyNmRhODJlYWQxNWE4MDUzM2EwMjY5NjY1NmIxNGI1ZGJmZDg0ZWIxNDc5MGYyZTFiZTVlOWU0NTgyMGVlYjAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMGY4ZDQzODA2MjYwY2ZjNmNjNzlmYjQwOGJhMTg5NzA1NDY2N2Y4MWMwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAyMjI0Y2FhMjIzNWRmOGRhM2QyMDE2ZDJhYjExMzdkMmQ1NDhhMjMyMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDA2MGUwMDBkMyJ9LCAic2lnbmF0dXJlIjogbnVsbCwgIm5ldHdvcmsiOiAidGVzdG5ldCJ9"
        """

        # Check transaction
        if not self._transaction:
            raise ValueError("Transaction is none, build transaction first.")

        return clean_transaction_raw(b64encode(str(json.dumps(dict(
            fee=self._fee,
            type=self._type,
            transaction=self._transaction,
            signature=self._signature,
            network=self._network,
            xrc20=self._xrc20
        ))).encode()).decode())


class NormalTransaction(Transaction):
    """
    XinFin Normal transaction.

    :param network: XinFin network, defaults to ``mainnet``.
    :type network: str
    :param xrc20: Normal transaction XRC20 token, default to ``False``.
    :type xrc20: bool
    :param provider: XinFin network provider, defaults to ``http``.
    :type provider: str

    :returns: NormalTransaction -- XinFin normal transaction instance.

    .. warning::
        Do not forget to build transaction after initialize fund transaction.
    """

    def __init__(self, network: str = config["network"], xrc20: bool = False, provider: str = config["provider"]):
        super().__init__(
            network=network, xrc20=xrc20, provider=provider
        )

    def build_transaction(self, address: str, recipient: dict, token_address: Optional[str] = None, unit: str = config["unit"]) -> "NormalTransaction":
        """
        Build XinFin normal transaction.

        :param address: XinFin sender address.
        :type address: str
        :param recipient: Recipients XinFin address and amount.
        :type recipient: dict
        :param token_address: XinFin XRC20 token address, default to ``None``.
        :type token_address: bool
        :param unit: XinFin unit, default to ``Wei``.
        :type unit: str

        :returns: NormalTransaction -- XinFin normal transaction instance.

        >>> from swap.providers.xinfin.transaction import NormalTransaction
        >>> normal_transaction: NormalTransaction = NormalTransaction(network="testnet")
        >>> normal_transaction.build_transaction(address="xdc2224caA2235DF8Da3D2016d2AB1137D2d548A232", recipient={"xdcf8D43806260CFc6cC79fB408BA1897054667F81C": 100_000_000})
        <swap.providers.xinfin.transaction.FundTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not is_address(address=address):
            raise AddressError(f"Invalid XinFin sender '{address}' address.")
        if unit not in ["XDC", "Gwei", "Wei"]:
            raise UnitError("Invalid XinFin unit, choose only 'XDC', 'Gwei' or 'Wei' units.")
        if len(recipient.items()) > 1:
            raise ValueError("You can't broadcast for multiple addresses on this version, only for one address.")

        # Set address, fee and confirmations
        recipient_address, amount = list(recipient.items())[0]
        self._address, self._token_address, self._amount = (
            address, token_address, Wei(
                amount if unit == "Wei" else amount_unit_converter(amount=amount, unit_from=f"{unit}2Wei")
            ) if not self._xrc20 else amount
        )

        if self._xrc20:
            # Get current working directory path (like linux or unix path).
            cwd: str = os.path.dirname(sys.modules[__package__].__file__)
            with open(f"{cwd}/contracts/libs/xrc20.json", "r") as xrc20_json_file:
                xrc20_contract_data: dict = json.loads(xrc20_json_file.read())["xrc20.sol:XRC20"]
                xrc20_json_file.close()

            xrc20_contract: Contract = self.web3.eth.contract(
                address=to_checksum_address(address=token_address, prefix="0x"), abi=xrc20_contract_data["abi"]
            )
            transfer_function = xrc20_contract.functions.transfer(
                to_checksum_address(address=recipient_address, prefix="0x"), self._amount
            )
            self._fee = transfer_function.estimateGas({
                "from": to_checksum_address(address=address, prefix="0x"),
                "value": Wei(0),
                "nonce": self.web3.eth.get_transaction_count(
                    to_checksum_address(address=address, prefix="0x")
                ),
                "gasPrice": self.web3.eth.gas_price
            })

            self._transaction = transfer_function.buildTransaction({
                "from": to_checksum_address(address=address, prefix="0x"),
                "value": Wei(0),
                "nonce": self.web3.eth.get_transaction_count(
                    to_checksum_address(address=address, prefix="0x")
                ),
                "gas": self._fee,
                "gasPrice": self.web3.eth.gas_price
            })
        else:
            self._transaction = {
                "from": to_checksum_address(address=address, prefix="0x"),
                "to": to_checksum_address(address=recipient_address, prefix="0x"),
                "value": self._amount,
                "nonce": self.web3.eth.get_transaction_count(
                    to_checksum_address(address=address, prefix="0x")
                ),
                "gasPrice": self.web3.eth.gas_price
            }
            self._fee = self.web3.eth.estimateGas(self._transaction)
            self._transaction.setdefault("gas", self._fee)

        self._type = "xinfin_xrc20_normal_unsigned" if self._xrc20 else "xinfin_normal_unsigned"
        return self

    def sign(self, solver: NormalSolver) -> "NormalTransaction":
        """
        Sign XinFin normal transaction.

        :param solver: XinFin normal solver.
        :type solver: xinfin.solver.NormalSolver

        :returns: NormalTransaction -- XinFin normal transaction instance.

        >>> from swap.providers.xinfin.transaction import NormalTransaction
        >>> from swap.providers.xinfin.solver import NormalSolver
        >>> normal_transaction: NormalTransaction = NormalTransaction(network="testnet")
        >>> normal_transaction.build_transaction(address="xdc2224caA2235DF8Da3D2016d2AB1137D2d548A232", recipient={"xdcf8D43806260CFc6cC79fB408BA1897054667F81C": 100_000_000})
        >>> normal_solver: NormalSolver = NormalSolver(xprivate_key="xprv9s21ZrQH143K3Y3pdbkbjreZQ9RVmqTLhRgf86uZyCJk2ou36YdUJt5frjwihGWmV1fQEDioiGZXWXUbHLy3kQf5xmhvhp8dZ2tfn6tgGUj", address=0)
        >>> normal_transaction.sign(solver=normal_solver)
        <swap.providers.xinfin.transaction.FundTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not isinstance(solver, NormalSolver):
            raise TypeError(f"Solver must be XinFin NormalSolver, not {type(solver).__name__} type.")

        wallet: Wallet = solver.solve()
        signed_normal_transaction: SignedTransaction = self.web3.eth.account.sign_transaction(
            transaction_dict=self._transaction,
            private_key=wallet.private_key()
        )

        self._signature = dict(
            hash=signed_normal_transaction["hash"].hex(),
            rawTransaction=signed_normal_transaction["rawTransaction"].hex(),
            r=signed_normal_transaction["r"],
            s=signed_normal_transaction["s"],
            v=signed_normal_transaction["v"]
        )
        self._type = "xinfin_xrc20_normal_signed" if self._xrc20 else "xinfin_normal_signed"
        return self


class FundTransaction(Transaction):
    """
    XinFin Fund transaction.

    :param network: XinFin network, defaults to ``mainnet``.
    :type network: str
    :param xrc20: Fund transaction XRC20 token, default to ``False``.
    :type xrc20: bool
    :param provider: XinFin network provider, defaults to ``http``.
    :type provider: str

    :returns: FundTransaction -- XinFin fund transaction instance.

    .. warning::
        Do not forget to build transaction after initialize fund transaction.
    """

    def __init__(self, network: str = config["network"], xrc20: bool = False, provider: str = config["provider"]):
        super().__init__(
            network=network, xrc20=xrc20, provider=provider
        )

    def build_transaction(self, address: str, htlc: HTLC, amount: Union[Wei, int, float],
                          unit: str = config["unit"]) -> "FundTransaction":
        """
        Build XinFin fund transaction.

        :param htlc: XinFin HTLC instance.
        :type htlc: xinfin.htlc.HTLC
        :param address: XinFin sender address.
        :type address: str
        :param amount: XinFin amount or XRC20 amount.
        :type amount: Wei, int, float
        :param unit: XinFin unit, default to ``Wei``.
        :type unit: str

        :returns: FundTransaction -- XinFin fund transaction instance.

        >>> from swap.providers.xinfin.htlc import HTLC
        >>> from swap.providers.xinfin.transaction import FundTransaction
        >>> from swap.utils import sha256, get_current_timestamp
        >>> htlc: HTLC = HTLC(contract_address="xdcdE06b10c67765c8C0b9F64E0eF423b45Eb86b8e7", network="testnet")
        >>> htlc.build_htlc(secret_hash=sha256("Hello Meheret!"), recipient_address="xdcf8D43806260CFc6cC79fB408BA1897054667F81C", sender_address="xdc2224caA2235DF8Da3D2016d2AB1137D2d548A232", endtime=get_current_timestamp(plus=3600))
        >>> fund_transaction: FundTransaction = FundTransaction(network="testnet")
        >>> fund_transaction.build_transaction(address="xdc2224caA2235DF8Da3D2016d2AB1137D2d548A232", htlc=htlc, amount=3, unit="XDC")
        <swap.providers.xinfin.transaction.FundTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not is_address(address=address):
            raise AddressError(f"Invalid XinFin sender '{address}' address.")
        if not isinstance(htlc, HTLC):
            raise TypeError("Invalid XinFin HTLC instance, only takes XinFin HTLC class")
        if to_checksum_address(address=address, prefix="xdc") != htlc.agreements["sender_address"]:
            raise AddressError(f"Wrong XinFin sender '{address}' address",
                               "address must be match with HTLC agreements sender address.")
        if unit not in ["XDC", "Gwei", "Wei"]:
            raise UnitError("Invalid XinFin unit, choose only 'XDC', 'Gwei' or 'Wei' units.")

        _amount: Wei = Wei(
            amount if unit == "Wei" else amount_unit_converter(amount=amount, unit_from=f"{unit}2Wei")
        ) if not self._xrc20 else amount

        htlc_contract: Contract = self.web3.eth.contract(
            address=htlc.contract_address(prefix="0x"), abi=htlc.abi()
        )

        if self._xrc20:
            htlc_fund_function = htlc_contract.functions.fund(
                to_checksum_address(htlc.agreements["token_address"], prefix="0x"),  # Token address
                unhexlify(htlc.agreements["secret_hash"]),  # Secret Hash
                to_checksum_address(htlc.agreements["recipient_address"], prefix="0x"),  # Recipient Address
                to_checksum_address(htlc.agreements["sender_address"], prefix="0x"),  # Sender Address
                htlc.agreements["endtime"]["timestamp"],  # Locktime Seconds
                _amount  # Amount
            )
        else:
            htlc_fund_function = htlc_contract.functions.fund(
                unhexlify(htlc.agreements["secret_hash"]),  # Secret Hash
                to_checksum_address(htlc.agreements["recipient_address"], prefix="0x"),  # Recipient Address
                to_checksum_address(htlc.agreements["sender_address"], prefix="0x"),  # Sender Address
                htlc.agreements["endtime"]["timestamp"]  # Locktime Seconds
            )

        self._fee = htlc_fund_function.estimateGas({
            "from": to_checksum_address(address=address, prefix="0x"),
            "value": _amount if not self._xrc20 else Wei(0),
            "nonce": self.web3.eth.get_transaction_count(
                to_checksum_address(address=address, prefix="0x")
            ),
            "gasPrice": self.web3.eth.gas_price
        })

        self._transaction = htlc_fund_function.buildTransaction({
            "from": to_checksum_address(address=address, prefix="0x"),
            "value": _amount if not self._xrc20 else Wei(0),
            "nonce": self.web3.eth.get_transaction_count(
                to_checksum_address(address=address, prefix="0x")
            ),
            "gas": self._fee,
            "gasPrice": self.web3.eth.gas_price
        })
        self._type = "xinfin_xrc20_fund_unsigned" if self._xrc20 else "xinfin_fund_unsigned"
        return self

    def sign(self, solver: FundSolver) -> "FundTransaction":
        """
        Sign XinFin fund transaction.

        :param solver: XinFin fund solver.
        :type solver: xinfin.solver.FundSolver

        :returns: FundTransaction -- XinFin fund transaction instance.

        >>> from swap.providers.xinfin.htlc import HTLC
        >>> from swap.providers.xinfin.transaction import FundTransaction
        >>> from swap.providers.xinfin.solver import FundSolver
        >>> from swap.utils import sha256, get_current_timestamp
        >>> htlc: HTLC = HTLC(contract_address="xdcdE06b10c67765c8C0b9F64E0eF423b45Eb86b8e7", network="testnet")
        >>> htlc.build_htlc(secret_hash=sha256("Hello Meheret!"), recipient_address="xdcf8D43806260CFc6cC79fB408BA1897054667F81C", sender_address="xdc2224caA2235DF8Da3D2016d2AB1137D2d548A232", endtime=get_current_timestamp(plus=3600))
        >>> fund_transaction: FundTransaction = FundTransaction(network="testnet")
        >>> fund_transaction.build_transaction(address="xdc2224caA2235DF8Da3D2016d2AB1137D2d548A232", htlc=htlc, amount=3, unit="XDC")
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="xprv9s21ZrQH143K3Y3pdbkbjreZQ9RVmqTLhRgf86uZyCJk2ou36YdUJt5frjwihGWmV1fQEDioiGZXWXUbHLy3kQf5xmhvhp8dZ2tfn6tgGUj", path="m/44'/550'/0'/0/0")
        >>> fund_transaction.sign(solver=fund_solver)
        <swap.providers.xinfin.transaction.FundTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not isinstance(solver, FundSolver):
            raise TypeError(f"Solver must be XinFin FundSolver, not {type(solver).__name__} type.")

        wallet: Wallet = solver.solve()
        signed_fund_transaction: SignedTransaction = self.web3.eth.account.sign_transaction(
            transaction_dict=self._transaction,
            private_key=wallet.private_key()
        )

        self._signature = dict(
            hash=signed_fund_transaction["hash"].hex(),
            rawTransaction=signed_fund_transaction["rawTransaction"].hex(),
            r=signed_fund_transaction["r"],
            s=signed_fund_transaction["s"],
            v=signed_fund_transaction["v"]
        )
        self._type = "xinfin_xrc20_fund_signed" if self._xrc20 else "xinfin_fund_signed"
        return self


class WithdrawTransaction(Transaction):
    """
    XinFin Withdraw transaction.

    :param network: XinFin network, defaults to ``mainnet``.
    :type network: str
    :param xrc20: Withdraw transaction XRC20 token, default to ``False``.
    :type xrc20: bool
    :param provider: XinFin network provider, defaults to ``http``.
    :type provider: str

    :returns: WithdrawTransaction -- XinFin withdraw transaction instance.

    .. warning::
        Do not forget to build transaction after initialize withdraw transaction.
    """

    def __init__(self, network: str = config["network"], xrc20: bool = False, provider: str = config["provider"]):
        super().__init__(
            network=network, xrc20=xrc20, provider=provider
        )

    def build_transaction(self, transaction_hash: str, address: str, secret_key: str,
                          contract_address: Optional[str] = None) -> "WithdrawTransaction":
        """
        Build XinFin withdraw transaction.

        :param transaction_hash: XinFin HTLC funded transaction hash.
        :type transaction_hash: str
        :param address: XinFin recipient address.
        :type address: str
        :param secret_key: Secret password/passphrase.
        :type secret_key: str
        :param contract_address: XinFin HTLC contract address, defaults to ``None``.
        :type contract_address: str

        :returns: WithdrawTransaction -- XinFin withdraw transaction instance.

        >>> from swap.providers.xinfin.transaction import WithdrawTransaction
        >>> withdraw_transaction: WithdrawTransaction = WithdrawTransaction(network="testnet")
        >>> withdraw_transaction.build_transaction(transaction_hash="0x0d4c93546aa3e5e476455931a63f1a97a2624e3b516e3fd8e3a582cb20aaeef9", secret_key="Hello Meheret!", address="xdcf8D43806260CFc6cC79fB408BA1897054667F81C", contract_address="xdcdE06b10c67765c8C0b9F64E0eF423b45Eb86b8e7")
        <swap.providers.xinfin.transaction.WithdrawTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not is_address(address=address):
            raise AddressError(f"Invalid XinFin recipient '{address}' address.")
        if contract_address and not is_address(address=contract_address):
            raise AddressError(f"Invalid XinFin HTLC contract '{contract_address}' address.")

        htlc: HTLC = HTLC(
            contract_address=contract_address, network=self._network, xrc20=self._xrc20
        )
        htlc_contract: Contract = self.web3.eth.contract(
            address=self.web3.toChecksumAddress(htlc.contract_address(prefix="0x")), abi=htlc.abi()
        )

        transaction_receipt: AttributeDict = _AttributeDict(get_transaction_receipt(
            transaction_hash=transaction_hash, network=self._network
        )).__attribute_dict__()
        log_fund: AttributeDict = htlc_contract.events.log_fund().processLog(
            log=transaction_receipt["logs"][2 if self._xrc20 else 0]
        )

        locked_contract_id: str = log_fund["args"]["locked_contract_id"]
        htlc_fund_function = htlc_contract.functions.withdraw(
            locked_contract_id,  # Locked Contract ID
            secret_key  # Secret Key
        )

        self._fee = htlc_fund_function.estimateGas({
            "from": to_checksum_address(address=address, prefix="0x"),
            "value": Wei(0),
            "nonce": self.web3.eth.get_transaction_count(
                to_checksum_address(address=address, prefix="0x")
            ),
            "gasPrice": self.web3.eth.gas_price
        })

        self._transaction = htlc_fund_function.buildTransaction({
            "from": to_checksum_address(address=address, prefix="0x"),
            "value": Wei(0),
            "nonce": self.web3.eth.get_transaction_count(
                to_checksum_address(address=address, prefix="0x")
            ),
            "gas": self._fee,
            "gasPrice": self.web3.eth.gas_price
        })
        self._type = "xinfin_xrc20_withdraw_unsigned" if self._xrc20 else "xinfin_withdraw_unsigned"
        return self

    def sign(self, solver: WithdrawSolver) -> "WithdrawTransaction":
        """
        Sign XinFin withdraw transaction.

        :param solver: XinFin withdraw solver.
        :type solver: xinfin.solver.WithdrawSolver

        :returns: WithdrawTransaction -- XinFin withdraw transaction instance.

        >>> from swap.providers.xinfin.transaction import WithdrawTransaction
        >>> from swap.providers.xinfin.solver import WithdrawSolver
        >>> withdraw_transaction: WithdrawTransaction = WithdrawTransaction(network="testnet")
        >>> withdraw_transaction.build_transaction(transaction_hash="0x0d4c93546aa3e5e476455931a63f1a97a2624e3b516e3fd8e3a582cb20aaeef9", secret_key="Hello Meheret!", address="xdcf8D43806260CFc6cC79fB408BA1897054667F81C", contract_address="xdcdE06b10c67765c8C0b9F64E0eF423b45Eb86b8e7")
        >>> withdraw_solver: WithdrawSolver = WithdrawSolver(xprivate_key="xprv9s21ZrQH143K4Kpce43z5guPyxLrFoc2i8aQAq835Zzp4Rt7i6nZaMCnVSDyHT6MnmJJGKHMrCUqaYpGojrug1ZN5qQDdShQffmkyv5xyUR", path="m/44'/550'/0'/0/0")
        >>> withdraw_transaction.sign(solver=withdraw_solver)
        <swap.providers.xinfin.transaction.WithdrawTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not isinstance(solver, WithdrawSolver):
            raise TypeError(f"Solver must be XinFin WithdrawSolver, not {type(solver).__name__} type.")

        wallet: Wallet = solver.solve()
        signed_withdraw_transaction: SignedTransaction = self.web3.eth.account.sign_transaction(
            transaction_dict=self._transaction,
            private_key=wallet.private_key()
        )

        self._signature = dict(
            hash=signed_withdraw_transaction["hash"].hex(),
            rawTransaction=signed_withdraw_transaction["rawTransaction"].hex(),
            r=signed_withdraw_transaction["r"],
            s=signed_withdraw_transaction["s"],
            v=signed_withdraw_transaction["v"]
        )
        self._type = "xinfin_xrc20_withdraw_signed" if self._xrc20 else "xinfin_withdraw_signed"
        return self


class RefundTransaction(Transaction):
    """
    XinFin Refund transaction.

    :param network: XinFin network, defaults to ``mainnet``.
    :type network: str
    :param xrc20: Refund transaction XRC20 token, default to ``False``.
    :type xrc20: bool
    :param provider: XinFin network provider, defaults to ``http``.
    :type provider: str

    :returns: RefundTransaction -- XinFin refund transaction instance.

    .. warning::
        Do not forget to build transaction after initialize refund transaction.
    """

    def __init__(self, network: str = config["network"], xrc20: bool = False, provider: str = config["provider"]):
        super().__init__(
            network=network, xrc20=xrc20, provider=provider
        )

    def build_transaction(self, transaction_hash: str, address: str,
                          contract_address: Optional[str] = None) -> "RefundTransaction":
        """
        Build XinFin refund transaction.

        :param transaction_hash: XinFin HTLC funded transaction hash.
        :type transaction_hash: str
        :param address: XinFin sender address.
        :type address: str
        :param contract_address: XinFin HTLC contract address, defaults to ``None``.
        :type contract_address: str

        :returns: RefundTransaction -- XinFin refund transaction instance.

        >>> from swap.providers.xinfin.transaction import RefundTransaction
        >>> refund_transaction: RefundTransaction = RefundTransaction(network="testnet")
        >>> refund_transaction.build_transaction(transaction_hash="0x0d4c93546aa3e5e476455931a63f1a97a2624e3b516e3fd8e3a582cb20aaeef9", address="xdc2224caA2235DF8Da3D2016d2AB1137D2d548A232", contract_address="xdcdE06b10c67765c8C0b9F64E0eF423b45Eb86b8e7")
        <swap.providers.xinfin.transaction.RefundTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not is_address(address=address):
            raise AddressError(f"Invalid XinFin sender '{address}' address.")
        if contract_address and not is_address(address=contract_address):
            raise AddressError(f"Invalid XinFin HTLC contract '{contract_address}' address.")

        htlc: HTLC = HTLC(
            contract_address=contract_address, network=self._network, xrc20=self._xrc20
        )
        htlc_contract: Contract = self.web3.eth.contract(
            address=self.web3.toChecksumAddress(htlc.contract_address(prefix="0x")), abi=htlc.abi()
        )

        transaction_receipt: AttributeDict = _AttributeDict(get_transaction_receipt(
            transaction_hash=transaction_hash, network=self._network
        )).__attribute_dict__()
        log_fund: AttributeDict = htlc_contract.events.log_fund().processLog(
            log=transaction_receipt["logs"][2 if self._xrc20 else 0]
        )

        locked_contract_id: str = log_fund["args"]["locked_contract_id"]
        htlc_refund_function = htlc_contract.functions.refund(
            locked_contract_id  # Locked Contract ID
        )

        self._fee = htlc_refund_function.estimateGas({
            "from": to_checksum_address(address=address, prefix="0x"),
            "value": Wei(0),
            "nonce": self.web3.eth.get_transaction_count(
                to_checksum_address(address=address, prefix="0x")
            ),
            "gasPrice": self.web3.eth.gas_price
        })

        self._transaction = htlc_refund_function.buildTransaction({
            "from": to_checksum_address(address=address, prefix="0x"),
            "value": Wei(0),
            "nonce": self.web3.eth.get_transaction_count(
                to_checksum_address(address=address, prefix="0x")
            ),
            "gas": self._fee,
            "gasPrice": self.web3.eth.gas_price
        })
        self._type = "xinfin_xrc20_refund_unsigned" if self._xrc20 else "xinfin_refund_unsigned"
        return self

    def sign(self, solver: RefundSolver) -> "RefundTransaction":
        """
        Sign XinFin refund transaction.

        :param solver: XinFin refund solver.
        :type solver: xinfin.solver.RefundSolver

        :returns: RefundTransaction -- XinFin refund transaction instance.

        >>> from swap.providers.xinfin.transaction import RefundTransaction
        >>> from swap.providers.xinfin.solver import RefundSolver
        >>> refund_transaction: RefundTransaction = RefundTransaction(network="testnet")
        >>> refund_transaction.build_transaction(transaction_hash="0x0d4c93546aa3e5e476455931a63f1a97a2624e3b516e3fd8e3a582cb20aaeef9", address="xdc2224caA2235DF8Da3D2016d2AB1137D2d548A232", contract_address="xdcdE06b10c67765c8C0b9F64E0eF423b45Eb86b8e7")
        >>> refund_solver: RefundSolver = RefundSolver(xprivate_key="xprv9s21ZrQH143K3Y3pdbkbjreZQ9RVmqTLhRgf86uZyCJk2ou36YdUJt5frjwihGWmV1fQEDioiGZXWXUbHLy3kQf5xmhvhp8dZ2tfn6tgGUj", path="m/44'/550'/0'/0/0")
        >>> refund_transaction.sign(solver=refund_solver)
        <swap.providers.xinfin.transaction.RefundTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not isinstance(solver, RefundSolver):
            raise TypeError(f"Solver must be XinFin RefundSolver, not {type(solver).__name__} type.")

        wallet: Wallet = solver.solve()
        signed_refund_transaction: SignedTransaction = self.web3.eth.account.sign_transaction(
            transaction_dict=self._transaction,
            private_key=wallet.private_key()
        )

        self._signature = dict(
            hash=signed_refund_transaction["hash"].hex(),
            rawTransaction=signed_refund_transaction["rawTransaction"].hex(),
            r=signed_refund_transaction["r"],
            s=signed_refund_transaction["s"],
            v=signed_refund_transaction["v"]
        )
        self._type = "xinfin_xrc20_refund_signed" if self._xrc20 else "xinfin_refund_signed"
        return self
