#!/usr/bin/env python3

from base64 import b64encode, b64decode

import json

from .transaction import Transaction
from .solver import FundSolver, ClaimSolver, RefundSolver
from .rpc import decode_tx_raw


# Signature
class Signature(Transaction):
    """
    Bytom Signature class.

    :param network: Bytom network, defaults to testnet.
    :type network: str
    :returns:  Transaction -- Bytom transaction instance.

    .. note::
        Bytom has only three networks, ``mainnet``, ``solonet`` and ``testnet``.
    """

    def __init__(self, network="testnet"):
        super().__init__(network)
        # Bytom transaction
        self.transaction = None
        # Signed raw, type and fee
        self._signed_raw, self._type, self._fee = None, None, 0,

        # Bytom setup network
        if network not in ["mainnet", "solonet", "testnet"]:
            raise ValueError("invalid network, please choose only mainnet, solonet or testnet networks")
        self.network = network

    # Transaction fee
    def fee(self):
        """
        Get Bitcoin transaction fee.

        :returns: int -- Bitcoin transaction fee.

        >>> from shuttle.providers.bytom.signature import Signature
        >>> from shuttle.providers.bytom.solver import FundSolver
        >>> bytom_fund_unsigned_raw = "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInVuc2lnbmVkIjogW3siZGF0YXMiOiBbIjM4NjAxYmY3Y2UwOGRhYjkyMTkxNmYyYzcyM2FjY2EwNDUxZDg5MDQ2NDliYmVjMTZjMjA3NmYxNDU1ZGQxYTIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgImhhc2giOiAiNzY0NzIyOGFlM2MxNGQ5OGI4N2JkOWE2ZWI5NGJiMjgzMjkxMzUzZWE2MmFjZDIxYWQzNTMxMWFlOTEwZWY2ZiIsICJyYXciOiAiMDcwMTAwMDEwMTYwMDE1ZWU1MDFhOTdlMTQ0OWExYTg5OTI1ZGYxMjU5ZWJmMWUxYzhmYmIyM2E2MTA3MmNmMzQ0YmIzMmVlNjc2YjY2YmRmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZTBkYjg4YzcwNzAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDE0NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDAwMTNkZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmQwZTBhNWMyMDcwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEwMCIsICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieXRvbV9mdW5kX3Vuc2lnbmVkIn0"
        >>> fund_solver = FundSolver(xprivate_key="205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
        >>> signature = Signature(network="testnet")
        >>> signature.sign(bytom_fund_unsigned_raw, fund_solver)
        >>> signature.fee()
        10000000
        """

        return self._fee

    # Transaction hash
    def hash(self):
        """
        Get Bytom signature transaction hash.

        :returns: str -- Bytom signature transaction hash or transaction id.

        >>> from shuttle.providers.bytom.signature import Signature
        >>> from shuttle.providers.bytom.solver import FundSolver
        >>> bytom_fund_unsigned_raw = "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInVuc2lnbmVkIjogW3siZGF0YXMiOiBbIjM4NjAxYmY3Y2UwOGRhYjkyMTkxNmYyYzcyM2FjY2EwNDUxZDg5MDQ2NDliYmVjMTZjMjA3NmYxNDU1ZGQxYTIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgImhhc2giOiAiNzY0NzIyOGFlM2MxNGQ5OGI4N2JkOWE2ZWI5NGJiMjgzMjkxMzUzZWE2MmFjZDIxYWQzNTMxMWFlOTEwZWY2ZiIsICJyYXciOiAiMDcwMTAwMDEwMTYwMDE1ZWU1MDFhOTdlMTQ0OWExYTg5OTI1ZGYxMjU5ZWJmMWUxYzhmYmIyM2E2MTA3MmNmMzQ0YmIzMmVlNjc2YjY2YmRmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZTBkYjg4YzcwNzAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDE0NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDAwMTNkZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmQwZTBhNWMyMDcwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEwMCIsICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieXRvbV9mdW5kX3Vuc2lnbmVkIn0"
        >>> fund_solver = FundSolver(xprivate_key="205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
        >>> signature = Signature(network="testnet")
        >>> signature.sign(bytom_fund_unsigned_raw, fund_solver)
        >>> signature.hash()
        "2993414225f65390220730d0c1a356c14e91bca76db112d37366df93e364a492"
        """

        if self.transaction is None:
            raise ValueError("transaction script is none, sign first")
        return self.transaction["hash"]

    # Transaction json
    def json(self):
        """
        Get Bytom signature transaction json format.

        :returns: dict -- Bytom signature transaction json format.

        >>> from shuttle.providers.bytom.signature import Signature
        >>> from shuttle.providers.bytom.solver import FundSolver
        >>> bytom_fund_unsigned_raw = "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInVuc2lnbmVkIjogW3siZGF0YXMiOiBbIjM4NjAxYmY3Y2UwOGRhYjkyMTkxNmYyYzcyM2FjY2EwNDUxZDg5MDQ2NDliYmVjMTZjMjA3NmYxNDU1ZGQxYTIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgImhhc2giOiAiNzY0NzIyOGFlM2MxNGQ5OGI4N2JkOWE2ZWI5NGJiMjgzMjkxMzUzZWE2MmFjZDIxYWQzNTMxMWFlOTEwZWY2ZiIsICJyYXciOiAiMDcwMTAwMDEwMTYwMDE1ZWU1MDFhOTdlMTQ0OWExYTg5OTI1ZGYxMjU5ZWJmMWUxYzhmYmIyM2E2MTA3MmNmMzQ0YmIzMmVlNjc2YjY2YmRmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZTBkYjg4YzcwNzAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDE0NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDAwMTNkZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmQwZTBhNWMyMDcwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEwMCIsICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieXRvbV9mdW5kX3Vuc2lnbmVkIn0"
        >>> fund_solver = FundSolver(xprivate_key="205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
        >>> signature = Signature(network="testnet")
        >>> signature.sign(bytom_fund_unsigned_raw, fund_solver)
        >>> signature.json()
        {"hash": "2993414225f65390220730d0c1a356c14e91bca76db112d37366df93e364a492", "status_fail": false, "size": 379, "submission_timestamp": 0, "memo": "", "inputs": [{"script": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 2450000000, "type": "spend"}], "outputs": [{"utxo_id": "5edccebe497893c289121f9e365fdeb34c97008b9eb5a9960fe9541e7923aabc", "script": "01642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0", "address": "smart contract", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 1000, "type": "control"}, {"utxo_id": "f8cfbb692db1963be88b09c314adcc9e19d91c6c019aa556fb7cb76ba8ffa1fa", "script": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 2439999000, "type": "control"}], "fee": 10000000, "balances": [{"asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": "-10001000"}], "types": ["ordinary"]}
        """
        if self.transaction is None:
            raise ValueError("transaction script is none, sign first")
        return decode_tx_raw(tx_raw=self.transaction["raw"])

    # Transaction raw
    def raw(self):
        """
        Get Bytom signature transaction raw.

        :returns: str -- Bytom signature transaction raw.

        >>> from shuttle.providers.bytom.signature import Signature
        >>> from shuttle.providers.bytom.solver import FundSolver
        >>> bytom_fund_unsigned_raw = "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInVuc2lnbmVkIjogW3siZGF0YXMiOiBbIjM4NjAxYmY3Y2UwOGRhYjkyMTkxNmYyYzcyM2FjY2EwNDUxZDg5MDQ2NDliYmVjMTZjMjA3NmYxNDU1ZGQxYTIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgImhhc2giOiAiNzY0NzIyOGFlM2MxNGQ5OGI4N2JkOWE2ZWI5NGJiMjgzMjkxMzUzZWE2MmFjZDIxYWQzNTMxMWFlOTEwZWY2ZiIsICJyYXciOiAiMDcwMTAwMDEwMTYwMDE1ZWU1MDFhOTdlMTQ0OWExYTg5OTI1ZGYxMjU5ZWJmMWUxYzhmYmIyM2E2MTA3MmNmMzQ0YmIzMmVlNjc2YjY2YmRmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZTBkYjg4YzcwNzAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDE0NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDAwMTNkZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmQwZTBhNWMyMDcwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEwMCIsICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieXRvbV9mdW5kX3Vuc2lnbmVkIn0"
        >>> fund_solver = FundSolver(xprivate_key="205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
        >>> signature = Signature(network="testnet")
        >>> signature.sign(bytom_fund_unsigned_raw, fund_solver)
        >>> signature.raw()
        "070100010160015e7f2d7ecec3f61d30d0b2968973a3ac8448f0599ea20dce883b48c903c4d6e87fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8091a0900901011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a22012091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e20201ad01ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe80701880101642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c000013dffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff98dcbd8b09011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a00"
        """

        if self.transaction is None:
            raise ValueError("transaction script is none, build transaction first")
        return self.transaction["raw"]

    def type(self):
        """
        Get Bytom signature transaction type.

        :returns: str -- Bytom signature transaction type.

        >>> from shuttle.providers.bytom.signature import Signature
        >>> from shuttle.providers.bytom.solver import FundSolver
        >>> bytom_fund_unsigned_raw = "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInVuc2lnbmVkIjogW3siZGF0YXMiOiBbIjM4NjAxYmY3Y2UwOGRhYjkyMTkxNmYyYzcyM2FjY2EwNDUxZDg5MDQ2NDliYmVjMTZjMjA3NmYxNDU1ZGQxYTIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgImhhc2giOiAiNzY0NzIyOGFlM2MxNGQ5OGI4N2JkOWE2ZWI5NGJiMjgzMjkxMzUzZWE2MmFjZDIxYWQzNTMxMWFlOTEwZWY2ZiIsICJyYXciOiAiMDcwMTAwMDEwMTYwMDE1ZWU1MDFhOTdlMTQ0OWExYTg5OTI1ZGYxMjU5ZWJmMWUxYzhmYmIyM2E2MTA3MmNmMzQ0YmIzMmVlNjc2YjY2YmRmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZTBkYjg4YzcwNzAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDE0NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDAwMTNkZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmQwZTBhNWMyMDcwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEwMCIsICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieXRvbV9mdW5kX3Vuc2lnbmVkIn0"
        >>> fund_solver = FundSolver(xprivate_key="205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
        >>> signature = Signature(network="testnet")
        >>> signature.sign(bytom_fund_unsigned_raw, fund_solver)
        >>> signature.type()
        "bytom_fund_signed"
        """

        if self._type is None:
            raise ValueError("not found type, sign first")
        return self._type

    def sign(self, unsigned_raw, solver):
        """
        Sign unsigned transaction raw.

        :param unsigned_raw: Bytom unsigned transaction raw.
        :type unsigned_raw: str
        :param solver: Bytom solver
        :type solver: bytom.solver.FundSolver, bytom.solver.ClaimSolver, bytom.solver.RefundSolver
        :returns:  FundSignature, ClaimSignature, RefundSignature -- Bytom signature instance.

        >>> from shuttle.providers.bytom.signature import Signature
        >>> from shuttle.providers.bytom.solver import FundSolver
        >>> bytom_fund_unsigned_raw = "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInVuc2lnbmVkIjogW3siZGF0YXMiOiBbIjM4NjAxYmY3Y2UwOGRhYjkyMTkxNmYyYzcyM2FjY2EwNDUxZDg5MDQ2NDliYmVjMTZjMjA3NmYxNDU1ZGQxYTIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgImhhc2giOiAiNzY0NzIyOGFlM2MxNGQ5OGI4N2JkOWE2ZWI5NGJiMjgzMjkxMzUzZWE2MmFjZDIxYWQzNTMxMWFlOTEwZWY2ZiIsICJyYXciOiAiMDcwMTAwMDEwMTYwMDE1ZWU1MDFhOTdlMTQ0OWExYTg5OTI1ZGYxMjU5ZWJmMWUxYzhmYmIyM2E2MTA3MmNmMzQ0YmIzMmVlNjc2YjY2YmRmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZTBkYjg4YzcwNzAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDE0NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDAwMTNkZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmQwZTBhNWMyMDcwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEwMCIsICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieXRvbV9mdW5kX3Vuc2lnbmVkIn0"
        >>> fund_solver = FundSolver(xprivate_key="205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
        >>> signature = Signature(network="testnet")
        >>> signature.sign(bytom_fund_unsigned_raw, fund_solver)
        <shuttle.providers.bytom.signature.FundSignature object at 0x0409DAF0>
        """

        transaction = json.loads(b64decode(
            str(unsigned_raw + "=" * (-len(unsigned_raw) % 4)).encode()).decode())
        if "type" not in transaction:
            raise ValueError("invalid Bytom unsigned transaction raw")
        self._type = transaction["type"]
        if transaction["type"] == "bytom_fund_unsigned":
            return FundSignature(network=self.network)\
                .sign(unsigned_raw=unsigned_raw, solver=solver)
        elif transaction["type"] == "bytom_claim_unsigned":
            return ClaimSignature(network=self.network)\
                .sign(unsigned_raw=unsigned_raw, solver=solver)
        elif transaction["type"] == "bytom_refund_unsigned":
            return RefundSignature(network=self.network)\
                .sign(unsigned_raw=unsigned_raw, solver=solver)

    def unsigned_datas(self, *args, **kwargs):
        """
        Get Bytom transaction unsigned datas with instruction.

        :returns: list -- Bytom transaction unsigned datas.

        >>> from shuttle.providers.bytom.signature import Signature
        >>> from shuttle.providers.bytom.solver import FundSolver
        >>> bytom_fund_unsigned_raw = "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInVuc2lnbmVkIjogW3siZGF0YXMiOiBbIjM4NjAxYmY3Y2UwOGRhYjkyMTkxNmYyYzcyM2FjY2EwNDUxZDg5MDQ2NDliYmVjMTZjMjA3NmYxNDU1ZGQxYTIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgImhhc2giOiAiNzY0NzIyOGFlM2MxNGQ5OGI4N2JkOWE2ZWI5NGJiMjgzMjkxMzUzZWE2MmFjZDIxYWQzNTMxMWFlOTEwZWY2ZiIsICJyYXciOiAiMDcwMTAwMDEwMTYwMDE1ZWU1MDFhOTdlMTQ0OWExYTg5OTI1ZGYxMjU5ZWJmMWUxYzhmYmIyM2E2MTA3MmNmMzQ0YmIzMmVlNjc2YjY2YmRmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZTBkYjg4YzcwNzAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDE0NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDAwMTNkZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmQwZTBhNWMyMDcwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEwMCIsICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieXRvbV9mdW5kX3Vuc2lnbmVkIn0"
        >>> fund_solver = FundSolver(xprivate_key="205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
        >>> signature = Signature(network="testnet")
        >>> signature.sign(bytom_fund_unsigned_raw, fund_solver)
        >>> signature.unsigned_datas()
        [{'datas': ['38601bf7ce08dab921916f2c723acca0451d8904649bbec16c2076f1455dd1a2'], 'public_key': '91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2', 'network': 'mainnet', 'path': 'm/44/153/1/0/1'}]
        """

        if self.transaction is None:
            raise ValueError("transaction script is none, build transaction first")
        return self.transaction["unsigned_datas"]

    def signed_raw(self):
        """
        Get Bytom signed transaction raw.

        :returns: str -- Bytom signed transaction raw.

        >>> from shuttle.providers.bytom.signature import Signature
        >>> from shuttle.providers.bytom.solver import FundSolver
        >>> bytom_fund_unsigned_raw = "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInVuc2lnbmVkIjogW3siZGF0YXMiOiBbIjM4NjAxYmY3Y2UwOGRhYjkyMTkxNmYyYzcyM2FjY2EwNDUxZDg5MDQ2NDliYmVjMTZjMjA3NmYxNDU1ZGQxYTIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgImhhc2giOiAiNzY0NzIyOGFlM2MxNGQ5OGI4N2JkOWE2ZWI5NGJiMjgzMjkxMzUzZWE2MmFjZDIxYWQzNTMxMWFlOTEwZWY2ZiIsICJyYXciOiAiMDcwMTAwMDEwMTYwMDE1ZWU1MDFhOTdlMTQ0OWExYTg5OTI1ZGYxMjU5ZWJmMWUxYzhmYmIyM2E2MTA3MmNmMzQ0YmIzMmVlNjc2YjY2YmRmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZTBkYjg4YzcwNzAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDE0NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDAwMTNkZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmQwZTBhNWMyMDcwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEwMCIsICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieXRvbV9mdW5kX3Vuc2lnbmVkIn0"
        >>> fund_solver = FundSolver(xprivate_key="205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
        >>> signature = Signature(network="testnet")
        >>> signature.sign(bytom_fund_unsigned_raw, fund_solver)
        >>> signature.signed_raw()
        "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTJjMzkyMjE3NDgzOTA2ZjkwMmU3M2M0YmMxMzI4NjRkZTU4MTUzNzcyZDc5MjY4OTYwOTk4MTYyMjY2NjM0YmUwMTAwMDAwMDAwZmZmZmZmZmYwMmU4MDMwMDAwMDAwMDAwMDAxN2E5MTQ5NzE4OTRjNThkODU5ODFjMTZjMjA1OWQ0MjJiY2RlMGIxNTZkMDQ0ODdhNjI5MDAwMDAwMDAwMDAwMTk3NmE5MTQ2YmNlNjVlNThhNTBiOTc5ODk5MzBlOWE0ZmYxYWMxYTc3NTE1ZWYxODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiAxMjM0MCwgIm4iOiAxLCAic2NyaXB0IjogIjc2YTkxNDZiY2U2NWU1OGE1MGI5Nzk4OTkzMGU5YTRmZjFhYzFhNzc1MTVlZjE4OGFjIn1dLCAidHlwZSI6ICJiaXRjb2luX2Z1bmRfdW5zaWduZWQifQ"
        """

        if self._signed_raw is None:
            raise ValueError("there is no signed data, sign first")
        return self._signed_raw


# Fund signature
class FundSignature(Signature):
    """
    Bytom FundSignature class.

    :param network: Bytom network, defaults to testnet.
    :type network: str
    :returns:  FundSignature -- Bytom fund signature instance.
    """

    def __init__(self, network="testnet"):
        super().__init__(network=network)

    def sign(self, unsigned_raw, solver):
        """
        Sign unsigned fund transaction raw.

        :param unsigned_raw: Bytom unsigned fund transaction raw.
        :type unsigned_raw: str
        :param solver: Bytom fund solver.
        :type solver: bytom.solver.FundSolver
        :returns:  FundSignature -- Bytom fund signature instance.

        >>> from shuttle.providers.bytom.signature import FundSignature
        >>> from shuttle.providers.bytom.solver import FundSolver
        >>> bytom_fund_unsigned_raw = "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInVuc2lnbmVkIjogW3siZGF0YXMiOiBbIjM4NjAxYmY3Y2UwOGRhYjkyMTkxNmYyYzcyM2FjY2EwNDUxZDg5MDQ2NDliYmVjMTZjMjA3NmYxNDU1ZGQxYTIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgImhhc2giOiAiNzY0NzIyOGFlM2MxNGQ5OGI4N2JkOWE2ZWI5NGJiMjgzMjkxMzUzZWE2MmFjZDIxYWQzNTMxMWFlOTEwZWY2ZiIsICJyYXciOiAiMDcwMTAwMDEwMTYwMDE1ZWU1MDFhOTdlMTQ0OWExYTg5OTI1ZGYxMjU5ZWJmMWUxYzhmYmIyM2E2MTA3MmNmMzQ0YmIzMmVlNjc2YjY2YmRmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZTBkYjg4YzcwNzAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDE0NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDAwMTNkZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmQwZTBhNWMyMDcwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEwMCIsICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieXRvbV9mdW5kX3Vuc2lnbmVkIn0"
        >>> fund_solver = FundSolver("205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b")
        >>> fund_signature = FundSignature(network="testnet")
        >>> fund_signature.sign(bytom_fund_unsigned_raw, fund_solver)
        <shuttle.providers.bytom.signature.FundSignature object at 0x0409DAF0>
        """
        
        # Decoding and loading fund transaction
        fund_transaction = json.loads(b64decode(
            str(unsigned_raw + "=" * (-len(unsigned_raw) % 4)).encode()).decode())
        # Checking fund transaction keys
        for key in ["raw", "unsigned_datas", "type", "fee", "network"]:
            if key not in fund_transaction:
                raise ValueError("invalid Bytom unsigned fund transaction raw")
        if not fund_transaction["type"] == "bytom_fund_unsigned":
            raise TypeError(f"invalid Bytom fund unsigned transaction type, "
                            f"you can't sign this {fund_transaction['type']} type by using FundSignature")
        if not isinstance(solver, FundSolver):
            raise TypeError("invalid Bytom solver, it's only takes Bytom FundSolver class")

        # Setting transaction fee, type, network and transaction
        self._fee, self._type, self.network, self.transaction = (
            fund_transaction["fee"], fund_transaction["type"],
            fund_transaction["network"], fund_transaction
        )

        # Setting sender wallet
        wallet = solver.solve()
        wallet.clean_derivation()  # Cleaning any derivation indexes/path
        # Signing refund transaction
        for unsigned in self.unsigned_datas():
            signed_data = list()
            unsigned_datas = unsigned["datas"]
            if unsigned["path"]:
                wallet.from_path(unsigned["path"])
            elif solver.path:
                wallet.from_path(solver.path)
            elif solver.indexes:
                wallet.from_indexes(solver.indexes)
            for unsigned_data in unsigned_datas:
                signed_data.append(wallet.sign(unsigned_data))
            self._signatures.append(signed_data)
            wallet.clean_derivation()

        # Encoding fund transaction raw
        self._type = "bytom_fund_signed"
        self._signed_raw = b64encode(str(json.dumps(dict(
            fee=self.fee(),
            guid=self.transaction["guid"],
            raw=self.raw(),
            hash=self.hash(),
            unsigned_datas=self.unsigned_datas(),
            network=self.network,
            signatures=self.signatures(),
            type=self.type()
        ))).encode()).decode()
        return self


# Claim signature
class ClaimSignature(Signature):
    """
    Bytom ClaimSignature class.

    :param network: Bytom network, defaults to testnet.
    :type network: str
    :returns:  ClaimSignature -- Bytom claim signature instance.
    """

    def __init__(self, network="testnet"):
        super().__init__(network=network)

    def sign(self, unsigned_raw, solver):
        """
        Sign unsigned claim transaction raw.

        :param unsigned_raw: Bytom unsigned claim transaction raw.
        :type unsigned_raw: str
        :param solver: Bytom claim solver.
        :type solver: bytom.solver.ClaimSolver
        :returns:  ClaimSignature -- Bytom claim signature instance.

        >>> from shuttle.providers.bytom.signature import ClaimSignature
        >>> from shuttle.providers.bytom.solver import ClaimSolver
        >>> bytom_claim_unsigned_raw = "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInVuc2lnbmVkIjogW3siZGF0YXMiOiBbIjM4NjAxYmY3Y2UwOGRhYjkyMTkxNmYyYzcyM2FjY2EwNDUxZDg5MDQ2NDliYmVjMTZjMjA3NmYxNDU1ZGQxYTIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgImhhc2giOiAiNzY0NzIyOGFlM2MxNGQ5OGI4N2JkOWE2ZWI5NGJiMjgzMjkxMzUzZWE2MmFjZDIxYWQzNTMxMWFlOTEwZWY2ZiIsICJyYXciOiAiMDcwMTAwMDEwMTYwMDE1ZWU1MDFhOTdlMTQ0OWExYTg5OTI1ZGYxMjU5ZWJmMWUxYzhmYmIyM2E2MTA3MmNmMzQ0YmIzMmVlNjc2YjY2YmRmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZTBkYjg4YzcwNzAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDE0NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDAwMTNkZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmQwZTBhNWMyMDcwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEwMCIsICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieXRvbV9mdW5kX3Vuc2lnbmVkIn0"
        >>> recipient_xprivate_key = "58dd4094155bbebf2868189231c47e4e0edbd9f74545f843c9537259e1d7a656983aef283d0ccebecc2d33577a9f650b53ac7adff44f48ec839e3346cc22418f"
        >>> claim_solver = ClaimSolver(recipient_xprivate_key, "Hello Meheret!", "3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb", "3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2", 1000)
        >>> claim_signature = ClaimSignature(network="testnet")
        >>> claim_signature.sign(bytom_claim_unsigned_raw, claim_solver)
        <shuttle.providers.bytom.signature.ClaimSignature object at 0x0409DAF0>
        """

        # Decoding and loading claim transaction
        claim_transaction = json.loads(b64decode(
            str(unsigned_raw + "=" * (-len(unsigned_raw) % 4)).encode()).decode())
        # Checking claim transaction keys
        for key in ["raw", "unsigned_datas", "type", "fee", "network"]:
            if key not in claim_transaction:
                raise ValueError("invalid Bytom unsigned claim transaction raw")
        if not claim_transaction["type"] == "bytom_claim_unsigned":
            raise TypeError(f"invalid Bytom claim unsigned transaction type, "
                            f"you can't sign this {claim_transaction['type']} type by using ClaimSignature")
        if not isinstance(solver, ClaimSolver):
            raise TypeError("invalid Bytom solver, it's only takes Bytom ClaimSolver class")

        # Setting transaction fee, type, network and transaction
        self._fee, self._type, self.network, self.transaction = (
            claim_transaction["fee"], claim_transaction["type"],
            claim_transaction["network"], claim_transaction,
        )

        # Setting recipient wallet
        wallet = solver.solve()
        wallet.clean_derivation()  # Cleaning any derivation indexes/path
        # Signing claim transaction
        for index, unsigned in enumerate(self.unsigned_datas()):
            signed_data = list()
            unsigned_datas = unsigned["datas"]
            if unsigned["path"]:
                wallet.from_path(unsigned["path"])
            elif solver.path:
                wallet.from_path(solver.path)
            elif solver.indexes:
                wallet.from_indexes(solver.indexes)
            for unsigned_data in unsigned_datas:
                if index == 0:
                    signed_data.append(bytearray(solver.secret.encode()).hex())
                    signed_data.append(wallet.sign(unsigned_data))
                    signed_data.append(str("00"))
                    signed_data.append(solver.witness(self.network, False))
                else:
                    signed_data.append(wallet.sign(unsigned_data))
            self._signatures.append(signed_data)
            wallet.clean_derivation()

        # Encoding claim transaction raw
        self._type = "bytom_claim_signed"
        self._signed_raw = b64encode(str(json.dumps(dict(
            fee=self.fee(),
            guid=self.transaction["guid"],
            raw=self.raw(),
            hash=self.hash(),
            unsigned_datas=self.unsigned_datas(),
            network=self.network,
            signatures=self.signatures(),
            type=self.type()
        ))).encode()).decode()
        return self


# Refund signature
class RefundSignature(Signature):
    """
    Bytom RefundSignature class.

    :param network: Bytom network, defaults to testnet.
    :type network: str
    :returns:  RefundSignature -- Bytom claim signature instance.
    """

    def __init__(self, network="testnet"):
        super().__init__(network=network)

    def sign(self, unsigned_raw, solver):
        """
        Sign unsigned refund transaction raw.

        :param unsigned_raw: Bytom unsigned refund transaction raw.
        :type unsigned_raw: str
        :param solver: Bytom refund solver.
        :type solver: bytom.solver.RefundSolver
        :returns:  RefundSignature -- Bytom refund signature instance.

        >>> from shuttle.providers.bytom.signature import RefundSignature
        >>> from shuttle.providers.bytom.solver import RefundSolver
        >>> bytom_refund_unsigned_raw = "eyJmZWUiOiAxMDAwMDAwMCwgImd1aWQiOiAiZjBlZDZkZGQtOWQ2Yi00OWZkLTg4NjYtYTUyZDEwODNhMTNiIiwgInVuc2lnbmVkIjogW3siZGF0YXMiOiBbIjM4NjAxYmY3Y2UwOGRhYjkyMTkxNmYyYzcyM2FjY2EwNDUxZDg5MDQ2NDliYmVjMTZjMjA3NmYxNDU1ZGQxYTIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgImhhc2giOiAiNzY0NzIyOGFlM2MxNGQ5OGI4N2JkOWE2ZWI5NGJiMjgzMjkxMzUzZWE2MmFjZDIxYWQzNTMxMWFlOTEwZWY2ZiIsICJyYXciOiAiMDcwMTAwMDEwMTYwMDE1ZWU1MDFhOTdlMTQ0OWExYTg5OTI1ZGYxMjU5ZWJmMWUxYzhmYmIyM2E2MTA3MmNmMzQ0YmIzMmVlNjc2YjY2YmRmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZTBkYjg4YzcwNzAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDE0NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDAwMTNkZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmQwZTBhNWMyMDcwMTE2MDAxNDJjZGE0Zjk5ZWE4MTEyZTZmYTYxY2RkMjYxNTdlZDZkYzQwODMzMmEwMCIsICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieXRvbV9mdW5kX3Vuc2lnbmVkIn0"
        >>> sender_xprivate_key = "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"
        >>> refund_solver = RefundSolver(sender_xprivate_key, "3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb", "3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2", 1000)
        >>> refund_signature = RefundSignature(network="testnet")
        >>> refund_signature.sign(bytom_refund_unsigned_raw, refund_solver)
        <shuttle.providers.bytom.signature.RefundSignature object at 0x0409DAF0>
        """

        # Decoding and loading refund transaction
        refund_transaction = json.loads(b64decode(
            str(unsigned_raw + "=" * (-len(unsigned_raw) % 4)).encode()).decode())
        # Checking refund transaction keys
        for key in ["raw", "unsigned_datas", "type", "fee", "network"]:
            if key not in refund_transaction:
                raise ValueError("invalid Bytom unsigned refund transaction raw")
        if not refund_transaction["type"] == "bytom_refund_unsigned":
            raise TypeError(f"invalid Bytom refund unsigned transaction type, "
                            f"you can't sign this {refund_transaction['type']} type by using RefundSignature")
        if not isinstance(solver, RefundSolver):
            raise TypeError("invalid Bytom solver, it's only takes Bytom RefundSolver class")

        # Setting transaction fee, type, network and transaction
        self._fee, self._type, self.network, self.transaction = (
            refund_transaction["fee"], refund_transaction["type"],
            refund_transaction["network"], refund_transaction
        )

        # Setting sender wallet
        wallet = solver.solve()
        wallet.clean_derivation()  # Cleaning any derivation indexes/path
        # Signing refund transaction
        for index, unsigned in enumerate(self.unsigned_datas()):
            signed_data = list()
            unsigned_datas = unsigned["datas"]
            if unsigned["path"]:
                wallet.from_path(unsigned["path"])
            elif solver.path:
                wallet.from_path(solver.path)
            elif solver.indexes:
                wallet.from_indexes(solver.indexes)
            for unsigned_data in unsigned_datas:
                if index == 0:
                    signed_data.append(wallet.sign(unsigned_data))
                    signed_data.append(str("01"))
                    signed_data.append(solver.witness(self.network, False))
                else:
                    signed_data.append(wallet.sign(unsigned_data))
            self._signatures.append(signed_data)
            wallet.clean_derivation()

        # Encoding refund transaction raw
        self._type = "bytom_refund_signed"
        self._signed_raw = b64encode(str(json.dumps(dict(
            fee=self.fee(),
            guid=self.transaction["guid"],
            raw=self.raw(),
            hash=self.hash(),
            unsigned_datas=self.unsigned_datas(),
            network=self.network,
            signatures=self.signatures(),
            type=self.type()
        ))).encode()).decode()
        return self
