#!/usr/bin/env python3

from swap.providers.ethereum.wallet import Wallet
from swap.providers.ethereum.htlc import HTLC
from swap.providers.ethereum.rpc import (
    submit_raw, wait_for_transaction_receipt
)

# Choose network mainnet, ropsten, kovan, rinkeby or testnet
NETWORK: str = "testnet"
# Ethereum private key
PRIVATE_KEY: str = "cf4c2fb2b88a556c211d5fe79335dcee6dd11403bbbc5b47a530e9cf56ee3aee"

# Initialize Ethereum wallet
wallet: Wallet = Wallet(network=NETWORK)
# Get Ethereum wallet from private key
wallet.from_private_key(private_key=PRIVATE_KEY)

print("=" * 10, "Compile Hash Time Lock Contract (HTLC) Smart contract")

# Initialize Ethereum HTLC
htlc: HTLC = HTLC(network=NETWORK)

print("HTLC ABI:", htlc.abi())
print("HTLC Bytecode:", htlc.bytecode())
print("HTLC Bytecode Runtime:", htlc.bytecode_runtime())
print("HTLC OP_Code:", htlc.opcode())

print("=" * 10, "Build, Sign and Submit HTLC Transaction | Wait to be mined")

# Build HTLC transaction
htlc.build_transaction(address=wallet.address())

# Sign HTLC transaction
htlc.sign_transaction(private_key=wallet.private_key())

# Submit HTLC transaction raw
submit_raw(transaction_raw=htlc.raw(), network=NETWORK)

# Wait 60 seconds for HTLC transaction to be mined
wait_for_transaction_receipt(
    transaction_hash=htlc.hash(), network=NETWORK, timeout=60
)

print("HTLC Fee:", htlc.fee(), "Wei")
print("HTLC Transaction Hash:", htlc.hash())
print("HTLC Transaction Json:", htlc.json())
print("HTLC Transaction Raw:", htlc.raw())
