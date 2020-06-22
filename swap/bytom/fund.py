#!/usr/bin/env python3

from shuttle.providers.bytom.wallet import Wallet
from shuttle.providers.bytom.htlc import HTLC
from shuttle.providers.bytom.transaction import FundTransaction
from shuttle.providers.bytom.solver import FundSolver
from shuttle.providers.bytom.signature import FundSignature
from shuttle.utils import sha256

import json

# Bytom network
NETWORK = "mainnet"
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

print("=" * 10, "Hash Time Lock Contract (HTLC) between Sender and Recipient")

# Initializing Hash Time Lock Contract (HTLC)
htlc = HTLC(network=NETWORK).init(
    secret_hash=sha256("Hello Meheret!".encode()).hex(),
    recipient_public=recipient_public_key,
    sender_public=sender_public_key,
    sequence=1000
)

htlc_bytecode = htlc.bytecode()
print("HTLC Bytecode:", htlc_bytecode)
htlc_opcode = htlc.opcode()
print("HTLC OP_Code:", htlc_opcode)
htlc_hash = htlc.hash()
print("HTLC Hash:", htlc_hash)
htlc_address = htlc.address()
print("HTLC Address:", htlc_address)

print("=" * 10, "Unsigned Fund Transaction")

# Initializing fund transaction
unsigned_fund_transaction = FundTransaction(network=NETWORK)
# Building fund transaction
unsigned_fund_transaction.build_transaction(
    wallet=sender_wallet,
    htlc=htlc,
    amount=AMOUNT,
    asset=ASSET
)

print("Unsigned Fund Transaction Fee:", unsigned_fund_transaction.fee())
print("Unsigned Fund Transaction Hash:", unsigned_fund_transaction.hash())
print("Unsigned Fund Transaction Raw:", unsigned_fund_transaction.raw())
# print("Unsigned Fund Transaction Json:", json.dumps(unsigned_fund_transaction.json(), indent=4))
print("Unsigned Fund Transaction Unsigned Datas:", json.dumps(unsigned_fund_transaction.unsigned_datas(), indent=4))
print("Unsigned Fund Transaction Signatures:", json.dumps(unsigned_fund_transaction.signatures(), indent=4))

unsigned_fund_raw = unsigned_fund_transaction.unsigned_raw()
print("Unsigned Fund Transaction Unsigned Raw:", unsigned_fund_raw)

print("=" * 10, "Signed Fund Transaction")

# Initializing fund solver
fund_solver = FundSolver(
    xprivate_key=sender_xprivate_key,
    path="m/44/153/1/0/1"
)

# Singing unsigned fund transaction
signed_fund_transaction = unsigned_fund_transaction.sign(fund_solver)

print("Signed Fund Transaction Fee:", signed_fund_transaction.fee())
print("Signed Fund Transaction Hash:", signed_fund_transaction.hash())
print("Signed Fund Transaction Raw:", signed_fund_transaction.raw())
# print("Signed Fund Transaction Json:", json.dumps(signed_fund_transaction.json(), indent=4))
print("Signed Fund Transaction Unsigned Datas:", json.dumps(signed_fund_transaction.unsigned_datas(), indent=4))
print("Signed Fund Transaction Signatures:", json.dumps(signed_fund_transaction.signatures(), indent=4))

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
print("Fund Signature Unsigned Datas:", json.dumps(fund_signature.unsigned_datas(), indent=4))
print("Fund Signature Transaction Signatures:", json.dumps(fund_signature.signatures(), indent=4))

signed_fund_raw = fund_signature.signed_raw()
print("Fund Signature Signed Raw:", signed_fund_raw)
