#!/usr/bin/env python3

from shuttle.providers.bitcoin.wallet import Wallet
from shuttle.providers.bitcoin.transaction import ClaimTransaction
from shuttle.providers.bitcoin.solver import ClaimSolver
from shuttle.providers.bitcoin.signature import ClaimSignature
from shuttle.utils import sha256

import json

# Bitcoin network
NETWORK = "testnet"
# Bitcoin transaction id/hash
TRANSACTION_ID = "31507decc14a0f334f5de2329f828f4e22017f7333add9579bb2e889203b7135"
# Recipient passphrase/password
RECIPIENT_PASSPHRASE = "Woo!"
# Sender Bitcoin address
SENDER_ADDRESS = "miAcLpYbaqE8KowBu2PwvqXG6y6vpQcfTJ"
# Bitcoin claim amount
AMOUNT = 10_000

print("=" * 10, "Recipient Bitcoin Account")

# Initializing recipient Bitcoin wallet
recipient_wallet = Wallet(network=NETWORK)
# Initializing Bitcoin wallet from passphrase
recipient_wallet.from_passphrase(passphrase=RECIPIENT_PASSPHRASE)
# Getting recipient wallet information's
recipient_private_key = recipient_wallet.private_key()
print("Recipient Private Key:", recipient_private_key)
recipient_public_key = recipient_wallet.public_key()
print("Recipient Public Key:", recipient_public_key)
recipient_compressed = recipient_wallet.compressed()
print("Recipient Compressed:", recipient_compressed)
recipient_uncompressed = recipient_wallet.uncompressed()
print("Recipient Uncompressed:", recipient_uncompressed)
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

print("=" * 10, "Sender Bitcoin Account")

# Initializing sender Bitcoin wallet
sender_wallet = Wallet(network=NETWORK)
# Initializing Bitcoin wallet from address
sender_wallet.from_address(address=SENDER_ADDRESS)
# Getting sender wallet information's
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

print("=" * 10, "Unsigned Claim Transaction")

# Initializing claim transaction
unsigned_claim_transaction = ClaimTransaction(version=2, network=NETWORK)
# Building claim transaction
unsigned_claim_transaction.build_transaction(
    transaction_id=TRANSACTION_ID,
    wallet=recipient_wallet,
    amount=AMOUNT
)

print("Unsigned Claim Transaction Fee:", unsigned_claim_transaction.fee())
print("Unsigned Claim Transaction Hash:", unsigned_claim_transaction.hash())
print("Unsigned Claim Transaction Raw:", unsigned_claim_transaction.raw())
# print("Unsigned Claim Transaction Json:", json.dumps(unsigned_claim_transaction.json(), indent=4))
print("Unsigned Claim Transaction Type:", unsigned_claim_transaction.type())

unsigned_claim_raw = unsigned_claim_transaction.unsigned_raw()
print("Unsigned Claim Transaction Unsigned Raw:", unsigned_claim_raw)

print("=" * 10, "Signed Claim Transaction")

# Initializing claim solver
claim_solver = ClaimSolver(
    private_key=recipient_private_key,
    secret="Hello Meheret!",
    secret_hash=sha256("Hello Meheret!".encode()).hex(),
    recipient_address=recipient_address,
    sender_address=sender_address,
    sequence=1000
)

# Singing unsigned claim transaction
signed_claim_transaction = unsigned_claim_transaction.sign(solver=claim_solver)

print("Signed Claim Transaction Fee:", signed_claim_transaction.fee())
print("Signed Claim Transaction Hash:", signed_claim_transaction.hash())
print("Signed Claim Transaction Raw:", signed_claim_transaction.raw())
# print("Signed Claim Transaction Json:", json.dumps(signed_claim_transaction.json(), indent=4))
print("Signed Claim Transaction Type:", signed_claim_transaction.type())

print("=" * 10, "Claim Signature")

# Initializing claim signature
claim_signature = ClaimSignature(network=NETWORK)
# Singing unsigned claim transaction raw
claim_signature.sign(
    unsigned_raw=unsigned_claim_raw,
    solver=claim_solver
)

print("Claim Signature Fee:", claim_signature.fee())
print("Claim Signature Hash:", claim_signature.hash())
print("Claim Signature Raw:", claim_signature.raw())
# print("Claim Signature Json:", json.dumps(claim_signature.json(), indent=4))
print("Claim Signature Type:", claim_signature.type())

signed_claim_raw = claim_signature.signed_raw()
print("Claim Signature Signed Raw:", signed_claim_raw)
