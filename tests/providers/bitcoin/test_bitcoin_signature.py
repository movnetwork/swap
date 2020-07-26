#!/usr/bin/env python3

from shuttle.providers.bitcoin.wallet import Wallet
from shuttle.providers.bitcoin.signature import (
    Signature, FundSignature, ClaimSignature, RefundSignature
)
from shuttle.providers.bitcoin.solver import (
    FundSolver, ClaimSolver, RefundSolver
)
from shuttle.utils import sha256

import pytest


network = "testnet"
sender_wallet = Wallet(network=network).from_passphrase("meheret tesfaye batu bayou")
recipient_wallet = Wallet(network=network).from_passphrase("meheret")


def test_bitcoin_fund_signature():

    unsigned_fund_transaction_raw = "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMWVjMzEyZTkyZDgzODdiMTVmNjIzOGQ0OTE4MzQ0YjYyYWIxNDdkN2YzODQ0ZGM4MWU2NTM3NzZmZThiODRlZjMwMTAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQyYmIwMTNjM2U0YmViMDg0MjFkZWRjZjgxNWNiNjVhNWMzODgxNzhiODc1MDhhMGUwMDAwMDAwMDAwMTk3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiA5NjM1OTAsICJuIjogMSwgInNjcmlwdCI6ICI3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"

    signature = Signature(version=2, network=network).sign(
        unsigned_raw=unsigned_fund_transaction_raw,
        solver=FundSolver(
            private_key=sender_wallet.private_key()
        )
    )

    fund_signature = FundSignature(version=2, network=network).sign(
        unsigned_raw=unsigned_fund_transaction_raw,
        solver=FundSolver(
            private_key=sender_wallet.private_key()
        )
    )

    assert signature.fee() == fund_signature.fee() == 678
    assert signature.hash() == fund_signature.hash() == "7e52333d38b7571807caac7971c925dd2c007dbf34a6c46138ff3d0213281d60"
    assert signature.raw() == fund_signature.raw() == "0200000001ec312e92d8387b15f6238d4918344b62ab147d7f3844dc81e653776fe8b84ef3010000006b483045022100b4d4de4c10bec380a9f07019d5232a9af9f0c2321e5efcf33f5326a60378144502203e1ab2ddaac8afade132832e715f055f956d3e730b9d035a4e99ec9dfdc7acfd012103c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84ffffffff02102700000000000017a9142bb013c3e4beb08421dedcf815cb65a5c388178b87508a0e00000000001976a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac00000000"
    assert signature.json() == fund_signature.json() == {'hex': '0200000001ec312e92d8387b15f6238d4918344b62ab147d7f3844dc81e653776fe8b84ef3010000006b483045022100b4d4de4c10bec380a9f07019d5232a9af9f0c2321e5efcf33f5326a60378144502203e1ab2ddaac8afade132832e715f055f956d3e730b9d035a4e99ec9dfdc7acfd012103c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84ffffffff02102700000000000017a9142bb013c3e4beb08421dedcf815cb65a5c388178b87508a0e00000000001976a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac00000000', 'txid': '7e52333d38b7571807caac7971c925dd2c007dbf34a6c46138ff3d0213281d60', 'hash': '7e52333d38b7571807caac7971c925dd2c007dbf34a6c46138ff3d0213281d60', 'size': 224, 'vsize': 224, 'version': 2, 'locktime': 0, 'vin': [{'txid': 'f34eb8e86f7753e681dc44387f7d14ab624b3418498d23f6157b38d8922e31ec', 'vout': 1, 'scriptSig': {'asm': '3045022100b4d4de4c10bec380a9f07019d5232a9af9f0c2321e5efcf33f5326a60378144502203e1ab2ddaac8afade132832e715f055f956d3e730b9d035a4e99ec9dfdc7acfd01 03c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84', 'hex': '483045022100b4d4de4c10bec380a9f07019d5232a9af9f0c2321e5efcf33f5326a60378144502203e1ab2ddaac8afade132832e715f055f956d3e730b9d035a4e99ec9dfdc7acfd012103c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84'}, 'sequence': '4294967295'}], 'vout': [{'value': '0.00010000', 'n': 0, 'scriptPubKey': {'asm': 'OP_HASH160 2bb013c3e4beb08421dedcf815cb65a5c388178b OP_EQUAL', 'hex': 'a9142bb013c3e4beb08421dedcf815cb65a5c388178b87', 'type': 'p2sh', 'address': '2MwEDybGC34949zgzWX4M9FHmE3crDSUydP'}}, {'value': '0.00952912', 'n': 1, 'scriptPubKey': {'asm': 'OP_DUP OP_HASH160 64a8390b0b1685fcbf2d4b457118dc8da92d5534 OP_EQUALVERIFY OP_CHECKSIG', 'hex': '76a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac', 'type': 'p2pkh', 'address': 'mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q'}}]}
    assert signature.type() == fund_signature.type() == "bitcoin_fund_signed"
    assert signature.signed_raw() == fund_signature.signed_raw() == "eyJyYXciOiAiMDIwMDAwMDAwMWVjMzEyZTkyZDgzODdiMTVmNjIzOGQ0OTE4MzQ0YjYyYWIxNDdkN2YzODQ0ZGM4MWU2NTM3NzZmZThiODRlZjMwMTAwMDAwMDZiNDgzMDQ1MDIyMTAwYjRkNGRlNGMxMGJlYzM4MGE5ZjA3MDE5ZDUyMzJhOWFmOWYwYzIzMjFlNWVmY2YzM2Y1MzI2YTYwMzc4MTQ0NTAyMjAzZTFhYjJkZGFhYzhhZmFkZTEzMjgzMmU3MTVmMDU1Zjk1NmQzZTczMGI5ZDAzNWE0ZTk5ZWM5ZGZkYzdhY2ZkMDEyMTAzYzU2YTYwMDVkNGE4ODkyZDI4Y2MzZjcyNjVlNTY4NWI1NDg2MjdkNTkxMDg5NzNlNDc0YzRlMjZmNjlhNGM4NGZmZmZmZmZmMDIxMDI3MDAwMDAwMDAwMDAwMTdhOTE0MmJiMDEzYzNlNGJlYjA4NDIxZGVkY2Y4MTVjYjY1YTVjMzg4MTc4Yjg3NTA4YTBlMDAwMDAwMDAwMDE5NzZhOTE0NjRhODM5MGIwYjE2ODVmY2JmMmQ0YjQ1NzExOGRjOGRhOTJkNTUzNDg4YWMwMDAwMDAwMCIsICJmZWUiOiA2NzgsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfc2lnbmVkIn0="


def test_bitcoin_claim_signature():

    unsigned_claim_transaction_raw = "eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMWVjMzEyZTkyZDgzODdiMTVmNjIzOGQ0OTE4MzQ0YjYyYWIxNDdkN2YzODQ0ZGM4MWU2NTM3NzZmZThiODRlZjMwMDAwMDAwMDAwZmZmZmZmZmYwMWQwMjQwMDAwMDAwMDAwMDAxOTc2YTkxNDk4Zjg3OWZiN2Y4YjQ5NTFkZWU5YmM4YTAzMjdiNzkyZmJlMzMyYjg4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsiYW1vdW50IjogMTAwMDAsICJuIjogMCwgInNjcmlwdCI6ICJhOTE0MmJiMDEzYzNlNGJlYjA4NDIxZGVkY2Y4MTVjYjY1YTVjMzg4MTc4Yjg3In0sICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX2NsYWltX3Vuc2lnbmVkIn0="

    signature = Signature(version=2, network=network).sign(
        unsigned_raw=unsigned_claim_transaction_raw,
        solver=ClaimSolver(
            private_key=recipient_wallet.private_key(),
            secret="Hello Meheret!",
            secret_hash=sha256("Hello Meheret!"),
            recipient_address=recipient_wallet.address(),
            sender_address=sender_wallet.address(),
            sequence=1000
        )
    )

    claim_signature = ClaimSignature(version=2, network=network).sign(
        unsigned_raw=unsigned_claim_transaction_raw,
        solver=ClaimSolver(
            private_key=recipient_wallet.private_key(),
            secret="Hello Meheret!",
            secret_hash=sha256("Hello Meheret!"),
            recipient_address=recipient_wallet.address(),
            sender_address=sender_wallet.address(),
            sequence=1000
        )
    )

    assert signature.fee() == claim_signature.fee() == 576
    assert signature.hash() == claim_signature.hash() == "5235dba12bc257f0a6b76129b4e2ee6621cdb906c76acb88fc0986731f957bad"
    assert signature.raw() == claim_signature.raw() == "0200000001ec312e92d8387b15f6238d4918344b62ab147d7f3844dc81e653776fe8b84ef300000000d9473044022041aed3386ab426810732f700a8f9f2a2749d0e3faa9c2500452f83f3205eac42022072708301b4726b6b7896fff617918a02986f83ec06c6758c71f0830c924d287d0121039213ebcaefdd3e109720c17867ce1bd6d076b0e65e3b6390e6e38548a65e76af0e48656c6c6f204d65686572657421514c5d63aa204683a21fd5ce2425adc90a3674b6d8d3d418935540fc3a71c6ec3cb249925dd38876a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac6702e803b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68ffffffff01d0240000000000001976a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac00000000"
    assert signature.json() == claim_signature.json() == {'hex': '0200000001ec312e92d8387b15f6238d4918344b62ab147d7f3844dc81e653776fe8b84ef300000000d9473044022041aed3386ab426810732f700a8f9f2a2749d0e3faa9c2500452f83f3205eac42022072708301b4726b6b7896fff617918a02986f83ec06c6758c71f0830c924d287d0121039213ebcaefdd3e109720c17867ce1bd6d076b0e65e3b6390e6e38548a65e76af0e48656c6c6f204d65686572657421514c5d63aa204683a21fd5ce2425adc90a3674b6d8d3d418935540fc3a71c6ec3cb249925dd38876a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac6702e803b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68ffffffff01d0240000000000001976a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac00000000', 'txid': '5235dba12bc257f0a6b76129b4e2ee6621cdb906c76acb88fc0986731f957bad', 'hash': '5235dba12bc257f0a6b76129b4e2ee6621cdb906c76acb88fc0986731f957bad', 'size': 302, 'vsize': 302, 'version': 2, 'locktime': 0, 'vin': [{'txid': 'f34eb8e86f7753e681dc44387f7d14ab624b3418498d23f6157b38d8922e31ec', 'vout': 0, 'scriptSig': {'asm': '3044022041aed3386ab426810732f700a8f9f2a2749d0e3faa9c2500452f83f3205eac42022072708301b4726b6b7896fff617918a02986f83ec06c6758c71f0830c924d287d01 039213ebcaefdd3e109720c17867ce1bd6d076b0e65e3b6390e6e38548a65e76af 48656c6c6f204d65686572657421 OP_1 63aa204683a21fd5ce2425adc90a3674b6d8d3d418935540fc3a71c6ec3cb249925dd38876a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac6702e803b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68', 'hex': '473044022041aed3386ab426810732f700a8f9f2a2749d0e3faa9c2500452f83f3205eac42022072708301b4726b6b7896fff617918a02986f83ec06c6758c71f0830c924d287d0121039213ebcaefdd3e109720c17867ce1bd6d076b0e65e3b6390e6e38548a65e76af0e48656c6c6f204d65686572657421514c5d63aa204683a21fd5ce2425adc90a3674b6d8d3d418935540fc3a71c6ec3cb249925dd38876a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac6702e803b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68'}, 'sequence': '4294967295'}], 'vout': [{'value': '0.00009424', 'n': 0, 'scriptPubKey': {'asm': 'OP_DUP OP_HASH160 98f879fb7f8b4951dee9bc8a0327b792fbe332b8 OP_EQUALVERIFY OP_CHECKSIG', 'hex': '76a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac', 'type': 'p2pkh', 'address': 'muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB'}}]}
    assert signature.type() == claim_signature.type() == "bitcoin_claim_signed"
    assert signature.signed_raw() == claim_signature.signed_raw() == "eyJyYXciOiAiMDIwMDAwMDAwMWVjMzEyZTkyZDgzODdiMTVmNjIzOGQ0OTE4MzQ0YjYyYWIxNDdkN2YzODQ0ZGM4MWU2NTM3NzZmZThiODRlZjMwMDAwMDAwMGQ5NDczMDQ0MDIyMDQxYWVkMzM4NmFiNDI2ODEwNzMyZjcwMGE4ZjlmMmEyNzQ5ZDBlM2ZhYTljMjUwMDQ1MmY4M2YzMjA1ZWFjNDIwMjIwNzI3MDgzMDFiNDcyNmI2Yjc4OTZmZmY2MTc5MThhMDI5ODZmODNlYzA2YzY3NThjNzFmMDgzMGM5MjRkMjg3ZDAxMjEwMzkyMTNlYmNhZWZkZDNlMTA5NzIwYzE3ODY3Y2UxYmQ2ZDA3NmIwZTY1ZTNiNjM5MGU2ZTM4NTQ4YTY1ZTc2YWYwZTQ4NjU2YzZjNmYyMDRkNjU2ODY1NzI2NTc0MjE1MTRjNWQ2M2FhMjA0NjgzYTIxZmQ1Y2UyNDI1YWRjOTBhMzY3NGI2ZDhkM2Q0MTg5MzU1NDBmYzNhNzFjNmVjM2NiMjQ5OTI1ZGQzODg3NmE5MTQ5OGY4NzlmYjdmOGI0OTUxZGVlOWJjOGEwMzI3Yjc5MmZiZTMzMmI4ODhhYzY3MDJlODAzYjI3NTc2YTkxNDY0YTgzOTBiMGIxNjg1ZmNiZjJkNGI0NTcxMThkYzhkYTkyZDU1MzQ4OGFjNjhmZmZmZmZmZjAxZDAyNDAwMDAwMDAwMDAwMDE5NzZhOTE0OThmODc5ZmI3ZjhiNDk1MWRlZTliYzhhMDMyN2I3OTJmYmUzMzJiODg4YWMwMDAwMDAwMCIsICJmZWUiOiA1NzYsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX2NsYWltX3NpZ25lZCJ9"


def test_bitcoin_refund_signature():

    unsigned_refund_transaction_raw = "eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMWVjMzEyZTkyZDgzODdiMTVmNjIzOGQ0OTE4MzQ0YjYyYWIxNDdkN2YzODQ0ZGM4MWU2NTM3NzZmZThiODRlZjMwMDAwMDAwMDAwZmZmZmZmZmYwMWQwMjQwMDAwMDAwMDAwMDAxOTc2YTkxNDY0YTgzOTBiMGIxNjg1ZmNiZjJkNGI0NTcxMThkYzhkYTkyZDU1MzQ4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsidmFsdWUiOiAxMDAwMCwgIm4iOiAwLCAic2NyaXB0X3B1YmtleSI6ICJhOTE0MmJiMDEzYzNlNGJlYjA4NDIxZGVkY2Y4MTVjYjY1YTVjMzg4MTc4Yjg3In0sICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX3JlZnVuZF91bnNpZ25lZCJ9"

    signature = Signature(version=2, network=network).sign(
        unsigned_raw=unsigned_refund_transaction_raw,
        solver=RefundSolver(
            private_key=sender_wallet.private_key(),
            secret_hash=sha256("Hello Meheret!"),
            recipient_address=recipient_wallet.address(),
            sender_address=sender_wallet.address(),
            sequence=1000
        )
    )

    refund_signature = RefundSignature(version=2, network=network).sign(
        unsigned_raw=unsigned_refund_transaction_raw,
        solver=RefundSolver(
            private_key=sender_wallet.private_key(),
            secret_hash=sha256("Hello Meheret!"),
            recipient_address=recipient_wallet.address(),
            sender_address=sender_wallet.address(),
            sequence=1000
        )
    )

    assert signature.fee() == refund_signature.fee() == 576
    assert signature.hash() == refund_signature.hash() == "429f99906296e801c2bb0423339208df552463ae5c04d8f13d302281541b0e5b"
    assert signature.raw() == refund_signature.raw() == "0200000001ec312e92d8387b15f6238d4918344b62ab147d7f3844dc81e653776fe8b84ef300000000ca47304402203c73c35fe39cf0e030b47c98a7a52e2520ed8bf25d8b58d741968cd80746ac3902203a704cfcf9ea74e113994f25becfac474d0c6cd07169ebe4cb589e44d515bb45012103c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84004c5d63aa204683a21fd5ce2425adc90a3674b6d8d3d418935540fc3a71c6ec3cb249925dd38876a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac6702e803b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68e803000001d0240000000000001976a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac00000000"
    assert signature.json() == refund_signature.json() == {'hex': '0200000001ec312e92d8387b15f6238d4918344b62ab147d7f3844dc81e653776fe8b84ef300000000ca47304402203c73c35fe39cf0e030b47c98a7a52e2520ed8bf25d8b58d741968cd80746ac3902203a704cfcf9ea74e113994f25becfac474d0c6cd07169ebe4cb589e44d515bb45012103c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84004c5d63aa204683a21fd5ce2425adc90a3674b6d8d3d418935540fc3a71c6ec3cb249925dd38876a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac6702e803b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68e803000001d0240000000000001976a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac00000000', 'txid': '429f99906296e801c2bb0423339208df552463ae5c04d8f13d302281541b0e5b', 'hash': '429f99906296e801c2bb0423339208df552463ae5c04d8f13d302281541b0e5b', 'size': 287, 'vsize': 287, 'version': 2, 'locktime': 0, 'vin': [{'txid': 'f34eb8e86f7753e681dc44387f7d14ab624b3418498d23f6157b38d8922e31ec', 'vout': 0, 'scriptSig': {'asm': '304402203c73c35fe39cf0e030b47c98a7a52e2520ed8bf25d8b58d741968cd80746ac3902203a704cfcf9ea74e113994f25becfac474d0c6cd07169ebe4cb589e44d515bb4501 03c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84 OP_0 63aa204683a21fd5ce2425adc90a3674b6d8d3d418935540fc3a71c6ec3cb249925dd38876a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac6702e803b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68', 'hex': '47304402203c73c35fe39cf0e030b47c98a7a52e2520ed8bf25d8b58d741968cd80746ac3902203a704cfcf9ea74e113994f25becfac474d0c6cd07169ebe4cb589e44d515bb45012103c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84004c5d63aa204683a21fd5ce2425adc90a3674b6d8d3d418935540fc3a71c6ec3cb249925dd38876a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac6702e803b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68'}, 'sequence': '1000'}], 'vout': [{'value': '0.00009424', 'n': 0, 'scriptPubKey': {'asm': 'OP_DUP OP_HASH160 64a8390b0b1685fcbf2d4b457118dc8da92d5534 OP_EQUALVERIFY OP_CHECKSIG', 'hex': '76a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac', 'type': 'p2pkh', 'address': 'mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q'}}]}
    assert signature.type() == refund_signature.type() == "bitcoin_refund_signed"
    assert signature.signed_raw() == refund_signature.signed_raw() == "eyJyYXciOiAiMDIwMDAwMDAwMWVjMzEyZTkyZDgzODdiMTVmNjIzOGQ0OTE4MzQ0YjYyYWIxNDdkN2YzODQ0ZGM4MWU2NTM3NzZmZThiODRlZjMwMDAwMDAwMGNhNDczMDQ0MDIyMDNjNzNjMzVmZTM5Y2YwZTAzMGI0N2M5OGE3YTUyZTI1MjBlZDhiZjI1ZDhiNThkNzQxOTY4Y2Q4MDc0NmFjMzkwMjIwM2E3MDRjZmNmOWVhNzRlMTEzOTk0ZjI1YmVjZmFjNDc0ZDBjNmNkMDcxNjllYmU0Y2I1ODllNDRkNTE1YmI0NTAxMjEwM2M1NmE2MDA1ZDRhODg5MmQyOGNjM2Y3MjY1ZTU2ODViNTQ4NjI3ZDU5MTA4OTczZTQ3NGM0ZTI2ZjY5YTRjODQwMDRjNWQ2M2FhMjA0NjgzYTIxZmQ1Y2UyNDI1YWRjOTBhMzY3NGI2ZDhkM2Q0MTg5MzU1NDBmYzNhNzFjNmVjM2NiMjQ5OTI1ZGQzODg3NmE5MTQ5OGY4NzlmYjdmOGI0OTUxZGVlOWJjOGEwMzI3Yjc5MmZiZTMzMmI4ODhhYzY3MDJlODAzYjI3NTc2YTkxNDY0YTgzOTBiMGIxNjg1ZmNiZjJkNGI0NTcxMThkYzhkYTkyZDU1MzQ4OGFjNjhlODAzMDAwMDAxZDAyNDAwMDAwMDAwMDAwMDE5NzZhOTE0NjRhODM5MGIwYjE2ODVmY2JmMmQ0YjQ1NzExOGRjOGRhOTJkNTUzNDg4YWMwMDAwMDAwMCIsICJmZWUiOiA1NzYsICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX3JlZnVuZF9zaWduZWQifQ=="


def test_signature_exceptions():

    with pytest.raises(ValueError, match="invalid network, please choose only mainnet or testnet networks"):
        Signature(network="solonet")

    with pytest.raises(ValueError, match="transaction script is none, sign first"):
        Signature().hash()

    with pytest.raises(ValueError, match="transaction script is none, sign first"):
        Signature().json()

    with pytest.raises(ValueError, match="transaction script is none, build transaction first"):
        Signature().raw()

    with pytest.raises(ValueError, match="not found type, sign first"):
        Signature().type()

    with pytest.raises(ValueError, match="there is no signed data, sign first"):
        Signature().signed_raw()

    with pytest.raises(TypeError, match=r"invalid Bitcoin fund unsigned transaction type, .*"):
        FundSignature().sign(
            unsigned_raw="eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMWVjMzEyZTkyZDgzODdiMTVmNjIzOGQ0OTE4MzQ0YjYyYWIxNDdkN2YzODQ0ZGM4MWU2NTM3NzZmZThiODRlZjMwMDAwMDAwMDAwZmZmZmZmZmYwMWQwMjQwMDAwMDAwMDAwMDAxOTc2YTkxNDY0YTgzOTBiMGIxNjg1ZmNiZjJkNGI0NTcxMThkYzhkYTkyZDU1MzQ4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsidmFsdWUiOiAxMDAwMCwgIm4iOiAwLCAic2NyaXB0X3B1YmtleSI6ICJhOTE0MmJiMDEzYzNlNGJlYjA4NDIxZGVkY2Y4MTVjYjY1YTVjMzg4MTc4Yjg3In0sICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX3JlZnVuZF91bnNpZ25lZCJ9",
            solver=FundSolver(
                private_key=sender_wallet.private_key()
            )
        )

    with pytest.raises(TypeError, match=r"invalid Bitcoin claim unsigned transaction type, .*"):
        ClaimSignature().sign(
            unsigned_raw="eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMWVjMzEyZTkyZDgzODdiMTVmNjIzOGQ0OTE4MzQ0YjYyYWIxNDdkN2YzODQ0ZGM4MWU2NTM3NzZmZThiODRlZjMwMTAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQyYmIwMTNjM2U0YmViMDg0MjFkZWRjZjgxNWNiNjVhNWMzODgxNzhiODc1MDhhMGUwMDAwMDAwMDAwMTk3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiA5NjM1OTAsICJuIjogMSwgInNjcmlwdCI6ICI3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9",
            solver=ClaimSolver(
                private_key=recipient_wallet.private_key(),
                secret="Hello Meheret!",
                secret_hash=sha256("Hello Meheret!"),
                recipient_address=recipient_wallet.address(),
                sender_address=sender_wallet.address(),
                sequence=1000
            )
        )

    with pytest.raises(TypeError, match=r"invalid Bitcoin refund unsigned transaction type, .*"):
        RefundSignature().sign(
            unsigned_raw="eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMWVjMzEyZTkyZDgzODdiMTVmNjIzOGQ0OTE4MzQ0YjYyYWIxNDdkN2YzODQ0ZGM4MWU2NTM3NzZmZThiODRlZjMwMDAwMDAwMDAwZmZmZmZmZmYwMWQwMjQwMDAwMDAwMDAwMDAxOTc2YTkxNDk4Zjg3OWZiN2Y4YjQ5NTFkZWU5YmM4YTAzMjdiNzkyZmJlMzMyYjg4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsiYW1vdW50IjogMTAwMDAsICJuIjogMCwgInNjcmlwdCI6ICJhOTE0MmJiMDEzYzNlNGJlYjA4NDIxZGVkY2Y4MTVjYjY1YTVjMzg4MTc4Yjg3In0sICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX2NsYWltX3Vuc2lnbmVkIn0",
            solver=RefundSolver(
                private_key=sender_wallet.private_key(),
                secret_hash=sha256("Hello Meheret!"),
                recipient_address=recipient_wallet.address(),
                sender_address=sender_wallet.address(),
                sequence=1000
            )
        )

    with pytest.raises(ValueError, match="invalid Bitcoin unsigned transaction raw"):
        Signature().sign("eyJtIjogImFzZCJ9", "")

    with pytest.raises(ValueError, match="invalid Bitcoin unsigned fund transaction raw"):
        FundSignature().sign("eyJtIjogImFzZCJ9", "")

    with pytest.raises(ValueError, match="invalid Bitcoin unsigned claim transaction raw"):
        ClaimSignature().sign("eyJtIjogImFzZCJ9", "")

    with pytest.raises(ValueError, match="invalid Bitcoin unsigned refund transaction raw"):
        RefundSignature().sign("eyJtIjogImFzZCJ9", "")

    with pytest.raises(TypeError, match="invalid Bitcoin solver, it's only takes Bitcoin FundSolver class"):
        FundSignature().sign(
            unsigned_raw="eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMWVjMzEyZTkyZDgzODdiMTVmNjIzOGQ0OTE4MzQ0YjYyYWIxNDdkN2YzODQ0ZGM4MWU2NTM3NzZmZThiODRlZjMwMTAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQyYmIwMTNjM2U0YmViMDg0MjFkZWRjZjgxNWNiNjVhNWMzODgxNzhiODc1MDhhMGUwMDAwMDAwMDAwMTk3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiA5NjM1OTAsICJuIjogMSwgInNjcmlwdCI6ICI3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9",
            solver=RefundSolver(
                private_key=sender_wallet.private_key(),
                secret_hash=sha256("Hello Meheret!"),
                recipient_address=recipient_wallet.address(),
                sender_address=sender_wallet.address(),
                sequence=1000
            )
        )

    with pytest.raises(TypeError, match="invalid Bitcoin solver, it's only takes Bitcoin ClaimSolver class"):
        ClaimSignature().sign(
            unsigned_raw="eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMWVjMzEyZTkyZDgzODdiMTVmNjIzOGQ0OTE4MzQ0YjYyYWIxNDdkN2YzODQ0ZGM4MWU2NTM3NzZmZThiODRlZjMwMDAwMDAwMDAwZmZmZmZmZmYwMWQwMjQwMDAwMDAwMDAwMDAxOTc2YTkxNDk4Zjg3OWZiN2Y4YjQ5NTFkZWU5YmM4YTAzMjdiNzkyZmJlMzMyYjg4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsiYW1vdW50IjogMTAwMDAsICJuIjogMCwgInNjcmlwdCI6ICJhOTE0MmJiMDEzYzNlNGJlYjA4NDIxZGVkY2Y4MTVjYjY1YTVjMzg4MTc4Yjg3In0sICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX2NsYWltX3Vuc2lnbmVkIn0",
            solver=FundSolver(
                private_key=sender_wallet.private_key()
            )
        )

    with pytest.raises(TypeError, match="invalid Bitcoin solver, it's only takes Bitcoin RefundSolver class"):
        RefundSignature().sign(
            unsigned_raw="eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMWVjMzEyZTkyZDgzODdiMTVmNjIzOGQ0OTE4MzQ0YjYyYWIxNDdkN2YzODQ0ZGM4MWU2NTM3NzZmZThiODRlZjMwMDAwMDAwMDAwZmZmZmZmZmYwMWQwMjQwMDAwMDAwMDAwMDAxOTc2YTkxNDY0YTgzOTBiMGIxNjg1ZmNiZjJkNGI0NTcxMThkYzhkYTkyZDU1MzQ4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsidmFsdWUiOiAxMDAwMCwgIm4iOiAwLCAic2NyaXB0X3B1YmtleSI6ICJhOTE0MmJiMDEzYzNlNGJlYjA4NDIxZGVkY2Y4MTVjYjY1YTVjMzg4MTc4Yjg3In0sICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX3JlZnVuZF91bnNpZ25lZCJ9",
            solver=ClaimSolver(
                private_key=recipient_wallet.private_key(),
                secret="Hello Meheret!",
                secret_hash=sha256("Hello Meheret!"),
                recipient_address=recipient_wallet.address(),
                sender_address=sender_wallet.address(),
                sequence=1000
            )
        )
