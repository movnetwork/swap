#!/usr/bin/env python3

from shuttle.providers.bitcoin.wallet import Wallet
from shuttle.providers.bitcoin.transaction import RefundTransaction
from shuttle.providers.bitcoin.solver import RefundSolver
from shuttle.providers.bitcoin.signature import RefundSignature

import json

# Setting network
# mainnet or testnet
network = "testnet"

print("=" * 10, "Sender Bitcoin Account")

sender_passphrase = "meheret tesfaye batu bayou".encode()
print("Sender Passphrase:", sender_passphrase.decode())

# Initialize sender bitcoin wallet
sender_wallet = Wallet(network=network)\
    .from_passphrase(sender_passphrase)
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
print("Sender Balance:", sender_balance, "Satoshi")
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

print("=" * 10, "Hash Time Lock Contract (HTLC) Transaction Id")

# Funded hash time lock contract transaction id/hash
htlc_transaction_id = "51d6a08e8051001dac7f74c3a59b0ef951c7710c66774dafcfb16745c63dc252"
print("HTLC Transaction Id:", htlc_transaction_id)


print("=" * 10, "Unsigned Refund Transaction")

unsigned_refund_transaction = RefundTransaction(version=2, network=network).build_transaction(
    transaction_id=htlc_transaction_id,
    wallet=recipient_wallet,
    amount=5000
)

print("Unsigned Refund Transaction Fee:", unsigned_refund_transaction.fee)
print("Unsigned Refund Transaction Hash:", unsigned_refund_transaction.hash())
print("Unsigned Refund Transaction Raw:", unsigned_refund_transaction.raw())
# print("Unsigned Refund Transaction Json:", json.dumps(unsigned_refund_transaction.json(), indent=4))

unsigned_fund_raw = unsigned_refund_transaction.unsigned_raw()
print("Unsigned Fund Transaction Unsigned Raw:", unsigned_fund_raw)

print("=" * 10, "Signed Refund Transaction")

# Refunding HTLC solver
refund_solver = RefundSolver(
    private_key=sender_private_key,
    secret="Hello Meheret!",
    recipient_address=recipient_address,
    sender_address=sender_address,
    sequence=5
)

signed_refund_transaction = unsigned_refund_transaction.sign(refund_solver)

print("Signed Refund Transaction Fee:", signed_refund_transaction.fee)
print("Signed Refund Transaction Hash:", signed_refund_transaction.hash())
print("Signed Refund Transaction Raw:", signed_refund_transaction.raw())
# print("Signed Refund Transaction Json:", json.dumps(signed_refund_transaction.json(), indent=4))

print("=" * 10, "Refund Signature")

# Singing Hash Time Lock Contract (HTLC)
refund_signature = RefundSignature(network=network)\
    .sign(unsigned_raw=unsigned_fund_raw, solver=refund_solver)

print("Refund Signature Fee:", refund_signature.fee)
print("Refund Signature Hash:", refund_signature.hash())
print("Refund Signature Raw:", refund_signature.raw())
# print("Refund Signature Json:", json.dumps(refund_signature.json(), indent=4))

signed_refund_raw = refund_signature.signed_raw()
print("Refund Signature Signed Raw:", signed_refund_raw)
