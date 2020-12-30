#!/usr/bin/env python3

from swap.providers.bitcoin.wallet import Wallet, DEFAULT_PATH
from swap.providers.bitcoin.transaction import ClaimTransaction
from swap.providers.bitcoin.solver import ClaimSolver
from swap.providers.bitcoin.signature import ClaimSignature
from swap.providers.bitcoin.utils import submit_transaction_raw

import json

# Choose network mainnet or testnet
NETWORK: str = "testnet"
# Bitcoin funded transaction id/hash
TRANSACTION_ID: str = "868f81fd172b8f1d24e0c195af011489c3a7948513521d4b6257b8b5fb2ef409"
# Bitcoin recipient wallet mnemonic
RECIPIENT_MNEMONIC: str = "hint excuse upgrade sleep easily deputy erase cluster section other ugly limit"
# Witness Hash Time Lock Contract (HTLC) bytecode
BYTECODE: str = "63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e0" \
                "1588876a9140e259e08f2ec9fc99a92b6f66fdfcb3c7914fd6888ac6702e803b275" \
                "76a91433ecab3d67f0e2bde43e52f41ec1ecbdc73f11f888ac68"
# Secret key of HTLC
SECRET_KEY: str = "Hello Meheret!"
# Bitcoin maximum withdraw amount
MAX_AMOUNT: bool = True

print("=" * 10, "Recipient Bitcoin Account")

# Initialize Bitcoin recipient wallet
recipient_wallet: Wallet = Wallet(network=NETWORK)
# Get Bitcoin recipient wallet from mnemonic
recipient_wallet.from_mnemonic(mnemonic=RECIPIENT_MNEMONIC)
# Drive Bitcoin recipient wallet from path
recipient_wallet.from_path(path=DEFAULT_PATH)

# Print some Bitcoin recipient wallet info's
print("Root XPrivate Key:", recipient_wallet.root_xprivate_key())
print("Root XPublic Key:", recipient_wallet.root_xprivate_key())
print("Private Key:", recipient_wallet.private_key())
print("Public Key:", recipient_wallet.public_key())
print("Address:", recipient_wallet.address())
print("Balance:", recipient_wallet.balance(unit="BTC"), "BTC")

print("=" * 10, "Unsigned Claim Transaction")

# Initialize claim transaction
unsigned_claim_transaction: ClaimTransaction = ClaimTransaction(network=NETWORK, version=2)
# Build claim transaction
unsigned_claim_transaction.build_transaction(
    address=recipient_wallet.address(),
    transaction_id=TRANSACTION_ID,
    max_amount=MAX_AMOUNT
)

print("Unsigned Claim Transaction Fee:", unsigned_claim_transaction.fee(unit="SATOSHI"), "SATOSHI")
print("Unsigned Claim Transaction Hash:", unsigned_claim_transaction.hash())
print("Unsigned Claim Transaction Main Raw:", unsigned_claim_transaction.raw())
# print("Unsigned Claim Transaction Json:", json.dumps(unsigned_claim_transaction.json(), indent=4))
print("Unsigned Claim Transaction Type:", unsigned_claim_transaction.type())

unsigned_claim_transaction_raw: str = unsigned_claim_transaction.transaction_raw()
print("Unsigned Claim Transaction Raw:", unsigned_claim_transaction_raw)

print("=" * 10, "Signed Claim Transaction")

# Initialize claim solver
claim_solver: ClaimSolver = ClaimSolver(
    root_xprivate_key=recipient_wallet.root_xprivate_key(),
    secret_key=SECRET_KEY,
    bytecode=BYTECODE
)

# Sing unsigned claim transaction
signed_claim_transaction: ClaimTransaction = unsigned_claim_transaction.sign(solver=claim_solver)

print("Signed Claim Transaction Fee:", signed_claim_transaction.fee(unit="SATOSHI"), "SATOSHI")
print("Signed Claim Transaction Hash:", signed_claim_transaction.hash())
print("Signed Claim Transaction Main Raw:", signed_claim_transaction.raw())
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

print("Claim Signature Fee:", claim_signature.fee(unit="SATOSHI"), "SATOSHI")
print("Claim Signature Hash:", claim_signature.hash())
print("Claim Signature Main Raw:", claim_signature.raw())
# print("Claim Signature Json:", json.dumps(claim_signature.json(), indent=4))
print("Claim Signature Type:", claim_signature.type())

signed_claim_signature_transaction_raw: str = claim_signature.transaction_raw()
print("Claim Signature Transaction Raw:", signed_claim_signature_transaction_raw)

# Check both signed claim transaction raws are equal
assert signed_claim_transaction_raw == signed_claim_signature_transaction_raw

# Submit claim transaction raw
# print("\nSubmitted Claim Transaction:", json.dumps(submit_transaction_raw(
#     transaction_raw=signed_claim_transaction_raw  # Or signed_claim_signature_transaction_raw
# ), indent=4))
