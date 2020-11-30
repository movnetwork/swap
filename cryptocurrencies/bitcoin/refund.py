#!/usr/bin/env python3

from swap.providers.bitcoin.wallet import Wallet, DEFAULT_PATH
from swap.providers.bitcoin.transaction import RefundTransaction
from swap.providers.bitcoin.solver import RefundSolver
from swap.providers.bitcoin.signature import RefundSignature
from swap.providers.bitcoin.utils import (
    submit_transaction_raw, amount_converter
)

import json

# Choose network mainnet or testnet
NETWORK: str = "testnet"
# Bitcoin funded transaction id/hash
TRANSACTION_ID: str = "5a9c45b067b26edb6ea3e735d20851efe23fe0653ad15d84276f5f8c9af32318"
# Bitcoin sender wallet mnemonic
SENDER_MNEMONIC: str = "indicate warm sock mistake code spot acid ribbon sing over taxi toast"
# Witness Hash Time Lock Contract (HTLC) bytecode
BYTECODE: str = "63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876" \
                "a914acf8419eecab574c494febbe03fd07fdae7bf2f488ac6702e803b27576a9141d0f671c" \
                "26a3ef7a865d1eda0fbd085e98adcc2388ac68"
# Bitcoin refund amount
AMOUNT: int = amount_converter(0.0001, "BTC2SATOSHI")

print("=" * 10, "Sender Bitcoin Account")

# Initialize Bitcoin sender wallet
sender_wallet: Wallet = Wallet(network=NETWORK)
# Get Bitcoin sender wallet from mnemonic
sender_wallet.from_mnemonic(mnemonic=SENDER_MNEMONIC)
# Drive Bitcoin sender wallet from path
sender_wallet.from_path(path=DEFAULT_PATH)

# Print some Bitcoin sender wallet info's
print("Private Key:", sender_wallet.private_key())
print("Public Key:", sender_wallet.public_key())
print("Wallet Important Format (WIF):", sender_wallet.wif())
print("Path:", sender_wallet.path())
print("Address:", sender_wallet.address())
print("Balance:", sender_wallet.balance())

print("=" * 10, "Unsigned Refund Transaction")

# Initialize refund transaction
unsigned_refund_transaction: RefundTransaction = RefundTransaction(network=NETWORK, version=2)
# Build refund transaction
unsigned_refund_transaction.build_transaction(
    address=sender_wallet.address(),
    transaction_id=TRANSACTION_ID,
    amount=AMOUNT
)

print("Unsigned Refund Transaction Fee:", unsigned_refund_transaction.fee())
print("Unsigned Refund Transaction Hash:", unsigned_refund_transaction.hash())
print("Unsigned Refund Transaction Main Raw:", unsigned_refund_transaction.raw())
# print("Unsigned Refund Transaction Json:", json.dumps(unsigned_refund_transaction.json(), indent=4))
print("Unsigned Refund Transaction Type:", unsigned_refund_transaction.type())

unsigned_refund_transaction_raw: str = unsigned_refund_transaction.transaction_raw()
print("Unsigned Refund Transaction Raw:", unsigned_refund_transaction_raw)

print("=" * 10, "Signed Refund Transaction")

# Initialize refund solver
refund_solver: RefundSolver = RefundSolver(
    root_xprivate_key=sender_wallet.root_xprivate_key(),
    bytecode=BYTECODE,
    sequence=1000  # Default to 1000
)

# Sing unsigned refund transaction
signed_refund_transaction: RefundTransaction = unsigned_refund_transaction.sign(refund_solver)

print("Signed Refund Transaction Fee:", signed_refund_transaction.fee())
print("Signed Refund Transaction Hash:", signed_refund_transaction.hash())
print("Signed Refund Transaction Main Raw:", signed_refund_transaction.raw())
# print("Signed Refund Transaction Json:", json.dumps(signed_refund_transaction.json(), indent=4))
print("Signed Refund Transaction Type:", signed_refund_transaction.type())

signed_refund_transaction_raw: str = signed_refund_transaction.transaction_raw()
print("Signed Refund Transaction Raw:", signed_refund_transaction_raw)

print("=" * 10, "Refund Signature")

# Initialize refund signature
refund_signature = RefundSignature(network=NETWORK)
# Sing unsigned refund transaction raw
refund_signature.sign(
    transaction_raw=unsigned_refund_transaction_raw,
    solver=refund_solver
)

print("Refund Signature Fee:", refund_signature.fee())
print("Refund Signature Hash:", refund_signature.hash())
print("Refund Signature Main Raw:", refund_signature.raw())
# print("Refund Signature Json:", json.dumps(refund_signature.json(), indent=4))
print("Refund Signature Type:", refund_signature.type())

signed_refund_signature_transaction_raw: str = refund_signature.transaction_raw()
print("Refund Signature Transaction Raw:", signed_refund_signature_transaction_raw)

# Check both signed refund transaction raws are equal
assert signed_refund_transaction_raw == signed_refund_signature_transaction_raw

# Submit refund transaction raw
# print("\nSubmitted Refund Transaction:", json.dumps(submit_transaction_raw(
#     transaction_raw=signed_refund_transaction_raw  # Or signed_refund_signature_transaction_raw
# ), indent=4))
