#!/usr/bin/env python3

from swap.providers.bitcoin.htlc import HTLC
from swap.utils import (
    sha256, get_current_timestamp
)

import json

# Choose network mainnet or testnet
NETWORK: str = "testnet"
# Secret key hash
SECRET_HASH: str = sha256("Hello Meheret!")
# Bitcoin recipient address
RECIPIENT_ADDRESS: str = "mgS3WMHp9nvdUPeDJxr5iCF2P5HuFZSR3V"
# Bitcoin sender address
SENDER_ADDRESS: str = "n1wgm6kkzMcNfAtJmes8YhpvtDzdNhDY5a"
# Expiration contract timestamp
ENDTIME: int = get_current_timestamp(plus=3600)  # 1 hour

print("=" * 10, "Hash Time Lock Contract (HTLC) between Sender and Recipient")

# Initialize Bitcoin HTLC
htlc: HTLC = HTLC(network=NETWORK)
# Build HTLC contract
htlc.build_htlc(
    secret_hash=SECRET_HASH,
    recipient_address=RECIPIENT_ADDRESS,
    sender_address=SENDER_ADDRESS,
    endtime=ENDTIME
)

# Print all Bitcoin HTLC info's
print("HTLC Agreements:", json.dumps(htlc.agreements, indent=4))
print("HTLC Bytecode:", htlc.bytecode())
print("HTLC OP_Code:", htlc.opcode())
print("HTLC Hash:", htlc.hash())
print("HTLC Contract Address:", htlc.contract_address())
print("HTLC Balance:", htlc.balance(unit="BTC"), "BTC")
print("HTLC UTXO's:", htlc.utxos())
