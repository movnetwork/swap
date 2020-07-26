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
            secret_hash=sha256("Hello Meheret!"),
            recipient_address=recipient_wallet.address(),
            sender_address=sender_wallet.address(),
            sequence=1000
        ),
        amount=10_000
    )

    assert unsigned_fund_transaction.fee() == 678
    assert unsigned_fund_transaction.hash() == "407d6e3a9146f6ac445590c0f126af53c08e14e34d28e8281ef6ec21452f56b4"
    assert unsigned_fund_transaction.raw() == "0200000001ec312e92d8387b15f6238d4918344b62ab147d7f3844dc81e653776fe8b84ef30100000000ffffffff02102700000000000017a914c5d32c6ac326c51ba9da21fa8064ac3bbd7e6bd787508a0e00000000001976a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac00000000"
    assert unsigned_fund_transaction.json() == {'hex': '0200000001ec312e92d8387b15f6238d4918344b62ab147d7f3844dc81e653776fe8b84ef30100000000ffffffff02102700000000000017a914c5d32c6ac326c51ba9da21fa8064ac3bbd7e6bd787508a0e00000000001976a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac00000000', 'txid': '407d6e3a9146f6ac445590c0f126af53c08e14e34d28e8281ef6ec21452f56b4', 'hash': '407d6e3a9146f6ac445590c0f126af53c08e14e34d28e8281ef6ec21452f56b4', 'size': 117, 'vsize': 117, 'version': 2, 'locktime': 0, 'vin': [{'txid': 'f34eb8e86f7753e681dc44387f7d14ab624b3418498d23f6157b38d8922e31ec', 'vout': 1, 'scriptSig': {'asm': '', 'hex': ''}, 'sequence': '4294967295'}], 'vout': [{'value': '0.00010000', 'n': 0, 'scriptPubKey': {'asm': 'OP_HASH160 c5d32c6ac326c51ba9da21fa8064ac3bbd7e6bd7 OP_EQUAL', 'hex': 'a914c5d32c6ac326c51ba9da21fa8064ac3bbd7e6bd787', 'type': 'p2sh', 'address': '2NBHE5fdVCLm98VkU8vakJyuteQMBNTKRcZ'}}, {'value': '0.00952912', 'n': 1, 'scriptPubKey': {'asm': 'OP_DUP OP_HASH160 64a8390b0b1685fcbf2d4b457118dc8da92d5534 OP_EQUALVERIFY OP_CHECKSIG', 'hex': '76a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac', 'type': 'p2pkh', 'address': 'mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q'}}]}
    assert unsigned_fund_transaction.type() == "bitcoin_fund_unsigned"
    assert unsigned_fund_transaction.unsigned_raw() == "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMWVjMzEyZTkyZDgzODdiMTVmNjIzOGQ0OTE4MzQ0YjYyYWIxNDdkN2YzODQ0ZGM4MWU2NTM3NzZmZThiODRlZjMwMTAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTRjNWQzMmM2YWMzMjZjNTFiYTlkYTIxZmE4MDY0YWMzYmJkN2U2YmQ3ODc1MDhhMGUwMDAwMDAwMDAwMTk3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiA5NjM1OTAsICJuIjogMSwgInNjcmlwdCI6ICI3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"

    signed_fund_transaction = unsigned_fund_transaction.sign(
        solver=FundSolver(
            private_key=sender_wallet.private_key()
        )
    )

    assert signed_fund_transaction.fee() == 678
    assert signed_fund_transaction.hash() == "df63936276dead080b467df409c0569175a2ecf4bbc5e11cef5eb5a54e70a6b4"
    assert signed_fund_transaction.raw() == "0200000001ec312e92d8387b15f6238d4918344b62ab147d7f3844dc81e653776fe8b84ef3010000006b48304502210085fa79c899143cc641aa22da33ea4cb4fbe1392dc28c1d1bfd2e5d22b1cfb77e022032b07a29a84a19ed8f8a1d248d557cc61ae5fb67fe3c972fd864c3c62bc3b888012103c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84ffffffff02102700000000000017a914c5d32c6ac326c51ba9da21fa8064ac3bbd7e6bd787508a0e00000000001976a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac00000000"
    assert signed_fund_transaction.json() == {'hex': '0200000001ec312e92d8387b15f6238d4918344b62ab147d7f3844dc81e653776fe8b84ef3010000006b48304502210085fa79c899143cc641aa22da33ea4cb4fbe1392dc28c1d1bfd2e5d22b1cfb77e022032b07a29a84a19ed8f8a1d248d557cc61ae5fb67fe3c972fd864c3c62bc3b888012103c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84ffffffff02102700000000000017a914c5d32c6ac326c51ba9da21fa8064ac3bbd7e6bd787508a0e00000000001976a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac00000000', 'txid': 'df63936276dead080b467df409c0569175a2ecf4bbc5e11cef5eb5a54e70a6b4', 'hash': 'df63936276dead080b467df409c0569175a2ecf4bbc5e11cef5eb5a54e70a6b4', 'size': 224, 'vsize': 224, 'version': 2, 'locktime': 0, 'vin': [{'txid': 'f34eb8e86f7753e681dc44387f7d14ab624b3418498d23f6157b38d8922e31ec', 'vout': 1, 'scriptSig': {'asm': '304502210085fa79c899143cc641aa22da33ea4cb4fbe1392dc28c1d1bfd2e5d22b1cfb77e022032b07a29a84a19ed8f8a1d248d557cc61ae5fb67fe3c972fd864c3c62bc3b88801 03c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84', 'hex': '48304502210085fa79c899143cc641aa22da33ea4cb4fbe1392dc28c1d1bfd2e5d22b1cfb77e022032b07a29a84a19ed8f8a1d248d557cc61ae5fb67fe3c972fd864c3c62bc3b888012103c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84'}, 'sequence': '4294967295'}], 'vout': [{'value': '0.00010000', 'n': 0, 'scriptPubKey': {'asm': 'OP_HASH160 c5d32c6ac326c51ba9da21fa8064ac3bbd7e6bd7 OP_EQUAL', 'hex': 'a914c5d32c6ac326c51ba9da21fa8064ac3bbd7e6bd787', 'type': 'p2sh', 'address': '2NBHE5fdVCLm98VkU8vakJyuteQMBNTKRcZ'}}, {'value': '0.00952912', 'n': 1, 'scriptPubKey': {'asm': 'OP_DUP OP_HASH160 64a8390b0b1685fcbf2d4b457118dc8da92d5534 OP_EQUALVERIFY OP_CHECKSIG', 'hex': '76a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac', 'type': 'p2pkh', 'address': 'mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q'}}]}
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
            secret_hash=sha256("Hello Meheret!"),
            recipient_address=recipient_wallet.address(),
            sender_address=sender_wallet.address(),
            sequence=1000
        )
    )

    assert signed_claim_transaction.fee() == 576
    assert signed_claim_transaction.hash() == "5235dba12bc257f0a6b76129b4e2ee6621cdb906c76acb88fc0986731f957bad"
    assert signed_claim_transaction.raw() == "0200000001ec312e92d8387b15f6238d4918344b62ab147d7f3844dc81e653776fe8b84ef300000000d9473044022041aed3386ab426810732f700a8f9f2a2749d0e3faa9c2500452f83f3205eac42022072708301b4726b6b7896fff617918a02986f83ec06c6758c71f0830c924d287d0121039213ebcaefdd3e109720c17867ce1bd6d076b0e65e3b6390e6e38548a65e76af0e48656c6c6f204d65686572657421514c5d63aa204683a21fd5ce2425adc90a3674b6d8d3d418935540fc3a71c6ec3cb249925dd38876a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac6702e803b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68ffffffff01d0240000000000001976a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac00000000"
    assert signed_claim_transaction.json() == {'hex': '0200000001ec312e92d8387b15f6238d4918344b62ab147d7f3844dc81e653776fe8b84ef300000000d9473044022041aed3386ab426810732f700a8f9f2a2749d0e3faa9c2500452f83f3205eac42022072708301b4726b6b7896fff617918a02986f83ec06c6758c71f0830c924d287d0121039213ebcaefdd3e109720c17867ce1bd6d076b0e65e3b6390e6e38548a65e76af0e48656c6c6f204d65686572657421514c5d63aa204683a21fd5ce2425adc90a3674b6d8d3d418935540fc3a71c6ec3cb249925dd38876a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac6702e803b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68ffffffff01d0240000000000001976a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac00000000', 'txid': '5235dba12bc257f0a6b76129b4e2ee6621cdb906c76acb88fc0986731f957bad', 'hash': '5235dba12bc257f0a6b76129b4e2ee6621cdb906c76acb88fc0986731f957bad', 'size': 302, 'vsize': 302, 'version': 2, 'locktime': 0, 'vin': [{'txid': 'f34eb8e86f7753e681dc44387f7d14ab624b3418498d23f6157b38d8922e31ec', 'vout': 0, 'scriptSig': {'asm': '3044022041aed3386ab426810732f700a8f9f2a2749d0e3faa9c2500452f83f3205eac42022072708301b4726b6b7896fff617918a02986f83ec06c6758c71f0830c924d287d01 039213ebcaefdd3e109720c17867ce1bd6d076b0e65e3b6390e6e38548a65e76af 48656c6c6f204d65686572657421 OP_1 63aa204683a21fd5ce2425adc90a3674b6d8d3d418935540fc3a71c6ec3cb249925dd38876a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac6702e803b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68', 'hex': '473044022041aed3386ab426810732f700a8f9f2a2749d0e3faa9c2500452f83f3205eac42022072708301b4726b6b7896fff617918a02986f83ec06c6758c71f0830c924d287d0121039213ebcaefdd3e109720c17867ce1bd6d076b0e65e3b6390e6e38548a65e76af0e48656c6c6f204d65686572657421514c5d63aa204683a21fd5ce2425adc90a3674b6d8d3d418935540fc3a71c6ec3cb249925dd38876a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac6702e803b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68'}, 'sequence': '4294967295'}], 'vout': [{'value': '0.00009424', 'n': 0, 'scriptPubKey': {'asm': 'OP_DUP OP_HASH160 98f879fb7f8b4951dee9bc8a0327b792fbe332b8 OP_EQUALVERIFY OP_CHECKSIG', 'hex': '76a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac', 'type': 'p2pkh', 'address': 'muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB'}}]}
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
            secret_hash=sha256("Hello Meheret!"),
            recipient_address=recipient_wallet.address(),
            sender_address=sender_wallet.address(),
            sequence=1000
        )
    )

    assert signed_refund_transaction.fee() == 576
    assert signed_refund_transaction.hash() == "429f99906296e801c2bb0423339208df552463ae5c04d8f13d302281541b0e5b"
    assert signed_refund_transaction.raw() == "0200000001ec312e92d8387b15f6238d4918344b62ab147d7f3844dc81e653776fe8b84ef300000000ca47304402203c73c35fe39cf0e030b47c98a7a52e2520ed8bf25d8b58d741968cd80746ac3902203a704cfcf9ea74e113994f25becfac474d0c6cd07169ebe4cb589e44d515bb45012103c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84004c5d63aa204683a21fd5ce2425adc90a3674b6d8d3d418935540fc3a71c6ec3cb249925dd38876a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac6702e803b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68e803000001d0240000000000001976a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac00000000"
    assert signed_refund_transaction.json() == {'hex': '0200000001ec312e92d8387b15f6238d4918344b62ab147d7f3844dc81e653776fe8b84ef300000000ca47304402203c73c35fe39cf0e030b47c98a7a52e2520ed8bf25d8b58d741968cd80746ac3902203a704cfcf9ea74e113994f25becfac474d0c6cd07169ebe4cb589e44d515bb45012103c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84004c5d63aa204683a21fd5ce2425adc90a3674b6d8d3d418935540fc3a71c6ec3cb249925dd38876a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac6702e803b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68e803000001d0240000000000001976a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac00000000', 'txid': '429f99906296e801c2bb0423339208df552463ae5c04d8f13d302281541b0e5b', 'hash': '429f99906296e801c2bb0423339208df552463ae5c04d8f13d302281541b0e5b', 'size': 287, 'vsize': 287, 'version': 2, 'locktime': 0, 'vin': [{'txid': 'f34eb8e86f7753e681dc44387f7d14ab624b3418498d23f6157b38d8922e31ec', 'vout': 0, 'scriptSig': {'asm': '304402203c73c35fe39cf0e030b47c98a7a52e2520ed8bf25d8b58d741968cd80746ac3902203a704cfcf9ea74e113994f25becfac474d0c6cd07169ebe4cb589e44d515bb4501 03c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84 OP_0 63aa204683a21fd5ce2425adc90a3674b6d8d3d418935540fc3a71c6ec3cb249925dd38876a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac6702e803b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68', 'hex': '47304402203c73c35fe39cf0e030b47c98a7a52e2520ed8bf25d8b58d741968cd80746ac3902203a704cfcf9ea74e113994f25becfac474d0c6cd07169ebe4cb589e44d515bb45012103c56a6005d4a8892d28cc3f7265e5685b548627d59108973e474c4e26f69a4c84004c5d63aa204683a21fd5ce2425adc90a3674b6d8d3d418935540fc3a71c6ec3cb249925dd38876a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac6702e803b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68'}, 'sequence': '1000'}], 'vout': [{'value': '0.00009424', 'n': 0, 'scriptPubKey': {'asm': 'OP_DUP OP_HASH160 64a8390b0b1685fcbf2d4b457118dc8da92d5534 OP_EQUALVERIFY OP_CHECKSIG', 'hex': '76a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac', 'type': 'p2pkh', 'address': 'mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q'}}]}
    assert signed_refund_transaction.type() == "bitcoin_refund_signed"
