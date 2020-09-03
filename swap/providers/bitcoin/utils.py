#!/usr/bin/env python3

from btcpy.structs.script import P2pkhScript, P2shScript
from btcpy.structs.transaction import Sequence, MutableTransaction
from btcpy.structs.address import Address
from btcpy.setup import setup as stp
from base64 import b64decode

import cryptos
import json
import datetime
import binascii
import requests

from ..config import bitcoin
from ...utils.exceptions import AddressError, NetworkError, APIError

# Request headers
headers = dict()
headers.setdefault("Content-Type", "application/json")

# Bitcoin configuration
bitcoin = bitcoin()


def decode_transaction_raw(transaction_raw):
    """
    Decode Bitcoin transaction raw.

    :param transaction_raw: Bitcoin transaction raw.
    :type transaction_raw: str
    :returns: dict -- decoded Bitcoin transaction.

    >>> from swap.providers.bitcoin.utils import decode_transaction_raw
    >>> transaction_raw = "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTg4OGJlN2VjMDY1MDk3ZDk1NjY0NzYzZjI3NmQ0MjU1NTJkNzM1ZmIxZDk3NGFlNzhiZjcyMTA2ZGNhMGYzOTEwMTAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQyYmIwMTNjM2U0YmViMDg0MjFkZWRjZjgxNWNiNjVhNWMzODgxNzhiODdiY2RkMGUwMDAwMDAwMDAwMTk3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiA5ODQ5NDYsICJuIjogMSwgInNjcmlwdCI6ICI3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"
    >>> decode_transaction_raw(transaction_raw)
    {'fee': 678, 'type': 'bitcoin_fund_unsigned', 'tx': {'hex': '0200000001888be7ec065097d95664763f276d425552d735fb1d974ae78bf72106dca0f3910100000000ffffffff02102700000000000017a9142bb013c3e4beb08421dedcf815cb65a5c388178b87bcdd0e00000000001976a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac00000000', 'txid': 'abc70fd3466aec9478ea3115200a84f993204ad1f614fe08e92ecc5997a0d3ba', 'hash': 'abc70fd3466aec9478ea3115200a84f993204ad1f614fe08e92ecc5997a0d3ba', 'size': 117, 'vsize': 117, 'version': 2, 'locktime': 0, 'vin': [{'txid': '91f3a0dc0621f78be74a971dfb35d75255426d273f766456d9975006ece78b88', 'vout': 1, 'scriptSig': {'asm': '', 'hex': ''}, 'sequence': '4294967295'}], 'vout': [{'value': '0.00010000', 'n': 0, 'scriptPubKey': {'asm': 'OP_HASH160 2bb013c3e4beb08421dedcf815cb65a5c388178b OP_EQUAL', 'hex': 'a9142bb013c3e4beb08421dedcf815cb65a5c388178b87', 'type': 'p2sh', 'address': '2MwEDybGC34949zgzWX4M9FHmE3crDSUydP'}}, {'value': '0.00974268', 'n': 1, 'scriptPubKey': {'asm': 'OP_DUP OP_HASH160 64a8390b0b1685fcbf2d4b457118dc8da92d5534 OP_EQUALVERIFY OP_CHECKSIG', 'hex': '76a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac', 'type': 'p2pkh', 'address': 'mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q'}}]}, 'network': 'testnet'}
    """

    transaction_raw = str(transaction_raw + "=" * (-len(transaction_raw) % 4))
    try:
        decoded_transaction_raw = json.loads(b64decode(str(transaction_raw).encode()).decode())
    except (binascii.Error, json.decoder.JSONDecodeError) as _error:
        raise ValueError("invalid Bitcoin transaction raw")
    if "type" not in decoded_transaction_raw or not str(decoded_transaction_raw["type"]).startswith("bitcoin"):
        raise ValueError("invalid Bitcoin transaction raw")
    # Setting testnet
    stp(decoded_transaction_raw["network"], strict=True)
    tx = MutableTransaction.unhexlify(decoded_transaction_raw["raw"])
    return dict(
        fee=decoded_transaction_raw["fee"],
        type=decoded_transaction_raw["type"],
        tx=tx.to_json(),
        network=decoded_transaction_raw["network"]
    )


def submit_payment(tx_raw, network="testnet", timeout=bitcoin["timeout"]):
    if isinstance(tx_raw, str):
        tx = json.dumps(dict(tx_hex=tx_raw))
        if "mainnet" == network:
            sochain_network = "BTC"
        elif "testnet" == network:
            sochain_network = "BTCTEST"
        else:
            raise ValueError("invalid network, only mainnet or testnet")
        url = bitcoin[network]["sochain"] + f"/send_tx/{sochain_network}"
        response = requests.post(url=url, data=tx, headers=headers, timeout=timeout)
        if "status" in response.json() and response.json()["status"] == "fail":
            raise APIError(response.json()["data"]["tx_hex"])
        elif "status" in response.json() and response.json()["status"] == "success":
            return response.json()["data"]
        else:
            raise Exception("Unknown Bitcoin submit payment error")
    raise TypeError("transaction raw must be string format!")


def submit_transaction_raw(transaction_raw):
    """
    Submit transaction raw to Bitcoin blockchain.

    :param transaction_raw: Bitcoin transaction raw.
    :type transaction_raw: str
    :returns: dict -- Bitcoin transaction id, fee, type and date.

    >>> from swap.providers.bitcoin.utils import submit_transaction_raw
    >>> transaction_raw = "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTg4OGJlN2VjMDY1MDk3ZDk1NjY0NzYzZjI3NmQ0MjU1NTJkNzM1ZmIxZDk3NGFlNzhiZjcyMTA2ZGNhMGYzOTEwMTAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQyYmIwMTNjM2U0YmViMDg0MjFkZWRjZjgxNWNiNjVhNWMzODgxNzhiODdiY2RkMGUwMDAwMDAwMDAwMTk3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiA5ODQ5NDYsICJuIjogMSwgInNjcmlwdCI6ICI3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"
    >>> submit_transaction_raw(transaction_raw)
    {'fee': '...', 'type': '...', 'transaction_id': '...', 'network': '...', 'date': '...'}
    """

    tx_raw = str(transaction_raw + "=" * (-len(transaction_raw) % 4))
    try:
        # Decoding transaction raw.
        decoded_tx_raw = json.loads(b64decode(str(tx_raw).encode()).decode())
    except (binascii.Error, json.decoder.JSONDecodeError) as _error:
        raise ValueError("invalid Bitcoin transaction raw")
    if "type" not in decoded_tx_raw or not str(decoded_tx_raw["type"]).startswith("bitcoin"):
        raise ValueError("invalid Bitcoin transaction raw")
    submitted = submit_payment(
        tx_raw=decoded_tx_raw["raw"],
        network=decoded_tx_raw["network"]
    )
    return dict(
        fee=decoded_tx_raw["fee"],
        type=decoded_tx_raw["type"],
        transaction_id=submitted["txid"],
        network=decoded_tx_raw["network"],
        date=str(datetime.datetime.utcnow())
    )


def is_address(address, network=None):
    """
    Check Bitcoin address.

    :param address: Bitcoin address.
    :type address: str
    :param network: Bitcoin network, defaults to None.
    :type network: str
    :returns: bool -- Bitcoin valid/invalid address.

    >>> from swap.providers.bitcoin.utils import is_address
    >>> is_address("mrmtGq2HMmqAogSsGDjCtXUpxrb7rHThFH", "testnet")
    True
    """

    if isinstance(address, str):
        if network is None:
            for boolean in [True, False]:
                valid = False
                if cryptos.Bitcoin(testnet=boolean).is_address(address):
                    valid = True
                    break
            return valid
        if network == "mainnet":
            return cryptos.Bitcoin(testnet=False).is_address(address)
        elif network == "testnet":
            return cryptos.Bitcoin(testnet=True).is_address(address)
        else:
            raise NetworkError("invalid %s network" % network, "only takes mainnet or testnet networks.")
    raise TypeError("address must be string format!")


def fee_calculator(transaction_input=1, transaction_output=1):
    """
    Bitcoin fee calculator.

    :param transaction_input: transaction input numbers, defaults to 1.
    :type transaction_input: int
    :param transaction_output: transaction output numbers, defaults to 1.
    :type transaction_output: int
    :returns: int -- Bitcoin fee.

    >>> from swap.providers.bitcoin.utils import fee_calculator
    >>> fee_calculator(2, 9)
    1836
    """

    # 444 input 102 output
    transaction_input = ((transaction_input - 1) * 444) + 576
    transaction_output = ((transaction_output - 1) * 102)
    return transaction_input + transaction_output


def expiration_to_script(sequence):

    if isinstance(sequence, int):
        if sequence <= 16:
            return "OP_%d" % sequence
        else:
            return Sequence(sequence).for_script()
    raise TypeError("Sequence must be integer format!")


def script_from_address(address, network="testnet"):

    if not is_address(address, network):
        raise AddressError("invalid %s %s address!" % (network, address))

    load_address = Address.from_string(address)
    get_type = load_address.get_type()
    if str(get_type) == "p2pkh":
        return P2pkhScript(load_address)
    elif str(get_type) == "p2sh":
        return P2shScript(load_address)


def address_to_hash(address, network="testnet"):
    """
    Get hash from address.

    :param address: Bitcoin address.
    :type address: str
    :param network: Bitcoin network, defaults to testnet.
    :type network: str
    :returns: P2pkhScript, P2shScript -- Bitcoin p2pkh or p2sh script instance.

    >>> from swap.providers.bitcoin.utils import address_to_hash
    >>> address_to_hash("mrmtGq2HMmqAogSsGDjCtXUpxrb7rHThFH", "testnet")
    "7b7c4431a43b612a72f8229935c469f1f6903658"
    """

    if not is_address(address, network):
        raise AddressError("invalid %s %s address!" % (network, address))
    return Address.from_string(address).hash.hex()
