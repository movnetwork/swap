#!/usr/bin/env python3

from shuttle.providers.bitcoin.wallet import Wallet
from shuttle.providers.bitcoin.transaction import ClaimTransaction
from shuttle.providers.bitcoin.solver import ClaimSolver
from shuttle.providers.bitcoin.signature import ClaimSignature, Signature

network = "testnet"
recipient_passphrase = "meheret".encode()

# Initialize recipient bitcoin wallet
recipient_wallet = Wallet(network=network)\
    .from_passphrase(recipient_passphrase)
recipient_private_key = recipient_wallet.private_key()
# Funded hash time lock contract transaction id/hash
fund_transaction_id = "91f3a0dc0621f78be74a971dfb35d75255426d273f766456d9975006ece78b88"


# Testing bitcoin claim
def test_bitcoin_claim():
    # Initialization claim transaction
    unsigned_claim_transaction = ClaimTransaction(version=2, network=network)
    # Building claim transaction
    unsigned_claim_transaction.build_transaction(
        transaction_id=fund_transaction_id,
        wallet=recipient_wallet,
        amount=2000
    )

    assert unsigned_claim_transaction.fee == 576
    assert unsigned_claim_transaction.hash() == "726e390af02215d346be089dff566ae070f7332e8927d83acbb40b0e9105a787"
    assert unsigned_claim_transaction.raw() == \
           "0200000001888be7ec065097d95664763f276d425552d735fb1d974ae78bf72106dca0f3910000000000ffffffff019005000" \
           "0000000001976a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac00000000"
    assert unsigned_claim_transaction.json()

    unsigned_claim_raw = unsigned_claim_transaction.unsigned_raw()
    assert unsigned_claim_raw == \
           "eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMTg4OGJlN2VjMDY1MDk3ZDk1NjY0NzYzZjI3NmQ0MjU1NTJkNzM1ZmIxZDk3N" \
           "GFlNzhiZjcyMTA2ZGNhMGYzOTEwMDAwMDAwMDAwZmZmZmZmZmYwMTkwMDUwMDAwMDAwMDAwMDAxOTc2YTkxNDk4Zjg3OWZiN2Y4Yj" \
           "Q5NTFkZWU5YmM4YTAzMjdiNzkyZmJlMzMyYjg4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IFt7ImFtb3VudCI6IDIwMDAsICJuIjo" \
           "gMCwgInNjcmlwdCI6ICJhOTE0NmYwOGIyNTRlNGM1OGRjNjVmNmYzOTljM2JlNzE3N2I5MDFmNGE2Njg3In1dLCAicmVjaXBpZW50" \
           "X2FkZHJlc3MiOiAibXVUbmZmTERSNUx0RmVMUjJpM1dzS1ZmZHl2emZ5UG5WQiIsICJzZW5kZXJfYWRkcmVzcyI6ICJtcGhCUFpmM" \
           "TVjUkZjTDV0VXE2bUNiRTg0WG9iWjF2ZzdRIiwgInNlY3JldCI6IG51bGwsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6IC" \
           "JiaXRjb2luX2NsYWltX3Vuc2lnbmVkIn0="

    # Claiming HTLC solver
    claim_solver = ClaimSolver(
        secret="Hello Meheret!",
        private_key=recipient_private_key
    )

    signed_claim_transaction = unsigned_claim_transaction.sign(claim_solver)

    assert signed_claim_transaction.fee
    assert signed_claim_transaction.hash()
    assert signed_claim_transaction.raw()
    assert signed_claim_transaction.json()

    # Singing Hash Time Lock Contract (HTLC)
    claim_signature = ClaimSignature(network=network)\
        .sign(unsigned_raw=unsigned_claim_raw, solver=claim_solver)

    signature = Signature(network=network) \
        .sign(unsigned_raw=unsigned_claim_raw, solver=claim_solver)

    assert signature.fee == claim_signature.fee == signed_claim_transaction.fee == 576
    assert signature.hash() == claim_signature.hash() == signed_claim_transaction.hash() == \
           "910a173757d59492a6e807bf270650e950dde7949d540e70cc0ce5123008a52c"
    assert signature.raw() == claim_signature.raw() == signed_claim_transaction.raw() == \
           "0200000001888be7ec065097d95664763f276d425552d735fb1d974ae78bf72106dca0f39100000000d847304402204e20eeb" \
           "3cb82dbe51f7929cd4e819891102d2d7a280919013ae31f12aa49212602206fbce96d734823579e6a4bb4b517d618dca47606" \
           "2f54d9df06aee4b73d08eae20121039213ebcaefdd3e109720c17867ce1bd6d076b0e65e3b6390e6e38548a65e76af0e48656" \
           "c6c6f204d65686572657421514c5c63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e015888" \
           "76a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac670164b27576a91464a8390b0b1685fcbf2d4b457118dc8da92" \
           "d553488ac68ffffffff0190050000000000001976a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac00000000"
    assert signature.json() == claim_signature.json() == signed_claim_transaction.json()

    signed_claim_raw = claim_signature.signed_raw()
    assert signature.signed_raw() == signed_claim_raw == \
           "eyJyYXciOiAiMDIwMDAwMDAwMTg4OGJlN2VjMDY1MDk3ZDk1NjY0NzYzZjI3NmQ0MjU1NTJkNzM1ZmIxZDk3NGFlNzhiZjcyMTA2Z" \
           "GNhMGYzOTEwMDAwMDAwMGQ4NDczMDQ0MDIyMDRlMjBlZWIzY2I4MmRiZTUxZjc5MjljZDRlODE5ODkxMTAyZDJkN2EyODA5MTkwMT" \
           "NhZTMxZjEyYWE0OTIxMjYwMjIwNmZiY2U5NmQ3MzQ4MjM1NzllNmE0YmI0YjUxN2Q2MThkY2E0NzYwNjJmNTRkOWRmMDZhZWU0Yjc" \
           "zZDA4ZWFlMjAxMjEwMzkyMTNlYmNhZWZkZDNlMTA5NzIwYzE3ODY3Y2UxYmQ2ZDA3NmIwZTY1ZTNiNjM5MGU2ZTM4NTQ4YTY1ZTc2" \
           "YWYwZTQ4NjU2YzZjNmYyMDRkNjU2ODY1NzI2NTc0MjE1MTRjNWM2M2FhMjA4MjExMjRiNTU0ZDEzZjI0N2IxZTVkMTBiODRlNDRmY" \
           "jEyOTZmMThmMzhiYmFhMWJlYTM0YTEyYzg0M2UwMTU4ODg3NmE5MTQ5OGY4NzlmYjdmOGI0OTUxZGVlOWJjOGEwMzI3Yjc5MmZiZT" \
           "MzMmI4ODhhYzY3MDE2NGIyNzU3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYzY4ZmZmZmZ" \
           "mZmYwMTkwMDUwMDAwMDAwMDAwMDAxOTc2YTkxNDk4Zjg3OWZiN2Y4YjQ5NTFkZWU5YmM4YTAzMjdiNzkyZmJlMzMyYjg4OGFjMDAw" \
           "MDAwMDAiLCAiZmVlIjogNTc2LCAibmV0d29yayI6ICJ0ZXN0bmV0IiwgInR5cGUiOiAiYml0Y29pbl9jbGFpbV9zaWduZWQifQ=="
