#!/usr/bin/env python3

from swap.providers.ethereum.htlc import HTLC
from swap.utils import (
    sha256, get_current_timestamp
)

import json

# Choose network mainnet, ropsten, kovan, rinkeby or testnet
NETWORK: str = "ropsten"
# Ethereum HTLC contract address
CONTRACT_ADDRESS: str = "0x0cc7C744f96729B7f60B12B36A4B9504191CD458"
# Secret key hash
SECRET_HASH: str = sha256("Hello Meheret!")
# Ethereum recipient address
RECIPIENT_ADDRESS: str = "0x1954C47a5D75bdDA53578CEe5D549bf84b8c6B94"
# Ethereum sender address
SENDER_ADDRESS: str = "0x69e04fe16c9A6A83076B3c2dc4b4Bc21b5d9A20C"
# Expiration block timestamp
ENDTIME: int = get_current_timestamp(plus=3600)  # 1 hour

print("=" * 10, "Hash Time Lock Contract (HTLC) between Sender and Recipient")

# Initialize Ethereum HTLC
htlc: HTLC = HTLC(
    contract_address=CONTRACT_ADDRESS, network=NETWORK
)
# Build HTLC contract
htlc.build_htlc(
    secret_hash=SECRET_HASH,
    recipient_address=RECIPIENT_ADDRESS,
    sender_address=SENDER_ADDRESS,
    endtime=ENDTIME
)

# Print all Ethereum HTLC info's
print("HTLC Agreements:", json.dumps(htlc.agreements, indent=4))
print("HTLC ABI:", htlc.abi())
print("HTLC Bytecode:", htlc.bytecode())
print("HTLC Bytecode Runtime:", htlc.bytecode_runtime())
print("HTLC OP_Code:", htlc.opcode())
print("HTLC Contract Address:", htlc.contract_address())
print("HTLC Balance:", htlc.balance(unit="Ether"), "Ether")
