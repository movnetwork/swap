#!/usr/bin/env python3

from shuttle.providers.bytom.wallet import Wallet
from shuttle.providers.bytom.transaction import RefundTransaction
from shuttle.providers.bytom.solver import RefundSolver
from shuttle.providers.bytom.signature import RefundSignature, Signature

sender_mnemonic = "indicate warm sock mistake code spot acid ribbon sing over taxi toast"
sender_bytom_wallet = Wallet(network="mainnet").from_mnemonic(sender_mnemonic)
sender_xprivate_key = sender_bytom_wallet.xprivate_key()

# Funded hash time lock contract transaction id/hash
fund_transaction_id = "8843bca172ed4685b511c0f106fd3f6889a42fa3f9383d057ea4e587f7db0cbe"


# Testing bytom refund
def test_bytom_refund():
    # Initialization refund transaction
    unsigned_refund_transaction = RefundTransaction(network="mainnet")
    # Building refund transaction
    unsigned_refund_transaction.build_transaction(
        transaction_id=fund_transaction_id,
        wallet=sender_bytom_wallet,
        amount=100,
        asset="f37dea62efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf"
    )

    assert unsigned_refund_transaction.fee == 10000000
    assert unsigned_refund_transaction.hash()
    assert unsigned_refund_transaction.raw()
    assert unsigned_refund_transaction.unsigned()

    unsigned_refund_raw = unsigned_refund_transaction.unsigned_raw()
    assert unsigned_refund_raw == \
           "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInVuc2lnbmVkIj" \
           "ogW3siZGF0YXMiOiBbIjQ5NGVlNzc2OTBhYzJhYjUxZTZkZTRkYWMyZWJhMmQzNTc3MTc0MzEyZWQwYTIyMjQ5NGE5OTVlMjhmZmY4" \
           "NDYiXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBbImVjYWJhNDAxYTZkZjljZmZiZWQzN2" \
           "QxYWJjZjIzYjkxYjNjODRlYzdhYTk0MTFkNDgxY2JlZjJlNDM3ZWY3YjEiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3" \
           "NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicG" \
           "F0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgImhhc2giOiAiMDY5YWU0NDg2MDQ3ZWQzMTQzMjkxYWFjNzVkM2FmNDhkMTI4MzZkMGI1" \
           "ODEyNzg3MTc3ZGM0MGJiOTY1YzkwZiIsICJyYXciOiAiMDcwMTAwMDIwMWQwMDEwMWNkMDEzZmJmMjRiNDBjOWE3OGI1Zjc2YmVlNW" \
           "U2YjI0MjhhOWVjNThhYmQ2NDA0OTVkNDk4NDQwOTYyNDFhMmMwMzY1ZjM3ZGVhNjJlZmQyOTY1MTc0Yjg0YmJiNTlhMGJkMGE2NzFj" \
           "ZjVmYjI4NTczMDNmZmQ3N2MxYjQ4MmI4NGJkZjY0MDAwMTg4MDEwMTY0MjA5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZT" \
           "NiZjUzYWRhZDU5YWRlZjk1NThhZDFiNjQ0OGYyMmUyMjBhYzEzYzBiYjE0NDU0MjNhNjQxNzU0MTgyZDUzZjA2NzdjZDQzNTFhMGU3" \
           "NDNlNmYxMGIzNTEyMmMzZDdlYTAxMjAyYjlhNTk0OWY1NTQ2ZjYzYTI1M2U0MWNkYTZiZmZkZWRiNTI3Mjg4YTdlMjRlZDk1M2Y1Yz" \
           "I2ODBjNzBkNmZmNzQxZjU0N2E2NDE2MDAwMDAwNTU3YWE4ODg1MzdhN2NhZTdjYWM2MzFmMDAwMDAwNTM3YWNkOWY2OTcyYWU3Y2Fj" \
           "MDBjMDAxMDAwMTYwMDE1ZTNmYmYyNGI0MGM5YTc4YjVmNzZiZWU1ZTZiMjQyOGE5ZWM1OGFiZDY0MDQ5NWQ0OTg0NDA5NjI0MWEyYz" \
           "AzNjVmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBkZDk2ZmQw" \
           "ODAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0Zj" \
           "Q3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDEzOWYzN2RlYTYyZWZkMjk2NTE3NGI4NGJiYjU5" \
           "YTBiZDBhNjcxY2Y1ZmIyODU3MzAzZmZkNzdjMWI0ODJiODRiZGY2NDAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2" \
           "VkNmRjNDA4MzMyYTAwMDEzZGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
           "ZmZmZmY4MGIwYjRmODA4MDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAic2lnbmF0dX" \
           "JlcyI6IFtdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInR5cGUiOiAiYnl0b21fcmVmdW5kX3Vuc2lnbmVkIn0="

    # Refunding HTLC solver
    refund_solver = RefundSolver(
        xprivate_key=sender_xprivate_key
    )

    # Singing Hash Time Lock Contract (HTLC)
    signed_refund_transaction = \
        unsigned_refund_transaction.sign(refund_solver)

    assert signed_refund_transaction.fee
    assert signed_refund_transaction.hash()
    assert signed_refund_transaction.raw()
    assert signed_refund_transaction.unsigned()
    assert signed_refund_transaction.signatures

    # Singing Hash Time Lock Contract (HTLC)
    refund_signature = RefundSignature(network="mainnet") \
        .sign(unsigned_raw=unsigned_refund_raw, solver=refund_solver)

    signature = Signature(network="mainnet") \
        .sign(unsigned_raw=unsigned_refund_raw, solver=refund_solver)

    assert signature.fee == refund_signature.fee == signed_refund_transaction.fee == \
           unsigned_refund_transaction.fee == 10000000
    assert refund_signature.hash() == signed_refund_transaction.hash() == unsigned_refund_transaction.hash() == \
           signature.hash() == "069ae4486047ed3143291aac75d3af48d12836d0b5812787177dc40bb965c90f"
    assert signature.raw() == refund_signature.raw() == signed_refund_transaction.raw() == \
           "0701000201d00101cd013fbf24b40c9a78b5f76bee5e6b2428a9ec58abd640495d49844096241a2c0365f37dea62efd2965174" \
           "b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf640001880101642091ff7f525ff40874c4f47f0cab42e46e3bf53ada" \
           "d59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a5949f5" \
           "546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f000000" \
           "537acd9f6972ae7cac00c001000160015e3fbf24b40c9a78b5f76bee5e6b2428a9ec58abd640495d49844096241a2c0365ffff" \
           "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff80dd96fd0801011600142cda4f99ea8112e6fa61cd" \
           "d26157ed6dc408332a22012091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2020139f37dea62" \
           "efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf64011600142cda4f99ea8112e6fa61cdd26157ed6dc408" \
           "332a00013dffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff80b0b4f808011600142cda4f99ea" \
           "8112e6fa61cdd26157ed6dc408332a00"
    assert signature.unsigned() == refund_signature.unsigned() == signed_refund_transaction.unsigned() == \
           unsigned_refund_transaction.unsigned() == [
                {
                    'datas': [
                        '494ee77690ac2ab51e6de4dac2eba2d3577174312ed0a222494a995e28fff846'
                    ],
                    'network': 'mainnet',
                    'path': None
                },
                {
                    'datas': [
                        'ecaba401a6df9cffbed37d1abcf23b91b3c84ec7aa9411d481cbef2e437ef7b1'
                    ],
                    'public_key': '91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2',
                    'network': 'mainnet',
                    'path': 'm/44/153/1/0/1'
                }
            ]
    assert signature.signatures == refund_signature.signatures == signed_refund_transaction.signatures == \
           unsigned_refund_transaction.signatures == [
                [
                    "65b4fcd9e6d58e2ab9ddadc6f330c519d3fcecfe3d30a4e48419920c9dba9dc88be503d7c9a825d09becd68380b6c"
                    "4e3adb0545d851b968128c08ddb01cde70d",
                    "01"
                ],
                [
                    "5bd906d6829b1679c1b6e987849e5f8432a1dd7114b026908f675dafb9a9526e25a7a23f451e08695c133e67a8990"
                    "79cf75410cc055b937158fc473e8154130a"
                ]
            ]

    assert signature.signed_raw() == refund_signature.signed_raw() == \
           "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInJhdyI6ICIwNz" \
           "AxMDAwMjAxZDAwMTAxY2QwMTNmYmYyNGI0MGM5YTc4YjVmNzZiZWU1ZTZiMjQyOGE5ZWM1OGFiZDY0MDQ5NWQ0OTg0NDA5NjI0MWEy" \
           "YzAzNjVmMzdkZWE2MmVmZDI5NjUxNzRiODRiYmI1OWEwYmQwYTY3MWNmNWZiMjg1NzMwM2ZmZDc3YzFiNDgyYjg0YmRmNjQwMDAxOD" \
           "gwMTAxNjQyMDkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIyMGFj" \
           "MTNjMGJiMTQ0NTQyM2E2NDE3NTQxODJkNTNmMDY3N2NkNDM1MWEwZTc0M2U2ZjEwYjM1MTIyYzNkN2VhMDEyMDJiOWE1OTQ5ZjU1ND" \
           "ZmNjNhMjUzZTQxY2RhNmJmZmRlZGI1MjcyODhhN2UyNGVkOTUzZjVjMjY4MGM3MGQ2ZmY3NDFmNTQ3YTY0MTYwMDAwMDA1NTdhYTg4" \
           "ODUzN2E3Y2FlN2NhYzYzMWYwMDAwMDA1MzdhY2Q5ZjY5NzJhZTdjYWMwMGMwMDEwMDAxNjAwMTVlM2ZiZjI0YjQwYzlhNzhiNWY3Nm" \
           "JlZTVlNmIyNDI4YTllYzU4YWJkNjQwNDk1ZDQ5ODQ0MDk2MjQxYTJjMDM2NWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
           "ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGRkOTZmZDA4MDEwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMj" \
           "YxNTdlZDZkYzQwODMzMmEyMjAxMjA5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1NThhZDFi" \
           "NjQ0OGYyMmUyMDIwMTM5ZjM3ZGVhNjJlZmQyOTY1MTc0Yjg0YmJiNTlhMGJkMGE2NzFjZjVmYjI4NTczMDNmZmQ3N2MxYjQ4MmI4NG" \
           "JkZjY0MDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAwMTNkZmZmZmZmZmZmZmZmZmZmZmZm" \
           "ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjgwYjBiNGY4MDgwMTE2MDAxNDJjZGE0Zjk5ZWE4MT" \
           "EyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEwMCIsICJoYXNoIjogIjA2OWFlNDQ4NjA0N2VkMzE0MzI5MWFhYzc1ZDNhZjQ4ZDEy" \
           "ODM2ZDBiNTgxMjc4NzE3N2RjNDBiYjk2NWM5MGYiLCAidW5zaWduZWQiOiBbeyJkYXRhcyI6IFsiNDk0ZWU3NzY5MGFjMmFiNTFlNm" \
           "RlNGRhYzJlYmEyZDM1NzcxNzQzMTJlZDBhMjIyNDk0YTk5NWUyOGZmZjg0NiJdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgi" \
           "OiBudWxsfSwgeyJkYXRhcyI6IFsiZWNhYmE0MDFhNmRmOWNmZmJlZDM3ZDFhYmNmMjNiOTFiM2M4NGVjN2FhOTQxMWQ0ODFjYmVmMm" \
           "U0MzdlZjdiMSJdLCAicHVibGljX2tleSI6ICI5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1" \
           "NThhZDFiNjQ0OGYyMmUyIiwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogIm0vNDQvMTUzLzEvMC8xIn1dLCAibmV0d29yay" \
           "I6ICJtYWlubmV0IiwgInNpZ25hdHVyZXMiOiBbWyI2NWI0ZmNkOWU2ZDU4ZTJhYjlkZGFkYzZmMzMwYzUxOWQzZmNlY2ZlM2QzMGE0" \
           "ZTQ4NDE5OTIwYzlkYmE5ZGM4OGJlNTAzZDdjOWE4MjVkMDliZWNkNjgzODBiNmM0ZTNhZGIwNTQ1ZDg1MWI5NjgxMjhjMDhkZGIwMW" \
           "NkZTcwZCIsICIwMSJdLCBbIjViZDkwNmQ2ODI5YjE2NzljMWI2ZTk4Nzg0OWU1Zjg0MzJhMWRkNzExNGIwMjY5MDhmNjc1ZGFmYjlh" \
           "OTUyNmUyNWE3YTIzZjQ1MWUwODY5NWMxMzNlNjdhODk5MDc5Y2Y3NTQxMGNjMDU1YjkzNzE1OGZjNDczZTgxNTQxMzBhIl1dLCAidH" \
           "lwZSI6ICJieXRvbV9yZWZ1bmRfc2lnbmVkIn0="
