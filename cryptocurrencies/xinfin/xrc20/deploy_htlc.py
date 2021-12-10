#!/usr/bin/env python3

from swap.providers.xinfin.wallet import Wallet
from swap.providers.xinfin.htlc import HTLC
from swap.providers.xinfin.utils import to_checksum_address
from swap.providers.xinfin.rpc import (
    submit_raw, wait_for_transaction_receipt
)

# Choose network mainnet, apothem or testnet
NETWORK: str = "apothem"
# Deploy new XinFin HTLC XRC20 protocol
XRC20: bool = True
# XinFin private key
PRIVATE_KEY: str = "..."

print("=" * 10, "Deploy new HTLC XRC20 Contract from XinFin Account")

# Initialize XinFin wallet
wallet: Wallet = Wallet(network=NETWORK)
# Get XinFin wallet from private key
wallet.from_private_key(private_key=PRIVATE_KEY)

print("Private Key:", wallet.private_key())
print("Public Key:", wallet.public_key())
print("Address:", wallet.address())
print("Balance:", wallet.balance(unit="XDC"), "XDC")

print("=" * 10, "Compile Hash Time Lock Contract (HTLC) XRC20 Smart contract")

# Initialize XinFin HTLC XRC20
htlc_xrc20: HTLC = HTLC(network=NETWORK, xrc20=XRC20)

print("HTLC XRC20 ABI:", htlc_xrc20.abi())
print("HTLC XRC20 Bytecode:", htlc_xrc20.bytecode())
print("HTLC XRC20 Bytecode Runtime:", htlc_xrc20.bytecode_runtime())
print("HTLC XRC20 OP_Code:", htlc_xrc20.opcode())

print("=" * 10, "Build and Sign HTLC XRC20 Transaction")

# Build HTLC XRC20 transaction
htlc_xrc20.build_transaction(address=wallet.address())

# Sign HTLC XRC20 transaction
htlc_xrc20.sign_transaction(private_key=wallet.private_key())

print("HTLC XRC20 Transaction Fee:", htlc_xrc20.fee(unit="Wei"), "Wei")
print("HTLC XRC20 Transaction Hash:", htlc_xrc20.hash())
print("HTLC XRC20 Transaction Json:", htlc_xrc20.json())
print("HTLC XRC20 Transaction Raw:", htlc_xrc20.raw())

print("=" * 10, "Submit and Wait to be mined for 5 minutes ...")

# Submit HTLC XRC20 transaction raw
submit_raw(transaction_raw=htlc_xrc20.raw(), network=NETWORK)

# Wait 300 seconds for HTLC XRC20 transaction to be mined
transaction_receipt = wait_for_transaction_receipt(
    transaction_hash=htlc_xrc20.hash(), network=NETWORK, timeout=300  # 5 minutes
)

print("HTLC XRC20 Contract Address:", to_checksum_address(transaction_receipt["contractAddress"]))
