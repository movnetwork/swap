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
        amount=10_000,
        asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
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
        amount=10_000,
        asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
    )

    assert unsigned_claim_transaction.type() == "bytom_claim_unsigned"
    assert unsigned_claim_transaction.unsigned_raw() == "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbImRjOTdiYjAzYjU1ODE0MzUzYjBiODAyNmUxNTZiZjZhNTI5ZGJlYzcyOTA1NmI3MTIwNzkwY2JjNzcwMDIzYzUiXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBbImEwNmVlZWIzODZlYTkxNjZkYjMwMTM1YmQ0YjQ1Nzk1ZjE5OWQxZDNlODlmNjVhNzlkMTVlN2E1NmQ2ZmFmMmQiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgImhhc2giOiAiMjU1NGM2OTU0YjczNWIwOTJmNjRiOWFhM2QzMWQ3NDVmMTRhYmVlYTc1NWQ3NWY5Y2RmYzBlMjUzMWQ3NWYxYiIsICJyYXciOiAiMDcwMTAwMDIwMTY5MDE2NzAyZTBiMWFkMjEwNzIyMmNmYzEzYWI2YzMzNjVkMzY2YjVkMTNiMTFlNmRjN2UxZTBjYzRhZTU2NzZjZGVlNDRmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOTA0ZTAwMDEyMjAwMjBhNWFkZGI3ZWI1NjQ5ZDEwMDMxMzA0ZWNlNzJkOWNjYzlkYzQyNGFiY2RhODk1ZDkwNGEzMDk3Mjc0MjRlNDBlMDEwMDAxNjAwMTVlNThjMmZjODFjNDY5ZWM3YTljOWQ5MjhiNzhkZWMxOGNjZTEwYmQwMjUwNGRhYWQxYWI5ZjRlMGFjYmM3NzYxY2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZlMDlhYmJlNTAzMDEwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEyMjAxMjA5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1NThhZDFiNjQ0OGYyMmUyMDIwMTNhZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjkwNGUwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEwMDAxM2RmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZTBlZGQ4ZTAwMzAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTAwIiwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJzaWduYXR1cmVzIjogW10sICJ0eXBlIjogImJ5dG9tX2NsYWltX3Vuc2lnbmVkIn0="
    assert unsigned_claim_transaction.signatures() == []

    signed_claim_transaction = unsigned_claim_transaction.sign(
        solver=ClaimSolver(
            xprivate_key=recipient_wallet.xprivate_key(),
            secret="Hello Meheret!",
            recipient_public=recipient_wallet.public_key(),
            sender_public=sender_wallet.public_key(),
            sequence=1000
        )
    )

    assert unsigned_claim_transaction.fee() == signed_claim_transaction.fee() == 10000000
    assert unsigned_claim_transaction.hash() == signed_claim_transaction.hash() == \
        "2554c6954b735b092f64b9aa3d31d745f14abeea755d75f9cdfc0e2531d75f1b"
    assert unsigned_claim_transaction.raw() == signed_claim_transaction.raw() == \
        "070100020169016702e0b1ad2107222cfc13ab6c3365d366b5d13b11e6dc7e1e0cc4ae5676cdee44ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff904e0001220020a5addb7eb5649d10031304ece72d9ccc9dc424abcda895d904a309727424e40e01000160015e58c2fc81c469ec7a9c9d928b78dec18cce10bd02504daad1ab9f4e0acbc7761cffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe09abbe50301011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a22012091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e202013affffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff904e011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a00013dffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe0edd8e003011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a00"
    # assert unsigned_claim_transaction.json() == signed_claim_transaction.json() == \
    #     {'tx_id': '2554c6954b735b092f64b9aa3d31d745f14abeea755d75f9cdfc0e2531d75f1b', 'version': 1, 'size': 372, 'time_range': 0, 'inputs': [{'type': 'spend', 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'asset_definition': {}, 'amount': 10000, 'control_program': '0020a5addb7eb5649d10031304ece72d9ccc9dc424abcda895d904a309727424e40e', 'address': 'bm1q5kkakl44vjw3qqcnqnkwwtvuejwugf9tek5ftkgy5vyhyapyus8qgcttcs', 'spent_output_id': '98a553b8cb08b8f6e0ded3c88a18841952d8cad7afdea41206881c5fa7a03548', 'input_id': '75565b5d1ff36b7898046d210ce53dbdff61322f4ed1e0e2a8943a99edb5b6b0', 'witness_arguments': None, 'sign_data': 'dc97bb03b55814353b0b8026e156bf6a529dbec729056b7120790cbc770023c5'}, {'type': 'spend', 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'asset_definition': {}, 'amount': 1018088800, 'control_program': '00142cda4f99ea8112e6fa61cdd26157ed6dc408332a', 'address': 'bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7', 'spent_output_id': '07ae20665bf1e00a8f513ea7f6ba345f368d98fe8419749ca5781cbe1283bb33', 'input_id': 'f68bef8e56badf7f72ae23b71f0a13be8d6f1a2a3e08b6998354f5e7c97bd02f', 'witness_arguments': ['91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2'], 'sign_data': 'a06eeeb386ea9166db30135bd4b45795f199d1d3e89f65a79d15e7a56d6faf2d'}], 'outputs': [{'type': 'control', 'id': '5c26468dbf810f007554233c838aca1b5faac6785e9586b7d92d79c17571d5f7', 'position': 0, 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'asset_definition': {}, 'amount': 10000, 'control_program': '00142cda4f99ea8112e6fa61cdd26157ed6dc408332a', 'address': 'bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7'}, {'type': 'control', 'id': 'b091a3f07b44ef3c2794ad26991ec2629a31daf9b31e80d3bb82ed75c9969444', 'position': 1, 'asset_id': 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff', 'asset_definition': {}, 'amount': 1008088800, 'control_program': '00142cda4f99ea8112e6fa61cdd26157ed6dc408332a', 'address': 'bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7'}], 'fee': 10000000}
    assert unsigned_claim_transaction.unsigned_datas() == signed_claim_transaction.unsigned_datas() == \
        [{'datas': ['dc97bb03b55814353b0b8026e156bf6a529dbec729056b7120790cbc770023c5'], 'network': 'mainnet', 'path': None}, {'datas': ['a06eeeb386ea9166db30135bd4b45795f199d1d3e89f65a79d15e7a56d6faf2d'], 'public_key': '91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2', 'network': 'mainnet', 'path': 'm/44/153/1/0/1'}]

    assert signed_claim_transaction.type() == "bytom_claim_signed"
    assert signed_claim_transaction.signatures() == [['48656c6c6f204d65686572657421', '833cb7e944688b0a7b8c09fbb920bcc67e39f4435a69e87d67c386004674c23e80ec95c62195e2e564c7ffc5c48d95a2dd261e1ce2a1d697aaed6e5ce7567f03', '00', '02e803203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e2091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0'], ['1f8bc09c404b1a6e67415690ff56059c754c88f6747ca06d99da45527bee1f7d3c4ce36a08db3b3b25f61e923a055289ff226161bf87cda3e7ad2d710ecd2201']]


def test_bytom_refund_transaction():

    unsigned_refund_transaction = RefundTransaction(network=network)

    unsigned_refund_transaction.build_transaction(
        transaction_id=transaction_id,
        wallet=sender_wallet,
        amount=10_000,
        asset="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
    )

    assert unsigned_refund_transaction.type() == "bytom_refund_unsigned"
    assert unsigned_refund_transaction.unsigned_raw() == "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiNTcxNzg0YTgtMDk0NS00ZDc4LWI5NzMtYWFjNGIwOWQ2NDM5IiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbIjZkNzk3OTEyMDk4YTFhNDgyM2ViMzAxMDgwMjgyNjA1NjEyODI1MTY5N2Q1YWNjNjViM2M3MzhiN2ZkZDU3MGQiXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBbIjliNmNlMjM5MjQ1YzVkMjRjZGE5ZTBmYmQ1M2Q0ZWI1YzRhOTJhMDVjZDBlZjkwNmRiY2M0YzNkYzBkZDMxOTAiXSwgInB1YmxpY19rZXkiOiAiM2UwYTM3N2FlNGFmYTAzMWQ0NTUxNTk5ZDliYjdkNWIyN2Y0NzM2ZDc3Zjc4Y2FjNGQ0NzZmMGZmYmE1YWUzZSIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgImhhc2giOiAiYjM4MWMxYmE1YmY1MzA5Y2Y1MTljNTIwMjZhZDBhMjQ0ODA5N2UwM2YwMzdlY2EyNzllOGRiODAxNDYxYmYwYyIsICJyYXciOiAiMDcwMTAwMDIwMTY5MDE2NzAyZTBiMWFkMjEwNzIyMmNmYzEzYWI2YzMzNjVkMzY2YjVkMTNiMTFlNmRjN2UxZTBjYzRhZTU2NzZjZGVlNDRmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOTA0ZTAwMDEyMjAwMjBhNWFkZGI3ZWI1NjQ5ZDEwMDMxMzA0ZWNlNzJkOWNjYzlkYzQyNGFiY2RhODk1ZDkwNGEzMDk3Mjc0MjRlNDBlMDEwMDAxNjAwMTVlMDJlMGIxYWQyMTA3MjIyY2ZjMTNhYjZjMzM2NWQzNjZiNWQxM2IxMWU2ZGM3ZTFlMGNjNGFlNTY3NmNkZWU0NGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmMDk4ODhkODAzMDEwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkyMjAxMjAzZTBhMzc3YWU0YWZhMDMxZDQ1NTE1OTlkOWJiN2Q1YjI3ZjQ3MzZkNzdmNzhjYWM0ZDQ3NmYwZmZiYTVhZTNlMDIwMTNhZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjkwNGUwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkwMDAxM2RmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjBlYmE1ZDMwMzAxMTYwMDE0ODg3ZWU2NmQ4NGE4MmYyZDg2ODI0YTQ1YmI1MWZkZWEwM2M5MmY0OTAwIiwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX3JlZnVuZF91bnNpZ25lZCJ9"
    assert unsigned_refund_transaction.signatures() == []

    signed_refund_transaction = unsigned_refund_transaction.sign(
        solver=RefundSolver(
            xprivate_key=sender_wallet.xprivate_key(),
            secret="Hello Meheret!",
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
