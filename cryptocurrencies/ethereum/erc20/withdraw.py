#!/usr/bin/env python3

from swap.providers.ethereum.wallet import (
    Wallet, DEFAULT_PATH
)
from swap.providers.ethereum.transaction import WithdrawTransaction
from swap.providers.ethereum.signature import WithdrawSignature
from swap.providers.ethereum.solver import WithdrawSolver
from swap.providers.ethereum.utils import submit_transaction_raw

import json

# Choose network mainnet, ropsten, kovan, rinkeby or testnet
NETWORK: str = "ropsten"
# Enable Ethereum HTLC ERC20
ERC20: bool = True
# Ethereum HTLC ERC20 contract address
CONTRACT_ADDRESS: str = "0x761c47A8dc8178d55aE14b661abf26cc0B599bc6"
# Ethereum HTLC ERC20 funded transaction hash/id
TRANSACTION_HASH: str = "0x5632da77014ddfeafa25eae677ce20edf7e0625f07e2db26b1293510c4d63f15"
# Ethereum recipient wallet mnemonic
RECIPIENT_MNEMONIC: str = "hint excuse upgrade sleep easily deputy erase cluster section other ugly limit"
# Ethereum ERC20 token address
TOKEN_ADDRESS: str = "0xa6f89f08cC9d112870E2561F1A8D750681DB59f1"
# The preimage of HTLC ERC20 contract
SECRET_KEY: str = "Hello Meheret!"

print("=" * 10, "Recipient Ethereum Account")

# Initialize Ethereum recipient wallet
recipient_wallet: Wallet = Wallet(network=NETWORK)
# Get Ethereum recipient wallet from mnemonic
recipient_wallet.from_mnemonic(mnemonic=RECIPIENT_MNEMONIC)
# Drive Ethereum recipient wallet from path
recipient_wallet.from_path(path=DEFAULT_PATH)

# Print some Ethereum recipient wallet info's
print("Root XPrivate Key:", recipient_wallet.root_xprivate_key())
print("Root XPublic Key:", recipient_wallet.root_xpublic_key())
print("Private Key:", recipient_wallet.private_key())
print("Public Key:", recipient_wallet.public_key())
print("Path:", recipient_wallet.path())
print("Address:", recipient_wallet.address())
print("Balance:", recipient_wallet.balance(unit="Ether"), "Ether")
print("ERC20 Balance:", recipient_wallet.erc20_balance(token_address=TOKEN_ADDRESS))

print("=" * 10, "Unsigned ERC20 Withdraw Transaction")

# Initialize ERC20 withdraw transaction
unsigned_withdraw_transaction: WithdrawTransaction = WithdrawTransaction(network=NETWORK, erc20=ERC20)
# Build ERC20 withdraw transaction
unsigned_withdraw_transaction.build_transaction(
    transaction_hash=TRANSACTION_HASH,
    address=recipient_wallet.address(),
    secret_key=SECRET_KEY,
    contract_address=CONTRACT_ADDRESS
)

print("Unsigned ERC20 Withdraw Transaction Fee:", unsigned_withdraw_transaction.fee())
print("Unsigned ERC20 Withdraw Transaction Hash:", unsigned_withdraw_transaction.hash())
print("Unsigned ERC20 Withdraw Transaction Main Raw:", unsigned_withdraw_transaction.raw())
# print("Unsigned ERC20 Withdraw Transaction Json:", json.dumps(unsigned_withdraw_transaction.json(), indent=4))
print("Unsigned ERC20 Withdraw Transaction Signature:", json.dumps(unsigned_withdraw_transaction.signature(), indent=4))
print("Unsigned ERC20 Withdraw Transaction Type:", unsigned_withdraw_transaction.type())

unsigned_withdraw_transaction_raw: str = unsigned_withdraw_transaction.transaction_raw()
print("Unsigned ERC20 Withdraw Transaction Raw:", unsigned_withdraw_transaction_raw)

print("=" * 10, "Signed ERC20 Withdraw Transaction")

# Initialize withdraw solver
withdraw_solver: WithdrawSolver = WithdrawSolver(
    xprivate_key=recipient_wallet.root_xprivate_key(), 
    path=recipient_wallet.path()
)

# Sing unsigned ERC20 withdraw transaction
signed_withdraw_transaction: WithdrawTransaction = unsigned_withdraw_transaction.sign(solver=withdraw_solver)

print("Signed ERC20 Withdraw Transaction Fee:", signed_withdraw_transaction.fee())
print("Signed ERC20 Withdraw Transaction Hash:", signed_withdraw_transaction.hash())
print("Signed ERC20 Withdraw Transaction Main Raw:", signed_withdraw_transaction.raw())
# print("Signed ERC20 Withdraw Transaction Json:", json.dumps(signed_withdraw_transaction.json(), indent=4))
print("Signed ERC20 Withdraw Transaction Signature:", json.dumps(signed_withdraw_transaction.signature(), indent=4))
print("Signed ERC20 Withdraw Transaction Type:", signed_withdraw_transaction.type())

signed_withdraw_transaction_raw: str = signed_withdraw_transaction.transaction_raw()
print("Signed ERC20 Withdraw Transaction Raw:", signed_withdraw_transaction_raw)

print("=" * 10, "ERC20 Withdraw Signature")

# Initialize ERC20 withdraw signature
withdraw_signature: WithdrawSignature = WithdrawSignature(network=NETWORK, erc20=ERC20)
# Sign unsigned ERC20 withdraw transaction raw
withdraw_signature.sign(
    transaction_raw=unsigned_withdraw_transaction_raw,
    solver=withdraw_solver
)

print("ERC20 Withdraw Signature Fee:", withdraw_signature.fee())
print("ERC20 Withdraw Signature Hash:", withdraw_signature.hash())
print("ERC20 Withdraw Signature Main Raw:", withdraw_signature.raw())
# print("ERC20 Withdraw Signature Json:", json.dumps(withdraw_signature.json(), indent=4))
print("ERC20 Withdraw Signature Transaction Signature:", json.dumps(withdraw_signature.signature(), indent=4))
print("ERC20 Withdraw Signature Type:", withdraw_signature.type())

signed_withdraw_signature_transaction_raw: str = withdraw_signature.transaction_raw()
print("ERC20 Withdraw Signature Transaction Raw:", signed_withdraw_signature_transaction_raw)

# Check both signed ERC20 withdraw transaction raws are equal
assert signed_withdraw_transaction_raw == signed_withdraw_signature_transaction_raw

# Submit ERC20 withdraw transaction raw
# print("\nSubmitted ERC20 Withdraw Transaction:", json.dumps(submit_transaction_raw(
#     transaction_raw=signed_withdraw_transaction_raw  # Or signed_withdraw_signature_transaction_raw
# ), indent=4))
