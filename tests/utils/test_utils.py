#!/usr/bin/env python3

from shuttle.utils import sha256, double_sha256, \
    generate_mnemonic, generate_passphrase
from mnemonic.mnemonic import Mnemonic

mnemonic = Mnemonic(language="korean")


def test_shuttle_utils():
    assert sha256("meherett".encode()).hex() == \
           "d4f5c55a45c004660b95ec833bb24569eba1559f214e90efa6e8d0b3afa14394"

    assert double_sha256("meherett".encode()).hex() == \
           "2803bf9ed1e5874825350b1b0753a96c00a99236b686bde337404453b11d3288"

    generated_mnemonic = generate_mnemonic(language="korean")
    assert mnemonic.check(generated_mnemonic)

    assert len(generate_passphrase(length=100)) == 100
