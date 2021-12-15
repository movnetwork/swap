#!/usr/bin/env python3

import pytest
import requests
import json
import os

from swap.exceptions import APIError
from swap.providers.bytom.rpc import (
    decode_raw, submit_raw
)

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_bytom_rpc():

    with pytest.raises(requests.exceptions.ConnectionError):
        assert decode_raw(
            raw=_["bytom"]["fund"]["unsigned"]["raw"],
            network=_["bytom"]["network"]
        ) == _["bytom"]["fund"]["unsigned"]["json"]

    # (600) finalize tx fail
    with pytest.raises(APIError):
        submit_raw(
            address=_["bytom"]["wallet"]["sender"]["address"],
            raw=_["bytom"]["fund"]["unsigned"]["raw"],
            signatures=_["bytom"]["fund"]["unsigned"]["signatures"],
            network=_["bytom"]["network"]
        )
