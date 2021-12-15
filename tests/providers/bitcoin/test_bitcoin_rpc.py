#!/usr/bin/env python3

import pytest
import requests
import json
import os

from swap.exceptions import APIError
from swap.providers.bitcoin.rpc import (
    decode_raw, submit_raw
)

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_bitcoin_rpc():

    assert decode_raw(raw=_["bitcoin"]["fund"]["unsigned"]["raw"], network=_["bitcoin"]["network"]) == _["bitcoin"]["fund"]["unsigned"]["json"]

    # (REQ_ERROR) 16: mandatory-script-verify-flag-failed (Operation not valid with the current stack size)
    with pytest.raises((APIError, requests.exceptions.ConnectionError)):
        submit_raw(raw=_["bitcoin"]["fund"]["unsigned"]["raw"], network=_["bitcoin"]["network"])
