#!/usr/bin/env python3

import requests
import json

from ..config import bytom


# Request headers
headers = dict()
# headers.setdefault("Content-Type", "application/json")

# Bytom configuration
bytom = bytom()


# Get balance by address
def get_balance(address, network="testnet", limit=1, page=1, timeout=bytom["timeout"]):
    parameter = dict(limit=limit, page=page)
    url = str(bytom[network]["blockmeta"]) + ("/address/%s" % address)
    response = requests.get(url=url, params=parameter,
                            headers=headers, timeout=timeout)
    if response.status_code == 204:
        return 0
    return response.json()["balance"]


# Create account in blockcenter
def account_create(xpublic_key, label="1st address", email=None,
                   network="testnet", timeout=bytom["timeout"]):
    url = str(bytom[network]["blockcenter"]) + "/account/create"
    data = dict(pubkey=xpublic_key, label=label, email=email)
    response = requests.post(url=url, data=json.dumps(data),
                             headers=headers, timeout=timeout)
    if response.status_code == 200 and response.json()["code"] == 300:
        raise Exception(response.json()["message"])
    return response.json()["result"]["data"]


# List addresses from blockcenter
def list_address(guid, limit=10, network="testnet", timeout=bytom["timeout"]):
    url = str(bytom[network]["blockcenter"]) + "/account/list-address"
    response = requests.post(url=url, data=json.dumps(dict(guid=guid)),
                             params=dict(limit=limit), headers=headers, timeout=timeout)
    if response.status_code == 200 and response.json()["code"] == 300:
        raise Exception(response.json()["message"])
    return response.json()["result"]["data"]
