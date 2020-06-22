#!/usr/bin/env python3

from btcpy.structs.crypto import PrivateKey
from btcpy.structs.sig import (
    P2pkhSolver, IfElseSolver, HashlockSolver, Branch, RelativeTimelockSolver
)
from btcpy.structs.transaction import Sequence

from ...utils import sha256
from ...utils.exceptions import AddressError
from ..config import bitcoin
from .utils import is_address
from .htlc import HTLC

# Bitcoin config
bitcoin = bitcoin()


# Fund Solver
class FundSolver:
    """
    Bitcoin FundSolver class.

    :param private_key: Bitcoin sender private key.
    :type private_key: str
    :returns:  FundSolver -- Bitcoin fund solver instance.

    >>> from shuttle.providers.bitcoin.solver import FundSolver
    >>> fund_solver = FundSolver(private_key="92cbbc5990cb5090326a76feeb321cad01048635afe5756523bbf9f7a75bf38b")
    <shuttle.providers.bitcoin.solver.FundSolver object at 0x03FCCA60>
    """

    # Initialization fund solver
    def __init__(self, private_key):
        # Checking parameter instances
        if not isinstance(private_key, str):
            raise TypeError("private key must be string format")

        # Setting Bitcoin private key
        self.private_key = PrivateKey.unhexlify(private_key)

    # Bitcoin signature solve
    def solve(self):
        return P2pkhSolver(
            privk=self.private_key
        )


# Claim Solver
class ClaimSolver:
    """
    Bitcoin ClaimSolver class.

    :param private_key: Bitcoin sender private key.
    :type private_key: str
    :param secret: Secret password/passphrase.
    :type secret: str
    :param secret_hash: Secret witness password/passphrase hash, defaults to None.
    :type secret_hash: str
    :param recipient_address: Bitcoin witness recipient address, defaults to None.
    :type recipient_address: str
    :param sender_address: Bitcoin witness sender address, defaults to None.
    :type sender_address: str
    :param sequence: Bitcoin witness sequence number(expiration block), defaults to 1000.
    :type sequence: int
    :param bytecode: Bitcoin witness HTLC bytecode, defaults to None.
    :type bytecode: str
    :returns:  ClaimSolver -- Bitcoin claim solver instance.

    >>> from shuttle.providers.bitcoin.solver import ClaimSolver
    >>> from shuttle.utils import sha256
    >>> claim_solver = ClaimSolver(private_key="6bc3b581f3dea1963f9257ec2a0195969babee3704e6ba7cd2ec535140b9816f", secret="Hello Meheret!", secret_hash=sha256("Hello Meheret!".encode()).hex(), recipient_address="muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB", sender_address="mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q", sequence=1000)
    <shuttle.providers.bitcoin.solver.ClaimSolver object at 0x03FCCA60>
    """

    # Initialization claim solver
    def __init__(self, private_key, secret, secret_hash=None, recipient_address=None,
                 sender_address=None, sequence=bitcoin["sequence"], bytecode=None):

        # Checking parameter instances
        if not isinstance(private_key, str):
            raise TypeError("private key must be string format")
        if not isinstance(secret, str):
            raise TypeError("secret must be string format")
        if bytecode is None:
            if not isinstance(secret_hash, str):
                raise TypeError("secret hash must be string format")
            if len(secret_hash) != 64:
                raise ValueError("invalid secret hash, length must be 64")
            if not is_address(recipient_address):
                raise AddressError(f"invalid recipient {recipient_address} address")
            if not is_address(sender_address):
                raise AddressError(f"invalid sender {sender_address} address")
            if not isinstance(sequence, int):
                raise TypeError("sequence must be integer format")
        else:
            if not isinstance(bytecode, str):
                raise TypeError("bytecode must be string format")

        # Setting Bitcoin private key and secret password/passphrase
        self.private_key, self.secret = PrivateKey.unhexlify(private_key), secret
        # Setting witness from bytecode or HTLC
        self.bytecode, self.htlc_args = bytecode, [
            secret_hash,  # Secret password/passphrase
            recipient_address,  # Bitcoin recipient address
            sender_address,  # Bitcoin sender address
            sequence  # Sequence/Expiration block
        ]

    # Bitcoin signature solve
    def solve(self):
        return IfElseSolver(
            branch=Branch.IF,
            inner_solver=HashlockSolver(
                preimage=self.secret.encode(),
                inner_solver=P2pkhSolver(self.private_key)
            )
        )

    # Bitcoin HTLC witnesses script
    def witness(self, network=bitcoin["network"]):
        if self.bytecode:
            return HTLC(network=network).from_bytecode(
                bytecode=self.bytecode
            ).script
        return HTLC(network=network).init(
            secret_hash=self.htlc_args[0],
            recipient_address=self.htlc_args[1],
            sender_address=self.htlc_args[2],
            sequence=self.htlc_args[3]
        ).script


# Refund Solver
class RefundSolver:
    """
    Bitcoin RefundSolver class.

    :param private_key: Bitcoin sender private key.
    :type private_key: str
    :param secret_hash: Secret witness password/passphrase hash, defaults to None.
    :type secret_hash: str
    :param recipient_address: Bitcoin witness recipient address, defaults to None.
    :type recipient_address: str
    :param sender_address: Bitcoin witness sender address, defaults to None.
    :type sender_address: str
    :param sequence: Bitcoin witness sequence number(expiration block), defaults to 1000.
    :type sequence: int
    :param bytecode: Bitcoin witness HTLC bytecode, defaults to None.
    :type bytecode: str
    :returns:  RefundSolver -- Bitcoin refund solver instance.

    >>> from shuttle.providers.bitcoin.solver import RefundSolver
    >>> from shuttle.utils import sha256
    >>> refund_solver = RefundSolver(private_key="92cbbc5990cb5090326a76feeb321cad01048635afe5756523bbf9f7a75bf38b", secret_hash=sha256("Hello Meheret!".encode()).hex(), recipient_address="muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB", sender_address="mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q", sequence=1000)
    <shuttle.providers.bitcoin.solver.RefundSolver object at 0x03FCCA60>
    """

    # Initialization refund solver
    def __init__(self, private_key, secret_hash=None, recipient_address=None,
                 sender_address=None, sequence=bitcoin["sequence"], bytecode=None):
        # Checking parameter instances
        if not isinstance(private_key, str):
            raise TypeError("private key must be string format")
        if bytecode is None:
            if not isinstance(secret_hash, str):
                raise TypeError("secret hash must be string format")
            if len(secret_hash) != 64:
                raise ValueError("invalid secret hash, length must be 64")
            if not is_address(recipient_address):
                raise AddressError(f"invalid recipient {recipient_address} address")
            if not is_address(sender_address):
                raise AddressError(f"invalid sender {sender_address} address")
            if not isinstance(sequence, int):
                raise TypeError("sequence must be integer format")
        else:
            if not isinstance(bytecode, str):
                raise TypeError("bytecode must be string format")

        # Setting Bitcoin private key and Bitcoin sequence/expiration block
        self.private_key, self.sequence = PrivateKey.unhexlify(private_key), sequence
        # Setting witness from bytecode or HTLC
        self.bytecode, self.htlc_args = bytecode, [
            secret_hash,  # Secret password/passphrase
            recipient_address,  # Bitcoin recipient address
            sender_address,  # Bitcoin sender address
            sequence  # Sequence/Expiration block
        ]

    # Bitcoin signature solve
    def solve(self):
        return IfElseSolver(
            branch=Branch.ELSE,
            inner_solver=RelativeTimelockSolver(
                sequence=Sequence(self.sequence),
                inner_solver=P2pkhSolver(self.private_key)
            )
        )

    # Bitcoin HTLC witnesses script
    def witness(self, network=bitcoin["network"]):
        if self.bytecode:
            return HTLC(network=network).from_bytecode(
                bytecode=self.bytecode
            ).script
        return HTLC(network=network).init(
            secret_hash=self.htlc_args[0],
            recipient_address=self.htlc_args[1],
            sender_address=self.htlc_args[2],
            sequence=self.htlc_args[3]
        ).script
