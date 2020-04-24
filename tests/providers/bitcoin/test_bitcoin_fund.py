#!/usr/bin/env python3

from shuttle.providers.bitcoin.wallet import Wallet
from shuttle.providers.bitcoin.htlc import HTLC
from shuttle.providers.bitcoin.transaction import FundTransaction
from shuttle.providers.bitcoin.solver import FundSolver
from shuttle.providers.bitcoin.signature import FundSignature, Signature
from shuttle.utils import sha256

import pytest


network = "testnet"
sender_passphrase = "meheret tesfaye batu bayou".encode()

# Initialize sender bitcoin wallet
sender_wallet = Wallet(network=network)
sender_wallet.from_passphrase(sender_passphrase, False)
sender_private_key = sender_wallet.private_key()
sender_public_key = sender_wallet.public_key()
sender_address = sender_wallet.address()

# Initialize recipient bitcoin wallet
recipient_wallet = Wallet(network=network)
recipient_wallet.from_address("muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB")
recipient_address = recipient_wallet.address()

# Initialize Hash Time Lock Contract (HTLC)
htlc = HTLC(network=network).init(
    secret_hash=sha256("Hello Meheret!".encode()).hex(),
    recipient_address=recipient_address,
    sequence=100,
    sender_address=sender_address
)


# Testing bitcoin fund
def test_bitcoin_fund():
    # Initialization fund transaction
    unsigned_fund_transaction = FundTransaction(version=2, network=network)
    # Building fund transaction
    unsigned_fund_transaction.build_transaction(
        wallet=sender_wallet,
        htlc=htlc,
        amount=10000
    )

    assert unsigned_fund_transaction.fee == 678
    assert unsigned_fund_transaction.hash() == "8e153f98a1e1ae918d59ac94e1ef08d139b7a3b492c3354ecf47e9d3705c2acf"
    assert unsigned_fund_transaction.raw() == \
           "020000000180dea6505f075127bd47d6527a0eb817b1f6e39e592b0d53e14bbd600a0fb18f0000000000ffffffff02102700" \
           "000000000017a9148726547c18c325ac7fab7a7c8209bbdbb7cf1d87875a970000000000001976a9146bce65e58a50b97989" \
           "930e9a4ff1ac1a77515ef188ac00000000"
    assert unsigned_fund_transaction.unsigned_raw() == \
           "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTgwZGVhNjUwNWYwNzUxMjdiZDQ3ZDY1MjdhMGViODE3YjFmNmUzOWU1OTJi" \
           "MGQ1M2UxNGJiZDYwMGEwZmIxOGYwMDAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQ4NzI2NTQ3YzE4YzMy" \
           "NWFjN2ZhYjdhN2M4MjA5YmJkYmI3Y2YxZDg3ODc1YTk3MDAwMDAwMDAwMDAwMTk3NmE5MTQ2YmNlNjVlNThhNTBiOTc5ODk5MzBl" \
           "OWE0ZmYxYWMxYTc3NTE1ZWYxODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiA0OTQyNCwgIm4iOiAwLCAic2Ny" \
           "aXB0IjogIjc2YTkxNDZiY2U2NWU1OGE1MGI5Nzk4OTkzMGU5YTRmZjFhYzFhNzc1MTVlZjE4OGFjIn1dLCAibmV0d29yayI6ICJ0" \
           "ZXN0bmV0IiwgInR5cGUiOiAiYml0Y29pbl9mdW5kX3Vuc2lnbmVkIn0="
    assert unsigned_fund_transaction.json()

    fund_solver = FundSolver(private_key=sender_private_key)
    assert unsigned_fund_transaction.sign(fund_solver)

    fund_signature = FundSignature(network=network)\
        .sign(unsigned_raw=unsigned_fund_transaction.unsigned_raw(), solver=fund_solver)

    assert fund_signature.fee == 678
    assert fund_signature.hash() == "5f9eed11af4e5d495733da6d258d9ef3f82bc1fd9f9b9fb54184c4dd03ecdba6"
    assert fund_signature.raw() == \
           "020000000180dea6505f075127bd47d6527a0eb817b1f6e39e592b0d53e14bbd600a0fb18f000000006a4730440220523ea5" \
           "0108a454cc90eee9189a6f745d0dd8f50e83840d489f6108fd704e0abd0220368d2ffd66d7e1b9258773220a0ec1056a2b94" \
           "ec9bccc88ec27365b60543010c012103c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84ffff" \
           "ffff02102700000000000017a9148726547c18c325ac7fab7a7c8209bbdbb7cf1d87875a970000000000001976a9146bce65" \
           "e58a50b97989930e9a4ff1ac1a77515ef188ac00000000"
    assert fund_signature.signed_raw() == \
           "eyJyYXciOiAiMDIwMDAwMDAwMTgwZGVhNjUwNWYwNzUxMjdiZDQ3ZDY1MjdhMGViODE3YjFmNmUzOWU1OTJiMGQ1M2UxNGJiZDYw" \
           "MGEwZmIxOGYwMDAwMDAwMDZhNDczMDQ0MDIyMDUyM2VhNTAxMDhhNDU0Y2M5MGVlZTkxODlhNmY3NDVkMGRkOGY1MGU4Mzg0MGQ0" \
           "ODlmNjEwOGZkNzA0ZTBhYmQwMjIwMzY4ZDJmZmQ2NmQ3ZTFiOTI1ODc3MzIyMGEwZWMxMDU2YTJiOTRlYzliY2NjODhlYzI3MzY1" \
           "YjYwNTQzMDEwYzAxMjEwM2M1NmE2MDA1ZDRhODg5MmQyOGNjM2Y3MjY1ZTU2ODViNTQ4NjI3ZDU5MTA4OTczZTQ3NGM0ZTI2ZjY5" \
           "YTRjODRmZmZmZmZmZjAyMTAyNzAwMDAwMDAwMDAwMDE3YTkxNDg3MjY1NDdjMThjMzI1YWM3ZmFiN2E3YzgyMDliYmRiYjdjZjFk" \
           "ODc4NzVhOTcwMDAwMDAwMDAwMDAxOTc2YTkxNDZiY2U2NWU1OGE1MGI5Nzk4OTkzMGU5YTRmZjFhYzFhNzc1MTVlZjE4OGFjMDAw" \
           "MDAwMDAiLCAiZmVlIjogNjc4LCAibmV0d29yayI6ICJ0ZXN0bmV0IiwgInR5cGUiOiAiYml0Y29pbl9mdW5kX3NpZ25lZCJ9"
    assert fund_signature.json()

    signature = Signature(network=network) \
        .sign(unsigned_raw=unsigned_fund_transaction.unsigned_raw(), solver=fund_solver)

    assert signature.fee == 678
    assert signature.hash() == "5f9eed11af4e5d495733da6d258d9ef3f82bc1fd9f9b9fb54184c4dd03ecdba6"
    assert signature.raw() == \
           "020000000180dea6505f075127bd47d6527a0eb817b1f6e39e592b0d53e14bbd600a0fb18f000000006a4730440220523ea5" \
           "0108a454cc90eee9189a6f745d0dd8f50e83840d489f6108fd704e0abd0220368d2ffd66d7e1b9258773220a0ec1056a2b94" \
           "ec9bccc88ec27365b60543010c012103c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84ffff" \
           "ffff02102700000000000017a9148726547c18c325ac7fab7a7c8209bbdbb7cf1d87875a970000000000001976a9146bce65" \
           "e58a50b97989930e9a4ff1ac1a77515ef188ac00000000"
    assert signature.signed_raw() == \
           "eyJyYXciOiAiMDIwMDAwMDAwMTgwZGVhNjUwNWYwNzUxMjdiZDQ3ZDY1MjdhMGViODE3YjFmNmUzOWU1OTJiMGQ1M2UxNGJiZDYw" \
           "MGEwZmIxOGYwMDAwMDAwMDZhNDczMDQ0MDIyMDUyM2VhNTAxMDhhNDU0Y2M5MGVlZTkxODlhNmY3NDVkMGRkOGY1MGU4Mzg0MGQ0" \
           "ODlmNjEwOGZkNzA0ZTBhYmQwMjIwMzY4ZDJmZmQ2NmQ3ZTFiOTI1ODc3MzIyMGEwZWMxMDU2YTJiOTRlYzliY2NjODhlYzI3MzY1" \
           "YjYwNTQzMDEwYzAxMjEwM2M1NmE2MDA1ZDRhODg5MmQyOGNjM2Y3MjY1ZTU2ODViNTQ4NjI3ZDU5MTA4OTczZTQ3NGM0ZTI2ZjY5" \
           "YTRjODRmZmZmZmZmZjAyMTAyNzAwMDAwMDAwMDAwMDE3YTkxNDg3MjY1NDdjMThjMzI1YWM3ZmFiN2E3YzgyMDliYmRiYjdjZjFk" \
           "ODc4NzVhOTcwMDAwMDAwMDAwMDAxOTc2YTkxNDZiY2U2NWU1OGE1MGI5Nzk4OTkzMGU5YTRmZjFhYzFhNzc1MTVlZjE4OGFjMDAw" \
           "MDAwMDAiLCAiZmVlIjogNjc4LCAibmV0d29yayI6ICJ0ZXN0bmV0IiwgInR5cGUiOiAiYml0Y29pbl9mdW5kX3NpZ25lZCJ9"
    assert signature.json()

    with pytest.raises(ValueError, match="transaction script is none, sign first"):
        Signature().hash()
    with pytest.raises(ValueError, match="transaction script is none, sign first"):
        Signature().json()
    with pytest.raises(ValueError, match="transaction script is none, build transaction first"):
        Signature().raw()
    # with pytest.raises(ValueError, match="not found type, sign first"):
    #     Signature().type()
    with pytest.raises(ValueError, match="there is no signed data, sign first"):
        Signature().signed_raw()
    with pytest.raises(ValueError, match="invalid unsigned transaction raw"):
        Signature().sign("eyJtIjogImFzZCJ9", "")
