#!/usr/bin/env python3

from swap.providers.ethereum.wallet import (
    Wallet, DEFAULT_PATH
)
from swap.providers.ethereum.transaction import RefundTransaction
from swap.providers.ethereum.signature import RefundSignature
from swap.providers.ethereum.solver import RefundSolver
from swap.providers.ethereum.utils import submit_transaction_raw

import json

# Choose network mainnet, ropsten, kovan, rinkeby or testnet
NETWORK: str = "ropsten"
# Enable Ethereum HTLC ERC20
ERC20: bool = True
# Ethereum HTLC ERC20 contract address
CONTRACT_ADDRESS: str = "0x761c47A8dc8178d55aE14b661abf26cc0B599bc6"
# Ethereum HTLC ERC20 funded transaction hash/id
TRANSACTION_HASH: str = "0x21f93142225519a878dffad54e9ab58e8ea8a1ba50888704acbc2b7edd5d2ee6"
# Ethereum sender wallet mnemonic
SENDER_MNEMONIC: str = "unfair divorce remind addict add roof park clown build renew illness fault"
# Ethereum ERC20 token address
TOKEN_ADDRESS: str = "0xa6f89f08cC9d112870E2561F1A8D750681DB59f1"

print("=" * 10, "Sender Ethereum Account")

# Initialize Ethereum sender wallet
sender_wallet: Wallet = Wallet(network=NETWORK)
# Get Ethereum sender wallet from mnemonic
sender_wallet.from_mnemonic(mnemonic=SENDER_MNEMONIC)
# Drive Ethereum sender wallet from path
sender_wallet.from_path(path=DEFAULT_PATH)

# Print some Ethereum sender wallet info's
print("Root XPrivate Key:", sender_wallet.root_xprivate_key())
print("Root XPublic Key:", sender_wallet.root_xpublic_key())
print("Private Key:", sender_wallet.private_key())
print("Public Key:", sender_wallet.public_key())
print("Path:", sender_wallet.path())
print("Address:", sender_wallet.address())
print("Balance:", sender_wallet.balance(unit="Ether"), "Ether")
print("ERC20 Balance:", sender_wallet.erc20_balance(token_address=TOKEN_ADDRESS))

print("=" * 10, "Unsigned ERC20 Refund Transaction")

# Initialize ERC20 refund transaction
unsigned_refund_transaction: RefundTransaction = RefundTransaction(network=NETWORK, erc20=ERC20)
# Build ERC20 refund transaction
unsigned_refund_transaction.build_transaction(
    transaction_hash=TRANSACTION_HASH,
    address=sender_wallet.address(),
    contract_address=CONTRACT_ADDRESS
)

print("Unsigned ERC20 Refund Transaction Fee:", unsigned_refund_transaction.fee())
print("Unsigned ERC20 Refund Transaction Hash:", unsigned_refund_transaction.hash())
print("Unsigned ERC20 Refund Transaction Main Raw:", unsigned_refund_transaction.raw())
# print("Unsigned ERC20 Refund Transaction Json:", json.dumps(unsigned_refund_transaction.json(), indent=4))
print("Unsigned ERC20 Refund Transaction Signature:", json.dumps(unsigned_refund_transaction.signature(), indent=4))
print("Unsigned ERC20 Refund Transaction Type:", unsigned_refund_transaction.type())

unsigned_refund_transaction_raw: str = unsigned_refund_transaction.transaction_raw()
print("Unsigned ERC20 Refund Transaction Raw:", unsigned_refund_transaction_raw)

print("=" * 10, "Signed ERC20 Refund Transaction")

# Initialize refund solver
refund_solver: RefundSolver = RefundSolver(
    xprivate_key=sender_wallet.root_xprivate_key(),
    path=sender_wallet.path()
)

# Sing unsigned ERC20 refund transaction
signed_refund_transaction: RefundTransaction = unsigned_refund_transaction.sign(solver=refund_solver)

print("Signed ERC20 Refund Transaction Fee:", signed_refund_transaction.fee())
print("Signed ERC20 Refund Transaction Hash:", signed_refund_transaction.hash())
print("Signed ERC20 Refund Transaction Main Raw:", signed_refund_transaction.raw())
# print("Signed ERC20 Refund Transaction Json:", json.dumps(signed_refund_transaction.json(), indent=4))
print("Signed ERC20 Refund Transaction Signature:", json.dumps(signed_refund_transaction.signature(), indent=4))
print("Signed ERC20 Refund Transaction Type:", signed_refund_transaction.type())

signed_refund_transaction_raw: str = signed_refund_transaction.transaction_raw()
print("Signed ERC20 Refund Transaction Raw:", signed_refund_transaction_raw)

print("=" * 10, "ERC20 Refund Signature")

# Initialize ERC20 refund signature
refund_signature: RefundSignature = RefundSignature(network=NETWORK, erc20=ERC20)
# Sign unsigned ERC20 refund transaction raw
refund_signature.sign(
    transaction_raw=unsigned_refund_transaction_raw,
    solver=refund_solver
)

print("ERC20 Refund Signature Fee:", refund_signature.fee())
print("ERC20 Refund Signature Hash:", refund_signature.hash())
print("ERC20 Refund Signature Main Raw:", refund_signature.raw())
# print("ERC20 Refund Signature Json:", json.dumps(refund_signature.json(), indent=4))
print("ERC20 Refund Signature Signature:", json.dumps(refund_signature.signature(), indent=4))
print("ERC20 Refund Signature Type:", refund_signature.type())

signed_refund_signature_transaction_raw: str = refund_signature.transaction_raw()
print("ERC20 Refund Signature Transaction Raw:", signed_refund_signature_transaction_raw)

# Check both signed ERC20 refund transaction raws are equal
assert signed_refund_transaction_raw == signed_refund_signature_transaction_raw

# Submit ERC20 refund transaction raw
# print("\nSubmitted ERC20 Refund Transaction:", json.dumps(submit_transaction_raw(
#     transaction_raw=signed_refund_transaction_raw  # Or signed_refund_signature_transaction_raw
# ), indent=4))
