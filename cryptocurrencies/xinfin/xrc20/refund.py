#!/usr/bin/env python3

from swap.providers.xinfin.wallet import (
    Wallet, DEFAULT_PATH
)
from swap.providers.xinfin.transaction import RefundTransaction
from swap.providers.xinfin.signature import RefundSignature
from swap.providers.xinfin.solver import RefundSolver
from swap.providers.xinfin.utils import submit_transaction_raw

import json

# Choose network mainnet, apothem or testnet
NETWORK: str = "apothem"
# Enable XinFin HTLC XRC20 protocol
XRC20: bool = True
# XinFin HTLC XRC20 contract address
CONTRACT_ADDRESS: str = "xdc4C909fdd6c30f5B4c4d48938C161637B2767d714"
# XinFin HTLC XRC20 funded transaction hash/id
TRANSACTION_HASH: str = "0x46e6169d8dbf0072000cbb81fbb5233029e86f5172f4eb8d13e9f59119f52127"
# XinFin sender wallet mnemonic
SENDER_MNEMONIC: str = "unfair divorce remind addict add roof park clown build renew illness fault"
# XinFin XRC20 token address
TOKEN_ADDRESS: str = "xdcd66dA17A97a91445A2B89805e9fa4B0ff649BF49"

print("=" * 10, "Sender XinFin Account")

# Initialize XinFin sender wallet
sender_wallet: Wallet = Wallet(network=NETWORK)
# Get XinFin sender wallet from mnemonic
sender_wallet.from_mnemonic(mnemonic=SENDER_MNEMONIC)
# Drive XinFin sender wallet from path
sender_wallet.from_path(path=DEFAULT_PATH)

# Print some XinFin sender wallet info's
print("Root XPrivate Key:", sender_wallet.root_xprivate_key())
print("Root XPublic Key:", sender_wallet.root_xpublic_key())
print("Private Key:", sender_wallet.private_key())
print("Public Key:", sender_wallet.public_key())
print("Path:", sender_wallet.path())
print("Address:", sender_wallet.address())
print("Balance:", sender_wallet.balance(unit="XDC"), "XDC")
print("XRC20 Balance:", sender_wallet.xrc20_balance(token_address=TOKEN_ADDRESS))

print("=" * 10, "Unsigned XRC20 Refund Transaction")

# Initialize XRC20 refund transaction
unsigned_refund_transaction: RefundTransaction = RefundTransaction(network=NETWORK, xrc20=XRC20)
# Build XRC20 refund transaction
unsigned_refund_transaction.build_transaction(
    transaction_hash=TRANSACTION_HASH,
    address=sender_wallet.address(),
    contract_address=CONTRACT_ADDRESS
)

print("Unsigned XRC20 Refund Transaction Fee:", unsigned_refund_transaction.fee())
print("Unsigned XRC20 Refund Transaction Hash:", unsigned_refund_transaction.hash())
print("Unsigned XRC20 Refund Transaction Main Raw:", unsigned_refund_transaction.raw())
# print("Unsigned XRC20 Refund Transaction Json:", json.dumps(unsigned_refund_transaction.json(), indent=4))
print("Unsigned XRC20 Refund Transaction Signature:", json.dumps(unsigned_refund_transaction.signature(), indent=4))
print("Unsigned XRC20 Refund Transaction Type:", unsigned_refund_transaction.type())

unsigned_refund_transaction_raw: str = unsigned_refund_transaction.transaction_raw()
print("Unsigned XRC20 Refund Transaction Raw:", unsigned_refund_transaction_raw)

print("=" * 10, "Signed XRC20 Refund Transaction")

# Initialize refund solver
refund_solver: RefundSolver = RefundSolver(
    xprivate_key=sender_wallet.root_xprivate_key(),
    path=sender_wallet.path()
)

# Sing unsigned XRC20 refund transaction
signed_refund_transaction: RefundTransaction = unsigned_refund_transaction.sign(solver=refund_solver)

print("Signed XRC20 Refund Transaction Fee:", signed_refund_transaction.fee())
print("Signed XRC20 Refund Transaction Hash:", signed_refund_transaction.hash())
print("Signed XRC20 Refund Transaction Main Raw:", signed_refund_transaction.raw())
# print("Signed XRC20 Refund Transaction Json:", json.dumps(signed_refund_transaction.json(), indent=4))
print("Signed XRC20 Refund Transaction Signature:", json.dumps(signed_refund_transaction.signature(), indent=4))
print("Signed XRC20 Refund Transaction Type:", signed_refund_transaction.type())

signed_refund_transaction_raw: str = signed_refund_transaction.transaction_raw()
print("Signed XRC20 Refund Transaction Raw:", signed_refund_transaction_raw)

print("=" * 10, "XRC20 Refund Signature")

# Initialize XRC20 refund signature
refund_signature: RefundSignature = RefundSignature(network=NETWORK, xrc20=XRC20)
# Sign unsigned XRC20 refund transaction raw
refund_signature.sign(
    transaction_raw=unsigned_refund_transaction_raw,
    solver=refund_solver
)

print("XRC20 Refund Signature Fee:", refund_signature.fee())
print("XRC20 Refund Signature Hash:", refund_signature.hash())
print("XRC20 Refund Signature Main Raw:", refund_signature.raw())
# print("XRC20 Refund Signature Json:", json.dumps(refund_signature.json(), indent=4))
print("XRC20 Refund Signature Signature:", json.dumps(refund_signature.signature(), indent=4))
print("XRC20 Refund Signature Type:", refund_signature.type())

signed_refund_signature_transaction_raw: str = refund_signature.transaction_raw()
print("XRC20 Refund Signature Transaction Raw:", signed_refund_signature_transaction_raw)

# Check both signed XRC20 refund transaction raws are equal
assert signed_refund_transaction_raw == signed_refund_signature_transaction_raw

# Submit XRC20 refund transaction raw
# print("\nSubmitted XRC20 Refund Transaction:", json.dumps(submit_transaction_raw(
#     transaction_raw=signed_refund_transaction_raw  # Or signed_refund_signature_transaction_raw
# ), indent=4))
