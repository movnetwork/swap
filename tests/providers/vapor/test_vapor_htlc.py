#!/usr/bin/env python3

import json
import os

from swap.providers.vapor.htlc import HTLC

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_vapor_htlc():

    htlc = HTLC(network=_["vapor"]["network"]).build_htlc(
        secret_hash=_["vapor"]["htlc"]["secret"]["hash"],
        recipient_public_key=_["vapor"]["wallet"]["recipient"]["public_key"],
        sender_public_key=_["vapor"]["wallet"]["sender"]["public_key"],
        endblock=_["vapor"]["htlc"]["endblock"]
    )

    assert htlc.bytecode() == _["vapor"]["htlc"]["bytecode"]
    assert htlc.opcode() == _["vapor"]["htlc"]["opcode"]
    assert htlc.hash() == _["vapor"]["htlc"]["hash"]
    assert htlc.contract_address() == _["vapor"]["htlc"]["contract_address"]

    htlc = HTLC(network=_["vapor"]["network"]).from_bytecode(
        bytecode=_["vapor"]["htlc"]["bytecode"]
    )

    assert htlc.bytecode() == _["vapor"]["htlc"]["bytecode"]
    assert htlc.opcode() is None
    assert htlc.hash() == _["vapor"]["htlc"]["hash"]
    assert htlc.contract_address() == _["vapor"]["htlc"]["contract_address"]

    assert isinstance(htlc.balance(), int)
    assert isinstance(htlc.utxos(), list)
