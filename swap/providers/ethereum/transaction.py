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
from ..config import ethereum as config
from .wallet import Wallet
from .htlc import HTLC
from .rpc import get_web3
from .utils import (
    is_network, is_address, to_checksum_address, amount_unit_converter
)
from .solver import (
    NormalSolver, FundSolver, WithdrawSolver, RefundSolver
)


class Transaction:
    """
    Ethereum Transaction.

    :param network: Ethereum network, defaults to ``mainnet``.
    :type network: str
    :param erc20: Transaction ERC20 token, default to ``False``.
    :type erc20: bool
    :param provider: Ethereum network provider, defaults to ``http``.
    :type provider: str
    :param token: Infura API endpoint token, defaults to ``4414fea5f7454211956b1627621450b4``.
    :type token: str

    :returns: Transaction -- Ethereum transaction instance.

    .. note::
        Ethereum has only five networks, ``mainnet``, ``ropsten``, ``kovan``, ``rinkeby`` and ``testnet``.
    """

    def __init__(self, network: str = config["network"], erc20: bool = False,
                 provider: str = config["provider"], token: Optional[str] = None):

        # Check parameter instances
        if not is_network(network=network):
            raise NetworkError(f"Invalid Ethereum '{network}' network",
                               "choose only 'mainnet', 'ropsten', 'kovan', 'rinkeby' or 'testnet' networks.")

        self._erc20: bool = erc20
        self._network: str = network
        self.web3: Web3 = get_web3(
            network=network, provider=provider, token=token
        )

        self._transaction: Optional[dict] = None
        self._signature: Optional[dict] = None
        self._type: Optional[str] = None
        self._fee: Optional[Wei] = None

    def fee(self, unit: str = config["unit"]) -> Union[Wei, int, float]:
        """
        Get Ethereum transaction fee.

        :param unit: Ethereum unit, default to ``Wei``.
        :type unit: str

        :returns: Wei, int, float -- Ethereum transaction fee.

        >>> from swap.providers.ethereum.htlc import HTLC
        >>> from swap.providers.ethereum.transaction import FundTransaction
        >>> from swap.utils import sha256, get_current_timestamp
        >>> htlc: HTLC = HTLC(network="mainnet")
        >>> htlc.build_htlc(secret_hash=sha256("Hello Meheret!"), recipient_address="0xd77E0d2Eef905cfB39c3C4b952Ed278d58f96E1f", sender_address="0x69e04fe16c9A6A83076B3c2dc4b4Bc21b5d9A20C", endtime=get_current_timestamp(plus=3600))
        >>> fund_transaction: FundTransaction = FundTransaction(network="mainnet")
        >>> fund_transaction.build_transaction(address="0x69e04fe16c9A6A83076B3c2dc4b4Bc21b5d9A20C", htlc=htlc, amount=100_000_000)
        >>> fund_transaction.fee(unit="Wei")
        1532774
        """

        # Check transaction
        if not self._transaction:
            raise ValueError("Transaction is none, build transaction first.")

        if unit not in ["Ether", "Gwei", "Wei"]:
            raise UnitError(f"Invalid Ethereum '{unit}' unit", "choose only 'Ether', 'Gwei' or 'Wei' units.")
        return self._fee if unit == "Wei" else \
            amount_unit_converter(amount=self._fee, unit_from=f"Wei2{unit}")

    def hash(self) -> Optional[str]:
        """
        Get Ethereum transaction hash.

        :returns: str -- Ethereum transaction hash.

        >>> from swap.providers.ethereum.transaction import WithdrawTransaction
        >>> from swap.providers.ethereum.solver import WithdrawSolver
        >>> withdraw_transaction: WithdrawTransaction = WithdrawTransaction(network="mainnet")
        >>> withdraw_transaction.build_transaction(transaction_hash="0xe49ff507739f8d916ae2c9fd51dd63764658ffa42a5288a49d93bc70a933edc4", secret_key="Hello Meheret!", address="0x69e04fe16c9A6A83076B3c2dc4b4Bc21b5d9A20C", contract_address="0x67324d402ffc103d061dAfA9096ff639f0676378")
        >>> withdraw_solver: WithdrawSolver = WithdrawSolver(xprivate_key="xprv9s21ZrQH143K3Y3pdbkbjreZQ9RVmqTLhRgf86uZyCJk2ou36YdUJt5frjwihGWmV1fQEDioiGZXWXUbHLy3kQf5xmhvhp8dZ2tfn6tgGUj", address=1)
        >>> withdraw_transaction.sign(solver=withdraw_solver)
        >>> withdraw_transaction.hash()
        "0x9bbf83e56fea4cd9d23e000e8273551ba28317e4d3c311a49be919b305feb711"
        """

        # Check transaction
        if not self._transaction:
            raise ValueError("Transaction is none, build transaction first.")

        return self._signature["hash"] if self._signature else None

    def json(self) -> dict:
        """
        Get Ethereum transaction fee.

        :returns: Wei, int, float -- Ethereum transaction fee.

        >>> from swap.providers.ethereum.htlc import HTLC
        >>> from swap.providers.ethereum.transaction import FundTransaction
        >>> from swap.utils import sha256, get_current_timestamp
        >>> htlc: HTLC = HTLC(network="mainnet")
        >>> htlc.build_htlc(secret_hash=sha256("Hello Meheret!"), recipient_address="0xd77E0d2Eef905cfB39c3C4b952Ed278d58f96E1f", sender_address="0x69e04fe16c9A6A83076B3c2dc4b4Bc21b5d9A20C", endtime=get_current_timestamp(plus=3600))
        >>> fund_transaction: FundTransaction = FundTransaction(network="mainnet")
        >>> fund_transaction.build_transaction(address="0x69e04fe16c9A6A83076B3c2dc4b4Bc21b5d9A20C", htlc=htlc, amount=100_000_000)
        >>> fund_transaction.json()
        {'chainId': 1337, 'from': '0x69e04fe16c9A6A83076B3c2dc4b4Bc21b5d9A20C', 'value': 3000000000000000000, 'nonce': 0, 'gas': 22488, 'gasPrice': 20000000000, 'to': '0xeaEaC81da5E386E8Ca4De1e64d40a10E468A5b40', 'data': '0xf4fd30623a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb000000000000000000000000d77e0d2eef905cfb39c3c4b952ed278d58f96e1f00000000000000000000000069e04fe16c9a6a83076b3c2dc4b4bc21b5d9a20c0000000000000000000000000000000000000000000000000000000060ce0ab6'}
        """

        # Check transaction
        if not self._transaction:
            raise ValueError("Transaction is none, build transaction first.")

        return self._transaction

    def raw(self) -> Optional[str]:
        """
        Get Ethereum transaction hash.

        :returns: str -- Ethereum transaction hash.

        >>> from swap.providers.ethereum.transaction import RefundTransaction
        >>> from swap.providers.ethereum.solver import RefundSolver
        >>> refund_transaction: RefundTransaction = RefundTransaction(network="mainnet")
        >>> refund_transaction.build_transaction(transaction_hash="0xe49ff507739f8d916ae2c9fd51dd63764658ffa42a5288a49d93bc70a933edc4", address="0x69e04fe16c9A6A83076B3c2dc4b4Bc21b5d9A20C", contract_address="0x67324d402ffc103d061dAfA9096ff639f0676378")
        >>> refund_solver: RefundSolver = RefundSolver(xprivate_key="xprv9s21ZrQH143K3Y3pdbkbjreZQ9RVmqTLhRgf86uZyCJk2ou36YdUJt5frjwihGWmV1fQEDioiGZXWXUbHLy3kQf5xmhvhp8dZ2tfn6tgGUj", address=0)
        >>> refund_transaction.sign(solver=refund_solver)
        >>> refund_transaction.hash()
        "0x9bbf83e56fea4cd9d23e000e8273551ba28317e4d3c311a49be919b305feb711"
        """

        # Check transaction
        if not self._transaction:
            raise ValueError("Transaction is none, build transaction first.")

        return self._signature["rawTransaction"] if self._signature else None

    def type(self) -> str:
        """
        Get Ethereum transaction hash.

        :returns: str -- Ethereum transaction hash.

        >>> from swap.providers.ethereum.transaction import WithdrawTransaction
        >>> from swap.providers.ethereum.solver import WithdrawSolver
        >>> withdraw_transaction: WithdrawTransaction = WithdrawTransaction(network="mainnet")
        >>> withdraw_transaction.build_transaction(transaction_hash="0xe49ff507739f8d916ae2c9fd51dd63764658ffa42a5288a49d93bc70a933edc4", secret_key="Hello Meheret!", address="0x69e04fe16c9A6A83076B3c2dc4b4Bc21b5d9A20C", contract_address="0x67324d402ffc103d061dAfA9096ff639f0676378")
        >>> withdraw_transaction.type()
        "ethereum_withdraw_unsigned"
        """

        # Check transaction
        if not self._transaction:
            raise ValueError("Transaction is none, build transaction first.")

        return self._type

    def signature(self) -> dict:
        """
        Get Ethereum transaction hash.

        :returns: str -- Ethereum transaction hash.

        >>> from swap.providers.ethereum.transaction import RefundTransaction
        >>> from swap.providers.ethereum.solver import RefundSolver
        >>> refund_transaction: RefundTransaction = RefundTransaction(network="mainnet")
        >>> refund_transaction.build_transaction(transaction_hash="0xe49ff507739f8d916ae2c9fd51dd63764658ffa42a5288a49d93bc70a933edc4", address="0x69e04fe16c9A6A83076B3c2dc4b4Bc21b5d9A20C", contract_address="0x67324d402ffc103d061dAfA9096ff639f0676378")
        >>> refund_solver: RefundSolver = RefundSolver(xprivate_key="xprv9s21ZrQH143K3Y3pdbkbjreZQ9RVmqTLhRgf86uZyCJk2ou36YdUJt5frjwihGWmV1fQEDioiGZXWXUbHLy3kQf5xmhvhp8dZ2tfn6tgGUj", address=0)
        >>> refund_transaction.sign(solver=refund_solver)
        >>> refund_transaction.signature()
        {'hash': '0x120241e6e89b54d90dc3a3f73d6353f83818c3d404c991d3b74691f000583396', 'rawTransaction': '0xf8f4018504a817c80083021cd094eaeac81da5e386e8ca4de1e64d40a10e468a5b408829a2241af62c0000b884f4fd30623a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb000000000000000000000000d77e0d2eef905cfb39c3c4b952ed278d58f96e1f00000000000000000000000069e04fe16c9a6a83076b3c2dc4b4bc21b5d9a20c0000000000000000000000000000000000000000000000000000000060ce40e8820a95a05d598fe47b96ef59b2a5b62a2793f499f1abce31938dc494b496b20969656cf4a063d515ee2a84d323a7f232eae4196e2e449a010eef52e6125b639b0b52fd2d2f', 'r': 42223337416619984402386667584480976881779168344975798352755076934920973937908, 's': 45155461792159514883067068644058913853180508583163102385805265017506142956847, 'v': 2709}
        """

        # Check transaction
        if not self._transaction:
            raise ValueError("Transaction is none, build transaction first.")

        return self._signature

    def transaction_raw(self) -> str:
        """
        Get Ethereum fund transaction raw.

        :returns: str -- Ethereum fund transaction raw.

        >>> from swap.providers.ethereum.htlc import HTLC
        >>> from swap.providers.ethereum.transaction import FundTransaction
        >>> from swap.utils import sha256, get_current_timestamp
        >>> htlc: HTLC = HTLC(network="mainnet")
        >>> htlc.build_htlc(secret_hash=sha256("Hello Meheret!"), recipient_address="0xd77E0d2Eef905cfB39c3C4b952Ed278d58f96E1f", sender_address="0x69e04fe16c9A6A83076B3c2dc4b4Bc21b5d9A20C", endtime=get_current_timestamp(plus=3600))
        >>> fund_transaction: FundTransaction = FundTransaction(network="mainnet")
        >>> fund_transaction.build_transaction(address="0x69e04fe16c9A6A83076B3c2dc4b4Bc21b5d9A20C", htlc=htlc, amount=100_000_000)
        >>> fund_transaction.transaction_raw()
        "eyJmZWUiOiAxMzg0NDgsICJ0cmFuc2FjdGlvbiI6IHsiY2hhaW5JZCI6IDEzMzcsICJmcm9tIjogIjB4NjllMDRmZTE2YzlBNkE4MzA3NkIzYzJkYzRiNEJjMjFiNWQ5QTIwQyIsICJ2YWx1ZSI6IDMwMDAwMDAwMDAwMDAwMDAwMDAsICJub25jZSI6IDEsICJnYXMiOiAxMzg0NDgsICJnYXNQcmljZSI6IDIwMDAwMDAwMDAwLCAidG8iOiAiMHhlYUVhQzgxZGE1RTM4NkU4Q2E0RGUxZTY0ZDQwYTEwRTQ2OEE1YjQwIiwgImRhdGEiOiAiMHhmNGZkMzA2MjNhMjZkYTgyZWFkMTVhODA1MzNhMDI2OTY2NTZiMTRiNWRiZmQ4NGViMTQ3OTBmMmUxYmU1ZTllNDU4MjBlZWIwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDBkNzdlMGQyZWVmOTA1Y2ZiMzljM2M0Yjk1MmVkMjc4ZDU4Zjk2ZTFmMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwNjllMDRmZTE2YzlhNmE4MzA3NmIzYzJkYzRiNGJjMjFiNWQ5YTIwYzAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwNjBjZTQwZTgifSwgInNpZ25hdHVyZSI6IG51bGwsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJldGhlcmV1bV9mdW5kX3Vuc2lnbmVkIn0"
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
            erc20=self._erc20
        ))).encode()).decode())


class NormalTransaction(Transaction):
    """
    Ethereum Normal transaction.

    :param network: Ethereum network, defaults to ``mainnet``.
    :type network: str
    :param erc20: Normal transaction ERC20 token, default to ``False``.
    :type erc20: bool
    :param provider: Ethereum network provider, defaults to ``http``.
    :type provider: str
    :param token: Infura API endpoint token, defaults to ``4414fea5f7454211956b1627621450b4``.
    :type token: str

    :returns: NormalTransaction -- Ethereum normal transaction instance.

    .. warning::
        Do not forget to build transaction after initialize fund transaction.
    """

    def __init__(self, network: str = config["network"], erc20: bool = False,
                 provider: str = config["provider"], token: Optional[str] = None):
        super().__init__(
            network=network, erc20=erc20, provider=provider, token=token
        )

    def build_transaction(self, address: str, recipient: dict, token_address: Optional[str] = None, unit: str = config["unit"]) -> "NormalTransaction":
        """
        Build Ethereum normal transaction.

        :param address: Ethereum sender address.
        :type address: str
        :param recipient: Recipients Ethereum address and amount.
        :type recipient: dict
        :param token_address: Ethereum ERC20 token address, default to ``None``.
        :type token_address: bool
        :param unit: Ethereum unit, default to ``Wei``.
        :type unit: str

        :returns: NormalTransaction -- Ethereum normal transaction instance.

        >>> from swap.providers.ethereum.transaction import NormalTransaction
        >>> normal_transaction: NormalTransaction = NormalTransaction(network="testnet")
        >>> normal_transaction.build_transaction(address="0x69e04fe16c9A6A83076B3c2dc4b4Bc21b5d9A20C", recipient={"0x1954C47a5D75bdDA53578CEe5D549bf84b8c6B94": 100_000_000})
        <swap.providers.ethereum.transaction.FundTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not is_address(address=address):
            raise AddressError(f"Invalid Ethereum sender '{address}' address.")
        if unit not in ["Ether", "Gwei", "Wei"]:
            raise UnitError("Invalid Ethereum unit, choose only 'Ether', 'Gwei' or 'Wei' units.")
        if len(recipient.items()) > 1:
            raise ValueError("You can't broadcast for multiple addresses on this version, only for one address.")

        # Set address, fee and confirmations
        recipient_address, amount = list(recipient.items())[0]
        self._address, self._token_address, self._amount = (
            address, token_address, Wei(
                amount if unit == "Wei" else amount_unit_converter(amount=amount, unit_from=f"{unit}2Wei")
            ) if not self._erc20 else amount
        )

        if self._erc20:
            # Get current working directory path (like linux or unix path).
            cwd: str = os.path.dirname(sys.modules[__package__].__file__)
            with open(f"{cwd}/contracts/libs/erc20.json", "r") as erc20_json_file:
                erc20_contract_data: dict = json.loads(erc20_json_file.read())["erc20.sol:ERC20"]
                erc20_json_file.close()

            erc20_contract: Contract = self.web3.eth.contract(
                address=to_checksum_address(address=token_address), abi=erc20_contract_data["abi"]
            )
            transfer_function = erc20_contract.functions.transfer(
                to_checksum_address(address=recipient_address), self._amount
            )
            self._fee = transfer_function.estimateGas({
                "from": to_checksum_address(address=address),
                "value": Wei(0),
                "nonce": self.web3.eth.get_transaction_count(
                    to_checksum_address(address=address)
                ),
                "gasPrice": self.web3.eth.gas_price
            })

            self._transaction = transfer_function.buildTransaction({
                "from": to_checksum_address(address=address),
                "value": Wei(0),
                "nonce": self.web3.eth.get_transaction_count(
                    to_checksum_address(address=address)
                ),
                "gas": self._fee,
                "gasPrice": self.web3.eth.gas_price
            })
        else:
            self._transaction = {
                "from": to_checksum_address(address=address),
                "to": to_checksum_address(address=recipient_address),
                "value": self._amount,
                "nonce": self.web3.eth.get_transaction_count(
                    to_checksum_address(address=address)
                ),
                "gasPrice": self.web3.eth.gas_price
            }
            self._fee = self.web3.eth.estimateGas(self._transaction)
            self._transaction.setdefault("gas", self._fee)

        self._type = "ethereum_erc20_normal_unsigned" if self._erc20 else "ethereum_normal_unsigned"
        return self

    def sign(self, solver: NormalSolver) -> "NormalTransaction":
        """
        Sign Ethereum normal transaction.

        :param solver: Ethereum normal solver.
        :type solver: ethereum.solver.NormalSolver

        :returns: NormalTransaction -- Ethereum normal transaction instance.

        >>> from swap.providers.ethereum.transaction import NormalTransaction
        >>> from swap.providers.ethereum.solver import NormalSolver
        >>> normal_transaction: NormalTransaction = NormalTransaction(network="testnet")
        >>> normal_transaction.build_transaction(address="0x69e04fe16c9A6A83076B3c2dc4b4Bc21b5d9A20C", recipient={"0x1954C47a5D75bdDA53578CEe5D549bf84b8c6B94": 100_000_000})
        >>> normal_solver: NormalSolver = NormalSolver(xprivate_key="xprv9s21ZrQH143K3Y3pdbkbjreZQ9RVmqTLhRgf86uZyCJk2ou36YdUJt5frjwihGWmV1fQEDioiGZXWXUbHLy3kQf5xmhvhp8dZ2tfn6tgGUj", address=0)
        >>> normal_transaction.sign(solver=normal_solver)
        <swap.providers.ethereum.transaction.FundTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not isinstance(solver, NormalSolver):
            raise TypeError(f"Solver must be Ethereum NormalSolver, not {type(solver).__name__} type.")

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
        self._type = "ethereum_erc20_normal_signed" if self._erc20 else "ethereum_normal_signed"
        return self


class FundTransaction(Transaction):
    """
    Ethereum Fund transaction.

    :param network: Ethereum network, defaults to ``mainnet``.
    :type network: str
    :param erc20: Fund transaction ERC20 token, default to ``False``.
    :type erc20: bool
    :param provider: Ethereum network provider, defaults to ``http``.
    :type provider: str
    :param token: Infura API endpoint token, defaults to ``4414fea5f7454211956b1627621450b4``.
    :type token: str

    :returns: FundTransaction -- Ethereum fund transaction instance.

    .. warning::
        Do not forget to build transaction after initialize fund transaction.
    """

    def __init__(self, network: str = config["network"], erc20: bool = False,
                 provider: str = config["provider"], token: Optional[str] = None):
        super().__init__(
            network=network, erc20=erc20, provider=provider, token=token
        )

    def build_transaction(self, address: str, htlc: HTLC, amount: Union[Wei, int],
                          unit: str = config["unit"]) -> "FundTransaction":
        """
        Build Ethereum fund transaction.

        :param address: Ethereum sender address.
        :type address: str
        :param htlc: Ethereum HTLC instance.
        :type htlc: ethereum.htlc.HTLC
        :param amount: Ethereum amount or ERC20 amount.
        :type amount: Wei, int, float
        :param unit: Ethereum unit, default to ``Wei``.
        :type unit: str

        :returns: FundTransaction -- Ethereum fund transaction instance.

        >>> from swap.providers.ethereum.htlc import HTLC
        >>> from swap.providers.ethereum.transaction import FundTransaction
        >>> from swap.utils import sha256, get_current_timestamp
        >>> htlc: HTLC = HTLC(network="mainnet", erc20=False)
        >>> htlc.build_htlc(secret_hash=sha256("Hello Meheret!"), recipient_address="0xd77E0d2Eef905cfB39c3C4b952Ed278d58f96E1f", sender_address="0x69e04fe16c9A6A83076B3c2dc4b4Bc21b5d9A20C", endtime=get_current_timestamp(plus=3600))
        >>> fund_transaction: FundTransaction = FundTransaction(network="mainnet")
        >>> fund_transaction.build_transaction(address="0x69e04fe16c9A6A83076B3c2dc4b4Bc21b5d9A20C", htlc=htlc, amount=100_000_000)
        <swap.providers.ethereum.transaction.FundTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not is_address(address=address):
            raise AddressError(f"Invalid Ethereum sender '{address}' address.")
        if not isinstance(htlc, HTLC):
            raise TypeError("Invalid Ethereum HTLC instance, only takes Ethereum HTLC class")
        if to_checksum_address(address=address) != htlc.agreements["sender_address"]:
            raise AddressError(f"Wrong Ethereum sender '{address}' address",
                               "address must be match with HTLC agreements sender address.")
        if unit not in ["Ether", "Gwei", "Wei"]:
            raise UnitError("Invalid Ethereum unit, choose only 'Ether', 'Gwei' or 'Wei' units.")

        _amount: Union[Wei, int, float] = Wei(
            amount if unit == "Wei" else amount_unit_converter(amount=amount, unit_from=f"{unit}2Wei")
        ) if not self._erc20 else amount

        htlc_contract: Contract = self.web3.eth.contract(
            address=htlc.contract_address(), abi=htlc.abi()
        )

        if self._erc20:
            htlc_fund_function = htlc_contract.functions.fund(
                htlc.agreements["token_address"],  # Token address
                unhexlify(htlc.agreements["secret_hash"]),  # Secret Hash
                htlc.agreements["recipient_address"],  # Recipient Address
                htlc.agreements["sender_address"],  # Sender Address
                htlc.agreements["endtime"]["timestamp"],  # Locktime Seconds
                _amount  # Amount
            )
        else:
            htlc_fund_function = htlc_contract.functions.fund(
                unhexlify(htlc.agreements["secret_hash"]),  # Secret Hash
                htlc.agreements["recipient_address"],  # Recipient Address
                htlc.agreements["sender_address"],  # Sender Address
                htlc.agreements["endtime"]["timestamp"]  # Locktime Seconds
            )

        self._fee = htlc_fund_function.estimateGas({
            "from": to_checksum_address(address=address),
            "value": _amount if not self._erc20 else Wei(0),
            "nonce": self.web3.eth.get_transaction_count(
                to_checksum_address(address=address)
            ),
            "gasPrice": self.web3.eth.gas_price
        })

        self._transaction = htlc_fund_function.buildTransaction({
            "from": to_checksum_address(address=address),
            "value": _amount if not self._erc20 else Wei(0),
            "nonce": self.web3.eth.get_transaction_count(
                to_checksum_address(address=address)
            ),
            "gas": self._fee,
            "gasPrice": self.web3.eth.gas_price
        })
        self._type = "ethereum_erc20_fund_unsigned" if self._erc20 else "ethereum_fund_unsigned"
        return self

    def sign(self, solver: FundSolver) -> "FundTransaction":
        """
        Sign Ethereum fund transaction.

        :param solver: Ethereum fund solver.
        :type solver: ethereum.solver.FundSolver

        :returns: FundTransaction -- Ethereum fund transaction instance.

        >>> from swap.providers.ethereum.htlc import HTLC
        >>> from swap.providers.ethereum.transaction import FundTransaction
        >>> from swap.providers.ethereum.solver import FundSolver
        >>> from swap.utils import sha256, get_current_timestamp
        >>> htlc: HTLC = HTLC(network="mainnet")
        >>> htlc.build_htlc(secret_hash=sha256("Hello Meheret!"), recipient_address="0xd77E0d2Eef905cfB39c3C4b952Ed278d58f96E1f", sender_address="0x69e04fe16c9A6A83076B3c2dc4b4Bc21b5d9A20C", endtime=get_current_timestamp(plus=3600))
        >>> fund_transaction: FundTransaction = FundTransaction(network="mainnet")
        >>> fund_transaction.build_transaction(address="0x69e04fe16c9A6A83076B3c2dc4b4Bc21b5d9A20C", htlc=htlc, amount=100_000_000)
        >>> fund_solver: FundSolver = FundSolver(xprivate_key="xprv9s21ZrQH143K3Y3pdbkbjreZQ9RVmqTLhRgf86uZyCJk2ou36YdUJt5frjwihGWmV1fQEDioiGZXWXUbHLy3kQf5xmhvhp8dZ2tfn6tgGUj", address=0)
        >>> fund_transaction.sign(solver=fund_solver)
        <swap.providers.ethereum.transaction.FundTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not isinstance(solver, FundSolver):
            raise TypeError(f"Solver must be Ethereum FundSolver, not {type(solver).__name__} type.")

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
        self._type = "ethereum_erc20_fund_signed" if self._erc20 else "ethereum_fund_signed"
        return self


class WithdrawTransaction(Transaction):
    """
    Ethereum Withdraw transaction.

    :param network: Ethereum network, defaults to ``mainnet``.
    :type network: str
    :param erc20: Withdraw transaction ERC20 token, default to ``False``.
    :type erc20: bool
    :param provider: Ethereum network provider, defaults to ``http``.
    :type provider: str
    :param token: Infura API endpoint token, defaults to ``4414fea5f7454211956b1627621450b4``.
    :type token: str

    :returns: WithdrawTransaction -- Ethereum withdraw transaction instance.

    .. warning::
        Do not forget to build transaction after initialize withdraw transaction.
    """

    def __init__(self, network: str = config["network"], erc20: bool = False, provider: str = config["provider"],
                 token: Optional[str] = None):
        super().__init__(
            network=network, erc20=erc20, provider=provider, token=token
        )

    def build_transaction(self, transaction_hash: str, address: str, secret_key: str,
                          contract_address: Optional[str] = None) -> "WithdrawTransaction":
        """
        Build Ethereum withdraw transaction.

        :param transaction_hash: Ethereum HTLC funded transaction hash.
        :type transaction_hash: str
        :param address: Ethereum recipient address.
        :type address: str
        :param secret_key: Secret password/passphrase.
        :type secret_key: str
        :param contract_address: Ethereum HTLC contract address, defaults to ``None``.
        :type contract_address: str

        :returns: WithdrawTransaction -- Ethereum withdraw transaction instance.

        >>> from swap.providers.ethereum.transaction import WithdrawTransaction
        >>> withdraw_transaction: WithdrawTransaction = WithdrawTransaction(network="mainnet")
        >>> withdraw_transaction.build_transaction(transaction_hash="0xe49ff507739f8d916ae2c9fd51dd63764658ffa42a5288a49d93bc70a933edc4", secret_key="Hello Meheret!", address="0x69e04fe16c9A6A83076B3c2dc4b4Bc21b5d9A20C", contract_address="0x67324d402ffc103d061dAfA9096ff639f0676378")
        <swap.providers.ethereum.transaction.WithdrawTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not is_address(address=address):
            raise AddressError(f"Invalid Ethereum recipient '{address}' address.")
        if contract_address and not is_address(address=contract_address):
            raise AddressError(f"Invalid Ethereum HTLC contract '{contract_address}' address.")

        htlc: HTLC = HTLC(
            contract_address=contract_address, network=self._network, erc20=self._erc20
        )
        htlc_contract: Contract = self.web3.eth.contract(
            address=htlc.contract_address(), abi=htlc.abi()
        )

        transaction_receipt: AttributeDict = self.web3.eth.get_transaction_receipt(transaction_hash)
        log_fund: AttributeDict = htlc_contract.events.log_fund().processLog(
            log=transaction_receipt["logs"][2 if self._erc20 else 0]
        )

        locked_contract_id: str = log_fund["args"]["locked_contract_id"]
        htlc_withdraw_function = htlc_contract.functions.withdraw(
            locked_contract_id,  # Locked Contract ID
            secret_key  # Secret Key
        )

        self._fee = htlc_withdraw_function.estimateGas({
            "from": to_checksum_address(address=address),
            "value": Wei(0),
            "nonce": self.web3.eth.get_transaction_count(
                to_checksum_address(address=address)
            ),
            "gasPrice": self.web3.eth.gas_price
        })

        self._transaction = htlc_withdraw_function.buildTransaction({
            "from": to_checksum_address(address=address),
            "value": Wei(0),
            "nonce": self.web3.eth.get_transaction_count(
                to_checksum_address(address=address)
            ),
            "gas": self._fee,
            "gasPrice": self.web3.eth.gas_price
        })
        self._type = "ethereum_erc20_withdraw_unsigned" if self._erc20 else "ethereum_withdraw_unsigned"
        return self

    def sign(self, solver: WithdrawSolver) -> "WithdrawTransaction":
        """
        Sign Ethereum withdraw transaction.

        :param solver: Ethereum withdraw solver.
        :type solver: ethereum.solver.WithdrawSolver

        :returns: WithdrawTransaction -- Ethereum withdraw transaction instance.

        >>> from swap.providers.ethereum.transaction import WithdrawTransaction
        >>> from swap.providers.ethereum.solver import WithdrawSolver
        >>> withdraw_transaction: WithdrawTransaction = WithdrawTransaction(network="mainnet")
        >>> withdraw_transaction.build_transaction(transaction_hash="0xe49ff507739f8d916ae2c9fd51dd63764658ffa42a5288a49d93bc70a933edc4", secret_key="Hello Meheret!", address="0x69e04fe16c9A6A83076B3c2dc4b4Bc21b5d9A20C", contract_address="0x67324d402ffc103d061dAfA9096ff639f0676378")
        >>> withdraw_solver: WithdrawSolver = WithdrawSolver(xprivate_key="xprv9s21ZrQH143K3Y3pdbkbjreZQ9RVmqTLhRgf86uZyCJk2ou36YdUJt5frjwihGWmV1fQEDioiGZXWXUbHLy3kQf5xmhvhp8dZ2tfn6tgGUj", address=1)
        >>> withdraw_transaction.sign(solver=withdraw_solver)
        <swap.providers.ethereum.transaction.WithdrawTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not isinstance(solver, WithdrawSolver):
            raise TypeError(f"Solver must be Ethereum WithdrawSolver, not {type(solver).__name__} type.")

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
        self._type = "ethereum_erc20_withdraw_signed" if self._erc20 else "ethereum_withdraw_signed"
        return self


class RefundTransaction(Transaction):
    """
    Ethereum Refund transaction.

    :param network: Ethereum network, defaults to ``mainnet``.
    :type network: str
    :param erc20: Refund transaction ERC20 token, default to ``False``.
    :type erc20: bool
    :param provider: Ethereum network provider, defaults to ``http``.
    :type provider: str
    :param token: Infura API endpoint token, defaults to ``4414fea5f7454211956b1627621450b4``.
    :type token: str

    :returns: RefundTransaction -- Ethereum refund transaction instance.

    .. warning::
        Do not forget to build transaction after initialize refund transaction.
    """

    def __init__(self, network: str = config["network"], erc20: bool = False,
                 provider: str = config["provider"], token: Optional[str] = None):
        super().__init__(
            network=network, erc20=erc20, provider=provider, token=token
        )

    def build_transaction(self, transaction_hash: str, address: str,
                          contract_address: Optional[str] = None) -> "RefundTransaction":
        """
        Build Ethereum refund transaction.

        :param transaction_hash: Ethereum HTLC funded transaction hash.
        :type transaction_hash: str
        :param address: Ethereum sender address.
        :type address: str
        :param contract_address: Ethereum HTLC contract address, defaults to ``None``.
        :type contract_address: str

        :returns: RefundTransaction -- Ethereum refund transaction instance.

        >>> from swap.providers.ethereum.transaction import RefundTransaction
        >>> refund_transaction: RefundTransaction = RefundTransaction(network="mainnet")
        >>> refund_transaction.build_transaction(transaction_hash="0xe49ff507739f8d916ae2c9fd51dd63764658ffa42a5288a49d93bc70a933edc4", address="0x69e04fe16c9A6A83076B3c2dc4b4Bc21b5d9A20C", contract_address="0x67324d402ffc103d061dAfA9096ff639f0676378")
        <swap.providers.ethereum.transaction.RefundTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not is_address(address=address):
            raise AddressError(f"Invalid Ethereum sender '{address}' address.")
        if contract_address and not is_address(address=contract_address):
            raise AddressError(f"Invalid Ethereum HTLC contract '{contract_address}' address.")

        htlc: HTLC = HTLC(
            contract_address=contract_address, network=self._network, erc20=self._erc20
        )
        htlc_contract: Contract = self.web3.eth.contract(
            address=htlc.contract_address(), abi=htlc.abi()
        )

        transaction_receipt: AttributeDict = self.web3.eth.get_transaction_receipt(transaction_hash)
        log_fund: AttributeDict = htlc_contract.events.log_fund().processLog(
            log=transaction_receipt["logs"][2 if self._erc20 else 0]
        )

        locked_contract_id: str = log_fund["args"]["locked_contract_id"]
        htlc_refund_function = htlc_contract.functions.refund(
            locked_contract_id  # Locked Contract ID
        )

        self._fee = htlc_refund_function.estimateGas({
            "from": to_checksum_address(address=address),
            "value": Wei(0),
            "nonce": self.web3.eth.get_transaction_count(
                to_checksum_address(address=address)
            ),
            "gasPrice": self.web3.eth.gas_price
        })

        self._transaction = htlc_refund_function.buildTransaction({
            "from": to_checksum_address(address=address),
            "value": Wei(0),
            "nonce": self.web3.eth.get_transaction_count(
                to_checksum_address(address=address)
            ),
            "gas": self._fee,
            "gasPrice": self.web3.eth.gas_price
        })
        self._type = "ethereum_erc20_refund_unsigned" if self._erc20 else "ethereum_refund_unsigned"
        return self

    def sign(self, solver: RefundSolver) -> "RefundTransaction":
        """
        Sign Ethereum refund transaction.

        :param solver: Ethereum refund solver.
        :type solver: ethereum.solver.RefundSolver

        :returns: RefundTransaction -- Ethereum refund transaction instance.

        >>> from swap.providers.ethereum.transaction import RefundTransaction
        >>> from swap.providers.ethereum.solver import RefundSolver
        >>> refund_transaction: RefundTransaction = RefundTransaction(network="mainnet")
        >>> refund_transaction.build_transaction(transaction_hash="0xe49ff507739f8d916ae2c9fd51dd63764658ffa42a5288a49d93bc70a933edc4", address="0x69e04fe16c9A6A83076B3c2dc4b4Bc21b5d9A20C", contract_address="0x67324d402ffc103d061dAfA9096ff639f0676378")
        >>> refund_solver: RefundSolver = RefundSolver(xprivate_key="xprv9s21ZrQH143K3Y3pdbkbjreZQ9RVmqTLhRgf86uZyCJk2ou36YdUJt5frjwihGWmV1fQEDioiGZXWXUbHLy3kQf5xmhvhp8dZ2tfn6tgGUj", address=0)
        >>> refund_transaction.sign(solver=refund_solver)
        <swap.providers.ethereum.transaction.RefundTransaction object at 0x0409DAF0>
        """

        # Check parameter instances
        if not isinstance(solver, RefundSolver):
            raise TypeError(f"Solver must be Ethereum RefundSolver, not {type(solver).__name__} type.")

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
        self._type = "ethereum_erc20_refund_signed" if self._erc20 else "ethereum_refund_signed"
        return self
