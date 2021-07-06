#!/usr/bin/env python3

import json
import os

from swap.providers.xinfin.htlc import HTLC

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_xinfin_htlc():
    
    htlc = HTLC(
        network=_["xinfin"]["network"]
    ).build_htlc(
        secret_hash=_["xinfin"]["htlc"]["secret"]["hash"],
        recipient_address=_["xinfin"]["wallet"]["recipient"]["address"],
        sender_address=_["xinfin"]["wallet"]["sender"]["address"],
        endtime=_["xinfin"]["htlc"]["endtime"]
    )

    assert htlc.abi() == _["xinfin"]["htlc"]["abi"]
    assert htlc.bytecode() == _["xinfin"]["htlc"]["bytecode"]
    assert htlc.bytecode_runtime() == _["xinfin"]["htlc"]["bytecode_runtime"]
    assert htlc.opcode() == _["xinfin"]["htlc"]["opcode"]
    assert htlc.contract_address() == _["xinfin"]["htlc"]["contract_address"]
    assert htlc.agreements["secret_hash"] == _["xinfin"]["htlc"]["agreements"]["secret_hash"]
    assert htlc.agreements["recipient_address"] == _["xinfin"]["htlc"]["agreements"]["recipient_address"]
    assert htlc.agreements["sender_address"] == _["xinfin"]["htlc"]["agreements"]["sender_address"]
    # assert htlc.agreements["endtime"]["datetime"] == _["xinfin"]["htlc"]["agreements"]["endtime"]["datetime"]
    assert htlc.agreements["endtime"]["timestamp"] == _["xinfin"]["htlc"]["agreements"]["endtime"]["timestamp"]
