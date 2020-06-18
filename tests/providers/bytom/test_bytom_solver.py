#!/usr/bin/env python3

from pybytom.wallet import Wallet as _Wallet

from shuttle.providers.bytom.wallet import Wallet
from shuttle.providers.bytom.solver import (
    FundSolver, ClaimSolver, RefundSolver
)
from shuttle.utils import sha256

import pytest


network = "mainnet"
sender_wallet = Wallet(network=network).from_mnemonic(
    mnemonic="hint excuse upgrade sleep easily deputy erase cluster section other ugly limit"
).from_guid(
    guid="571784a8-0945-4d78-b973-aac4b09d6439"
)
recipient_wallet = Wallet(network=network).from_mnemonic(
    mnemonic="indicate warm sock mistake code spot acid ribbon sing over taxi toast"
).from_guid(
    guid="f0ed6ddd-9d6b-49fd-8866-a52d1083a13b"
)


def test_bytom_fund_solver():

    fund_solver = FundSolver(
        xprivate_key=sender_wallet.xprivate_key()
    )

    assert sender_wallet.xprivate_key() == fund_solver.xprivate_key
    assert isinstance(fund_solver.solve(), _Wallet)

    with pytest.raises(TypeError, match="xprivate key must be string format"):
        FundSolver(float())


def test_bytom_claim_solver():

    htlc_claim_solver = ClaimSolver(
        xprivate_key=recipient_wallet.xprivate_key(),
        secret="Hello Meheret!",
        # Witness from HTLC agreements
        secret_hash=sha256("Hello Meheret!".encode()).hex(),
        recipient_public=recipient_wallet.public_key(),
        sender_public=sender_wallet.public_key(),
        sequence=1000
    )

    assert recipient_wallet.xprivate_key() == htlc_claim_solver.xprivate_key
    assert isinstance(htlc_claim_solver.solve(), _Wallet)
    assert isinstance(htlc_claim_solver.witness("mainnet"), str)

    bytecode_claim_solver = ClaimSolver(
        xprivate_key=recipient_wallet.xprivate_key(),
        secret="Hello Meheret!",
        # Witness from HTLC bytecode
        bytecode="01642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423"
                 "a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01203a26da82ead15a80533a02696656b14b5dbf"
                 "d84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f697"
                 "2ae7cac00c0"
    )

    assert recipient_wallet.xprivate_key() == bytecode_claim_solver.xprivate_key
    assert isinstance(bytecode_claim_solver.solve(), _Wallet)
    assert isinstance(bytecode_claim_solver.witness("testnet"), str)

    with pytest.raises(TypeError, match="xprivate key must be string format"):
        ClaimSolver(int(), str())
    with pytest.raises(TypeError, match="secret must be string format"):
        ClaimSolver(str(), int())
    with pytest.raises(TypeError, match="secret hash must be string format"):
        ClaimSolver(str(), str(), int())
    with pytest.raises(ValueError, match="invalid secret hash, length must be 64"):
        ClaimSolver(str(), str(), str())
    with pytest.raises(TypeError, match="recipient public key must be string format"):
        ClaimSolver(str(), str(), sha256(b"Hello Meheret!").hex(), bool())
    with pytest.raises(ValueError, match="invalid recipient public key, length must be 64"):
        ClaimSolver(str(), str(), sha256(b"Hello Meheret!").hex(), "asdfsdfasdf")
    with pytest.raises(TypeError, match="sender public key must be string format"):
        ClaimSolver(str(), str(), sha256(b"Hello Meheret!").hex(),
                    recipient_wallet.public_key(), bool())
    with pytest.raises(ValueError, match="invalid sender public key, length must be 64"):
        ClaimSolver(str(), str(), sha256(b"Hello Meheret!").hex(),
                    recipient_wallet.public_key(), "asdfsdfasdf")
    with pytest.raises(TypeError, match="sequence must be integer format"):
        ClaimSolver(str(), str(), sha256(b"Hello Meheret!").hex(),
                    recipient_wallet.public_key(), sender_wallet.public_key(), float())
    with pytest.raises(TypeError, match="bytecode must be string format"):
        ClaimSolver(str(), str(), bytecode=123423423423)


def test_bytom_refund_solver():

    htlc_refund_solver = RefundSolver(
        xprivate_key=sender_wallet.xprivate_key(),
        # Witness from HTLC agreements
        secret_hash=sha256("Hello Meheret!".encode()).hex(),
        recipient_public=recipient_wallet.public_key(),
        sender_public=sender_wallet.public_key(),
        sequence=1000
    )

    assert sender_wallet.xprivate_key() == htlc_refund_solver.xprivate_key
    assert isinstance(htlc_refund_solver.solve(), _Wallet)
    assert isinstance(htlc_refund_solver.witness("mainnet"), str)

    bytecode_refund_solver = RefundSolver(
        xprivate_key=sender_wallet.xprivate_key(),
        # Witness from HTLC bytecode
        bytecode="63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a91498f879fb7f8"
                 "b4951dee9bc8a0327b792fbe332b888ac670164b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68"
    )

    assert sender_wallet.xprivate_key() == bytecode_refund_solver.xprivate_key
    assert isinstance(bytecode_refund_solver.solve(), _Wallet)
    assert isinstance(bytecode_refund_solver.witness("mainnet"), str)

    with pytest.raises(TypeError, match="xprivate key must be string format"):
        RefundSolver(int())
    with pytest.raises(TypeError, match="secret hash must be string format"):
        RefundSolver(str(), int())
    with pytest.raises(ValueError, match="invalid secret hash, length must be 64"):
        RefundSolver(str(), str())
    with pytest.raises(TypeError, match="recipient public key must be string format"):
        RefundSolver(str(), sha256(b"Hello Meheret!").hex(), bool())
    with pytest.raises(ValueError, match="invalid recipient public key, length must be 64"):
        RefundSolver(str(), sha256(b"Hello Meheret!").hex(), "asdfsdfasdf")
    with pytest.raises(TypeError, match="sender public key must be string format"):
        RefundSolver(str(), sha256(b"Hello Meheret!").hex(),
                     recipient_wallet.public_key(), bool())
    with pytest.raises(ValueError, match="invalid sender public key, length must be 64"):
        RefundSolver(str(), sha256(b"Hello Meheret!").hex(),
                     recipient_wallet.public_key(), "asdfsdfasdf")
    with pytest.raises(TypeError, match="sequence must be integer format"):
        RefundSolver(str(), sha256(b"Hello Meheret!").hex(),
                     recipient_wallet.public_key(), sender_wallet.public_key(), float())
    with pytest.raises(TypeError, match="bytecode must be string format"):
        RefundSolver(str(), bytecode=123423423423)
