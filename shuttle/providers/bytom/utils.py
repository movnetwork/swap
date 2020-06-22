#!/usr/bin/env python3

from base64 import b64encode, b64decode
from pybytom.signature import sign as btm_sign

import ed25519
import json
import binascii
import datetime

from .rpc import get_transaction, decode_tx_raw, submit_payment


def sign(private_key, message):
    return btm_sign(private_key, message)


def verify(public_key, signature, message):
    result = False
    verifying_key = ed25519.VerifyingKey(public_key.encode(), encoding="hex")
    try:
        verifying_key.verify(signature.encode(), bytes.fromhex(message), encoding="hex")
        result = True
    except ed25519.BadSignatureError:
        result = False
    return result


def find_contract_utxo_id(tx_id, network):
    """
    Find smart contract UTXO id.

    :param tx_id: Bytom transaction id or hash.
    :type tx_id: str
    :param network: Bytom network.
    :type network: str
    :returns: str -- UTXO id.

    >>> from shuttle.providers.bytom.utils import find_contract_utxo_id
    >>> find_contract_utxo_id(bytom_transaction_id, "mainnet")
    "9059cd0d03e4d4fab70a415169a45be47583f7240115c36cf298d6f261c0a1ac"
    """

    utxo_id = None
    contract_transaction = get_transaction(tx_id=tx_id, network=network)
    contract_outputs = contract_transaction["outputs"]
    for contract_output in contract_outputs:
        if contract_output["address"] == "smart contract":
            utxo_id = contract_output["utxo_id"]
            break
    return utxo_id


def decode_transaction_raw(transaction_raw):
    """
    Decode Bytom transaction raw.

    :param transaction_raw: Bytom transaction raw.
    :type transaction_raw: str
    :returns: dict -- decoded Bytom transaction.

    >>> from shuttle.providers.bytom.utils import decode_transaction_raw
    >>> decode_transaction_raw(transaction_raw)
    {...}
    """

    transaction_raw = str(transaction_raw + "=" * (-len(transaction_raw) % 4))
    try:
        # Decoding transaction raw.
        decoded_transaction_raw = json.loads(b64decode(str(transaction_raw).encode()).decode())
    except (binascii.Error, json.decoder.JSONDecodeError) as _error:
        raise ValueError("invalid Bytom transaction raw")
    if "type" not in decoded_transaction_raw or not str(decoded_transaction_raw["type"]).startswith("bytom"):
        raise ValueError("invalid Bytom transaction raw")
    return dict(
        fee=decoded_transaction_raw["fee"],
        guid=decoded_transaction_raw["guid"],
        type=decoded_transaction_raw["type"],
        tx=decode_tx_raw(tx_raw=decoded_transaction_raw["raw"]),
        unsigned_datas=decoded_transaction_raw["unsigned_datas"],
        signatures=decoded_transaction_raw["signatures"],
        network=decoded_transaction_raw["network"]
    )


def submit_transaction_raw(transaction_raw):
    """
    Submit transaction raw to Bytom blockchain.

    :param transaction_raw: Bytom transaction raw.
    :type transaction_raw: str
    :returns: dict -- Bytom transaction id, fee, type and date.

    >>> from shuttle.providers.bytom.utils import submit_transaction_raw
    >>> submit_transaction_raw(transaction_raw)
    {...}
    """

    transaction_raw = str(transaction_raw + "=" * (-len(transaction_raw) % 4))
    try:
        # Decoding transaction raw.
        decoded_tx_raw = json.loads(b64decode(str(transaction_raw).encode()).decode())
    except (binascii.Error, json.decoder.JSONDecodeError) as _error:
        raise ValueError("invalid Bytom transaction raw")
    if "type" not in decoded_tx_raw or not str(decoded_tx_raw["type"]).startswith("bytom"):
        raise ValueError("invalid Bytom transaction raw")
    submitted = submit_payment(
        guid=decoded_tx_raw["guid"],
        tx_raw=decoded_tx_raw["raw"],
        signatures=decoded_tx_raw["signatures"],
        network=decoded_tx_raw["network"]
    )
    return dict(
        fee=decoded_tx_raw["fee"],
        type=decoded_tx_raw["type"],
        tx_id=submitted["transaction_hash"],
        network=decoded_tx_raw["network"],
        date=str(datetime.datetime.utcnow())
    )


def spend_utxo_action(utxo):
    """
    Get spend UTXO action

    :param utxo: Bytom butxo id.
    :type utxo: str
    :returns: dict -- Bytom spend utxo action.

    >>> from shuttle.providers.bytom.utils import spend_utxo_action
    >>> spend_utxo_action(bytom_utxo_id)
    {...}
    """

    return dict(type=str("spend_utxo"), output_id=utxo)


def contract_arguments(amount, address):
    """
    Get contract arguments.

    :param amount: Bytom amount.
    :type amount: int
    :param address: Bytom address.
    :type address: str
    :returns: list -- Bytom contract arguments.

    >>> from shuttle.providers.bytom.utils import contract_arguments
    >>> contract_arguments(bytom_amount, bytom_address)
    [...]
    """

    return [dict(type=str("integer"), value=amount),
            dict(type=str("address"), value=address), dict(type=str("data"), value=str())]


def spend_wallet_action(amount, asset):
    """
    Get spend wallet action.

    :param amount: Bytom amount.
    :type amount: int
    :param asset: Bytom asset.
    :type asset: str
    :returns: dict -- Bytom spend wallet action.

    >>> from shuttle.providers.bytom.utils import spend_wallet_action
    >>> spend_wallet_action(bytom_amount, bytom_asset)
    {...}
    """

    return dict(amount=amount,
                asset=asset, type=str("spend_wallet"))


def spend_account_action(account, amount, asset):
    """
    Get spend account action.

    :param account: Bytom account.
    :type account: str
    :param amount: Bytom amount.
    :type amount: int
    :param asset: Bytom asset.
    :type asset: str
    :returns: dict -- Bytom spend account action.

    >>> from shuttle.providers.bytom.utils import spend_account_action
    >>> spend_account_action(bytom_account, bytom_amount, bytom_asset)
    {...}
    """

    return dict(account=account,
                amount=amount, asset=asset, type=str("spend_account"))


def control_program_action(amount, asset, control_program):
    """
    Get control program action.

    :param amount: Bytom amount.
    :type amount: int
    :param asset: Bytom asset.
    :type asset: str
    :param control_program: Bytom control program.
    :type control_program: str
    :returns: dict -- Bytom control program action.

    >>> from shuttle.providers.bytom.utils import control_program_action
    >>> control_program_action(bytom_amount, bytom_asset, bytom_control_program)
    {...}
    """

    return dict(amount=amount, asset=asset,
                control_program=control_program, type=str("control_program"))


def control_address_action(amount, asset, address):
    """
    Get control address action.

    :param amount: Bytom amount.
    :type amount: int
    :param asset: Bytom asset.
    :type asset: str
    :param address: Bytom address.
    :type address: str
    :returns: dict -- Bytom control address action.

    >>> from shuttle.providers.bytom.utils import control_address_action
    >>> control_address_action(bytom_amount, bytom_asset, bytom_address)
    {...}
    """

    return dict(amount=amount, asset=asset,
                address=address, type=str("control_address"))
