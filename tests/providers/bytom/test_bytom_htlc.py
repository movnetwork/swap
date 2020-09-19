#!/usr/bin/env python3

from equity.exceptions import ConnectionError

import pytest
import json
import os

from swap.providers.bytom.wallet import Wallet
from swap.providers.bytom.htlc import HTLC

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
_ = open(file_path, "r")
TEST_VALUES = json.loads(_.read())
_.close()

network: str = TEST_VALUES["bytom"]["network"]
sender_wallet: Wallet = Wallet(network=network).from_mnemonic(
    mnemonic=TEST_VALUES["bytom"]["wallet"]["sender"]["mnemonic"],
    passphrase=TEST_VALUES["bytom"]["wallet"]["recipient"]["passphrase"]
).from_path(
    path=TEST_VALUES["bytom"]["wallet"]["sender"]["path"]
)
recipient_wallet: Wallet = Wallet(network=network).from_mnemonic(
    mnemonic=TEST_VALUES["bytom"]["wallet"]["recipient"]["mnemonic"],
    passphrase=TEST_VALUES["bytom"]["wallet"]["recipient"]["passphrase"]
).from_path(
    path=TEST_VALUES["bytom"]["wallet"]["recipient"]["path"]
)


def test_bytom_htlc():

    htlc = HTLC(network=network).init(
        secret_hash=TEST_VALUES["bytom"]["htlc"]["secret"]["hash"],
        recipient_public=recipient_wallet.public_key(),
        sender_public=sender_wallet.public_key(),
        sequence=TEST_VALUES["bytom"]["htlc"]["sequence"],
        use_script=False
    )

    assert htlc.bytecode() == TEST_VALUES["bytom"]["htlc"]["bytecode"]
    assert htlc.opcode() == TEST_VALUES["bytom"]["htlc"]["opcode"]
    assert htlc.hash() == TEST_VALUES["bytom"]["htlc"]["hash"]
    assert htlc.address() == TEST_VALUES["bytom"]["htlc"]["address"]

    htlc = HTLC(network=network).from_bytecode(
        bytecode=TEST_VALUES["bytom"]["htlc"]["bytecode"]
    )

    assert htlc.bytecode() == TEST_VALUES["bytom"]["htlc"]["bytecode"]
    assert htlc.hash() == TEST_VALUES["bytom"]["htlc"]["hash"]
    assert htlc.address() == TEST_VALUES["bytom"]["htlc"]["address"]


def test_bytom_htlc_exception():

    with pytest.raises(ConnectionError, match=r".*http://localhost:9888*."):
        HTLC(network="mainnet").init(
            secret_hash=TEST_VALUES["bytom"]["htlc"]["secret"]["hash"],
            recipient_public=recipient_wallet.public_key(),
            sender_public=sender_wallet.public_key(),
            sequence=100,
            use_script=True
        )

    with pytest.raises(TypeError, match="secret hash must be string format"):
        HTLC(network="mainnet").init(int(), str(), str(), int())

    with pytest.raises(ValueError, match="invalid secret hash, length must be 64"):
        HTLC(network="mainnet").init(str(), str(), str(), int())

    with pytest.raises(ValueError, match="htlc script is none, initialization htlc first"):
        HTLC(network="mainnet").bytecode()

    with pytest.raises(ValueError, match="htlc script is none, initialization htlc first"):
        HTLC(network="mainnet").opcode()

    with pytest.raises(ValueError, match="htlc script is none, initialization htlc first"):
        HTLC(network="mainnet").hash()

    with pytest.raises(ValueError, match="htlc script is none, initialization htlc first"):
        HTLC(network="mainnet").address()

    with pytest.raises(TypeError, match="recipient public key must be string format"):
        HTLC(network="mainnet").init("3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb",
                                     float(), str(), int())

    with pytest.raises(ValueError, match="invalid recipient public key, length must be 64"):
        HTLC(network="mainnet").init("3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb",
                                     str(), str(), int())

    with pytest.raises(TypeError, match="sender public key must be string format"):
        HTLC(network="mainnet").init("3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb",
                                     "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2",
                                     bool(), int())

    with pytest.raises(ValueError, match="invalid sender public key, length must be 64"):
        HTLC(network="mainnet").init("3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb",
                                     "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2",
                                     str(), int())

    with pytest.raises(TypeError, match="sequence must be integer format"):
        HTLC(network="mainnet").init("3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb",
                                     "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2",
                                     "ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01",
                                     str())
