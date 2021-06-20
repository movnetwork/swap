#!/usr/bin/env python3

from swap.providers.ethereum.wallet import Wallet, DEFAULT_BIP44_PATH
from swap.providers.ethereum.transaction import RefundTransaction
from swap.providers.ethereum.signature import RefundSignature
from swap.providers.ethereum.solver import RefundSolver
from swap.providers.ethereum.utils import submit_transaction_raw

import json

# Choose network mainnet or testnet
NETWORK: str = "testnet"
# HTLC Ethereum contract address
CONTRACT_ADDRESS: str = "0xeaEaC81da5E386E8Ca4De1e64d40a10E468A5b40"
# Ethereum sender wallet mnemonic
RECIPIENT_MNEMONIC: str = "unfair divorce remind addict add roof park clown build renew illness fault"
# Derivation for sender wallet mnemonic
ACCOUNT, CHANGE, ADDRESS = 0, False, 0
# Funded transaction hash/id
TRANSACTION_HASH: str = "0x20f7807242dd6e4edc5855324a5e1eb679be153f786930cd3cc9b97411ff1fac"

print("=" * 10, "Sender Ethereum Account")

# Initialize Ethereum sender wallet
wallet: Wallet = Wallet(network=NETWORK)
# Get Ethereum sender wallet from mnemonic
wallet.from_mnemonic(mnemonic=RECIPIENT_MNEMONIC)
# Drive Ethereum sender wallet from path
wallet.from_path(
    path=DEFAULT_BIP44_PATH.format(
        account=ACCOUNT, change=(1 if CHANGE else 0), address=ADDRESS
    )
)

# Print some Ethereum sender wallet info's
print("Root XPrivate Key:", wallet.root_xprivate_key())
print("Root XPublic Key:", wallet.root_xpublic_key())
print("Private Key:", wallet.private_key())
print("Public Key:", wallet.public_key())
print("Path:", wallet.path())
print("Address:", wallet.address())
print("Balance:", wallet.balance(unit="Ether"), "Ether")

print("=" * 10, "Unsigned Refund Transaction")

# Initialize refund transaction
unsigned_refund_transaction: RefundTransaction = RefundTransaction(network=NETWORK)
# Build refund transaction
unsigned_refund_transaction.build_transaction(
    transaction_hash=TRANSACTION_HASH,
    address=wallet.address(),
    contract_address=CONTRACT_ADDRESS
)

print("Unsigned Refund Transaction Fee:", unsigned_refund_transaction.fee())
print("Unsigned Refund Transaction Hash:", unsigned_refund_transaction.hash())
print("Unsigned Refund Transaction Raw:", unsigned_refund_transaction.raw())
print("Unsigned Refund Transaction Json:", unsigned_refund_transaction.json())
print("Unsigned Refund Transaction Signature:", unsigned_refund_transaction.signature())
print("Unsigned Refund Transaction Type:", unsigned_refund_transaction.type())

unsigned_refund_transaction_raw: str = unsigned_refund_transaction.transaction_raw()
print("Unsigned Refund Transaction Raw:", unsigned_refund_transaction_raw)

print("=" * 10, "Signed Refund Transaction")

# Initialize refund solver
refund_solver: RefundSolver = RefundSolver(
    xprivate_key=wallet.root_xprivate_key(), path=DEFAULT_BIP44_PATH.format(
        account=ACCOUNT, change=(1 if CHANGE else 0), address=ADDRESS
    )
)

# Sing unsigned refund transaction
signed_refund_transaction: RefundTransaction = unsigned_refund_transaction.sign(solver=refund_solver)

print("Signed Refund Transaction Fee:", signed_refund_transaction.fee())
print("Signed Refund Transaction Hash:", signed_refund_transaction.hash())
print("Signed Refund Transaction Json:", signed_refund_transaction.json())
print("Signed Refund Transaction Main Raw:", signed_refund_transaction.raw())
print("Signed Refund Transaction Signature:", signed_refund_transaction.signature())
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
print("Refund Signature Json:", refund_signature.json())
print("Refund Signature Raw:", refund_signature.raw())
print("Refund Signature Transaction Signature:", refund_signature.signature())
print("Refund Signature Type:", refund_signature.type())

signed_refund_signature_transaction_raw: str = refund_signature.transaction_raw()
print("Refund Signature Transaction Raw:", signed_refund_signature_transaction_raw)

# Check both signed refund transaction raws are equal
assert signed_refund_transaction_raw == signed_refund_signature_transaction_raw

# Submit refund transaction raw
# print("\nSubmitted Refund Transaction:", json.dumps(submit_transaction_raw(
#     transaction_raw=signed_refund_transaction_raw  # Or signed_refund_signature_transaction_raw
# ), indent=4))
