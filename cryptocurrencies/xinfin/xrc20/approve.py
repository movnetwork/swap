#!/usr/bin/env python3

from web3.contract import Contract
from web3 import Web3

from swap.providers.xinfin.wallet import Wallet
from swap.providers.xinfin.utils import (
    to_checksum_address, get_xrc20_data
)
from swap.providers.xinfin.rpc import (
    get_web3, get_xrc20_decimals, submit_raw, wait_for_transaction_receipt
)

# Choose network mainnet, apothem or testnet
NETWORK: str = "apothem"
# XinFin HTLC XRC20 Contract address
CONTRACT_ADDRESS: str = "xdc4C909fdd6c30f5B4c4d48938C161637B2767d714"
# XinFin private key
PRIVATE_KEY: str = "8a4bc8131e99a5d1064cdbca6949aa2ec16152967b19f2cee3096daefd5ca857"
# XinFin XRC20 token address
TOKEN_ADDRESS: str = "xdcd66dA17A97a91445A2B89805e9fa4B0ff649BF49"
# XinFin XRC20 token approve amount
AMOUNT: int = 25 * (10 ** get_xrc20_decimals(token_address=TOKEN_ADDRESS, network=NETWORK))

print("=" * 10, "Sender XinFin Account")

# Initialize XinFin wallet
wallet: Wallet = Wallet(network=NETWORK)
# Get XinFin wallet from private key
wallet.from_private_key(private_key=PRIVATE_KEY)

print("Private Key:", wallet.private_key())
print("Public Key:", wallet.public_key())
print("Address:", wallet.address())
print("Balance:", wallet.balance(unit="XDC"), "XDC")
print("XRC20 Balance:", wallet.xrc20_balance(token_address=TOKEN_ADDRESS))

# Initialize XinFin Web3
web3: Web3 = get_web3(network=NETWORK)
# Initialize XinFin XRC20 token contract
xrc20_token: Contract = web3.eth.contract(
    address=to_checksum_address(address=TOKEN_ADDRESS, prefix="0x"), abi=get_xrc20_data("abi")
)

print("=" * 10, "Approve HTLC XRC20 address and Set amount")

# Call approve function and set HTLC XRC20 token address with amount
xrc20_approve_function = xrc20_token.functions.approve(
    to_checksum_address(address=CONTRACT_ADDRESS, prefix="0x"), AMOUNT
)

# Get estimate gas or fee
fee: dict = xrc20_approve_function.estimateGas({
    "from": to_checksum_address(address=wallet.address(), prefix="0x"),
    "nonce": web3.eth.get_transaction_count(
        to_checksum_address(address=wallet.address(), prefix="0x")
    ),
    "gasPrice": web3.eth.gasPrice
})

# Build unsigned transaction for approve function
unsigned_transaction = xrc20_approve_function.buildTransaction({
    "from": to_checksum_address(address=wallet.address(), prefix="0x"),
    "nonce": web3.eth.get_transaction_count(
        to_checksum_address(address=wallet.address(), prefix="0x")
    ),
    "gas": fee,
    "gasPrice": web3.eth.gas_price
})
# Sing unsigned transaction of approve function
signed_transaction = web3.eth.account.sign_transaction(
    transaction_dict=unsigned_transaction,
    private_key=wallet.private_key()
)

print("Approve Transaction Fee:", fee)
print("Approve Transaction Hash:", signed_transaction["hash"].hex())
print("Approve Transaction Json:", signed_transaction)
print("Approve Transaction Raw:", signed_transaction["rawTransaction"].hex())

print("=" * 10, "Submit and Wait to be mined for 5 minutes ...")

# Submit Approve transaction raw
submit_raw(transaction_raw=signed_transaction["rawTransaction"].hex(), network=NETWORK)

# Wait 300 seconds for HTLC transaction to be mined
transaction_receipt = wait_for_transaction_receipt(
    transaction_hash=signed_transaction["hash"].hex(), network=NETWORK, timeout=300  # 5 minutes
)

print("Transaction Receipt:", transaction_receipt)

print("=" * 10, "Check XRC20 token Allowance amount for HTLC XRC20 Contract Address")

xrc20_allowance_function: int = xrc20_token.functions.allowance(
    to_checksum_address(address=wallet.address(), prefix="0x"),
    to_checksum_address(address=CONTRACT_ADDRESS, prefix="0x")
).call()

assert xrc20_allowance_function == AMOUNT

print("Allowance Amount:", xrc20_allowance_function)
