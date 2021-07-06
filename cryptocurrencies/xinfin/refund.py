#!/usr/bin/env python3

from swap.providers.xinfin.wallet import (
    Wallet, DEFAULT_PATH
)
from swap.providers.xinfin.transaction import RefundTransaction
from swap.providers.xinfin.signature import RefundSignature
from swap.providers.xinfin.solver import RefundSolver
from swap.providers.xinfin.utils import submit_transaction_raw

import json

# Choose network mainnet or testnet
NETWORK: str = "mainnet"
# XinFin HTLC contract address
CONTRACT_ADDRESS: str = "xdc656869af3Ec1E8b2982Fc370A0526541C0Ceb90B"
# XinFin funded transaction hash/id
TRANSACTION_HASH: str = "0x0cfc885274ad38ff880f0c682e5ccae7f5101d5209f5599b41645612bafaa56a"
# XinFin sender wallet mnemonic
SENDER_MNEMONIC: str = "unfair divorce remind addict add roof park clown build renew illness fault"

print("=" * 10, "Sender XinFin Account")

# Initialize XinFin sender wallet
sender_wallet: Wallet = Wallet(network=NETWORK)
# Get XinFin sender wallet from mnemonic
sender_wallet.from_mnemonic(mnemonic=SENDER_MNEMONIC)
# Drive XinFin sender wallet from path
sender_wallet.from_path(path=DEFAULT_PATH)

# Print some XinFin sender wallet info's
print("Root XPrivate Key:", sender_wallet.root_xprivate_key())
print("Root XPublic Key:", sender_wallet.root_xpublic_key())
print("Private Key:", sender_wallet.private_key())
print("Public Key:", sender_wallet.public_key())
print("Path:", sender_wallet.path())
print("Address:", sender_wallet.address())
print("Balance:", sender_wallet.balance(unit="XDC"), "XDC")

print("=" * 10, "Unsigned Refund Transaction")

# Initialize refund transaction
unsigned_refund_transaction: RefundTransaction = RefundTransaction(network=NETWORK)
# Build refund transaction
unsigned_refund_transaction.build_transaction(
    transaction_hash=TRANSACTION_HASH,
    address=sender_wallet.address(),
    contract_address=CONTRACT_ADDRESS
)

print("Unsigned Refund Transaction Fee:", unsigned_refund_transaction.fee())
print("Unsigned Refund Transaction Hash:", unsigned_refund_transaction.hash())
print("Unsigned Refund Transaction Main Raw:", unsigned_refund_transaction.raw())
# print("Unsigned Refund Transaction Json:", json.dumps(unsigned_refund_transaction.json(), indent=4))
print("Unsigned Refund Transaction Signature:", json.dumps(unsigned_refund_transaction.signature(), indent=4))
print("Unsigned Refund Transaction Type:", unsigned_refund_transaction.type())

unsigned_refund_transaction_raw: str = unsigned_refund_transaction.transaction_raw()
print("Unsigned Refund Transaction Raw:", unsigned_refund_transaction_raw)

print("=" * 10, "Signed Refund Transaction")

# Initialize refund solver
refund_solver: RefundSolver = RefundSolver(
    xprivate_key=sender_wallet.root_xprivate_key(),
    path=sender_wallet.path()
)

# Sing unsigned refund transaction
signed_refund_transaction: RefundTransaction = unsigned_refund_transaction.sign(solver=refund_solver)

print("Signed Refund Transaction Fee:", signed_refund_transaction.fee())
print("Signed Refund Transaction Hash:", signed_refund_transaction.hash())
print("Signed Refund Transaction Main Raw:", signed_refund_transaction.raw())
# print("Signed Refund Transaction Json:", json.dumps(signed_refund_transaction.json(), indent=4))
print("Signed Refund Transaction Signature:", json.dumps(signed_refund_transaction.signature(), indent=4))
print("Signed Refund Transaction Type:", signed_refund_transaction.type())

signed_refund_transaction_raw: str = signed_refund_transaction.transaction_raw()
print("Signed Refund Transaction Raw:", signed_refund_transaction_raw)

print("=" * 10, "Refund Signature")

# Initialize refund signature
refund_signature: RefundSignature = RefundSignature(network=NETWORK)
# Sign unsigned refund transaction raw
refund_signature.sign(
    transaction_raw=unsigned_refund_transaction_raw,
    solver=refund_solver
)

print("Refund Signature Fee:", refund_signature.fee())
print("Refund Signature Hash:", refund_signature.hash())
print("Refund Signature Main Raw:", refund_signature.raw())
# print("Refund Signature Json:", json.dumps(refund_signature.json(), indent=4))
print("Refund Signature Signature:", json.dumps(refund_signature.signature(), indent=4))
print("Refund Signature Type:", refund_signature.type())

signed_refund_signature_transaction_raw: str = refund_signature.transaction_raw()
print("Refund Signature Transaction Raw:", signed_refund_signature_transaction_raw)

# Check both signed refund transaction raws are equal
assert signed_refund_transaction_raw == signed_refund_signature_transaction_raw

# Submit refund transaction raw
# print("\nSubmitted Refund Transaction:", json.dumps(submit_transaction_raw(
#     transaction_raw=signed_refund_transaction_raw  # Or signed_refund_signature_transaction_raw
# ), indent=4))
