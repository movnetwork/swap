#!/usr/bin/env python3

from swap.providers.xinfin.wallet import (
    Wallet, DEFAULT_PATH
)
from swap.providers.xinfin.transaction import WithdrawTransaction
from swap.providers.xinfin.signature import WithdrawSignature
from swap.providers.xinfin.solver import WithdrawSolver
from swap.providers.xinfin.utils import submit_transaction_raw

import json

# Choose network mainnet, apothem or testnet
NETWORK: str = "apothem"
# Enable XinFin HTLC XRC20
XRC20: bool = True
# XinFin HTLC XRC20 contract address
CONTRACT_ADDRESS: str = "xdc4C909fdd6c30f5B4c4d48938C161637B2767d714"
# XinFin HTLC XRC20 funded transaction hash/id
TRANSACTION_HASH: str = "0xfc28ef53d380d98bee785060c0ceaf382078b48af4e94a61aa0997ebcb1ed57b"
# XinFin recipient wallet mnemonic
RECIPIENT_MNEMONIC: str = "hint excuse upgrade sleep easily deputy erase cluster section other ugly limit"
# XinFin XRC20 token address
TOKEN_ADDRESS: str = "xdcd66dA17A97a91445A2B89805e9fa4B0ff649BF49"
# The preimage of HTLC XRC20 contract
SECRET_KEY: str = "Hello Meheret!"

print("=" * 10, "Recipient XinFin Account")

# Initialize XinFin recipient wallet
recipient_wallet: Wallet = Wallet(network=NETWORK)
# Get XinFin recipient wallet from mnemonic
recipient_wallet.from_mnemonic(mnemonic=RECIPIENT_MNEMONIC)
# Drive XinFin recipient wallet from path
recipient_wallet.from_path(path=DEFAULT_PATH)

# Print some XinFin recipient wallet info's
print("Root XPrivate Key:", recipient_wallet.root_xprivate_key())
print("Root XPublic Key:", recipient_wallet.root_xpublic_key())
print("Private Key:", recipient_wallet.private_key())
print("Public Key:", recipient_wallet.public_key())
print("Path:", recipient_wallet.path())
print("Address:", recipient_wallet.address())
print("Balance:", recipient_wallet.balance(unit="XDC"), "XDC")
print("XRC20 Balance:", recipient_wallet.xrc20_balance(token_address=TOKEN_ADDRESS))

print("=" * 10, "Unsigned XRC20 Withdraw Transaction")

# Initialize XRC20 withdraw transaction
unsigned_withdraw_transaction: WithdrawTransaction = WithdrawTransaction(network=NETWORK, xrc20=XRC20)
# Build XRC20 withdraw transaction
unsigned_withdraw_transaction.build_transaction(
    transaction_hash=TRANSACTION_HASH,
    address=recipient_wallet.address(),
    secret_key=SECRET_KEY,
    contract_address=CONTRACT_ADDRESS
)

print("Unsigned XRC20 Withdraw Transaction Fee:", unsigned_withdraw_transaction.fee())
print("Unsigned XRC20 Withdraw Transaction Hash:", unsigned_withdraw_transaction.hash())
print("Unsigned XRC20 Withdraw Transaction Main Raw:", unsigned_withdraw_transaction.raw())
# print("Unsigned XRC20 Withdraw Transaction Json:", json.dumps(unsigned_withdraw_transaction.json(), indent=4))
print("Unsigned XRC20 Withdraw Transaction Signature:", json.dumps(unsigned_withdraw_transaction.signature(), indent=4))
print("Unsigned XRC20 Withdraw Transaction Type:", unsigned_withdraw_transaction.type())

unsigned_withdraw_transaction_raw: str = unsigned_withdraw_transaction.transaction_raw()
print("Unsigned XRC20 Withdraw Transaction Raw:", unsigned_withdraw_transaction_raw)

print("=" * 10, "Signed XRC20 Withdraw Transaction")

# Initialize withdraw solver
withdraw_solver: WithdrawSolver = WithdrawSolver(
    xprivate_key=recipient_wallet.root_xprivate_key(), 
    path=recipient_wallet.path()
)

# Sing unsigned XRC20 withdraw transaction
signed_withdraw_transaction: WithdrawTransaction = unsigned_withdraw_transaction.sign(solver=withdraw_solver)

print("Signed XRC20 Withdraw Transaction Fee:", signed_withdraw_transaction.fee())
print("Signed XRC20 Withdraw Transaction Hash:", signed_withdraw_transaction.hash())
print("Signed XRC20 Withdraw Transaction Main Raw:", signed_withdraw_transaction.raw())
# print("Signed XRC20 Withdraw Transaction Json:", json.dumps(signed_withdraw_transaction.json(), indent=4))
print("Signed XRC20 Withdraw Transaction Signature:", json.dumps(signed_withdraw_transaction.signature(), indent=4))
print("Signed XRC20 Withdraw Transaction Type:", signed_withdraw_transaction.type())

signed_withdraw_transaction_raw: str = signed_withdraw_transaction.transaction_raw()
print("Signed XRC20 Withdraw Transaction Raw:", signed_withdraw_transaction_raw)

print("=" * 10, "XRC20 Withdraw Signature")

# Initialize XRC20 withdraw signature
withdraw_signature: WithdrawSignature = WithdrawSignature(network=NETWORK, xrc20=XRC20)
# Sign unsigned XRC20 withdraw transaction raw
withdraw_signature.sign(
    transaction_raw=unsigned_withdraw_transaction_raw,
    solver=withdraw_solver
)

print("XRC20 Withdraw Signature Fee:", withdraw_signature.fee())
print("XRC20 Withdraw Signature Hash:", withdraw_signature.hash())
print("XRC20 Withdraw Signature Main Raw:", withdraw_signature.raw())
# print("XRC20 Withdraw Signature Json:", json.dumps(withdraw_signature.json(), indent=4))
print("XRC20 Withdraw Signature Transaction Signature:", json.dumps(withdraw_signature.signature(), indent=4))
print("XRC20 Withdraw Signature Type:", withdraw_signature.type())

signed_withdraw_signature_transaction_raw: str = withdraw_signature.transaction_raw()
print("XRC20 Withdraw Signature Transaction Raw:", signed_withdraw_signature_transaction_raw)

# Check both signed XRC20 withdraw transaction raws are equal
assert signed_withdraw_transaction_raw == signed_withdraw_signature_transaction_raw

# Submit XRC20 withdraw transaction raw
# print("\nSubmitted XRC20 Withdraw Transaction:", json.dumps(submit_transaction_raw(
#     transaction_raw=signed_withdraw_transaction_raw  # Or signed_withdraw_signature_transaction_raw
# ), indent=4))
