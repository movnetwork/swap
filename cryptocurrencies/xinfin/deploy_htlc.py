#!/usr/bin/env python3

from swap.providers.xinfin.wallet import Wallet
from swap.providers.xinfin.htlc import HTLC
from swap.providers.xinfin.utils import to_checksum_address
from swap.providers.xinfin.rpc import (
    submit_raw, wait_for_transaction_receipt
)

# Choose network mainnet or testnet
NETWORK: str = "mainnet"
# XinFin private key
PRIVATE_KEY: str = "..."

print("=" * 10, "Deploy HTLC from XinFin Account")

# Initialize XinFin wallet
wallet: Wallet = Wallet(network=NETWORK)
# Get XinFin wallet from private key
wallet.from_private_key(private_key=PRIVATE_KEY)

print("Private Key:", wallet.private_key())
print("Public Key:", wallet.public_key())
print("Address:", wallet.address())
print("Balance:", wallet.balance(unit="XDC"), "XDC")

print("=" * 10, "Compile Hash Time Lock Contract (HTLC) Smart contract")

# Initialize XinFin HTLC
htlc: HTLC = HTLC(network=NETWORK)

print("HTLC ABI:", htlc.abi())
print("HTLC Bytecode:", htlc.bytecode())
print("HTLC Bytecode Runtime:", htlc.bytecode_runtime())
print("HTLC OP_Code:", htlc.opcode())

print("=" * 10, "Build, Sign and Submit HTLC Transaction")

# Build HTLC transaction
htlc.build_transaction(address=wallet.address())

# Sign HTLC transaction
htlc.sign_transaction(private_key=wallet.private_key())

# Submit HTLC transaction raw
submit_raw(transaction_raw=htlc.raw(), network=NETWORK)

print("HTLC Transaction Fee:", htlc.fee(unit="Wei"), "Wei")
print("HTLC Transaction Hash:", htlc.hash())
print("HTLC Transaction Json:", htlc.json())
print("HTLC Transaction Raw:", htlc.raw())

print("=" * 10, "Wait to be mined for 5 minutes ...")

# Wait 300 seconds for HTLC transaction to be mined
transaction_receipt = wait_for_transaction_receipt(
    transaction_hash=htlc.hash(), network=NETWORK, timeout=300  # 5 minutes
)

print("HTLC Contract Address:", to_checksum_address(transaction_receipt["contractAddress"]))
