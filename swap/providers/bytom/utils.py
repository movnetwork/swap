#!/usr/bin/env python3

from base64 import b64decode
from pybytom.utils import is_address as btm_is_address
from typing import Optional, Union

import requests
import json
import datetime

from ...utils import clean_transaction_raw
from ...exceptions import (
    NetworkError, APIError, TransactionRawError, UnitError, AddressError
)
from ..config import bytom as config


def amount_unit_converter(amount: Union[int, float], unit_from: str = "NEU2BTM") -> Union[int, float]:
    """
    Bytom amount unit converter

    :param amount: Bytom any amount.
    :type amount: int, float
    :param unit_from: Bytom unit convert from symbol, default to NEU2BTM.
    :type unit_from: str

    :returns: int, float -- BTM asset amount.

    >>> from swap.providers.bytom.utils import amount_unit_converter
    >>> amount_unit_converter(amount=10_000_000, unit_from="NEU2BTM")
    0.1
    """

    if unit_from not in ["BTM2mBTM", "BTM2NEU", "mBTM2BTM", "mBTM2NEU", "NEU2BTM", "NEU2mBTM"]:
        raise UnitError(f"Invalid Bytom '{unit_from}' unit from",
                        "choose only 'BTM2mBTM', 'BTM2NEU', 'mBTM2BTM', 'mBTM2NEU', "
                        "'NEU2BTM' or 'NEU2mBTM' units.")

    # Constant unit values
    BTM, mBTM, NEU = (1, 1000, 100_000_000)

    if unit_from == "BTM2mBTM":
        return float((amount * mBTM) / BTM)
    elif unit_from == "BTM2NEU":
        return int((amount * NEU) / BTM)
    elif unit_from == "mBTM2BTM":
        return float((amount * BTM) / mBTM)
    elif unit_from == "mBTM2NEU":
        return int((amount * NEU) / mBTM)
    elif unit_from == "NEU2BTM":
        return float((amount * BTM) / NEU)
    elif unit_from == "NEU2mBTM":
        return int((amount * mBTM) / NEU)


def get_address_type(address: str) -> Optional[str]:
    """
    Get Bytom address type.

    :param address: Bytom address.
    :type address: str

    :returns: str -- Bytom address type (P2WPKH, P2WSH).

    >>> from swap.providers.bytom.utils import get_address_type
    >>> get_address_type(address="bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7")
    "p2wpkh"
    """

    if not is_address(address=address):
        raise AddressError(f"Invalid Bytom '{address}' address.")

    if len(address) == 42:
        return "p2wpkh"
    elif len(address) == 62:
        return "p2wsh"
    else:
        return None


def is_network(network: str) -> bool:
    """
    Check Bytom network.

    :param network: Bytom network.
    :type network: str

    :returns: bool -- Bytom valid/invalid network.

    >>> from swap.providers.bytom.utils import is_network
    >>> is_network(network="solonet")
    True
    """

    if not isinstance(network, str):
        raise TypeError(f"Network must be str, not '{type(network)}' type.")
    return network in ["mainnet", "solonet", "testnet"]


def is_address(address: str, network: Optional[str] = None, address_type: Optional[str] = None) -> bool:
    """
    Check Bytom address.

    :param address: Bytom address.
    :type address: str
    :param network: Bytom network, defaults to None.
    :type network: str
    :param address_type: Bytom address type, defaults to None.
    :type address_type: str

    :returns: bool -- Bytom valid/invalid address.

    >>> from swap.providers.bytom.utils import is_address
    >>> is_address(address="bm1q9ndylx02syfwd7npehfxz4lddhzqsve2fu6vc7", network="mainnet")
    True
    """

    if not isinstance(address, str):
        raise TypeError(f"Address must be str, not '{type(address)}' type.")
    if address_type and address_type not in ["p2wpkh", "p2wsh"]:
        raise TypeError("Address type must be str and choose only 'p2wpkh' or 'p2wsh' types.")

    if network is None:
        valid = btm_is_address(address=address, vapor=False)
    elif not is_network(network=network):
        raise NetworkError(f"Invalid Bytom '{network}' network",
                           "choose only 'mainnet', 'solonet' or 'testnet' networks.")
    else:
        valid = btm_is_address(address=address, network=network, vapor=False)
    if address_type:
        return True if valid and (get_address_type(address=address) == address_type) else False
    return valid


def is_transaction_raw(transaction_raw: str) -> bool:
    """
    Check Bytom transaction raw.

    :param transaction_raw: Bytom transaction raw.
    :type transaction_raw: str

    :returns: bool -- Bytom valid/invalid transaction raw.

    >>> from swap.providers.bytom.utils import is_transaction_raw
    >>> transaction_raw = "eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcWU5MHFqdDl3NG04cnQzdG51dTBwenAyNGRrZmZlbHlzOHpjd3llIiwgInJhdyI6ICIwNzAxMDAwMjAxNWYwMTVkMzA1YTI4ZDhkMzRiNDBjNjU5MzY4MTBmOWU5YzFmOGJjOWM3OTNlYzJlNzJjNzBmOTIwM2ZiYmViMGE1NmRiOWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGFkZTIwNDAxMDExNjAwMTQwZTQzYTkyYTllOGFjYTc4OGViMTU1MWMzMTY0NDhjMmUzZjc4MjE1MDEwMDAxNWYwMTVkMjAyZmQyNTU3YjY3ZjFkZjhiOGFjZWYwNjZmNWQ0NmE4NTAwODE0MzliNDE5MzI1ZDU1ZGJkOTM0MWUxMWFjNGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MDg0YWY1ZjAxMDExNjAwMTRjOTVlMDkyY2FlYWVjZTM1YzU3M2U3MWUxMTA1NTU2ZDkyOWNmYzkwMjIwMTIwNTk5MDdmZGFkMGZmOTVmZWJhNDNhZWYzN2QyZTU1YzU3YjZlMTg2Y2QzYWQxN2M4M2U2YzgwYzY1ODIxOGI2NTAyMDEzYWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDExNjAwMTRjOTVlMDkyY2FlYWVjZTM1YzU3M2U3MWUxMTA1NTU2ZDkyOWNmYzkwMDAwMTNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmUwOTQ5MDY0MDExNjAwMTRjOTVlMDkyY2FlYWVjZTM1YzU3M2U3MWUxMTA1NTU2ZDkyOWNmYzkwMDAiLCAiaGFzaCI6ICI3NzlmYzliOWNhNGRiMTVkNDFhYzgwNDNlZDRlNDFkYjg4NDU2ZjA1YzljZmJhMDQ5MzYyZWNlZmQ2MjY3ZmMzIiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbIjMzZThkYThjZThlZjEzZmI0OTM4YTM3NGFlYTM2NjRlNGNkMmNkMDBmZGQ5ZDI5ODU5M2JkYmQ4NzJkNjZiODgiXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBbIjc1ZTg3Yzc5MzNiNGRjNGE4N2UwNmZlZDMyM2U4NDI1ZTU0YTQ5NGZmODBkYzdmOGM0NTUyY2RiMGE2YmM3NGEiXSwgInB1YmxpY19rZXkiOiAiNTk5MDdmZGFkMGZmOTVmZWJhNDNhZWYzN2QyZTU1YzU3YjZlMTg2Y2QzYWQxN2M4M2U2YzgwYzY1ODIxOGI2NSIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX2NsYWltX3Vuc2lnbmVkIn0"
    >>> is_transaction_raw(transaction_raw=transaction_raw)
    True
    """

    if not isinstance(transaction_raw, str):
        raise TypeError(f"Transaction raw must be str, not '{type(transaction_raw)}' type.")

    try:
        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())
        return loaded_transaction_raw["type"] in [
            "bytom_normal_unsigned", "bytom_normal_signed",
            "bytom_fund_unsigned", "bytom_fund_signed",
            "bytom_claim_unsigned", "bytom_claim_signed",
            "bytom_refund_unsigned", "bytom_refund_signed"
        ]
    except:
        return False


def decode_transaction_raw(transaction_raw: str, headers: dict = config["headers"],
                           timeout: int = config["timeout"]) -> dict:
    """
    Decode Bytom transaction raw.

    :param transaction_raw: Bytom transaction raw.
    :type transaction_raw: str
    :param headers: Request headers, default to common headers.
    :type headers: dict
    :param timeout: Request timeout, default to 60.
    :type timeout: int

    :returns: dict -- Decoded Bytom transaction raw.

    >>> from swap.providers.bytom.utils import decode_transaction_raw
    >>> transaction_raw = "eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcWU5MHFqdDl3NG04cnQzdG51dTBwenAyNGRrZmZlbHlzOHpjd3llIiwgInJhdyI6ICIwNzAxMDAwMjAxNWYwMTVkMzA1YTI4ZDhkMzRiNDBjNjU5MzY4MTBmOWU5YzFmOGJjOWM3OTNlYzJlNzJjNzBmOTIwM2ZiYmViMGE1NmRiOWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGFkZTIwNDAxMDExNjAwMTQwZTQzYTkyYTllOGFjYTc4OGViMTU1MWMzMTY0NDhjMmUzZjc4MjE1MDEwMDAxNWYwMTVkMjAyZmQyNTU3YjY3ZjFkZjhiOGFjZWYwNjZmNWQ0NmE4NTAwODE0MzliNDE5MzI1ZDU1ZGJkOTM0MWUxMWFjNGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MDg0YWY1ZjAxMDExNjAwMTRjOTVlMDkyY2FlYWVjZTM1YzU3M2U3MWUxMTA1NTU2ZDkyOWNmYzkwMjIwMTIwNTk5MDdmZGFkMGZmOTVmZWJhNDNhZWYzN2QyZTU1YzU3YjZlMTg2Y2QzYWQxN2M4M2U2YzgwYzY1ODIxOGI2NTAyMDEzYWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDExNjAwMTRjOTVlMDkyY2FlYWVjZTM1YzU3M2U3MWUxMTA1NTU2ZDkyOWNmYzkwMDAwMTNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmUwOTQ5MDY0MDExNjAwMTRjOTVlMDkyY2FlYWVjZTM1YzU3M2U3MWUxMTA1NTU2ZDkyOWNmYzkwMDAiLCAiaGFzaCI6ICI3NzlmYzliOWNhNGRiMTVkNDFhYzgwNDNlZDRlNDFkYjg4NDU2ZjA1YzljZmJhMDQ5MzYyZWNlZmQ2MjY3ZmMzIiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbIjMzZThkYThjZThlZjEzZmI0OTM4YTM3NGFlYTM2NjRlNGNkMmNkMDBmZGQ5ZDI5ODU5M2JkYmQ4NzJkNjZiODgiXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBbIjc1ZTg3Yzc5MzNiNGRjNGE4N2UwNmZlZDMyM2U4NDI1ZTU0YTQ5NGZmODBkYzdmOGM0NTUyY2RiMGE2YmM3NGEiXSwgInB1YmxpY19rZXkiOiAiNTk5MDdmZGFkMGZmOTVmZWJhNDNhZWYzN2QyZTU1YzU3YjZlMTg2Y2QzYWQxN2M4M2U2YzgwYzY1ODIxOGI2NSIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX2NsYWltX3Vuc2lnbmVkIn0"
    >>> decode_transaction_raw(transaction_raw=transaction_raw)
    {'fee': ..., 'type': '...', 'address': '...', 'transaction': {...}, 'unsigned_datas': [...], 'signatures': [...], 'network': '...'}
    """

    if not is_transaction_raw(transaction_raw=transaction_raw):
        raise TransactionRawError("Invalid Bytom transaction raw.")

    transaction_raw = clean_transaction_raw(transaction_raw)
    decoded_transaction_raw = b64decode(transaction_raw.encode())
    loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

    url = f"{config[loaded_transaction_raw['network']]['bytom-core']}/decode-raw-transaction"
    data = dict(raw_transaction=loaded_transaction_raw["raw"])
    response = requests.post(
        url=url, data=json.dumps(data), headers=headers, timeout=timeout
    )
    response_json = response.json()
    if response.status_code == 400:
        raise APIError(response_json["msg"], response_json["code"])

    return dict(
        fee=loaded_transaction_raw["fee"],
        address=loaded_transaction_raw["address"],
        type=loaded_transaction_raw["type"],
        tx=response_json["data"],
        unsigned_datas=loaded_transaction_raw["unsigned_datas"],
        signatures=loaded_transaction_raw["signatures"],
        network=loaded_transaction_raw["network"]
    )


def submit_transaction_raw(transaction_raw: str, headers: dict = config["headers"],
                           timeout: int = config["timeout"]) -> dict:
    """
    Submit Bytom transaction raw.

    :param transaction_raw: Bytom transaction raw.
    :type transaction_raw: str
    :param headers: Request headers, default to common headers.
    :type headers: dict
    :param timeout: Request timeout, default to 60.
    :type timeout: int

    :returns: dict -- Bytom submitted transaction id, fee, type and date.

    >>> from swap.providers.bytom.utils import submit_transaction_raw
    >>> transaction_raw = "eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcWU5MHFqdDl3NG04cnQzdG51dTBwenAyNGRrZmZlbHlzOHpjd3llIiwgInJhdyI6ICIwNzAxMDAwMjAxNWYwMTVkMzA1YTI4ZDhkMzRiNDBjNjU5MzY4MTBmOWU5YzFmOGJjOWM3OTNlYzJlNzJjNzBmOTIwM2ZiYmViMGE1NmRiOWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGFkZTIwNDAxMDExNjAwMTQwZTQzYTkyYTllOGFjYTc4OGViMTU1MWMzMTY0NDhjMmUzZjc4MjE1MDEwMDAxNWYwMTVkMjAyZmQyNTU3YjY3ZjFkZjhiOGFjZWYwNjZmNWQ0NmE4NTAwODE0MzliNDE5MzI1ZDU1ZGJkOTM0MWUxMWFjNGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MDg0YWY1ZjAxMDExNjAwMTRjOTVlMDkyY2FlYWVjZTM1YzU3M2U3MWUxMTA1NTU2ZDkyOWNmYzkwMjIwMTIwNTk5MDdmZGFkMGZmOTVmZWJhNDNhZWYzN2QyZTU1YzU3YjZlMTg2Y2QzYWQxN2M4M2U2YzgwYzY1ODIxOGI2NTAyMDEzYWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDExNjAwMTRjOTVlMDkyY2FlYWVjZTM1YzU3M2U3MWUxMTA1NTU2ZDkyOWNmYzkwMDAwMTNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmUwOTQ5MDY0MDExNjAwMTRjOTVlMDkyY2FlYWVjZTM1YzU3M2U3MWUxMTA1NTU2ZDkyOWNmYzkwMDAiLCAiaGFzaCI6ICI3NzlmYzliOWNhNGRiMTVkNDFhYzgwNDNlZDRlNDFkYjg4NDU2ZjA1YzljZmJhMDQ5MzYyZWNlZmQ2MjY3ZmMzIiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbIjMzZThkYThjZThlZjEzZmI0OTM4YTM3NGFlYTM2NjRlNGNkMmNkMDBmZGQ5ZDI5ODU5M2JkYmQ4NzJkNjZiODgiXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBbIjc1ZTg3Yzc5MzNiNGRjNGE4N2UwNmZlZDMyM2U4NDI1ZTU0YTQ5NGZmODBkYzdmOGM0NTUyY2RiMGE2YmM3NGEiXSwgInB1YmxpY19rZXkiOiAiNTk5MDdmZGFkMGZmOTVmZWJhNDNhZWYzN2QyZTU1YzU3YjZlMTg2Y2QzYWQxN2M4M2U2YzgwYzY1ODIxOGI2NSIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX2NsYWltX3Vuc2lnbmVkIn0"
    >>> submit_transaction_raw(transaction_raw=transaction_raw)
    {'fee': ..., 'type': '...', 'transaction_id': '...', 'network': '...', 'date': '...'}
    """

    if not is_transaction_raw(transaction_raw=transaction_raw):
        raise TransactionRawError("Invalid Bytom transaction raw.")

    transaction_raw = clean_transaction_raw(transaction_raw)
    decoded_transaction_raw = b64decode(transaction_raw.encode())
    loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

    url = f"{config[loaded_transaction_raw['network']]['blockcenter']}/merchant/submit-payment"
    data = dict(raw_transaction=loaded_transaction_raw["raw"], signatures=loaded_transaction_raw["signatures"])
    params = dict(address=loaded_transaction_raw["address"])
    response = requests.post(
        url=url, data=json.dumps(data), params=params, headers=headers, timeout=timeout
    )
    response_json = response.json()
    if response_json["code"] != 200 and response_json["code"] != 200:
        raise APIError(response_json["msg"], response_json["code"])

    return dict(
        fee=loaded_transaction_raw["fee"],
        type=loaded_transaction_raw["type"],
        transaction_id=response_json["data"]["tx_hash"],
        network=loaded_transaction_raw["network"],
        date=str(datetime.datetime.now())
    )
