#!/usr/bin/env python3

from swap.providers.bitcoin.wallet import Wallet
from swap.providers.bitcoin.htlc import HTLC
from swap.providers.bitcoin.transaction import FundTransaction
from swap.providers.bitcoin.solver import FundSolver
from swap.providers.bitcoin.signature import FundSignature
from swap.providers.bitcoin.utils import submit_transaction_raw

import json

# Bitcoin network
NETWORK = "testnet"
# Sender passphrase/password
SENDER_PASSPHRASE = "Boom!"
# Hash Time Lock Contract (HTLC) bytecode
HTLC_BYTECODE = "63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876" \
                "a914acf8419eecab574c494febbe03fd07fdae7bf2f488ac6702e803b27576a9141d0f671c" \
                "26a3ef7a865d1eda0fbd085e98adcc2388ac68"
# Bitcoin fund amount
AMOUNT = 10_000

print("=" * 10, "Sender Bitcoin Account")

# Initializing sender Bitcoin wallet
sender_wallet = Wallet(network=NETWORK)
# Initializing Bitcoin wallet from passphrase
sender_wallet.from_passphrase(passphrase=SENDER_PASSPHRASE)
# Getting sender wallet information's
sender_private_key = sender_wallet.private_key()
print("Sender Private Key:", sender_private_key)
sender_public_key = sender_wallet.public_key()
print("Sender Public Key:", sender_public_key)
sender_compressed = sender_wallet.compressed()
print("Sender Compressed:", sender_compressed)
sender_uncompressed = sender_wallet.uncompressed()
print("Sender Uncompressed:", sender_uncompressed)
sender_address = sender_wallet.address()
print("Sender Address:", sender_address)
sender_hash = sender_wallet.hash()
print("Sender Hash:", sender_hash)
sender_p2pkh = sender_wallet.p2pkh()
print("Sender P2PKH:", sender_p2pkh)
sender_p2sh = sender_wallet.p2sh()
print("Sender P2SH:", sender_p2sh)
# sender_balance = sender_wallet.balance()
# print("Sender Balance:", sender_balance)

print("=" * 10, "Hash Time Lock Contract (HTLC) from Bytecode")

# Initializing Hash Time Lock Contract (HTLC)
htlc = HTLC(network=NETWORK)
# Initializing HTLC from bytecode
htlc.from_bytecode(bytecode=HTLC_BYTECODE)

htlc_bytecode = htlc.bytecode()
print("HTLC Bytecode:", htlc_bytecode)
htlc_opcode = htlc.opcode()
print("HTLC OP_Code:", htlc_opcode)
htlc_hash = htlc.hash()
print("HTLC Hash:", htlc_hash)
htlc_address = htlc.address()
print("HTLC Address:", htlc_address)

print("=" * 10, "Unsigned Fund Transaction")

# Initialization fund transaction
unsigned_fund_transaction = FundTransaction(version=2, network=NETWORK)
# Building fund transaction
unsigned_fund_transaction.build_transaction(
    wallet=sender_wallet,
    htlc=htlc,
    amount=AMOUNT
)

print("Unsigned Fund Transaction Fee:", unsigned_fund_transaction.fee())
print("Unsigned Fund Transaction Hash:", unsigned_fund_transaction.hash())
print("Unsigned Fund Transaction Raw:", unsigned_fund_transaction.raw())
# print("Unsigned Fund Transaction Json:", json.dumps(unsigned_fund_transaction.json(), indent=4))
print("Unsigned Fund Transaction Type:", unsigned_fund_transaction.type())

unsigned_fund_raw = unsigned_fund_transaction.unsigned_raw()
print("Unsigned Fund Transaction Unsigned Raw:", unsigned_fund_raw)

print("=" * 10, "Signed Fund Transaction")

# Initializing fund solver
fund_solver = FundSolver(
    private_key=sender_private_key
)

# Singing unsigned fund transaction
signed_fund_transaction = unsigned_fund_transaction.sign(solver=fund_solver)

print("Signed Fund Transaction Fee:", signed_fund_transaction.fee())
print("Signed Fund Transaction Hash:", signed_fund_transaction.hash())
print("Signed Fund Transaction Raw:", signed_fund_transaction.raw())
# print("Signed Fund Transaction Json:", json.dumps(signed_fund_transaction.json(), indent=4))
print("Signed Fund Transaction Type:", signed_fund_transaction.type())

print("=" * 10, "Fund Signature")

# Initializing fund signature
fund_signature = FundSignature(network=NETWORK)
# Singing unsigned fund transaction raw
fund_signature.sign(
    unsigned_raw=unsigned_fund_raw,
    solver=fund_solver
)

print("Fund Signature Fee:", fund_signature.fee())
print("Fund Signature Hash:", fund_signature.hash())
print("Fund Signature Raw:", fund_signature.raw())
# print("Fund Signature Json:", json.dumps(fund_signature.json(), indent=4))
print("Fund Signature Type:", fund_signature.type())

signed_fund_raw = fund_signature.signed_raw()
print("Fund Signature Signed Raw:", signed_fund_raw)

# Submitting fund transaction raw
# print("\nSubmitted Fund Transaction:", submit_transaction_raw(
#     transaction_raw=signed_fund_raw
# ))
