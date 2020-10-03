#!/usr/bin/env python3

from swap.providers.bitcoin.wallet import Wallet
from swap.providers.bitcoin.transaction import ClaimTransaction
from swap.providers.bitcoin.solver import ClaimSolver
from swap.providers.bitcoin.signature import ClaimSignature
from swap.providers.bitcoin.utils import (
    submit_transaction_raw, amount_converter
)

import json

# Bitcoin network
NETWORK: str = "testnet"
# Bitcoin funded transaction id/hash
TRANSACTION_ID: str = "5a9c45b067b26edb6ea3e735d20851efe23fe0653ad15d84276f5f8c9af32318"
# Bitcoin recipient wallet mnemonic
RECIPIENT_MNEMONIC: str = "hint excuse upgrade sleep easily deputy erase cluster section other ugly limit"
# Bitcoin wallet derivation path
PATH: str = "m/44'/0'/0'/0/0"
# Witness Hash Time Lock Contract (HTLC) bytecode
BYTECODE: str = "63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876" \
                "a914acf8419eecab574c494febbe03fd07fdae7bf2f488ac6702e803b27576a9141d0f671c" \
                "26a3ef7a865d1eda0fbd085e98adcc2388ac68"
# Bitcoin claim amount
AMOUNT: int = amount_converter(0.0001, "BTC2SATOSHI")

print("=" * 10, "Recipient Bitcoin Account")

# Initialize Bitcoin recipient wallet
recipient_wallet: Wallet = Wallet(network=NETWORK)
# Get Bitcoin recipient wallet from mnemonic
recipient_wallet.from_mnemonic(mnemonic=RECIPIENT_MNEMONIC)
# Drive Bitcoin recipient wallet from path
recipient_wallet.from_path(path=PATH)

# Print some Bitcoin recipient wallet info's
print("Private Key:", recipient_wallet.private_key())
print("Public Key:", recipient_wallet.public_key())
print("Wallet Important Format (WIF):", recipient_wallet.wif())
print("Path:", recipient_wallet.path())
print("Address:", recipient_wallet.address())
print("Balance:", recipient_wallet.balance())

print("=" * 10, "Unsigned Claim Transaction")

# Initialize claim transaction
unsigned_claim_transaction: ClaimTransaction = ClaimTransaction(version=2, network=NETWORK)
# Build claim transaction
unsigned_claim_transaction.build_transaction(
    address=recipient_wallet.address(),
    transaction_id=TRANSACTION_ID,
    amount=AMOUNT
)

print("Unsigned Claim Transaction Fee:", unsigned_claim_transaction.fee())
print("Unsigned Claim Transaction Hash:", unsigned_claim_transaction.hash())
print("Unsigned Claim Transaction Main Raw:", unsigned_claim_transaction.raw())
# print("Unsigned Claim Transaction Json:", json.dumps(unsigned_claim_transaction.json(), indent=4))
print("Unsigned Claim Transaction Type:", unsigned_claim_transaction.type())

unsigned_claim_transaction_raw: str = unsigned_claim_transaction.transaction_raw()
print("Unsigned Claim Transaction Raw:", unsigned_claim_transaction_raw)

print("=" * 10, "Signed Claim Transaction")

# Initialize claim solver
claim_solver = ClaimSolver(
    root_xprivate_key=recipient_wallet.root_xprivate_key(),
    secret_key="Hello Meheret!",
    bytecode=BYTECODE
)

# Sing unsigned claim transaction
signed_claim_transaction: ClaimTransaction = unsigned_claim_transaction.sign(solver=claim_solver)

print("Signed Claim Transaction Fee:", signed_claim_transaction.fee())
print("Signed Claim Transaction Hash:", signed_claim_transaction.hash())
print("Signed Claim Transaction Raw:", signed_claim_transaction.raw())
# print("Signed Claim Transaction Json:", json.dumps(signed_claim_transaction.json(), indent=4))
print("Signed Claim Transaction Type:", signed_claim_transaction.type())

signed_claim_transaction_raw: str = signed_claim_transaction.transaction_raw()
print("Signed Claim Transaction Raw:", signed_claim_transaction_raw)

print("=" * 10, "Claim Signature")

# Initialize claim signature
claim_signature: ClaimSignature = ClaimSignature(network=NETWORK)
# Sing unsigned claim transaction raw
claim_signature.sign(
    transaction_raw=unsigned_claim_transaction_raw,
    solver=claim_solver
)

print("Claim Signature Fee:", claim_signature.fee())
print("Claim Signature Hash:", claim_signature.hash())
print("Claim Signature Raw:", claim_signature.raw())
# print("Claim Signature Json:", json.dumps(claim_signature.json(), indent=4))
print("Claim Signature Type:", claim_signature.type())

signed_claim_signature_transaction_raw: str = claim_signature.transaction_raw()
print("Claim Signature Transaction Raw:", signed_claim_signature_transaction_raw)

# Check both signed claim transaction raws are equal
assert signed_claim_transaction_raw == signed_claim_signature_transaction_raw

# Submit claim transaction raw
# print("\nSubmitted Claim Transaction:", submit_transaction_raw(
#     transaction_raw=signed_claim_transaction_raw  # Or signed_claim_signature_transaction_raw
# ))
