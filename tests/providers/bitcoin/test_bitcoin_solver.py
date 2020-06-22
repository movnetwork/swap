#!/usr/bin/env python3

from btcpy.structs.script import IfElseScript
from btcpy.structs.sig import (
    P2pkhSolver, IfElseSolver, HashlockSolver, Branch, RelativeTimelockSolver
)

from shuttle.providers.bitcoin.wallet import Wallet
from shuttle.providers.bitcoin.solver import (
    FundSolver, ClaimSolver, RefundSolver
)
from shuttle.utils.exceptions import AddressError
from shuttle.utils import sha256

import pytest


network = "testnet"
sender_wallet = Wallet(network=network).from_passphrase("meheret tesfaye batu bayou")
recipient_wallet = Wallet(network=network).from_passphrase("meheret")


def test_bitcoin_fund_solver():

    fund_solver = FundSolver(
        private_key=sender_wallet.private_key()
    )

    assert sender_wallet.private_key() == fund_solver.private_key.hexlify()

    assert isinstance(fund_solver.solve(), P2pkhSolver)

    with pytest.raises(TypeError, match="private key must be string format"):
        FundSolver(float())


def test_bitcoin_claim_solver():

    htlc_claim_solver = ClaimSolver(
        private_key=recipient_wallet.private_key(),
        secret="Hello Meheret!",
        # Witness from HTLC agreements
        secret_hash=sha256("Hello Meheret!".encode()).hex(),
        recipient_address=recipient_wallet.address(),
        sender_address=sender_wallet.address(),
        sequence=1000
    )

    assert recipient_wallet.private_key() == htlc_claim_solver.private_key.hexlify()
    assert isinstance(htlc_claim_solver.solve(), IfElseSolver)
    assert isinstance(htlc_claim_solver.witness("testnet"), IfElseScript)

    bytecode_claim_solver = ClaimSolver(
        private_key=recipient_wallet.private_key(),
        secret="Hello Meheret!",
        # Witness from HTLC bytecode
        bytecode="63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a91498f879fb7f8"
                 "b4951dee9bc8a0327b792fbe332b888ac670164b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68"
    )

    assert recipient_wallet.private_key() == bytecode_claim_solver.private_key.hexlify()
    assert isinstance(bytecode_claim_solver.solve(), IfElseSolver)
    assert isinstance(bytecode_claim_solver.witness("testnet"), IfElseScript)

    with pytest.raises(TypeError, match="private key must be string format"):
        ClaimSolver(int(), str())
    with pytest.raises(TypeError, match="secret must be string format"):
        ClaimSolver(str(), int())
    with pytest.raises(TypeError, match="secret hash must be string format"):
        ClaimSolver(str(), str(), int())
    with pytest.raises(ValueError, match="invalid secret hash, length must be 64"):
        ClaimSolver(str(), str(), str())
    with pytest.raises(AddressError, match=r"invalid recipient *.* address"):
        ClaimSolver(str(), str(), sha256(b"Hello Meheret!").hex(), "adsfsdfsd")
    with pytest.raises(AddressError, match=r"invalid sender *.* address"):
        ClaimSolver(str(), str(), sha256(b"Hello Meheret!").hex(),
                    "2N729UBGZB3xjsGFRgKivy4bSjkaJGMVSpB", "adsfsdfsd")
    with pytest.raises(TypeError, match="sequence must be integer format"):
        ClaimSolver(str(), str(), sha256(b"Hello Meheret!").hex(),
                    "2N729UBGZB3xjsGFRgKivy4bSjkaJGMVSpB", "2N729UBGZB3xjsGFRgKivy4bSjkaJGMVSpB", float())
    with pytest.raises(TypeError, match="bytecode must be string format"):
        ClaimSolver(str(), str(), bytecode=123423423423)


def test_bitcoin_refund_solver():

    htlc_refund_solver = RefundSolver(
        private_key=sender_wallet.private_key(),
        # Witness from HTLC agreements
        secret_hash=sha256("Hello Meheret!".encode()).hex(),
        recipient_address=recipient_wallet.address(),
        sender_address=sender_wallet.address(),
        sequence=1000
    )

    assert sender_wallet.private_key() == htlc_refund_solver.private_key.hexlify()
    assert isinstance(htlc_refund_solver.solve(), IfElseSolver)
    assert isinstance(htlc_refund_solver.witness("testnet"), IfElseScript)

    bytecode_refund_solver = RefundSolver(
        private_key=sender_wallet.private_key(),
        # Witness from HTLC bytecode
        bytecode="63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a91498f879fb7f8"
                 "b4951dee9bc8a0327b792fbe332b888ac670164b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68"
    )

    assert sender_wallet.private_key() == bytecode_refund_solver.private_key.hexlify()
    assert isinstance(bytecode_refund_solver.solve(), IfElseSolver)
    assert isinstance(bytecode_refund_solver.witness("testnet"), IfElseScript)

    with pytest.raises(TypeError, match="private key must be string format"):
        RefundSolver(int())
    with pytest.raises(TypeError, match="secret hash must be string format"):
        RefundSolver(str(), int())
    with pytest.raises(ValueError, match="invalid secret hash, length must be 64"):
        RefundSolver(str(), str())
    with pytest.raises(AddressError, match=r"invalid recipient *.* address"):
        RefundSolver(str(), sha256(b"Hello Meheret!").hex(), "adsfsdfsd")
    with pytest.raises(AddressError, match=r"invalid sender *.* address"):
        RefundSolver(str(), sha256(b"Hello Meheret!").hex(),
                    "2N729UBGZB3xjsGFRgKivy4bSjkaJGMVSpB", "adsfsdfsd")
    with pytest.raises(TypeError, match="sequence must be integer format"):
        RefundSolver(str(), sha256(b"Hello Meheret!").hex(),
                    "2N729UBGZB3xjsGFRgKivy4bSjkaJGMVSpB", "2N729UBGZB3xjsGFRgKivy4bSjkaJGMVSpB", float())
    with pytest.raises(TypeError, match="bytecode must be string format"):
        RefundSolver(str(), bytecode=123423423423)
