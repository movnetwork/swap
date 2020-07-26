#!/usr/bin/env python3

from shuttle.providers.bytom.wallet import Wallet
from shuttle.providers.bytom.htlc import HTLC
from shuttle.providers.bytom.rpc import get_balance
from shuttle.utils import sha256


# Bytom network
NETWORK = "mainnet"
# Secret password/passphrase hash
SECRET_HASH = sha256("Hello Meheret!")
# Recipient Bytom public key
RECIPIENT_PUBLIC_KEY = "3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e"
# Sender Bytom public key
SENDER_PUBLIC_KEY = "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2"
# Expiration block (Sequence)
SEQUENCE = 1000
# Bytom fund asset id
ASSET = "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"

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
    secret_hash=SECRET_HASH,
    recipient_public=recipient_public_key,
    sender_public=sender_public_key,
    sequence=SEQUENCE
)

htlc_bytecode = htlc.bytecode()
print("HTLC Bytecode:", htlc_bytecode)
htlc_opcode = htlc.opcode()
print("HTLC OP_Code:", htlc_opcode)
htlc_hash = htlc.hash()
print("HTLC Hash:", htlc_hash)
htlc_address = htlc.address()
print("HTLC Address:", htlc_address)

# Getting HTLC balance
htlc_balance = get_balance(address=htlc_address, asset=ASSET, network=NETWORK)
print("HTLC Balance:", htlc_balance)
