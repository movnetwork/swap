#!/usr/bin/env python3

from mnemonic import Mnemonic
from random import choice

import string
import hashlib

# Alphabet and digits.
letters = string.ascii_letters + string.digits


# Generate random letters.
def generate_passphrase(length=32):
    return str().join(choice(letters) for _ in range(length))


# Generate random 12 words.
def generate_mnemonic(language="english"):   # japanese
    return Mnemonic(language=language).generate()


# SHA256 hash
def sha256(data):
    return hashlib.sha256(data).digest()


# Double SHA256 hash
def double_sha256(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()
