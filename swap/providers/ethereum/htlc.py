#!/usr/bin/env python3

from binascii import unhexlify
from eth_account.datastructures import SignedTransaction
from web3.contract import (
    ContractConstructor, Contract
)
from semantic_version.base import Version
from typing import (
    Optional, Type, Union
)
from pathlib import PurePosixPath
from solcx import compile_files
from web3.types import Wei

import os

from ...exceptions import (
    AddressError, NetworkError, TransactionError, UnitError
)
from ..config import ethereum as config
from .rpc import (
    get_web3, get_balance
)
from .utils import (
    is_network, is_address, to_checksum_address, amount_unit_converter
)


class HTLC:

    def __init__(self, contract_address: Optional[str] = None, network: str = config["network"],
                 provider: str = config["provider"], token: Optional[str] = None):

        # Check parameter instances
        if not is_network(network=network):
            raise NetworkError(f"Invalid Ethereum '{network}' network",
                               "choose only 'mainnet', 'ropsten', 'kovan', 'rinkeby' or 'testnet' networks.")

        self._network: str = network
        if contract_address:
            if not is_address(address=contract_address):
                raise ValueError(f"Invalid Ethereum HTLC contact {contract_address} address.")
            self._contract_address: str = to_checksum_address(address=contract_address)
        else:
            self._contract_address: Optional[str] = config[self._network]["contract_address"]

        self.htlc_agreements: Optional[tuple] = None
        self.web3 = get_web3(
            network=network, provider=provider, token=token
        )

        # Get current working directory path (like linux or unix path).
        cwd: str = PurePosixPath(os.path.dirname(os.path.realpath(__file__))).__str__().replace("\\", "/")

        compiled_files: dict = compile_files(
            source_files=[f"{cwd}/contracts/htlc.sol"],
            output_values=["abi", "bin", "bin-runtime", "opcodes"],
            solc_version=Version("0.8.3")
        )

        self._abi: list = compiled_files[f"{cwd}/contracts/htlc.sol:HTLC"]["abi"]
        self._bytecode: str = compiled_files[f"{cwd}/contracts/htlc.sol:HTLC"]["bin"]
        self._bytecode_runtime: str = compiled_files[f"{cwd}/contracts/htlc.sol:HTLC"]["bin-runtime"]
        self._opcodes: str = compiled_files[f"{cwd}/contracts/htlc.sol:HTLC"]["opcodes"]

        self._estimated_gas: Optional[Wei] = None
        self._unsigned_transaction: Optional[dict] = None
        self._signed_transaction: Optional[SignedTransaction] = None
        self._hash: Optional[bytes] = None

    def build_transaction(self, address: str) -> "HTLC":

        # Check parameter instances
        if not is_address(address=address):
            raise AddressError(f"Invalid Ethereum '{address}' address.")

        contract: Type[Contract] = self.web3.eth.contract(
            abi=self._abi, bytecode=self._bytecode, bytecode_runtime=self._bytecode_runtime
        )

        constructed: ContractConstructor = contract.constructor()
        self._estimated_gas: Wei = Wei(constructed.estimateGas())
        self._unsigned_transaction: dict = constructed.buildTransaction({
            "from": to_checksum_address(address=address),
            "value": Wei(0),
            "nonce": self.web3.eth.get_transaction_count(
                to_checksum_address(address=address)
            ),
            "gas": self._estimated_gas,
            "gasPrice": self.web3.eth.gasPrice
        })
        return self

    def sign_transaction(self, private_key: str) -> "HTLC":

        if len(private_key) != 64:
            raise ValueError(f"Invalid Ethereum '{private_key}' private key.")
        if not self._unsigned_transaction or not isinstance(self._unsigned_transaction, dict):
            raise TransactionError(f"Can't sign HTLC transaction, Build transaction first.")

        self._signed_transaction: SignedTransaction = self.web3.eth.account.sign_transaction(
            transaction_dict=self._unsigned_transaction,
            private_key=private_key
        )
        return self

    def fee(self) -> Wei:

        if not self._unsigned_transaction or not isinstance(self._unsigned_transaction, dict):
            raise TransactionError(f"Can't get HTLC transaction fee, Build transaction first.")
        return self._estimated_gas

    def raw(self) -> str:

        if not self._signed_transaction or not isinstance(self._signed_transaction, SignedTransaction):
            raise TransactionError(f"Can't get HTLC transaction raw, Build transaction and sign first.")
        return self._signed_transaction["rawTransaction"].hex()

    def contract_address(self) -> str:

        # Check parameter instances
        if not self._contract_address:
            raise ValueError(
                f"HTLC contact address is required. Before build HTLC, initial contract address first.")
        if not is_address(address=self._contract_address):
            raise ValueError(f"Invalid Ethereum HTLC contact {self._contract_address} address.")

        return to_checksum_address(address=self._contract_address)

    def build_htlc(self, secret_hash: str, recipient_address: str, sender_address: str, locktime: int) -> "HTLC":

        # Check parameter instances
        if not self._contract_address:
            raise ValueError(f"HTLC contact address is required. Before build HTLC, initial contract address first.")
        if len(secret_hash) != 64:
            raise ValueError("Invalid secret hash, length must be 64.")
        if not is_address(recipient_address):
            raise AddressError(f"Invalid Ethereum recipient {recipient_address} address.")
        if not is_address(sender_address):
            raise AddressError(f"Invalid Ethereum sender {sender_address} address.")
        if not isinstance(locktime, int):
            raise TypeError("Locktime must be integer format (seconds).")

        self.htlc_agreements = (
            to_checksum_address(self._contract_address),
            unhexlify(secret_hash),
            to_checksum_address(recipient_address),
            to_checksum_address(sender_address),
            int(locktime)
        )
        return self

    def abi(self) -> list:
        return self._abi

    def bytecode(self) -> str:
        return self._bytecode

    def bytecode_runtime(self) -> str:
        return self._bytecode_runtime

    def opcode(self) -> str:
        return self._opcodes

    def balance(self, unit: str = config["unit"]) -> Union[Wei, int, float]:
        """
        Get Ethereum HTLC balance.

        :param unit: Ethereum unit, default to Ether.
        :type unit: str

        :return: int, float -- Ethereum HTLC balance.

        >>> from swap.providers.bitcoin.htlc import HTLC
        >>> from swap.utils import sha256
        >>> htlc = HTLC(contract_address="0xeaEaC81da5E386E8Ca4De1e64d40a10E468A5b40", network="testnet")
        >>> htlc.balance(unit="Ether")
        1.56
        """

        if unit not in ["Ether", "Gwei", "Wei"]:
            raise UnitError(f"Invalid Ethereum '{unit}' unit", "choose only 'Ether', 'Gwei' or 'Wei' units.")
        balance: int = get_balance(address=self.contract_address(), network=self._network)
        return balance if unit == "Wei" else \
            amount_unit_converter(amount=balance, unit=f"Wei2{unit}")
