#!/usr/bin/env python3

from swap.providers.ethereum.wallet import (
    Wallet, DEFAULT_PATH
)
from swap.providers.ethereum.transaction import WithdrawTransaction
from swap.providers.ethereum.signature import WithdrawSignature
from swap.providers.ethereum.solver import WithdrawSolver
from swap.providers.ethereum.utils import submit_transaction_raw

import json

# Choose network mainnet or testnet
NETWORK: str = "ropsten"
# Ethereum HTLC contract address
CONTRACT_ADDRESS: str = "0xE5cb615899436A490dBde26d7880A0C2502Fc676"
# Ethereum funded transaction hash/id
TRANSACTION_HASH: str = "0xa42f5c441c9ba006c6abcbdbb6e1a3f21e491a9803df127958ee5acd8e17b74e"
# Ethereum recipient wallet mnemonic
RECIPIENT_MNEMONIC: str = "hint excuse upgrade sleep easily deputy erase cluster section other ugly limit"
# The preimage of HTLC contract
SECRET_KEY: str = "Hello Meheret!"

print("=" * 10, "Recipient Ethereum Account")

# Initialize Ethereum recipient wallet
recipient_wallet: Wallet = Wallet(network=NETWORK)
# Get Ethereum recipient wallet from mnemonic
recipient_wallet.from_mnemonic(mnemonic=RECIPIENT_MNEMONIC)
# Drive Ethereum recipient wallet from path
recipient_wallet.from_path(path=DEFAULT_PATH)

# Print some Ethereum recipient wallet info's
print("Root XPrivate Key:", recipient_wallet.root_xprivate_key())
print("Root XPublic Key:", recipient_wallet.root_xpublic_key())
print("Private Key:", recipient_wallet.private_key())
print("Public Key:", recipient_wallet.public_key())
print("Path:", recipient_wallet.path())
print("Address:", recipient_wallet.address())
print("Balance:", recipient_wallet.balance(unit="Ether"), "Ether")

print("=" * 10, "Unsigned Withdraw Transaction")

# Initialize withdraw transaction
unsigned_withdraw_transaction: WithdrawTransaction = WithdrawTransaction(network=NETWORK)
# Build withdraw transaction
unsigned_withdraw_transaction.build_transaction(
    transaction_hash=TRANSACTION_HASH,
    address=recipient_wallet.address(),
    secret_key=SECRET_KEY,
    contract_address=CONTRACT_ADDRESS
)

print("Unsigned Withdraw Transaction Fee:", unsigned_withdraw_transaction.fee())
print("Unsigned Withdraw Transaction Hash:", unsigned_withdraw_transaction.hash())
print("Unsigned Withdraw Transaction Main Raw:", unsigned_withdraw_transaction.raw())
# print("Unsigned Withdraw Transaction Json:", json.dumps(unsigned_withdraw_transaction.json(), indent=4))
print("Unsigned Withdraw Transaction Signature:", json.dumps(unsigned_withdraw_transaction.signature(), indent=4))
print("Unsigned Withdraw Transaction Type:", unsigned_withdraw_transaction.type())

unsigned_withdraw_transaction_raw: str = unsigned_withdraw_transaction.transaction_raw()
print("Unsigned Withdraw Transaction Raw:", unsigned_withdraw_transaction_raw)

print("=" * 10, "Signed Withdraw Transaction")

# Initialize withdraw solver
withdraw_solver: WithdrawSolver = WithdrawSolver(
    xprivate_key=recipient_wallet.root_xprivate_key(), 
    path=recipient_wallet.path()
)

# Sing unsigned withdraw transaction
signed_withdraw_transaction: WithdrawTransaction = unsigned_withdraw_transaction.sign(solver=withdraw_solver)

print("Signed Withdraw Transaction Fee:", signed_withdraw_transaction.fee())
print("Signed Withdraw Transaction Hash:", signed_withdraw_transaction.hash())
print("Signed Withdraw Transaction Main Raw:", signed_withdraw_transaction.raw())
# print("Signed Withdraw Transaction Json:", json.dumps(signed_withdraw_transaction.json(), indent=4))
print("Signed Withdraw Transaction Signature:", json.dumps(signed_withdraw_transaction.signature(), indent=4))
print("Signed Withdraw Transaction Type:", signed_withdraw_transaction.type())

signed_withdraw_transaction_raw: str = signed_withdraw_transaction.transaction_raw()
print("Signed Withdraw Transaction Raw:", signed_withdraw_transaction_raw)

print("=" * 10, "Withdraw Signature")

# Initialize withdraw signature
withdraw_signature: WithdrawSignature = WithdrawSignature(network=NETWORK)
# Sign unsigned withdraw transaction raw
withdraw_signature.sign(
    transaction_raw=unsigned_withdraw_transaction_raw,
    solver=withdraw_solver
)

print("Withdraw Signature Fee:", withdraw_signature.fee())
print("Withdraw Signature Hash:", withdraw_signature.hash())
print("Withdraw Signature Main Raw:", withdraw_signature.raw())
# print("Withdraw Signature Json:", json.dumps(withdraw_signature.json(), indent=4))
print("Withdraw Signature Transaction Signature:", json.dumps(withdraw_signature.signature(), indent=4))
print("Withdraw Signature Type:", withdraw_signature.type())

signed_withdraw_signature_transaction_raw: str = withdraw_signature.transaction_raw()
print("Withdraw Signature Transaction Raw:", signed_withdraw_signature_transaction_raw)

# Check both signed withdraw transaction raws are equal
assert signed_withdraw_transaction_raw == signed_withdraw_signature_transaction_raw

# Submit withdraw transaction raw
# print("\nSubmitted Withdraw Transaction:", json.dumps(submit_transaction_raw(
#     transaction_raw=signed_withdraw_transaction_raw  # Or signed_withdraw_signature_transaction_raw
# ), indent=4))
