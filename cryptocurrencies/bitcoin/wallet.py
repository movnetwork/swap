#!/usr/bin/env python3

from swap.providers.bitcoin.wallet import Wallet
from swap.utils import generate_entropy

# Bitcoin network
# Choose only mainnet, solonet or testnet networks
NETWORK: str = "mainnet"  # Default to mainnet
# Entropy strength
# Choose only 128, 160, 192, 224 or 256 strengths
STRENGTH: int = 128  # Default to 128
# Bitcoin wallet entropy
ENTROPY: str = generate_entropy(strength=STRENGTH)
# Mnemonic language
# Choose only english, french, italian, spanish, chinese_simplified, chinese_traditional, japanese or korean languages
LANGUAGE: str = "korean"  # Default to english
# Bitcoin wallet derivation path
PATH: str = "m/44'/0'/0'/0/0"

# Initialize Bitcoin wallet
wallet: Wallet = Wallet(network=NETWORK)
# Get Bitcoin wallet from entropy
wallet.from_entropy(entropy=ENTROPY, language=LANGUAGE)
# Drive Bitcoin wallet from path
wallet.from_path(path=PATH)

# Print all wallet info's
print("Entropy:", wallet.entropy())
print("Mnemonic:", wallet.mnemonic())
print("Language:", wallet.language())
print("Passphrase:", wallet.passphrase())
print("Seed:", wallet.seed())
print("Root XPrivate Key:", wallet.root_xprivate_key())
print("Root XPublic Key:", wallet.root_xpublic_key())
print("XPrivate Key:", wallet.xprivate_key())
print("XPublic Key:", wallet.xpublic_key())
print("Uncompressed:", wallet.uncompressed())
print("Compressed:", wallet.compressed())
print("Chain Code:", wallet.chain_code())
print("Private Key:", wallet.private_key())
print("Public Key:", wallet.public_key())
print("Wallet Important Format (WIF):", wallet.wif())
print("Public Kay/Address Hash:", wallet.hash())
print("Pay to Public Key Hash (P2PKH):", wallet.p2pkh())
print("Finger Print:", wallet.finger_print())
print("Path:", wallet.path())
print("Address:", wallet.address())
print("Balance:", wallet.balance())
print("UTXO's:", wallet.utxos())
