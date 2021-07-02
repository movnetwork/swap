#!/usr/bin/env python
# coding=utf-8

from base64 import b64decode

import json
import sys

from ....cli import click
from ....providers.vapor.solver import (
    FundSolver, WithdrawSolver, RefundSolver
)
from ....providers.vapor.signature import (
    FundSignature, WithdrawSignature, RefundSignature
)
from ....providers.vapor.utils import is_transaction_raw
from ....exceptions import TransactionRawError
from ....utils import clean_transaction_raw


@click.command("sign", options_metavar="[OPTIONS]",
               short_help="Select Vapor Transaction raw signer.")
@click.option("-xpk", "--xprivate-key", type=str, required=True, help="Set Vapor xprivate key.")
@click.option("-tr", "--transaction-raw", type=str, required=True, help="Set Vapor unsigned transaction raw.")
@click.option("-b", "--bytecode", type=str, default=None,
              help="Set Vapor witness HTLC bytecode.  [default: None]", show_default=True)
@click.option("-sk", "--secret-key", type=str, default=None,
              help="Set secret key.  [default: None]", show_default=True)
@click.option("-ac", "--account", type=int, default=1,
              help="Set Vapor derivation from account.", show_default=True)
@click.option("-ch", "--change", type=bool, default=False,
              help="Set Vapor derivation from change.", show_default=True)
@click.option("-ad", "--address", type=int, default=1,
              help="Set Vapor derivation from address.", show_default=True)
@click.option("-p", "--path", type=str, default=None,
              help="Set Vapor derivation from path.  [default: None]", show_default=True)
@click.option("-i", "--indexes", type=list, default=None,
              help="Set Vapor derivation from indexes.  [default: None]", show_default=True)
def sign(xprivate_key: str, transaction_raw: str, bytecode: str,
         secret_key: str, account: int, change: bool, address: int, path: str, indexes: list):
    try:
        if not is_transaction_raw(transaction_raw=transaction_raw):
            raise TransactionRawError("Invalid Bitcoin unsigned transaction raw.")

        transaction_raw = clean_transaction_raw(transaction_raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())

        if loaded_transaction_raw["type"] == "vapor_fund_unsigned":
            # Fund HTLC solver
            fund_solver = FundSolver(
                xprivate_key=xprivate_key,
                account=account, change=change, address=address,
                path=path, indexes=indexes
            )
            # Fund signature
            fund_signature = FundSignature(
                network=loaded_transaction_raw["network"]
            )
            fund_signature.sign(
                transaction_raw=transaction_raw, solver=fund_solver
            )
            click.echo(fund_signature.transaction_raw())

        elif loaded_transaction_raw["type"] == "vapor_withdraw_unsigned":
            if secret_key is None:
                click.echo(click.style("Error: {}").format(
                    "Secret key is required for withdraw, use -sk or --secret-key \"Hello Meheret!\""
                ), err=True)
                sys.exit()
            if bytecode is None:
                click.echo(click.style("Error: {}").format(
                    "Witness bytecode is required for withdraw, use -b or --bytecode \"016...\""
                ), err=True)
                sys.exit()

            # Withdraw HTLC solver
            withdraw_solver = WithdrawSolver(
                xprivate_key=xprivate_key, secret_key=secret_key, bytecode=bytecode,
                account=account, change=change, address=address,
                path=path, indexes=indexes
            )
            # Withdraw signature
            withdraw_signature = WithdrawSignature(
                network=loaded_transaction_raw["network"]
            )
            withdraw_signature.sign(
                transaction_raw=transaction_raw, solver=withdraw_solver
            )
            click.echo(withdraw_signature.transaction_raw())

        elif loaded_transaction_raw["type"] == "vapor_refund_unsigned":
            if bytecode is None:
                click.echo(click.style("Error: {}").format(
                    "Witness bytecode is required for withdraw, use -b or --bytecode \"016...\""
                ), err=True)
                sys.exit()

            # Refunding HTLC solver
            refund_solver = RefundSolver(
                xprivate_key=xprivate_key, bytecode=bytecode,
                account=account, change=change, address=address,
                path=path, indexes=indexes
            )
            # Refund signature
            refund_signature = RefundSignature(
                network=loaded_transaction_raw["network"]
            )
            refund_signature.sign(
                transaction_raw=transaction_raw, solver=refund_solver
            )
            click.echo(refund_signature.transaction_raw())
        else:
            click.echo(click.style("Error: {}")
                       .format("Unknown Vapor unsigned transaction raw type."), err=True)
            sys.exit()
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
