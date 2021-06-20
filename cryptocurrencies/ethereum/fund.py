#!/usr/bin/env python3

from swap.providers.ethereum.wallet import Wallet, DEFAULT_BIP44_PATH
from swap.providers.ethereum.htlc import HTLC
from swap.providers.ethereum.transaction import FundTransaction
from swap.providers.ethereum.signature import FundSignature
from swap.providers.ethereum.solver import FundSolver
from swap.providers.ethereum.utils import (
    amount_unit_converter, submit_transaction_raw
)
from swap.utils import (
    sha256, get_current_timestamp
)

import json

# Choose network mainnet or testnet
NETWORK: str = "testnet"
# Ethereum HTLC transaction hash
HTLC_TRANSACTION_HASH: str = "0x728c83cc83bb4b1a67fbfd480a9bdfdd55cb5fc6fd519f6a98fa35db3a2a9160"

# Secret key hash
SECRET_HASH: str = sha256("Hello Meheret!")
# Ethereum recipient address
RECIPIENT_ADDRESS: str = "0xd77E0d2Eef905cfB39c3C4b952Ed278d58f96E1f"
# Ethereum sender mnemonic
SENDER_MNEMONIC: str = "unfair divorce remind addict add roof park clown build renew illness fault"
# Derivation for sender mnemonic
ACCOUNT, CHANGE, ADDRESS = 0, False, 0
# Expiration block time (Seconds)
ENDTIME: int = get_current_timestamp() + 300  # 300 seconds equal with 5 min
# Ethereum fund amount
AMOUNT: int = amount_unit_converter(3, "Ether2Wei")

print("=" * 10, "Sender Ethereum Account")

# Initialize Ethereum sender wallet
wallet: Wallet = Wallet(network=NETWORK)
# Get Ethereum sender wallet from mnemonic
wallet.from_mnemonic(mnemonic=SENDER_MNEMONIC)
# Drive Ethereum sender wallet from path
wallet.from_path(
    path=DEFAULT_BIP44_PATH.format(
        account=ACCOUNT, change=(1 if CHANGE else 0), address=ADDRESS
    )
)

# Print some Ethereum sender wallet info's
print("Root XPrivate Key:", wallet.root_xprivate_key())
print("Root XPublic Key:", wallet.root_xpublic_key())
print("Private Key:", wallet.private_key())
print("Public Key:", wallet.public_key())
print("Path:", wallet.path())
print("Address:", wallet.address())
print("Balance:", wallet.balance(unit="Ether"), "Ether")

print("=" * 10, "Build Hash Time Lock Contract (HTLC) between Sender and Recipient")

# Initialize Ethereum HTLC
htlc: HTLC = HTLC(
    transaction_hash=HTLC_TRANSACTION_HASH, network=NETWORK
)
# Build HTLC contract
htlc.build_htlc(
    secret_hash=SECRET_HASH,
    recipient_address=RECIPIENT_ADDRESS,
    sender_address=wallet.address(),
    endtime=ENDTIME
)

# Print all Ethereum HTLC info's
print("HTLC ABI:", htlc.abi())
print("HTLC Bytecode:", htlc.bytecode())
print("HTLC Bytecode Runtime:", htlc.bytecode_runtime())
print("HTLC OP_Code:", htlc.opcode())
print("HTLC Contract Address:", htlc.contract_address())
print("HTLC Balance:", htlc.balance(unit="Ether"), "Ether")

print("=" * 10, "Unsigned Fund Transaction")

# Initialize fund transaction
unsigned_fund_transaction: FundTransaction = FundTransaction(network=NETWORK)
# Build fund transaction
unsigned_fund_transaction.build_transaction(
    address=wallet.address(), htlc=htlc, amount=AMOUNT
)

print("Unsigned Fund Transaction Fee:", unsigned_fund_transaction.fee())
print("Unsigned Fund Transaction Hash:", unsigned_fund_transaction.hash())
print("Unsigned Fund Transaction Raw:", unsigned_fund_transaction.raw())
print("Unsigned Fund Transaction Json:", unsigned_fund_transaction.json())
print("Unsigned Fund Transaction Signature:", unsigned_fund_transaction.signature())
print("Unsigned Fund Transaction Type:", unsigned_fund_transaction.type())

unsigned_fund_transaction_raw: str = unsigned_fund_transaction.transaction_raw()
print("Unsigned Fund Transaction Raw:", unsigned_fund_transaction_raw)

print("=" * 10, "Signed Fund Transaction")

# Initialize fund solver
fund_solver: FundSolver = FundSolver(
    xprivate_key=wallet.root_xprivate_key(), path=DEFAULT_BIP44_PATH.format(
        account=ACCOUNT, change=(1 if CHANGE else 0), address=ADDRESS
    )
)

# Sing unsigned fund transaction
signed_fund_transaction: FundTransaction = unsigned_fund_transaction.sign(solver=fund_solver)

print("Signed Fund Transaction Fee:", signed_fund_transaction.fee())
print("Signed Fund Transaction Hash:", signed_fund_transaction.hash())
print("Signed Fund Transaction Json:", signed_fund_transaction.json())
print("Signed Fund Transaction Main Raw:", signed_fund_transaction.raw())
print("Signed Fund Transaction Signature:", signed_fund_transaction.signature())
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

print("Fund Signature Fee:", fund_signature.fee())
print("Fund Signature Hash:", fund_signature.hash())
print("Fund Signature Json:", fund_signature.json())
print("Fund Signature Raw:", fund_signature.raw())
print("Fund Signature Transaction Signature:", fund_signature.signature())
print("Fund Signature Type:", fund_signature.type())

signed_fund_signature_transaction_raw: str = fund_signature.transaction_raw()
print("Fund Signature Transaction Raw:", signed_fund_signature_transaction_raw)

# Check both signed fund transaction raws are equal
assert signed_fund_transaction_raw == signed_fund_signature_transaction_raw

# Submit fund transaction raw
# print("\nSubmitted Fund Transaction:", json.dumps(submit_transaction_raw(
#     transaction_raw=signed_fund_transaction_raw  # Or signed_fund_signature_transaction_raw
# ), indent=4))
