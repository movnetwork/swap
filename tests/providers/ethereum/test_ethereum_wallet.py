#!/usr/bin/env python3

import json
import os

from swap.providers.ethereum.wallet import Wallet

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_ethereum_wallet_from_entropy():

    wallet = Wallet(network=_["ethereum"]["network"])

    wallet.from_entropy(
        entropy=_["ethereum"]["wallet"]["sender"]["entropy"],
        language=_["ethereum"]["wallet"]["sender"]["language"],
        passphrase=_["ethereum"]["wallet"]["sender"]["passphrase"]
    )

    wallet.from_path(
        path=_["ethereum"]["wallet"]["sender"]["derivation"]["path"]
    )

    assert wallet.entropy() == _["ethereum"]["wallet"]["sender"]["entropy"]
    assert wallet.mnemonic() == _["ethereum"]["wallet"]["sender"]["mnemonic"]
    assert wallet.language() == _["ethereum"]["wallet"]["sender"]["language"]
    assert wallet.passphrase() is None
    assert wallet.seed() == _["ethereum"]["wallet"]["sender"]["seed"]
    assert wallet.root_xprivate_key() == _["ethereum"]["wallet"]["sender"]["root_xprivate_key"]
    assert wallet.root_xpublic_key() == _["ethereum"]["wallet"]["sender"]["root_xpublic_key"]
    assert wallet.xprivate_key() == _["ethereum"]["wallet"]["sender"]["xprivate_key"]
    assert wallet.xpublic_key() == _["ethereum"]["wallet"]["sender"]["xpublic_key"]
    assert wallet.uncompressed() == _["ethereum"]["wallet"]["sender"]["uncompressed"]
    assert wallet.compressed() == _["ethereum"]["wallet"]["sender"]["compressed"]
    assert wallet.chain_code() == _["ethereum"]["wallet"]["sender"]["chain_code"]
    assert wallet.private_key() == _["ethereum"]["wallet"]["sender"]["private_key"]
    assert wallet.public_key() == _["ethereum"]["wallet"]["sender"]["public_key"]
    assert wallet.wif() == _["ethereum"]["wallet"]["sender"]["wif"]
    assert wallet.hash() == _["ethereum"]["wallet"]["sender"]["hash"]
    assert wallet.finger_print() == _["ethereum"]["wallet"]["sender"]["finger_print"]
    assert wallet.path() == _["ethereum"]["wallet"]["sender"]["derivation"]["path"]
    assert wallet.address() == _["ethereum"]["wallet"]["sender"]["address"]

    assert isinstance(wallet.balance(), int)


def test_ethereum_wallet_from_mnemonic():

    wallet = Wallet(network=_["ethereum"]["network"])

    wallet.from_mnemonic(
        mnemonic=_["ethereum"]["wallet"]["sender"]["mnemonic"],
        language=_["ethereum"]["wallet"]["sender"]["language"],
        passphrase=_["ethereum"]["wallet"]["sender"]["passphrase"]
    )

    wallet.from_path(
        path=_["ethereum"]["wallet"]["sender"]["derivation"]["path"]
    )

    assert wallet.entropy() == _["ethereum"]["wallet"]["sender"]["entropy"]
    assert wallet.mnemonic() == _["ethereum"]["wallet"]["sender"]["mnemonic"]
    assert wallet.language() == _["ethereum"]["wallet"]["sender"]["language"]
    assert wallet.passphrase() is None
    assert wallet.seed() == _["ethereum"]["wallet"]["sender"]["seed"]
    assert wallet.root_xprivate_key() == _["ethereum"]["wallet"]["sender"]["root_xprivate_key"]
    assert wallet.root_xpublic_key() == _["ethereum"]["wallet"]["sender"]["root_xpublic_key"]
    assert wallet.xprivate_key() == _["ethereum"]["wallet"]["sender"]["xprivate_key"]
    assert wallet.xpublic_key() == _["ethereum"]["wallet"]["sender"]["xpublic_key"]
    assert wallet.uncompressed() == _["ethereum"]["wallet"]["sender"]["uncompressed"]
    assert wallet.compressed() == _["ethereum"]["wallet"]["sender"]["compressed"]
    assert wallet.chain_code() == _["ethereum"]["wallet"]["sender"]["chain_code"]
    assert wallet.private_key() == _["ethereum"]["wallet"]["sender"]["private_key"]
    assert wallet.public_key() == _["ethereum"]["wallet"]["sender"]["public_key"]
    assert wallet.wif() == _["ethereum"]["wallet"]["sender"]["wif"]
    assert wallet.hash() == _["ethereum"]["wallet"]["sender"]["hash"]
    assert wallet.finger_print() == _["ethereum"]["wallet"]["sender"]["finger_print"]
    assert wallet.path() == _["ethereum"]["wallet"]["sender"]["derivation"]["path"]
    assert wallet.address() == _["ethereum"]["wallet"]["sender"]["address"]

    # assert isinstance(wallet.balance(), int)


def test_ethereum_wallet_from_seed():

    wallet = Wallet(network=_["ethereum"]["network"])

    wallet.from_seed(
        seed=_["ethereum"]["wallet"]["recipient"]["seed"]
    )

    wallet.from_path(
        path=_["ethereum"]["wallet"]["recipient"]["derivation"]["path"]
    )

    assert wallet.entropy() is None
    assert wallet.mnemonic() is None
    assert wallet.language() is None
    assert wallet.passphrase() is None
    assert wallet.seed() == _["ethereum"]["wallet"]["recipient"]["seed"]
    assert wallet.root_xprivate_key() == _["ethereum"]["wallet"]["recipient"]["root_xprivate_key"]
    assert wallet.root_xpublic_key() == _["ethereum"]["wallet"]["recipient"]["root_xpublic_key"]
    assert wallet.xprivate_key() == _["ethereum"]["wallet"]["recipient"]["xprivate_key"]
    assert wallet.xpublic_key() == _["ethereum"]["wallet"]["recipient"]["xpublic_key"]
    assert wallet.uncompressed() == _["ethereum"]["wallet"]["recipient"]["uncompressed"]
    assert wallet.compressed() == _["ethereum"]["wallet"]["recipient"]["compressed"]
    assert wallet.chain_code() == _["ethereum"]["wallet"]["recipient"]["chain_code"]
    assert wallet.private_key() == _["ethereum"]["wallet"]["recipient"]["private_key"]
    assert wallet.public_key() == _["ethereum"]["wallet"]["recipient"]["public_key"]
    assert wallet.wif() == _["ethereum"]["wallet"]["recipient"]["wif"]
    assert wallet.hash() == _["ethereum"]["wallet"]["recipient"]["hash"]
    assert wallet.finger_print() == _["ethereum"]["wallet"]["recipient"]["finger_print"]
    assert wallet.path() == _["ethereum"]["wallet"]["recipient"]["derivation"]["path"]
    assert wallet.address() == _["ethereum"]["wallet"]["recipient"]["address"]

    # assert isinstance(wallet.balance(), int)


def test_ethereum_wallet_from_root_xprivate_key():

    wallet = Wallet(network=_["ethereum"]["network"])

    wallet.from_root_xprivate_key(
        xprivate_key=_["ethereum"]["wallet"]["sender"]["root_xprivate_key"]
    )

    wallet.from_path(
        path=_["ethereum"]["wallet"]["sender"]["derivation"]["path"]
    )

    assert wallet.entropy() is None
    assert wallet.mnemonic() is None
    assert wallet.language() is None
    assert wallet.passphrase() is None
    assert wallet.seed() is None
    assert wallet.root_xprivate_key() == _["ethereum"]["wallet"]["sender"]["root_xprivate_key"]
    assert wallet.root_xpublic_key() == _["ethereum"]["wallet"]["sender"]["root_xpublic_key"]
    assert wallet.xprivate_key() == _["ethereum"]["wallet"]["sender"]["xprivate_key"]
    assert wallet.xpublic_key() == _["ethereum"]["wallet"]["sender"]["xpublic_key"]
    assert wallet.uncompressed() == _["ethereum"]["wallet"]["sender"]["uncompressed"]
    assert wallet.compressed() == _["ethereum"]["wallet"]["sender"]["compressed"]
    assert wallet.chain_code() == _["ethereum"]["wallet"]["sender"]["chain_code"]
    assert wallet.private_key() == _["ethereum"]["wallet"]["sender"]["private_key"]
    assert wallet.public_key() == _["ethereum"]["wallet"]["sender"]["public_key"]
    assert wallet.wif() == _["ethereum"]["wallet"]["sender"]["wif"]
    assert wallet.hash() == _["ethereum"]["wallet"]["sender"]["hash"]
    assert wallet.finger_print() == _["ethereum"]["wallet"]["sender"]["finger_print"]
    assert wallet.path() == _["ethereum"]["wallet"]["sender"]["derivation"]["path"]
    assert wallet.address() == _["ethereum"]["wallet"]["sender"]["address"]

    # assert isinstance(wallet.balance(), int)


def test_ethereum_wallet_from_xprivate_key():

    wallet = Wallet(network=_["ethereum"]["network"])

    wallet.from_xprivate_key(
        xprivate_key=_["ethereum"]["wallet"]["recipient"]["xprivate_key"]
    )

    assert wallet.entropy() is None
    assert wallet.mnemonic() is None
    assert wallet.language() is None
    assert wallet.passphrase() is None
    assert wallet.seed() is None
    assert wallet.root_xprivate_key() is None
    assert wallet.root_xpublic_key() is None
    assert wallet.xprivate_key() == _["ethereum"]["wallet"]["recipient"]["xprivate_key"]
    assert wallet.xpublic_key() == _["ethereum"]["wallet"]["recipient"]["xpublic_key"]
    assert wallet.uncompressed() == _["ethereum"]["wallet"]["recipient"]["uncompressed"]
    assert wallet.compressed() == _["ethereum"]["wallet"]["recipient"]["compressed"]
    assert wallet.chain_code() == _["ethereum"]["wallet"]["recipient"]["chain_code"]
    assert wallet.private_key() == _["ethereum"]["wallet"]["recipient"]["private_key"]
    assert wallet.public_key() == _["ethereum"]["wallet"]["recipient"]["public_key"]
    assert wallet.wif() == _["ethereum"]["wallet"]["recipient"]["wif"]
    assert wallet.hash() == _["ethereum"]["wallet"]["recipient"]["hash"]
    assert wallet.finger_print() == _["ethereum"]["wallet"]["recipient"]["finger_print"]
    assert wallet.path() is None
    assert wallet.address() == _["ethereum"]["wallet"]["recipient"]["address"]

    # assert isinstance(wallet.balance(), int)


def test_ethereum_wallet_from_private_key():

    wallet = Wallet(network=_["ethereum"]["network"])

    wallet.from_private_key(
        private_key=_["ethereum"]["wallet"]["sender"]["private_key"]
    )

    assert wallet.entropy() is None
    assert wallet.mnemonic() is None
    assert wallet.language() is None
    assert wallet.passphrase() is None
    assert wallet.seed() is None
    assert wallet.root_xprivate_key() is None
    assert wallet.root_xpublic_key() is None
    assert wallet.xprivate_key() is None
    assert wallet.xpublic_key() is None
    assert wallet.uncompressed() == _["ethereum"]["wallet"]["sender"]["uncompressed"]
    assert wallet.compressed() == _["ethereum"]["wallet"]["sender"]["compressed"]
    assert wallet.chain_code() is None
    assert wallet.private_key() == _["ethereum"]["wallet"]["sender"]["private_key"]
    assert wallet.public_key() == _["ethereum"]["wallet"]["sender"]["public_key"]
    assert wallet.wif() == _["ethereum"]["wallet"]["sender"]["wif"]
    assert wallet.hash() == _["ethereum"]["wallet"]["sender"]["hash"]
    assert wallet.finger_print() == _["ethereum"]["wallet"]["sender"]["finger_print"]
    assert wallet.path() is None
    assert wallet.address() == _["ethereum"]["wallet"]["sender"]["address"]

    # assert isinstance(wallet.balance(), int)
