#!/usr/bin/env python3

from base64 import b64decode
from datetime import datetime
from pyxdc.utils import (
    is_address as _is_address,
    is_checksum_address as _is_checksum_address,
    to_checksum_address as _to_checksum_address
)
from web3.types import ChecksumAddress
from web3.datastructures import AttributeDict
from hexbytes.main import HexBytes
from web3 import Web3
from typing import Union

import json
import sys
import os

from ...utils import clean_transaction_raw
from ...exceptions import (
    AddressError, UnitError, TransactionRawError
)
from ..config import xinfin as config


def is_network(network: str) -> bool:
    """
    Check XinFin network.

    :param network: XinFin network.
    :type network: str

    :returns: bool -- XinFin valid/invalid network.

    >>> from swap.providers.xinfin.utils import is_network
    >>> is_network(network="apothem")
    True
    """

    # Check parameter instances
    if not isinstance(network, str):
        raise TypeError(f"Network must be str, not '{type(network)}' type.")

    return network in ["mainnet", "apothem", "testnet"]


def is_address(address: str) -> bool:
    """
    Check XinFin address.

    :param address: XinFin address.
    :type address: str

    :returns: bool -- XinFin valid/invalid address.

    >>> from swap.providers.xinfin.utils import is_address
    >>> is_address(address="xdc2224caA2235DF8Da3D2016d2AB1137D2d548A232")
    True
    """

    # Check parameter instances
    if not isinstance(address, str):
        raise TypeError(f"Address must be str, not '{type(address)}' type.")

    return _is_address(address=address)


def is_checksum_address(address: str) -> bool:
    """
    Check XinFin checksum address.

    :param address: XinFin address.
    :type address: str

    :returns: bool -- XinFin valid/invalid checksum address.

    >>> from swap.providers.xinfin.utils import is_checksum_address
    >>> is_checksum_address(address="xdc2224caA2235DF8Da3D2016d2AB1137D2d548A232")
    False
    >>> is_checksum_address(address="xdc1Ee11011ae12103a488A82DC33e03f337Bc93ba7")
    True
    """

    # Check parameter instances
    if not isinstance(address, str):
        raise TypeError(f"Address must be str, not '{type(address)}' type.")

    return _is_checksum_address(address=address)


def to_checksum_address(address: str, prefix: str = "xdc") -> Union[str, ChecksumAddress]:
    """
    Change XinFin address to checksum address.

    :param address: XinFin address.
    :type address: str
    :param prefix: XinFin address prefix, default to ``xdc``.
    :type prefix: str

    :returns: str, ChecksumAddress -- XinFin checksum address.

    >>> from swap.providers.xinfin.utils import to_checksum_address
    >>>  to_checksum_address(address="xdc2224caA2235DF8Da3D2016d2AB1137D2d548A232")
    "xdc2224caA2235DF8Da3D2016d2AB1137D2d548A232"
    """

    # Check parameter instances
    if not is_address(address):
        raise AddressError(f"Invalid XinFin '{type(address)}' address.")

    return ChecksumAddress(_to_checksum_address(address=address, prefix="0x")) \
        if prefix == "0x" else _to_checksum_address(address=address, prefix=prefix)


def is_transaction_raw(transaction_raw: str) -> bool:
    """
    Check XinFin transaction raw.

    :param transaction_raw: XinFin transaction raw.
    :type transaction_raw: str

    :returns: bool -- XinFin valid/invalid transaction raw.

    >>> from swap.providers.xinfin.utils import is_transaction_raw
    >>> transaction_raw: str = "eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcWU5MHFqdDl3NG04cnQzdG51dTBwenAyNGRrZmZlbHlzOHpjd3llIiwgInJhdyI6ICIwNzAxMDAwMjAxNWYwMTVkMzA1YTI4ZDhkMzRiNDBjNjU5MzY4MTBmOWU5YzFmOGJjOWM3OTNlYzJlNzJjNzBmOTIwM2ZiYmViMGE1NmRiOWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGFkZTIwNDAxMDExNjAwMTQwZTQzYTkyYTllOGFjYTc4OGViMTU1MWMzMTY0NDhjMmUzZjc4MjE1MDEwMDAxNWYwMTVkMjAyZmQyNTU3YjY3ZjFkZjhiOGFjZWYwNjZmNWQ0NmE4NTAwODE0MzliNDE5MzI1ZDU1ZGJkOTM0MWUxMWFjNGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MDg0YWY1ZjAxMDExNjAwMTRjOTVlMDkyY2FlYWVjZTM1YzU3M2U3MWUxMTA1NTU2ZDkyOWNmYzkwMjIwMTIwNTk5MDdmZGFkMGZmOTVmZWJhNDNhZWYzN2QyZTU1YzU3YjZlMTg2Y2QzYWQxN2M4M2U2YzgwYzY1ODIxOGI2NTAyMDEzYWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDExNjAwMTRjOTVlMDkyY2FlYWVjZTM1YzU3M2U3MWUxMTA1NTU2ZDkyOWNmYzkwMDAwMTNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmUwOTQ5MDY0MDExNjAwMTRjOTVlMDkyY2FlYWVjZTM1YzU3M2U3MWUxMTA1NTU2ZDkyOWNmYzkwMDAiLCAiaGFzaCI6ICI3NzlmYzliOWNhNGRiMTVkNDFhYzgwNDNlZDRlNDFkYjg4NDU2ZjA1YzljZmJhMDQ5MzYyZWNlZmQ2MjY3ZmMzIiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbIjMzZThkYThjZThlZjEzZmI0OTM4YTM3NGFlYTM2NjRlNGNkMmNkMDBmZGQ5ZDI5ODU5M2JkYmQ4NzJkNjZiODgiXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBbIjc1ZTg3Yzc5MzNiNGRjNGE4N2UwNmZlZDMyM2U4NDI1ZTU0YTQ5NGZmODBkYzdmOGM0NTUyY2RiMGE2YmM3NGEiXSwgInB1YmxpY19rZXkiOiAiNTk5MDdmZGFkMGZmOTVmZWJhNDNhZWYzN2QyZTU1YzU3YjZlMTg2Y2QzYWQxN2M4M2U2YzgwYzY1ODIxOGI2NSIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX2NsYWltX3Vuc2lnbmVkIn0"
    >>> is_transaction_raw(transaction_raw=transaction_raw)
    True
    """

    # Check parameter instances
    if not isinstance(transaction_raw, str):
        raise TypeError(f"Transaction raw must be str, not '{type(transaction_raw)}' type.")

    try:
        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())
        return loaded_transaction_raw["type"] in [
            "xinfin_normal_unsigned", "xinfin_normal_signed", "xinfin_xrc20_normal_unsigned", "xinfin_xrc20_normal_signed",
            "xinfin_fund_unsigned", "xinfin_fund_signed", "xinfin_xrc20_fund_unsigned", "xinfin_xrc20_fund_signed",
            "xinfin_withdraw_unsigned", "xinfin_withdraw_signed", "xinfin_xrc20_withdraw_unsigned", "xinfin_xrc20_withdraw_signed",
            "xinfin_refund_unsigned", "xinfin_refund_signed", "xinfin_xrc20_refund_unsigned", "xinfin_xrc20_refund_signed"
        ]
    except:
        return False


def get_xrc20_data(key: str) -> dict:
    # Get current working directory path (like linux or unix path).
    cwd: str = os.path.dirname(sys.modules[__package__].__file__)
    with open(f"{cwd}/contracts/libs/xrc20.json", "r") as xrc20_json_file:
        xrc20_data: dict = json.loads(xrc20_json_file.read())["xrc20.sol:XRC20"]
        xrc20_json_file.close()
    return xrc20_data[key]


def decode_transaction_raw(transaction_raw: str) -> dict:
    """
    Decode XinFin transaction raw.

    :param transaction_raw: XinFin transaction raw.
    :type transaction_raw: str

    :returns: dict -- Decoded xinfin transaction raw.

    >>> from swap.providers.xinfin.utils import decode_transaction_raw
    >>> transaction_raw: str = "eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcWU5MHFqdDl3NG04cnQzdG51dTBwenAyNGRrZmZlbHlzOHpjd3llIiwgInJhdyI6ICIwNzAxMDAwMjAxNWYwMTVkMzA1YTI4ZDhkMzRiNDBjNjU5MzY4MTBmOWU5YzFmOGJjOWM3OTNlYzJlNzJjNzBmOTIwM2ZiYmViMGE1NmRiOWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGFkZTIwNDAxMDExNjAwMTQwZTQzYTkyYTllOGFjYTc4OGViMTU1MWMzMTY0NDhjMmUzZjc4MjE1MDEwMDAxNWYwMTVkMjAyZmQyNTU3YjY3ZjFkZjhiOGFjZWYwNjZmNWQ0NmE4NTAwODE0MzliNDE5MzI1ZDU1ZGJkOTM0MWUxMWFjNGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MDg0YWY1ZjAxMDExNjAwMTRjOTVlMDkyY2FlYWVjZTM1YzU3M2U3MWUxMTA1NTU2ZDkyOWNmYzkwMjIwMTIwNTk5MDdmZGFkMGZmOTVmZWJhNDNhZWYzN2QyZTU1YzU3YjZlMTg2Y2QzYWQxN2M4M2U2YzgwYzY1ODIxOGI2NTAyMDEzYWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDExNjAwMTRjOTVlMDkyY2FlYWVjZTM1YzU3M2U3MWUxMTA1NTU2ZDkyOWNmYzkwMDAwMTNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmUwOTQ5MDY0MDExNjAwMTRjOTVlMDkyY2FlYWVjZTM1YzU3M2U3MWUxMTA1NTU2ZDkyOWNmYzkwMDAiLCAiaGFzaCI6ICI3NzlmYzliOWNhNGRiMTVkNDFhYzgwNDNlZDRlNDFkYjg4NDU2ZjA1YzljZmJhMDQ5MzYyZWNlZmQ2MjY3ZmMzIiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbIjMzZThkYThjZThlZjEzZmI0OTM4YTM3NGFlYTM2NjRlNGNkMmNkMDBmZGQ5ZDI5ODU5M2JkYmQ4NzJkNjZiODgiXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBbIjc1ZTg3Yzc5MzNiNGRjNGE4N2UwNmZlZDMyM2U4NDI1ZTU0YTQ5NGZmODBkYzdmOGM0NTUyY2RiMGE2YmM3NGEiXSwgInB1YmxpY19rZXkiOiAiNTk5MDdmZGFkMGZmOTVmZWJhNDNhZWYzN2QyZTU1YzU3YjZlMTg2Y2QzYWQxN2M4M2U2YzgwYzY1ODIxOGI2NSIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX2NsYWltX3Vuc2lnbmVkIn0"
    >>> decode_transaction_raw(transaction_raw=transaction_raw)
    {'fee': ..., 'type': '...', 'address': '...', 'transaction': {...}, 'unsigned_datas': [...], 'signatures': [...], 'network': '...'}
    """

    if not is_transaction_raw(transaction_raw=transaction_raw):
        raise TransactionRawError("Invalid XinFin transaction raw.")

    transaction_raw = clean_transaction_raw(transaction_raw)
    decoded_transaction_raw = b64decode(transaction_raw.encode())
    loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

    return dict(
        fee=loaded_transaction_raw["fee"],
        transaction=loaded_transaction_raw["transaction"],
        signatures=loaded_transaction_raw["signature"],
        network=loaded_transaction_raw["network"],
        type=loaded_transaction_raw["type"],
    )


def submit_transaction_raw(transaction_raw: str, provider: str = config["provider"]) -> dict:
    """
    Submit XinFin transaction raw.

    :param transaction_raw: XinFin transaction raw.
    :type transaction_raw: str
    :param provider: XinFin network provider, defaults to ``http``.
    :type provider: str

    :returns: dict -- XinFin submitted transaction id, fee, type and date.

    >>> from swap.providers.xinfin.utils import submit_transaction_raw
    >>> transaction_raw: str = "eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcWU5MHFqdDl3NG04cnQzdG51dTBwenAyNGRrZmZlbHlzOHpjd3llIiwgInJhdyI6ICIwNzAxMDAwMjAxNWYwMTVkMzA1YTI4ZDhkMzRiNDBjNjU5MzY4MTBmOWU5YzFmOGJjOWM3OTNlYzJlNzJjNzBmOTIwM2ZiYmViMGE1NmRiOWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGFkZTIwNDAxMDExNjAwMTQwZTQzYTkyYTllOGFjYTc4OGViMTU1MWMzMTY0NDhjMmUzZjc4MjE1MDEwMDAxNWYwMTVkMjAyZmQyNTU3YjY3ZjFkZjhiOGFjZWYwNjZmNWQ0NmE4NTAwODE0MzliNDE5MzI1ZDU1ZGJkOTM0MWUxMWFjNGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MDg0YWY1ZjAxMDExNjAwMTRjOTVlMDkyY2FlYWVjZTM1YzU3M2U3MWUxMTA1NTU2ZDkyOWNmYzkwMjIwMTIwNTk5MDdmZGFkMGZmOTVmZWJhNDNhZWYzN2QyZTU1YzU3YjZlMTg2Y2QzYWQxN2M4M2U2YzgwYzY1ODIxOGI2NTAyMDEzYWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDExNjAwMTRjOTVlMDkyY2FlYWVjZTM1YzU3M2U3MWUxMTA1NTU2ZDkyOWNmYzkwMDAwMTNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmUwOTQ5MDY0MDExNjAwMTRjOTVlMDkyY2FlYWVjZTM1YzU3M2U3MWUxMTA1NTU2ZDkyOWNmYzkwMDAiLCAiaGFzaCI6ICI3NzlmYzliOWNhNGRiMTVkNDFhYzgwNDNlZDRlNDFkYjg4NDU2ZjA1YzljZmJhMDQ5MzYyZWNlZmQ2MjY3ZmMzIiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbIjMzZThkYThjZThlZjEzZmI0OTM4YTM3NGFlYTM2NjRlNGNkMmNkMDBmZGQ5ZDI5ODU5M2JkYmQ4NzJkNjZiODgiXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBbIjc1ZTg3Yzc5MzNiNGRjNGE4N2UwNmZlZDMyM2U4NDI1ZTU0YTQ5NGZmODBkYzdmOGM0NTUyY2RiMGE2YmM3NGEiXSwgInB1YmxpY19rZXkiOiAiNTk5MDdmZGFkMGZmOTVmZWJhNDNhZWYzN2QyZTU1YzU3YjZlMTg2Y2QzYWQxN2M4M2U2YzgwYzY1ODIxOGI2NSIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX2NsYWltX3Vuc2lnbmVkIn0"
    >>> submit_transaction_raw(transaction_raw=transaction_raw)
    {'fee': ..., 'type': '...', 'transaction_id': '...', 'network': '...', 'date': '...'}
    """

    # Check parameter instances
    if not is_transaction_raw(transaction_raw=transaction_raw):
        raise TransactionRawError("Invalid XinFin transaction raw.")

    transaction_raw = clean_transaction_raw(transaction_raw)
    decoded_transaction_raw = b64decode(transaction_raw.encode())
    loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

    if not loaded_transaction_raw["type"] in [
        "xinfin_normal_signed", "xinfin_xrc20_normal_signed",
        "xinfin_fund_signed", "xinfin_xrc20_fund_signed",
        "xinfin_withdraw_signed", "xinfin_xrc20_withdraw_signed",
        "xinfin_refund_signed", "xinfin_xrc20_refund_signed"
    ]:
        raise TransactionRawError("Wrong XinFin transaction raw must be signed, not unsigned transaction raw.")

    from .rpc import get_web3
    web3: Web3 = get_web3(
        network=loaded_transaction_raw["network"], provider=provider
    )
    transaction_hash: HexBytes = web3.eth.send_raw_transaction(
        loaded_transaction_raw["signature"]["rawTransaction"]
    )

    return dict(
        fee=loaded_transaction_raw["fee"],
        type=loaded_transaction_raw["type"],
        transaction_hash=transaction_hash.hex(),
        network=loaded_transaction_raw["network"],
        date=str(datetime.now())
    )


def amount_unit_converter(amount: Union[int, float], unit_from: str = "Wei2XDC") -> Union[int, float]:
    """
    XinFin amount unit converter.

    :param amount: XinFIn amount.
    :type amount: int, float
    :param unit_from: XinFIn unit from, default to ``Wei2XDC``
    :type unit_from: str

    :returns: int, float -- XinFin amount.

    >>> from swap.providers.xinfin.utils import amount_unit_converter
    >>> amount_unit_converter(amount=100_000_000, unit_from="Wei2XDC")
    0.1
    """

    if unit_from not in ["XDC2Gwei", "XDC2Wei", "Gwei2XDC", "Gwei2Wei", "Wei2XDC", "Wei2Gwei"]:
        raise UnitError(f"Invalid XinFin '{unit_from}' unit from",
                        "choose only 'XDC2Gwei', 'XDC2Wei', 'Gwei2XDC', 'Gwei2Wei', 'Wei2XDC' or 'Wei2Gwei' units.")

    # Constant values
    XDC, Gwei, Wei = (
        config["units"]["XDC"],
        config["units"]["Gwei"],
        config["units"]["Wei"]
    )

    if unit_from == "XDC2Gwei":
        return float((amount * Gwei) / XDC)
    elif unit_from == "XDC2Wei":
        return int((amount * Wei) / XDC)
    elif unit_from == "Gwei2XDC":
        return float((amount * XDC) / Gwei)
    elif unit_from == "Gwei2Wei":
        return int((amount * Wei) / Gwei)
    elif unit_from == "Wei2XDC":
        return float((amount * XDC) / Wei)
    elif unit_from == "Wei2Gwei":
        return int((amount * Gwei) / Wei)


class _AttributeDict:

    def __init__(self, data: dict):
        self._attribute_dict: AttributeDict = self.dict_attribute(data)

    def __attribute_dict__(self) -> AttributeDict:
        return self._attribute_dict

    @staticmethod
    def str_attribute(data: str) -> Union[HexBytes, str]:

        if is_address(data):
            return to_checksum_address(data, prefix="0x")
        elif data.startswith("0x"):
            return HexBytes(data)
        else:
            return data

    def dict_attribute(self, data: dict) -> AttributeDict:

        for key, value in data.items():
            if isinstance(value, str):
                data[key] = self.str_attribute(data[key])
            elif isinstance(value, dict):
                data[key] = self.dict_attribute(data[key])
            elif isinstance(value, list):
                data[key] = self.list_attribute(data[key])
        return AttributeDict(data)

    def list_attribute(self, datas: list) -> list:

        temp_datas: list = []
        for data in datas:
            if isinstance(data, str):
                temp_datas.append(self.str_attribute(data))
            elif isinstance(data, dict):
                temp_datas.append(self.dict_attribute(data))
            elif isinstance(data, list):
                temp_datas.append(self.list_attribute(data))
            else:
                temp_datas.append(data)
        return temp_datas
