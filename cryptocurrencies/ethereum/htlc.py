#!/usr/bin/env python3

from swap.providers.ethereum.htlc import HTLC
from swap.utils import (
    sha256, get_current_timestamp
)

# Choose network mainnet, ropsten, kovan, rinkeby or testnet
NETWORK: str = "testnet"
# Ethereum HTLC transaction hash
HTLC_TRANSACTION_HASH: str = "0x728c83cc83bb4b1a67fbfd480a9bdfdd55cb5fc6fd519f6a98fa35db3a2a9160"
# Secret key hash
SECRET_HASH: str = sha256("Hello Meheret!")
# Recipient Ethereum address
RECIPIENT_ADDRESS: str = "0xd77E0d2Eef905cfB39c3C4b952Ed278d58f96E1f"
# Sender Ethereum address
SENDER_ADDRESS: str = "0x69e04fe16c9A6A83076B3c2dc4b4Bc21b5d9A20C"
# Expiration block time (Seconds)
ENDTIME: int = get_current_timestamp() + 300  # 300 sec equal to 5 min

print("=" * 10, "Hash Time Lock Contract (HTLC) between Sender and Recipient")

# Initialize Ethereum HTLC
htlc: HTLC = HTLC(
    transaction_hash=HTLC_TRANSACTION_HASH, network=NETWORK
)
# Build HTLC contract
htlc.build_htlc(
    secret_hash=SECRET_HASH,
    recipient_address=RECIPIENT_ADDRESS,
    sender_address=SENDER_ADDRESS,
    endtime=ENDTIME
)

# Print all Ethereum HTLC info's
print("HTLC ABI:", htlc.abi())
print("HTLC Bytecode:", htlc.bytecode())
print("HTLC Bytecode Runtime:", htlc.bytecode_runtime())
print("HTLC OP_Code:", htlc.opcode())
print("HTLC Contract Address:", htlc.contract_address())
print("HTLC Balance:", htlc.balance(unit="Ether"), "Ether")
