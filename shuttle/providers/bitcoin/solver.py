#!/usr/bin/env python3

from btcpy.structs.crypto import PrivateKey
from btcpy.structs.sig import P2pkhSolver, \
    IfElseSolver, HashlockSolver, Branch, RelativeTimelockSolver
from btcpy.structs.transaction import Sequence

from ...utils import sha256
from ..config import bitcoin
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
    def __init__(self, private_key: str):
        # Private key of sender to sign signature
        self.private_key = PrivateKey.unhexlify(private_key)

    # Bitcoin signature solve
    def solve(self):
        return P2pkhSolver(self.private_key)


# Claim Solver
class ClaimSolver:
    """
    Bitcoin ClaimSolver class.

    :param private_key: Bitcoin sender private key.
    :type private_key: str
    :param secret: Secret password/passphrase.
    :type secret: str
    :param recipient_address: Bitcoin recipient address.
    :type recipient_address: str
    :param sender_address: Bitcoin sender address.
    :type sender_address: str
    :param sequence: Bitcoin sequence number(expiration block), defaults to 1000.
    :type sequence: int
    :returns:  ClaimSolver -- Bitcoin claim solver instance.

    >>> from shuttle.providers.bitcoin.solver import ClaimSolver
    >>> claim_solver = ClaimSolver(private_key="6bc3b581f3dea1963f9257ec2a0195969babee3704e6ba7cd2ec535140b9816f", secret="Hello Meheret!", recipient_address="muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB", sender_address="mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q", sequence=1000)
    <shuttle.providers.bitcoin.solver.ClaimSolver object at 0x03FCCA60>
    """

    # Initialization claim solver
    def __init__(self, private_key: str, secret: str,
                 recipient_address: str, sender_address: str, sequence=bitcoin["sequence"]):
        # Private key of recipient to sign signature
        self.private_key = PrivateKey.unhexlify(private_key)
        # HTLC witness agreements
        self.htlc_args = [
            secret.encode(),  # Secret password/passphrase
            recipient_address,  # Bitcoin recipient address
            sender_address,  # Bitcoin sender address
            sequence  # Sequence/Expiration block
        ]

    # Bitcoin signature solve
    def solve(self):
        return IfElseSolver(
            Branch.IF,
            HashlockSolver(
                self.htlc_args[0],
                P2pkhSolver(self.private_key)
            )
        )

    # Bitcoin HTLC witnesses script
    def witness(self, network=bitcoin["network"]):
        return HTLC(network=network).init(
            secret_hash=sha256(self.htlc_args[0]).hex(),
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
    :param secret: Secret password/passphrase.
    :type secret: str
    :param recipient_address: Bitcoin recipient address.
    :type recipient_address: str
    :param sender_address: Bitcoin sender address.
    :type sender_address: str
    :param sequence: Bitcoin sequence number(expiration block), defaults to 1000.
    :type sequence: int
    :returns:  RefundSolver -- Bitcoin refund solver instance.

    >>> from shuttle.providers.bitcoin.solver import RefundSolver
    >>> refund_solver = RefundSolver(private_key="92cbbc5990cb5090326a76feeb321cad01048635afe5756523bbf9f7a75bf38b", secret="Hello Meheret!", recipient_address="muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB", sender_address="mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q", sequence=1000)
    <shuttle.providers.bitcoin.solver.RefundSolver object at 0x03FCCA60>
    """

    # Initialization refund solver
    def __init__(self, private_key: str, secret: str,
                 recipient_address: str, sender_address: str, sequence=bitcoin["sequence"]):
        # Private key of recipient to sign signature
        self.private_key = PrivateKey.unhexlify(private_key)
        # HTLC witness agreements
        self.htlc_args = [
            secret.encode(),  # Secret password/passphrase
            recipient_address,  # Bitcoin recipient address
            sender_address,  # Bitcoin sender address
            sequence  # Sequence/Expiration block
        ]

    # Bitcoin signature solve
    def solve(self):
        return IfElseSolver(
            Branch.ELSE,
            RelativeTimelockSolver(
                Sequence(self.htlc_args[3]),
                P2pkhSolver(self.private_key)
            )
        )

    # Bitcoin HTLC witnesses script
    def witness(self, network=bitcoin["network"]):
        return HTLC(network=network).init(
            secret_hash=sha256(self.htlc_args[0]).hex(),
            recipient_address=self.htlc_args[1],
            sender_address=self.htlc_args[2],
            sequence=self.htlc_args[3]
        ).script

