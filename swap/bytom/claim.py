#!/usr/bin/env python3

from shuttle.providers.bytom.wallet import Wallet
from shuttle.providers.bytom.transaction import ClaimTransaction
from shuttle.providers.bytom.solver import ClaimSolver
from shuttle.providers.bytom.signature import ClaimSignature

import json


print("=" * 10, "Recipient Bytom Account")

recipient_mnemonic = "indicate warm sock mistake code spot acid ribbon sing over taxi toast"
print("Recipient Mnemonic:", recipient_mnemonic)
# Initialize bytom recipient wallet
recipient_bytom_wallet = Wallet(network="mainnet").from_mnemonic(recipient_mnemonic)
# Recipient wallet information's
recipient_seed = recipient_bytom_wallet.seed()
print("Recipient Seed:", recipient_seed)
recipient_xprivate_key = recipient_bytom_wallet.xprivate_key()
print("Recipient XPrivate Key:", recipient_xprivate_key)
recipient_xpublic_key = recipient_bytom_wallet.xpublic_key()
print("Recipient XPublic Key:", recipient_xpublic_key)
recipient_expand_xprivate_key = recipient_bytom_wallet.expand_xprivate_key()
print("Recipient Expand XPrivate Key:", recipient_expand_xprivate_key)
recipient_private_key = recipient_bytom_wallet.private_key()
print("Recipient Private Key:", recipient_private_key)
recipient_public_key = recipient_bytom_wallet.public_key()
print("Recipient Public Key:", recipient_public_key)
recipient_program = recipient_bytom_wallet.program()
print("Recipient Program:", recipient_program)
recipient_address = recipient_bytom_wallet.address()
print("Recipient Address:", recipient_address)
recipient_path = recipient_bytom_wallet.path()
print("Recipient Path:", recipient_path)
recipient_guid = recipient_bytom_wallet.guid()
print("Recipient GUID:", recipient_guid)
# recipient_balance = recipient_bytom_wallet.balance()
# print("Recipient Balance:", recipient_balance)

print("=" * 10, "Hash Time Lock Contract (HTLC) Fund Transaction Id")

# Funded hash time lock contract transaction id/hash
fund_transaction_id = "9059cd0d03e4d4fab70a415169a45be47583f7240115c36cf298d6f261c0a1ac"
print("HTLC Fund Transaction Id:", fund_transaction_id)

print("=" * 10, "Unsigned Claim Transaction")

# Initialization claim transaction
unsigned_claim_transaction = ClaimTransaction(network="mainnet")
# Building claim transaction
unsigned_claim_transaction.build_transaction(
    transaction_id=fund_transaction_id,
    wallet=recipient_bytom_wallet,
    amount=100,
    asset="f37dea62efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf"
)

print("Unsigned Claim Transaction Fee:", unsigned_claim_transaction.fee)
print("Unsigned Claim Transaction Hash:", unsigned_claim_transaction.hash())
print("Unsigned Claim Transaction Raw:", unsigned_claim_transaction.raw())
# print("Unsigned Claim Transaction Json:", json.dumps(unsigned_claim_transaction.json(), indent=4))
print("Unsigned Claim Transaction Unsigned:", json.dumps(unsigned_claim_transaction.unsigned(), indent=4))
print("Unsigned Claim Transaction Signatures:", json.dumps(unsigned_claim_transaction.signatures, indent=4))

unsigned_claim_raw = unsigned_claim_transaction.unsigned_raw()
print("Unsigned Claim Transaction Unsigned Raw:", unsigned_claim_raw)

print("=" * 10, "Signed Claim Transaction")

# Claiming HTLC solver
claim_solver = ClaimSolver(
    secret="Hello Meheret!",
    xprivate_key=recipient_xprivate_key
)

# Singing Hash Time Lock Contract (HTLC)
signed_claim_transaction = unsigned_claim_transaction.sign(claim_solver)

print("Signed Claim Transaction Fee:", signed_claim_transaction.fee)
print("Signed Claim Transaction Hash:", signed_claim_transaction.hash())
print("Signed Claim Transaction Raw:", signed_claim_transaction.raw())
# print("Signed Claim Transaction Json:", json.dumps(signed_claim_transaction.json(), indent=4))
print("Signed Claim Transaction Unsigned:", json.dumps(signed_claim_transaction.unsigned(), indent=4))
print("Signed Claim Transaction Signatures:", json.dumps(signed_claim_transaction.signatures, indent=4))

print("=" * 10, "Claim Signature")

# Singing Hash Time Lock Contract (HTLC)
claim_signature = ClaimSignature(network="mainnet")\
    .sign(unsigned_raw=unsigned_claim_raw, solver=claim_solver)

print("Claim Signature Fee:", claim_signature.fee)
print("Claim Signature Hash:", claim_signature.hash())
print("Claim Signature Raw:", claim_signature.raw())
# print("Claim Signature Json:", json.dumps(claim_signature.json(), indent=4))
print("Claim Signature Unsigned:", json.dumps(claim_signature.unsigned(), indent=4))
print("Claim Signature Transaction Signatures:", json.dumps(signed_claim_transaction.signatures, indent=4))

signed_claim_raw = claim_signature.signed_raw()
print("Claim Signature Signed Raw:", signed_claim_raw)
