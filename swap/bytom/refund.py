#!/usr/bin/env python3

from shuttle.providers.bytom.wallet import Wallet
from shuttle.providers.bytom.transaction import RefundTransaction
from shuttle.providers.bytom.solver import RefundSolver
from shuttle.providers.bytom.signature import RefundSignature

import json


print("=" * 10, "Sender Bytom Account")

sender_mnemonic = "indicate warm sock mistake code spot acid ribbon sing over taxi toast"
print("Sender Mnemonic:", sender_mnemonic)
# Initialize bytom sender wallet
sender_bytom_wallet = Wallet(network="mainnet").from_mnemonic(sender_mnemonic)
# Sender wallet information's
sender_seed = sender_bytom_wallet.seed()
print("Sender Seed:", sender_seed)
sender_xprivate_key = sender_bytom_wallet.xprivate_key()
print("Sender XPrivate Key:", sender_xprivate_key)
sender_xpublic_key = sender_bytom_wallet.xpublic_key()
print("Sender XPublic Key:", sender_xpublic_key)
sender_expand_xprivate_key = sender_bytom_wallet.expand_xprivate_key()
print("Sender Expand XPrivate Key:", sender_expand_xprivate_key)
sender_private_key = sender_bytom_wallet.private_key()
print("Sender Private Key:", sender_private_key)
sender_public_key = sender_bytom_wallet.public_key()
print("Sender Public Key:", sender_public_key)
sender_program = sender_bytom_wallet.program()
print("Sender Program:", sender_program)
sender_address = sender_bytom_wallet.address()
print("Sender Address:", sender_address)
sender_path = sender_bytom_wallet.path()
print("Sender Path:", sender_path)
sender_guid = sender_bytom_wallet.guid()
print("Sender GUID:", sender_guid)
# sender_balance = sender_bytom_wallet.balance()
# print("Sender Balance:", sender_balance)

print("=" * 10, "Hash Time Lock Contract (HTLC) Fund Transaction Id")

# Funded hash time lock contract transaction id/hash
fund_transaction_id = "9059cd0d03e4d4fab70a415169a45be47583f7240115c36cf298d6f261c0a1ac"
print("HTLC Fund Transaction Id:", fund_transaction_id)

print("=" * 10, "Unsigned Refund Transaction")

# Initialization refund transaction
unsigned_refund_transaction = RefundTransaction(network="mainnet")
# Building refund transaction
unsigned_refund_transaction.build_transaction(
    transaction_id=fund_transaction_id,
    wallet=sender_bytom_wallet,
    amount=100,
    asset="f37dea62efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf"
)

print("Unsigned Refund Transaction Fee:", unsigned_refund_transaction.fee)
print("Unsigned Refund Transaction Hash:", unsigned_refund_transaction.hash())
print("Unsigned Refund Transaction Raw:", unsigned_refund_transaction.raw())
print("Unsigned Refund Transaction Json:", json.dumps(unsigned_refund_transaction.json(), indent=4))
print("Unsigned Refund Transaction Unsigned:", json.dumps(unsigned_refund_transaction.unsigned(), indent=4))
print("Unsigned Refund Transaction Signatures:", json.dumps(unsigned_refund_transaction.signatures, indent=4))

unsigned_refund_raw = unsigned_refund_transaction.unsigned_raw()
print("Unsigned Refund Transaction Unsigned Raw:", unsigned_refund_raw)

print("=" * 10, "Signed Refund Transaction")

# Initialize solver
refund_solver = RefundSolver(xprivate_key=sender_xprivate_key)

# Singing Hash Time Lock Contract (HTLC)
signed_refund_transaction = unsigned_refund_transaction.sign(refund_solver)

print("Signed Refund Transaction Fee:", signed_refund_transaction.fee)
print("Signed Refund Transaction Hash:", signed_refund_transaction.hash())
print("Signed Refund Transaction Raw:", signed_refund_transaction.raw())
print("Signed Refund Transaction Json:", json.dumps(signed_refund_transaction.json(), indent=4))
print("Signed Refund Transaction Unsigned:", json.dumps(signed_refund_transaction.unsigned(), indent=4))
print("Signed Refund Transaction Signatures:", json.dumps(signed_refund_transaction.signatures, indent=4))

print("=" * 10, "Refund Signature")

# Singing Hash Time Lock Contract (HTLC)
refund_signature = RefundSignature(network="mainnet")\
    .sign(unsigned_raw=unsigned_refund_raw, solver=refund_solver)

print("Refund Signature Fee:", refund_signature.fee)
print("Refund Signature Hash:", refund_signature.hash())
print("Refund Signature Raw:", refund_signature.raw())
print("Refund Signature Json:", json.dumps(refund_signature.json(), indent=4))
print("Refund Signature Unsigned:", json.dumps(refund_signature.unsigned(), indent=4))
print("Refund Signature Transaction Signatures:", json.dumps(signed_refund_transaction.signatures, indent=4))

signed_refund_raw = refund_signature.signed_raw()
print("Refund Signature Signed Raw:", signed_refund_raw)
