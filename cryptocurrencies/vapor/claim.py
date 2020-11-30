#!/usr/bin/env python3

from swap.providers.vapor.wallet import Wallet, DEFAULT_PATH
from swap.providers.vapor.transaction import ClaimTransaction
from swap.providers.vapor.assets import BTM as ASSET
from swap.providers.vapor.solver import ClaimSolver
from swap.providers.vapor.signature import ClaimSignature
from swap.providers.vapor.utils import (
    submit_transaction_raw, amount_converter
)

import json

# Choose network mainnet, solonet or testnet
NETWORK: str = "mainnet"
# Vapor funded transaction id/hash
TRANSACTION_ID: str = "969d871257b53c067f473b3894c68bf7be11673e4f3905d432954d97dbf34751"
# Vapor recipient wallet mnemonic
RECIPIENT_MNEMONIC: str = "hint excuse upgrade sleep easily deputy erase cluster section other ugly limit"
# Witness Hash Time Lock Contract (HTLC) bytecode
BYTECODE: str = "02e8032091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2203e" \
                "0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead1" \
                "5a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa8" \
                "88537a7cae7cac631f000000537acd9f6972ae7cac00c0"
# Secret key of HTLC
SECRET_KEY: str = "Hello Meheret!"
# Vapor fund amount
AMOUNT: int = amount_converter(0.0001, "BTM2NEU")

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
print("Program:", recipient_wallet.program())
print("Path:", recipient_wallet.path())
print("Address:", recipient_wallet.address())
print("Balance:", recipient_wallet.balance())

print("=" * 10, "Unsigned Claim Transaction")

# Initialize claim transaction
unsigned_claim_transaction: ClaimTransaction = ClaimTransaction(network=NETWORK)
# Build claim transaction
unsigned_claim_transaction.build_transaction(
    address=recipient_wallet.address(),
    transaction_id=TRANSACTION_ID,
    amount=AMOUNT,
    asset=ASSET
)

print("Unsigned Claim Transaction Fee:", unsigned_claim_transaction.fee())
print("Unsigned Claim Transaction Hash:", unsigned_claim_transaction.hash())
print("Unsigned Claim Transaction Main Raw:", unsigned_claim_transaction.raw())
# print("Unsigned Claim Transaction Json:", json.dumps(unsigned_claim_transaction.json(), indent=4))
print("Unsigned Claim Transaction Unsigned Datas:", json.dumps(unsigned_claim_transaction.unsigned_datas(), indent=4))
print("Unsigned Claim Transaction Signatures:", json.dumps(unsigned_claim_transaction.signatures(), indent=4))
print("Unsigned Claim Transaction Type:", unsigned_claim_transaction.type())

unsigned_claim_transaction_raw: str = unsigned_claim_transaction.transaction_raw()
print("Unsigned Claim Transaction Raw:", unsigned_claim_transaction_raw)

print("=" * 10, "Signed Claim Transaction")

# Initialize claim solver
claim_solver: ClaimSolver = ClaimSolver(
    xprivate_key=recipient_wallet.xprivate_key(),
    secret_key=SECRET_KEY,
    bytecode=BYTECODE
)

# Sign unsigned claim transaction
signed_claim_transaction: ClaimTransaction = unsigned_claim_transaction.sign(claim_solver)

print("Signed Claim Transaction Fee:", signed_claim_transaction.fee())
print("Signed Claim Transaction Hash:", signed_claim_transaction.hash())
print("Signed Claim Transaction Main Raw:", signed_claim_transaction.raw())
# print("Signed Claim Transaction Json:", json.dumps(signed_claim_transaction.json(), indent=4))
print("Signed Claim Transaction Unsigned Datas:", json.dumps(signed_claim_transaction.unsigned_datas(), indent=4))
print("Signed Claim Transaction Signatures:", json.dumps(signed_claim_transaction.signatures(), indent=4))
print("Signed Claim Transaction Type:", signed_claim_transaction.type())

signed_claim_transaction_raw: str = signed_claim_transaction.transaction_raw()
print("Signed Claim Transaction Raw:", signed_claim_transaction_raw)

print("=" * 10, "Claim Signature")

# Initialize claim signature
claim_signature: ClaimSignature = ClaimSignature(network=NETWORK)
# Sign unsigned claim transaction raw
claim_signature.sign(
    transaction_raw=unsigned_claim_transaction_raw,
    solver=claim_solver
)

print("Claim Signature Fee:", claim_signature.fee())
print("Claim Signature Hash:", claim_signature.hash())
print("Claim Signature Main Raw:", claim_signature.raw())
# print("Claim Signature Json:", json.dumps(claim_signature.json(), indent=4))
print("Claim Signature Unsigned Datas:", json.dumps(claim_signature.unsigned_datas(), indent=4))
print("Claim Signature Signatures:", json.dumps(claim_signature.signatures(), indent=4))
print("Claim Signature Type:", claim_signature.type())

signed_claim_signature_transaction_raw: str = claim_signature.transaction_raw()
print("Claim Signature Transaction Raw:", signed_claim_signature_transaction_raw)

# Check both signed claim transaction raws are equal
assert signed_claim_transaction_raw == signed_claim_signature_transaction_raw

# Submit claim transaction raw
# print("\nSubmitted Claim Transaction:", json.dumps(submit_transaction_raw(
#     transaction_raw=signed_claim_transaction_raw  # Or signed_claim_signature_transaction_raw
# ), indent=4))
