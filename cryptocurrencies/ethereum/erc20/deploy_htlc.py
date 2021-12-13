#!/usr/bin/env python3

from swap.providers.ethereum.wallet import Wallet
from swap.providers.ethereum.htlc import HTLC
from swap.providers.ethereum.utils import to_checksum_address
from swap.providers.ethereum.rpc import (
    submit_raw, wait_for_transaction_receipt
)

# Choose network mainnet, ropsten, kovan, rinkeby or testnet
NETWORK: str = "ropsten"
# Deploy new Ethereum HTLC ERC20 protocol.
ERC20: bool = True
# Ethereum private key
PRIVATE_KEY: str = "..."

print("=" * 10, "Deploy HTLC ERC20 from Ethereum Account")

# Initialize Ethereum wallet
wallet: Wallet = Wallet(network=NETWORK)
# Get Ethereum wallet from private key
wallet.from_private_key(private_key=PRIVATE_KEY)

print("Private Key:", wallet.private_key())
print("Public Key:", wallet.public_key())
print("Address:", wallet.address())
print("Balance:", wallet.balance(unit="Ether"), "Ether")

print("=" * 10, "Compile Hash Time Lock Contract (HTLC) ERC20 Smart contract")

# Initialize Ethereum HTLC ERC20
htlc_erc20: HTLC = HTLC(network=NETWORK, erc20=ERC20)

print("HTLC ERC20 ABI:", htlc_erc20.abi())
print("HTLC ERC20 Bytecode:", htlc_erc20.bytecode())
print("HTLC ERC20 Bytecode Runtime:", htlc_erc20.bytecode_runtime())
print("HTLC ERC20 OP_Code:", htlc_erc20.opcode())

print("=" * 10, "Build, Sign and Submit HTLC ERC20 Transaction")

# Build HTLC ERC20 transaction
htlc_erc20.build_transaction(address=wallet.address())

# Sign HTLC ERC20 transaction
htlc_erc20.sign_transaction(private_key=wallet.private_key())

# Submit HTLC ERC20 transaction raw
submit_raw(transaction_raw=htlc_erc20.raw(), network=NETWORK)

print("HTLC ERC20 Transaction Fee:", htlc_erc20.fee(unit="Wei"), "Wei")
print("HTLC ERC20 Transaction Hash:", htlc_erc20.hash())
print("HTLC ERC20 Transaction Json:", htlc_erc20.json())
print("HTLC ERC20 Transaction Raw:", htlc_erc20.raw())

print("=" * 10, "Wait to be mined for 5 minutes ...")

# Wait 300 seconds for HTLC ERC20 transaction to be mined
transaction_receipt = wait_for_transaction_receipt(
    transaction_hash=htlc_erc20.hash(), network=NETWORK, timeout=300  # 5 minutes
)

print("HTLC ERC20 Contract Address:", to_checksum_address(transaction_receipt["contractAddress"]))
