#!/usr/bin/env python3

from web3.contract import Contract
from web3 import Web3

from swap.providers.ethereum.wallet import Wallet
from swap.providers.ethereum.utils import (
    to_checksum_address, get_erc20_data
)
from swap.providers.ethereum.rpc import (
    get_web3, get_erc20_decimals, submit_raw, wait_for_transaction_receipt
)

# Choose network mainnet, ropsten, kovan, rinkeby or testnet
NETWORK: str = "ropsten"
# Ethereum HTLC ERC20 Contract address
CONTRACT_ADDRESS: str = "0x761c47A8dc8178d55aE14b661abf26cc0B599bc6"
# Ethereum private key
PRIVATE_KEY: str = "cf4c2fb2b88a556c211d5fe79335dcee6dd11403bbbc5b47a530e9cf56ee3aee"
# Ethereum ERC20 token address
TOKEN_ADDRESS: str = "0xa6f89f08cC9d112870E2561F1A8D750681DB59f1"
# Ethereum ERC20 token approve amount
AMOUNT: int = 39 * (10 ** get_erc20_decimals(token_address=TOKEN_ADDRESS, network=NETWORK))

print("=" * 10, "Sender Ethereum Account")

# Initialize Ethereum wallet
wallet: Wallet = Wallet(network=NETWORK)
# Get Ethereum wallet from private key
wallet.from_private_key(private_key=PRIVATE_KEY)

print("Private Key:", wallet.private_key())
print("Public Key:", wallet.public_key())
print("Address:", wallet.address())
print("Balance:", wallet.balance(unit="Ether"), "Ether")
print("ERC20 Balance:", wallet.erc20_balance(token_address=TOKEN_ADDRESS))

# Initialize Ethereum Web3
web3: Web3 = get_web3(network=NETWORK)
# Initialize Ethereum ERC20 token contract
erc20_token: Contract = web3.eth.contract(
    address=to_checksum_address(address=TOKEN_ADDRESS), abi=get_erc20_data("abi")
)

print("=" * 10, "Approve HTLC ERC20 address and Set amount")

# Call approve function and set HTLC ERC20 token address with amount
erc20_approve_function = erc20_token.functions.approve(
    to_checksum_address(address=CONTRACT_ADDRESS), AMOUNT
)

# Get estimate gas or fee
fee: dict = erc20_approve_function.estimateGas({
    "from": to_checksum_address(address=wallet.address()),
    "nonce": web3.eth.get_transaction_count(
        to_checksum_address(address=wallet.address())
    ),
    "gasPrice": web3.eth.gasPrice
})

# Build unsigned transaction for approve function
unsigned_transaction = erc20_approve_function.buildTransaction({
    "from": to_checksum_address(address=wallet.address()),
    "nonce": web3.eth.get_transaction_count(
        to_checksum_address(address=wallet.address())
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

print("=" * 10, "Check ERC20 token Allowance amount for HTLC ERC20 Contract Address")

erc20_allowance_function: int = erc20_token.functions.allowance(
    to_checksum_address(address=wallet.address()),
    to_checksum_address(address=CONTRACT_ADDRESS)
).call()

assert erc20_allowance_function == AMOUNT

print("Allowance Amount:", erc20_allowance_function)
