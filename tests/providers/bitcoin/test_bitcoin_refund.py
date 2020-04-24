#!/usr/bin/env python3

from shuttle.providers.bitcoin.wallet import Wallet
from shuttle.providers.bitcoin.transaction import RefundTransaction
from shuttle.providers.bitcoin.solver import RefundSolver
from shuttle.providers.bitcoin.signature import RefundSignature, Signature

network = "testnet"
sender_passphrase = "meheret".encode()

# Initialize sender bitcoin wallet
sender_wallet = Wallet(network=network)\
    .from_passphrase(sender_passphrase)
sender_private_key = sender_wallet.private_key()
# Initialize recipient bitcoin wallet
recipient_wallet = Wallet(network=network)
recipient_wallet.from_address("muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB")
recipient_address = recipient_wallet.address()
# Funded hash time lock contract transaction id/hash
fund_transaction_id = "91f3a0dc0621f78be74a971dfb35d75255426d273f766456d9975006ece78b88"


# Testing bitcoin refund
def test_bitcoin_refund():
    # Initialization refund transaction
    unsigned_refund_transaction = RefundTransaction(version=2, network=network)
    # Building refund transaction
    unsigned_refund_transaction.build_transaction(
        transaction_id=fund_transaction_id,
        wallet=recipient_wallet,
        amount=2000
    )

    assert unsigned_refund_transaction.fee == 576
    assert unsigned_refund_transaction.hash() == "0a22fd29c2d2a8f0e162028737c8cbc1ea9e266d5f4cf42248aa22c1c96d1e15"
    assert unsigned_refund_transaction.raw() == \
           "0200000001888be7ec065097d95664763f276d425552d735fb1d974ae78bf72106dca0f3910000000000ffffffff0190050000" \
           "000000001976a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac00000000"
    assert unsigned_refund_transaction.json()

    unsigned_refund_raw = unsigned_refund_transaction.unsigned_raw()
    assert unsigned_refund_raw == \
           "eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTg4OGJlN2VjMDY1MDk3ZDk1NjY0NzYzZjI3NmQ0MjU1NTJkNzM1ZmIxZDk3NG" \
           "FlNzhiZjcyMTA2ZGNhMGYzOTEwMDAwMDAwMDAwZmZmZmZmZmYwMTkwMDUwMDAwMDAwMDAwMDAxOTc2YTkxNDY0YTgzOTBiMGIxNjg1" \
           "ZmNiZjJkNGI0NTcxMThkYzhkYTkyZDU1MzQ4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IFt7ImFtb3VudCI6IDIwMDAsICJuIjogMC" \
           "wgInNjcmlwdCI6ICJhOTE0NmYwOGIyNTRlNGM1OGRjNjVmNmYzOTljM2JlNzE3N2I5MDFmNGE2Njg3In1dLCAicmVjaXBpZW50X2Fk" \
           "ZHJlc3MiOiAibXVUbmZmTERSNUx0RmVMUjJpM1dzS1ZmZHl2emZ5UG5WQiIsICJzZW5kZXJfYWRkcmVzcyI6ICJtcGhCUFpmMTVjUk" \
           "ZjTDV0VXE2bUNiRTg0WG9iWjF2ZzdRIiwgInNlY3JldCI6IG51bGwsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRj" \
           "b2luX3JlZnVuZF91bnNpZ25lZCJ9"

    # Refunding HTLC solver
    refund_solver = RefundSolver(
        secret="Hello Meheret!",
        private_key=sender_private_key
    )

    signed_refund_transaction = unsigned_refund_transaction.sign(refund_solver)

    assert signed_refund_transaction.fee
    assert signed_refund_transaction.hash()
    assert signed_refund_transaction.raw()
    assert signed_refund_transaction.json()

    # Singing Hash Time Lock Contract (HTLC)
    refund_signature = RefundSignature(network=network)\
        .sign(unsigned_raw=unsigned_refund_raw, solver=refund_solver)

    signature = Signature(network=network) \
        .sign(unsigned_raw=unsigned_refund_raw, solver=refund_solver)

    assert signature.fee == refund_signature.fee == signed_refund_transaction.fee == 576
    assert signature.hash() == refund_signature.hash() == signed_refund_transaction.hash() == \
           "cab253322cfeaa066b0d52ab6f4a18a035d723271d4bbfb39d43d0aa0ca86c2e"
    assert signature.raw() == refund_signature.raw() == signed_refund_transaction.raw() == \
           "0200000001888be7ec065097d95664763f276d425552d735fb1d974ae78bf72106dca0f39100000000ca483045022100ce6ad4" \
           "458c1ba40b4d08f02b5bdf4aa0a2f73abf9cd7af3c4a1909187f00b7810220049a4733b994732fe52afd78b714bce067a4d31b" \
           "e4b02716f4fb7384f53786160121039213ebcaefdd3e109720c17867ce1bd6d076b0e65e3b6390e6e38548a65e76af004c5c63" \
           "aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a91498f879fb7f8b4951dee9bc8a03" \
           "27b792fbe332b888ac670164b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac686400000001900500000000" \
           "00001976a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac00000000"
    assert signature.json() == refund_signature.json() == signed_refund_transaction.json()

    signed_refund_raw = refund_signature.signed_raw()
    assert signature.signed_raw() == signed_refund_raw == \
           "eyJyYXciOiAiMDIwMDAwMDAwMTg4OGJlN2VjMDY1MDk3ZDk1NjY0NzYzZjI3NmQ0MjU1NTJkNzM1ZmIxZDk3NGFlNzhiZjcyMTA2ZG" \
           "NhMGYzOTEwMDAwMDAwMGNhNDgzMDQ1MDIyMTAwY2U2YWQ0NDU4YzFiYTQwYjRkMDhmMDJiNWJkZjRhYTBhMmY3M2FiZjljZDdhZjNj" \
           "NGExOTA5MTg3ZjAwYjc4MTAyMjAwNDlhNDczM2I5OTQ3MzJmZTUyYWZkNzhiNzE0YmNlMDY3YTRkMzFiZTRiMDI3MTZmNGZiNzM4NG" \
           "Y1Mzc4NjE2MDEyMTAzOTIxM2ViY2FlZmRkM2UxMDk3MjBjMTc4NjdjZTFiZDZkMDc2YjBlNjVlM2I2MzkwZTZlMzg1NDhhNjVlNzZh" \
           "ZjAwNGM1YzYzYWEyMDgyMTEyNGI1NTRkMTNmMjQ3YjFlNWQxMGI4NGU0NGZiMTI5NmYxOGYzOGJiYWExYmVhMzRhMTJjODQzZTAxNT" \
           "g4ODc2YTkxNDk4Zjg3OWZiN2Y4YjQ5NTFkZWU5YmM4YTAzMjdiNzkyZmJlMzMyYjg4OGFjNjcwMTY0YjI3NTc2YTkxNDY0YTgzOTBi" \
           "MGIxNjg1ZmNiZjJkNGI0NTcxMThkYzhkYTkyZDU1MzQ4OGFjNjg2NDAwMDAwMDAxOTAwNTAwMDAwMDAwMDAwMDE5NzZhOTE0NjRhOD" \
           "M5MGIwYjE2ODVmY2JmMmQ0YjQ1NzExOGRjOGRhOTJkNTUzNDg4YWMwMDAwMDAwMCIsICJmZWUiOiA1NzYsICJuZXR3b3JrIjogInRl" \
           "c3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX3JlZnVuZF9zaWduZWQifQ=="
