#!/usr/bin/env python3

import pytest
import json
import os

from swap.providers.xinfin.rpc import (
    decode_raw, submit_raw
)

# Test Values
base_path = os.path.dirname(__file__)
file_path = os.path.abspath(os.path.join(base_path, "..", "..", "values.json"))
values = open(file_path, "r")
_ = json.loads(values.read())
values.close()


def test_xinfin_rpc():

    assert decode_raw(
        raw=_["xinfin"]["fund"]["signed"]["raw"],
    )

    # (600) {'code': -32000, 'message': 'invalid sender'}
    with pytest.raises(ValueError):
        submit_raw(
            raw=_["ethereum"]["fund"]["signed"]["raw"],
            network=_["xinfin"]["network"]
        )
