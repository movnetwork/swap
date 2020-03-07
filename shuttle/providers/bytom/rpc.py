#!/usr/bin/env python3

import requests
import json

from ...utils.exceptions import ClientError, APIError
from ..config import bytom


# Request headers
headers = dict()
# headers.setdefault("Content-Type", "application/json")

# Bytom configuration
bytom = bytom()


# Get balance by address
def get_balance(address, network="testnet", limit=1, page=1, timeout=bytom["timeout"]):
    """
    Get bytom balance.

    :param address: bytom address.
    :type address: str
    :param network: bytom network, defaults to testnet.
    :type network: str
    :param limit: bytom limit, defaults to 1.
    :type limit: str
    :param page: bytom network, defaults to 1.
    :type page: str
    :param timeout: request timeout, default to 15.
    :type timeout: int
    :returns: int -- bytom balance.

    >>> from shuttle.providers.bytom.rpc import get_balance
    >>> get_balance(bytom_address, "mainnet")
    25800000
    """

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
    """
    Create account in blockcenter.

    :param xpublic_key: bytom xpublic key.
    :type xpublic_key: str
    :param label: bytom limit, defaults to 1st address.
    :type label: str
    :param email: email address, defaults to None.
    :type email: str
    :param network: bytom network, defaults to testnet.
    :type network: str
    :param timeout: request timeout, default to 15.
    :type timeout: int
    :returns: dict -- bytom blockcenter guid, address and label.

    >>> from shuttle.providers.bytom.rpc import account_create
    >>> account_create(xpublic_key, "mainnet")
    {"guid": "f0ed6ddd-9d6b-49fd-8866-a52d1083a13b", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "label": "1st address"}
    """

    url = str(bytom[network]["blockcenter"]) + "/account/create"
    data = dict(pubkey=xpublic_key, label=label, email=email)
    response = requests.post(url=url, data=json.dumps(data),
                             headers=headers, timeout=timeout)
    if response.status_code == 200 and response.json()["code"] == 300:
        raise APIError(response.json()["msg"])
    return response.json()["result"]["data"]


# List addresses from blockcenter
def list_address(guid, limit=10, network="testnet", timeout=bytom["timeout"]):
    """
    List address from blockcenter.

    :param guid: bytom blockcenter guid.
    :type guid: str
    :param limit: blockcenter limit default to 10.
    :type limit: int
    :param network: bytom network, defaults to testnet.
    :type network: str
    :param timeout: request timeout, default to 15.
    :type timeout: int
    :returns: list -- bytom blockcenter list of addresses.

    >>> from shuttle.providers.bytom.rpc import list_address
    >>> list_address(guid, 5 "mainnet")
    [{"guid": "f0ed6ddd-9d6b-49fd-8866-a52d1083a13b", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "label": "1st address", "balances": [{"asset": "f37dea62efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf", "balance": "100000000000", "total_received": "100000000000", "total_sent": "0", "decimals": 8, "alias": "Asset", "icon": "", "name": "f37dea62efd2965174b84bbb59a0bd0a671cf5fb2857303ffd77c1b482b84bdf", "symbol": "Asset", "in_usd": "0.00", "in_cny": "0.00", "in_btc": "0.000000"}, {"asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "balance": "2450000000", "total_received": "4950000000", "total_sent": "2500000000", "decimals": 8, "alias": "btm", "icon": "", "name": "BTM", "symbol": "BTM", "in_usd": "2.90", "in_cny": "20.58", "in_btc": "0.000283"}]}]
    """

    url = str(bytom[network]["blockcenter"]) + "/account/list-address"
    response = requests.post(url=url, data=json.dumps(dict(guid=guid)),
                             params=dict(limit=limit), headers=headers, timeout=timeout)
    if response.status_code == 200 and response.json()["code"] == 300:
        raise APIError(response.json()["msg"])
    return response.json()["result"]["data"]


# Build transaction in blockcenter
def build_transaction(tx, network="testnet", timeout=bytom["timeout"]):
    """
    Build bytom transaction in blockcenter.

    :param tx: bytom transaction.
    :type tx: dict
    :param network: bytom network, defaults to testnet.
    :type network: str
    :param timeout: request timeout, default to 15.
    :type timeout: int
    :returns: dict -- bytom built transaction.

    >>> from shuttle.providers.bytom.rpc import build_transaction
    >>> build_transaction(transaction, "mainnet")
    {"tx": {"hash": "2993414225f65390220730d0c1a356c14e91bca76db112d37366df93e364a492", "status_fail": false, "size": 379, "submission_timestamp": 0, "memo": "", "inputs": [{"script": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 2450000000, "type": "spend"}], "outputs": [{"utxo_id": "5edccebe497893c289121f9e365fdeb34c97008b9eb5a9960fe9541e7923aabc", "script": "01642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0", "address": "smart contract", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 1000, "type": "control"}, {"utxo_id": "f8cfbb692db1963be88b09c314adcc9e19d91c6c019aa556fb7cb76ba8ffa1fa", "script": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 2439999000, "type": "control"}], "fee": 10000000, "balances": [{"asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": "-10001000"}], "types": ["ordinary"]}, "raw_transaction": "070100010160015e7f2d7ecec3f61d30d0b2968973a3ac8448f0599ea20dce883b48c903c4d6e87fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8091a0900901011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a22012091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e20201ad01ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe80701880101642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c000013dffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff98dcbd8b09011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a00", "signing_instructions": [{"derivation_path": ["2c000000", "99000000", "01000000", "00000000", "01000000"], "sign_data": ["37727d44af9801e9723eb325592f4d55cc8d7e3815b1d663d61b7f1af9fc13a7"], "pubkey": "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2"}], "fee": 10000000}
    """

    url = str(bytom[network]["blockcenter"]) + "/merchant/build-transaction"
    response = requests.post(url=url, data=json.dumps(tx),
                             headers=headers, timeout=timeout)
    if response.status_code == 200 and response.json()["code"] == 300:
        raise APIError(response.json()["msg"])
    elif response.status_code == 200 and response.json()["code"] == 503:
        raise APIError(response.json()["msg"])
    return response.json()["result"]["data"]


# Get transaction from blockcenter
def get_transaction(tx_id, network="testnet", timeout=bytom["timeout"]):
    """
    Get bytom transaction detail.

    :param tx_id: bytom transaction id.
    :type tx_id: str
    :param network: bytom network, defaults to testnet.
    :type network: str
    :param timeout: request timeout, default to 15.
    :type timeout: int
    :returns: dict -- bytom built transaction.

    >>> from shuttle.providers.bytom.rpc import get_transaction
    >>> get_transaction(transaction_id, "mainnet")
    {"tx": {"hash": "2993414225f65390220730d0c1a356c14e91bca76db112d37366df93e364a492", "status_fail": false, "size": 379, "submission_timestamp": 0, "memo": "", "inputs": [{"script": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 2450000000, "type": "spend"}], "outputs": [{"utxo_id": "5edccebe497893c289121f9e365fdeb34c97008b9eb5a9960fe9541e7923aabc", "script": "01642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c0", "address": "smart contract", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 1000, "type": "control"}, {"utxo_id": "f8cfbb692db1963be88b09c314adcc9e19d91c6c019aa556fb7cb76ba8ffa1fa", "script": "00142cda4f99ea8112e6fa61cdd26157ed6dc408332a", "address": "bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", "asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": 2439999000, "type": "control"}], "fee": 10000000, "balances": [{"asset": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", "amount": "-10001000"}], "types": ["ordinary"]}, "raw_transaction": "070100010160015e7f2d7ecec3f61d30d0b2968973a3ac8448f0599ea20dce883b48c903c4d6e87fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8091a0900901011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a22012091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e20201ad01ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe80701880101642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01202b9a5949f5546f63a253e41cda6bffdedb527288a7e24ed953f5c2680c70d6ff741f547a6416000000557aa888537a7cae7cac631f000000537acd9f6972ae7cac00c000013dffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff98dcbd8b09011600142cda4f99ea8112e6fa61cdd26157ed6dc408332a00", "signing_instructions": [{"derivation_path": ["2c000000", "99000000", "01000000", "00000000", "01000000"], "sign_data": ["37727d44af9801e9723eb325592f4d55cc8d7e3815b1d663d61b7f1af9fc13a7"], "pubkey": "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2"}], "fee": 10000000}
    """

    url = str(bytom[network]["blockcenter"]) + "/merchant/get-transaction"
    response = requests.post(url=url, data=json.dumps(dict(tx_id=tx_id)),
                             headers=headers, timeout=timeout)
    if response.status_code == 200 and response.json()["code"] == 300:
        raise APIError(response.json()["msg"])
    return response.json()["result"]["data"]


# Submit payment from blockcenter
def submit_payment(guid, tx_raw, signatures,
                   network, memo="mock", timeout=bytom["timeout"]):
    """
     Submit transaction raw to Bytom blockchain.

    :param guid: bytom blockcenter id.
    :type guid: str
    :param tx_raw: bytom transaction raw.
    :type tx_raw: str
    :param signatures: bytom signed datas.
    :type signatures: list
    :param network: bytom network, defaults to testnet.
    :type network: str
    :param memo: memo, defaults to mock.
    :type memo: str
    :param timeout: request timeout, default to 15.
    :type timeout: int
    :returns: dict -- bytom transaction id, fee, type and date.

    >>> from shuttle.providers.bytom.rpc import submit_payment
    >>> submit_payment("guid", transaction_raw, [[...]], "mainent")
    {...}
    """
    if not isinstance(signatures, list):
        raise ClientError("signatures must be list format.")
    url = str(bytom[network]["blockcenter"]) + "/merchant/submit-payment"
    data = dict(guid=guid, raw_transaction=tx_raw, signatures=signatures, memo=memo)
    response = requests.post(url=url, data=json.dumps(data),
                             headers=headers, timeout=timeout)
    if response.json()["code"] != 200:
        raise APIError(response.json()["msg"])
    return response.json()["result"]["data"]


# Decode transaction raw
def decode_tx_raw(tx_raw, network="testnet", timeout=bytom["timeout"]):
    """
    Get decoded transaction raw.

    :param tx_raw: bytom transaction raw.
    :type tx_raw: str
    :param network: bytom network, defaults to testnet.
    :type network: str
    :param timeout: request timeout, default to 15.
    :type timeout: int
    :returns: dict -- bytom decoded transaction raw.

    >>> from shuttle.providers.bytom.rpc import decode_tx_raw
    >>> decode_tx_raw(transaction_raw, "testnet")
    {...}
    """
    
    url = str(bytom[network]["bytom"]) + "/decode-raw-transaction"
    response = requests.post(url=url, data=json.dumps(dict(raw_transaction=tx_raw)),
                             headers=headers, timeout=timeout)
    if response.status_code == 400:
        raise APIError(response.json()["msg"])
    return response.json()["data"]
