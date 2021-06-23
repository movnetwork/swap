#!/usr/bin/env python3

from swap.providers.xinfin.wallet import Wallet, DEFAULT_BIP44_PATH
from swap.providers.xinfin.transaction import WithdrawTransaction
from swap.providers.xinfin.signature import WithdrawSignature
from swap.providers.xinfin.solver import WithdrawSolver
from swap.providers.xinfin.utils import submit_transaction_raw

import json

# Choose network mainnet or testnet
NETWORK: str = "testnet"
# XinFin HTLC transaction hash
HTLC_TRANSACTION_HASH: str = "0x728c83cc83bb4b1a67fbfd480a9bdfdd55cb5fc6fd519f6a98fa35db3a2a9160"
# XinFin recipient wallet mnemonic
RECIPIENT_MNEMONIC: str = "unfair divorce remind addict add roof park clown build renew illness fault"
# Derivation for recipient wallet mnemonic
ACCOUNT, CHANGE, ADDRESS = 0, False, 1
# Funded transaction hash/id
TRANSACTION_HASH: str = "0xe87b1aefec9fecbb7699e16d101e757e4825db157eb94d2e71ecfaf17fd3d75d"
# Secret key to unlock the contract
SECRET_KEY: str = "Hello Meheret!"

print("=" * 10, "Recipient XinFin Account")

# Initialize XinFin recipient wallet
wallet: Wallet = Wallet(network=NETWORK)
# Get XinFin recipient wallet from mnemonic
wallet.from_mnemonic(mnemonic=RECIPIENT_MNEMONIC)
# Drive XinFin recipient wallet from path
wallet.from_path(
    path=DEFAULT_BIP44_PATH.format(
        account=ACCOUNT, change=(1 if CHANGE else 0), address=ADDRESS
    )
)

# Print some XinFin recipient wallet info's
print("Root XPrivate Key:", wallet.root_xprivate_key())
print("Root XPublic Key:", wallet.root_xpublic_key())
print("Private Key:", wallet.private_key())
print("Public Key:", wallet.public_key())
print("Path:", wallet.path())
print("Address:", wallet.address())
print("Balance:", wallet.balance(unit="XDC"), "XDC")

print("=" * 10, "Unsigned Withdraw Transaction")

# Initialize withdraw transaction
unsigned_withdraw_transaction: WithdrawTransaction = WithdrawTransaction(network=NETWORK)
# Build withdraw transaction
unsigned_withdraw_transaction.build_transaction(
    transaction_hash=TRANSACTION_HASH,
    address=wallet.address(),
    secret_key=SECRET_KEY,
    htlc_transaction_hash=HTLC_TRANSACTION_HASH
)

print("Unsigned Withdraw Transaction Fee:", unsigned_withdraw_transaction.fee())
print("Unsigned Withdraw Transaction Hash:", unsigned_withdraw_transaction.hash())
print("Unsigned Withdraw Transaction Raw:", unsigned_withdraw_transaction.raw())
print("Unsigned Withdraw Transaction Json:", unsigned_withdraw_transaction.json())
print("Unsigned Withdraw Transaction Signature:", unsigned_withdraw_transaction.signature())
print("Unsigned Withdraw Transaction Type:", unsigned_withdraw_transaction.type())

unsigned_withdraw_transaction_raw: str = unsigned_withdraw_transaction.transaction_raw()
print("Unsigned Withdraw Transaction Raw:", unsigned_withdraw_transaction_raw)

print("=" * 10, "Signed Withdraw Transaction")

# Initialize withdraw solver
withdraw_solver: WithdrawSolver = WithdrawSolver(
    xprivate_key=wallet.root_xprivate_key(), path=DEFAULT_BIP44_PATH.format(
        account=ACCOUNT, change=(1 if CHANGE else 0), address=ADDRESS
    )
)

# Sing unsigned withdraw transaction
signed_withdraw_transaction: WithdrawTransaction = unsigned_withdraw_transaction.sign(solver=withdraw_solver)

print("Signed Withdraw Transaction Fee:", signed_withdraw_transaction.fee())
print("Signed Withdraw Transaction Hash:", signed_withdraw_transaction.hash())
print("Signed Withdraw Transaction Json:", signed_withdraw_transaction.json())
print("Signed Withdraw Transaction Main Raw:", signed_withdraw_transaction.raw())
print("Signed Withdraw Transaction Signature:", signed_withdraw_transaction.signature())
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
print("Withdraw Signature Json:", withdraw_signature.json())
print("Withdraw Signature Raw:", withdraw_signature.raw())
print("Withdraw Signature Transaction Signature:", withdraw_signature.signature())
print("Withdraw Signature Type:", withdraw_signature.type())

signed_withdraw_signature_transaction_raw: str = withdraw_signature.transaction_raw()
print("Withdraw Signature Transaction Raw:", signed_withdraw_signature_transaction_raw)

# Check both signed withdraw transaction raws are equal
assert signed_withdraw_transaction_raw == signed_withdraw_signature_transaction_raw

# Submit withdraw transaction raw
# print("\nSubmitted Withdraw Transaction:", json.dumps(submit_transaction_raw(
#     transaction_raw=signed_withdraw_transaction_raw  # Or signed_withdraw_signature_transaction_raw
# ), indent=4))
