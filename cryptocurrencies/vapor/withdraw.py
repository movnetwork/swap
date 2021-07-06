#!/usr/bin/env python3

from swap.providers.vapor.wallet import (
    Wallet, DEFAULT_PATH
)
from swap.providers.vapor.transaction import WithdrawTransaction
from swap.providers.vapor.assets import BTM as ASSET
from swap.providers.vapor.solver import WithdrawSolver
from swap.providers.vapor.signature import WithdrawSignature
from swap.providers.vapor.utils import submit_transaction_raw

import json

# Choose network mainnet, solonet or testnet
NETWORK: str = "mainnet"
# Vapor funded transaction hash/id
TRANSACTION_HASH: str = "37b36d7be5dfda0cc5dc3c918705464ff901dc5eadb6f4f049db03a679e02bfe"
# Vapor recipient wallet mnemonic
RECIPIENT_MNEMONIC: str = "hint excuse upgrade sleep easily deputy erase cluster section other ugly limit"
# The preimage of HTLC contract
SECRET_KEY: str = "Hello Meheret!"
# Witness Hash Time Lock Contract (HTLC) bytecode
BYTECODE: str = "042ccf300720fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212203e0" \
                "a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a8053" \
                "3a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7" \
                "cac631f000000537acd9f6972ae7cac00c0"

print("=" * 10, "Recipient Vapor Account")

# Initialize Vapor recipient wallet
recipient_wallet: Wallet = Wallet(network=NETWORK)
# Get Vapor recipient wallet from mnemonic
recipient_wallet.from_mnemonic(mnemonic=RECIPIENT_MNEMONIC)
# Drive Vapor recipient wallet from path
recipient_wallet.from_path(path=DEFAULT_PATH)

# Print some Vapor recipient wallet info's
print("XPrivate Key:", recipient_wallet.xprivate_key())
print("XPublic Key:", recipient_wallet.xpublic_key())
print("Private Key:", recipient_wallet.private_key())
print("Public Key:", recipient_wallet.public_key())
print("Path:", recipient_wallet.path())
print("Address:", recipient_wallet.address())
print("Balance:", recipient_wallet.balance(asset=ASSET, unit="BTM"), "BTM")

print("=" * 10, "Unsigned Withdraw Transaction")

# Initialize withdraw transaction
unsigned_withdraw_transaction: WithdrawTransaction = WithdrawTransaction(network=NETWORK)
# Build withdraw transaction
unsigned_withdraw_transaction.build_transaction(
    address=recipient_wallet.address(),
    transaction_hash=TRANSACTION_HASH,
    asset=ASSET
)

print("Unsigned Withdraw Transaction Fee:", unsigned_withdraw_transaction.fee(unit="NEU"), "NEU")
print("Unsigned Withdraw Transaction Hash:", unsigned_withdraw_transaction.hash())
print("Unsigned Withdraw Transaction Main Raw:", unsigned_withdraw_transaction.raw())
# print("Unsigned Withdraw Transaction Json:", json.dumps(unsigned_withdraw_transaction.json(), indent=4))
print("Unsigned Withdraw Transaction Unsigned Datas:", json.dumps(unsigned_withdraw_transaction.unsigned_datas(), indent=4))
print("Unsigned Withdraw Transaction Signatures:", json.dumps(unsigned_withdraw_transaction.signatures(), indent=4))
print("Unsigned Withdraw Transaction Type:", unsigned_withdraw_transaction.type())

unsigned_withdraw_transaction_raw: str = unsigned_withdraw_transaction.transaction_raw()
print("Unsigned Withdraw Transaction Raw:", unsigned_withdraw_transaction_raw)

print("=" * 10, "Signed Withdraw Transaction")

# Initialize withdraw solver
withdraw_solver: WithdrawSolver = WithdrawSolver(
    xprivate_key=recipient_wallet.xprivate_key(),
    path=recipient_wallet.path(),
    secret_key=SECRET_KEY,
    bytecode=BYTECODE
)

# Sign unsigned withdraw transaction
signed_withdraw_transaction: WithdrawTransaction = unsigned_withdraw_transaction.sign(withdraw_solver)

print("Signed Withdraw Transaction Fee:", signed_withdraw_transaction.fee(unit="NEU"), "NEU")
print("Signed Withdraw Transaction Hash:", signed_withdraw_transaction.hash())
print("Signed Withdraw Transaction Main Raw:", signed_withdraw_transaction.raw())
# print("Signed Withdraw Transaction Json:", json.dumps(signed_withdraw_transaction.json(), indent=4))
print("Signed Withdraw Transaction Unsigned Datas:", json.dumps(signed_withdraw_transaction.unsigned_datas(), indent=4))
print("Signed Withdraw Transaction Signatures:", json.dumps(signed_withdraw_transaction.signatures(), indent=4))
print("Signed Withdraw Transaction Type:", signed_withdraw_transaction.type())

signed_withdraw_transaction_raw: str = signed_withdraw_transaction.transaction_raw()
print("Signed Withdraw Transaction Raw:", signed_withdraw_transaction_raw)

print("=" * 10, "Withdraw Signature")

# Initialize withdraw signature
withdraw_signature: WithdrawSignature = WithdrawSignature(network=NETWORK)
# Sign unsigned withdraw transaction raw
withdraw_signature.sign(
    transaction_raw=unsigned_withdraw_transaction_raw,
    solver=withdraw_solver
)

print("Withdraw Signature Fee:", withdraw_signature.fee(unit="NEU"), "NEU")
print("Withdraw Signature Hash:", withdraw_signature.hash())
print("Withdraw Signature Main Raw:", withdraw_signature.raw())
# print("Withdraw Signature Json:", json.dumps(withdraw_signature.json(), indent=4))
print("Withdraw Signature Unsigned Datas:", json.dumps(withdraw_signature.unsigned_datas(), indent=4))
print("Withdraw Signature Signatures:", json.dumps(withdraw_signature.signatures(), indent=4))
print("Withdraw Signature Type:", withdraw_signature.type())

signed_withdraw_signature_transaction_raw: str = withdraw_signature.transaction_raw()
print("Withdraw Signature Transaction Raw:", signed_withdraw_signature_transaction_raw)

# Check both signed withdraw transaction raws are equal
assert signed_withdraw_transaction_raw == signed_withdraw_signature_transaction_raw

# Submit withdraw transaction raw
# print("\nSubmitted Withdraw Transaction:", json.dumps(submit_transaction_raw(
#     transaction_raw=signed_withdraw_transaction_raw  # Or signed_withdraw_signature_transaction_raw
# ), indent=4))
