#!/usr/bin/env python3

from swap.providers.bitcoin.wallet import (
    Wallet, DEFAULT_PATH
)
from swap.providers.bitcoin.transaction import WithdrawTransaction
from swap.providers.bitcoin.solver import WithdrawSolver
from swap.providers.bitcoin.signature import WithdrawSignature
from swap.providers.bitcoin.utils import submit_transaction_raw

import json

# Choose network mainnet or testnet
NETWORK: str = "testnet"
# Bitcoin funded transaction hash/id
TRANSACTION_HASH: str = "853a27875a51ba8290cf5e5b32a0e1bbc9273343ff2b65ffad949bce942b9379"
# Bitcoin recipient wallet mnemonic
RECIPIENT_MNEMONIC: str = "hint excuse upgrade sleep easily deputy erase cluster section other ugly limit"
# The preimage of HTLC contract
SECRET_KEY: str = "Hello Meheret!"
# Witness Hash Time Lock Contract (HTLC) bytecode
BYTECODE: str = "63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a9140e259e08f2" \
                "ec9fc99a92b6f66fdfcb3c7914fd6888ac67043e3be060b17576a91493162bcadf4406af6429b59958964f62" \
                "5d550fcd88ac68"

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
print("Path:", recipient_wallet.path())
print("Address:", recipient_wallet.address())
print("Balance:", recipient_wallet.balance(unit="BTC"), "BTC")

print("=" * 10, "Unsigned Withdraw Transaction")

# Initialize withdraw transaction
unsigned_withdraw_transaction: WithdrawTransaction = WithdrawTransaction(network=NETWORK, version=2)
# Build withdraw transaction
unsigned_withdraw_transaction.build_transaction(
    address=recipient_wallet.address(), transaction_hash=TRANSACTION_HASH
)

print("Unsigned Withdraw Transaction Fee:", unsigned_withdraw_transaction.fee(unit="Satoshi"), "Satoshi")
print("Unsigned Withdraw Transaction Hash:", unsigned_withdraw_transaction.hash())
print("Unsigned Withdraw Transaction Main Raw:", unsigned_withdraw_transaction.raw())
# print("Unsigned Withdraw Transaction Json:", json.dumps(unsigned_withdraw_transaction.json(), indent=4))
print("Unsigned Withdraw Transaction Type:", unsigned_withdraw_transaction.type())

unsigned_withdraw_transaction_raw: str = unsigned_withdraw_transaction.transaction_raw()
print("Unsigned Withdraw Transaction Raw:", unsigned_withdraw_transaction_raw)

print("=" * 10, "Signed Withdraw Transaction")

# Initialize withdraw solver
withdraw_solver: WithdrawSolver = WithdrawSolver(
    xprivate_key=recipient_wallet.root_xprivate_key(),
    path=recipient_wallet.path(),
    secret_key=SECRET_KEY,
    bytecode=BYTECODE
)

# Sing unsigned withdraw transaction
signed_withdraw_transaction: WithdrawTransaction = unsigned_withdraw_transaction.sign(solver=withdraw_solver)

print("Signed Withdraw Transaction Fee:", signed_withdraw_transaction.fee(unit="Satoshi"), "Satoshi")
print("Signed Withdraw Transaction Hash:", signed_withdraw_transaction.hash())
print("Signed Withdraw Transaction Main Raw:", signed_withdraw_transaction.raw())
# print("Signed Withdraw Transaction Json:", json.dumps(signed_withdraw_transaction.json(), indent=4))
print("Signed Withdraw Transaction Type:", signed_withdraw_transaction.type())

signed_withdraw_transaction_raw: str = signed_withdraw_transaction.transaction_raw()
print("Signed Withdraw Transaction Raw:", signed_withdraw_transaction_raw)

print("=" * 10, "Withdraw Signature")

# Initialize withdraw signature
withdraw_signature: WithdrawSignature = WithdrawSignature(network=NETWORK)
# Sing unsigned withdraw transaction raw
withdraw_signature.sign(
    transaction_raw=unsigned_withdraw_transaction_raw,
    solver=withdraw_solver
)

print("Withdraw Signature Fee:", withdraw_signature.fee(unit="Satoshi"), "Satoshi")
print("Withdraw Signature Hash:", withdraw_signature.hash())
print("Withdraw Signature Main Raw:", withdraw_signature.raw())
# print("Withdraw Signature Json:", json.dumps(withdraw_signature.json(), indent=4))
print("Withdraw Signature Type:", withdraw_signature.type())

signed_withdraw_signature_transaction_raw: str = withdraw_signature.transaction_raw()
print("Withdraw Signature Transaction Raw:", signed_withdraw_signature_transaction_raw)

# Check both signed withdraw transaction raws are equal
assert signed_withdraw_transaction_raw == signed_withdraw_signature_transaction_raw

# Submit withdraw transaction raw
# print("\nSubmitted Withdraw Transaction:", json.dumps(submit_transaction_raw(
#     transaction_raw=signed_withdraw_transaction_raw  # Or signed_withdraw_signature_transaction_raw
# ), indent=4))
