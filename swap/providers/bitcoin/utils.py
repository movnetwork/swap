#!/usr/bin/env python3

from btcpy.structs.script import (
    ScriptSig, Script
)
from btcpy.structs.transaction import (
    MutableTransaction, Sequence, TxIn, TxOut
)
from btcpy.structs.address import Address
from btcpy.setup import setup as stp
from btcpy.structs.script import (
    P2pkhScript, P2shScript
)
from base64 import b64decode
from typing import (
    Union, Optional, Tuple
)

import requests
import cryptos
import json
import datetime

from ...utils import clean_transaction_raw
from ...exceptions import (
    AddressError, NetworkError, APIError, UnitError, TransactionRawError
)
from ..config import bitcoin as config


def fee_calculator(transaction_input: int = 1, transaction_output: int = 1) -> int:
    """
    Bitcoin fee calculator.

    :param transaction_input: transaction input numbers, defaults to ``1``.
    :type transaction_input: int
    :param transaction_output: transaction output numbers, defaults to ``1``.
    :type transaction_output: int

    :returns: int -- Bitcoin fee (Satoshi amount).

    >>> from swap.providers.bitcoin.utils import fee_calculator
    >>> fee_calculator(transaction_input=2, transaction_output=9)
    1836
    """

    # 444 input 102 output
    transaction_input = ((transaction_input - 1) * 444) + 576
    transaction_output = ((transaction_output - 1) * 102)
    return transaction_input + transaction_output


def get_address_type(address: str) -> str:
    """
    Get Bitcoin address type.

    :param address: Bitcoin address.
    :type address: str

    :returns: str -- Bitcoin address type (P2PKH, P2SH).

    >>> from swap.providers.bitcoin.utils import get_address_type
    >>> get_address_type(address="mrmtGq2HMmqAogSsGDjCtXUpxrb7rHThFH")
    "p2pkh"
    """

    if not is_address(address=address):
        raise AddressError(f"Invalid Bitcoin '{address}' address.")

    loaded_address = Address.from_string(address)
    address_type = loaded_address.get_type()
    return str(address_type)


def is_network(network: str) -> bool:
    """
    Check Bitcoin network.

    :param network: Bitcoin network.
    :type network: str

    :returns: bool -- Bitcoin valid/invalid network.

    >>> from swap.providers.bitcoin.utils import is_network
    >>> is_network(network="testnet")
    True
    """

    if not isinstance(network, str):
        raise TypeError(f"Network must be str, not '{type(network)}' type.")
    return network in ["mainnet", "testnet"]


def is_address(address: str, network: Optional[str] = None, address_type: Optional[str] = None) -> bool:
    """
    Check Bitcoin address.

    :param address: Bitcoin address.
    :type address: str
    :param network: Bitcoin network, defaults to ``None``.
    :type network: str
    :param address_type: Bitcoin address type, defaults to ``None``.
    :type address_type: str

    :returns: bool -- Bitcoin valid/invalid address.

    >>> from swap.providers.bitcoin.utils import is_address
    >>> is_address(address="mrmtGq2HMmqAogSsGDjCtXUpxrb7rHThFH", network="testnet")
    True
    """

    if not isinstance(address, str):
        raise TypeError(f"Address must be str, not '{type(address)}' type.")
    if address_type and address_type not in ["p2pkh", "p2sh"]:
        raise TypeError("Address type must be str and choose only 'p2pkh' or 'p2sh' types.")

    if network is None:
        for boolean in [True, False]:
            valid = False
            if cryptos.Bitcoin(testnet=boolean).is_address(address):
                valid = True
                break
        if address_type:
            valid = True if valid and (get_address_type(address=address) == address_type) else False
        return valid

    if not is_network(network=network):
        raise NetworkError(f"Invalid Bitcoin '{network}' network",
                           "choose only 'mainnet' or 'testnet' networks.")

    valid: bool = False
    if network == "mainnet":
        valid = cryptos.Bitcoin(testnet=False).is_address(address)
        if address_type:
            valid = True if valid and (get_address_type(address=address) == address_type) else False
    elif network == "testnet":
        valid = cryptos.Bitcoin(testnet=True).is_address(address)
        if address_type:
            valid = True if valid and (get_address_type(address=address) == address_type) else False
    return valid


def is_transaction_raw(transaction_raw: str) -> bool:
    """
    Check Bitcoin transaction raw.

    :param transaction_raw: Bitcoin transaction raw.
    :type transaction_raw: str

    :returns: bool -- Bitcoin valid/invalid transaction raw.

    >>> from swap.providers.bitcoin.utils import is_transaction_raw
    >>> transaction_raw = "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTg4OGJlN2VjMDY1MDk3ZDk1NjY0NzYzZjI3NmQ0MjU1NTJkNzM1ZmIxZDk3NGFlNzhiZjcyMTA2ZGNhMGYzOTEwMTAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQyYmIwMTNjM2U0YmViMDg0MjFkZWRjZjgxNWNiNjVhNWMzODgxNzhiODdiY2RkMGUwMDAwMDAwMDAwMTk3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiA5ODQ5NDYsICJuIjogMSwgInNjcmlwdCI6ICI3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"
    >>> is_transaction_raw(transaction_raw=transaction_raw)
    True
    """

    if not isinstance(transaction_raw, str):
        raise TypeError(f"Transaction raw must be str, not '{type(transaction_raw)}' type.")

    try:
        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loads_transaction_raw = json.loads(decoded_transaction_raw.decode())
        return loads_transaction_raw["type"] in [
            "bitcoin_normal_unsigned", "bitcoin_normal_signed",
            "bitcoin_fund_unsigned", "bitcoin_fund_signed",
            "bitcoin_withdraw_unsigned", "bitcoin_withdraw_signed",
            "bitcoin_refund_unsigned", "bitcoin_refund_signed"
        ]
    except:
        return False


def amount_unit_converter(amount: Union[int, float], unit_from: str = "Satoshi2BTC") -> Union[int, float]:
    """
    Bitcoin amount unit converter

    :param amount: Bitcoin any amount.
    :type amount: Union[int, float]
    :param unit_from: Bitcoin unit convert from symbol, default to ``Satoshi2BTC``.
    :type unit_from: str

    :returns: int, float -- BTC asset amount.

    >>> from swap.providers.bitcoin.utils import amount_unit_converter
    >>> amount_unit_converter(amount=10_000_000, unit_from="Satoshi2BTC")
    0.1
    """

    if unit_from not in ["BTC2mBTC", "BTC2Satoshi", "mBTC2BTC", "mBTC2Satoshi", "Satoshi2BTC", "Satoshi2mBTC"]:
        raise UnitError(f"Invalid Bitcoin '{unit_from}' unit from",
                        "choose only 'BTC2mBTC', 'BTC2Satoshi', 'mBTC2BTC', 'mBTC2Satoshi', "
                        "'Satoshi2BTC' or 'Satoshi2mBTC' units.")

    # Constant unit values
    BTC, mBTC, Satoshi = (
        config["units"]["BTC"],
        config["units"]["mBTC"],
        config["units"]["Satoshi"]
    )

    if unit_from == "BTC2mBTC":
        return float((amount * mBTC) / BTC)
    elif unit_from == "BTC2Satoshi":
        return int((amount * Satoshi) / BTC)
    elif unit_from == "mBTC2BTC":
        return float((amount * BTC) / mBTC)
    elif unit_from == "mBTC2Satoshi":
        return int((amount * Satoshi) / mBTC)
    elif unit_from == "Satoshi2BTC":
        return float((amount * BTC) / Satoshi)
    elif unit_from == "Satoshi2mBTC":
        return int((amount * mBTC) / Satoshi)


def decode_transaction_raw(transaction_raw: str, offline: bool = True,
                           headers: dict = config["headers"], timeout: int = config["timeout"]) -> dict:
    """
    Decode Bitcoin transaction raw.

    :param transaction_raw: Bitcoin transaction raw.
    :type transaction_raw: str
    :param offline: Offline decode, defaults to ``True``.
    :type offline: bool
    :param headers: Request headers, default to ``common-headers``.
    :type headers: dict
    :param timeout: Request timeout, default to ``60``.
    :type timeout: int

    :returns: dict -- Decoded Bitcoin transaction raw.

    >>> from swap.providers.bitcoin.utils import decode_transaction_raw
    >>> transaction_raw = "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTg4OGJlN2VjMDY1MDk3ZDk1NjY0NzYzZjI3NmQ0MjU1NTJkNzM1ZmIxZDk3NGFlNzhiZjcyMTA2ZGNhMGYzOTEwMTAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQyYmIwMTNjM2U0YmViMDg0MjFkZWRjZjgxNWNiNjVhNWMzODgxNzhiODdiY2RkMGUwMDAwMDAwMDAwMTk3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiA5ODQ5NDYsICJuIjogMSwgInNjcmlwdCI6ICI3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"
    >>> decode_transaction_raw(transaction_raw=transaction_raw)
    {'fee': 678, 'type': 'bitcoin_fund_unsigned', 'tx': {'hex': '0200000001888be7ec065097d95664763f276d425552d735fb1d974ae78bf72106dca0f3910100000000ffffffff02102700000000000017a9142bb013c3e4beb08421dedcf815cb65a5c388178b87bcdd0e00000000001976a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac00000000', 'txid': 'abc70fd3466aec9478ea3115200a84f993204ad1f614fe08e92ecc5997a0d3ba', 'hash': 'abc70fd3466aec9478ea3115200a84f993204ad1f614fe08e92ecc5997a0d3ba', 'size': 117, 'vsize': 117, 'version': 2, 'locktime': 0, 'vin': [{'txid': '91f3a0dc0621f78be74a971dfb35d75255426d273f766456d9975006ece78b88', 'vout': 1, 'scriptSig': {'asm': '', 'hex': ''}, 'sequence': '4294967295'}], 'vout': [{'value': '0.00010000', 'n': 0, 'scriptPubKey': {'asm': 'OP_HASH160 2bb013c3e4beb08421dedcf815cb65a5c388178b OP_EQUAL', 'hex': 'a9142bb013c3e4beb08421dedcf815cb65a5c388178b87', 'type': 'p2sh', 'address': '2MwEDybGC34949zgzWX4M9FHmE3crDSUydP'}}, {'value': '0.00974268', 'n': 1, 'scriptPubKey': {'asm': 'OP_DUP OP_HASH160 64a8390b0b1685fcbf2d4b457118dc8da92d5534 OP_EQUALVERIFY OP_CHECKSIG', 'hex': '76a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac', 'type': 'p2pkh', 'address': 'mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q'}}]}, 'network': 'testnet'}
    """

    if not is_transaction_raw(transaction_raw=transaction_raw):
        raise TransactionRawError("Invalid Bitcoin transaction raw.")

    transaction_raw = clean_transaction_raw(transaction_raw)
    decoded_transaction_raw = b64decode(transaction_raw.encode())
    loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

    decoded_transaction: Optional[dict] = None

    if offline:
        stp(loaded_transaction_raw["network"], strict=True, force=True)
        tx = MutableTransaction.unhexlify(loaded_transaction_raw["raw"])
        decoded_transaction = tx.to_json()
    else:
        url = f"{config[loaded_transaction_raw['network']]['blockcypher']['url']}/txs/decode"
        parameter = dict(token=config[loaded_transaction_raw["network"]]["blockcypher"]["token"])
        data = dict(tx=loaded_transaction_raw["raw"])
        response = requests.post(
            url=url, data=json.dumps(data), params=parameter, headers=headers, timeout=timeout
        )
        decoded_transaction = response.json()

    return dict(
        fee=loaded_transaction_raw["fee"],
        type=loaded_transaction_raw["type"],
        transaction=decoded_transaction,
        network=loaded_transaction_raw["network"]
    )


def submit_transaction_raw(transaction_raw: str, endpoint: str = "sochain", headers: dict = config["headers"],
                           timeout: int = config["timeout"]) -> dict:
    """
    Submit transaction raw to Bitcoin blockchain.

    :param transaction_raw: Bitcoin transaction raw.
    :type transaction_raw: str
    :param endpoint: Bitcoin transaction submiter endpoint api name, defaults to ``sochain``.
    :type endpoint: str
    :param headers: Request headers, default to ``common-headers``.
    :type headers: dict
    :param timeout: Request timeout, default to ``60``.
    :type timeout: int

    :returns: dict -- Bitcoin submitted transaction id, fee, type and date.

    >>> from swap.providers.bitcoin.utils import submit_transaction_raw
    >>> transaction_raw = "eyJmZWUiOiA2NzgsICJyYXciOiAiMDIwMDAwMDAwMTg4OGJlN2VjMDY1MDk3ZDk1NjY0NzYzZjI3NmQ0MjU1NTJkNzM1ZmIxZDk3NGFlNzhiZjcyMTA2ZGNhMGYzOTEwMTAwMDAwMDAwZmZmZmZmZmYwMjEwMjcwMDAwMDAwMDAwMDAxN2E5MTQyYmIwMTNjM2U0YmViMDg0MjFkZWRjZjgxNWNiNjVhNWMzODgxNzhiODdiY2RkMGUwMDAwMDAwMDAwMTk3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYzAwMDAwMDAwIiwgIm91dHB1dHMiOiBbeyJhbW91bnQiOiA5ODQ5NDYsICJuIjogMSwgInNjcmlwdCI6ICI3NmE5MTQ2NGE4MzkwYjBiMTY4NWZjYmYyZDRiNDU3MTE4ZGM4ZGE5MmQ1NTM0ODhhYyJ9XSwgIm5ldHdvcmsiOiAidGVzdG5ldCIsICJ0eXBlIjogImJpdGNvaW5fZnVuZF91bnNpZ25lZCJ9"
    >>> submit_transaction_raw(transaction_raw=transaction_raw)
    {'fee': '...', 'type': '...', 'transaction_id': '...', 'network': '...', 'date': '...'}
    """

    if not is_transaction_raw(transaction_raw=transaction_raw):
        raise TransactionRawError("Invalid Bitcoin transaction raw.")

    transaction_raw = clean_transaction_raw(transaction_raw)
    decoded_transaction_raw = b64decode(transaction_raw.encode())
    loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

    if endpoint == "smartbit":
        url = f"{config[loaded_transaction_raw['network']]['smartbit']}/pushtx"
        data = dict(hex=loaded_transaction_raw["raw"])
        response = requests.post(
            url=url, data=json.dumps(data), headers=headers, timeout=timeout
        )
        response_json = response.json()
        if "success" in response_json and not response_json["success"]:
            raise APIError(response_json["error"]["message"], response_json["error"]["code"])
        elif "success" in response_json and response_json["success"]:
            return dict(
                fee=loaded_transaction_raw["fee"],
                type=loaded_transaction_raw["type"],
                transaction_hash=response_json["txid"],
                network=loaded_transaction_raw["network"],
                date=str(datetime.datetime.now())
            )
        else:
            raise APIError("Unknown Bitcoin submit payment error.")
    elif endpoint == "sochain":
        url = str(config[loaded_transaction_raw['network']]['sochain']).format(links="send_tx")
        data = dict(tx_hex=loaded_transaction_raw["raw"])
        response = requests.post(
            url=url, data=json.dumps(data), headers=headers, timeout=timeout
        )
        response_json = response.json()
        if "status" in response_json and response_json["status"] == "success":
            return dict(
                fee=loaded_transaction_raw["fee"],
                type=loaded_transaction_raw["type"],
                transaction_hash=response_json["data"]["txid"],
                network=loaded_transaction_raw["network"],
                date=str(datetime.datetime.now())
            )
        elif "status" in response_json and response_json["status"] == "fail":
            raise APIError(response_json["data"]["tx_hex"])
        else:
            raise APIError("Unknown Bitcoin submit payment error.")
    else:
        raise TypeError("Invalid Bitcoin endpoint api name, please choose only smartbit or sochain only.")


def get_address_hash(address: str, script: bool = False) -> Union[str, P2pkhScript, P2shScript]:
    """
    Get Bitcoin address hash.

    :param address: Bitcoin address.
    :type address: str
    :param script: Return script (P2pkhScript, P2shScript), default to ``False``.
    :type script: bool

    :returns: str -- Bitcoin address hash.

    >>> from swap.providers.bitcoin.utils import get_address_hash
    >>> get_address_hash(address="mrmtGq2HMmqAogSsGDjCtXUpxrb7rHThFH", script=False)
    "7b7c4431a43b612a72f8229935c469f1f6903658"
    """

    if not is_address(address=address):
        raise AddressError(f"Invalid Bitcoin '{address}' address.")

    loaded_address = Address.from_string(address)
    get_type = loaded_address.get_type()
    if not script:
        return loaded_address.hash.hex()
    if str(get_type) == "p2pkh":
        return P2pkhScript(loaded_address)
    elif str(get_type) == "p2sh":
        return P2shScript(loaded_address)


def _get_previous_transaction_indexes(utxos: list, amount: int, transaction_output: int = 2) -> Tuple[list, int]:
    temp_amount, max_amount = 0, 0
    previous_transaction_indexes: list = []
    for index, utxo in enumerate(utxos):
        temp_amount += utxo["value"]
        if temp_amount > (amount + fee_calculator((index + 1), transaction_output)):
            previous_transaction_indexes.append(index)
            break
        previous_transaction_indexes.append(index)
    for utxo in utxos:
        max_amount += utxo["value"]
    return previous_transaction_indexes, max_amount


def _build_inputs(utxos: list, previous_transaction_indexes: Optional[list] = None) -> tuple:
    inputs, amount = [], 0
    for index, utxo in enumerate(utxos):
        if previous_transaction_indexes is None or index in previous_transaction_indexes:
            amount += utxo["value"]
            inputs.append(
                TxIn(
                    txid=utxo["tx_hash"],
                    txout=utxo["tx_output_n"],
                    script_sig=ScriptSig.empty(),
                    sequence=Sequence.max()
                )
            )
    return inputs, amount


def _build_outputs(utxos: list, previous_transaction_indexes: Optional[list] = None, only_dict: bool = False) -> list:
    outputs = []
    for index, utxo in enumerate(utxos):
        if previous_transaction_indexes is None or index in previous_transaction_indexes:
            outputs.append(
                TxOut(
                    value=utxo["value"],
                    n=utxo["tx_output_n"],
                    script_pubkey=Script.unhexlify(
                        hex_string=utxo["script"]
                    )
                )
                if not only_dict else
                dict(
                    value=utxo["value"],
                    tx_output_n=utxo["tx_output_n"],
                    script=utxo["script"]
                )
            )
    return outputs
