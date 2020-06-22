#!/usr/bin/env python3

from shuttle.providers.bytom.wallet import Wallet
from shuttle.providers.bytom.transaction import ClaimTransaction
from shuttle.providers.bytom.solver import ClaimSolver
from shuttle.providers.bytom.signature import ClaimSignature
from shuttle.utils import sha256

import json

# Bytom network
NETWORK = "mainnet"
# Bytom transaction id/hash
TRANSACTION_ID = "5ec2547c7aece45af6b4b97fabcc42cb6b1ecfa9c7d30a0b3c4655888284b1bd"
# Recipient 12 word mnemonic
RECIPIENT_MNEMONIC = "hint excuse upgrade sleep easily deputy erase cluster section other ugly limit"
# Sender Bytom public key
SENDER_PUBLIC_KEY = "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2"
# Bytom fund asset id
ASSET = "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
# Bytom fund amount
AMOUNT = 10_000

print("=" * 10, "Recipient Bytom Account")

# Initializing Bytom recipient wallet
recipient_wallet = Wallet(network="mainnet")
# Initializing Bytom wallet from mnemonic
recipient_wallet.from_mnemonic(mnemonic=RECIPIENT_MNEMONIC)
# Getting recipient wallet information's
recipient_seed = recipient_wallet.seed()
print("Recipient Seed:", recipient_seed)
recipient_xprivate_key = recipient_wallet.xprivate_key()
print("Recipient XPrivate Key:", recipient_xprivate_key)
recipient_xpublic_key = recipient_wallet.xpublic_key()
print("Recipient XPublic Key:", recipient_xpublic_key)
recipient_expand_xprivate_key = recipient_wallet.expand_xprivate_key()
print("Recipient Expand XPrivate Key:", recipient_expand_xprivate_key)
recipient_private_key = recipient_wallet.private_key()
print("Recipient Private Key:", recipient_private_key)
recipient_public_key = recipient_wallet.public_key()
print("Recipient Public Key:", recipient_public_key)
recipient_program = recipient_wallet.program()
print("Recipient Program:", recipient_program)
recipient_address = recipient_wallet.address()
print("Recipient Address:", recipient_address)
recipient_path = recipient_wallet.path()
print("Recipient Path:", recipient_path)
recipient_guid = recipient_wallet.guid()
print("Recipient GUID:", recipient_guid)
# recipient_balance = recipient_wallet.balance()
# print("Recipient Balance:", recipient_balance)

print("=" * 10, "Sender Bytom Account")

# Initializing Bytom sender wallet
sender_wallet = Wallet(network=NETWORK)
# Initializing Bytom wallet from public key
sender_wallet.from_public_key(public=SENDER_PUBLIC_KEY)
# Getting sender wallet information's
sender_public_key = sender_wallet.public_key()
print("Sender Public Key:", sender_public_key)
sender_program = sender_wallet.program()
print("Sender Program:", sender_program)
sender_address = sender_wallet.address()
print("Sender Address:", sender_address)
# sender_balance = sender_wallet.balance()
# print("Sender Balance:", sender_balance)

print("=" * 10, "Unsigned Claim Transaction")

# Initializing claim transaction
unsigned_claim_transaction = ClaimTransaction(network="mainnet")
# Building claim transaction
unsigned_claim_transaction.build_transaction(
    transaction_id=TRANSACTION_ID,
    wallet=recipient_wallet,
    amount=AMOUNT,
    asset=ASSET
)

print("Unsigned Claim Transaction Fee:", unsigned_claim_transaction.fee())
print("Unsigned Claim Transaction Hash:", unsigned_claim_transaction.hash())
print("Unsigned Claim Transaction Raw:", unsigned_claim_transaction.raw())
# print("Unsigned Claim Transaction Json:", json.dumps(unsigned_claim_transaction.json(), indent=4))
print("Unsigned Claim Transaction Unsigned:", json.dumps(unsigned_claim_transaction.unsigned_datas(), indent=4))
print("Unsigned Claim Transaction Signatures:", json.dumps(unsigned_claim_transaction.signatures(), indent=4))

unsigned_claim_raw = unsigned_claim_transaction.unsigned_raw()
print("Unsigned Claim Transaction Unsigned Raw:", unsigned_claim_raw)

print("=" * 10, "Signed Claim Transaction")

# Initializing claim solver
claim_solver = ClaimSolver(
    xprivate_key=recipient_xprivate_key,
    secret="Hello Meheret!",
    secret_hash=sha256("Hello Meheret!".encode()).hex(),
    recipient_public=recipient_public_key,
    sender_public=sender_public_key,
    sequence=1000
)

# Singing unsigned claim transaction
signed_claim_transaction = unsigned_claim_transaction.sign(claim_solver)

print("Signed Claim Transaction Fee:", signed_claim_transaction.fee())
print("Signed Claim Transaction Hash:", signed_claim_transaction.hash())
print("Signed Claim Transaction Raw:", signed_claim_transaction.raw())
# print("Signed Claim Transaction Json:", json.dumps(signed_claim_transaction.json(), indent=4))
print("Signed Claim Transaction Unsigned:", json.dumps(signed_claim_transaction.unsigned_datas(), indent=4))
print("Signed Claim Transaction Signatures:", json.dumps(signed_claim_transaction.signatures(), indent=4))

print("=" * 10, "Claim Signature")

# Initializing claim signature
claim_signature = ClaimSignature(network="mainnet")
# Singing unsigned claim transaction raw
claim_signature.sign(
    unsigned_raw=unsigned_claim_raw,
    solver=claim_solver
)

print("Claim Signature Fee:", claim_signature.fee())
print("Claim Signature Hash:", claim_signature.hash())
print("Claim Signature Raw:", claim_signature.raw())
# print("Claim Signature Json:", json.dumps(claim_signature.json(), indent=4))
print("Claim Signature Unsigned:", json.dumps(claim_signature.unsigned_datas(), indent=4))
print("Claim Signature Transaction Signatures:", json.dumps(claim_signature.signatures(), indent=4))

signed_claim_raw = claim_signature.signed_raw()
print("Claim Signature Signed Raw:", signed_claim_raw)
