#!/usr/bin/env python3

from swap.providers.ethereum.wallet import (
    Wallet, DEFAULT_PATH
)
from swap.providers.ethereum.transaction import NormalTransaction
from swap.providers.ethereum.signature import NormalSignature
from swap.providers.ethereum.solver import NormalSolver
from swap.providers.ethereum.rpc import get_erc20_decimals
from swap.providers.ethereum.utils import submit_transaction_raw

import json

# Choose network mainnet, ropsten, kovan, rinkeby or testnet
NETWORK: str = "ropsten"
# Enable Ethereum ERC20
ERC20: bool = True
# Ethereum sender wallet mnemonic
SENDER_MNEMONIC: str = "unfair divorce remind addict add roof park clown build renew illness fault"
# Ethereum ERC20 token address
TOKEN_ADDRESS: str = "0xa6f89f08cC9d112870E2561F1A8D750681DB59f1"
# Ethereum recipient address and amount
RECIPIENT: dict = {
    "0x1954C47a5D75bdDA53578CEe5D549bf84b8c6B94": 25 * (10 ** get_erc20_decimals(token_address=TOKEN_ADDRESS, network=NETWORK))
}

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

print("=" * 10, "Unsigned ERC20 Normal Transaction")

# Initialize ERC20 normal transaction
unsigned_normal_transaction: NormalTransaction = NormalTransaction(network=NETWORK, erc20=ERC20)
# Build ERC20 normal transaction
unsigned_normal_transaction.build_transaction(
    address=sender_wallet.address(), recipient=RECIPIENT, token_address=TOKEN_ADDRESS
)

print("Unsigned ERC20 Normal Transaction Fee:", unsigned_normal_transaction.fee())
print("Unsigned ERC20 Normal Transaction Hash:", unsigned_normal_transaction.hash())
print("Unsigned ERC20 Normal Transaction Raw:", unsigned_normal_transaction.raw())
# print("Unsigned ERC20 Normal Transaction Json:", json.dumps(unsigned_normal_transaction.json(), indent=4))
print("Unsigned ERC20 Normal Transaction Signature:", json.dumps(unsigned_normal_transaction.signature(), indent=4))
print("Unsigned ERC20 Normal Transaction Type:", unsigned_normal_transaction.type())

unsigned_normal_transaction_raw: str = unsigned_normal_transaction.transaction_raw()
print("Unsigned ERC20 Normal Transaction Raw:", unsigned_normal_transaction_raw)

print("=" * 10, "Signed ERC20 Normal Transaction")

# Initialize normal solver
normal_solver: NormalSolver = NormalSolver(
    xprivate_key=sender_wallet.root_xprivate_key(), 
    path=sender_wallet.path()
)

# Sing unsigned ERC20 normal transaction
signed_normal_transaction: NormalTransaction = unsigned_normal_transaction.sign(solver=normal_solver)

print("Signed ERC20 Normal Transaction Fee:", signed_normal_transaction.fee())
print("Signed ERC20 Normal Transaction Hash:", signed_normal_transaction.hash())
print("Signed ERC20 Normal Transaction Main Raw:", signed_normal_transaction.raw())
# print("Signed Normal Transaction Json:", json.dumps(signed_normal_transaction.json(), indent=4))
print("Signed ERC20 Normal Transaction Signature:", json.dumps(signed_normal_transaction.signature(), indent=4))
print("Signed ERC20 Normal Transaction Type:", signed_normal_transaction.type())

signed_normal_transaction_raw: str = signed_normal_transaction.transaction_raw()
print("Signed ERC20 Normal Transaction Raw:", signed_normal_transaction_raw)

print("=" * 10, "ERC20 Normal Signature")

# Initialize ERC20 normal signature
normal_signature: NormalSignature = NormalSignature(network=NETWORK, erc20=ERC20)
# Sign unsigned ERC20 normal transaction raw
normal_signature.sign(
    transaction_raw=unsigned_normal_transaction_raw,
    solver=normal_solver
)

print("ERC20 Normal Signature Fee:", normal_signature.fee())
print("ERC20 Normal Signature Hash:", normal_signature.hash())
print("ERC20 Normal Signature Raw:", normal_signature.raw())
# print("ERC20 Normal Signature Json:", json.dumps(normal_signature.json(), indent=4))
print("ERC20 Normal Signature Signature:", json.dumps(normal_signature.signature(), indent=4))
print("ERC20 Normal Signature Type:", normal_signature.type())

signed_normal_signature_transaction_raw: str = normal_signature.transaction_raw()
print("ERC20 Normal Signature Transaction Raw:", signed_normal_signature_transaction_raw)

# Check both signed normal transaction raws are equal
assert signed_normal_transaction_raw == signed_normal_signature_transaction_raw

# Submit ERC20 normal transaction raw
# print("\nSubmitted ERC20 Normal Transaction:", json.dumps(submit_transaction_raw(
#     transaction_raw=signed_normal_transaction_raw  # Or signed_normal_signature_transaction_raw
# ), indent=4))
