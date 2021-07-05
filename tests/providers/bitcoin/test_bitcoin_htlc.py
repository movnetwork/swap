#!/usr/bin/env python3

import json
import os

from swap.providers.bitcoin.htlc import HTLC

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_bitcoin_htlc():
    
    htlc = HTLC(network=_["bitcoin"]["network"]).build_htlc(
        secret_hash=_["bitcoin"]["htlc"]["secret"]["hash"],
        recipient_address=_["bitcoin"]["wallet"]["recipient"]["address"],
        sender_address=_["bitcoin"]["wallet"]["sender"]["address"],
        endtime=_["bitcoin"]["htlc"]["endtime"]
    )

    assert htlc.bytecode() == _["bitcoin"]["htlc"]["bytecode"]
    assert htlc.opcode() == _["bitcoin"]["htlc"]["opcode"]
    assert htlc.hash() == _["bitcoin"]["htlc"]["hash"]
    assert htlc.contract_address() == _["bitcoin"]["htlc"]["contract_address"]
    assert htlc.agreements == _["bitcoin"]["htlc"]["agreements"]

    htlc = HTLC(network=_["bitcoin"]["network"]).from_bytecode(
        bytecode=_["bitcoin"]["htlc"]["bytecode"]
    )

    assert htlc.bytecode() == _["bitcoin"]["htlc"]["bytecode"]
    assert htlc.opcode() == _["bitcoin"]["htlc"]["opcode"]
    assert htlc.hash() == _["bitcoin"]["htlc"]["hash"]
    assert htlc.contract_address() == _["bitcoin"]["htlc"]["contract_address"]

    htlc = HTLC(network=_["bitcoin"]["network"]).from_opcode(
        opcode=_["bitcoin"]["htlc"]["opcode"]
    )

    assert htlc.bytecode() == _["bitcoin"]["htlc"]["bytecode"]
    assert htlc.opcode() == _["bitcoin"]["htlc"]["opcode"]
    assert htlc.hash() == _["bitcoin"]["htlc"]["hash"]
    assert htlc.contract_address() == _["bitcoin"]["htlc"]["contract_address"]
