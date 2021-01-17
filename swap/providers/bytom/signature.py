#!/usr/bin/env python3

from base64 import (
    b64encode, b64decode
)
from typing import (
    Optional, Union, List
)

import json

from ...utils import clean_transaction_raw
from ...exceptions import (
    TransactionRawError, NetworkError, UnitError
)
from ..config import bytom as config
from .transaction import Transaction
from .solver import (
    NormalSolver, FundSolver, ClaimSolver, RefundSolver
)
from .rpc import decode_raw
from .utils import (
    is_network, is_transaction_raw, amount_unit_converter
)


class Signature(Transaction):
    """
    Bytom Signature.

    :param network: Bytom network, defaults to mainnet.
    :type network: str

    :returns: Signature -- Bytom signature instance.

    .. note::
        Bytom has only three networks, ``mainnet``, ``solonet`` and ``testnet``.
    """

    def __init__(self, network: str = config["network"]):

        if not is_network(network=network):
            raise NetworkError(f"Invalid Bytom '{network}' network",
                               "choose only 'mainnet', 'solonet' or 'testnet' networks.")

        self._network: str = network
        self._address: Optional[str] = None
        self._transaction: Optional[dict] = None
        self._type: Optional[str] = None
        self._datas: dict = {}
        self._confirmations: int = config["confirmations"]
        self._signed_raw: Optional[str] = None
        self._fee: int = 0

        super().__init__(network)

    def fee(self, unit: str = config["unit"]) -> Union[int, float]:
        """
        Get Bytom transaction fee.

        :param unit: Bytom unit, default to NEU.
        :type unit: str

        :returns: int, float -- Bytom transaction fee.

        >>> from swap.providers.bytom.signature import Signature
        >>> from swap.providers.bytom.solver import FundSolver
        >>> unsigned_fund_transaction_raw = "eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcTluZHlseDAyc3lmd2Q3bnBlaGZ4ejRsZGRoenFzdmUyZnU2dmM3IiwgInJhdyI6ICIwNzAxMDAwMjAxNWYwMTVkODJlNjVmOTY0ZDNjMzUzMjU0OGRmZGU5Mzg0NjJmNTY2Yzk1ZDNjOTBlNmEzYTE4MmEwYjNiZGFlNDZhYTc5MGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MDg2ZjIwMzAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAxNWYwMTVkMDcwZDBlYjIyZDMyYjgyZDNkMmYzZmM0YmFmYjdhODVmNTIyOWY3ZmQ4OTA0MmQyZmYzMjU3Mzc1ZTQzZDNlYmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOGY1Zjc0ZjAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDE0NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDAwMTNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmQ4YjhmODUyMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAiaGFzaCI6ICI1MGIzMzZhYjZlMDU1ZDlkNGQ2NWE5ZjIyOTViNTMyNzBhYmQzODE2YzIzYmE0Yzk1NDg0MWYzOTlhYTc3MmQ1IiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbImY3ZDNhYTE4YjI5NWNkYTZmMmIxMTMyYzQyMzE5MzNjYzkyZjNiYWNhNzA1OTc0YzVkZTM3OGY5YjY5NWYwZTIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9LCB7ImRhdGFzIjogWyJjYTYxNWJhMmM3MjllNDYzZmJmNzlhMTE0MTkxNzYyNjFiMWJmNmJlNDQ4MTMzMzVkMmIyNTZlOGE3YmJjZWVlIl0sICJwdWJsaWNfa2V5IjogIjkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieXRvbV9mdW5kX3Vuc2lnbmVkIn0"
        >>> sender_xprivate_key = "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"
        >>> fund_solver = FundSolver(sender_xprivate_key)
        >>> signature = Signature("mainnet")
        >>> signature.sign(unsigned_fund_transaction_raw, fund_solver)
        >>> signature.fee(unit="BTM")
        0.1
        """

        if self._transaction is None:
            raise ValueError("Transaction is none, sign unsigned transaction raw first.")
        if unit not in ["BTM", "mBTM", "NEU"]:
            raise UnitError("Invalid Bytom unit, choose only BTM, mBTM or NEU units.")
        return self._fee if unit == "NEU" else \
            amount_unit_converter(amount=self._fee, unit_from=f"NEU2{unit}")

    def hash(self) -> str:
        """
        Get Bytom signature transaction hash.

        :returns: str -- Bytom signature transaction hash or transaction id.

        >>> from swap.providers.bytom.signature import Signature
        >>> from swap.providers.bytom.solver import ClaimSolver
        >>> unsigned_claim_transaction_raw = "eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcTNwbHd2bXZ5NHFoam1wNXpmZnptazUwYWFncHVqdDZmNWplODVwIiwgInJhdyI6ICIwNzAxMDAwMjAxNWYwMTVkMzA1YTI4ZDhkMzRiNDBjNjU5MzY4MTBmOWU5YzFmOGJjOWM3OTNlYzJlNzJjNzBmOTIwM2ZiYmViMGE1NmRiOWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGFkZTIwNDAxMDExNjAwMTQwZTQzYTkyYTllOGFjYTc4OGViMTU1MWMzMTY0NDhjMmUzZjc4MjE1MDEwMDAxNWQwMTViMTM4ODFmMzI3ZTJiZTBkNWMwMGYzODU2MGYxYzI5NDg2Y2RhZjI1NWMwOWMwMWVlZTFhMWViYWEzNzgzZGRkOWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDAwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkyMjAxMjAzZTBhMzc3YWU0YWZhMDMxZDQ1NTE1OTlkOWJiN2Q1YjI3ZjQ3MzZkNzdmNzhjYWM0ZDQ3NmYwZmZiYTVhZTNlMDIwMTNhZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjkwNGUwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkwMDAxM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjBkZWUxMDQwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkwMCIsICJoYXNoIjogImQ1NDRhZDJkMDhmOWRkYTMzYjc4OTUzYzc0ZWVkZTljOWViNWQ4MDgzNTY5NTMxMGIyNDJkNTc5NmNmYjkxZDYiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiNTE3MjI5MGE5ODU4YTRhMDdjNjAzYzc0MWY2ZmQ4ZTg2NzE1YThhNDQ3MGViMjM3ZDBhMmQ4MzI1YzE3MDZiNyJdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiBudWxsfSwgeyJkYXRhcyI6IFsiZTQxYWI5NjQ3MDFmMjBhMjM0NzMzNDBiMTFkNWNiY2ZiYTlhMzczY2VkZjI4NGY4MDljMGM2MWNlN2Q3MTVkYSJdLCAicHVibGljX2tleSI6ICIzZTBhMzc3YWU0YWZhMDMxZDQ1NTE1OTlkOWJiN2Q1YjI3ZjQ3MzZkNzdmNzhjYWM0ZDQ3NmYwZmZiYTVhZTNlIiwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogIm0vNDQvMTUzLzEvMC8xIn1dLCAic2lnbmF0dXJlcyI6IFtdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInR5cGUiOiAiYnl0b21fY2xhaW1fdW5zaWduZWQifQ"
        >>> recipient_xprivate_key = "58dd4094155bbebf2868189231c47e4e0edbd9f74545f843c9537259e1d7a656983aef283d0ccebecc2d33577a9f650b53ac7adff44f48ec839e3346cc22418f"
        >>> bytecode = "02e8032091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"
        >>> claim_solver = ClaimSolver(recipient_xprivate_key, "Hello Meheret!", bytecode)
        >>> signature = Signature("mainnet")
        >>> signature.sign(unsigned_claim_transaction_raw, claim_solver)
        >>> signature.hash()
        "d544ad2d08f9dda33b78953c74eede9c9eb5d80835695310b242d5796cfb91d6"
        """

        if self._transaction is None:
            raise ValueError("Transaction is none, sign unsigned transaction raw first.")
        return self._transaction["hash"]

    def json(self) -> dict:
        """
        Get Bytom signature transaction json format.

        :returns: dict -- Bytom signature transaction json format.

        >>> from swap.providers.bytom.signature import Signature
        >>> from swap.providers.bytom.solver import FundSolver
        >>> unsigned_fund_transaction_raw = "eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcTluZHlseDAyc3lmd2Q3bnBlaGZ4ejRsZGRoenFzdmUyZnU2dmM3IiwgInJhdyI6ICIwNzAxMDAwMjAxNWYwMTVkODJlNjVmOTY0ZDNjMzUzMjU0OGRmZGU5Mzg0NjJmNTY2Yzk1ZDNjOTBlNmEzYTE4MmEwYjNiZGFlNDZhYTc5MGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MDg2ZjIwMzAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAxNWYwMTVkMDcwZDBlYjIyZDMyYjgyZDNkMmYzZmM0YmFmYjdhODVmNTIyOWY3ZmQ4OTA0MmQyZmYzMjU3Mzc1ZTQzZDNlYmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOGY1Zjc0ZjAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDE0NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDAwMTNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmQ4YjhmODUyMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAiaGFzaCI6ICI1MGIzMzZhYjZlMDU1ZDlkNGQ2NWE5ZjIyOTViNTMyNzBhYmQzODE2YzIzYmE0Yzk1NDg0MWYzOTlhYTc3MmQ1IiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbImY3ZDNhYTE4YjI5NWNkYTZmMmIxMTMyYzQyMzE5MzNjYzkyZjNiYWNhNzA1OTc0YzVkZTM3OGY5YjY5NWYwZTIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9LCB7ImRhdGFzIjogWyJjYTYxNWJhMmM3MjllNDYzZmJmNzlhMTE0MTkxNzYyNjFiMWJmNmJlNDQ4MTMzMzVkMmIyNTZlOGE3YmJjZWVlIl0sICJwdWJsaWNfa2V5IjogIjkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieXRvbV9mdW5kX3Vuc2lnbmVkIn0"
        >>> sender_xprivate_key = "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"
        >>> fund_solver = FundSolver(sender_xprivate_key)
        >>> signature = Signature("mainnet")
        >>> signature.sign(unsigned_fund_transaction_raw, fund_solver)
        >>> signature.json()
        {"tx_id": "50b336ab6e055d9d4d65a9f2295b53270abd3816c23ba4c954841f399aa772d5", "version": 1, "size": 405, "time_range": 0, "inputs": [{"type": "spend", "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "asset_definition": {}, "amount": 8160000, "control_program": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "spent_output_id": "88289fa4c7633574931be7ce4102aeb24def0de20e38e7d69a5ddd6efc116b95", "input_id": "49e97e1685d5b08b82713e6acb6747bd176177141cb5618aeecca418c3afd03a", "witness_arguments": ["91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2"], "sign_data": "f7d3aa18b295cda6f2b1132c4231933cc92f3baca705974c5de378f9b695f0e2"}, {"type": "spend", "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "asset_definition": {}, "amount": 167639800, "control_program": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "spent_output_id": "d0cc73f664fdda20d6a9bb6f4c0204f30e738959b02f3b645ad17d190fafd5b3", "input_id": "d8729c2683f56cb50ee65c12484edfb4ea8182f71b11de84dfaf5cc05ccde47b", "witness_arguments": ["91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2"], "sign_data": "ca615ba2c729e463fbf79a11419176261b1bf6be44813335d2b256e8a7bbceee"}], "outputs": [{"type": "control", "id": "9c8c0b8ceaba9bea5ffe12fc51ac5ef82f1da6bebde537ab7d621845d1182151", "position": 0, "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "asset_definition": {}, "amount": 10000, "control_program": "00204f8f0e88d0a44b3d884b07b6dd4536518ffcbb596a91ca0e6b2f37e96463bbfc", "address": "bm1qf78sazxs539nmzztq7md63fk2x8lew6ed2gu5rnt9um7jerrh07q3yf5q8"}, {"type": "control", "id": "7dc2e56534ee173e0319020db5b05fd4450cab483f9b97f9b01dbc1879b1b8ff", "position": 1, "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "asset_definition": {}, "amount": 173939800, "control_program": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7"}], "fee": 1850000}
        """
        if self._transaction is None:
            raise ValueError("Transaction is none, sign unsigned transaction raw first.")
        return decode_raw(raw=self._transaction["raw"])

    def raw(self) -> str:
        """
        Get Bytom signature transaction raw.

        :returns: str -- Bytom signature transaction raw.

        >>> from swap.providers.bytom.signature import Signature
        >>> from swap.providers.bytom.solver import FundSolver
        >>> unsigned_fund_transaction_raw = "eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcTluZHlseDAyc3lmd2Q3bnBlaGZ4ejRsZGRoenFzdmUyZnU2dmM3IiwgInJhdyI6ICIwNzAxMDAwMjAxNWYwMTVkODJlNjVmOTY0ZDNjMzUzMjU0OGRmZGU5Mzg0NjJmNTY2Yzk1ZDNjOTBlNmEzYTE4MmEwYjNiZGFlNDZhYTc5MGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MDg2ZjIwMzAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAxNWYwMTVkMDcwZDBlYjIyZDMyYjgyZDNkMmYzZmM0YmFmYjdhODVmNTIyOWY3ZmQ4OTA0MmQyZmYzMjU3Mzc1ZTQzZDNlYmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOGY1Zjc0ZjAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDE0NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDAwMTNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmQ4YjhmODUyMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAiaGFzaCI6ICI1MGIzMzZhYjZlMDU1ZDlkNGQ2NWE5ZjIyOTViNTMyNzBhYmQzODE2YzIzYmE0Yzk1NDg0MWYzOTlhYTc3MmQ1IiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbImY3ZDNhYTE4YjI5NWNkYTZmMmIxMTMyYzQyMzE5MzNjYzkyZjNiYWNhNzA1OTc0YzVkZTM3OGY5YjY5NWYwZTIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9LCB7ImRhdGFzIjogWyJjYTYxNWJhMmM3MjllNDYzZmJmNzlhMTE0MTkxNzYyNjFiMWJmNmJlNDQ4MTMzMzVkMmIyNTZlOGE3YmJjZWVlIl0sICJwdWJsaWNfa2V5IjogIjkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieXRvbV9mdW5kX3Vuc2lnbmVkIn0"
        >>> sender_xprivate_key = "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"
        >>> fund_solver = FundSolver(sender_xprivate_key)
        >>> signature = Signature("mainnet")
        >>> signature.sign(unsigned_fund_transaction_raw, fund_solver)
        >>> signature.raw()
        "07010002015f015d82e65f964d3c3532548dfde938462f566c95d3c90e6a3a182a0b3bdae46aa790ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8086f20301011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a22012091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2015f015d070d0eb22d32b82d3d2f3fc4bafb7a85f5229f7fd89042d2ff3257375e43d3ebfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8f5f74f01011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a22012091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2020146ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff904e012200204f8f0e88d0a44b3d884b07b6dd4536518ffcbb596a91ca0e6b2f37e96463bbfc00013cffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffd8b8f852011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a00"
        """

        if self._transaction is None:
            raise ValueError("Transaction is none, sign unsigned transaction raw first.")
        return self._transaction["raw"]

    def type(self) -> str:
        """
        Get Bytom signature transaction type.

        :returns: str -- Bytom signature transaction type.

        >>> from swap.providers.bytom.signature import Signature
        >>> from swap.providers.bytom.solver import RefundSolver
        >>> unsigned_refund_transaction_raw = "eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcTluZHlseDAyc3lmd2Q3bnBlaGZ4ejRsZGRoenFzdmUyZnU2dmM3IiwgImhhc2giOiAiNjlhNWYzMDI4ODBhNzNkMzYzZWNiMzkyYzgyZGNkMzMyODNiZDFiYmU1NmFhMzAyODU4NzMzZTc5ZTE2Mzc5OCIsICJyYXciOiAiMDcwMTAwMDIwMTVmMDE1ZDMwNWEyOGQ4ZDM0YjQwYzY1OTM2ODEwZjllOWMxZjhiYzljNzkzZWMyZTcyYzcwZjkyMDNmYmJlYjBhNTZkYjlmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBhZGUyMDQwMTAxMTYwMDE0MGU0M2E5MmE5ZThhY2E3ODhlYjE1NTFjMzE2NDQ4YzJlM2Y3ODIxNTAxMDAwMTVmMDE1ZDgyZTY1Zjk2NGQzYzM1MzI1NDhkZmRlOTM4NDYyZjU2NmM5NWQzYzkwZTZhM2ExODJhMGIzYmRhZTQ2YWE3OTBmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODA4NmYyMDMwMTAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTIyMDEyMDkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIwMjAxM2FmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOTA0ZTAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTAwMDEzY2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZlMDk2ZDMwODAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTAwIiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbIjY0ODJiMmRmZTliM2U3NjY0MzVlMDQ4MmI2MDAzN2FmYWVhYmFhYWExMDg5Mzc0OGEyODhiY2EwMjlmZjFjNTIiXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBbIjBhNDY3NmE3MzI0MmNkMTI2NjFkYjBmM2Y3Mzc5NGQ0OWI3Nzc1NTBiZDk4MTc2YThkODhlYTg3NTVlNDE3ZjIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX3JlZnVuZF91bnNpZ25lZCJ9"
        >>> sender_xprivate_key = "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"
        >>> bytecode = "02e8032091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"
        >>> refund_solver = RefundSolver(sender_xprivate_key, bytecode, 1000)
        >>> signature = Signature("mainnet")
        >>> signature.sign(unsigned_refund_transaction_raw, refund_solver)
        >>> signature.type()
        "bytom_refund_signed"
        """

        if self._type is None:
            raise ValueError("Type is none, sign unsigned transaction raw first.")
        return self._type

    def sign(self, transaction_raw: str, solver: Union[NormalSolver, FundSolver, ClaimSolver, RefundSolver]) \
            -> Union["NormalSignature", "FundSignature", "ClaimSignature", "RefundSignature"]:
        """
        Sign unsigned transaction raw.

        :param transaction_raw: Bytom unsigned transaction raw.
        :type transaction_raw: str
        :param solver: Bytom solver
        :type solver: bytom.solver.NormalSolver, bytom.solver.FundSolver, bytom.solver.ClaimSolver, bytom.solver.RefundSolver

        :returns: NormalSignature, FundSignature, ClaimSignature, RefundSignature -- Bytom signature instance.

        >>> from swap.providers.bytom.signature import Signature
        >>> from swap.providers.bytom.solver import FundSolver
        >>> unsigned_fund_transaction_raw = "eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcTluZHlseDAyc3lmd2Q3bnBlaGZ4ejRsZGRoenFzdmUyZnU2dmM3IiwgInJhdyI6ICIwNzAxMDAwMjAxNWYwMTVkODJlNjVmOTY0ZDNjMzUzMjU0OGRmZGU5Mzg0NjJmNTY2Yzk1ZDNjOTBlNmEzYTE4MmEwYjNiZGFlNDZhYTc5MGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MDg2ZjIwMzAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAxNWYwMTVkMDcwZDBlYjIyZDMyYjgyZDNkMmYzZmM0YmFmYjdhODVmNTIyOWY3ZmQ4OTA0MmQyZmYzMjU3Mzc1ZTQzZDNlYmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOGY1Zjc0ZjAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDE0NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDAwMTNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmQ4YjhmODUyMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAiaGFzaCI6ICI1MGIzMzZhYjZlMDU1ZDlkNGQ2NWE5ZjIyOTViNTMyNzBhYmQzODE2YzIzYmE0Yzk1NDg0MWYzOTlhYTc3MmQ1IiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbImY3ZDNhYTE4YjI5NWNkYTZmMmIxMTMyYzQyMzE5MzNjYzkyZjNiYWNhNzA1OTc0YzVkZTM3OGY5YjY5NWYwZTIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9LCB7ImRhdGFzIjogWyJjYTYxNWJhMmM3MjllNDYzZmJmNzlhMTE0MTkxNzYyNjFiMWJmNmJlNDQ4MTMzMzVkMmIyNTZlOGE3YmJjZWVlIl0sICJwdWJsaWNfa2V5IjogIjkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieXRvbV9mdW5kX3Vuc2lnbmVkIn0"
        >>> sender_xprivate_key = "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"
        >>> fund_solver = FundSolver(sender_xprivate_key)
        >>> signature = Signature("mainnet")
        >>> signature.sign(transaction_raw=unsigned_fund_transaction_raw, solver=fund_solver)
        <swap.providers.bytom.signature.FundSignature object at 0x0409DAF0>
        """

        if not is_transaction_raw(transaction_raw=transaction_raw):
            raise TransactionRawError("Invalid Bytom unsigned transaction raw.")

        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

        self._type = loaded_transaction_raw["type"]
        if loaded_transaction_raw["type"] == "bytom_normal_unsigned":
            return NormalSignature(network=self._network).sign(
                transaction_raw=transaction_raw, solver=solver
            )
        elif loaded_transaction_raw["type"] == "bytom_fund_unsigned":
            return FundSignature(network=self._network).sign(
                transaction_raw=transaction_raw, solver=solver
            )
        elif loaded_transaction_raw["type"] == "bytom_claim_unsigned":
            return ClaimSignature(network=self._network).sign(
                transaction_raw=transaction_raw, solver=solver
            )
        elif loaded_transaction_raw["type"] == "bytom_refund_unsigned":
            return RefundSignature(network=self._network).sign(
                transaction_raw=transaction_raw, solver=solver
            )

    def unsigned_datas(self, *args, **kwargs) -> List[dict]:
        """
        Get Bytom transaction unsigned datas with instruction.

        :returns: list -- Bytom transaction unsigned datas.

        >>> from swap.providers.bytom.signature import Signature
        >>> from swap.providers.bytom.solver import ClaimSolver
        >>> unsigned_claim_transaction_raw = "eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcTNwbHd2bXZ5NHFoam1wNXpmZnptazUwYWFncHVqdDZmNWplODVwIiwgInJhdyI6ICIwNzAxMDAwMjAxNWYwMTVkMzA1YTI4ZDhkMzRiNDBjNjU5MzY4MTBmOWU5YzFmOGJjOWM3OTNlYzJlNzJjNzBmOTIwM2ZiYmViMGE1NmRiOWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGFkZTIwNDAxMDExNjAwMTQwZTQzYTkyYTllOGFjYTc4OGViMTU1MWMzMTY0NDhjMmUzZjc4MjE1MDEwMDAxNWQwMTViMTM4ODFmMzI3ZTJiZTBkNWMwMGYzODU2MGYxYzI5NDg2Y2RhZjI1NWMwOWMwMWVlZTFhMWViYWEzNzgzZGRkOWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDAwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkyMjAxMjAzZTBhMzc3YWU0YWZhMDMxZDQ1NTE1OTlkOWJiN2Q1YjI3ZjQ3MzZkNzdmNzhjYWM0ZDQ3NmYwZmZiYTVhZTNlMDIwMTNhZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjkwNGUwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkwMDAxM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjBkZWUxMDQwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkwMCIsICJoYXNoIjogImQ1NDRhZDJkMDhmOWRkYTMzYjc4OTUzYzc0ZWVkZTljOWViNWQ4MDgzNTY5NTMxMGIyNDJkNTc5NmNmYjkxZDYiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiNTE3MjI5MGE5ODU4YTRhMDdjNjAzYzc0MWY2ZmQ4ZTg2NzE1YThhNDQ3MGViMjM3ZDBhMmQ4MzI1YzE3MDZiNyJdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiBudWxsfSwgeyJkYXRhcyI6IFsiZTQxYWI5NjQ3MDFmMjBhMjM0NzMzNDBiMTFkNWNiY2ZiYTlhMzczY2VkZjI4NGY4MDljMGM2MWNlN2Q3MTVkYSJdLCAicHVibGljX2tleSI6ICIzZTBhMzc3YWU0YWZhMDMxZDQ1NTE1OTlkOWJiN2Q1YjI3ZjQ3MzZkNzdmNzhjYWM0ZDQ3NmYwZmZiYTVhZTNlIiwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogIm0vNDQvMTUzLzEvMC8xIn1dLCAic2lnbmF0dXJlcyI6IFtdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInR5cGUiOiAiYnl0b21fY2xhaW1fdW5zaWduZWQifQ"
        >>> recipient_xprivate_key = "58dd4094155bbebf2868189231c47e4e0edbd9f74545f843c9537259e1d7a656983aef283d0ccebecc2d33577a9f650b53ac7adff44f48ec839e3346cc22418f"
        >>> bytecode = "02e8032091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"
        >>> claim_solver = ClaimSolver(recipient_xprivate_key, "Hello Meheret!", bytecode)
        >>> signature = Signature("mainnet")
        >>> signature.sign(unsigned_claim_transaction_raw, claim_solver)
        >>> signature.unsigned_datas()
        [{"datas": ["5172290a9858a4a07c603c741f6fd8e86715a8a4470eb237d0a2d8325c1706b7"], "network": "mainnet", "path": null}, {"datas": ["e41ab964701f20a23473340b11d5cbcfba9a373cedf284f809c0c61ce7d715da"], "public_key": "3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e", "network": "mainnet", "path": "m/44/153/1/0/1"}]
        """

        if self._transaction is None:
            raise ValueError("Transaction is none, sign unsigned transaction raw first.")
        return self._transaction["unsigned_datas"]

    def signatures(self) -> List[List[str]]:
        """
        Get Bytom transaction signatures(signed datas).

        :returns: list -- Bytom transaction signatures.

        >>> from swap.providers.bytom.signature import Signature
        >>> from swap.providers.bytom.solver import FundSolver
        >>> unsigned_fund_transaction_raw = "eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcTluZHlseDAyc3lmd2Q3bnBlaGZ4ejRsZGRoenFzdmUyZnU2dmM3IiwgInJhdyI6ICIwNzAxMDAwMjAxNWYwMTVkODJlNjVmOTY0ZDNjMzUzMjU0OGRmZGU5Mzg0NjJmNTY2Yzk1ZDNjOTBlNmEzYTE4MmEwYjNiZGFlNDZhYTc5MGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MDg2ZjIwMzAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAxNWYwMTVkMDcwZDBlYjIyZDMyYjgyZDNkMmYzZmM0YmFmYjdhODVmNTIyOWY3ZmQ4OTA0MmQyZmYzMjU3Mzc1ZTQzZDNlYmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOGY1Zjc0ZjAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDE0NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDAwMTNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmQ4YjhmODUyMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAiaGFzaCI6ICI1MGIzMzZhYjZlMDU1ZDlkNGQ2NWE5ZjIyOTViNTMyNzBhYmQzODE2YzIzYmE0Yzk1NDg0MWYzOTlhYTc3MmQ1IiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbImY3ZDNhYTE4YjI5NWNkYTZmMmIxMTMyYzQyMzE5MzNjYzkyZjNiYWNhNzA1OTc0YzVkZTM3OGY5YjY5NWYwZTIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9LCB7ImRhdGFzIjogWyJjYTYxNWJhMmM3MjllNDYzZmJmNzlhMTE0MTkxNzYyNjFiMWJmNmJlNDQ4MTMzMzVkMmIyNTZlOGE3YmJjZWVlIl0sICJwdWJsaWNfa2V5IjogIjkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieXRvbV9mdW5kX3Vuc2lnbmVkIn0"
        >>> sender_xprivate_key = "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"
        >>> fund_solver = FundSolver(sender_xprivate_key)
        >>> signature = Signature("mainnet")
        >>> signature.sign(unsigned_fund_transaction_raw, fund_solver)
        >>> signature.signatures()
        [["00c005bc114ec5f89b49e48526f90312b6f1a5274efd252049880023aeb8e7998c15e0baa4ff10fabbdae702f245405a36022e3c9acc5e5e6c9ac4b9d937a801"], ["fbfb123ef062c9068dad22ce28de2a4e72f82076b6f98cb7e0909c11856260e7020aecbdca639f0b6e39d345c05913d2c9291db130b53d5b2bc59f61adfc1406"]]
        """

        # Check transaction
        if self._transaction is None:
            raise ValueError("Transaction is none, build transaction first.")
        return self._signatures

    def datas(self) -> dict:
        return self._datas

    def transaction_raw(self) -> str:
        """
        Get Bytom signed transaction raw.

        :returns: str -- Bytom signed transaction raw.

        >>> from swap.providers.bytom.signature import Signature
        >>> from swap.providers.bytom.solver import FundSolver
        >>> unsigned_fund_transaction_raw = "eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcTluZHlseDAyc3lmd2Q3bnBlaGZ4ejRsZGRoenFzdmUyZnU2dmM3IiwgInJhdyI6ICIwNzAxMDAwMjAxNWYwMTVkODJlNjVmOTY0ZDNjMzUzMjU0OGRmZGU5Mzg0NjJmNTY2Yzk1ZDNjOTBlNmEzYTE4MmEwYjNiZGFlNDZhYTc5MGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MDg2ZjIwMzAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAxNWYwMTVkMDcwZDBlYjIyZDMyYjgyZDNkMmYzZmM0YmFmYjdhODVmNTIyOWY3ZmQ4OTA0MmQyZmYzMjU3Mzc1ZTQzZDNlYmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOGY1Zjc0ZjAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDE0NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDAwMTNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmQ4YjhmODUyMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAiaGFzaCI6ICI1MGIzMzZhYjZlMDU1ZDlkNGQ2NWE5ZjIyOTViNTMyNzBhYmQzODE2YzIzYmE0Yzk1NDg0MWYzOTlhYTc3MmQ1IiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbImY3ZDNhYTE4YjI5NWNkYTZmMmIxMTMyYzQyMzE5MzNjYzkyZjNiYWNhNzA1OTc0YzVkZTM3OGY5YjY5NWYwZTIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9LCB7ImRhdGFzIjogWyJjYTYxNWJhMmM3MjllNDYzZmJmNzlhMTE0MTkxNzYyNjFiMWJmNmJlNDQ4MTMzMzVkMmIyNTZlOGE3YmJjZWVlIl0sICJwdWJsaWNfa2V5IjogIjkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieXRvbV9mdW5kX3Vuc2lnbmVkIn0"
        >>> sender_xprivate_key = "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"
        >>> fund_solver = FundSolver(sender_xprivate_key)
        >>> signature = Signature("mainnet")
        >>> signature.sign(unsigned_fund_transaction_raw, fund_solver)
        >>> signature.transaction_raw()
        "eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcTluZHlseDAyc3lmd2Q3bnBlaGZ4ejRsZGRoenFzdmUyZnU2dmM3IiwgInJhdyI6ICIwNzAxMDAwMjAxNWYwMTVkODJlNjVmOTY0ZDNjMzUzMjU0OGRmZGU5Mzg0NjJmNTY2Yzk1ZDNjOTBlNmEzYTE4MmEwYjNiZGFlNDZhYTc5MGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MDg2ZjIwMzAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAxNWYwMTVkMDcwZDBlYjIyZDMyYjgyZDNkMmYzZmM0YmFmYjdhODVmNTIyOWY3ZmQ4OTA0MmQyZmYzMjU3Mzc1ZTQzZDNlYmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOGY1Zjc0ZjAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDE0NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDAwMTNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmQ4YjhmODUyMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAiaGFzaCI6ICI1MGIzMzZhYjZlMDU1ZDlkNGQ2NWE5ZjIyOTViNTMyNzBhYmQzODE2YzIzYmE0Yzk1NDg0MWYzOTlhYTc3MmQ1IiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbImY3ZDNhYTE4YjI5NWNkYTZmMmIxMTMyYzQyMzE5MzNjYzkyZjNiYWNhNzA1OTc0YzVkZTM3OGY5YjY5NWYwZTIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9LCB7ImRhdGFzIjogWyJjYTYxNWJhMmM3MjllNDYzZmJmNzlhMTE0MTkxNzYyNjFiMWJmNmJlNDQ4MTMzMzVkMmIyNTZlOGE3YmJjZWVlIl0sICJwdWJsaWNfa2V5IjogIjkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJzaWduYXR1cmVzIjogW1siMDBjMDA1YmMxMTRlYzVmODliNDllNDg1MjZmOTAzMTJiNmYxYTUyNzRlZmQyNTIwNDk4ODAwMjNhZWI4ZTc5OThjMTVlMGJhYTRmZjEwZmFiYmRhZTcwMmYyNDU0MDVhMzYwMjJlM2M5YWNjNWU1ZTZjOWFjNGI5ZDkzN2E4MDEiXSwgWyJmYmZiMTIzZWYwNjJjOTA2OGRhZDIyY2UyOGRlMmE0ZTcyZjgyMDc2YjZmOThjYjdlMDkwOWMxMTg1NjI2MGU3MDIwYWVjYmRjYTYzOWYwYjZlMzlkMzQ1YzA1OTEzZDJjOTI5MWRiMTMwYjUzZDViMmJjNTlmNjFhZGZjMTQwNiJdXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX2Z1bmRfc2lnbmVkIn0"
        """

        if self._signed_raw is None:
            raise ValueError("Transaction is none, sign unsigned transaction raw first.")
        return clean_transaction_raw(self._signed_raw)


class NormalSignature(Signature):
    """
    Bytom Normal signature.

    :param network: Bytom network, defaults to mainnet.
    :type network: str

    :returns: NormalSignature -- Bytom normal signature instance.
    """

    def __init__(self, network: str = config["network"]):
        super().__init__(network=network)

    def sign(self, transaction_raw: str, solver: NormalSolver) -> "NormalSignature":
        """
        Sign unsigned normal transaction raw.

        :param transaction_raw: Bytom unsigned normal transaction raw.
        :type transaction_raw: str
        :param solver: Bytom normal solver.
        :type solver: bytom.solver.NormalSolver

        :returns: NormalSignature -- Bytom normal signature instance.

        >>> from swap.providers.bytom.signature import NormalSignature
        >>> from swap.providers.bytom.solver import NormalSolver
        >>> unsigned_normal_transaction_raw = "eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcTluZHlseDAyc3lmd2Q3bnBlaGZ4ejRsZGRoenFzdmUyZnU2dmM3IiwgInJhdyI6ICIwNzAxMDAwMjAxNWYwMTVkODJlNjVmOTY0ZDNjMzUzMjU0OGRmZGU5Mzg0NjJmNTY2Yzk1ZDNjOTBlNmEzYTE4MmEwYjNiZGFlNDZhYTc5MGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MDg2ZjIwMzAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAxNWYwMTVkMDcwZDBlYjIyZDMyYjgyZDNkMmYzZmM0YmFmYjdhODVmNTIyOWY3ZmQ4OTA0MmQyZmYzMjU3Mzc1ZTQzZDNlYmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOGY1Zjc0ZjAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDE0NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDAwMTNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmQ4YjhmODUyMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAiaGFzaCI6ICI1MGIzMzZhYjZlMDU1ZDlkNGQ2NWE5ZjIyOTViNTMyNzBhYmQzODE2YzIzYmE0Yzk1NDg0MWYzOTlhYTc3MmQ1IiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbImY3ZDNhYTE4YjI5NWNkYTZmMmIxMTMyYzQyMzE5MzNjYzkyZjNiYWNhNzA1OTc0YzVkZTM3OGY5YjY5NWYwZTIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9LCB7ImRhdGFzIjogWyJjYTYxNWJhMmM3MjllNDYzZmJmNzlhMTE0MTkxNzYyNjFiMWJmNmJlNDQ4MTMzMzVkMmIyNTZlOGE3YmJjZWVlIl0sICJwdWJsaWNfa2V5IjogIjkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieXRvbV9mdW5kX3Vuc2lnbmVkIn0"
        >>> sender_xprivate_key = "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"
        >>> normal_solver = NormalSolver(sender_xprivate_key)
        >>> normal_signature = NormalSignature("mainnet")
        >>> normal_signature.sign(unsigned_normal_transaction_raw, normal_solver)
        <swap.providers.bytom.signature.NormalSignature object at 0x0409DAF0>
        """

        if not is_transaction_raw(transaction_raw=transaction_raw):
            raise TransactionRawError("Invalid Bytom unsigned transaction raw.")

        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

        if not loaded_transaction_raw["type"] == "bytom_normal_unsigned":
            raise TypeError(f"Invalid Bytom normal unsigned transaction raw type, "
                            f"you can't sign {loaded_transaction_raw['type']} type by using normal signature.")

        # Check parameter instances
        if not isinstance(solver, NormalSolver):
            raise TypeError(f"Solver must be Bytom NormalSolver, not {type(solver).__name__} type.")

        # Set transaction, fee, type and network
        self._fee, self._type, self._datas, self._network, self._transaction = (
            loaded_transaction_raw["fee"], loaded_transaction_raw["type"], loaded_transaction_raw["datas"],
            loaded_transaction_raw["network"], loaded_transaction_raw
        )

        # Set recipient wallet
        wallet, path, indexes = solver.solve()
        # Clean derivation indexes/path
        wallet.clean_derivation()
        # Sign normal transaction
        for unsigned in self.unsigned_datas():
            signed_data = list()
            unsigned_datas = unsigned["datas"]
            if unsigned["path"]:
                wallet.from_path(unsigned["path"])
            elif path:
                wallet.from_path(path)
            elif indexes:
                wallet.from_indexes(indexes)
            for unsigned_data in unsigned_datas:
                signed_data.append(wallet.sign(unsigned_data))
            self._signatures.append(signed_data)
            wallet.clean_derivation()

        # Set transaction type
        self._type = "bytom_normal_signed"
        # Encode normal transaction raw
        self._signed_raw = b64encode(str(json.dumps(dict(
            fee=self._fee,
            address=self._transaction["address"],
            raw=self.raw(),
            hash=self.hash(),
            unsigned_datas=self.unsigned_datas(),
            signatures=self.signatures(),
            network=self._network,
            type=self._type,
            datas=self._datas
        ))).encode()).decode()
        return self


class FundSignature(Signature):
    """
    Bytom Fund signature.

    :param network: Bytom network, defaults to mainnet.
    :type network: str

    :returns: FundSignature -- Bytom fund signature instance.
    """

    def __init__(self, network: str = config["network"]):
        super().__init__(network=network)

    def sign(self, transaction_raw: str, solver: FundSolver) -> "FundSignature":
        """
        Sign unsigned fund transaction raw.

        :param transaction_raw: Bytom unsigned fund transaction raw.
        :type transaction_raw: str
        :param solver: Bytom fund solver.
        :type solver: bytom.solver.FundSolver

        :returns: FundSignature -- Bytom fund signature instance.

        >>> from swap.providers.bytom.signature import FundSignature
        >>> from swap.providers.bytom.solver import FundSolver
        >>> unsigned_fund_transaction_raw = "eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcTluZHlseDAyc3lmd2Q3bnBlaGZ4ejRsZGRoenFzdmUyZnU2dmM3IiwgInJhdyI6ICIwNzAxMDAwMjAxNWYwMTVkODJlNjVmOTY0ZDNjMzUzMjU0OGRmZGU5Mzg0NjJmNTY2Yzk1ZDNjOTBlNmEzYTE4MmEwYjNiZGFlNDZhYTc5MGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MDg2ZjIwMzAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAxNWYwMTVkMDcwZDBlYjIyZDMyYjgyZDNkMmYzZmM0YmFmYjdhODVmNTIyOWY3ZmQ4OTA0MmQyZmYzMjU3Mzc1ZTQzZDNlYmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOGY1Zjc0ZjAxMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMjIwMTIwOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMjAyMDE0NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDEyMjAwMjA0ZjhmMGU4OGQwYTQ0YjNkODg0YjA3YjZkZDQ1MzY1MThmZmNiYjU5NmE5MWNhMGU2YjJmMzdlOTY0NjNiYmZjMDAwMTNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmQ4YjhmODUyMDExNjAwMTQyY2RhNGY5OWVhODExMmU2ZmE2MWNkZDI2MTU3ZWQ2ZGM0MDgzMzJhMDAiLCAiaGFzaCI6ICI1MGIzMzZhYjZlMDU1ZDlkNGQ2NWE5ZjIyOTViNTMyNzBhYmQzODE2YzIzYmE0Yzk1NDg0MWYzOTlhYTc3MmQ1IiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbImY3ZDNhYTE4YjI5NWNkYTZmMmIxMTMyYzQyMzE5MzNjYzkyZjNiYWNhNzA1OTc0YzVkZTM3OGY5YjY5NWYwZTIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9LCB7ImRhdGFzIjogWyJjYTYxNWJhMmM3MjllNDYzZmJmNzlhMTE0MTkxNzYyNjFiMWJmNmJlNDQ4MTMzMzVkMmIyNTZlOGE3YmJjZWVlIl0sICJwdWJsaWNfa2V5IjogIjkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIiLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiAibS80NC8xNTMvMS8wLzEifV0sICJzaWduYXR1cmVzIjogW10sICJuZXR3b3JrIjogIm1haW5uZXQiLCAidHlwZSI6ICJieXRvbV9mdW5kX3Vuc2lnbmVkIn0"
        >>> sender_xprivate_key = "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"
        >>> fund_solver = FundSolver(sender_xprivate_key)
        >>> fund_signature = FundSignature("mainnet")
        >>> fund_signature.sign(unsigned_fund_transaction_raw, fund_solver)
        <swap.providers.bytom.signature.FundSignature object at 0x0409DAF0>
        """

        if not is_transaction_raw(transaction_raw=transaction_raw):
            raise TransactionRawError("Invalid Bytom unsigned transaction raw.")

        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

        if not loaded_transaction_raw["type"] == "bytom_fund_unsigned":
            raise TypeError(f"Invalid Bytom fund unsigned transaction raw type, "
                            f"you can't sign {loaded_transaction_raw['type']} type by using fund signature.")

        # Check parameter instances
        if not isinstance(solver, FundSolver):
            raise TypeError(f"Solver must be Bytom FundSolver, not {type(solver).__name__} type.")

        # Set transaction, fee, type and network
        self._fee, self._type, self._datas, self._network, self._transaction = (
            loaded_transaction_raw["fee"], loaded_transaction_raw["type"], loaded_transaction_raw["datas"],
            loaded_transaction_raw["network"], loaded_transaction_raw
        )

        # Set recipient wallet
        wallet, path, indexes = solver.solve()
        # Clean derivation indexes/path
        wallet.clean_derivation()
        # Sign fund transaction
        for unsigned in self.unsigned_datas():
            signed_data = list()
            unsigned_datas = unsigned["datas"]
            if unsigned["path"]:
                wallet.from_path(unsigned["path"])
            elif path:
                wallet.from_path(path)
            elif indexes:
                wallet.from_indexes(indexes)
            for unsigned_data in unsigned_datas:
                signed_data.append(wallet.sign(unsigned_data))
            self._signatures.append(signed_data)
            wallet.clean_derivation()

        # Set transaction type
        self._type = "bytom_fund_signed"
        # Encode fund transaction raw
        self._signed_raw = b64encode(str(json.dumps(dict(
            fee=self._fee,
            address=self._transaction["address"],
            raw=self.raw(),
            hash=self.hash(),
            unsigned_datas=self.unsigned_datas(),
            signatures=self.signatures(),
            network=self._network,
            type=self._type,
            datas=self._datas
        ))).encode()).decode()
        return self


class ClaimSignature(Signature):
    """
    Bytom Claim signature.

    :param network: Bytom network, defaults to mainnet.
    :type network: str

    :returns: ClaimSignature -- Bytom claim signature instance.
    """

    def __init__(self, network: str = config["network"]):
        super().__init__(network=network)

    def sign(self, transaction_raw: str, solver: ClaimSolver) -> "ClaimSignature":
        """
        Sign unsigned claim transaction raw.

        :param transaction_raw: Bytom unsigned claim transaction raw.
        :type transaction_raw: str
        :param solver: Bytom claim solver.
        :type solver: bytom.solver.ClaimSolver

        :returns: ClaimSignature -- Bytom claim signature instance.

        >>> from swap.providers.bytom.signature import ClaimSignature
        >>> from swap.providers.bytom.solver import ClaimSolver
        >>> unsigned_claim_transaction_raw = "eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcTNwbHd2bXZ5NHFoam1wNXpmZnptazUwYWFncHVqdDZmNWplODVwIiwgInJhdyI6ICIwNzAxMDAwMjAxNWYwMTVkMzA1YTI4ZDhkMzRiNDBjNjU5MzY4MTBmOWU5YzFmOGJjOWM3OTNlYzJlNzJjNzBmOTIwM2ZiYmViMGE1NmRiOWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGFkZTIwNDAxMDExNjAwMTQwZTQzYTkyYTllOGFjYTc4OGViMTU1MWMzMTY0NDhjMmUzZjc4MjE1MDEwMDAxNWQwMTViMTM4ODFmMzI3ZTJiZTBkNWMwMGYzODU2MGYxYzI5NDg2Y2RhZjI1NWMwOWMwMWVlZTFhMWViYWEzNzgzZGRkOWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDAwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkyMjAxMjAzZTBhMzc3YWU0YWZhMDMxZDQ1NTE1OTlkOWJiN2Q1YjI3ZjQ3MzZkNzdmNzhjYWM0ZDQ3NmYwZmZiYTVhZTNlMDIwMTNhZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjkwNGUwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkwMDAxM2NmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZjBkZWUxMDQwMTE2MDAxNDg4N2VlNjZkODRhODJmMmQ4NjgyNGE0NWJiNTFmZGVhMDNjOTJmNDkwMCIsICJoYXNoIjogImQ1NDRhZDJkMDhmOWRkYTMzYjc4OTUzYzc0ZWVkZTljOWViNWQ4MDgzNTY5NTMxMGIyNDJkNTc5NmNmYjkxZDYiLCAidW5zaWduZWRfZGF0YXMiOiBbeyJkYXRhcyI6IFsiNTE3MjI5MGE5ODU4YTRhMDdjNjAzYzc0MWY2ZmQ4ZTg2NzE1YThhNDQ3MGViMjM3ZDBhMmQ4MzI1YzE3MDZiNyJdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInBhdGgiOiBudWxsfSwgeyJkYXRhcyI6IFsiZTQxYWI5NjQ3MDFmMjBhMjM0NzMzNDBiMTFkNWNiY2ZiYTlhMzczY2VkZjI4NGY4MDljMGM2MWNlN2Q3MTVkYSJdLCAicHVibGljX2tleSI6ICIzZTBhMzc3YWU0YWZhMDMxZDQ1NTE1OTlkOWJiN2Q1YjI3ZjQ3MzZkNzdmNzhjYWM0ZDQ3NmYwZmZiYTVhZTNlIiwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogIm0vNDQvMTUzLzEvMC8xIn1dLCAic2lnbmF0dXJlcyI6IFtdLCAibmV0d29yayI6ICJtYWlubmV0IiwgInR5cGUiOiAiYnl0b21fY2xhaW1fdW5zaWduZWQifQ"
        >>> recipient_xprivate_key = "58dd4094155bbebf2868189231c47e4e0edbd9f74545f843c9537259e1d7a656983aef283d0ccebecc2d33577a9f650b53ac7adff44f48ec839e3346cc22418f"
        >>> bytecode = "02e8032091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"
        >>> claim_solver = ClaimSolver(recipient_xprivate_key, "Hello Meheret!", bytecode)
        >>> claim_signature = ClaimSignature("mainnet")
        >>> claim_signature.sign(transaction_raw=unsigned_claim_transaction_raw, solver=claim_solver)
        <swap.providers.bytom.signature.ClaimSignature object at 0x0409DAF0>
        """

        if not is_transaction_raw(transaction_raw=transaction_raw):
            raise TransactionRawError("Invalid Bytom unsigned transaction raw.")

        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

        if not loaded_transaction_raw["type"] == "bytom_claim_unsigned":
            raise TypeError(f"Invalid Bytom claim unsigned transaction raw type, "
                            f"you can't sign {loaded_transaction_raw['type']} type by using claim signature.")

        # Check parameter instances
        if not isinstance(solver, ClaimSolver):
            raise TypeError(f"Solver must be Bytom ClaimSolver, not {type(solver).__name__} type.")

        # Set transaction, fee, type and network
        self._fee, self._type, self._datas, self._network, self._transaction = (
            loaded_transaction_raw["fee"], loaded_transaction_raw["type"], loaded_transaction_raw["datas"],
            loaded_transaction_raw["network"], loaded_transaction_raw
        )

        # Set recipient wallet
        wallet, secret, path, indexes = solver.solve()
        # Clean derivation indexes/path
        wallet.clean_derivation()
        # Sign claim transaction
        for index, unsigned in enumerate(self.unsigned_datas()):
            signed_data = list()
            unsigned_datas = unsigned["datas"]
            if unsigned["path"]:
                wallet.from_path(unsigned["path"])
            elif path:
                wallet.from_path(path)
            elif indexes:
                wallet.from_indexes(indexes)
            for unsigned_data in unsigned_datas:
                signed_data.append(bytearray(secret.encode()).hex())
                signed_data.append(wallet.sign(unsigned_data))
                signed_data.append(str("00"))
                signed_data.append(solver.witness(self._network))
            self._signatures.append(signed_data)
            wallet.clean_derivation()

        # Set transaction type
        self._type = "bytom_claim_signed"
        # Encode claim transaction raw
        self._signed_raw = b64encode(str(json.dumps(dict(
            fee=self._fee,
            address=self._transaction["address"],
            raw=self.raw(),
            hash=self.hash(),
            unsigned_datas=self.unsigned_datas(),
            signatures=self.signatures(),
            network=self._network,
            type=self._type,
            datas=self._datas
        ))).encode()).decode()
        return self


class RefundSignature(Signature):
    """
    Bytom Refund signature.

    :param network: Bytom network, defaults to mainnet.
    :type network: str

    :returns: RefundSignature -- Bytom claim signature instance.
    """

    def __init__(self, network: str = config["network"]):
        super().__init__(network=network)

    def sign(self, transaction_raw: str, solver: RefundSolver) -> "RefundSignature":
        """
        Sign unsigned refund transaction raw.

        :param transaction_raw: Bytom unsigned refund transaction raw.
        :type transaction_raw: str
        :param solver: Bytom refund solver.
        :type solver: bytom.solver.RefundSolver
        
        :returns: RefundSignature -- Bytom refund signature instance.

        >>> from swap.providers.bytom.signature import RefundSignature
        >>> from swap.providers.bytom.solver import RefundSolver
        >>> unsigned_refund_transaction_raw = "eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcTluZHlseDAyc3lmd2Q3bnBlaGZ4ejRsZGRoenFzdmUyZnU2dmM3IiwgImhhc2giOiAiNjlhNWYzMDI4ODBhNzNkMzYzZWNiMzkyYzgyZGNkMzMyODNiZDFiYmU1NmFhMzAyODU4NzMzZTc5ZTE2Mzc5OCIsICJyYXciOiAiMDcwMTAwMDIwMTVmMDE1ZDMwNWEyOGQ4ZDM0YjQwYzY1OTM2ODEwZjllOWMxZjhiYzljNzkzZWMyZTcyYzcwZjkyMDNmYmJlYjBhNTZkYjlmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODBhZGUyMDQwMTAxMTYwMDE0MGU0M2E5MmE5ZThhY2E3ODhlYjE1NTFjMzE2NDQ4YzJlM2Y3ODIxNTAxMDAwMTVmMDE1ZDgyZTY1Zjk2NGQzYzM1MzI1NDhkZmRlOTM4NDYyZjU2NmM5NWQzYzkwZTZhM2ExODJhMGIzYmRhZTQ2YWE3OTBmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmODA4NmYyMDMwMTAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTIyMDEyMDkxZmY3ZjUyNWZmNDA4NzRjNGY0N2YwY2FiNDJlNDZlM2JmNTNhZGFkNTlhZGVmOTU1OGFkMWI2NDQ4ZjIyZTIwMjAxM2FmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmOTA0ZTAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTAwMDEzY2ZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZlMDk2ZDMwODAxMTYwMDE0MmNkYTRmOTllYTgxMTJlNmZhNjFjZGQyNjE1N2VkNmRjNDA4MzMyYTAwIiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbIjY0ODJiMmRmZTliM2U3NjY0MzVlMDQ4MmI2MDAzN2FmYWVhYmFhYWExMDg5Mzc0OGEyODhiY2EwMjlmZjFjNTIiXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBbIjBhNDY3NmE3MzI0MmNkMTI2NjFkYjBmM2Y3Mzc5NGQ0OWI3Nzc1NTBiZDk4MTc2YThkODhlYTg3NTVlNDE3ZjIiXSwgInB1YmxpY19rZXkiOiAiOTFmZjdmNTI1ZmY0MDg3NGM0ZjQ3ZjBjYWI0MmU0NmUzYmY1M2FkYWQ1OWFkZWY5NTU4YWQxYjY0NDhmMjJlMiIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX3JlZnVuZF91bnNpZ25lZCJ9"
        >>> sender_xprivate_key = "205b15f70e253399da90b127b074ea02904594be9d54678207872ec1ba31ee51ef4490504bd2b6f997113671892458830de09518e6bd5958d5d5dd97624cfa4b"
        >>> bytecode = "02e8032091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0"
        >>> refund_solver = RefundSolver(sender_xprivate_key, bytecode, 1000)
        >>> refund_signature = RefundSignature("mainnet")
        >>> refund_signature.sign(transaction_raw=unsigned_refund_transaction_raw, solver=refund_solver)
        <swap.providers.bytom.signature.RefundSignature object at 0x0409DAF0>
        """

        if not is_transaction_raw(transaction_raw=transaction_raw):
            raise TransactionRawError("Invalid Bytom unsigned transaction raw.")

        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

        if not loaded_transaction_raw["type"] == "bytom_refund_unsigned":
            raise TypeError(f"Invalid Bytom refund unsigned transaction raw type, "
                            f"you can't sign {loaded_transaction_raw['type']} type by using refund signature.")

        # Check parameter instances
        if not isinstance(solver, RefundSolver):
            raise TypeError(f"Solver must be Bytom RefundSolver, not {type(solver).__name__} type.")

        # Set transaction, fee, type and network
        self._fee, self._type, self._datas, self._network, self._transaction = (
            loaded_transaction_raw["fee"], loaded_transaction_raw["type"], loaded_transaction_raw["datas"],
            loaded_transaction_raw["network"], loaded_transaction_raw
        )

        # Set recipient wallet
        wallet, path, indexes = solver.solve()
        # Clean derivation indexes/path
        wallet.clean_derivation()
        # Sign refund transaction
        for index, unsigned in enumerate(self.unsigned_datas()):
            signed_data = list()
            unsigned_datas = unsigned["datas"]
            if unsigned["path"]:
                wallet.from_path(unsigned["path"])
            elif path:
                wallet.from_path(path)
            elif indexes:
                wallet.from_indexes(indexes)
            for unsigned_data in unsigned_datas:
                signed_data.append(wallet.sign(unsigned_data))
                signed_data.append(str("01"))
                signed_data.append(solver.witness(self._network))
            self._signatures.append(signed_data)
            wallet.clean_derivation()

        # Encode refund transaction raw
        self._type = "bytom_refund_signed"
        self._signed_raw = b64encode(str(json.dumps(dict(
            fee=self._fee,
            address=self._transaction["address"],
            raw=self.raw(),
            hash=self.hash(),
            unsigned_datas=self.unsigned_datas(),
            signatures=self.signatures(),
            network=self._network,
            type=self._type,
            datas=self._datas
        ))).encode()).decode()
        return self
