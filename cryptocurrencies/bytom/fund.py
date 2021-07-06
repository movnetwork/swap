#!/usr/bin/env python3

from swap.providers.bytom.wallet import (
    Wallet, DEFAULT_PATH
)
from swap.providers.bytom.htlc import HTLC
from swap.providers.bytom.transaction import FundTransaction
from swap.providers.bytom.assets import BTM as ASSET
from swap.providers.bytom.solver import FundSolver
from swap.providers.bytom.signature import FundSignature
from swap.providers.bytom.utils import (
    submit_transaction_raw, amount_unit_converter, estimate_endblock
)
from swap.utils import (
    sha256, get_current_timestamp
)

import json

# Choose network mainnet, solonet or testnet
NETWORK: str = "mainnet"
# Secret key hash
SECRET_HASH: str = sha256("Hello Meheret!")
# Bytom sender wallet mnemonic
SENDER_MNEMONIC: str = "unfair divorce remind addict add roof park clown build renew illness fault"
# Bytom recipient public key
RECIPIENT_PUBLIC_KEY: str = "3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e"
# Expiration block height
ENDBLOCK: int = estimate_endblock(endtime=get_current_timestamp(plus=3600))  # 1 hour
# Bytom fund amount
AMOUNT: int = amount_unit_converter(0.1, unit_from="BTM2NEU")

print("=" * 10, "Sender Bytom Account")

# Initialize Bytom sender wallet
sender_wallet: Wallet = Wallet(network=NETWORK)
# Get Bytom sender wallet from mnemonic
sender_wallet.from_mnemonic(mnemonic=SENDER_MNEMONIC)
# Drive Bytom sender wallet from path
sender_wallet.from_path(path=DEFAULT_PATH)

# Print some Bytom sender wallet info's
print("XPrivate Key:", sender_wallet.xprivate_key())
print("XPublic Key:", sender_wallet.xpublic_key())
print("Private Key:", sender_wallet.private_key())
print("Public Key:", sender_wallet.public_key())
print("Path:", sender_wallet.path())
print("Address:", sender_wallet.address())
print("Balance:", sender_wallet.balance(asset=ASSET, unit="BTM"), "BTM")

print("=" * 10, "Hash Time Lock Contract (HTLC) between Sender and Recipient")

# Initialize Bytom HTLC
htlc: HTLC = HTLC(network=NETWORK)
# Build HTLC contract
htlc.build_htlc(
    secret_hash=SECRET_HASH,
    recipient_public_key=RECIPIENT_PUBLIC_KEY,
    sender_public_key=sender_wallet.public_key(),
    endblock=ENDBLOCK
)

# Print all Bytom HTLC info's
print("HTLC Agreements:", json.dumps(htlc.agreements, indent=4))
print("HTLC Bytecode:", htlc.bytecode())
print("HTLC OP_Code:", htlc.opcode())
print("HTLC Hash:", htlc.hash())
print("HTLC Contract Address:", htlc.contract_address())
print("HTLC Balance:", htlc.balance(asset=ASSET, unit="BTM"), "BTM")
print("HTLC UTXO's:", htlc.utxos())

print("=" * 10, "Unsigned Fund Transaction")

# Initialize fund transaction
unsigned_fund_transaction: FundTransaction = FundTransaction(network=NETWORK)
# Build fund transaction
unsigned_fund_transaction.build_transaction(
    address=sender_wallet.address(), htlc=htlc, amount=AMOUNT, asset=ASSET
)

print("Unsigned Fund Transaction Fee:", unsigned_fund_transaction.fee(unit="NEU"), "NEU")
print("Unsigned Fund Transaction Hash:", unsigned_fund_transaction.hash())
print("Unsigned Fund Transaction Main Raw:", unsigned_fund_transaction.raw())
# print("Unsigned Fund Transaction Json:", json.dumps(unsigned_fund_transaction.json(), indent=4))
print("Unsigned Fund Transaction Unsigned Datas:", json.dumps(unsigned_fund_transaction.unsigned_datas(), indent=4))
print("Unsigned Fund Transaction Signatures:", json.dumps(unsigned_fund_transaction.signatures(), indent=4))
print("Unsigned Fund Transaction Type:", unsigned_fund_transaction.type())

unsigned_fund_transaction_raw = unsigned_fund_transaction.transaction_raw()
print("Unsigned Fund Transaction Raw:", unsigned_fund_transaction_raw)

print("=" * 10, "Signed Fund Transaction")

# Initialize fund solver
fund_solver: FundSolver = FundSolver(
    xprivate_key=sender_wallet.xprivate_key(),
    path=sender_wallet.path()
)

# Sing unsigned fund transaction
signed_fund_transaction: FundTransaction = unsigned_fund_transaction.sign(fund_solver)

print("Signed Fund Transaction Fee:", signed_fund_transaction.fee(unit="NEU"), "NEU")
print("Signed Fund Transaction Hash:", signed_fund_transaction.hash())
print("Signed Fund Transaction Main Raw:", signed_fund_transaction.raw())
# print("Signed Fund Transaction Json:", json.dumps(signed_fund_transaction.json(), indent=4))
print("Signed Fund Transaction Unsigned Datas:", json.dumps(signed_fund_transaction.unsigned_datas(), indent=4))
print("Signed Fund Transaction Signatures:", json.dumps(signed_fund_transaction.signatures(), indent=4))
print("Signed Fund Transaction Type:", signed_fund_transaction.type())

signed_fund_transaction_raw: str = signed_fund_transaction.transaction_raw()
print("Signed Fund Transaction Raw:", signed_fund_transaction_raw)

print("=" * 10, "Fund Signature")

# Initialize fund signature
fund_signature: FundSignature = FundSignature(network=NETWORK)
# Sign unsigned fund transaction raw
fund_signature.sign(
    transaction_raw=unsigned_fund_transaction_raw,
    solver=fund_solver
)

print("Fund Signature Fee:", fund_signature.fee(unit="NEU"), "NEU")
print("Fund Signature Hash:", fund_signature.hash())
print("Fund Signature Main Raw:", fund_signature.raw())
# print("Fund Signature Json:", json.dumps(fund_signature.json(), indent=4))
print("Fund Signature Unsigned Datas:", json.dumps(fund_signature.unsigned_datas(), indent=4))
print("Fund Signature Signatures:", json.dumps(fund_signature.signatures(), indent=4))
print("Fund Signature Type:", fund_signature.type())

signed_fund_signature_transaction_raw: str = fund_signature.transaction_raw()
print("Fund Signature Transaction Raw:", signed_fund_signature_transaction_raw)

# Check both signed fund transaction raws are equal
assert signed_fund_transaction_raw == signed_fund_signature_transaction_raw

# Submit fund transaction raw
# print("\nSubmitted Fund Transaction:", json.dumps(submit_transaction_raw(
#     transaction_raw=signed_fund_transaction_raw  # Or signed_fund_signature_transaction_raw
# ), indent=4))
