#!/usr/bin/env python3

from swap.providers.xinfin.wallet import (
    Wallet, DEFAULT_PATH
)
from swap.providers.xinfin.htlc import HTLC
from swap.providers.xinfin.transaction import FundTransaction
from swap.providers.xinfin.signature import FundSignature
from swap.providers.xinfin.solver import FundSolver
from swap.providers.xinfin.rpc import get_xrc20_decimals
from swap.providers.xinfin.utils import submit_transaction_raw
from swap.utils import (
    sha256, get_current_timestamp
)

import json

# Choose network mainnet, apothem or testnet
NETWORK: str = "apothem"
# Enable XinFin HTLC XRC20
XRC20: bool = True
# XinFin HTLC XRC20 contract address
CONTRACT_ADDRESS: str = "xdc4C909fdd6c30f5B4c4d48938C161637B2767d714"
# Secret key hash
SECRET_HASH: str = sha256("Hello Meheret!")
# XinFin sender wallet mnemonic
SENDER_MNEMONIC: str = "unfair divorce remind addict add roof park clown build renew illness fault"
# XinFin recipient address
RECIPIENT_ADDRESS: str = "xdcf8D43806260CFc6cC79fB408BA1897054667F81C"
# Expiration block timestamp
ENDTIME: int = get_current_timestamp(plus=3600)  # 1 hour
# XinFin XRC20 token address
TOKEN_ADDRESS: str = "xdcd66dA17A97a91445A2B89805e9fa4B0ff649BF49"
# XinFin XRC20 token fund amount
AMOUNT: int = 25 * (10 ** get_xrc20_decimals(token_address=TOKEN_ADDRESS, network=NETWORK))

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

print("=" * 10, "Build Hash Time Lock Contract (HTLC) XRC20 between Sender and Recipient")

# Initialize XinFin HTLC XRC20 contract
htlc_xrc20: HTLC = HTLC(
    contract_address=CONTRACT_ADDRESS, network=NETWORK, xrc20=XRC20
)
# Build HTLC XRC20 contract
htlc_xrc20.build_htlc(
    secret_hash=SECRET_HASH,
    recipient_address=RECIPIENT_ADDRESS,
    sender_address=sender_wallet.address(),
    endtime=ENDTIME,
    token_address=TOKEN_ADDRESS
)

# Print all XinFin HTLC XRC20 info's
print("HTLC XRC20 Agreements:", json.dumps(htlc_xrc20.agreements, indent=4))
print("HTLC XRC20 ABI:", htlc_xrc20.abi())
print("HTLC XRC20 Bytecode:", htlc_xrc20.bytecode())
print("HTLC XRC20 Bytecode Runtime:", htlc_xrc20.bytecode_runtime())
print("HTLC XRC20 OP_Code:", htlc_xrc20.opcode())
print("HTLC XRC20 Contract Address:", htlc_xrc20.contract_address())
print("HTLC XRC20 Balance:", htlc_xrc20.balance(unit="XDC"), "XDC")
print("HTLC XRC20 Balance:", htlc_xrc20.xrc20_balance(token_address=TOKEN_ADDRESS))

print("=" * 10, "Unsigned XRC20 Fund Transaction")

# Initialize XRC20 fund transaction
unsigned_fund_transaction: FundTransaction = FundTransaction(network=NETWORK, xrc20=XRC20)
# Build XRC20 fund transaction
unsigned_fund_transaction.build_transaction(
    address=sender_wallet.address(), htlc=htlc_xrc20, amount=AMOUNT
)

print("Unsigned XRC20 Fund Transaction Fee:", unsigned_fund_transaction.fee())
print("Unsigned XRC20 Fund Transaction Hash:", unsigned_fund_transaction.hash())
print("Unsigned XRC20 Fund Transaction Raw:", unsigned_fund_transaction.raw())
# print("Unsigned XRC20 Fund Transaction Json:", json.dumps(unsigned_fund_transaction.json(), indent=4))
print("Unsigned XRC20 Fund Transaction Signature:", json.dumps(unsigned_fund_transaction.signature(), indent=4))
print("Unsigned XRC20 Fund Transaction Type:", unsigned_fund_transaction.type())

unsigned_fund_transaction_raw: str = unsigned_fund_transaction.transaction_raw()
print("Unsigned XRC20 Fund Transaction Raw:", unsigned_fund_transaction_raw)

print("=" * 10, "Signed XRC20 Fund Transaction")

# Initialize fund solver
fund_solver: FundSolver = FundSolver(
    xprivate_key=sender_wallet.root_xprivate_key(), 
    path=sender_wallet.path()
)

# Sing unsigned XRC20 fund transaction
signed_fund_transaction: FundTransaction = unsigned_fund_transaction.sign(solver=fund_solver)

print("Signed XRC20 Fund Transaction Fee:", signed_fund_transaction.fee())
print("Signed XRC20 Fund Transaction Hash:", signed_fund_transaction.hash())
print("Signed XRC20 Fund Transaction Main Raw:", signed_fund_transaction.raw())
# print("Signed XRC20 Fund Transaction Json:", json.dumps(signed_fund_transaction.json(), indent=4))
print("Signed XRC20 Fund Transaction Signature:", json.dumps(signed_fund_transaction.signature(), indent=4))
print("Signed XRC20 Fund Transaction Type:", signed_fund_transaction.type())

signed_fund_transaction_raw: str = signed_fund_transaction.transaction_raw()
print("Signed XRC20 Fund Transaction Raw:", signed_fund_transaction_raw)

print("=" * 10, "XRC20 Fund Signature")

# Initialize XRC20 fund signature
fund_signature: FundSignature = FundSignature(network=NETWORK, xrc20=XRC20)
# Sign unsigned XRC20 fund transaction raw
fund_signature.sign(
    transaction_raw=unsigned_fund_transaction_raw,
    solver=fund_solver
)

print("XRC20 Fund Signature Fee:", fund_signature.fee())
print("XRC20 Fund Signature Hash:", fund_signature.hash())
print("XRC20 Fund Signature Raw:", fund_signature.raw())
# print("XRC20 Fund Signature Json:", json.dumps(fund_signature.json(), indent=4))
print("XRC20 Fund Signature Signature:", json.dumps(fund_signature.signature(), indent=4))
print("XRC20 Fund Signature Type:", fund_signature.type())

signed_fund_signature_transaction_raw: str = fund_signature.transaction_raw()
print("XRC20 Fund Signature Transaction Raw:", signed_fund_signature_transaction_raw)

# Check both signed XRC20 fund transaction raws are equal
assert signed_fund_transaction_raw == signed_fund_signature_transaction_raw

# Submit XRC20 fund transaction raw
# print("\nSubmitted XRC20 Fund Transaction:", json.dumps(submit_transaction_raw(
#     transaction_raw=signed_fund_transaction_raw  # Or signed_fund_signature_transaction_raw
# ), indent=4))
