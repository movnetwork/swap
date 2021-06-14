#!/usr/bin/env python3

from binascii import unhexlify, hexlify
from base64 import b64encode

import json

from ..config import ethereum
from .wallet import Wallet
from .htlc import HTLC
from .rpc import get_web3
from .utils import is_address, to_checksum_address
from .solver import FundSolver, ClaimSolver, RefundSolver
from ...utils.exceptions import BuildTransactionError


# Ethereum configuration
ethereum = ethereum()


class Transaction:
    """
    Ethereum Transaction class.

    :param network: ethereum network, defaults to ropsten.
    :type network: str
    :returns:  Transaction -- ethereum transaction instance.

    .. note::
        Ethereum has only three networks, ``mainnet``. ``solonet`` and ``ropsten``.
    """

    # Initialization transaction
    def __init__(self, network="ropsten"):
        # Transaction
        self.transaction = None
        # Ethereum network
        self.network = network
        # Ethereum fee
        self.fee = None
        # Signed datas
        self.signature = dict()

    # Transaction hash
    def hash(self):
        """
        Get ethereum transaction hash.

        :returns: str -- ethereum transaction hash or transaction id.

        >>> transaction.hash()
        "2993414225f65390220730d0c1a356c14e91bca76db112d37366df93e364a492"
        """

        return self.signature["hash"]\
            if "hash" in self.signature else None

    # Transaction json
    def json(self):
        """
        Get ethereum transaction json format.

        :returns: dict -- ethereum transaction json format.

        >>> transaction.json()
        {'gas': 134320, 'gasPrice': 20000000000, 'chainId': 1337, 'from': '0x053929E43A1eF27E3822E7fb193527edE04C415B', 'nonce': 15, 'value': 100, 'to': '0x9f77B9f27e8Bc8ad0b58FBf99aeA28feEC7eC50b', 'data': '0x335ef5bd00000000000000000000000031aa61a5d8756c84ebdf0f34e01cab90514f2a573a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb000000000000000000000000000000000000000000000000000000005ea55961'}
        """
        if self.transaction is None:
            raise ValueError("transaction is none, build transaction first.")
        return self.transaction

    # Transaction raw
    def raw(self):
        """
        Get ethereum transaction raw.

        :returns: str -- ethereum transaction raw.

        >>> transaction.raw()
        "f8cc0f8504a817c80083020cb0949f77b9f27e8bc8ad0b58fbf99aea28feec7ec50b64b864335ef5bd00000000000000000000000031aa61a5d8756c84ebdf0f34e01cab90514f2a573a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb000000000000000000000000000000000000000000000000000000005ea55961820a95a08bae7e0a7481d11518f7771fedc6f25ab5cc85bc24a0767573ce60e52a090c8da04d6efaafedc5096ecc998cdbca5b3ea4fc6b009b44a8041b8c71be5520c3a356"
        """

        return self.signature["rawTransaction"]\
            if "rawTransaction" in self.signature else None


class FundTransaction(Transaction):
    """
    Ethereum FundTransaction class.

    :param network: ethereum network, defaults to ropsten.
    :type network: str
    :returns: FundTransaction -- ethereum fund transaction instance.

    .. warning::
        Do not forget to build transaction after initialize fund transaction.

    :fee: Get ethereum fund transaction fee.

    >>> fund_transaction.fee
    1000000000000

    :signatures: Get ethereum fund transaction signature data.

    >>> fund_transaction.signature
    {...}
    """

    # Initialization fund transaction
    def __init__(self, network="ropsten"):
        # Setting network
        super().__init__(network=network)
        # Initializing web3 and getting previous hash & contract address of htlc
        self._hash, self._contract_address, self.web3 = get_web3(network=network)

    # Building transaction
    def build_transaction(self, wallet, htlc, amount):

        # Checking build transaction arguments instance
        if not isinstance(wallet, Wallet):
            raise TypeError("invalid wallet instance, only takes ethereum Wallet class")
        if not isinstance(htlc, HTLC):
            raise TypeError("invalid htlc instance, only takes ethereum HTLC class")
        if not isinstance(amount, int):
            raise TypeError("invalid amount instance, only takes integer type")

        self._hash = unhexlify(htlc.hash().encode())
        tx_receipt = self.web3.eth.getTransactionReceipt(transaction_hash=self._hash)
        if tx_receipt is None:
            raise BuildTransactionError("HTLC %s still not mined, wait for it to be mined..." % htlc.hash())
        self._contract_address = to_checksum_address(tx_receipt.contractAddress)

        # Getting HTLC instances
        htlc_contract = self.web3.eth.contract(
            address=self._contract_address,
            abi=htlc.abi()
        )

        # Building new HTLC transaction
        self.transaction = htlc_contract.functions.newContract(
            htlc.contract_init[0],
            htlc.contract_init[1],
            htlc.contract_init[2]
        ).buildTransaction({
            "from": to_checksum_address(wallet.address()),
            "nonce": self.web3.eth.getTransactionCount(to_checksum_address(wallet.address())),
            "value": int(amount)
        })
        self.fee = int(self.transaction["gas"])
        return self

    # Signing transaction using fund solver
    def sign(self, solver):
        """
        Sign ethereum fund transaction.

        :param solver: ethereum fund solver.
        :type solver: ethereum.solver.FundSolver
        :returns: FundTransaction -- ethereum fund transaction instance.

        >>> from shuttle.providers.ethereum.transaction import FundTransaction
        >>> fund_transaction = FundTransaction(network="ropsten")
        >>> fund_transaction.build_transaction(sender_wallet, htlc, 10000)
        >>> fund_transaction.sign(fund_solver)
        <shuttle.providers.ethereum.transaction.FundTransaction object at 0x0409DAF0>
        """

        if not isinstance(solver, FundSolver):
            raise TypeError("Solver must be FundSolver format.")
        account = self.web3.eth.account.privateKeyToAccount(solver.solve().private_key())
        signature = account.signTransaction(self.transaction)
        self.signature = dict(
            rawTransaction=hexlify(signature.rawTransaction).decode(),
            hash=hexlify(signature.hash).decode(),
            r=str(signature.r), s=str(signature.s), v=str(signature.v)
        )
        return self

    def unsigned_raw(self):
        """
        Get ethereum unsigned fund transaction raw.

        :returns: str -- ethereum unsigned fund transaction raw.

        >>> from shuttle.providers.ethereum.transaction import FundTransaction
        >>> fund_transaction = FundTransaction(network="ropsten")
        >>> fund_transaction.build_transaction(sender_wallet, htlc, 10000)
        >>> fund_transaction.unsigned_raw()
        "eyJmZWUiOiAxMzQzMjAsICJ0eCI6IHsiZ2FzIjogMTM0MzIwLCAiZ2FzUHJpY2UiOiAyMDAwMDAwMDAwMCwgImNoYWluSWQiOiAxMzM3LCAiZnJvbSI6ICIweDA1MzkyOUU0M0ExZUYyN0UzODIyRTdmYjE5MzUyN2VkRTA0QzQxNUIiLCAibm9uY2UiOiAxNCwgInZhbHVlIjogMTAwLCAidG8iOiAiMHhDMEUwQTRDQTlmQ0E4YzczOTdmQzUzMjBBOTQyNGFmZTY2QzI5ZGUxIiwgImRhdGEiOiAiMHgzMzVlZjViZDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDMxYWE2MWE1ZDg3NTZjODRlYmRmMGYzNGUwMWNhYjkwNTE0ZjJhNTczYTI2ZGE4MmVhZDE1YTgwNTMzYTAyNjk2NjU2YjE0YjVkYmZkODRlYjE0NzkwZjJlMWJlNWU5ZTQ1ODIwZWViMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDA1ZWE1NTcyMSJ9LCAibmV0d29yayI6ICJnYW5hY2hlIiwgInR5cGUiOiAiZXRoZXJldW1fZnVuZF91bnNpZ25lZCJ9"
        """

        if not self.transaction:
            raise ValueError("transaction script is none, build transaction first")

        return b64encode(str(json.dumps(dict(
            fee=self.fee,
            tx=self.transaction,
            network=self.network,
            type="ethereum_fund_unsigned"
        ))).encode()).decode()


class ClaimTransaction(Transaction):
    """
    Bytom ClaimTransaction class.

    :param network: ethereum network, defaults to ropsten.
    :type network: str
    :returns: ClaimTransaction -- ethereum claim transaction instance.

    .. warning::
        Do not forget to build transaction after initialize claim transaction.

    :fee: Get ethereum claim transaction fee.

    >>> claim_transaction.fee
    10000000

    :signatures: Get ethereum fund transaction signature data.

    >>> claim_transaction.signature
    {...}
    """

    # Initialization fund transaction
    def __init__(self, network="ropsten"):
        # Setting network
        super().__init__(network=network)
        # Secret key
        self.secret = None
        # Initializing web3 and getting previous hash & contract address of htlc
        self._hash, self._contract_address, self.web3 = get_web3(network=network)

    def build_transaction(self, transaction_id, wallet, amount, secret=None):
        """
        Build ethereum claim transaction.

        :param wallet: ethereum recipient wallet.
        :type wallet: ethereum.wallet.Wallet
        :param amount: ethereum amount to withdraw.
        :type amount: int
        :param transaction_id: ethereum fund transaction id to redeem, default to None.
        :type transaction_id: str
        :param secret: secret key.
        :type secret: str
        :returns: ClaimTransaction -- ethereum claim transaction instance.

        >>> from shuttle.providers.ethereum.transaction import ClaimTransaction
        >>> claim_transaction = ClaimTransaction(network="ropsten")
        >>> claim_transaction.build_transaction(fund_transaction_id, recipient_wallet, 10000)
        <shuttle.providers.ethereum.transaction.ClaimTransaction object at 0x0409DAF0>
        """

        # Checking build transaction arguments instance
        if transaction_id and not isinstance(transaction_id, str):
            raise TypeError("invalid transaction id instance, only takes ethereum string type")
        if not isinstance(wallet, Wallet):
            raise TypeError("invalid wallet instance, only takes ethereum Wallet class")
        if not isinstance(amount, int):
            raise TypeError("invalid asset instance, only takes integer type")
        if secret is not None and not isinstance(secret, str):
            raise TypeError("invalid secret instance, only takes string type")

        # Getting transaction receipt
        transaction_receipt = self.web3.eth.getTransactionReceipt(transaction_id)
        if transaction_receipt is None:
            raise ValueError("You can't claim now, wait for it to be mined....")

        # Getting HTLC instances
        htlc = HTLC(network=self.network)
        htlc_contract = self.web3.eth.contract(
            address=self._contract_address,
            abi=htlc.abi()
        )

        # Getting log htlc new event.
        log_htlc_new = htlc_contract.events.LogHTLCNew()\
            .processLog(transaction_receipt.logs[0])
        # Getting contract id from transaction hash/id
        contract_id = hexlify(log_htlc_new.args.contractId).decode()

        # Building new HTLC transaction
        self.transaction = htlc_contract.functions.withdraw(
            contract_id, secret
        ).buildTransaction({
            "from": to_checksum_address(wallet.address()),
            "nonce": self.web3.eth.getTransactionCount(to_checksum_address(wallet.address())),
            "value": int(amount)
        })
        self.fee = int(self.transaction["gas"])
        self.secret = secret
        return self

    # Signing transaction using private keys
    def sign(self, solver):
        """
        Sign ethereum claim transaction.

        :param solver: ethereum claim solver.
        :type solver: ethereum.solver.ClaimSolver
        :returns: ClaimTransaction -- ethereum claim transaction instance.

        >>> from shuttle.providers.ethereum.transaction import ClaimTransaction
        >>> claim_transaction = ClaimTransaction(network="ropsten")
        >>> claim_transaction.build_transaction(fund_transaction_id, recipient_wallet, 10000)
        >>> claim_transaction.sign(claim_solver)
        <shuttle.providers.ethereum.transaction.ClaimTransaction object at 0x0409DAF0>
        """

        if not isinstance(solver, ClaimSolver):
            raise TypeError("solver must be ClaimSolver format.")
        wallet = solver.solve()
        return self

    def unsigned_raw(self):
        """
        Get ethereum unsigned claim transaction raw.

        :returns: str -- ethereum unsigned claim transaction raw.

        >>> from shuttle.providers.ethereum.transaction import ClaimTransaction
        >>> claim_transaction = ClaimTransaction(network="ropsten")
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
            type="ethereum_claim_unsigned"
        ))).encode()).decode()

