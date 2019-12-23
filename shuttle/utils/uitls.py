from mnemonic import Mnemonic
from random import choice

import string

# Alphabet and digits.
letters = string.ascii_letters + string.digits


# Generate random letters.
def generate_passphrase(length=32):
    return str().join(choice(letters) for _ in range(length))


# Generate random 12 words.
def generate_mnemonic(language="english"):   # japanese
    return Mnemonic(language=language).generate()
