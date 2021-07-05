#!/usr/bin/env python3

from swap.providers.xinfin.htlc import HTLC
from swap.utils import (
    sha256, get_current_timestamp
)

import json

# Choose network mainnet or testnet
NETWORK: str = "mainnet"
# XinFin HTLC contract address
CONTRACT_ADDRESS: str = "xdc656869af3Ec1E8b2982Fc370A0526541C0Ceb90B"
# Secret key hash
SECRET_HASH: str = sha256("Hello Meheret!")
# XinFin recipient address
RECIPIENT_ADDRESS: str = "xdcf8D43806260CFc6cC79fB408BA1897054667F81C"
# XinFin sender address
SENDER_ADDRESS: str = "xdc2224caA2235DF8Da3D2016d2AB1137D2d548A232"
# Expiration block timestamp
ENDTIME: int = get_current_timestamp(plus=3600)  # 1 hour

print("=" * 10, "Hash Time Lock Contract (HTLC) between Sender and Recipient")

# Initialize XinFin HTLC
htlc: HTLC = HTLC(
    contract_address=CONTRACT_ADDRESS, network=NETWORK
)
# Build HTLC contract
htlc.build_htlc(
    secret_hash=SECRET_HASH,
    recipient_address=RECIPIENT_ADDRESS,
    sender_address=SENDER_ADDRESS,
    endtime=ENDTIME
)

# Print all XinFin HTLC info's
print("HTLC Agreements:", json.dumps(htlc.agreements, indent=4))
print("HTLC ABI:", htlc.abi())
print("HTLC Bytecode:", htlc.bytecode())
print("HTLC Bytecode Runtime:", htlc.bytecode_runtime())
print("HTLC OP_Code:", htlc.opcode())
print("HTLC Contract Address:", htlc.contract_address())
print("HTLC Balance:", htlc.balance(unit="XDC"), "XDC")
