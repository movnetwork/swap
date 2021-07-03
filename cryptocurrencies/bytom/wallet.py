#!/usr/bin/env python3

from swap.providers.bytom.wallet import (
    Wallet, DEFAULT_PATH
)
from swap.providers.bytom.assets import BTM as ASSET
from swap.utils import (
    generate_entropy, generate_passphrase
)

# Choose network mainnet, solonet or testnet
NETWORK: str = "mainnet"  # Default to mainnet
# Choose strength 128, 160, 192, 224 or 256
STRENGTH: int = 160  # Default is 128
# Choose language english, french, italian, spanish, chinese_simplified, chinese_traditional, japanese or korean
LANGUAGE: str = "english"  # Default is english
# Set passphrase length
LENGTH: int = 32  # Default is 32
# Generate new entropy hex string
ENTROPY: str = generate_entropy(strength=STRENGTH)
# Generate new passphrase
PASSPHRASE: str = generate_passphrase(length=LENGTH)

# Initialize Bytom wallet
wallet: Wallet = Wallet(network=NETWORK)
# Get Bytom wallet from entropy
wallet.from_entropy(
    entropy=ENTROPY, language=LANGUAGE, passphrase=PASSPHRASE
)
# Drive Bytom wallet from path
wallet.from_path(path=DEFAULT_PATH)

# Print all Bytom wallet info's
print("Strength:", wallet.strength())
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
# print("GUID:", wallet.guid())
print("Indexes:", wallet.indexes())
print("Path:", wallet.path())
print("Private Key:", wallet.private_key())
print("Public Key:", wallet.public_key())
print("Program:", wallet.program())
print("Address:", wallet.address())
print("Balance:", wallet.balance(asset=ASSET, unit="BTM"), "BTM")
print("UTXO's:", wallet.utxos(asset=ASSET))
