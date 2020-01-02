#!/usr/bin/env python3

import requests
import json

from ..config import bytom


# Request headers
headers = dict()
headers.setdefault("Content-Type", "application/json")

# Bytom configuration
bytom = bytom()


# Get balance by address
def get_balance(address, network="testnet", limit=1, page=1, timeout=5):
    parameter = dict(limit=limit, page=page)
    url = str(bytom[network]["blockmeta"]) + ("/address/%s" % address)
    response = requests.get(url=url, params=parameter,
                            headers=headers, timeout=timeout)
    if response.status_code == 204:
        return 0
    return response.json()["balance"]
