#!/usr/bin/env python3

from shuttle.providers.bytom.wallet import Wallet
from shuttle.providers.bytom.transaction import ClaimTransaction
from shuttle.providers.bytom.solver import ClaimSolver
from shuttle.providers.bytom.signature import ClaimSignature, Signature

recipient_mnemonic = "indicate warm sock mistake code spot acid ribbon sing over taxi toast"
recipient_bytom_wallet = Wallet(network="mainnet").from_mnemonic(recipient_mnemonic)
recipient_xprivate_key = recipient_bytom_wallet.xprivate_key()

# Funded hash time lock contract transaction id/hash
fund_transaction_id = "8843bca172ed4685b511c0f106fd3f6889a42fa3f9383d057ea4e587f7db0cbe"


# Testing bytom claim
def test_bytom_claim():
    # Initialization claim transaction
    unsigned_claim_transaction = ClaimTransaction(network="mainnet")
    # Building claim transaction
    unsigned_claim_transaction.build_transaction(
        transaction_id=fund_transaction_id,
        wallet=recipient_bytom_wallet,
        amount=100,
        asset="f37dea62efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf"
    )

    assert unsigned_claim_transaction.fee == 10000000
    assert unsigned_claim_transaction.hash()
    assert unsigned_claim_transaction.raw()
    assert unsigned_claim_transaction.unsigned()

    unsigned_claim_raw = unsigned_claim_transaction.unsigned_raw()
    assert unsigned_claim_raw == \
           "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInVuc2lnbmVkI" \
           "jogW3siZGF0YXMiOiBbIjQ5NGVlNzc2OTBhYzJhYjUxZTZkZTRkYWMyZWJhMmQzNTc3MTc0MzEyZWQwYTIyMjQ5NGE5OTVlMjhmZm" \
           "Y4NDYiXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBbImVjYWJhNDAxYTZkZjljZmZiZWQ" \
           "zN2QxYWJjZjIzYjkxYjNjODRlYzdhYTk0MTFkNDgxY2JlZjJlNDM3ZWY3YjEiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0" \
           "MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiL" \
           "CAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgImhhc2giOiAiMDY5YWU0NDg2MDQ3ZWQzMTQzMjkxYWFjNzVkM2FmNDhkMTI4Mz" \
           "ZkMGI1ODEyNzg3MTc3ZGM0MGJiOTY1YzkwZiIsICJyYXciOiAiMDcwMTAwMDIwMWQwMDEwMWNkMDEzZmJmMjRiNDBjOWE3OGI1Zjc" \
           "2YmVlNWU2YjI0MjhhOWVjNThhYmQ2NDA0OTVkNDk4NDQwOTYyNDFhMmMwMzY1ZjM3ZGVhNjJlZmQyOTY1MTc0Yjg0YmJiNTlhMGJk" \
           "MGE2NzFjZjVmYjI4NTczMDNmZmQ3N2MxYjQ4MmI4NGJkZjY0MDAwMTg4MDEwMTY0MjA5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhY" \
           "jQyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1NThhZDFiNjQ0OGYyMmUyMjBhYzEzYzBiYjE0NDU0MjNhNjQxNzU0MTgyZDUzZjA2NzdjZD" \
           "QzNTFhMGU3NDNlNmYxMGIzNTEyMmMzZDdlYTAxMjAyYjlhNTk0OWY1NTQ2ZjYzYTI1M2U0MWNkYTZiZmZkZWRiNTI3Mjg4YTdlMjR" \
           "lZDk1M2Y1YzI2ODBjNzBkNmZmNzQxZjU0N2E2NDE2MDAwMDAwNTU3YWE4ODg1MzdhN2NhZTdjYWM2MzFmMDAwMDAwNTM3YWNkOWY2" \
           "OTcyYWU3Y2FjMDBjMDAxMDAwMTYwMDE1ZTNmYmYyNGI0MGM5YTc4YjVmNzZiZWU1ZTZiMjQyOGE5ZWM1OGFiZDY0MDQ5NWQ0OTg0N" \
           "DA5NjI0MWEyYzAzNjVmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
           "ZmODBkZDk2ZmQwODAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI" \
           "1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDEzOWYzN2RlYTYyZWZkMjk2" \
           "NTE3NGI4NGJiYjU5YTBiZDBhNjcxY2Y1ZmIyODU3MzAzZmZkNzdjMWI0ODJiODRiZGY2NDAxMTYwMDE0MmNkYTRmOTllYTgxMTJlN" \
           "mZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTAwMDEzZGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
           "ZmZmZmZmZmZmZmZmZmZmZmZmY4MGIwYjRmODA4MDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJ" \
           "hMDAiLCAic2VjcmV0IjogbnVsbCwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJzaWduYXR1cmVzIjogW10sICJ0eXBlIjogImJ5dG9t" \
           "X2NsYWltX3Vuc2lnbmVkIn0="

    # Claiming HTLC solver
    claim_solver = ClaimSolver(
        secret="Hello Meheret!",
        xprivate_key=recipient_xprivate_key
    )

    # Singing Hash Time Lock Contract (HTLC)
    signed_claim_transaction = \
        unsigned_claim_transaction.sign(claim_solver)

    assert signed_claim_transaction.fee
    assert signed_claim_transaction.hash()
    assert signed_claim_transaction.raw()
    assert signed_claim_transaction.unsigned()
    assert signed_claim_transaction.signatures

    # Singing Hash Time Lock Contract (HTLC)
    claim_signature = ClaimSignature(network="mainnet") \
        .sign(unsigned_raw=unsigned_claim_raw, solver=claim_solver)

    signature = Signature(network="mainnet") \
        .sign(unsigned_raw=unsigned_claim_raw, solver=claim_solver)

    assert signature.fee == claim_signature.fee == signed_claim_transaction.fee == \
           unsigned_claim_transaction.fee == 10000000
    assert claim_signature.hash() == signed_claim_transaction.hash() == unsigned_claim_transaction.hash() == \
           signature.hash() == "069ae4486047ed3143291aac75d3af48d12836d0b5812787177dc40bb965c90f"
    assert signature.raw() == claim_signature.raw() == signed_claim_transaction.raw() == unsigned_claim_transaction.raw() == \
           "0701000201d00101cd013fbf24b40c9a78b5f76bee5e6b2428a9ec58abd640495d49844096241a2c0365f37dea62efd296517" \
           "4b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf640001880101642091ff7f525ff40874c4f47f0cab42e46e3bf53a" \
           "dad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a594" \
           "9f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f00" \
           "0000537acd9f6972ae7cac00c001000160015e3fbf24b40c9a78b5f76bee5e6b2428a9ec58abd640495d49844096241a2c036" \
           "5ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff80dd96fd0801011600142cda4f99ea8112e6" \
           "fa61cdd26157ed6dc408332a22012091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2020139f" \
           "37dea62efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf64011600142cda4f99ea8112e6fa61cdd26157" \
           "ed6dc408332a00013dffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff80b0b4f808011600142" \
           "cda4f99ea8112e6fa61cdd26157ed6dc408332a00"
    assert signature.unsigned() == claim_signature.unsigned() == signed_claim_transaction.unsigned() == \
           unsigned_claim_transaction.unsigned() == [
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
    assert signature.signatures == claim_signature.signatures == signed_claim_transaction.signatures == \
           unsigned_claim_transaction.signatures == [
               [
                   '48656c6c6f204d65686572657421',
                   '65b4fcd9e6d58e2ab9ddadc6f330c519d3fcecfe3d30a4e48419920c9dba9dc88be503d7c9a825d09becd68380b6c'
                   '4e3adb0545d851b968128c08ddb01cde70d',
                   ''],
               [
                   '5bd906d6829b1679c1b6e987849e5f8432a1dd7114b026908f675dafb9a9526e25a7a23f451e08695c133e67a8990'
                   '79cf75410cc055b937158fc473e8154130a'
               ]
           ]

    assert signature.signed_raw() == claim_signature.signed_raw() == \
           "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInJhdyI6ICIwN" \
           "zAxMDAwMjAxZDAwMTAxY2QwMTNmYmYyNGI0MGM5YTc4YjVmNzZiZWU1ZTZiMjQyOGE5ZWM1OGFiZDY0MDQ5NWQ0OTg0NDA5NjI0MW" \
           "EyYzAzNjVmMzdkZWE2MmVmZDI5NjUxNzRiODRiYmI1OWEwYmQwYTY3MWNmNWZiMjg1NzMwM2ZmZDc3YzFiNDgyYjg0YmRmNjQwMDA" \
           "xODgwMTAxNjQyMDkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIy" \
           "MGFjMTNjMGJiMTQ0NTQyM2E2NDE3NTQxODJkNTNmMDY3N2NkNDM1MWEwZTc0M2U2ZjEwYjM1MTIyYzNkN2VhMDEyMDJiOWE1OTQ5Z" \
           "jU1NDZmNjNhMjUzZTQxY2RhNmJmZmRlZGI1MjcyODhhN2UyNGVkOTUzZjVjMjY4MGM3MGQ2ZmY3NDFmNTQ3YTY0MTYwMDAwMDA1NT" \
           "dhYTg4ODUzN2E3Y2FlN2NhYzYzMWYwMDAwMDA1MzdhY2Q5ZjY5NzJhZTdjYWMwMGMwMDEwMDAxNjAwMTVlM2ZiZjI0YjQwYzlhNzh" \
           "iNWY3NmJlZTVlNmIyNDI4YTllYzU4YWJkNjQwNDk1ZDQ5ODQ0MDk2MjQxYTJjMDM2NWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
           "ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGRkOTZmZDA4MDEwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmY" \
           "TYxY2RkMjYxNTdlZDZkYzQwODMzMmEyMjAxMjA5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWRlZj" \
           "k1NThhZDFiNjQ0OGYyMmUyMDIwMTM5ZjM3ZGVhNjJlZmQyOTY1MTc0Yjg0YmJiNTlhMGJkMGE2NzFjZjVmYjI4NTczMDNmZmQ3N2M" \
           "xYjQ4MmI4NGJkZjY0MDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAwMTNkZmZmZmZmZmZm" \
           "ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjgwYjBiNGY4MDgwMTE2MDAxNDJjZ" \
           "GE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEwMCIsICJoYXNoIjogIjA2OWFlNDQ4NjA0N2VkMzE0MzI5MWFhYz" \
           "c1ZDNhZjQ4ZDEyODM2ZDBiNTgxMjc4NzE3N2RjNDBiYjk2NWM5MGYiLCAidW5zaWduZWQiOiBbeyJkYXRhcyI6IFsiNDk0ZWU3NzY" \
           "5MGFjMmFiNTFlNmRlNGRhYzJlYmEyZDM1NzcxNzQzMTJlZDBhMjIyNDk0YTk5NWUyOGZmZjg0NiJdLCAibmV0d29yayI6ICJtYWlu" \
           "bmV0IiwgInBhdGgiOiBudWxsfSwgeyJkYXRhcyI6IFsiZWNhYmE0MDFhNmRmOWNmZmJlZDM3ZDFhYmNmMjNiOTFiM2M4NGVjN2FhO" \
           "TQxMWQ0ODFjYmVmMmU0MzdlZjdiMSJdLCAicHVibGljX2tleSI6ICI5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZj" \
           "UzYWRhZDU5YWRlZjk1NThhZDFiNjQ0OGYyMmUyIiwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogIm0vNDQvMTUzLzEvMC8" \
           "xIn1dLCAibmV0d29yayI6ICJtYWlubmV0IiwgInNpZ25hdHVyZXMiOiBbWyI0ODY1NmM2YzZmMjA0ZDY1Njg2NTcyNjU3NDIxIiwg" \
           "IjY1YjRmY2Q5ZTZkNThlMmFiOWRkYWRjNmYzMzBjNTE5ZDNmY2VjZmUzZDMwYTRlNDg0MTk5MjBjOWRiYTlkYzg4YmU1MDNkN2M5Y" \
           "TgyNWQwOWJlY2Q2ODM4MGI2YzRlM2FkYjA1NDVkODUxYjk2ODEyOGMwOGRkYjAxY2RlNzBkIiwgIiJdLCBbIjViZDkwNmQ2ODI5Yj" \
           "E2NzljMWI2ZTk4Nzg0OWU1Zjg0MzJhMWRkNzExNGIwMjY5MDhmNjc1ZGFmYjlhOTUyNmUyNWE3YTIzZjQ1MWUwODY5NWMxMzNlNjd" \
           "hODk5MDc5Y2Y3NTQxMGNjMDU1YjkzNzE1OGZjNDczZTgxNTQxMzBhIl1dLCAidHlwZSI6ICJieXRvbV9jbGFpbV9zaWduZWQifQ=="
