#!/usr/bin/env python3

from swap.providers.xinfin.wallet import (
    Wallet, DEFAULT_PATH
)
from swap.providers.xinfin.transaction import NormalTransaction
from swap.providers.xinfin.signature import NormalSignature
from swap.providers.xinfin.solver import NormalSolver
from swap.providers.xinfin.utils import (
    amount_unit_converter, submit_transaction_raw
)

import json

# Choose network mainnet, apothem or testnet
NETWORK: str = "apothem"
# XinFin sender wallet mnemonic
SENDER_MNEMONIC: str = "unfair divorce remind addict add roof park clown build renew illness fault"
# XinFin recipient address and amount
RECIPIENT: dict = {
    "xdcf8D43806260CFc6cC79fB408BA1897054667F81C": amount_unit_converter(0.1, "XDC2Wei")
}

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

print("=" * 10, "Unsigned Normal Transaction")

# Initialize normal transaction
unsigned_normal_transaction: NormalTransaction = NormalTransaction(network=NETWORK)
# Build normal transaction
unsigned_normal_transaction.build_transaction(
    address=sender_wallet.address(), recipient=RECIPIENT
)

print("Unsigned Normal Transaction Fee:", unsigned_normal_transaction.fee())
print("Unsigned Normal Transaction Hash:", unsigned_normal_transaction.hash())
print("Unsigned Normal Transaction Raw:", unsigned_normal_transaction.raw())
# print("Unsigned Normal Transaction Json:", json.dumps(unsigned_normal_transaction.json(), indent=4))
print("Unsigned Normal Transaction Signature:", json.dumps(unsigned_normal_transaction.signature(), indent=4))
print("Unsigned Normal Transaction Type:", unsigned_normal_transaction.type())

unsigned_normal_transaction_raw: str = unsigned_normal_transaction.transaction_raw()
print("Unsigned Normal Transaction Raw:", unsigned_normal_transaction_raw)

print("=" * 10, "Signed Normal Transaction")

# Initialize normal solver
normal_solver: NormalSolver = NormalSolver(
    xprivate_key=sender_wallet.root_xprivate_key(), 
    path=sender_wallet.path()
)

# Sing unsigned normal transaction
signed_normal_transaction: NormalTransaction = unsigned_normal_transaction.sign(solver=normal_solver)

print("Signed Normal Transaction Fee:", signed_normal_transaction.fee())
print("Signed Normal Transaction Hash:", signed_normal_transaction.hash())
print("Signed Normal Transaction Main Raw:", signed_normal_transaction.raw())
# print("Signed Normal Transaction Json:", json.dumps(signed_normal_transaction.json(), indent=4))
print("Signed Normal Transaction Signature:", json.dumps(signed_normal_transaction.signature(), indent=4))
print("Signed Normal Transaction Type:", signed_normal_transaction.type())

signed_normal_transaction_raw: str = signed_normal_transaction.transaction_raw()
print("Signed Normal Transaction Raw:", signed_normal_transaction_raw)

print("=" * 10, "Normal Signature")

# Initialize normal signature
normal_signature: NormalSignature = NormalSignature(network=NETWORK)
# Sign unsigned normal transaction raw
normal_signature.sign(
    transaction_raw=unsigned_normal_transaction_raw,
    solver=normal_solver
)

print("Normal Signature Fee:", normal_signature.fee())
print("Normal Signature Hash:", normal_signature.hash())
print("Normal Signature Raw:", normal_signature.raw())
# print("Normal Signature Json:", json.dumps(normal_signature.json(), indent=4))
print("Normal Signature Signature:", json.dumps(normal_signature.signature(), indent=4))
print("Normal Signature Type:", normal_signature.type())

signed_normal_signature_transaction_raw: str = normal_signature.transaction_raw()
print("Normal Signature Transaction Raw:", signed_normal_signature_transaction_raw)

# Check both signed normal transaction raws are equal
assert signed_normal_transaction_raw == signed_normal_signature_transaction_raw

# Submit normal transaction raw
# print("\nSubmitted Normal Transaction:", json.dumps(submit_transaction_raw(
#     transaction_raw=signed_normal_transaction_raw  # Or signed_normal_signature_transaction_raw
# ), indent=4))
