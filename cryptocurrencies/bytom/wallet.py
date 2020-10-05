#!/usr/bin/env python3

from swap.providers.bytom.wallet import Wallet
from swap.utils import generate_entropy

# Bytom network
# Choose only mainnet, solonet or testnet networks
NETWORK: str = "mainnet"  # Default to mainnet
# Entropy strength
# Choose only 128, 160, 192, 224 or 256 strengths
STRENGTH: int = 128  # Default to 128
# Bytom wallet entropy
ENTROPY: str = generate_entropy(strength=STRENGTH)
# Mnemonic language
# Choose only english, french, italian, spanish, chinese_simplified, chinese_traditional, japanese or korean languages
LANGUAGE: str = "spanish"  # Default to english
# Mnemonic password/passphrase
PASSPHRASE = None  # str("meherett")
# Bytom wallet derivation path
PATH: str = "m/44/153/1/0/1"

# Initialize Bytom wallet
wallet: Wallet = Wallet(network=NETWORK)
# Get Bytom wallet from entropy
wallet.from_entropy(entropy=ENTROPY, language=LANGUAGE, passphrase=PASSPHRASE)
# Drive Bytom wallet from path
wallet.from_path(path=PATH)

# Print all wallet info's
print("Entropy:", wallet.entropy())
print("Mnemonic:", wallet.mnemonic())
print("Language:", wallet.language())
print("Passphrase:", wallet.passphrase())
print("Seed:", wallet.seed())
print("XPrivate Key:", wallet.xprivate_key())
print("XPublic Key:", wallet.xpublic_key())
print("Expand XPrivate Key:", wallet.expand_xprivate_key())
print("Child XPrivate Key:", wallet.child_xprivate_key())
print("Child XPublic Key:", wallet.child_xpublic_key())
print("GUID:", wallet.guid())
print("Indexes:", wallet.indexes())
print("Path:", wallet.path())
print("Private Key:", wallet.private_key())
print("Public Key:", wallet.public_key())
print("Program:", wallet.program())
print("Address:", wallet.address())
print("Balance:", wallet.balance())
print("UTXO's:", wallet.utxos())
