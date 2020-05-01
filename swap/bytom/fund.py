#!/usr/bin/env python3

from shuttle.providers.bytom.wallet import Wallet
from shuttle.providers.bytom.htlc import HTLC
from shuttle.providers.bytom.transaction import FundTransaction
from shuttle.providers.bytom.solver import FundSolver
from shuttle.providers.bytom.signature import FundSignature
from shuttle.utils import sha256

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

print("=" * 10, "Recipient Bytom Account")

recipient_public = "ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01"
# Initialize bytom sender wallet
recipient_bytom_wallet = Wallet(network="mainnet").from_public_key(recipient_public)
# Recipient wallet information's
recipient_public_key = recipient_bytom_wallet.public_key()
print("Recipient Public Key:", recipient_public_key)
recipient_program = recipient_bytom_wallet.program()
print("Recipient Program:", recipient_program)
recipient_address = recipient_bytom_wallet.address()
print("Recipient Address:", recipient_address)
# recipient_balance = recipient_bytom_wallet.balance()
# print("Recipient Balance:", recipient_balance)

print("=" * 10, "Hash Time Lock Contract (HTLC) between Sender and Recipient")

# Initialization Hash Time Lock Contract (HTLC).
bytom_htlc = HTLC(network="mainnet").init(
    secret_hash=sha256("Hello Meheret!".encode()).hex(),
    recipient_public=recipient_public_key,
    sender_public=sender_public_key,
    sequence=100
)

htlc_bytecode = bytom_htlc.bytecode()
print("HTLC Bytecode:", htlc_bytecode)
htlc_opcode = bytom_htlc.opcode()
print("HTLC OP_Code:", htlc_opcode)

print("=" * 10, "Unsigned Fund Transaction")

# Initialization fund transaction
unsigned_fund_transaction = FundTransaction(network="mainnet")
# Building fund transaction
unsigned_fund_transaction.build_transaction(
    wallet=sender_bytom_wallet,
    htlc=bytom_htlc,
    amount=100,
    asset="f37dea62efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf"
)

print("Unsigned Fund Transaction Fee:", unsigned_fund_transaction.fee)
print("Unsigned Fund Transaction Hash:", unsigned_fund_transaction.hash())
print("Unsigned Fund Transaction Raw:", unsigned_fund_transaction.raw())
print("Unsigned Fund Transaction Json:", json.dumps(unsigned_fund_transaction.json(), indent=4))
print("Unsigned Fund Transaction Unsigned:", json.dumps(unsigned_fund_transaction.unsigned(), indent=4))
print("Unsigned Fund Transaction Signatures:", json.dumps(unsigned_fund_transaction.signatures, indent=4))

unsigned_fund_raw = unsigned_fund_transaction.unsigned_raw()
print("Unsigned Fund Transaction Unsigned Raw:", unsigned_fund_raw)

print("=" * 10, "Signed Fund Transaction")

# Initialize solver
fund_solver = FundSolver(xprivate_key=sender_xprivate_key)

# Singing Hash Time Lock Contract (HTLC)
signed_fund_transaction = unsigned_fund_transaction.sign(fund_solver)

print("Signed Fund Transaction Fee:", signed_fund_transaction.fee)
print("Signed Fund Transaction Hash:", signed_fund_transaction.hash())
print("Signed Fund Transaction Raw:", signed_fund_transaction.raw())
print("Signed Fund Transaction Json:", json.dumps(signed_fund_transaction.json(), indent=4))
print("Signed Fund Transaction Unsigned:", json.dumps(signed_fund_transaction.unsigned(), indent=4))
print("Signed Fund Transaction Signatures:", json.dumps(signed_fund_transaction.signatures, indent=4))

print("=" * 10, "Fund Signature")

# Initialize Fund signature.
fund_signature = FundSignature(network="mainnet")
# Singing Hash Time Lock Contract (HTLC).
fund_signature.sign(unsigned_raw=unsigned_fund_raw, solver=fund_solver)

print("Fund Signature Fee:", fund_signature.fee)
print("Fund Signature Hash:", fund_signature.hash())
print("Fund Signature Raw:", fund_signature.raw())
print("Fund Signature Json:", json.dumps(fund_signature.json(), indent=4))
print("Fund Signature Unsigned:", json.dumps(fund_signature.unsigned(), indent=4))
print("Fund Signature Transaction Signatures:", json.dumps(signed_fund_transaction.signatures, indent=4))

signed_fund_raw = fund_signature.signed_raw()
print("Fund Signature Signed Raw:", signed_fund_raw)
