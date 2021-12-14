#!/usr/bin/env python3

import json
import os

from swap.providers.xinfin.htlc import HTLC

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_xinfin_xrc20_htlc():
    
    xrc20_htlc = HTLC(
        network=_["xinfin"]["network"], xrc20=True
    ).build_htlc(
        secret_hash=_["xinfin"]["xrc20_htlc"]["secret"]["hash"],
        recipient_address=_["xinfin"]["wallet"]["recipient"]["address"],
        sender_address=_["xinfin"]["wallet"]["sender"]["address"],
        endtime=_["xinfin"]["xrc20_htlc"]["endtime"],
        token_address=_["xinfin"]["xrc20_htlc"]["agreements"]["token_address"]
    )

    assert xrc20_htlc.abi() == _["xinfin"]["xrc20_htlc"]["abi"]
    assert xrc20_htlc.bytecode() == _["xinfin"]["xrc20_htlc"]["bytecode"]
    assert xrc20_htlc.bytecode_runtime() == _["xinfin"]["xrc20_htlc"]["bytecode_runtime"]
    assert xrc20_htlc.opcode() == _["xinfin"]["xrc20_htlc"]["opcode"]
    assert xrc20_htlc.contract_address() == _["xinfin"]["xrc20_htlc"]["contract_address"]
    assert xrc20_htlc.agreements["secret_hash"] == _["xinfin"]["xrc20_htlc"]["agreements"]["secret_hash"]
    assert xrc20_htlc.agreements["recipient_address"] == _["xinfin"]["xrc20_htlc"]["agreements"]["recipient_address"]
    assert xrc20_htlc.agreements["sender_address"] == _["xinfin"]["xrc20_htlc"]["agreements"]["sender_address"]
    # assert xrc20_htlc.agreements["endtime"]["datetime"] == _["xinfin"]["xrc20_htlc"]["agreements"]["endtime"]["datetime"]
    assert xrc20_htlc.agreements["endtime"]["timestamp"] == _["xinfin"]["xrc20_htlc"]["agreements"]["endtime"]["timestamp"]
    assert xrc20_htlc.agreements["token_address"] == _["xinfin"]["xrc20_htlc"]["agreements"]["token_address"]
