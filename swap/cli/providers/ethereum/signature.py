#!/usr/bin/env python
# coding=utf-8

from typing import Optional
from base64 import b64decode

import json
import sys

from ....cli import click
from ....providers.ethereum.solver import (
    FundSolver, WithdrawSolver, RefundSolver
)
from ....providers.ethereum.signature import (
    FundSignature, WithdrawSignature, RefundSignature
)
from ....providers.ethereum.utils import is_transaction_raw
from ....exceptions import TransactionRawError
from ....utils import clean_transaction_raw


@click.command("sign", options_metavar="[OPTIONS]",
               short_help="Select Ethereum Transaction raw signer.")
@click.option("-xpk", "--xprivate-key", type=str, required=True, help="Set Ethereum root xprivate key.")
@click.option("-tr", "--transaction-raw", type=str, required=True, help="Set Ethereum unsigned transaction raw.")
@click.option("-ac", "--account", type=int, default=0,
              help="Set Ethereum derivation from account.", show_default=True)
@click.option("-ch", "--change", type=bool, default=False,
              help="Set Ethereum derivation from change.", show_default=True)
@click.option("-ad", "--address", type=int, default=0,
              help="Set Ethereum derivation from address.", show_default=True)
@click.option("-p", "--path", type=str, default=None,
              help="Set Ethereum derivation from path.  [default: None]", show_default=True)
def sign(xprivate_key: str, transaction_raw: str, account: int, change: bool, address: int, path: Optional[str]):

    try:
        if not is_transaction_raw(transaction_raw=transaction_raw):
            raise TransactionRawError("Invalid Ethereum unsigned transaction raw.")

        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())
        
        if loaded_transaction_raw["type"] == "ethereum_fund_unsigned":
            # Fund HTLC solver
            fund_solver: FundSolver = FundSolver(
                xprivate_key=xprivate_key,
                account=account, change=change, address=address,
                path=path
            )
            # Fund signature
            fund_signature: FundSignature = FundSignature(
                network=loaded_transaction_raw["network"], erc20=loaded_transaction_raw["erc20"]
            )
            fund_signature.sign(
                transaction_raw=transaction_raw, solver=fund_solver
            )
            click.echo(fund_signature.transaction_raw())

        elif loaded_transaction_raw["type"] == "ethereum_withdraw_unsigned":

            # Withdraw HTLC solver
            withdraw_solver: WithdrawSolver = WithdrawSolver(
                xprivate_key=xprivate_key,
                account=account, change=change, address=address,
                path=path
            )
            # Withdraw signature
            withdraw_signature: WithdrawSignature = WithdrawSignature(
                network=loaded_transaction_raw["network"], erc20=loaded_transaction_raw["erc20"]
            )
            withdraw_signature.sign(
                transaction_raw=transaction_raw, solver=withdraw_solver
            )
            click.echo(withdraw_signature.transaction_raw())

        elif loaded_transaction_raw["type"] == "ethereum_refund_unsigned":

            # Refunding HTLC solver
            refund_solver: RefundSolver = RefundSolver(
                xprivate_key=xprivate_key,
                account=account, change=change, address=address,
                path=path
            )
            # Refund signature
            refund_signature: RefundSignature = RefundSignature(
                network=loaded_transaction_raw["network"], erc20=loaded_transaction_raw["erc20"]
            )
            refund_signature.sign(
                transaction_raw=transaction_raw, solver=refund_solver
            )
            click.echo(refund_signature.transaction_raw())
        else:
            click.echo(click.style("Error: {}")
                       .format("Unknown Ethereum unsigned transaction raw type."), err=True)
            sys.exit()
    except Exception as exception:
        click.echo(click.style("Error: {}").format(str(exception)), err=True)
        sys.exit()
