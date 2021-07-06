#!/usr/bin/env python3

from swap.providers.bytom.htlc import HTLC
from swap.providers.bytom.utils import estimate_endblock
from swap.providers.bytom.assets import BTM as ASSET
from swap.utils import (
    sha256, get_current_timestamp
)

import json

# Choose network mainnet, solonet or testnet
NETWORK: str = "mainnet"
# Secret key hash
SECRET_HASH: str = sha256("Hello Meheret!")
# Bytom recipient public key
RECIPIENT_PUBLIC_KEY: str = "3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e"
# Bytom sender public key
SENDER_PUBLIC_KEY: str = "fe6b3fd4458291b19605d92837ae1060cc0237e68022b2eb9faf01a118226212"
# Expiration block height
ENDBLOCK: int = estimate_endblock(endtime=get_current_timestamp(plus=3600))  # 1 hour

print("=" * 10, "Hash Time Lock Contract (HTLC) between Sender and Recipient")

# Initialize Bytom HTLC
htlc: HTLC = HTLC(network=NETWORK)
# Build HTLC contract
htlc.build_htlc(
    secret_hash=SECRET_HASH,
    recipient_public_key=RECIPIENT_PUBLIC_KEY,
    sender_public_key=SENDER_PUBLIC_KEY,
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
