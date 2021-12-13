#!/usr/bin/env python3

from base64 import b64decode
from datetime import datetime
from web3.types import ChecksumAddress
from hexbytes.main import HexBytes
from web3 import Web3
from typing import (
    Union, Optional
)

import json
import sys
import os

from ...utils import clean_transaction_raw
from ...exceptions import (
    AddressError, UnitError, TransactionRawError
)
from ..config import ethereum as config


def is_network(network: str) -> bool:
    """
    Check Ethereum network.

    :param network: Ethereum network.
    :type network: str

    :returns: bool -- Ethereum valid/invalid network.

    >>> from swap.providers.ethereum.utils import is_network
    >>> is_network(network="kovan")
    True
    """

    # Check parameter instances
    if not isinstance(network, str):
        raise TypeError(f"Network must be str, not '{type(network)}' type.")

    return network in ["mainnet", "ropsten", "kovan", "rinkeby", "testnet"]


def is_address(address: str) -> bool:
    """
    Check Ethereum address.

    :param address: Ethereum address.
    :type address: str

    :returns: bool -- Ethereum valid/invalid address.

    >>> from swap.providers.ethereum.utils import is_address
    >>> is_address(address="0x1ee11011ae12103a488a82dc33e03f337bc93ba7")
    True
    """

    # Check parameter instances
    if not isinstance(address, str):
        raise TypeError(f"Address must be str, not '{type(address)}' type.")

    return Web3.isAddress(address)


def is_checksum_address(address: str) -> bool:
    """
    Check Ethereum checksum address.

    :param address: Ethereum address.
    :type address: str

    :returns: bool -- Ethereum valid/invalid checksum address.

    >>> from swap.providers.ethereum.utils import is_checksum_address
    >>> is_checksum_address(address="0x1ee11011ae12103a488a82dc33e03f337bc93ba7")
    False
    >>> is_checksum_address(address="0x1Ee11011ae12103a488A82DC33e03f337Bc93ba7")
    True
    """

    # Check parameter instances
    if not isinstance(address, str):
        raise TypeError(f"Address must be str, not '{type(address)}' type.")

    return Web3.isChecksumAddress(address)


def to_checksum_address(address: str) -> ChecksumAddress:
    """
    Change Ethereum address to checksum address.

    :param address: Ethereum address.
    :type address: ChecksumAddress

    :returns: str -- Ethereum checksum address.

    >>> from swap.providers.ethereum.utils import to_checksum_address
    >>>  is_checksum_address(address="0x1ee11011ae12103a488a82dc33e03f337bc93ba7")
    "0x1Ee11011ae12103a488A82DC33e03f337Bc93ba7"
    """

    # Check parameter instances
    if not is_address(address):
        raise AddressError(f"Invalid Ethereum '{type(address)}' address.")

    return Web3.toChecksumAddress(address)


def is_transaction_raw(transaction_raw: str) -> bool:
    """
    Check Ethereum transaction raw.

    :param transaction_raw: Ethereum transaction raw.
    :type transaction_raw: str

    :returns: bool -- Ethereum valid/invalid transaction raw.

    >>> from swap.providers.ethereum.utils import is_transaction_raw
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
            "ethereum_normal_unsigned", "ethereum_normal_signed", "ethereum_erc20_normal_unsigned", "ethereum_erc20_normal_signed",
            "ethereum_fund_unsigned", "ethereum_fund_signed", "ethereum_erc20_fund_unsigned", "ethereum_erc20_fund_signed",
            "ethereum_withdraw_unsigned", "ethereum_withdraw_signed", "ethereum_erc20_withdraw_unsigned", "ethereum_erc20_withdraw_signed",
            "ethereum_refund_unsigned", "ethereum_refund_signed", "ethereum_erc20_refund_unsigned", "ethereum_erc20_refund_signed"
        ]
    except:
        return False


def get_erc20_data(key: str) -> dict:
    # Get current working directory path (like linux or unix path).
    cwd: str = os.path.dirname(sys.modules[__package__].__file__)
    with open(f"{cwd}/contracts/libs/erc20.json", "r") as erc20_json_file:
        erc20_data: dict = json.loads(erc20_json_file.read())["erc20.sol:ERC20"]
        erc20_json_file.close()
    return erc20_data[key]


def decode_transaction_raw(transaction_raw: str) -> dict:
    """
    Decode Ethereum transaction raw.

    :param transaction_raw: Ethereum transaction raw.
    :type transaction_raw: str

    :returns: dict -- Decoded ethereum transaction raw.

    >>> from swap.providers.ethereum.utils import decode_transaction_raw
    >>> transaction_raw: str = "eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcWU5MHFqdDl3NG04cnQzdG51dTBwenAyNGRrZmZlbHlzOHpjd3llIiwgInJhdyI6ICIwNzAxMDAwMjAxNWYwMTVkMzA1YTI4ZDhkMzRiNDBjNjU5MzY4MTBmOWU5YzFmOGJjOWM3OTNlYzJlNzJjNzBmOTIwM2ZiYmViMGE1NmRiOWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGFkZTIwNDAxMDExNjAwMTQwZTQzYTkyYTllOGFjYTc4OGViMTU1MWMzMTY0NDhjMmUzZjc4MjE1MDEwMDAxNWYwMTVkMjAyZmQyNTU3YjY3ZjFkZjhiOGFjZWYwNjZmNWQ0NmE4NTAwODE0MzliNDE5MzI1ZDU1ZGJkOTM0MWUxMWFjNGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MDg0YWY1ZjAxMDExNjAwMTRjOTVlMDkyY2FlYWVjZTM1YzU3M2U3MWUxMTA1NTU2ZDkyOWNmYzkwMjIwMTIwNTk5MDdmZGFkMGZmOTVmZWJhNDNhZWYzN2QyZTU1YzU3YjZlMTg2Y2QzYWQxN2M4M2U2YzgwYzY1ODIxOGI2NTAyMDEzYWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDExNjAwMTRjOTVlMDkyY2FlYWVjZTM1YzU3M2U3MWUxMTA1NTU2ZDkyOWNmYzkwMDAwMTNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmUwOTQ5MDY0MDExNjAwMTRjOTVlMDkyY2FlYWVjZTM1YzU3M2U3MWUxMTA1NTU2ZDkyOWNmYzkwMDAiLCAiaGFzaCI6ICI3NzlmYzliOWNhNGRiMTVkNDFhYzgwNDNlZDRlNDFkYjg4NDU2ZjA1YzljZmJhMDQ5MzYyZWNlZmQ2MjY3ZmMzIiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbIjMzZThkYThjZThlZjEzZmI0OTM4YTM3NGFlYTM2NjRlNGNkMmNkMDBmZGQ5ZDI5ODU5M2JkYmQ4NzJkNjZiODgiXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBbIjc1ZTg3Yzc5MzNiNGRjNGE4N2UwNmZlZDMyM2U4NDI1ZTU0YTQ5NGZmODBkYzdmOGM0NTUyY2RiMGE2YmM3NGEiXSwgInB1YmxpY19rZXkiOiAiNTk5MDdmZGFkMGZmOTVmZWJhNDNhZWYzN2QyZTU1YzU3YjZlMTg2Y2QzYWQxN2M4M2U2YzgwYzY1ODIxOGI2NSIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX2NsYWltX3Vuc2lnbmVkIn0"
    >>> decode_transaction_raw(transaction_raw=transaction_raw)
    {'fee': ..., 'type': '...', 'address': '...', 'transaction': {...}, 'unsigned_datas': [...], 'signatures': [...], 'network': '...'}
    """

    if not is_transaction_raw(transaction_raw=transaction_raw):
        raise TransactionRawError("Invalid Ethereum transaction raw.")

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


def submit_transaction_raw(transaction_raw: str, provider: str = config["provider"],
                           token: Optional[str] = None) -> dict:
    """
    Submit Ethereum transaction raw.

    :param transaction_raw: Ethereum transaction raw.
    :type transaction_raw: str
    :param provider: Ethereum network provider, defaults to ``http``.
    :type provider: str
    :param token: Infura API endpoint token, defaults to ``4414fea5f7454211956b1627621450b4``.
    :type token: str

    :returns: dict -- Ethereum submitted transaction id, fee, type and date.

    >>> from swap.providers.ethereum.utils import submit_transaction_raw
    >>> transaction_raw: str = "eyJmZWUiOiAxMDAwMDAwMCwgImFkZHJlc3MiOiAiYm0xcWU5MHFqdDl3NG04cnQzdG51dTBwenAyNGRrZmZlbHlzOHpjd3llIiwgInJhdyI6ICIwNzAxMDAwMjAxNWYwMTVkMzA1YTI4ZDhkMzRiNDBjNjU5MzY4MTBmOWU5YzFmOGJjOWM3OTNlYzJlNzJjNzBmOTIwM2ZiYmViMGE1NmRiOWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MGFkZTIwNDAxMDExNjAwMTQwZTQzYTkyYTllOGFjYTc4OGViMTU1MWMzMTY0NDhjMmUzZjc4MjE1MDEwMDAxNWYwMTVkMjAyZmQyNTU3YjY3ZjFkZjhiOGFjZWYwNjZmNWQ0NmE4NTAwODE0MzliNDE5MzI1ZDU1ZGJkOTM0MWUxMWFjNGZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY4MDg0YWY1ZjAxMDExNjAwMTRjOTVlMDkyY2FlYWVjZTM1YzU3M2U3MWUxMTA1NTU2ZDkyOWNmYzkwMjIwMTIwNTk5MDdmZGFkMGZmOTVmZWJhNDNhZWYzN2QyZTU1YzU3YjZlMTg2Y2QzYWQxN2M4M2U2YzgwYzY1ODIxOGI2NTAyMDEzYWZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmY5MDRlMDExNjAwMTRjOTVlMDkyY2FlYWVjZTM1YzU3M2U3MWUxMTA1NTU2ZDkyOWNmYzkwMDAwMTNjZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmZmUwOTQ5MDY0MDExNjAwMTRjOTVlMDkyY2FlYWVjZTM1YzU3M2U3MWUxMTA1NTU2ZDkyOWNmYzkwMDAiLCAiaGFzaCI6ICI3NzlmYzliOWNhNGRiMTVkNDFhYzgwNDNlZDRlNDFkYjg4NDU2ZjA1YzljZmJhMDQ5MzYyZWNlZmQ2MjY3ZmMzIiwgInVuc2lnbmVkX2RhdGFzIjogW3siZGF0YXMiOiBbIjMzZThkYThjZThlZjEzZmI0OTM4YTM3NGFlYTM2NjRlNGNkMmNkMDBmZGQ5ZDI5ODU5M2JkYmQ4NzJkNjZiODgiXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJwYXRoIjogbnVsbH0sIHsiZGF0YXMiOiBbIjc1ZTg3Yzc5MzNiNGRjNGE4N2UwNmZlZDMyM2U4NDI1ZTU0YTQ5NGZmODBkYzdmOGM0NTUyY2RiMGE2YmM3NGEiXSwgInB1YmxpY19rZXkiOiAiNTk5MDdmZGFkMGZmOTVmZWJhNDNhZWYzN2QyZTU1YzU3YjZlMTg2Y2QzYWQxN2M4M2U2YzgwYzY1ODIxOGI2NSIsICJuZXR3b3JrIjogIm1haW5uZXQiLCAicGF0aCI6ICJtLzQ0LzE1My8xLzAvMSJ9XSwgInNpZ25hdHVyZXMiOiBbXSwgIm5ldHdvcmsiOiAibWFpbm5ldCIsICJ0eXBlIjogImJ5dG9tX2NsYWltX3Vuc2lnbmVkIn0"
    >>> submit_transaction_raw(transaction_raw=transaction_raw)
    {'fee': ..., 'type': '...', 'transaction_id': '...', 'network': '...', 'date': '...'}
    """

    # Check parameter instances
    if not is_transaction_raw(transaction_raw=transaction_raw):
        raise TransactionRawError("Invalid Ethereum transaction raw.")

    transaction_raw = clean_transaction_raw(transaction_raw)
    decoded_transaction_raw = b64decode(transaction_raw.encode())
    loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

    if not loaded_transaction_raw["type"] in [
        "ethereum_normal_signed", "ethereum_erc20_normal_signed",
        "ethereum_fund_signed", "ethereum_erc20_fund_signed",
        "ethereum_withdraw_signed", "ethereum_erc20_withdraw_signed",
        "ethereum_refund_signed", "ethereum_erc20_refund_signed"
    ]:
        raise TransactionRawError("Wrong Ethereum transaction raw must be signed, not unsigned transaction raw.")

    from .rpc import get_web3
    web3: Web3 = get_web3(
        network=loaded_transaction_raw["network"], provider=provider, token=token
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


def amount_unit_converter(amount: Union[int, float], unit_from: str = "Wei2Ether") -> Union[int, float]:
    """
    Ethereum amount unit converter.

    :param amount: Ethereum amount.
    :type amount: int, float
    :param unit_from: Ethereum unit, default to Wei2Ether
    :type unit_from: str

    :returns: int, float -- Ethereum amount.

    >>> from swap.providers.ethereum.utils import amount_unit_converter
    >>> amount_unit_converter(amount=100_000_000, unit_from="Wei2Ether")
    0.1
    """

    if unit_from not in ["Ether2Gwei", "Ether2Wei", "Gwei2Ether", "Gwei2Wei", "Wei2Ether", "Wei2Gwei"]:
        raise UnitError(f"Invalid Ethereum '{unit_from}' unit from",
                        "choose only 'Ether2Gwei', 'Ether2Wei', 'Gwei2Ether', 'Gwei2Wei', 'Wei2Ether' or 'Wei2Gwei' units.")

    # Constant values
    Ether, Gwei, Wei = (
        config["units"]["Ether"],
        config["units"]["Gwei"],
        config["units"]["Wei"]
    )

    if unit_from == "Ether2Gwei":
        return float((amount * Gwei) / Ether)
    elif unit_from == "Ether2Wei":
        return int((amount * Wei) / Ether)
    elif unit_from == "Gwei2Ether":
        return float((amount * Ether) / Gwei)
    elif unit_from == "Gwei2Wei":
        return int((amount * Wei) / Gwei)
    elif unit_from == "Wei2Ether":
        return float((amount * Ether) / Wei)
    elif unit_from == "Wei2Gwei":
        return int((amount * Gwei) / Wei)
