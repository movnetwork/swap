#!/usr/bin/env python3

from shuttle.providers.bitcoin.wallet import Wallet
from shuttle.providers.bitcoin.htlc import HTLC
from shuttle.providers.bitcoin.transaction import (
    FundTransaction, ClaimTransaction, RefundTransaction
)
from shuttle.providers.bitcoin.solver import (
    FundSolver, ClaimSolver, RefundSolver
)
from shuttle.utils import sha256

import pytest


network = "testnet"
sender_wallet = Wallet(network=network).from_passphrase("meheret tesfaye batu bayou")
recipient_wallet = Wallet(network=network).from_passphrase("meheret")
transaction_id = "f34eb8e86f7753e681dc44387f7d14ab624b3418498d23f6157b38d8922e31ec"


def test_bitcoin_fund_transaction():

    unsigned_fund_transaction = FundTransaction(
        version=2, network=network
    )

    unsigned_fund_transaction.build_transaction(
        wallet=sender_wallet,
        htlc=HTLC(network=network).init(
            secret_hash=sha256("Hello Meheret!".encode()).hex(),
            recipient_address=recipient_wallet.address(),
            sender_address=sender_wallet.address(),
            sequence=1000
        ),
        amount=10_000
    )

    assert unsigned_fund_transaction.fee() == 678
    assert unsigned_fund_transaction.hash() == "f05f2afb0706020cc15b66d63e2fd9d89cfe5ce7a9f458f3a8a6fb3c1849cf20"
    assert unsigned_fund_transaction.raw() == "0200000001ec312e92d8387b15f6238d4918344b62ab147d7f3844dc81e653776fe8b84ef30100000000ffffffff02102700000000000017a9142bb013c3e4beb08421dedcf815cb65a5c388178b87508a0e00000000001976a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac00000000"
    assert unsigned_fund_transaction.json() == {'hex': '0200000001ec312e92d8387b15f6238d4918344b62ab147d7f3844dc81e653776fe8b84ef30100000000ffffffff02102700000000000017a9142bb013c3e4beb08421dedcf815cb65a5c388178b87508a0e00000000001976a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac00000000', 'txid': 'f05f2afb0706020cc15b66d63e2fd9d89cfe5ce7a9f458f3a8a6fb3c1849cf20', 'hash': 'f05f2afb0706020cc15b66d63e2fd9d89cfe5ce7a9f458f3a8a6fb3c1849cf20', 'size': 117, 'vsize': 117, 'version': 2, 'locktime': 0, 'vin': [{'txid': 'f34eb8e86f7753e681dc44387f7d14ab624b3418498d23f6157b38d8922e31ec', 'vout': 1, 'scriptSig': {'asm': '', 'hex': ''}, 'sequence': '4294967295'}], 'vout': [{'value': '0.00010000', 'n': 0, 'scriptPubKey': {'asm': 'OP_HASH160 2bb013c3e4beb08421dedcf815cb65a5c388178b OP_EQUAL', 'hex': 'a9142bb013c3e4beb08421dedcf815cb65a5c388178b87', 'type': 'p2sh', 'address': '2MwEDybGC34949zgzWX4M9FHmE3crDSUydP'}}, {'value': '0.00952912', 'n': 1, 'scriptPubKey': {'asm': 'OP_DUP OP_HASH160 64a8390b0b1685fcbf2d4b457118dc8da92d5534 OP_EQUALVERIFY OP_CHECKSIG', 'hex': '76a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac', 'type': 'p2pkh', 'address': 'mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q'}}]}
    assert unsigned_fund_transaction.type() == "bitcoin_fund_unsigned"
    assert unsigned_fund_transaction.unsigned_raw() == "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMWVjMzEyZTkyZDgzODdiMTVmNjIzOGQ0OTE4MzQ0YjYyYWIxNDdkN2YzODQ0ZGM4MWU2NTM3NzZmZThiODRlZjMwMTAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQyYmIwMTNjM2U0YmViMDg0MjFkZWRjZjgxNWNiNjVhNWMzODgxNzhiODc1MDhhMGUwMDAwMDAwMDAwMTk3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiA5NjM1OTAsICJuIjogMSwgInNjcmlwdCI6ICI3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"

    signed_fund_transaction = unsigned_fund_transaction.sign(
        solver=FundSolver(
            private_key=sender_wallet.private_key()
        )
    )

    assert signed_fund_transaction.fee() == 678
    assert signed_fund_transaction.hash() == "7e52333d38b7571807caac7971c925dd2c007dbf34a6c46138ff3d0213281d60"
    assert signed_fund_transaction.raw() == "0200000001ec312e92d8387b15f6238d4918344b62ab147d7f3844dc81e653776fe8b84ef3010000006b483045022100b4d4de4c10bec380a9f07019d5232a9af9f0c2321e5efcf33f5326a60378144502203e1ab2ddaac8afade132832e715f055f956d3e730b9d035a4e99ec9dfdc7acfd012103c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84ffffffff02102700000000000017a9142bb013c3e4beb08421dedcf815cb65a5c388178b87508a0e00000000001976a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac00000000"
    assert signed_fund_transaction.json() == {'hex': '0200000001ec312e92d8387b15f6238d4918344b62ab147d7f3844dc81e653776fe8b84ef3010000006b483045022100b4d4de4c10bec380a9f07019d5232a9af9f0c2321e5efcf33f5326a60378144502203e1ab2ddaac8afade132832e715f055f956d3e730b9d035a4e99ec9dfdc7acfd012103c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84ffffffff02102700000000000017a9142bb013c3e4beb08421dedcf815cb65a5c388178b87508a0e00000000001976a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac00000000', 'txid': '7e52333d38b7571807caac7971c925dd2c007dbf34a6c46138ff3d0213281d60', 'hash': '7e52333d38b7571807caac7971c925dd2c007dbf34a6c46138ff3d0213281d60', 'size': 224, 'vsize': 224, 'version': 2, 'locktime': 0, 'vin': [{'txid': 'f34eb8e86f7753e681dc44387f7d14ab624b3418498d23f6157b38d8922e31ec', 'vout': 1, 'scriptSig': {'asm': '3045022100b4d4de4c10bec380a9f07019d5232a9af9f0c2321e5efcf33f5326a60378144502203e1ab2ddaac8afade132832e715f055f956d3e730b9d035a4e99ec9dfdc7acfd01 03c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84', 'hex': '483045022100b4d4de4c10bec380a9f07019d5232a9af9f0c2321e5efcf33f5326a60378144502203e1ab2ddaac8afade132832e715f055f956d3e730b9d035a4e99ec9dfdc7acfd012103c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84'}, 'sequence': '4294967295'}], 'vout': [{'value': '0.00010000', 'n': 0, 'scriptPubKey': {'asm': 'OP_HASH160 2bb013c3e4beb08421dedcf815cb65a5c388178b OP_EQUAL', 'hex': 'a9142bb013c3e4beb08421dedcf815cb65a5c388178b87', 'type': 'p2sh', 'address': '2MwEDybGC34949zgzWX4M9FHmE3crDSUydP'}}, {'value': '0.00952912', 'n': 1, 'scriptPubKey': {'asm': 'OP_DUP OP_HASH160 64a8390b0b1685fcbf2d4b457118dc8da92d5534 OP_EQUALVERIFY OP_CHECKSIG', 'hex': '76a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac', 'type': 'p2pkh', 'address': 'mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q'}}]}
    assert signed_fund_transaction.type() == "bitcoin_fund_signed"


def test_bitcoin_claim_transaction():

    unsigned_claim_transaction = ClaimTransaction(
        version=2, network=network
    )

    unsigned_claim_transaction.build_transaction(
        transaction_id=transaction_id,
        wallet=recipient_wallet,
        amount=10_000
    )

    assert unsigned_claim_transaction.fee() == 576
    assert unsigned_claim_transaction.hash() == "a179dd565ea771869b0dfe1fd90c629f379cce9bd31d8814137fcb48fdd43b7e"
    assert unsigned_claim_transaction.raw() == "0200000001ec312e92d8387b15f6238d4918344b62ab147d7f3844dc81e653776fe8b84ef30000000000ffffffff01d0240000000000001976a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac00000000"
    assert unsigned_claim_transaction.json() == {'hex': '0200000001ec312e92d8387b15f6238d4918344b62ab147d7f3844dc81e653776fe8b84ef30000000000ffffffff01d0240000000000001976a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac00000000', 'txid': 'a179dd565ea771869b0dfe1fd90c629f379cce9bd31d8814137fcb48fdd43b7e', 'hash': 'a179dd565ea771869b0dfe1fd90c629f379cce9bd31d8814137fcb48fdd43b7e', 'size': 85, 'vsize': 85, 'version': 2, 'locktime': 0, 'vin': [{'txid': 'f34eb8e86f7753e681dc44387f7d14ab624b3418498d23f6157b38d8922e31ec', 'vout': 0, 'scriptSig': {'asm': '', 'hex': ''}, 'sequence': '4294967295'}], 'vout': [{'value': '0.00009424', 'n': 0, 'scriptPubKey': {'asm': 'OP_DUP OP_HASH160 98f879fb7f8b4951dee9bc8a0327b792fbe332b8 OP_EQUALVERIFY OP_CHECKSIG', 'hex': '76a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac', 'type': 'p2pkh', 'address': 'muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB'}}]}
    assert unsigned_claim_transaction.type() == "bitcoin_claim_unsigned"
    assert unsigned_claim_transaction.unsigned_raw() == "eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMWVjMzEyZTkyZDgzODdiMTVmNjIzOGQ0OTE4MzQ0YjYyYWIxNDdkN2YzODQ0ZGM4MWU2NTM3NzZmZThiODRlZjMwMDAwMDAwMDAwZmZmZmZmZmYwMWQwMjQwMDAwMDAwMDAwMDAxOTc2YTkxNDk4Zjg3OWZiN2Y4YjQ5NTFkZWU5YmM4YTAzMjdiNzkyZmJlMzMyYjg4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsiYW1vdW50IjogMTAwMDAsICJuIjogMCwgInNjcmlwdCI6ICJhOTE0MmJiMDEzYzNlNGJlYjA4NDIxZGVkY2Y4MTVjYjY1YTVjMzg4MTc4Yjg3In0sICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX2NsYWltX3Vuc2lnbmVkIn0="

    signed_claim_transaction = unsigned_claim_transaction.sign(
        solver=ClaimSolver(
            private_key=recipient_wallet.private_key(),
            secret="Hello Meheret!",
            secret_hash=sha256("Hello Meheret!".encode()).hex(),
            recipient_address=recipient_wallet.address(),
            sender_address=sender_wallet.address(),
            sequence=1000
        )
    )

    assert signed_claim_transaction.fee() == 576
    assert signed_claim_transaction.hash() == "8f98079b6257d65abc2c1c1a14c3bff50a6be949e75a30c127b3a2c0618012e1"
    assert signed_claim_transaction.raw() == "0200000001ec312e92d8387b15f6238d4918344b62ab147d7f3844dc81e653776fe8b84ef300000000d9473044022060291b5a87474f775dda5c244b21fc2716bfa09c4636ea4c707918c9f759374e02201ef5e768af10d01a1031294e952f6a8ed5c0a75e23f58aee062a89fed2134af70121039213ebcaefdd3e109720c17867ce1bd6d076b0e65e3b6390e6e38548a65e76af0e48656c6c6f204d65686572657421514c5d63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac6702e803b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68ffffffff01d0240000000000001976a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac00000000"
    assert signed_claim_transaction.json() == {'hex': '0200000001ec312e92d8387b15f6238d4918344b62ab147d7f3844dc81e653776fe8b84ef300000000d9473044022060291b5a87474f775dda5c244b21fc2716bfa09c4636ea4c707918c9f759374e02201ef5e768af10d01a1031294e952f6a8ed5c0a75e23f58aee062a89fed2134af70121039213ebcaefdd3e109720c17867ce1bd6d076b0e65e3b6390e6e38548a65e76af0e48656c6c6f204d65686572657421514c5d63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac6702e803b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68ffffffff01d0240000000000001976a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac00000000', 'txid': '8f98079b6257d65abc2c1c1a14c3bff50a6be949e75a30c127b3a2c0618012e1', 'hash': '8f98079b6257d65abc2c1c1a14c3bff50a6be949e75a30c127b3a2c0618012e1', 'size': 302, 'vsize': 302, 'version': 2, 'locktime': 0, 'vin': [{'txid': 'f34eb8e86f7753e681dc44387f7d14ab624b3418498d23f6157b38d8922e31ec', 'vout': 0, 'scriptSig': {'asm': '3044022060291b5a87474f775dda5c244b21fc2716bfa09c4636ea4c707918c9f759374e02201ef5e768af10d01a1031294e952f6a8ed5c0a75e23f58aee062a89fed2134af701 039213ebcaefdd3e109720c17867ce1bd6d076b0e65e3b6390e6e38548a65e76af 48656c6c6f204d65686572657421 OP_1 63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac6702e803b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68', 'hex': '473044022060291b5a87474f775dda5c244b21fc2716bfa09c4636ea4c707918c9f759374e02201ef5e768af10d01a1031294e952f6a8ed5c0a75e23f58aee062a89fed2134af70121039213ebcaefdd3e109720c17867ce1bd6d076b0e65e3b6390e6e38548a65e76af0e48656c6c6f204d65686572657421514c5d63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac6702e803b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68'}, 'sequence': '4294967295'}], 'vout': [{'value': '0.00009424', 'n': 0, 'scriptPubKey': {'asm': 'OP_DUP OP_HASH160 98f879fb7f8b4951dee9bc8a0327b792fbe332b8 OP_EQUALVERIFY OP_CHECKSIG', 'hex': '76a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac', 'type': 'p2pkh', 'address': 'muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB'}}]}
    assert signed_claim_transaction.type() == "bitcoin_claim_signed"


def test_bitcoin_refund_transaction():

    unsigned_refund_transaction = RefundTransaction(
        version=2, network=network
    )

    unsigned_refund_transaction.build_transaction(
        transaction_id=transaction_id,
        wallet=sender_wallet,
        amount=10_000
    )

    assert unsigned_refund_transaction.fee() == 576
    assert unsigned_refund_transaction.hash() == "a2022290e62f4073bc642d6b45f92ec3686c6524d0ef3d67d9edfd5f7dab0ea1"
    assert unsigned_refund_transaction.raw() == "0200000001ec312e92d8387b15f6238d4918344b62ab147d7f3844dc81e653776fe8b84ef30000000000ffffffff01d0240000000000001976a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac00000000"
    assert unsigned_refund_transaction.json() == {'hex': '0200000001ec312e92d8387b15f6238d4918344b62ab147d7f3844dc81e653776fe8b84ef30000000000ffffffff01d0240000000000001976a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac00000000', 'txid': 'a2022290e62f4073bc642d6b45f92ec3686c6524d0ef3d67d9edfd5f7dab0ea1', 'hash': 'a2022290e62f4073bc642d6b45f92ec3686c6524d0ef3d67d9edfd5f7dab0ea1', 'size': 85, 'vsize': 85, 'version': 2, 'locktime': 0, 'vin': [{'txid': 'f34eb8e86f7753e681dc44387f7d14ab624b3418498d23f6157b38d8922e31ec', 'vout': 0, 'scriptSig': {'asm': '', 'hex': ''}, 'sequence': '4294967295'}], 'vout': [{'value': '0.00009424', 'n': 0, 'scriptPubKey': {'asm': 'OP_DUP OP_HASH160 64a8390b0b1685fcbf2d4b457118dc8da92d5534 OP_EQUALVERIFY OP_CHECKSIG', 'hex': '76a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac', 'type': 'p2pkh', 'address': 'mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q'}}]}
    assert unsigned_refund_transaction.type() == "bitcoin_refund_unsigned"
    assert unsigned_refund_transaction.unsigned_raw() == "eyJmZWUiOiA1NzYsICJyYXciOiAiMDIwMDAwMDAwMWVjMzEyZTkyZDgzODdiMTVmNjIzOGQ0OTE4MzQ0YjYyYWIxNDdkN2YzODQ0ZGM4MWU2NTM3NzZmZThiODRlZjMwMDAwMDAwMDAwZmZmZmZmZmYwMWQwMjQwMDAwMDAwMDAwMDAxOTc2YTkxNDY0YTgzOTBiMGIxNjg1ZmNiZjJkNGI0NTcxMThkYzhkYTkyZDU1MzQ4OGFjMDAwMDAwMDAiLCAib3V0cHV0cyI6IHsidmFsdWUiOiAxMDAwMCwgIm4iOiAwLCAic2NyaXB0X3B1YmtleSI6ICJhOTE0MmJiMDEzYzNlNGJlYjA4NDIxZGVkY2Y4MTVjYjY1YTVjMzg4MTc4Yjg3In0sICJuZXR3b3JrIjogInRlc3RuZXQiLCAidHlwZSI6ICJiaXRjb2luX3JlZnVuZF91bnNpZ25lZCJ9"

    signed_refund_transaction = unsigned_refund_transaction.sign(
        solver=RefundSolver(
            private_key=sender_wallet.private_key(),
            secret_hash=sha256("Hello Meheret!".encode()).hex(),
            recipient_address=recipient_wallet.address(),
            sender_address=sender_wallet.address(),
            sequence=1000
        )
    )

    assert signed_refund_transaction.fee() == 576
    assert signed_refund_transaction.hash() == "9b429fdff11ccb19e4642521fed4ae7d89129c49a08214f41e709bd3e2a0e4f5"
    assert signed_refund_transaction.raw() == "0200000001ec312e92d8387b15f6238d4918344b62ab147d7f3844dc81e653776fe8b84ef300000000ca47304402200b0fc3b3b891761e5cbee5bc1f3c6d7b0904c13475eef5b7965c9bfda1d08a2a02205ebdc72cb763a2e7f290787b8d7defd972b41a2b4dc1c499d69991f0e4506659012103c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84004c5d63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac6702e803b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68e803000001d0240000000000001976a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac00000000"
    assert signed_refund_transaction.json() == {'hex': '0200000001ec312e92d8387b15f6238d4918344b62ab147d7f3844dc81e653776fe8b84ef300000000ca47304402200b0fc3b3b891761e5cbee5bc1f3c6d7b0904c13475eef5b7965c9bfda1d08a2a02205ebdc72cb763a2e7f290787b8d7defd972b41a2b4dc1c499d69991f0e4506659012103c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84004c5d63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac6702e803b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68e803000001d0240000000000001976a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac00000000', 'txid': '9b429fdff11ccb19e4642521fed4ae7d89129c49a08214f41e709bd3e2a0e4f5', 'hash': '9b429fdff11ccb19e4642521fed4ae7d89129c49a08214f41e709bd3e2a0e4f5', 'size': 287, 'vsize': 287, 'version': 2, 'locktime': 0, 'vin': [{'txid': 'f34eb8e86f7753e681dc44387f7d14ab624b3418498d23f6157b38d8922e31ec', 'vout': 0, 'scriptSig': {'asm': '304402200b0fc3b3b891761e5cbee5bc1f3c6d7b0904c13475eef5b7965c9bfda1d08a2a02205ebdc72cb763a2e7f290787b8d7defd972b41a2b4dc1c499d69991f0e450665901 03c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84 OP_0 63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac6702e803b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68', 'hex': '47304402200b0fc3b3b891761e5cbee5bc1f3c6d7b0904c13475eef5b7965c9bfda1d08a2a02205ebdc72cb763a2e7f290787b8d7defd972b41a2b4dc1c499d69991f0e4506659012103c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84004c5d63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac6702e803b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68'}, 'sequence': '1000'}], 'vout': [{'value': '0.00009424', 'n': 0, 'scriptPubKey': {'asm': 'OP_DUP OP_HASH160 64a8390b0b1685fcbf2d4b457118dc8da92d5534 OP_EQUALVERIFY OP_CHECKSIG', 'hex': '76a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac', 'type': 'p2pkh', 'address': 'mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q'}}]}
    assert signed_refund_transaction.type() == "bitcoin_refund_signed"
