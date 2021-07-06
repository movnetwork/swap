#!/usr/bin/env python3

import json
import os

from swap.providers.bytom.htlc import HTLC

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_bytom_htlc():

    htlc = HTLC(network=_["bytom"]["network"]).build_htlc(
        secret_hash=_["bytom"]["htlc"]["secret"]["hash"],
        recipient_public_key=_["bytom"]["wallet"]["recipient"]["public_key"],
        sender_public_key=_["bytom"]["wallet"]["sender"]["public_key"],
        endblock=_["bytom"]["htlc"]["endblock"]
    )

    assert htlc.bytecode() == _["bytom"]["htlc"]["bytecode"]
    assert htlc.opcode() == _["bytom"]["htlc"]["opcode"]
    assert htlc.hash() == _["bytom"]["htlc"]["hash"]
    assert htlc.contract_address() == _["bytom"]["htlc"]["contract_address"]
    assert htlc.agreements == _["bytom"]["htlc"]["agreements"]

    htlc = HTLC(network=_["bytom"]["network"]).from_bytecode(
        bytecode=_["bytom"]["htlc"]["bytecode"]
    )

    assert htlc.bytecode() == _["bytom"]["htlc"]["bytecode"]
    assert htlc.opcode() is None
    assert htlc.hash() == _["bytom"]["htlc"]["hash"]
    assert htlc.contract_address() == _["bytom"]["htlc"]["contract_address"]
