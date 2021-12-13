#!/usr/bin/env python3

from swap.providers.ethereum.wallet import (
    Wallet, DEFAULT_PATH
)
from swap.providers.ethereum.htlc import HTLC
from swap.providers.ethereum.transaction import FundTransaction
from swap.providers.ethereum.signature import FundSignature
from swap.providers.ethereum.solver import FundSolver
from swap.providers.ethereum.rpc import get_erc20_decimals
from swap.providers.ethereum.utils import submit_transaction_raw
from swap.utils import (
    sha256, get_current_timestamp
)

import json

# Choose network mainnet, ropsten, kovan, rinkeby or testnet
NETWORK: str = "ropsten"
# Enable Ethereum HTLC ERC20
ERC20: bool = True
# Ethereum HTLC ERC20 contract address
CONTRACT_ADDRESS: str = "0x761c47A8dc8178d55aE14b661abf26cc0B599bc6"
# Secret key hash
SECRET_HASH: str = sha256("Hello Meheret!")
# Ethereum sender wallet mnemonic
SENDER_MNEMONIC: str = "unfair divorce remind addict add roof park clown build renew illness fault"
# Ethereum recipient address
RECIPIENT_ADDRESS: str = "0x1954C47a5D75bdDA53578CEe5D549bf84b8c6B94"
# Expiration block timestamp
ENDTIME: int = get_current_timestamp(plus=3600)  # 1 hour
# Ethereum ERC20 token address
TOKEN_ADDRESS: str = "0xa6f89f08cC9d112870E2561F1A8D750681DB59f1"
# Ethereum ERC20 token fund amount
AMOUNT: int = 25 * (10 ** get_erc20_decimals(token_address=TOKEN_ADDRESS, network=NETWORK))

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

print("=" * 10, "Build Hash Time Lock Contract (HTLC) ERC20 between Sender and Recipient")

# Initialize Ethereum HTLC ERC20 contract
htlc_erc20: HTLC = HTLC(
    contract_address=CONTRACT_ADDRESS, network=NETWORK, erc20=ERC20
)
# Build HTLC ERC20 contract
htlc_erc20.build_htlc(
    secret_hash=SECRET_HASH,
    recipient_address=RECIPIENT_ADDRESS,
    sender_address=sender_wallet.address(),
    endtime=ENDTIME,
    token_address=TOKEN_ADDRESS
)

# Print all Ethereum HTLC ERC20 info's
print("HTLC ERC20 Agreements:", json.dumps(htlc_erc20.agreements, indent=4))
print("HTLC ERC20 ABI:", htlc_erc20.abi())
print("HTLC ERC20 Bytecode:", htlc_erc20.bytecode())
print("HTLC ERC20 Bytecode Runtime:", htlc_erc20.bytecode_runtime())
print("HTLC ERC20 OP_Code:", htlc_erc20.opcode())
print("HTLC ERC20 Contract Address:", htlc_erc20.contract_address())
print("HTLC ERC20 Balance:", htlc_erc20.balance(unit="Ether"), "Ether")
print("HTLC ERC20 Balance:", htlc_erc20.erc20_balance(token_address=TOKEN_ADDRESS))

print("=" * 10, "Unsigned ERC20 Fund Transaction")

# Initialize ERC20 fund transaction
unsigned_fund_transaction: FundTransaction = FundTransaction(network=NETWORK, erc20=ERC20)
# Build ERC20 fund transaction
unsigned_fund_transaction.build_transaction(
    address=sender_wallet.address(), htlc=htlc_erc20, amount=AMOUNT
)

print("Unsigned ERC20 Fund Transaction Fee:", unsigned_fund_transaction.fee())
print("Unsigned ERC20 Fund Transaction Hash:", unsigned_fund_transaction.hash())
print("Unsigned ERC20 Fund Transaction Raw:", unsigned_fund_transaction.raw())
# print("Unsigned ERC20 Fund Transaction Json:", json.dumps(unsigned_fund_transaction.json(), indent=4))
print("Unsigned ERC20 Fund Transaction Signature:", json.dumps(unsigned_fund_transaction.signature(), indent=4))
print("Unsigned ERC20 Fund Transaction Type:", unsigned_fund_transaction.type())

unsigned_fund_transaction_raw: str = unsigned_fund_transaction.transaction_raw()
print("Unsigned ERC20 Fund Transaction Raw:", unsigned_fund_transaction_raw)

print("=" * 10, "Signed ERC20 Fund Transaction")

# Initialize fund solver
fund_solver: FundSolver = FundSolver(
    xprivate_key=sender_wallet.root_xprivate_key(), 
    path=sender_wallet.path()
)

# Sing unsigned ERC20 fund transaction
signed_fund_transaction: FundTransaction = unsigned_fund_transaction.sign(solver=fund_solver)

print("Signed ERC20 Fund Transaction Fee:", signed_fund_transaction.fee())
print("Signed ERC20 Fund Transaction Hash:", signed_fund_transaction.hash())
print("Signed ERC20 Fund Transaction Main Raw:", signed_fund_transaction.raw())
# print("Signed ERC20 Fund Transaction Json:", json.dumps(signed_fund_transaction.json(), indent=4))
print("Signed ERC20 Fund Transaction Signature:", json.dumps(signed_fund_transaction.signature(), indent=4))
print("Signed ERC20 Fund Transaction Type:", signed_fund_transaction.type())

signed_fund_transaction_raw: str = signed_fund_transaction.transaction_raw()
print("Signed ERC20 Fund Transaction Raw:", signed_fund_transaction_raw)

print("=" * 10, "ERC20 Fund Signature")

# Initialize ERC20 fund signature
fund_signature: FundSignature = FundSignature(network=NETWORK, erc20=ERC20)
# Sign unsigned ERC20 fund transaction raw
fund_signature.sign(
    transaction_raw=unsigned_fund_transaction_raw,
    solver=fund_solver
)

print("ERC20 Fund Signature Fee:", fund_signature.fee())
print("ERC20 Fund Signature Hash:", fund_signature.hash())
print("ERC20 Fund Signature Raw:", fund_signature.raw())
# print("ERC20 Fund Signature Json:", json.dumps(fund_signature.json(), indent=4))
print("ERC20 Fund Signature Signature:", json.dumps(fund_signature.signature(), indent=4))
print("ERC20 Fund Signature Type:", fund_signature.type())

signed_fund_signature_transaction_raw: str = fund_signature.transaction_raw()
print("ERC20 Fund Signature Transaction Raw:", signed_fund_signature_transaction_raw)

# Check both signed ERC20 fund transaction raws are equal
assert signed_fund_transaction_raw == signed_fund_signature_transaction_raw

# Submit ERC20 fund transaction raw
# print("\nSubmitted ERC20 Fund Transaction:", json.dumps(submit_transaction_raw(
#     transaction_raw=signed_fund_transaction_raw  # Or signed_fund_signature_transaction_raw
# ), indent=4))
