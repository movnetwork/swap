#!/usr/bin/env python3

from swap.providers.bitcoin.wallet import Wallet, DEFAULT_PATH
from swap.providers.bitcoin.transaction import FundTransaction
from swap.providers.bitcoin.solver import FundSolver
from swap.providers.bitcoin.signature import FundSignature
from swap.providers.bitcoin.utils import (
    submit_transaction_raw, amount_converter
)

import json

# Choose network mainnet or testnet
NETWORK: str = "testnet"
# Bitcoin sender wallet mnemonic
SENDER_MNEMONIC: str = "indicate warm sock mistake code spot acid ribbon sing over taxi toast"
# Bitcoin Hash Time Lock Contract (HTLC) address
HTLC_ADDRESS: str = "2N6kHwQy6Ph5EdKNgzGrcW2WhGHKGfmP5ae"
# Bitcoin fund amount
AMOUNT: int = amount_converter(amount=0.1, symbol="BTC2SATOSHI")

print("=" * 10, "Sender Bitcoin Account")

# Initialize Bitcoin sender wallet
sender_wallet: Wallet = Wallet(network=NETWORK)
# Get Bitcoin sender wallet from mnemonic
sender_wallet.from_mnemonic(mnemonic=SENDER_MNEMONIC)
# Drive Bitcoin sender wallet from path
sender_wallet.from_path(path=DEFAULT_PATH)

# Print some Bitcoin sender wallet info's
print("Root XPrivate Key:", sender_wallet.root_xprivate_key())
print("Root XPublic Key:", sender_wallet.root_xprivate_key())
print("Private Key:", sender_wallet.private_key())
print("Public Key:", sender_wallet.public_key())
print("Address:", sender_wallet.address())
print("Balance:", sender_wallet.balance(symbol="BTC"), "BTC")

print("=" * 10, "Unsigned Fund Transaction")

# Initialize fund transaction
unsigned_fund_transaction: FundTransaction = FundTransaction(network=NETWORK, version=2)
# Build fund transaction
unsigned_fund_transaction.build_transaction(
    address=sender_wallet.address(),
    htlc_address=HTLC_ADDRESS,
    amount=AMOUNT
)

print("Unsigned Fund Transaction Fee:", unsigned_fund_transaction.fee(symbol="SATOSHI"), "SATOSHI")
print("Unsigned Fund Transaction Hash:", unsigned_fund_transaction.hash())
print("Unsigned Fund Transaction Main Raw:", unsigned_fund_transaction.raw())
# print("Unsigned Fund Transaction Json:", json.dumps(unsigned_fund_transaction.json(), indent=4))
print("Unsigned Fund Transaction Type:", unsigned_fund_transaction.type())

unsigned_fund_transaction_raw: str = unsigned_fund_transaction.transaction_raw()
print("Unsigned Fund Transaction Raw:", unsigned_fund_transaction_raw)

print("=" * 10, "Signed Fund Transaction")

# Initialize fund solver
fund_solver: FundSolver = FundSolver(
    root_xprivate_key=sender_wallet.root_xprivate_key()
)

# Sing unsigned fund transaction
signed_fund_transaction: FundTransaction = unsigned_fund_transaction.sign(solver=fund_solver)

print("Signed Fund Transaction Fee:", signed_fund_transaction.fee(symbol="SATOSHI"), "SATOSHI")
print("Signed Fund Transaction Hash:", signed_fund_transaction.hash())
print("Signed Fund Transaction Main Raw:", signed_fund_transaction.raw())
# print("Signed Fund Transaction Json:", json.dumps(signed_fund_transaction.json(), indent=4))
print("Signed Fund Transaction Type:", signed_fund_transaction.type())

signed_fund_transaction_raw = signed_fund_transaction.transaction_raw()
print("Signed Fund Transaction Raw:", signed_fund_transaction_raw)

print("=" * 10, "Fund Signature")

# Initialize fund signature
fund_signature: FundSignature = FundSignature(network=NETWORK)
# Sing unsigned fund transaction raw
fund_signature.sign(
    transaction_raw=unsigned_fund_transaction_raw,
    solver=fund_solver
)

print("Fund Signature Fee:", fund_signature.fee(symbol="SATOSHI"), "SATOSHI")
print("Fund Signature Hash:", fund_signature.hash())
print("Fund Signature Main Raw:", fund_signature.raw())
# print("Fund Signature Json:", json.dumps(fund_signature.json(), indent=4))
print("Fund Signature Type:", fund_signature.type())

signed_fund_signature_transaction_raw: str = fund_signature.transaction_raw()
print("Fund Signature Transaction Raw:", signed_fund_signature_transaction_raw)

# Check both signed fund transaction raws are equal
assert signed_fund_transaction_raw == signed_fund_signature_transaction_raw

# Submit fund transaction raw
# print("\nSubmitted Fund Transaction:", json.dumps(submit_transaction_raw(
#     transaction_raw=signed_fund_transaction_raw  # Or signed_fund_signature_transaction_raw
# ), indent=4))
