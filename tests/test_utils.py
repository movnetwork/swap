#!/usr/bin/env python3

from swap.utils import (
    generate_passphrase, generate_entropy, generate_mnemonic,
    is_mnemonic, get_mnemonic_language, sha256, double_sha256
)

import pytest


MNEMONIC: str = "병아리 실컷 여인 축제 극히 저녁 경찰 설사 할인 해물 시각 자가용"


def test_swap_utils():

    assert len(generate_entropy(strength=128)) == 32

    assert is_mnemonic("sceptre capter séquence girafe absolu relatif fleur zoologie muscle sirop saboter parure")

    assert len(generate_mnemonic(language="chinese_traditional", strength=128).split(" ")) == 12

    assert get_mnemonic_language(
        mnemonic="sceptre capter séquence girafe absolu relatif fleur zoologie muscle sirop saboter parure"
    ) == "french"

    with pytest.raises(ValueError, match=r".*[128, 160, 192, 224, 256].*"):
        assert len(generate_entropy(strength=129).split(" ")) == 12

    assert is_mnemonic(mnemonic=MNEMONIC, language="korean")

    with pytest.raises(ValueError, match=r"invalid language, .*"):
        assert is_mnemonic(mnemonic=MNEMONIC, language="amharic")

    assert not is_mnemonic(mnemonic=12341234, language="english")

    with pytest.raises(ValueError, match="Invalid mnemonic words."):
        assert get_mnemonic_language("1234 meheret tesfaye")

    with pytest.raises(ValueError, match=r"invalid language, .*"):
        assert generate_mnemonic(language="amharic")

    with pytest.raises(ValueError, match=r"Strength should be one of the following .*"):
        assert generate_mnemonic(strength=129)

    assert len(generate_passphrase(length=100)) == 100

    assert sha256("meherett") == \
        "d4f5c55a45c004660b95ec833bb24569eba1559f214e90efa6e8d0b3afa14394"

    assert double_sha256("meherett") == \
        "2803bf9ed1e5874825350b1b0753a96c00a99236b686bde337404453b11d3288"

    assert sha256("meherett".encode()) == \
        "d4f5c55a45c004660b95ec833bb24569eba1559f214e90efa6e8d0b3afa14394"

    assert double_sha256("meherett".encode()) == \
        "2803bf9ed1e5874825350b1b0753a96c00a99236b686bde337404453b11d3288"
