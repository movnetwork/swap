#!/usr/bin/env python3

import json
import os

from swap.providers.xinfin.wallet import Wallet

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_xinfin_wallet_from_entropy():

    wallet = Wallet(network=_["xinfin"]["network"])

    wallet.from_entropy(
        entropy=_["xinfin"]["wallet"]["sender"]["entropy"],
        language=_["xinfin"]["wallet"]["sender"]["language"],
        passphrase=_["xinfin"]["wallet"]["sender"]["passphrase"]
    )

    wallet.from_path(
        path=_["xinfin"]["wallet"]["sender"]["derivation"]["path"]
    )

    assert wallet.entropy() == _["xinfin"]["wallet"]["sender"]["entropy"]
    assert wallet.mnemonic() == _["xinfin"]["wallet"]["sender"]["mnemonic"]
    assert wallet.language() == _["xinfin"]["wallet"]["sender"]["language"]
    assert wallet.passphrase() is None
    assert wallet.seed() == _["xinfin"]["wallet"]["sender"]["seed"]
    assert wallet.root_xprivate_key() == _["xinfin"]["wallet"]["sender"]["root_xprivate_key"]
    assert wallet.root_xpublic_key() == _["xinfin"]["wallet"]["sender"]["root_xpublic_key"]
    assert wallet.xprivate_key() == _["xinfin"]["wallet"]["sender"]["xprivate_key"]
    assert wallet.xpublic_key() == _["xinfin"]["wallet"]["sender"]["xpublic_key"]
    assert wallet.uncompressed() == _["xinfin"]["wallet"]["sender"]["uncompressed"]
    assert wallet.compressed() == _["xinfin"]["wallet"]["sender"]["compressed"]
    assert wallet.chain_code() == _["xinfin"]["wallet"]["sender"]["chain_code"]
    assert wallet.private_key() == _["xinfin"]["wallet"]["sender"]["private_key"]
    assert wallet.public_key() == _["xinfin"]["wallet"]["sender"]["public_key"]
    assert wallet.wif() == _["xinfin"]["wallet"]["sender"]["wif"]
    assert wallet.hash() == _["xinfin"]["wallet"]["sender"]["hash"]
    assert wallet.finger_print() == _["xinfin"]["wallet"]["sender"]["finger_print"]
    assert wallet.path() == _["xinfin"]["wallet"]["sender"]["derivation"]["path"]
    assert wallet.address() == _["xinfin"]["wallet"]["sender"]["address"]

    assert isinstance(wallet.balance(), int)


def test_xinfin_wallet_from_mnemonic():

    wallet = Wallet(network=_["xinfin"]["network"])

    wallet.from_mnemonic(
        mnemonic=_["xinfin"]["wallet"]["sender"]["mnemonic"],
        language=_["xinfin"]["wallet"]["sender"]["language"],
        passphrase=_["xinfin"]["wallet"]["sender"]["passphrase"]
    )

    wallet.from_path(
        path=_["xinfin"]["wallet"]["sender"]["derivation"]["path"]
    )

    assert wallet.entropy() == _["xinfin"]["wallet"]["sender"]["entropy"]
    assert wallet.mnemonic() == _["xinfin"]["wallet"]["sender"]["mnemonic"]
    assert wallet.language() == _["xinfin"]["wallet"]["sender"]["language"]
    assert wallet.passphrase() is None
    assert wallet.seed() == _["xinfin"]["wallet"]["sender"]["seed"]
    assert wallet.root_xprivate_key() == _["xinfin"]["wallet"]["sender"]["root_xprivate_key"]
    assert wallet.root_xpublic_key() == _["xinfin"]["wallet"]["sender"]["root_xpublic_key"]
    assert wallet.xprivate_key() == _["xinfin"]["wallet"]["sender"]["xprivate_key"]
    assert wallet.xpublic_key() == _["xinfin"]["wallet"]["sender"]["xpublic_key"]
    assert wallet.uncompressed() == _["xinfin"]["wallet"]["sender"]["uncompressed"]
    assert wallet.compressed() == _["xinfin"]["wallet"]["sender"]["compressed"]
    assert wallet.chain_code() == _["xinfin"]["wallet"]["sender"]["chain_code"]
    assert wallet.private_key() == _["xinfin"]["wallet"]["sender"]["private_key"]
    assert wallet.public_key() == _["xinfin"]["wallet"]["sender"]["public_key"]
    assert wallet.wif() == _["xinfin"]["wallet"]["sender"]["wif"]
    assert wallet.hash() == _["xinfin"]["wallet"]["sender"]["hash"]
    assert wallet.finger_print() == _["xinfin"]["wallet"]["sender"]["finger_print"]
    assert wallet.path() == _["xinfin"]["wallet"]["sender"]["derivation"]["path"]
    assert wallet.address() == _["xinfin"]["wallet"]["sender"]["address"]

    # assert isinstance(wallet.balance(), int)


def test_xinfin_wallet_from_seed():

    wallet = Wallet(network=_["xinfin"]["network"])

    wallet.from_seed(
        seed=_["xinfin"]["wallet"]["recipient"]["seed"]
    )

    wallet.from_path(
        path=_["xinfin"]["wallet"]["recipient"]["derivation"]["path"]
    )

    assert wallet.entropy() is None
    assert wallet.mnemonic() is None
    assert wallet.language() is None
    assert wallet.passphrase() is None
    assert wallet.seed() == _["xinfin"]["wallet"]["recipient"]["seed"]
    assert wallet.root_xprivate_key() == _["xinfin"]["wallet"]["recipient"]["root_xprivate_key"]
    assert wallet.root_xpublic_key() == _["xinfin"]["wallet"]["recipient"]["root_xpublic_key"]
    assert wallet.xprivate_key() == _["xinfin"]["wallet"]["recipient"]["xprivate_key"]
    assert wallet.xpublic_key() == _["xinfin"]["wallet"]["recipient"]["xpublic_key"]
    assert wallet.uncompressed() == _["xinfin"]["wallet"]["recipient"]["uncompressed"]
    assert wallet.compressed() == _["xinfin"]["wallet"]["recipient"]["compressed"]
    assert wallet.chain_code() == _["xinfin"]["wallet"]["recipient"]["chain_code"]
    assert wallet.private_key() == _["xinfin"]["wallet"]["recipient"]["private_key"]
    assert wallet.public_key() == _["xinfin"]["wallet"]["recipient"]["public_key"]
    assert wallet.wif() == _["xinfin"]["wallet"]["recipient"]["wif"]
    assert wallet.hash() == _["xinfin"]["wallet"]["recipient"]["hash"]
    assert wallet.finger_print() == _["xinfin"]["wallet"]["recipient"]["finger_print"]
    assert wallet.path() == _["xinfin"]["wallet"]["recipient"]["derivation"]["path"]
    assert wallet.address() == _["xinfin"]["wallet"]["recipient"]["address"]

    # assert isinstance(wallet.balance(), int)


def test_xinfin_wallet_from_root_xprivate_key():

    wallet = Wallet(network=_["xinfin"]["network"])

    wallet.from_xprivate_key(
        xprivate_key=_["xinfin"]["wallet"]["sender"]["root_xprivate_key"]
    )

    wallet.from_path(
        path=_["xinfin"]["wallet"]["sender"]["derivation"]["path"]
    )

    assert wallet.entropy() is None
    assert wallet.mnemonic() is None
    assert wallet.language() is None
    assert wallet.passphrase() is None
    assert wallet.seed() is None
    assert wallet.root_xprivate_key() == _["xinfin"]["wallet"]["sender"]["root_xprivate_key"]
    assert wallet.root_xpublic_key() == _["xinfin"]["wallet"]["sender"]["root_xpublic_key"]
    assert wallet.xprivate_key() == _["xinfin"]["wallet"]["sender"]["xprivate_key"]
    assert wallet.xpublic_key() == _["xinfin"]["wallet"]["sender"]["xpublic_key"]
    assert wallet.uncompressed() == _["xinfin"]["wallet"]["sender"]["uncompressed"]
    assert wallet.compressed() == _["xinfin"]["wallet"]["sender"]["compressed"]
    assert wallet.chain_code() == _["xinfin"]["wallet"]["sender"]["chain_code"]
    assert wallet.private_key() == _["xinfin"]["wallet"]["sender"]["private_key"]
    assert wallet.public_key() == _["xinfin"]["wallet"]["sender"]["public_key"]
    assert wallet.wif() == _["xinfin"]["wallet"]["sender"]["wif"]
    assert wallet.hash() == _["xinfin"]["wallet"]["sender"]["hash"]
    assert wallet.finger_print() == _["xinfin"]["wallet"]["sender"]["finger_print"]
    assert wallet.path() == _["xinfin"]["wallet"]["sender"]["derivation"]["path"]
    assert wallet.address() == _["xinfin"]["wallet"]["sender"]["address"]

    # assert isinstance(wallet.balance(), int)


def test_xinfin_wallet_from_private_key():

    wallet = Wallet(network=_["xinfin"]["network"])

    wallet.from_private_key(
        private_key=_["xinfin"]["wallet"]["sender"]["private_key"]
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
    assert wallet.uncompressed() == _["xinfin"]["wallet"]["sender"]["uncompressed"]
    assert wallet.compressed() == _["xinfin"]["wallet"]["sender"]["compressed"]
    assert wallet.chain_code() is None
    assert wallet.private_key() == _["xinfin"]["wallet"]["sender"]["private_key"]
    assert wallet.public_key() == _["xinfin"]["wallet"]["sender"]["public_key"]
    assert wallet.wif() == _["xinfin"]["wallet"]["sender"]["wif"]
    assert wallet.hash() == _["xinfin"]["wallet"]["sender"]["hash"]
    assert wallet.finger_print() == _["xinfin"]["wallet"]["sender"]["finger_print"]
    assert wallet.path() is None
    assert wallet.address() == _["xinfin"]["wallet"]["sender"]["address"]

    # assert isinstance(wallet.balance(), int)
