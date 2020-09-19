#!/usr/bin/env python3

from swap.providers.bitcoin.htlc import HTLC
from swap.providers.bitcoin.rpc import get_balance
from swap.utils import sha256

# Bitcoin network
NETWORK: str = "testnet"
# Secret password/passphrase hash
SECRET_HASH: str = sha256("Hello Meheret!")
# Recipient Bitcoin address
RECIPIENT_ADDRESS: str = "mwHXvCcug5Rn24c2rpgcRDSo3PyfxZJQQT"
# Sender Bitcoin address
SENDER_ADDRESS: str = "miAcLpYbaqE8KowBu2PwvqXG6y6vpQcfTJ"
# Expiration block (Sequence)
SEQUENCE: int = 1000

print("=" * 10, "Hash Time Lock Contract (HTLC) between Sender and Recipient")

# Initialize Hash Time Lock Contract (HTLC)
htlc: HTLC = HTLC(network=NETWORK)
# Build new HTLC contract
htlc.build(
    secret_hash=SECRET_HASH,
    recipient_address=RECIPIENT_ADDRESS,
    sender_address=SENDER_ADDRESS,
    sequence=SEQUENCE,
)

print("HTLC Bytecode:", htlc.bytecode())
print("HTLC OP_Code:", htlc.opcode())
print("HTLC Hash:", htlc.hash())
print("HTLC Address:", htlc.address())

# Get HTLC balance
print("HTLC Balance:", get_balance(
    address=htlc.address(), network=NETWORK
))
