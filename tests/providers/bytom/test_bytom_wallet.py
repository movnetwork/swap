#!/usr/bin/env python3

import json
import os

from swap.providers.bytom.wallet import Wallet

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_bytom_wallet_from_entropy():

    wallet = Wallet(network=_["bytom"]["network"])

    wallet.from_entropy(
        entropy=_["bytom"]["wallet"]["sender"]["entropy"],
        passphrase=_["bytom"]["wallet"]["sender"]["passphrase"],
        language=_["bytom"]["wallet"]["sender"]["language"]
    )

    wallet.from_path(
        path=_["bytom"]["wallet"]["sender"]["derivation"]["path"]
    )

    assert wallet.entropy() == _["bytom"]["wallet"]["sender"]["entropy"]
    assert wallet.mnemonic() == _["bytom"]["wallet"]["sender"]["mnemonic"]
    assert wallet.language() == _["bytom"]["wallet"]["sender"]["language"]
    assert wallet.passphrase() is None
    assert wallet.seed() == _["bytom"]["wallet"]["sender"]["seed"]
    assert wallet.xprivate_key() == _["bytom"]["wallet"]["sender"]["xprivate_key"]
    assert wallet.xpublic_key() == _["bytom"]["wallet"]["sender"]["xpublic_key"]
    assert wallet.expand_xprivate_key() == _["bytom"]["wallet"]["sender"]["expand_xprivate_key"]
    assert wallet.child_xprivate_key() == _["bytom"]["wallet"]["sender"]["child_xprivate_key"]
    assert wallet.child_xpublic_key() == _["bytom"]["wallet"]["sender"]["child_xpublic_key"]
    assert wallet.guid() == _["bytom"]["wallet"]["sender"]["guid"]
    assert wallet.private_key() == _["bytom"]["wallet"]["sender"]["private_key"]
    assert wallet.public_key() == _["bytom"]["wallet"]["sender"]["public_key"]
    assert wallet.program() == _["bytom"]["wallet"]["sender"]["program"]
    assert wallet.indexes() == _["bytom"]["wallet"]["sender"]["derivation"]["indexes"]
    assert wallet.path() == _["bytom"]["wallet"]["sender"]["derivation"]["path"]
    assert wallet.address() == _["bytom"]["wallet"]["sender"]["address"]

    assert isinstance(wallet.balance(), int)
    assert isinstance(wallet.utxos(), list)


def test_bytom_wallet_from_mnemonic():

    wallet = Wallet(network=_["bytom"]["network"])

    wallet.from_mnemonic(
        mnemonic=_["bytom"]["wallet"]["sender"]["mnemonic"],
        passphrase=_["bytom"]["wallet"]["sender"]["passphrase"],
        language=_["bytom"]["wallet"]["sender"]["language"]
    )

    wallet.from_path(
        path=_["bytom"]["wallet"]["sender"]["derivation"]["path"]
    )

    assert wallet.entropy() == _["bytom"]["wallet"]["sender"]["entropy"]
    assert wallet.mnemonic() == _["bytom"]["wallet"]["sender"]["mnemonic"]
    assert wallet.language() == _["bytom"]["wallet"]["sender"]["language"]
    assert wallet.passphrase() is None
    assert wallet.seed() == _["bytom"]["wallet"]["sender"]["seed"]
    assert wallet.xprivate_key() == _["bytom"]["wallet"]["sender"]["xprivate_key"]
    assert wallet.xpublic_key() == _["bytom"]["wallet"]["sender"]["xpublic_key"]
    assert wallet.expand_xprivate_key() == _["bytom"]["wallet"]["sender"]["expand_xprivate_key"]
    assert wallet.child_xprivate_key() == _["bytom"]["wallet"]["sender"]["child_xprivate_key"]
    assert wallet.child_xpublic_key() == _["bytom"]["wallet"]["sender"]["child_xpublic_key"]
    assert wallet.guid() == _["bytom"]["wallet"]["sender"]["guid"]
    assert wallet.private_key() == _["bytom"]["wallet"]["sender"]["private_key"]
    assert wallet.public_key() == _["bytom"]["wallet"]["sender"]["public_key"]
    assert wallet.program() == _["bytom"]["wallet"]["sender"]["program"]
    assert wallet.indexes() == _["bytom"]["wallet"]["sender"]["derivation"]["indexes"]
    assert wallet.path() == _["bytom"]["wallet"]["sender"]["derivation"]["path"]
    assert wallet.address() == _["bytom"]["wallet"]["sender"]["address"]

    # assert isinstance(wallet.balance(), int)
    # assert isinstance(wallet.utxos(), list)


def test_bytom_wallet_from_seed():

    wallet = Wallet(network=_["bytom"]["network"])

    wallet.from_seed(
        seed=_["bytom"]["wallet"]["recipient"]["seed"]
    )

    wallet.from_path(
        path=_["bytom"]["wallet"]["recipient"]["derivation"]["path"]
    )

    assert wallet.entropy() is None
    assert wallet.mnemonic() is None
    assert wallet.language() is None
    assert wallet.passphrase() is None
    assert wallet.seed() == _["bytom"]["wallet"]["recipient"]["seed"]
    assert wallet.xprivate_key() == _["bytom"]["wallet"]["recipient"]["xprivate_key"]
    assert wallet.xpublic_key() == _["bytom"]["wallet"]["recipient"]["xpublic_key"]
    assert wallet.expand_xprivate_key() == _["bytom"]["wallet"]["recipient"]["expand_xprivate_key"]
    assert wallet.child_xprivate_key() == _["bytom"]["wallet"]["recipient"]["child_xprivate_key"]
    assert wallet.child_xpublic_key() == _["bytom"]["wallet"]["recipient"]["child_xpublic_key"]
    # assert wallet.guid() == _["bytom"]["wallet"]["recipient"]["guid"]
    assert wallet.private_key() == _["bytom"]["wallet"]["recipient"]["private_key"]
    assert wallet.public_key() == _["bytom"]["wallet"]["recipient"]["public_key"]
    assert wallet.program() == _["bytom"]["wallet"]["recipient"]["program"]
    assert wallet.indexes() == _["bytom"]["wallet"]["recipient"]["derivation"]["indexes"]
    assert wallet.path() == _["bytom"]["wallet"]["recipient"]["derivation"]["path"]
    assert wallet.address() == _["bytom"]["wallet"]["recipient"]["address"]

    # assert isinstance(wallet.balance(), int)
    # assert isinstance(wallet.utxos(), list)


def test_bytom_wallet_from_xprivate_key():

    wallet = Wallet(network=_["bytom"]["network"])

    wallet.from_xprivate_key(
        xprivate_key=_["bytom"]["wallet"]["sender"]["xprivate_key"]
    )

    wallet.from_path(
        path=_["bytom"]["wallet"]["sender"]["derivation"]["path"]
    )

    assert wallet.entropy() is None
    assert wallet.mnemonic() is None
    assert wallet.language() is None
    assert wallet.passphrase() is None
    assert wallet.seed() is None
    assert wallet.xprivate_key() == _["bytom"]["wallet"]["sender"]["xprivate_key"]
    assert wallet.xpublic_key() == _["bytom"]["wallet"]["sender"]["xpublic_key"]
    assert wallet.expand_xprivate_key() == _["bytom"]["wallet"]["sender"]["expand_xprivate_key"]
    assert wallet.child_xprivate_key() == _["bytom"]["wallet"]["sender"]["child_xprivate_key"]
    assert wallet.child_xpublic_key() == _["bytom"]["wallet"]["sender"]["child_xpublic_key"]
    # assert wallet.guid() == _["bytom"]["wallet"]["sender"]["guid"]
    assert wallet.private_key() == _["bytom"]["wallet"]["sender"]["private_key"]
    assert wallet.public_key() == _["bytom"]["wallet"]["sender"]["public_key"]
    assert wallet.program() == _["bytom"]["wallet"]["sender"]["program"]
    assert wallet.indexes() == _["bytom"]["wallet"]["recipient"]["derivation"]["indexes"]
    assert wallet.path() == _["bytom"]["wallet"]["recipient"]["derivation"]["path"]
    assert wallet.address() == _["bytom"]["wallet"]["sender"]["address"]

    # assert isinstance(wallet.balance(), int)
    # assert isinstance(wallet.utxos(), list)


def test_bytom_wallet_from_private_key():

    wallet = Wallet(network=_["bytom"]["network"])

    wallet.from_private_key(
        private_key=_["bytom"]["wallet"]["recipient"]["private_key"]
    )

    assert wallet.entropy() is None
    assert wallet.mnemonic() is None
    assert wallet.language() is None
    assert wallet.passphrase() is None
    assert wallet.seed() is None
    # assert wallet.xprivate_key() is None
    assert wallet.xpublic_key() is None
    assert wallet.expand_xprivate_key() is None
    assert wallet.child_xprivate_key() is None
    assert wallet.child_xpublic_key() is None
    assert wallet.guid() is None
    assert wallet.private_key() == _["bytom"]["wallet"]["recipient"]["private_key"]
    assert wallet.public_key() == _["bytom"]["wallet"]["recipient"]["public_key"]
    assert wallet.program() == _["bytom"]["wallet"]["recipient"]["program"]
    assert wallet.indexes() == []
    assert wallet.path() is None
    assert wallet.address() == _["bytom"]["wallet"]["recipient"]["address"]

    # assert isinstance(wallet.balance(), int)
    # assert isinstance(wallet.utxos(), list)
