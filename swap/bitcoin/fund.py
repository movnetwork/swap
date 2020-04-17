#!/usr/bin/env python3

from shuttle.providers.bitcoin.wallet import Wallet
from shuttle.providers.bitcoin.htlc import HTLC
from shuttle.providers.bitcoin.transaction import FundTransaction
from shuttle.providers.bitcoin.solver import FundSolver
from shuttle.providers.bitcoin.signature import FundSignature
from shuttle.utils import sha256

import json

# Setting network
# mainnet or testnet
network = "testnet"

print("=" * 10, "Sender Bitcoin Account")

sender_passphrase = "meheret tesfaye batu bayou".encode()
print("Sender Passphrase:", sender_passphrase.decode())

# Initialize sender bitcoin wallet
sender_wallet = Wallet(network=network)
sender_wallet.from_passphrase(sender_passphrase)
# Getting wallet information's
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
sender_balance = sender_wallet.balance()
print("Sender Balance:", sender_balance)
# sender_unspent = sender_wallet.unspent()
# for index, unspent in enumerate(sender_unspent):
#     print("Sender %d Unspent" % index, unspent)

print("=" * 10, "Recipient Bitcoin Account")

# Initialize recipient bitcoin wallet
recipient_wallet = Wallet(network=network)
recipient_wallet.from_address("muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB")
# Getting wallet information's
recipient_address = recipient_wallet.address()
print("Recipient Address:", recipient_address)
recipient_hash = recipient_wallet.hash()
print("Recipient Hash:", recipient_hash)
recipient_p2pkh = recipient_wallet.p2pkh()
print("Recipient P2PKH:", recipient_p2pkh)
recipient_p2sh = recipient_wallet.p2sh()
print("Recipient P2SH:", recipient_p2sh)
recipient_balance = recipient_wallet.balance()
print("Recipient Balance:", recipient_balance)
# recipient_unspent = recipient_wallet.unspent()
# for index, unspent in enumerate(recipient_unspent):
#     print("Recipient %d Unspent" % index, unspent)

print("=" * 10, "Hash Time Lock Contract (HTLC) between Sender and Recipient")

# Initialize Hash Time Lock Contract (HTLC)
htlc = HTLC(network=network).init(
    secret_hash=sha256("Hello Meheret!".encode()).hex(),
    recipient_address=recipient_address,
    sequence=100,
    sender_address=sender_address
)

htlc_bytecode = htlc.bytecode()
print("HTLC Bytecode:", htlc_bytecode)
htlc_opcode = htlc.opcode()
print("HTLC OP_Code:", htlc_opcode)
htlc_address = htlc.address()
print("HTLC Address:", htlc_address)
htlc_hash = htlc.hash()
print("HTLC Hash:", htlc_hash)

print("=" * 10, "Unsigned Fund Transaction")

# Initialization fund transaction
unsigned_fund_transaction = FundTransaction(version=2, network=network)
# Building fund transaction
unsigned_fund_transaction.build_transaction(
    wallet=sender_wallet,
    htlc=htlc,
    amount=10000
)

print("Unsigned Fund Transaction Fee:", unsigned_fund_transaction.fee)
print("Unsigned Fund Transaction Hash:", unsigned_fund_transaction.hash())
print("Unsigned Fund Transaction Raw:", unsigned_fund_transaction.raw())
# print("Unsigned Fund Transaction Json:", json.dumps(unsigned_fund_transaction.json(), indent=4))

unsigned_fund_raw = unsigned_fund_transaction.unsigned_raw()
print("Unsigned Fund Transaction Unsigned Raw:", unsigned_fund_raw)

print("=" * 10, "Signed Fund Transaction")

# Initialize solver
fund_solver = FundSolver(private_key=sender_private_key)

# Singing Hash Time Lock Contract (HTLC)
signed_fund_transaction = unsigned_fund_transaction.sign(fund_solver)

print("Signed Fund Transaction Fee:", signed_fund_transaction.fee)
print("Signed Fund Transaction Hash:", signed_fund_transaction.hash())
print("Signed Fund Transaction Raw:", signed_fund_transaction.raw())
# print("Signed Fund Transaction Json:", json.dumps(signed_fund_transaction.json(), indent=4))

print("=" * 10, "Fund Signature")

# Singing Hash Time Lock Contract (HTLC)
fund_signature = FundSignature(network=network)\
    .sign(unsigned_raw=unsigned_fund_raw, solver=fund_solver)

print("Fund Signature Fee:", fund_signature.fee)
print("Fund Signature Hash:", fund_signature.hash())
print("Fund Signature Raw:", fund_signature.raw())
# print("Fund Signature Json:", json.dumps(fund_signature.json(), indent=4))

signed_fund_raw = fund_signature.signed_raw()
print("Fund Signature Signed Raw:", signed_fund_raw)
