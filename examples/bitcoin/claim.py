#!/usr/bin/env python3

from shuttle.providers.bitcoin.wallet import Wallet
from shuttle.providers.bitcoin.transaction import ClaimTransaction
from shuttle.providers.bitcoin.solver import ClaimSolver
from shuttle.providers.bitcoin.signature import ClaimSignature

import json

# Setting network
# mainnet or testnet
network = "testnet"

print("=" * 10, "Recipient Bitcoin Account")

recipient_passphrase = "meheret".encode()
print("Recipient Passphrase:", recipient_passphrase.decode())

# Initialize recipient bitcoin wallet
recipient_wallet = Wallet(network=network)\
    .from_passphrase(recipient_passphrase)
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
print("Recipient Balance:", recipient_balance, "Satoshi")
# recipient_unspent = recipient_wallet.unspent()
# for index, unspent in enumerate(recipient_unspent):
#     print("Recipient %d Unspent" % index, unspent)

print("=" * 10, "Hash Time Lock Contract (HTLC) Fund Transaction Id")

# Funded hash time lock contract transaction id/hash
fund_transaction_id = "f7a709ffe08856d7539a155b857913e69e1e6ab4079a47d1c4b94eaa38982768"
print("HTLC Fund Transaction Id:", fund_transaction_id)

print("=" * 10, "Unsigned Claim Transaction")

# Initialization claim transaction
unsigned_claim_transaction = ClaimTransaction(version=2, network=network)
# Building claim transaction
unsigned_claim_transaction.build_transaction(
    transaction_id=fund_transaction_id,
    wallet=recipient_wallet,
    amount=700
)

print("Unsigned Claim Transaction Fee:", unsigned_claim_transaction.fee)
print("Unsigned Claim Transaction Hash:", unsigned_claim_transaction.hash())
print("Unsigned Claim Transaction Raw:", unsigned_claim_transaction.raw())
# print("Unsigned Claim Transaction Json:", json.dumps(unsigned_claim_transaction.json(), indent=4))

unsigned_claim_raw = unsigned_claim_transaction.unsigned_raw()
print("Unsigned Claim Transaction Unsigned Raw:", unsigned_claim_raw)

print("=" * 10, "Signed Claim Transaction")

# Claiming HTLC solver
claim_solver = ClaimSolver(
    secret="Hello Meheret!",
    private_key=recipient_private_key
)

signed_claim_transaction = unsigned_claim_transaction.sign(claim_solver)

print("Signed Claim Transaction Fee:", signed_claim_transaction.fee)
print("Signed Claim Transaction Hash:", signed_claim_transaction.hash())
print("Signed Claim Transaction Raw:", signed_claim_transaction.raw())
# print("Signed Claim Transaction Json:", json.dumps(signed_claim_transaction.json(), indent=4))

print("=" * 10, "Claim Signature")

# Singing Hash Time Lock Contract (HTLC)
claim_signature = ClaimSignature(network=network)\
    .sign(unsigned_raw=unsigned_claim_raw, solver=claim_solver)

print("Claim Signature Fee:", claim_signature.fee)
print("Claim Signature Hash:", claim_signature.hash())
print("Claim Signature Raw:", claim_signature.raw())
# print("Claim Signature Json:", json.dumps(claim_signature.json(), indent=4))

signed_claim_raw = claim_signature.signed_raw()
print("Claim Signature Signed Raw:", signed_claim_raw)
