#!/usr/bin/env python3

from binascii import unhexlify, hexlify
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

from ...exceptions import (
    AddressError, NetworkError, TransactionError, UnitError
)
from ...utils import clean_transaction_raw
from ..config import ethereum as config
from .wallet import Wallet
from .htlc import HTLC
from .rpc import (
    get_web3, get_balance
)
from .utils import (
    is_network, is_address, to_checksum_address, amount_unit_converter
)
from .solver import (
    NormalSolver, FundSolver, WithdrawSolver, RefundSolver
)


class Transaction:
    """
    Ethereum Transaction.

    :param network: Ethereum network, defaults to ``ropsten``.
    :type network: str

    :returns: Transaction -- Ethereum transaction instance.

    .. note::
        Ethereum has only three networks, ``mainnet``, ``ropsten``, ``kovan``, ``rinkeby`` and ``testnet``.
    """

    def __init__(self, network: str = config["network"], provider: str = config["provider"],
                 token: Optional[str] = None):

        # Check parameter instances
        if not is_network(network=network):
            raise NetworkError(f"Invalid Ethereum '{network}' network",
                               "choose only 'mainnet', 'ropsten', 'kovan', 'rinkeby' or 'testnet' networks.")

        self._network: str = network
        self.web3: Web3 = get_web3(
            network=network, provider=provider, token=token
        )

        self._transaction: Optional[dict] = None
        self._signature: Optional[dict] = None
        self._type: Optional[int] = None
        self._fee: Optional[int] = None

    def fee(self, unit: str = config["unit"]) -> Union[Wei, int, float]:

        # Check transaction
        if not self._transaction:
            raise ValueError("Transaction is none, build transaction first.")

        if unit not in ["Ether", "Gwei", "Wei"]:
            raise UnitError(f"Invalid Ethereum '{unit}' unit", "choose only 'Ether', 'Gwei' or 'Wei' units.")
        return self._fee if unit == "Wei" else \
            amount_unit_converter(amount=self._fee, unit=f"Wei2{unit}")

    def hash(self) -> str:

        # Check signature
        if not self._signature:
            raise ValueError("There is no signed transaction, build transaction then sign it first.")

        return self._signature["hash"]

    def json(self) -> dict:

        # Check transaction
        if not self._transaction:
            raise ValueError("Transaction is none, build transaction first.")

        return self._transaction

    def raw(self) -> str:

        # Check signature
        if not self._signature:
            raise ValueError("There is no signed transaction, build transaction then sign it first.")

        return self._signature["rawTransaction"]

    def signature(self) -> dict:

        # Check signature
        if not self._signature:
            raise ValueError("There is no signed transaction, build transaction then sign it first.")

        return self._signature


class NormalTransaction(Transaction):
    """
    Ethereum Normal transaction.

    :param network: Ethereum network, defaults to ``ropsten``.
    :type network: str
    :param provider: Ethereum network provider, defaults to ``http``.
    :type provider: str
    :param token: Infura API endpoint token, defaults to ``4414fea5f7454211956b1627621450b4``.
    :type token: str

    :returns: NormalTransaction -- Ethereum normal transaction instance.

    .. warning::
        Do not forget to build transaction after initialize normal transaction.
    """

    def __init__(self, network: str = config["network"], provider: str = config["provider"],
                 token: Optional[str] = None):
        super().__init__(
            network=network, provider=provider, token=token
        )

    def build_transaction(self, address: str, recipient_address: str, amount: Union[Wei, int]) -> "NormalTransaction":

        # Check parameter instances
        if not is_address(address=address):
            raise AddressError(f"Invalid Ethereum sender '{address}' address.")
        if not is_address(address=address):
            raise AddressError(f"Invalid Ethereum recipient '{recipient_address}' address.")

        self._fee = self.web3.eth.estimateGas({
            "from": to_checksum_address(address=address),
            "to": to_checksum_address(address=recipient_address),
            "value": Wei(amount),
            "nonce": self.web3.eth.get_transaction_count(
                to_checksum_address(address=address)
            ),
            "gasPrice": self.web3.eth.gasPrice
        })

        self._transaction = {
            "from": to_checksum_address(address=address),
            "to": to_checksum_address(address=recipient_address),
            "value": Wei(amount),
            "nonce": self.web3.eth.get_transaction_count(
                to_checksum_address(address=address)
            ),
            "gas": self._fee,
            "gasPrice": self.web3.eth.gasPrice
        }
        self._type = "ethereum_normal_unsigned"
        return self

    def sign(self, solver: NormalSolver) -> "NormalTransaction":

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
        self._type = "ethereum_normal_signed"
        return self

    def transaction_raw(self) -> str:

        # Check transaction
        if not self._transaction:
            raise ValueError("Transaction is none, build normal transaction first.")

        return clean_transaction_raw(b64encode(str(json.dumps(dict(
            fee=self._fee,
            transaction=self._transaction,
            signature=self._signature,
            network=self._network,
            type=self._type
        ))).encode()).decode())


class FundTransaction(Transaction):
    """
    Ethereum Fund transaction.

    :param network: Ethereum network, defaults to ``ropsten``.
    :type network: str
    :param provider: Ethereum network provider, defaults to ``http``.
    :type provider: str
    :param token: Infura API endpoint token, defaults to ``4414fea5f7454211956b1627621450b4``.
    :type token: str

    :returns: FundTransaction -- Ethereum fund transaction instance.

    .. warning::
        Do not forget to build transaction after initialize fund transaction.
    """

    def __init__(self, network: str = config["network"], provider: str = config["provider"],
                 token: Optional[str] = None):
        super().__init__(
            network=network, provider=provider, token=token
        )

    def build_transaction(self, htlc: HTLC, address: str,  amount: int) -> "FundTransaction":

        # Check parameter instances
        if not isinstance(htlc, HTLC):
            raise TypeError("Invalid HTLC instance, only takes ethereum HTLC class")
        if not is_address(address=address):
            raise AddressError(f"Invalid Ethereum sender '{address}' address.")
        if to_checksum_address(address=address) != htlc.agreements["sender_address"]:
            raise AddressError(f"Wrong Ethereum sender '{address}' address",
                               "address must be equal with HTLC agreements sender address.")

        htlc_contract: Contract = self.web3.eth.contract(
            address=htlc.contract_address(), abi=htlc.abi()
        )

        htlc_fund_function = htlc_contract.functions.fund(
            htlc.agreements["secret_hash"],  # Secret Hash
            htlc.agreements["recipient_address"],  # Recipient Address
            htlc.agreements["sender_address"],  # Sender Address
            htlc.agreements["endtime"]  # Locktime Seconds
        )

        self._fee = htlc_fund_function.estimateGas({
            "from": to_checksum_address(address=address),
            "value": Wei(amount),
            "nonce": self.web3.eth.get_transaction_count(
                to_checksum_address(address=address)
            ),
            "gasPrice": self.web3.eth.gasPrice
        })

        self._transaction = htlc_fund_function.buildTransaction({
            "from": to_checksum_address(address=address),
            "value": Wei(amount),
            "nonce": self.web3.eth.get_transaction_count(
                to_checksum_address(address=address)
            ),
            "gas": self._fee,
            "gasPrice": self.web3.eth.gasPrice
        })
        self._type = "ethereum_fund_unsigned"
        return self

    def sign(self, solver: FundSolver) -> "FundTransaction":

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
        self._type = "ethereum_fund_signed"
        return self

    def transaction_raw(self) -> str:

        # Check transaction
        if not self._transaction:
            raise ValueError("Transaction is none, build fund transaction first.")

        return clean_transaction_raw(b64encode(str(json.dumps(dict(
            fee=self._fee,
            transaction=self._transaction,
            signature=self._signature,
            network=self._network,
            type=self._type
        ))).encode()).decode())


class WithdrawTransaction(Transaction):
    """
    Ethereum Withdraw transaction.

    :param network: Ethereum network, defaults to ``ropsten``.
    :type network: str
    :param provider: Ethereum network provider, defaults to ``http``.
    :type provider: str
    :param token: Infura API endpoint token, defaults to ``4414fea5f7454211956b1627621450b4``.
    :type token: str

    :returns: WithdrawTransaction -- Ethereum withdraw transaction instance.

    .. warning::
        Do not forget to build transaction after initialize withdraw transaction.
    """

    def __init__(self, network: str = config["network"], provider: str = config["provider"],
                 token: Optional[str] = None):
        super().__init__(
            network=network, provider=provider, token=token
        )

    def build_transaction(self, transaction_id: str, address: str, secret_key: str,
                          contract_address: Optional[str] = None) -> "WithdrawTransaction":

        # Check parameter instances
        if not is_address(address=address):
            raise AddressError(f"Invalid Ethereum recipient '{address}' address.")
        if contract_address:
            if not is_address(address=contract_address):
                raise ValueError(f"Invalid Ethereum HTLC contact '{contract_address}' address.")
            contract_address: str = to_checksum_address(address=contract_address)
        else:
            contract_address: Optional[str] = config[self._network]["contract_address"]

        htlc: HTLC = HTLC(
            contract_address=contract_address, network=self._network
        )
        htlc_contract: Contract = self.web3.eth.contract(
            address=htlc.contract_address(), abi=htlc.abi()
        )

        transaction_receipt: AttributeDict = self.web3.eth.get_transaction_receipt(transaction_id)
        log_fund: AttributeDict = htlc_contract.events.log_fund().processLog(
            log=transaction_receipt["logs"][0]
        )

        locked_contract_id: str = log_fund["args"]["locked_contract_id"]
        htlc_fund_function = htlc_contract.functions.withdraw(
            locked_contract_id,  # Locked Contract ID
            secret_key  # Secret Key
        )

        self._fee = htlc_fund_function.estimateGas({
            "from": to_checksum_address(address=address),
            "value": Wei(0),
            "nonce": self.web3.eth.get_transaction_count(
                to_checksum_address(address=address)
            ),
            "gasPrice": self.web3.eth.gasPrice
        })

        self._transaction = htlc_fund_function.buildTransaction({
            "from": to_checksum_address(address=address),
            "value": Wei(0),
            "nonce": self.web3.eth.get_transaction_count(
                to_checksum_address(address=address)
            ),
            "gas": self._fee,
            "gasPrice": self.web3.eth.gasPrice
        })
        self._type = "ethereum_withdraw_unsigned"
        return self

    def sign(self, solver: WithdrawSolver) -> "WithdrawTransaction":

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
        self._type = "ethereum_withdraw_signed"
        return self

    def transaction_raw(self) -> str:

        # Check transaction
        if not self._transaction:
            raise ValueError("Transaction is none, build withdraw transaction first.")

        return clean_transaction_raw(b64encode(str(json.dumps(dict(
            fee=self._fee,
            transaction=self._transaction,
            signature=self._signature,
            network=self._network,
            type=self._type
        ))).encode()).decode())


class RefundTransaction(Transaction):
    """
    Ethereum Refund transaction.

    :param network: Ethereum network, defaults to ``ropsten``.
    :type network: str
    :param provider: Ethereum network provider, defaults to ``http``.
    :type provider: str
    :param token: Infura API endpoint token, defaults to ``4414fea5f7454211956b1627621450b4``.
    :type token: str

    :returns: RefundTransaction -- Ethereum refund transaction instance.

    .. warning::
        Do not forget to build transaction after initialize refund transaction.
    """

    def __init__(self, network: str = config["network"], provider: str = config["provider"],
                 token: Optional[str] = None):
        super().__init__(
            network=network, provider=provider, token=token
        )

    def build_transaction(self, transaction_id: str, address: str,
                          contract_address: Optional[str] = None) -> "RefundTransaction":

        # Check parameter instances
        if not is_address(address=address):
            raise AddressError(f"Invalid Ethereum recipient '{address}' address.")
        if contract_address:
            if not is_address(address=contract_address):
                raise ValueError(f"Invalid Ethereum HTLC contact '{contract_address}' address.")
            contract_address: str = to_checksum_address(address=contract_address)
        else:
            contract_address: Optional[str] = config[self._network]["contract_address"]

        htlc: HTLC = HTLC(
            contract_address=contract_address, network=self._network
        )
        htlc_contract: Contract = self.web3.eth.contract(
            address=htlc.contract_address(), abi=htlc.abi()
        )

        transaction_receipt: AttributeDict = self.web3.eth.get_transaction_receipt(transaction_id)
        log_fund: AttributeDict = htlc_contract.events.log_fund().processLog(
            log=transaction_receipt["logs"][0]
        )

        locked_contract_id: str = log_fund["args"]["locked_contract_id"]
        htlc_refund_function = htlc_contract.functions.refund(
            locked_contract_id,  # Locked Contract ID
        )

        self._fee = htlc_refund_function.estimateGas({
            "from": to_checksum_address(address=address),
            "value": Wei(0),
            "nonce": self.web3.eth.get_transaction_count(
                to_checksum_address(address=address)
            ),
            "gasPrice": self.web3.eth.gasPrice
        })

        self._transaction = htlc_refund_function.buildTransaction({
            "from": to_checksum_address(address=address),
            "value": Wei(0),
            "nonce": self.web3.eth.get_transaction_count(
                to_checksum_address(address=address)
            ),
            "gas": self._fee,
            "gasPrice": self.web3.eth.gasPrice
        })
        self._type = "ethereum_refund_unsigned"
        return self

    def sign(self, solver: RefundSolver) -> "RefundTransaction":

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
        self._type = "ethereum_refund_signed"
        return self

    def transaction_raw(self) -> str:

        # Check transaction
        if not self._transaction:
            raise ValueError("Transaction is none, build refund transaction first.")

        return clean_transaction_raw(b64encode(str(json.dumps(dict(
            fee=self._fee,
            transaction=self._transaction,
            signature=self._signature,
            network=self._network,
            type=self._type
        ))).encode()).decode())
