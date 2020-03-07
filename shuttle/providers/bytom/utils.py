#!/usr/bin/env python3

from base64 import b64encode, b64decode

import ed25519
import json
import binascii
import datetime

from .rpc import get_transaction, decode_tx_raw, submit_payment


def sign(private_key_str, message_str):
    signing_key = ed25519.SigningKey(bytes.fromhex(private_key_str))
    # signature = signing_key.sign(message_str.encode(), encoding='hex')
    signature = signing_key.sign(bytes.fromhex(message_str), encoding='hex')
    return signature.decode()


def verify(public_key_str, signature_str, message_str):
    result = False
    verifying_key = ed25519.VerifyingKey(public_key_str.encode(), encoding='hex')
    try:
        verifying_key.verify(signature_str.encode(), bytes.fromhex(message_str), encoding='hex')
        result = True
    except ed25519.BadSignatureError:
        result = False
    return result


def find_contract_utxo_id(tx_id, network):
    """
    Find smart contract UTXO id.

    :param tx_id: bytom transaction id or hash.
    :type tx_id: str
    :param network: bytom network.
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


def decode_transaction_raw(tx_raw):
    """
    Decode bytom transaction raw.

    :param tx_raw: bytom transaction raw.
    :type tx_raw: str
    :returns: dict -- decoded bytom transaction.

    >>> from shuttle.providers.bytom.utils import decode_transaction_raw
    >>> decode_transaction_raw(transaction_raw)
    {...}
    """

    tx_raw = str(tx_raw + "=" * (-len(tx_raw) % 4))
    try:
        # Decoding transaction raw.
        decoded_tx_raw = json.loads(b64decode(str(tx_raw).encode()).decode())
    except (binascii.Error, json.decoder.JSONDecodeError) as _error:
        raise ValueError("invalid bytom transaction raw")
    if "type" not in decoded_tx_raw and not str(decoded_tx_raw["type"]).startswith("bytom"):
        raise ValueError("invalid bytom transaction raw")
    return dict(
        fee=decoded_tx_raw["fee"],
        guid=decoded_tx_raw["guid"],
        type=decoded_tx_raw["type"],
        tx=decode_tx_raw(tx_raw=decoded_tx_raw["raw"]),
        unsigned=decoded_tx_raw["unsigned"],
        signatures=decoded_tx_raw["signatures"],
        network=decoded_tx_raw["network"]
    )


def submit_transaction_raw(tx_raw):
    """
    Submit transaction raw to Bytom blockchain.

    :param tx_raw: bytom transaction raw.
    :type tx_raw: str
    :returns: dict -- bytom transaction id, fee, type and date.

    >>> from shuttle.providers.bytom.utils import submit_transaction_raw
    >>> submit_transaction_raw(transaction_raw)
    {...}
    """

    tx_raw = str(tx_raw + "=" * (-len(tx_raw) % 4))
    try:
        # Decoding transaction raw.
        decoded_tx_raw = json.loads(b64decode(str(tx_raw).encode()).decode())
    except (binascii.Error, json.decoder.JSONDecodeError) as _error:
        raise ValueError("invalid bytom transaction raw")
    if "type" not in decoded_tx_raw and not str(decoded_tx_raw["type"]).startswith("bytom"):
        raise ValueError("invalid bytom transaction raw")
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

    :param utxo: bytom butxo id.
    :type utxo: str
    :returns: dict -- bytom spend utxo action.

    >>> from shuttle.providers.bytom.utils import spend_utxo_action
    >>> spend_utxo_action(bytom_utxo_id)
    {...}
    """

    return dict(type=str("spend_utxo"), output_id=utxo)


def contract_arguments(amount, address):
    """
    Get contract arguments.

    :param amount: bytom amount.
    :type amount: int
    :param address: bytom address.
    :type address: str
    :returns: list -- bytom contract arguments.

    >>> from shuttle.providers.bytom.utils import contract_arguments
    >>> contract_arguments(bytom_amount, bytom_address)
    [...]
    """

    return [dict(type=str("integer"), value=amount),
            dict(type=str("address"), value=address), dict(type=str("data"), value=str())]


def spend_wallet_action(amount, asset):
    """
    Get spend wallet action.

    :param amount: bytom amount.
    :type amount: int
    :param asset: bytom asset.
    :type asset: str
    :returns: dict -- bytom spend wallet action.

    >>> from shuttle.providers.bytom.utils import spend_wallet_action
    >>> spend_wallet_action(bytom_amount, bytom_asset)
    {...}
    """

    return dict(amount=amount,
                asset=asset, type=str("spend_wallet"))


def spend_account_action(account, amount, asset):
    """
    Get spend account action.

    :param account: bytom account.
    :type account: str
    :param amount: bytom amount.
    :type amount: int
    :param asset: bytom asset.
    :type asset: str
    :returns: dict -- bytom spend account action.

    >>> from shuttle.providers.bytom.utils import spend_account_action
    >>> spend_account_action(bytom_account, bytom_amount, bytom_asset)
    {...}
    """

    return dict(account=account,
                amount=amount, asset=asset, type=str("spend_account"))


def control_program_action(amount, asset, control_program):
    """
    Get control program action.

    :param amount: bytom amount.
    :type amount: int
    :param asset: bytom asset.
    :type asset: str
    :param control_program: bytom control program.
    :type control_program: str
    :returns: dict -- bytom control program action.

    >>> from shuttle.providers.bytom.utils import control_program_action
    >>> control_program_action(bytom_amount, bytom_asset, bytom_control_program)
    {...}
    """

    return dict(amount=amount, asset=asset,
                control_program=control_program, type=str("control_program"))


def control_address_action(amount, asset, address):
    """
    Get control address action.

    :param amount: bytom amount.
    :type amount: int
    :param asset: bytom asset.
    :type asset: str
    :param address: bytom address.
    :type address: str
    :returns: dict -- bytom control address action.

    >>> from shuttle.providers.bytom.utils import control_address_action
    >>> control_address_action(bytom_amount, bytom_asset, bytom_address)
    {...}
    """

    return dict(amount=amount, asset=asset,
                address=address, type=str("control_address"))
