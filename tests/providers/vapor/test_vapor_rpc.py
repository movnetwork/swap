#!/usr/bin/env python3

import pytest
import requests
import json
import os

from swap.exceptions import APIError
from swap.providers.vapor.rpc import (
    decode_raw, submit_raw
)

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_vapor_rpc():

    with pytest.raises(requests.exceptions.ConnectionError):
        assert decode_raw(
            raw=_["vapor"]["fund"]["unsigned"]["raw"],
            network=_["vapor"]["network"]
        ) == _["vapor"]["fund"]["unsigned"]["json"]

    # (600) finalize tx fail
    with pytest.raises(APIError):
        submit_raw(
            address=_["vapor"]["wallet"]["sender"]["address"],
            raw=_["vapor"]["fund"]["unsigned"]["raw"],
            signatures=_["vapor"]["fund"]["unsigned"]["signatures"],
            network=_["vapor"]["network"]
        )
