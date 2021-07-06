#!/usr/bin/env python3

from types import SimpleNamespace
from mnemonic.mnemonic import Mnemonic
from datetime import datetime
from binascii import (
    hexlify, unhexlify
)
from random import choice
from typing import (
    Optional, Union
)

import unicodedata
import string
import os
import hashlib

# Alphabet and digits.
letters: str = string.ascii_letters + string.digits


class NestedNamespace(SimpleNamespace):
    def __init__(self, dictionary, **kwargs):
        super().__init__(**kwargs)
        for key, value in dictionary.items():
            if isinstance(value, dict):
                self.__setattr__(key, NestedNamespace(value))
            else:
                self.__setattr__(key, value)


def generate_passphrase(length: int = 32) -> str:
    """
    Generate entropy hex string.

    :param length: Passphrase length, default to 32.
    :type length: int

    :returns: str -- Passphrase hex string.

    >>> from swap.utils import generate_passphrase
    >>> generate_passphrase(length=32)
    "N39rPfa3QvF2Tm2nPyoBpXNiBFXJywTz"
    """

    return str().join(choice(letters) for _ in range(length))


def generate_entropy(strength: int = 128) -> str:
    """
    Generate entropy hex string.

    :param strength: Entropy strength, default to 128.
    :type strength: int

    :returns: str -- Entropy hex string.

    >>> from swap.utils import generate_entropy
    >>> generate_entropy(strength=128)
    "ee535b143b0d9d1f87546f9df0d06b1a"
    """

    if strength not in [128, 160, 192, 224, 256]:
        raise ValueError(
            "Strength should be one of the following "
            "[128, 160, 192, 224, 256], but it is not (%d)."
            % strength
        )
    return hexlify(os.urandom(strength // 8)).decode()


def generate_mnemonic(language: str = "english", strength: int = 128) -> str:
    """
    Generate mnemonic words.

    :param language: Mnemonic language, default to english.
    :type language: str
    :param strength: Entropy strength, default to 128.
    :type strength: int

    :returns: str -- Mnemonic words.

    >>> from swap.utils import generate_mnemonic
    >>> generate_mnemonic(language="french")
    "sceptre capter séquence girafe absolu relatif fleur zoologie muscle sirop saboter parure"
    """

    if language and language not in ["english", "french", "italian", "japanese",
                                     "chinese_simplified", "chinese_traditional", "korean", "spanish"]:
        raise ValueError("invalid language, use only this options english, french, "
                         "italian, spanish, chinese_simplified, chinese_traditional, japanese or korean languages.")
    if strength not in [128, 160, 192, 224, 256]:
        raise ValueError(
            "Strength should be one of the following "
            "[128, 160, 192, 224, 256], but it is not (%d)."
            % strength
        )

    return Mnemonic(language=language).generate(strength=strength)


def get_current_timestamp(plus: int = 0) -> int:
    """
    Get current timestamp.

    :param plus: Add seconds on current time, default to ``0``.
    :type plus: int

    :returns: int -- Current timestamp.

    >>> from swap.utils import get_current_timestamp
    >>> get_current_timestamp()
    1623869258
    """

    return int(datetime.timestamp(datetime.now())) \
        if plus == 0 else int(datetime.timestamp(datetime.now())) + plus


def is_entropy(entropy: str) -> bool:
    """
    Check entropy hex string.

    :param entropy: Mnemonic words.
    :type entropy: str

    :returns: bool -- Entropy valid/invalid.

    >>> from swap.utils import is_entropy
    >>> is_entropy(entropy="ee535b143b0d9d1f87546f9df0d06b1a")
    True
    """

    return len(unhexlify(entropy)) in [16, 20, 24, 28, 32]


def is_mnemonic(mnemonic: str, language: Optional[str] = None) -> bool:
    """
    Check mnemonic words.

    :param mnemonic: Mnemonic words.
    :type mnemonic: str
    :param language: Mnemonic language, default to None.
    :type language: str

    :returns: bool -- Mnemonic valid/invalid.

    >>> from swap.utils import is_mnemonic
    >>> is_mnemonic(mnemonic="sceptre capter séquence girafe absolu relatif fleur zoologie muscle sirop saboter parure")
    True
    """

    if language and language not in ["english", "french", "italian", "japanese",
                                     "chinese_simplified", "chinese_traditional", "korean", "spanish"]:
        raise ValueError("invalid language, use only this options english, french, "
                         "italian, spanish, chinese_simplified, chinese_traditional, japanese or korean languages.")
    try:
        mnemonic = unicodedata.normalize("NFKD", mnemonic)
        if language is None:
            for _language in ["english", "french", "italian",
                              "chinese_simplified", "chinese_traditional", "japanese", "korean", "spanish"]:
                valid = False
                if Mnemonic(language=_language).check(mnemonic=mnemonic) is True:
                    valid = True
                    break
            return valid
        else:
            return Mnemonic(language=language).check(mnemonic=mnemonic)
    except:
        return False


def get_entropy_strength(entropy: str) -> int:
    """
    Get entropy strength.

    :param entropy: Entropy hex string.
    :type entropy: str

    :returns: int -- Entropy strength.

    >>> from swap.utils import get_entropy_strength
    >>> get_entropy_strength(entropy="ee535b143b0d9d1f87546f9df0d06b1a")
    128
    """

    if not is_entropy(entropy=entropy):
        raise ValueError("Invalid entropy hex string.")

    length = len(unhexlify(entropy))
    if length == 16:
        return 128
    elif length == 20:
        return 160
    elif length == 24:
        return 192
    elif length == 28:
        return 224
    elif length == 32:
        return 256


def get_mnemonic_strength(mnemonic: str, language: Optional[str] = None) -> int:
    """
    Get mnemonic strength.

    :param mnemonic: Mnemonic words.
    :type mnemonic: str
    :param language: Mnemonic language, default to None.
    :type language: str

    :returns: int -- Mnemonic strength.

    >>> from swap.utils import get_mnemonic_strength
    >>> get_mnemonic_strength(mnemonic="sceptre capter séquence girafe absolu relatif fleur zoologie muscle sirop saboter parure")
    128
    """

    if not is_mnemonic(mnemonic=mnemonic, language=language):
        raise ValueError("Invalid mnemonic words.")

    words = len(unicodedata.normalize("NFKD", mnemonic).split(" "))
    if words == 12:
        return 128
    elif words == 15:
        return 160
    elif words == 18:
        return 192
    elif words == 21:
        return 224
    elif words == 24:
        return 256


def get_mnemonic_language(mnemonic: str) -> str:
    """
    Get mnemonic language.

    :param mnemonic: Mnemonic words.
    :type mnemonic: str

    :returns: str -- Mnemonic language.

    >>> from swap.utils import get_mnemonic_language
    >>> get_mnemonic_language(mnemonic="sceptre capter séquence girafe absolu relatif fleur zoologie muscle sirop saboter parure")
    "french"
    """

    if not is_mnemonic(mnemonic=mnemonic):
        raise ValueError("Invalid mnemonic words.")

    language = None
    mnemonic = unicodedata.normalize("NFKD", mnemonic)
    for _language in ["english", "french", "italian",
                      "chinese_simplified", "chinese_traditional", "japanese", "korean", "spanish"]:
        if Mnemonic(language=_language).check(mnemonic=mnemonic) is True:
            language = _language
            break
    return language


def entropy_to_mnemonic(entropy: str, language: str = "english") -> str:
    """
    Get mnemonic from entropy hex string.

    :param entropy: Entropy hex string.
    :type entropy: str
    :param language: Mnemonic language, default to english.
    :type language: str

    :returns: str -- Mnemonic words.

    >>> from swap.utils import entropy_to_mnemonic
    >>> entropy_to_mnemonic(entropy="ee535b143b0d9d1f87546f9df0d06b1a", language="korean")
    "학력 외침 주민 스위치 출연 연습 근본 여전히 울음 액수 귀신 마누라"
    """

    if not is_entropy(entropy=entropy):
        raise ValueError("Invalid entropy hex string.")

    if language and language not in ["english", "french", "italian", "japanese",
                                     "chinese_simplified", "chinese_traditional", "korean", "spanish"]:
        raise ValueError("Invalid language, use only this options english, french, "
                         "italian, spanish, chinese_simplified, chinese_traditional, japanese or korean languages.")

    return Mnemonic(language=language).to_mnemonic(unhexlify(entropy))


def mnemonic_to_entropy(mnemonic: str, language: Optional[str] = None) -> str:
    """
    Get entropy from mnemonic words.

    :param mnemonic: Mnemonic words.
    :type mnemonic: str
    :param language: Mnemonic language, default to english.
    :type language: str

    :returns: str -- Enropy hex string.

    >>> from swap.utils import mnemonic_to_entropy
    >>> mnemonic_to_entropy(mnemonic="학력 외침 주민 스위치 출연 연습 근본 여전히 울음 액수 귀신 마누라", language="korean")
    "ee535b143b0d9d1f87546f9df0d06b1a"
    """

    if not is_mnemonic(mnemonic=mnemonic, language=language):
        raise ValueError("Invalid mnemonic words.")

    mnemonic = unicodedata.normalize("NFKD", mnemonic)
    language = language if language else get_mnemonic_language(mnemonic=mnemonic)
    return Mnemonic(language=language).to_entropy(mnemonic).hex()


def sha256(data: Union[str, bytes]) -> str:
    """
    SHA256 hash.

    :param data: Any string/bytes data.
    :type data: str, bytes
    :returns: str -- SHA256 hash.

    >>> from swap.utils import sha256
    >>> sha256(data="Hello Meheret!")
    "3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb"
    """

    if isinstance(data, str):
        return hashlib.sha256(data.encode()).digest().hex()
    return hashlib.sha256(data).digest().hex()


def double_sha256(data: Union[str, bytes]) -> str:
    """
    Double SHA256 hash.

    :param data: Any string/bytes data.
    :type data: str, bytes
    :returns: str -- Double SHA256 hash.

    >>> from swap.utils import double_sha256
    >>> double_sha256(data="Hello Meheret!")
    "821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e0158"
    """
    return hashlib.sha256(unhexlify(sha256(data))).digest().hex()


def clean_transaction_raw(transaction_raw: str) -> str:
    """
    Clean transaction raw.

    :param transaction_raw: Any transaction raw.
    :type transaction_raw: str
    :returns: str -- Cleaned transaction raw.

    >>> from swap.utils import clean_transaction_raw
    >>> clean_transaction_raw(transaction_raw="eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcTluZHlseDAyc3lmd2Q3bnBlaGZ4ejRsZGRoenFzdmUyZnU2dmM3IiwgInJhdyI6ICIwNzAxMDAwMjAxNWYwMTVkODJlNjVmOTY0ZDNjMzUzMjU0OGRmZGU5Mzg0NjJmNTY2Yzk1ZDNjOTBlNmEzYTE4MmEwYjNiZGFlNDZhYTc5MGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MDg2ZjIwMzAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAxNWYwMTVkMDcwZDBlYjIyZDMyYjgyZDNkMmYzZmM0YmFmYjdhODVmNTIyOWY3ZmQ4OTA0MmQyZmYzMjU3Mzc1ZTQzZDNlYmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOGY1Zjc0ZjAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDE0NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDAwMTNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmQ4YjhmODUyMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAiaGFzaCI6ICI1MGIzMzZhYjZlMDU1ZDlkNGQ2NWE5ZjIyOTViNTMyNzBhYmQzODE2YzIzYmE0Yzk1NDg0MWYzOTlhYTc3MmQ1IiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbImY3ZDNhYTE4YjI5NWNkYTZmMmIxMTMyYzQyMzE5MzNjYzkyZjNiYWNhNzA1OTc0YzVkZTM3OGY5YjY5NWYwZTIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9LCB7ImRhdGFzIjogWyJjYTYxNWJhMmM3MjllNDYzZmJmNzlhMTE0MTkxNzYyNjFiMWJmNmJlNDQ4MTMzMzVkMmIyNTZlOGE3YmJjZWVlIl0sICJwdWJsaWNfa2V5IjogIjkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieXRvbV9mdW5kX3Vuc2lnbmVkIn0")
    "eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcTluZHlseDAyc3lmd2Q3bnBlaGZ4ejRsZGRoenFzdmUyZnU2dmM3IiwgInJhdyI6ICIwNzAxMDAwMjAxNWYwMTVkODJlNjVmOTY0ZDNjMzUzMjU0OGRmZGU5Mzg0NjJmNTY2Yzk1ZDNjOTBlNmEzYTE4MmEwYjNiZGFlNDZhYTc5MGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MDg2ZjIwMzAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAxNWYwMTVkMDcwZDBlYjIyZDMyYjgyZDNkMmYzZmM0YmFmYjdhODVmNTIyOWY3ZmQ4OTA0MmQyZmYzMjU3Mzc1ZTQzZDNlYmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOGY1Zjc0ZjAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDE0NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDAwMTNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmQ4YjhmODUyMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAiaGFzaCI6ICI1MGIzMzZhYjZlMDU1ZDlkNGQ2NWE5ZjIyOTViNTMyNzBhYmQzODE2YzIzYmE0Yzk1NDg0MWYzOTlhYTc3MmQ1IiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbImY3ZDNhYTE4YjI5NWNkYTZmMmIxMTMyYzQyMzE5MzNjYzkyZjNiYWNhNzA1OTc0YzVkZTM3OGY5YjY5NWYwZTIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9LCB7ImRhdGFzIjogWyJjYTYxNWJhMmM3MjllNDYzZmJmNzlhMTE0MTkxNzYyNjFiMWJmNmJlNDQ4MTMzMzVkMmIyNTZlOGE3YmJjZWVlIl0sICJwdWJsaWNfa2V5IjogIjkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieXRvbV9mdW5kX3Vuc2lnbmVkIn0="
    """
    return str(transaction_raw + "=" * (-len(transaction_raw) % 4))
