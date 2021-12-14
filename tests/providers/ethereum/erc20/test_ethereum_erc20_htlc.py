#!/usr/bin/env python3

import json
import os

from swap.providers.ethereum.htlc import HTLC

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_ethereum_erc20_htlc():
    
    erc20_htlc = HTLC(
        network=_["ethereum"]["network"], erc20=True
    ).build_htlc(
        secret_hash=_["ethereum"]["erc20_htlc"]["secret"]["hash"],
        recipient_address=_["ethereum"]["wallet"]["recipient"]["address"],
        sender_address=_["ethereum"]["wallet"]["sender"]["address"],
        endtime=_["ethereum"]["erc20_htlc"]["endtime"],
        token_address=_["ethereum"]["erc20_htlc"]["agreements"]["token_address"]
    )

    assert erc20_htlc.abi() == _["ethereum"]["erc20_htlc"]["abi"]
    assert erc20_htlc.bytecode() == _["ethereum"]["erc20_htlc"]["bytecode"]
    assert erc20_htlc.bytecode_runtime() == _["ethereum"]["erc20_htlc"]["bytecode_runtime"]
    assert erc20_htlc.opcode() == _["ethereum"]["erc20_htlc"]["opcode"]
    assert erc20_htlc.contract_address() == _["ethereum"]["erc20_htlc"]["contract_address"]
    assert erc20_htlc.agreements["secret_hash"] == _["ethereum"]["erc20_htlc"]["agreements"]["secret_hash"]
    assert erc20_htlc.agreements["recipient_address"] == _["ethereum"]["erc20_htlc"]["agreements"]["recipient_address"]
    assert erc20_htlc.agreements["sender_address"] == _["ethereum"]["erc20_htlc"]["agreements"]["sender_address"]
    # assert erc20_htlc.agreements["endtime"]["datetime"] == _["ethereum"]["erc20_htlc"]["agreements"]["endtime"]["datetime"]
    assert erc20_htlc.agreements["endtime"]["timestamp"] == _["ethereum"]["erc20_htlc"]["agreements"]["endtime"]["timestamp"]
    assert erc20_htlc.agreements["token_address"] == _["ethereum"]["erc20_htlc"]["agreements"]["token_address"]
