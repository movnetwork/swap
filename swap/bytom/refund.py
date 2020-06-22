#!/usr/bin/env python3

from shuttle.providers.bytom.wallet import Wallet
from shuttle.providers.bytom.transaction import RefundTransaction
from shuttle.providers.bytom.solver import RefundSolver
from shuttle.providers.bytom.signature import RefundSignature
from shuttle.utils import sha256

import json

# Bytom network
NETWORK = "mainnet"
# Bytom transaction id/hash
TRANSACTION_ID = "5ec2547c7aece45af6b4b97fabcc42cb6b1ecfa9c7d30a0b3c4655888284b1bd"
# Sender 12 word mnemonic
SENDER_MNEMONIC = "indicate warm sock mistake code spot acid ribbon sing over taxi toast"
# Recipient Bytom public key
RECIPIENT_PUBLIC_KEY = "3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e"
# Bytom fund asset id
ASSET = "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
# Bytom fund amount
AMOUNT = 10_000

print("=" * 10, "Sender Bytom Account")

# Initializing Bytom sender wallet
sender_wallet = Wallet(network=NETWORK)
# Initializing Bytom wallet from mnemonic
sender_wallet.from_mnemonic(mnemonic=SENDER_MNEMONIC)
# Getting sender wallet information's
sender_seed = sender_wallet.seed()
print("Sender Seed:", sender_seed)
sender_xprivate_key = sender_wallet.xprivate_key()
print("Sender XPrivate Key:", sender_xprivate_key)
sender_xpublic_key = sender_wallet.xpublic_key()
print("Sender XPublic Key:", sender_xpublic_key)
sender_expand_xprivate_key = sender_wallet.expand_xprivate_key()
print("Sender Expand XPrivate Key:", sender_expand_xprivate_key)
sender_private_key = sender_wallet.private_key()
print("Sender Private Key:", sender_private_key)
sender_public_key = sender_wallet.public_key()
print("Sender Public Key:", sender_public_key)
sender_program = sender_wallet.program()
print("Sender Program:", sender_program)
sender_address = sender_wallet.address()
print("Sender Address:", sender_address)
sender_path = sender_wallet.path()
print("Sender Path:", sender_path)
sender_guid = sender_wallet.guid()
print("Sender GUID:", sender_guid)
# sender_balance = sender_wallet.balance()
# print("Sender Balance:", sender_balance)

print("=" * 10, "Recipient Bytom Account")

# Initializing Bytom recipient wallet
recipient_wallet = Wallet(network=NETWORK)
# Initializing Bytom wallet from public key
recipient_wallet.from_public_key(public=RECIPIENT_PUBLIC_KEY)
# Getting recipient wallet information's
recipient_public_key = recipient_wallet.public_key()
print("Recipient Public Key:", recipient_public_key)
recipient_program = recipient_wallet.program()
print("Recipient Program:", recipient_program)
recipient_address = recipient_wallet.address()
print("Recipient Address:", recipient_address)
# recipient_balance = recipient_wallet.balance()
# print("Recipient Balance:", recipient_balance)

print("=" * 10, "Unsigned Refund Transaction")

# Initializing refund transaction
unsigned_refund_transaction = RefundTransaction(network="mainnet")
# Building refund transaction
unsigned_refund_transaction.build_transaction(
    transaction_id=TRANSACTION_ID,
    wallet=sender_wallet,
    amount=AMOUNT,
    asset=ASSET
)

print("Unsigned Refund Transaction Fee:", unsigned_refund_transaction.fee())
print("Unsigned Refund Transaction Hash:", unsigned_refund_transaction.hash())
print("Unsigned Refund Transaction Raw:", unsigned_refund_transaction.raw())
# print("Unsigned Refund Transaction Json:", json.dumps(unsigned_refund_transaction.json(), indent=4))
print("Unsigned Refund Transaction Unsigned:", json.dumps(unsigned_refund_transaction.unsigned_datas(), indent=4))
print("Unsigned Refund Transaction Signatures:", json.dumps(unsigned_refund_transaction.signatures(), indent=4))

unsigned_refund_raw = unsigned_refund_transaction.unsigned_raw()
print("Unsigned Refund Transaction Unsigned Raw:", unsigned_refund_raw)

print("=" * 10, "Signed Refund Transaction")

# Initializing refund solver
refund_solver = RefundSolver(
    xprivate_key=sender_xprivate_key,
    secret_hash=sha256("Hello Meheret!".encode()).hex(),
    recipient_public=recipient_public_key,
    sender_public=sender_public_key,
    sequence=1000
)

# Singing unsigned refund transaction
signed_refund_transaction = unsigned_refund_transaction.sign(refund_solver)

print("Signed Refund Transaction Fee:", signed_refund_transaction.fee())
print("Signed Refund Transaction Hash:", signed_refund_transaction.hash())
print("Signed Refund Transaction Raw:", signed_refund_transaction.raw())
# print("Signed Refund Transaction Json:", json.dumps(signed_refund_transaction.json(), indent=4))
print("Signed Refund Transaction Unsigned:", json.dumps(signed_refund_transaction.unsigned_datas(), indent=4))
print("Signed Refund Transaction Signatures:", json.dumps(signed_refund_transaction.signatures(), indent=4))

print("=" * 10, "Refund Signature")

# Initializing refund signature
refund_signature = RefundSignature(network="mainnet")
# Singing unsigned refund transaction raw
refund_signature.sign(
    unsigned_raw=unsigned_refund_raw,
    solver=refund_solver
)

print("Refund Signature Fee:", refund_signature.fee())
print("Refund Signature Hash:", refund_signature.hash())
print("Refund Signature Raw:", refund_signature.raw())
# print("Refund Signature Json:", json.dumps(refund_signature.json(), indent=4))
print("Refund Signature Unsigned:", json.dumps(refund_signature.unsigned_datas(), indent=4))
print("Refund Signature Transaction Signatures:", json.dumps(refund_signature.signatures(), indent=4))

signed_refund_raw = refund_signature.signed_raw()
print("Refund Signature Signed Raw:", signed_refund_raw)
