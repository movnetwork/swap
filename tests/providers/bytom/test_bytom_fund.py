#!/usr/bin/env python3

from shuttle.providers.bytom.wallet import Wallet
from shuttle.providers.bytom.htlc import HTLC
from shuttle.providers.bytom.transaction import FundTransaction
from shuttle.providers.bytom.solver import FundSolver
from shuttle.providers.bytom.signature import FundSignature, Signature

import pytest


network = "mainnet"

# Initialize bytom sender wallet
sender_mnemonic = "indicate warm sock mistake code spot acid ribbon sing over taxi toast"
sender_bytom_wallet = Wallet(network=network).from_mnemonic(sender_mnemonic)
sender_xprivate_key = sender_bytom_wallet.xprivate_key()

# Initialize bytom recipient wallet
recipient_public = "ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01"
recipient_bytom_wallet = Wallet(network=network).from_public_key(recipient_public)
recipient_public_key = recipient_bytom_wallet.public_key()
recipient_program = recipient_bytom_wallet.program()


UNSIGNED_FUND = \
       "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInVuc2lnbmVk" \
       "IjogW3siZGF0YXMiOiBbImIxYzVlYTFkNjAwNjY0Y2U4MTAwNzMxNmQ2Zjg5NThlMjQ4ZWZhNjk3YWRhN2Q0M2E4YzI2YjJkNjE1" \
       "NjAxNDgiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4" \
       "YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9LCB7ImRhdGFzIjog" \
       "WyIyNTFmYmQ4YTAzMmM3MmJmMjkwN2VjNGFmYzk1ZGYxZTE2Mzg5NDZiODE5MGQwYjIxZTk1MjA2YmU2YzZhOTYyIl0sICJwdWJs" \
       "aWNfa2V5IjogIjkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIi" \
       "LCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJoYXNoIjogImM2YjMyYjk1ODEwYTEw" \
       "MDIzZDA3ODk2ODczNTI3NGQwMWU4YjVmZjhjNTU3NjNkODM3OGZhZjZhZjI5YTY2NjYiLCAicmF3IjogIjA3MDEwMDAyMDE2MTAx" \
       "NWY4MWU1MGUxMmY4MjM2ZjkxYzg4NDJkM2Y0OTU1MDJiOTc1MmZjMzVkMDE1MDA5MWVhNWIyYzI2NjA1MTVjM2I1ZjM3ZGVhNjJl" \
       "ZmQyOTY1MTc0Yjg0YmJiNTlhMGJkMGE2NzFjZjVmYjI4NTczMDNmZmQ3N2MxYjQ4MmI4NGJkZmE4Y2JkYmMzZjQwMjAxMDExNjAw" \
       "MTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0" \
       "MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAxNjAwMTVlM2ZiZjI0YjQwYzlhNzhiNWY3NmJlZTVlNmIyNDI4" \
       "YTllYzU4YWJkNjQwNDk1ZDQ5ODQ0MDk2MjQxYTJjMDM2NWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
       "ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGRkOTZmZDA4MDEwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZk" \
       "YzQwODMzMmEyMjAxMjA5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1NThhZDFiNjQ0OGYy" \
       "MmUyMDMwMWFjMDFmMzdkZWE2MmVmZDI5NjUxNzRiODRiYmI1OWEwYmQwYTY3MWNmNWZiMjg1NzMwM2ZmZDc3YzFiNDgyYjg0YmRm" \
       "NjQwMTg4MDEwMTY0MjA5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGNhYjQyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1NThhZDFiNjQ0OGYy" \
       "MmUyMjBhYzEzYzBiYjE0NDU0MjNhNjQxNzU0MTgyZDUzZjA2NzdjZDQzNTFhMGU3NDNlNmYxMGIzNTEyMmMzZDdlYTAxMjAzYTI2" \
       "ZGE4MmVhZDE1YTgwNTMzYTAyNjk2NjU2YjE0YjVkYmZkODRlYjE0NzkwZjJlMWJlNWU5ZTQ1ODIwZWViNzQxZjU0N2E2NDE2MDAw" \
       "MDAwNTU3YWE4ODg1MzdhN2NhZTdjYWM2MzFmMDAwMDAwNTM3YWNkOWY2OTcyYWU3Y2FjMDBjMDAwMDEzZWYzN2RlYTYyZWZkMjk2" \
       "NTE3NGI4NGJiYjU5YTBiZDBhNjcxY2Y1ZmIyODU3MzAzZmZkNzdjMWI0ODJiODRiZGZjNGNhZGJjM2Y0MDIwMTE2MDAxNDJjZGE0" \
       "Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEwMDAxM2RmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
       "ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBiMGI0ZjgwODAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1" \
       "N2VkNmRjNDA4MzMyYTAwIiwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX2Z1" \
       "bmRfdW5zaWduZWQifQ=="


# Fake HTLC.
class FakeHTLC(HTLC):

    def bytecode(self):
        return "01642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b644" \
               "8f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122" \
               "c3d7ea01203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e" \
               "9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd" \
               "9f6972ae7cac00c0"

    def opcode(self):
        return "0x64 0x91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448" \
               "f22e2 0xac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3" \
               "d7ea01 0x3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e4" \
               "5820eeb DEPTH 0x547a6416000000557aa888537a7cae7cac631f000000537acd" \
               "9f6972ae7cac FALSE CHECKPREDICATE"


# Testing bytom fund
def test_bytom_fund():
    # Init fake HTLC
    fake_htlc = FakeHTLC()
    # Initialization fund transaction
    unsigned_fund_transaction = FundTransaction(network=network)
    # Building fund transaction
    unsigned_fund_transaction.build_transaction(
        wallet=sender_bytom_wallet,
        htlc=fake_htlc,
        amount=100,
        asset="f37dea62efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf"
    )

    assert unsigned_fund_transaction.fee
    assert unsigned_fund_transaction.hash()
    assert unsigned_fund_transaction.raw()
    unsigned_fund_raw = unsigned_fund_transaction.unsigned_raw()
    assert unsigned_fund_transaction.unsigned()
    assert unsigned_fund_transaction.signatures == []
    assert unsigned_fund_raw == UNSIGNED_FUND

    # assert unsigned_fund_transaction.json()

    fund_solver = FundSolver(
        xprivate_key=sender_xprivate_key
    )

    signed_fund_transaction = \
        unsigned_fund_transaction.sign(fund_solver)

    assert signed_fund_transaction.fee
    assert signed_fund_transaction.hash()
    assert signed_fund_transaction.raw()
    assert signed_fund_transaction.unsigned()
    assert signed_fund_transaction.signatures

    # Singing Hash Time Lock Contract (HTLC)
    fund_signature = FundSignature(network=network) \
        .sign(unsigned_raw=unsigned_fund_raw, solver=fund_solver)

    signature = Signature(network=network) \
        .sign(unsigned_raw=unsigned_fund_raw, solver=fund_solver)

    assert fund_signature.fee == signature.fee == signed_fund_transaction.fee == \
           unsigned_fund_transaction.fee == 10000000
    assert fund_signature.hash() == signed_fund_transaction.hash() == unsigned_fund_transaction.hash() == \
           signature.hash() == "c6b32b95810a10023d078968735274d01e8b5ff8c55763d8378faf6af29a6666"
    assert fund_signature.raw() == signature.raw() == signed_fund_transaction.raw() == \
           "070100020161015f81e50e12f8236f91c8842d3f495502b9752fc35d0150091ea5b2c2660515c3b5f37dea62efd29651" \
           "74b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdfa8cbdbc3f40201011600142cda4f99ea8112e6fa61cdd261" \
           "57ed6dc408332a22012091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e20160015e3fbf" \
           "24b40c9a78b5f76bee5e6b2428a9ec58abd640495d49844096241a2c0365ffffffffffffffffffffffffffffffffffff" \
           "ffffffffffffffffffffffffffff80dd96fd0801011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a22012091" \
           "ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e20301ac01f37dea62efd2965174b84bbb59" \
           "a0bd0a671cf5fb2857303ffd77c1b482b84bdf6401880101642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59a" \
           "def9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01203a26da82" \
           "ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac63" \
           "1f000000537acd9f6972ae7cac00c000013ef37dea62efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b8" \
           "4bdfc4cadbc3f402011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a00013dffffffffffffffffffffffffff" \
           "ffffffffffffffffffffffffffffffffffffff80b0b4f808011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a" \
           "00"
    assert fund_signature.unsigned() == signature.unsigned() == signed_fund_transaction.unsigned() == \
           unsigned_fund_transaction.unsigned() == [
               {
                   'datas': [
                       'b1c5ea1d600664ce81007316d6f8958e248efa697ada7d43a8c26b2d61560148'
                   ],
                   'public_key': '91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2',
                   'network': 'mainnet',
                   'path': 'm/44/153/1/0/1'
               },
               {
                   'datas': [
                       '251fbd8a032c72bf2907ec4afc95df1e1638946b8190d0b21e95206be6c6a962'
                   ],
                   'public_key': '91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2',
                   'network': 'mainnet',
                   'path': 'm/44/153/1/0/1'
               }
           ]
    assert fund_signature.signatures == signed_fund_transaction.signatures == \
           unsigned_fund_transaction.signatures == signature.signatures == [
               [
                   "dfda4a7a739508eafb67846aaa28be97017c5642d5d3c5ce368605e11e0fca1e359d4edf2c112a528622d4fc75941"
                   "11c5ad921cee67378c62a6c0db2dd379201"
               ],
               [
                   "8cfe5dfa39fb23ee6c15eb5ccb8009f32948c2c159b16b5cab8b7b179936ae5900173f96ff76b7fb0b458cdb70230"
                   "abadb8f69d6f6ee8422239ecb9049cea30f"
               ]
           ]

    assert fund_signature.signed_raw() == signature.signed_raw() == \
           "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInJhdyI6ICIwN" \
           "zAxMDAwMjAxNjEwMTVmODFlNTBlMTJmODIzNmY5MWM4ODQyZDNmNDk1NTAyYjk3NTJmYzM1ZDAxNTAwOTFlYTViMmMyNjYwNTE1Yz" \
           "NiNWYzN2RlYTYyZWZkMjk2NTE3NGI4NGJiYjU5YTBiZDBhNjcxY2Y1ZmIyODU3MzAzZmZkNzdjMWI0ODJiODRiZGZhOGNiZGJjM2Y" \
           "0MDIwMTAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTIyMDEyMDkxZmY3ZjUyNWZmNDA4NzRj" \
           "NGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIwMTYwMDE1ZTNmYmYyNGI0MGM5YTc4YjVmNzZiZ" \
           "WU1ZTZiMjQyOGE5ZWM1OGFiZDY0MDQ5NWQ0OTg0NDA5NjI0MWEyYzAzNjVmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZm" \
           "ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBkZDk2ZmQwODAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI" \
           "2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQx" \
           "YjY0NDhmMjJlMjAzMDFhYzAxZjM3ZGVhNjJlZmQyOTY1MTc0Yjg0YmJiNTlhMGJkMGE2NzFjZjVmYjI4NTczMDNmZmQ3N2MxYjQ4M" \
           "mI4NGJkZjY0MDE4ODAxMDE2NDIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYj" \
           "Y0NDhmMjJlMjIwYWMxM2MwYmIxNDQ1NDIzYTY0MTc1NDE4MmQ1M2YwNjc3Y2Q0MzUxYTBlNzQzZTZmMTBiMzUxMjJjM2Q3ZWEwMTI" \
           "wM2EyNmRhODJlYWQxNWE4MDUzM2EwMjY5NjY1NmIxNGI1ZGJmZDg0ZWIxNDc5MGYyZTFiZTVlOWU0NTgyMGVlYjc0MWY1NDdhNjQx" \
           "NjAwMDAwMDU1N2FhODg4NTM3YTdjYWU3Y2FjNjMxZjAwMDAwMDUzN2FjZDlmNjk3MmFlN2NhYzAwYzAwMDAxM2VmMzdkZWE2MmVmZ" \
           "DI5NjUxNzRiODRiYmI1OWEwYmQwYTY3MWNmNWZiMjg1NzMwM2ZmZDc3YzFiNDgyYjg0YmRmYzRjYWRiYzNmNDAyMDExNjAwMTQyY2" \
           "RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAwMTNkZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZ" \
           "mZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjgwYjBiNGY4MDgwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYx" \
           "NTdlZDZkYzQwODMzMmEwMCIsICJoYXNoIjogImM2YjMyYjk1ODEwYTEwMDIzZDA3ODk2ODczNTI3NGQwMWU4YjVmZjhjNTU3NjNkO" \
           "DM3OGZhZjZhZjI5YTY2NjYiLCAidW5zaWduZWQiOiBbeyJkYXRhcyI6IFsiYjFjNWVhMWQ2MDA2NjRjZTgxMDA3MzE2ZDZmODk1OG" \
           "UyNDhlZmE2OTdhZGE3ZDQzYThjMjZiMmQ2MTU2MDE0OCJdLCAicHVibGljX2tleSI6ICI5MWZmN2Y1MjVmZjQwODc0YzRmNDdmMGN" \
           "hYjQyZTQ2ZTNiZjUzYWRhZDU5YWRlZjk1NThhZDFiNjQ0OGYyMmUyIiwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogIm0v" \
           "NDQvMTUzLzEvMC8xIn0sIHsiZGF0YXMiOiBbIjI1MWZiZDhhMDMyYzcyYmYyOTA3ZWM0YWZjOTVkZjFlMTYzODk0NmI4MTkwZDBiM" \
           "jFlOTUyMDZiZTZjNmE5NjIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYW" \
           "Q1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSw" \
           "gIm5ldHdvcmsiOiAibWFpbm5ldCIsICJzaWduYXR1cmVzIjogW1siZGZkYTRhN2E3Mzk1MDhlYWZiNjc4NDZhYWEyOGJlOTcwMTdj" \
           "NTY0MmQ1ZDNjNWNlMzY4NjA1ZTExZTBmY2ExZTM1OWQ0ZWRmMmMxMTJhNTI4NjIyZDRmYzc1OTQxMTFjNWFkOTIxY2VlNjczNzhjN" \
           "jJhNmMwZGIyZGQzNzkyMDEiXSwgWyI4Y2ZlNWRmYTM5ZmIyM2VlNmMxNWViNWNjYjgwMDlmMzI5NDhjMmMxNTliMTZiNWNhYjhiN2" \
           "IxNzk5MzZhZTU5MDAxNzNmOTZmZjc2YjdmYjBiNDU4Y2RiNzAyMzBhYmFkYjhmNjlkNmY2ZWU4NDIyMjM5ZWNiOTA0OWNlYTMwZiJ" \
           "dXSwgInR5cGUiOiAiYnl0b21fZnVuZF9zaWduZWQifQ=="

    with pytest.raises(ValueError, match="transaction is none, build transaction first."):
        Signature().hash()
    with pytest.raises(ValueError, match="transaction is none, build transaction first."):
        Signature().json()
    with pytest.raises(ValueError, match="transaction is none, build transaction first."):
        Signature().raw()
    # with pytest.raises(ValueError, match="not found type, sign first"):
    #     Signature().type()
    with pytest.raises(ValueError, match="there is no signed data, sign first"):
        Signature().signed_raw()
    with pytest.raises(ValueError, match="transaction is none, build transaction first."):
        Signature().unsigned()
    with pytest.raises(ValueError, match="invalid unsigned transaction raw"):
        Signature().sign("eyJtIjogImFzZCJ9", "")
