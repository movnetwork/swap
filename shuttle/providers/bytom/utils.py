#!/usr/bin/env python3

import ed25519


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


def spend_utxo_action(utxo):
    return dict(type=str("spend_utxo"), output_id=utxo)


def contract_arguments(amount, address):
    return [dict(type=str("integer"), value=amount),
            dict(type=str("address"), value=address), dict(type=str("data"), value=str())]


def spend_wallet_action(amount, asset_id):
    return dict(amount=amount, asset_id=asset_id, type=str("spend_wallet"))


def spend_account_action(account_id, amount, asset_id):
    return dict(account_id=account_id, amount=amount, asset_id=asset_id, type=str("spend_account"))


def control_program_action(amount, asset_id, control_program):
    return dict(amount=amount, asset_id=asset_id, control_program=control_program, type=str("control_program"))


def control_address_action(amount, asset_id, address):
    return dict(amount=amount, asset_id=asset_id, address=address, type=str("control_address"))
