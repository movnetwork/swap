#!/usr/bin/env python3

from shuttle.providers.bytom.wallet import Wallet
from shuttle.providers.bytom.htlc import HTLC
from shuttle.providers.bytom.transaction import (
    FundTransaction, ClaimTransaction, RefundTransaction
)
from shuttle.providers.bytom.solver import (
    FundSolver, ClaimSolver, RefundSolver
)
from shuttle.utils import sha256

import pytest


network = "mainnet"
sender_wallet = Wallet(network=network).from_mnemonic(
    mnemonic="hint excuse upgrade sleep easily deputy erase cluster section other ugly limit"
).from_guid(
    guid="571784a8-0945-4d78-b973-aac4b09d6439"
)
recipient_wallet = Wallet(network=network).from_mnemonic(
    mnemonic="indicate warm sock mistake code spot acid ribbon sing over taxi toast"
).from_guid(
    guid="f0ed6ddd-9d6b-49fd-8866-a52d1083a13b"
)
transaction_id = "049d4c26bb15885572c16e0eefac5b2f4d0fde50eaf90f002272d39507ff315b"
asset = "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
amount = 10_000


def test_bytom_fund_transaction():

    unsigned_fund_transaction = FundTransaction(network=network)

    unsigned_fund_transaction.build_transaction(
        wallet=sender_wallet,
        htlc=HTLC(network=network).init(
            secret_hash=sha256("Hello Meheret!".encode()).hex(),
            recipient_public=recipient_wallet.public_key(),
            sender_public=sender_wallet.public_key(),
            sequence=1000
        ),
        amount=amount,
        asset=asset
    )

    assert unsigned_fund_transaction.type() == "bytom_fund_unsigned"
    assert unsigned_fund_transaction.unsigned_raw() == "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiNTcxNzg0YTgtMDk0NS00ZDc4LWI5NzMtYWFjNGIwOWQ2NDM5IiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbImI1NTgxODRiZDJjNWNmMWQ3YWY5NTIyN2Y4OTk2Nzc3ZDQ2ZDQxMDY5YTgyZjc4YzExYzYxODBhNTMyZWViODUiXSwgInB1YmxpY19rZXkiOiAiM2UwYTM3N2FlNGFmYTAzMWQ0NTUxNTk5ZDliYjdkNWIyN2Y0NzM2ZDc3Zjc4Y2FjNGQ0NzZmMGZmYmE1YWUzZSIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgImhhc2giOiAiODljOTU0NDA0YmRiM2U2MTIzZWQ4YTQxM2ZlM2JkNTI2YmY3YjU1MjkzNmQ4MGZkOGMzN2MyZDdlYWU2ZDBjMCIsICJyYXciOiAiMDcwMTAwMDEwMTYwMDE1ZTAyZTBiMWFkMjEwNzIyMmNmYzEzYWI2YzMzNjVkMzY2YjVkMTNiMTFlNmRjN2UxZTBjYzRhZTU2NzZjZGVlNDRmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjA5ODg4ZDgwMzAxMDExNjAwMTQ4ODdlZTY2ZDg0YTgyZjJkODY4MjRhNDViYjUxZmRlYTAzYzkyZjQ5MjIwMTIwM2UwYTM3N2FlNGFmYTAzMWQ0NTUxNTk5ZDliYjdkNWIyN2Y0NzM2ZDc3Zjc4Y2FjNGQ0NzZmMGZmYmE1YWUzZTAyMDE0NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDEyMjAwMjBhNWFkZGI3ZWI1NjQ5ZDEwMDMxMzA0ZWNlNzJkOWNjYzlkYzQyNGFiY2RhODk1ZDkwNGEzMDk3Mjc0MjRlNDBlMDAwMTNkZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmUwOWRhNWQzMDMwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkwMCIsICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieXRvbV9mdW5kX3Vuc2lnbmVkIn0="
    assert unsigned_fund_transaction.signatures() == []

    signed_fund_transaction = unsigned_fund_transaction.sign(
        solver=FundSolver(
            xprivate_key=sender_wallet.xprivate_key()
        )
    )

    assert unsigned_fund_transaction.fee() == signed_fund_transaction.fee() == 10000000
    assert unsigned_fund_transaction.hash() == signed_fund_transaction.hash() == \
           "89c954404bdb3e6123ed8a413fe3bd526bf7b552936d80fd8c37c2d7eae6d0c0"
    assert unsigned_fund_transaction.raw() == signed_fund_transaction.raw() == \
           "070100010160015e02e0b1ad2107222cfc13ab6c3365d366b5d13b11e6dc7e1e0cc4ae5676cdee44fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff09888d8030101160014887ee66d84a82f2d86824a45bb51fdea03c92f492201203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e020146ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff904e01220020a5addb7eb5649d10031304ece72d9ccc9dc424abcda895d904a309727424e40e00013dffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe09da5d30301160014887ee66d84a82f2d86824a45bb51fdea03c92f4900"
    # assert unsigned_fund_transaction.json() == signed_fund_transaction.json() == \
    #      {'tx_id': '89c954404bdb3e6123ed8a413fe3bd526bf7b552936d80fd8c37c2d7eae6d0c0', 'version': 1, 'size': 275, 'time_range': 0, 'inputs': [{'type': 'spend', 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'asset_definition': {}, 'amount': 989990000, 'control_program': '0014887ee66d84a82f2d86824a45bb51fdea03c92f49', 'address': 'bm1q3plwvmvy4qhjmp5zffzmk50aagpujt6f5je85p', 'spent_output_id': '94f85b2b634c4d42bfc2ca883e74145a508f482dfc10adb407be59df3069aff7', 'input_id': '8a3b64f6cbf76f7fab17d53dd17ba2fdd4402e143b0384a62e3a371f54f77681', 'witness_arguments': ['3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e'], 'sign_data': 'b558184bd2c5cf1d7af95227f8996777d46d41069a82f78c11c6180a532eeb85'}], 'outputs': [{'type': 'control', 'id': '72f09f149c9c8c9d1ee8122472a8b0bd2e0c897d51f21daa7480428f1b61fc3c', 'position': 0, 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'asset_definition': {}, 'amount': 10000, 'control_program': '0020a5addb7eb5649d10031304ece72d9ccc9dc424abcda895d904a309727424e40e', 'address': 'bm1q5kkakl44vjw3qqcnqnkwwtvuejwugf9tek5ftkgy5vyhyapyus8qgcttcs'}, {'type': 'control', 'id': 'f95b95b531da409f4d80e959ba9351d592b0bcc3e6b0f79cfaea03143c520ed9', 'position': 1, 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'asset_definition': {}, 'amount': 979980000, 'control_program': '0014887ee66d84a82f2d86824a45bb51fdea03c92f49', 'address': 'bm1q3plwvmvy4qhjmp5zffzmk50aagpujt6f5je85p'}], 'fee': 10000000}
    assert unsigned_fund_transaction.unsigned_datas() == signed_fund_transaction.unsigned_datas() == \
        [{'datas': ['b558184bd2c5cf1d7af95227f8996777d46d41069a82f78c11c6180a532eeb85'], 'public_key': '3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e', 'network': 'mainnet', 'path': 'm/44/153/1/0/1'}]

    assert signed_fund_transaction.type() == "bytom_fund_signed"
    assert signed_fund_transaction.signatures() == [['e0af0886e126924fa1637314e38669512d2759e60b6cf69699616d8da5b0a316b7f662fed558c8adc65f288e937fc1e273d23587fbaea62994d1ad1fa795f103']]


def test_bytom_claim_transaction():

    unsigned_claim_transaction = ClaimTransaction(network=network)

    unsigned_claim_transaction.build_transaction(
        transaction_id=transaction_id,
        wallet=recipient_wallet,
        amount=amount,
        asset=asset
    )

    assert unsigned_claim_transaction.type() == "bytom_claim_unsigned"
    assert unsigned_claim_transaction.unsigned_raw() != "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbIjgzNGRkZjFkNjk3MmJlNzlhODhjYmVlNTc0YjQ1MmI1ZGRmZGFlZmYwZjg0OWJhNDFlMTk2OGZhOGQ4MjBlYWIiXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBbIjcyZGY2N2U5OWY3ZTI0OWM2YjJmN2JjNzA4MTgzODcyM2ExNDJlMWIzY2Y5YmIxZDRkODIzNTE5MDYwMTljMGYiXSwgInB1YmxpY19rZXkiOiAiNjkyOTdlOWI3NWVjODhhNGNhN2YwYzdhMWJiNjFkNjRlYTkzOTFiMTRhOTAyY2RhNDg1ODBmZTNlMTJhODJhYiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzEvMTIifV0sICJoYXNoIjogImQ1NTUwZGQxM2IxMGRhOTdiN2NkMjgyM2E2YTdjYmRlODgyYmQwMWI0MThjZjJjZDkyZmRjMjA3MzA5MDM3NDkiLCAicmF3IjogIjA3MDEwMDAyMDE2OTAxNjcwMmUwYjFhZDIxMDcyMjJjZmMxM2FiNmMzMzY1ZDM2NmI1ZDEzYjExZTZkYzdlMWUwY2M0YWU1Njc2Y2RlZTQ0ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjkwNGUwMDAxMjIwMDIwYTVhZGRiN2ViNTY0OWQxMDAzMTMwNGVjZTcyZDljY2M5ZGM0MjRhYmNkYTg5NWQ5MDRhMzA5NzI3NDI0ZTQwZTAxMDAwMTVmMDE1ZDdmMmQ3ZWNlYzNmNjFkMzBkMGIyOTY4OTczYTNhYzg0NDhmMDU5OWVhMjBkY2U4ODNiNDhjOTAzYzRkNmU4N2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmYzBmMmZkMTYwMDAxMTYwMDE0MmI1ZDExMGE4OWQxOTNlYThmMmYxZTU1M2E4OTIwODQ5YTU4ZTY4OTIyMDEyMDY5Mjk3ZTliNzVlYzg4YTRjYTdmMGM3YTFiYjYxZDY0ZWE5MzkxYjE0YTkwMmNkYTQ4NTgwZmUzZTEyYTgyYWIwMjAxM2FmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOTA0ZTAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTAwMDEzY2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjMGM1OWIxMjAxMTYwMDE0MmI1ZDExMGE4OWQxOTNlYThmMmYxZTU1M2E4OTIwODQ5YTU4ZTY4OTAwIiwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJzaWduYXR1cmVzIjogW10sICJ0eXBlIjogImJ5dG9tX2NsYWltX3Vuc2lnbmVkIn0="
    assert unsigned_claim_transaction.signatures() == []

    signed_claim_transaction = unsigned_claim_transaction.sign(
        solver=ClaimSolver(
            xprivate_key=recipient_wallet.xprivate_key(),
            secret="Hello Meheret!",
            secret_hash=sha256("Hello Meheret!".encode()).hex(),
            recipient_public=recipient_wallet.public_key(),
            sender_public=sender_wallet.public_key(),
            sequence=1000
        )
    )

    assert unsigned_claim_transaction.fee() == signed_claim_transaction.fee() == 10000000
    assert unsigned_claim_transaction.hash() == signed_claim_transaction.hash() != \
        "d5550dd13b10da97b7cd2823a6a7cbde882bd01b418cf2cd92fdc20730903749"
    assert unsigned_claim_transaction.raw() == signed_claim_transaction.raw() != \
        "070100020169016702e0b1ad2107222cfc13ab6c3365d366b5d13b11e6dc7e1e0cc4ae5676cdee44ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff904e0001220020a5addb7eb5649d10031304ece72d9ccc9dc424abcda895d904a309727424e40e0100015f015d7f2d7ecec3f61d30d0b2968973a3ac8448f0599ea20dce883b48c903c4d6e87fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffc0f2fd1600011600142b5d110a89d193ea8f2f1e553a8920849a58e68922012069297e9b75ec88a4ca7f0c7a1bb61d64ea9391b14a902cda48580fe3e12a82ab02013affffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff904e011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a00013cffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffc0c59b12011600142b5d110a89d193ea8f2f1e553a8920849a58e68900"
    # assert unsigned_claim_transaction.json() == signed_claim_transaction.json() == \
    #     {'tx_id': 'd5550dd13b10da97b7cd2823a6a7cbde882bd01b418cf2cd92fdc20730903749', 'version': 1, 'size': 370, 'time_range': 0, 'inputs': [{'type': 'spend', 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'asset_definition': {}, 'amount': 10000, 'control_program': '0020a5addb7eb5649d10031304ece72d9ccc9dc424abcda895d904a309727424e40e', 'address': 'bm1q5kkakl44vjw3qqcnqnkwwtvuejwugf9tek5ftkgy5vyhyapyus8qgcttcs', 'spent_output_id': '98a553b8cb08b8f6e0ded3c88a18841952d8cad7afdea41206881c5fa7a03548', 'input_id': '75565b5d1ff36b7898046d210ce53dbdff61322f4ed1e0e2a8943a99edb5b6b0', 'witness_arguments': None, 'sign_data': '834ddf1d6972be79a88cbee574b452b5ddfdaeff0f849ba41e1968fa8d820eab'}, {'type': 'spend', 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'asset_definition': {}, 'amount': 48200000, 'control_program': '00142b5d110a89d193ea8f2f1e553a8920849a58e689', 'address': 'bm1q9dw3zz5f6xf74re0re2n4zfqsjd93e5f9l4jxl', 'spent_output_id': '7e86b3f635595de17686c6d8d9d4f0281239d0db6af0bf0eaca763c46c2d455b', 'input_id': '5c49cf1f42e72aa418cd143628fcd321557fdda52da5249eb13cb2c57eb8d76e', 'witness_arguments': ['69297e9b75ec88a4ca7f0c7a1bb61d64ea9391b14a902cda48580fe3e12a82ab'], 'sign_data': '72df67e99f7e249c6b2f7bc7081838723a142e1b3cf9bb1d4d82351906019c0f'}], 'outputs': [{'type': 'control', 'id': 'a274d332fa3691ea34529d3f01949dd9bbc954978d6ea904916ea9ab5c3f17e7', 'position': 0, 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'asset_definition': {}, 'amount': 10000, 'control_program': '00142cda4f99ea8112e6fa61cdd26157ed6dc408332a', 'address': 'bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7'}, {'type': 'control', 'id': '0ce43636740fa0c9939b3dd1ad64afe9669c1af6b3cf7538a035bfe7aacd94e1', 'position': 1, 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'asset_definition': {}, 'amount': 38200000, 'control_program': '00142b5d110a89d193ea8f2f1e553a8920849a58e689', 'address': 'bm1q9dw3zz5f6xf74re0re2n4zfqsjd93e5f9l4jxl'}], 'fee': 10000000}
    assert unsigned_claim_transaction.unsigned_datas() == signed_claim_transaction.unsigned_datas() != \
        [{'datas': ['834ddf1d6972be79a88cbee574b452b5ddfdaeff0f849ba41e1968fa8d820eab'], 'network': 'mainnet', 'path': None}, {'datas': ['72df67e99f7e249c6b2f7bc7081838723a142e1b3cf9bb1d4d82351906019c0f'], 'public_key': '69297e9b75ec88a4ca7f0c7a1bb61d64ea9391b14a902cda48580fe3e12a82ab', 'network': 'mainnet', 'path': 'm/44/153/1/1/12'}]

    assert signed_claim_transaction.type() == "bytom_claim_signed"
    assert signed_claim_transaction.signatures() != [['48656c6c6f204d65686572657421', 'd1161ad0379968958bbbbfd84e46910269f95c8d1dacb1bb362494439d71ab91113c237631936b1a10d987e879a14706f7117779c21b8a3792b9bfad37f9dc02', '00', '02e803203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e2091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0'], ['ea93bd2fe334088e139156e843d828992a5dddc7e85d16eb2b711b86368b5cb61a4ba8428c89674f71e993c451e2bfa87cbb257592adfae512e527d26f6cc60c']]


def test_bytom_refund_transaction():

    unsigned_refund_transaction = RefundTransaction(network=network)

    unsigned_refund_transaction.build_transaction(
        transaction_id=transaction_id,
        wallet=sender_wallet,
        amount=amount,
        asset=asset
    )

    assert unsigned_refund_transaction.type() == "bytom_refund_unsigned"
    assert unsigned_refund_transaction.unsigned_raw() == "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiNTcxNzg0YTgtMDk0NS00ZDc4LWI5NzMtYWFjNGIwOWQ2NDM5IiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbIjZkNzk3OTEyMDk4YTFhNDgyM2ViMzAxMDgwMjgyNjA1NjEyODI1MTY5N2Q1YWNjNjViM2M3MzhiN2ZkZDU3MGQiXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBbIjliNmNlMjM5MjQ1YzVkMjRjZGE5ZTBmYmQ1M2Q0ZWI1YzRhOTJhMDVjZDBlZjkwNmRiY2M0YzNkYzBkZDMxOTAiXSwgInB1YmxpY19rZXkiOiAiM2UwYTM3N2FlNGFmYTAzMWQ0NTUxNTk5ZDliYjdkNWIyN2Y0NzM2ZDc3Zjc4Y2FjNGQ0NzZmMGZmYmE1YWUzZSIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgImhhc2giOiAiYjM4MWMxYmE1YmY1MzA5Y2Y1MTljNTIwMjZhZDBhMjQ0ODA5N2UwM2YwMzdlY2EyNzllOGRiODAxNDYxYmYwYyIsICJyYXciOiAiMDcwMTAwMDIwMTY5MDE2NzAyZTBiMWFkMjEwNzIyMmNmYzEzYWI2YzMzNjVkMzY2YjVkMTNiMTFlNmRjN2UxZTBjYzRhZTU2NzZjZGVlNDRmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOTA0ZTAwMDEyMjAwMjBhNWFkZGI3ZWI1NjQ5ZDEwMDMxMzA0ZWNlNzJkOWNjYzlkYzQyNGFiY2RhODk1ZDkwNGEzMDk3Mjc0MjRlNDBlMDEwMDAxNjAwMTVlMDJlMGIxYWQyMTA3MjIyY2ZjMTNhYjZjMzM2NWQzNjZiNWQxM2IxMWU2ZGM3ZTFlMGNjNGFlNTY3NmNkZWU0NGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmMDk4ODhkODAzMDEwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkyMjAxMjAzZTBhMzc3YWU0YWZhMDMxZDQ1NTE1OTlkOWJiN2Q1YjI3ZjQ3MzZkNzdmNzhjYWM0ZDQ3NmYwZmZiYTVhZTNlMDIwMTNhZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjkwNGUwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkwMDAxM2RmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjBlYmE1ZDMwMzAxMTYwMDE0ODg3ZWU2NmQ4NGE4MmYyZDg2ODI0YTQ1YmI1MWZkZWEwM2M5MmY0OTAwIiwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX3JlZnVuZF91bnNpZ25lZCJ9"
    assert unsigned_refund_transaction.signatures() == []

    signed_refund_transaction = unsigned_refund_transaction.sign(
        solver=RefundSolver(
            xprivate_key=sender_wallet.xprivate_key(),
            secret_hash=sha256("Hello Meheret!".encode()).hex(),
            recipient_public=recipient_wallet.public_key(),
            sender_public=sender_wallet.public_key(),
            sequence=1000
        )
    )

    assert unsigned_refund_transaction.fee() == signed_refund_transaction.fee() == 10000000
    assert unsigned_refund_transaction.hash() == signed_refund_transaction.hash() == \
           "b381c1ba5bf5309cf519c52026ad0a2448097e03f037eca279e8db801461bf0c"
    assert unsigned_refund_transaction.raw() == signed_refund_transaction.raw() == \
           "070100020169016702e0b1ad2107222cfc13ab6c3365d366b5d13b11e6dc7e1e0cc4ae5676cdee44ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff904e0001220020a5addb7eb5649d10031304ece72d9ccc9dc424abcda895d904a309727424e40e01000160015e02e0b1ad2107222cfc13ab6c3365d366b5d13b11e6dc7e1e0cc4ae5676cdee44fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff09888d8030101160014887ee66d84a82f2d86824a45bb51fdea03c92f492201203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e02013affffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff904e01160014887ee66d84a82f2d86824a45bb51fdea03c92f4900013dfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff0eba5d30301160014887ee66d84a82f2d86824a45bb51fdea03c92f4900"
    # assert unsigned_refund_transaction.json() == signed_refund_transaction.json() == \
    #        {'tx_id': 'b381c1ba5bf5309cf519c52026ad0a2448097e03f037eca279e8db801461bf0c', 'version': 1, 'size': 372, 'time_range': 0, 'inputs': [{'type': 'spend', 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'asset_definition': {}, 'amount': 10000, 'control_program': '0020a5addb7eb5649d10031304ece72d9ccc9dc424abcda895d904a309727424e40e', 'address': 'bm1q5kkakl44vjw3qqcnqnkwwtvuejwugf9tek5ftkgy5vyhyapyus8qgcttcs', 'spent_output_id': '98a553b8cb08b8f6e0ded3c88a18841952d8cad7afdea41206881c5fa7a03548', 'input_id': '75565b5d1ff36b7898046d210ce53dbdff61322f4ed1e0e2a8943a99edb5b6b0', 'witness_arguments': None, 'sign_data': '6d797912098a1a4823eb3010802826056128251697d5acc65b3c738b7fdd570d'}, {'type': 'spend', 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'asset_definition': {}, 'amount': 989990000, 'control_program': '0014887ee66d84a82f2d86824a45bb51fdea03c92f49', 'address': 'bm1q3plwvmvy4qhjmp5zffzmk50aagpujt6f5je85p', 'spent_output_id': '94f85b2b634c4d42bfc2ca883e74145a508f482dfc10adb407be59df3069aff7', 'input_id': '8a3b64f6cbf76f7fab17d53dd17ba2fdd4402e143b0384a62e3a371f54f77681', 'witness_arguments': ['3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e'], 'sign_data': '9b6ce239245c5d24cda9e0fbd53d4eb5c4a92a05cd0ef906dbcc4c3dc0dd3190'}], 'outputs': [{'type': 'control', 'id': '08e033e3602e1d45f888ab9f1507582781215ec9c87df78c98b6ce13ffff4392', 'position': 0, 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'asset_definition': {}, 'amount': 10000, 'control_program': '0014887ee66d84a82f2d86824a45bb51fdea03c92f49', 'address': 'bm1q3plwvmvy4qhjmp5zffzmk50aagpujt6f5je85p'}, {'type': 'control', 'id': 'd70a580cf71dfe9caef032f670df515fb8d4155c881eaed35deee07448d7548a', 'position': 1, 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'asset_definition': {}, 'amount': 979990000, 'control_program': '0014887ee66d84a82f2d86824a45bb51fdea03c92f49', 'address': 'bm1q3plwvmvy4qhjmp5zffzmk50aagpujt6f5je85p'}], 'fee': 10000000}
    assert unsigned_refund_transaction.unsigned_datas() == signed_refund_transaction.unsigned_datas() == \
           [{'datas': ['6d797912098a1a4823eb3010802826056128251697d5acc65b3c738b7fdd570d'], 'network': 'mainnet', 'path': None}, {'datas': ['9b6ce239245c5d24cda9e0fbd53d4eb5c4a92a05cd0ef906dbcc4c3dc0dd3190'], 'public_key': '3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e', 'network': 'mainnet', 'path': 'm/44/153/1/0/1'}]

    assert signed_refund_transaction.type() == "bytom_refund_signed"
    assert signed_refund_transaction.signatures() == [['96ebd6a2676f1e433535460ed00b0703cebfa5b2e7e70533bf929771b479301fbbc8f01633dbef71ede6d26f0b9723cc351c90d2f9723a7c6db9c4902f157c08', '01', '02e803203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e2091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0'], ['dde169c6d51cbff60f1c2eca6a531865578770fefae90e02d2b661400d5fbf17799c4f65174b4402fbe7a7d4d354fdcb742e49d5105a75236a82272cca6cab0a']]
