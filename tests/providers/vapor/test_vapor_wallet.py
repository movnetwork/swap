#!/usr/bin/env python3

import json
import os

from swap.providers.vapor.wallet import Wallet

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_vapor_wallet_from_entropy():

    wallet = Wallet(network=_["vapor"]["network"])

    wallet.from_entropy(
        entropy=_["vapor"]["wallet"]["sender"]["entropy"],
        language=_["vapor"]["wallet"]["sender"]["language"],
        passphrase=_["bytom"]["wallet"]["sender"]["passphrase"]
    )

    wallet.from_path(
        path=_["vapor"]["wallet"]["sender"]["derivation"]["path"]
    )

    assert wallet.entropy() == _["vapor"]["wallet"]["sender"]["entropy"]
    assert wallet.mnemonic() == _["vapor"]["wallet"]["sender"]["mnemonic"]
    assert wallet.language() == _["vapor"]["wallet"]["sender"]["language"]
    assert wallet.passphrase() is None
    assert wallet.seed() == _["vapor"]["wallet"]["sender"]["seed"]
    assert wallet.xprivate_key() == _["vapor"]["wallet"]["sender"]["xprivate_key"]
    assert wallet.xpublic_key() == _["vapor"]["wallet"]["sender"]["xpublic_key"]
    assert wallet.expand_xprivate_key() == _["vapor"]["wallet"]["sender"]["expand_xprivate_key"]
    assert wallet.child_xprivate_key() == _["vapor"]["wallet"]["sender"]["child_xprivate_key"]
    assert wallet.child_xpublic_key() == _["vapor"]["wallet"]["sender"]["child_xpublic_key"]
    # assert wallet.guid() == _["vapor"]["wallet"]["sender"]["guid"]
    assert wallet.private_key() == _["vapor"]["wallet"]["sender"]["private_key"]
    assert wallet.public_key() == _["vapor"]["wallet"]["sender"]["public_key"]
    assert wallet.program() == _["vapor"]["wallet"]["sender"]["program"]
    assert wallet.indexes() == _["vapor"]["wallet"]["sender"]["derivation"]["indexes"]
    assert wallet.path() == _["vapor"]["wallet"]["sender"]["derivation"]["path"]
    assert wallet.address() == _["vapor"]["wallet"]["sender"]["address"]

    assert isinstance(wallet.balance(), int)
    assert isinstance(wallet.utxos(), list)


def test_vapor_wallet_from_mnemonic():

    wallet = Wallet(network=_["vapor"]["network"])

    wallet.from_mnemonic(
        mnemonic=_["vapor"]["wallet"]["sender"]["mnemonic"],
        language=_["vapor"]["wallet"]["sender"]["language"],
        passphrase=_["bytom"]["wallet"]["sender"]["passphrase"],
    )

    wallet.from_path(
        path=_["vapor"]["wallet"]["sender"]["derivation"]["path"]
    )

    assert wallet.entropy() == _["vapor"]["wallet"]["sender"]["entropy"]
    assert wallet.mnemonic() == _["vapor"]["wallet"]["sender"]["mnemonic"]
    assert wallet.language() == _["vapor"]["wallet"]["sender"]["language"]
    assert wallet.passphrase() is None
    assert wallet.seed() == _["vapor"]["wallet"]["sender"]["seed"]
    assert wallet.xprivate_key() == _["vapor"]["wallet"]["sender"]["xprivate_key"]
    assert wallet.xpublic_key() == _["vapor"]["wallet"]["sender"]["xpublic_key"]
    assert wallet.expand_xprivate_key() == _["vapor"]["wallet"]["sender"]["expand_xprivate_key"]
    assert wallet.child_xprivate_key() == _["vapor"]["wallet"]["sender"]["child_xprivate_key"]
    assert wallet.child_xpublic_key() == _["vapor"]["wallet"]["sender"]["child_xpublic_key"]
    # assert wallet.guid() == _["vapor"]["wallet"]["sender"]["guid"]
    assert wallet.private_key() == _["vapor"]["wallet"]["sender"]["private_key"]
    assert wallet.public_key() == _["vapor"]["wallet"]["sender"]["public_key"]
    assert wallet.program() == _["vapor"]["wallet"]["sender"]["program"]
    assert wallet.indexes() == _["vapor"]["wallet"]["sender"]["derivation"]["indexes"]
    assert wallet.path() == _["vapor"]["wallet"]["sender"]["derivation"]["path"]
    assert wallet.address() == _["vapor"]["wallet"]["sender"]["address"]

    # assert isinstance(wallet.balance(), int)
    # assert isinstance(wallet.utxos(), list)


def test_vapor_wallet_from_seed():

    wallet = Wallet(network=_["vapor"]["network"])

    wallet.from_seed(
        seed=_["vapor"]["wallet"]["recipient"]["seed"]
    )

    wallet.from_path(
        path=_["vapor"]["wallet"]["recipient"]["derivation"]["path"]
    )

    assert wallet.entropy() is None
    assert wallet.mnemonic() is None
    assert wallet.language() is None
    assert wallet.passphrase() is None
    assert wallet.seed() == _["vapor"]["wallet"]["recipient"]["seed"]
    assert wallet.xprivate_key() == _["vapor"]["wallet"]["recipient"]["xprivate_key"]
    assert wallet.xpublic_key() == _["vapor"]["wallet"]["recipient"]["xpublic_key"]
    assert wallet.expand_xprivate_key() == _["vapor"]["wallet"]["recipient"]["expand_xprivate_key"]
    assert wallet.child_xprivate_key() == _["vapor"]["wallet"]["recipient"]["child_xprivate_key"]
    assert wallet.child_xpublic_key() == _["vapor"]["wallet"]["recipient"]["child_xpublic_key"]
    # assert wallet.guid() == _["vapor"]["wallet"]["recipient"]["guid"]
    assert wallet.private_key() == _["vapor"]["wallet"]["recipient"]["private_key"]
    assert wallet.public_key() == _["vapor"]["wallet"]["recipient"]["public_key"]
    assert wallet.program() == _["vapor"]["wallet"]["recipient"]["program"]
    assert wallet.indexes() == _["vapor"]["wallet"]["recipient"]["derivation"]["indexes"]
    assert wallet.path() == _["vapor"]["wallet"]["recipient"]["derivation"]["path"]
    assert wallet.address() == _["vapor"]["wallet"]["recipient"]["address"]

    # assert isinstance(wallet.balance(), int)
    # assert isinstance(wallet.utxos(), list)


def test_vapor_wallet_from_xprivate_key():

    wallet = Wallet(network=_["vapor"]["network"])

    wallet.from_xprivate_key(
        xprivate_key=_["vapor"]["wallet"]["sender"]["xprivate_key"]
    )

    wallet.from_path(
        path=_["vapor"]["wallet"]["sender"]["derivation"]["path"]
    )

    assert wallet.entropy() is None
    assert wallet.mnemonic() is None
    assert wallet.language() is None
    assert wallet.passphrase() is None
    assert wallet.seed() is None
    assert wallet.xprivate_key() == _["vapor"]["wallet"]["sender"]["xprivate_key"]
    assert wallet.xpublic_key() == _["vapor"]["wallet"]["sender"]["xpublic_key"]
    assert wallet.expand_xprivate_key() == _["vapor"]["wallet"]["sender"]["expand_xprivate_key"]
    assert wallet.child_xprivate_key() == _["vapor"]["wallet"]["sender"]["child_xprivate_key"]
    assert wallet.child_xpublic_key() == _["vapor"]["wallet"]["sender"]["child_xpublic_key"]
    # assert wallet.guid() == _["vapor"]["wallet"]["sender"]["guid"]
    assert wallet.private_key() == _["vapor"]["wallet"]["sender"]["private_key"]
    assert wallet.public_key() == _["vapor"]["wallet"]["sender"]["public_key"]
    assert wallet.program() == _["vapor"]["wallet"]["sender"]["program"]
    assert wallet.indexes() == _["vapor"]["wallet"]["recipient"]["derivation"]["indexes"]
    assert wallet.path() == _["vapor"]["wallet"]["recipient"]["derivation"]["path"]
    assert wallet.address() == _["vapor"]["wallet"]["sender"]["address"]

    # assert isinstance(wallet.balance(), int)
    # assert isinstance(wallet.utxos(), list)


def test_vapor_wallet_from_private_key():

    wallet = Wallet(network=_["vapor"]["network"])

    wallet.from_private_key(
        private_key=_["vapor"]["wallet"]["recipient"]["private_key"]
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
    assert wallet.private_key() == _["vapor"]["wallet"]["recipient"]["private_key"]
    assert wallet.public_key() == _["vapor"]["wallet"]["recipient"]["public_key"]
    assert wallet.program() == _["vapor"]["wallet"]["recipient"]["program"]
    assert wallet.indexes() == []
    assert wallet.path() is None
    assert wallet.address() == _["vapor"]["wallet"]["recipient"]["address"]

    # assert isinstance(wallet.balance(), int)
    # assert isinstance(wallet.utxos(), list)
