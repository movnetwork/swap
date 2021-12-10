#!/usr/bin/env python3

from swap.providers.xinfin.htlc import HTLC
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
# XinFin recipient address
RECIPIENT_ADDRESS: str = "xdcf8D43806260CFc6cC79fB408BA1897054667F81C"
# XinFin sender address
SENDER_ADDRESS: str = "xdc2224caA2235DF8Da3D2016d2AB1137D2d548A232"
# Expiration block timestamp
ENDTIME: int = get_current_timestamp(plus=3600)  # 1 hour
# XinFin XRC20 token address
TOKEN_ADDRESS: str = "xdcd66dA17A97a91445A2B89805e9fa4B0ff649BF49"

print("=" * 10, "Hash Time Lock Contract (HTLC) XRC20 between Sender and Recipient")

# Initialize XinFin HTLC XRC20
htlc_xrc20: HTLC = HTLC(
    contract_address=CONTRACT_ADDRESS, network=NETWORK, xrc20=XRC20
)
# Build HTLC XRC20 contract
htlc_xrc20.build_htlc(
    secret_hash=SECRET_HASH,
    recipient_address=RECIPIENT_ADDRESS,
    sender_address=SENDER_ADDRESS,
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
