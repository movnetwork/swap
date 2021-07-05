#!/usr/bin/env python3

import json
import os

from swap.providers.ethereum.htlc import HTLC

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_ethereum_htlc():
    
    htlc = HTLC(
        network=_["ethereum"]["network"]
    ).build_htlc(
        secret_hash=_["ethereum"]["htlc"]["secret"]["hash"],
        recipient_address=_["ethereum"]["wallet"]["recipient"]["address"],
        sender_address=_["ethereum"]["wallet"]["sender"]["address"],
        endtime=_["ethereum"]["htlc"]["endtime"]
    )

    assert htlc.abi() == _["ethereum"]["htlc"]["abi"]
    assert htlc.bytecode() == _["ethereum"]["htlc"]["bytecode"]
    assert htlc.bytecode_runtime() == _["ethereum"]["htlc"]["bytecode_runtime"]
    assert htlc.opcode() == _["ethereum"]["htlc"]["opcode"]
    assert htlc.contract_address() == _["ethereum"]["htlc"]["contract_address"]
    assert htlc.agreements["secret_hash"] == _["ethereum"]["htlc"]["agreements"]["secret_hash"]
    assert htlc.agreements["recipient_address"] == _["ethereum"]["htlc"]["agreements"]["recipient_address"]
    assert htlc.agreements["sender_address"] == _["ethereum"]["htlc"]["agreements"]["sender_address"]
    # assert htlc.agreements["endtime"]["datetime"] == _["ethereum"]["htlc"]["agreements"]["endtime"]["datetime"]
    assert htlc.agreements["endtime"]["timestamp"] == _["ethereum"]["htlc"]["agreements"]["endtime"]["timestamp"]
