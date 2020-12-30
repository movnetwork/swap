#!/usr/bin/env python
# coding=utf-8

import sys

from ....cli import click
from ....providers.bytom.transaction import RefundTransaction
from ....providers.bytom.utils import amount_unit_converter
from ....providers.config import bytom as config


@click.command("refund", options_metavar="[OPTIONS]",
               short_help="Select Bytom Refund transaction builder.")
@click.option("-a", "--address", type=str, required=True, help="Set Bytom sender address.")
@click.option("-ti", "--transaction-id", type=str, required=True, help="Set Bytom funded transaction id/hash.")
@click.option("-am", "--amount", type=float, default=0,
              help="Set Bytom refund amount.  [default: None]", show_default=False)
@click.option("-ma", "--max-amount", type=bool, default=True,
              help="Set Bytom refund max amount.", show_default=True)
@click.option("-u", "--unit", type=str, default=config["unit"],
              help="Set Bytom refund amount unit.", show_default=True)
@click.option("-as", "--asset", type=str, default=config["asset"],
              help="Set Bytom asset id.", show_default=True)
@click.option("-n", "--network", type=str, default=config["network"],
              help="Set Bytom network.", show_default=True)
def refund(address: str, transaction_id: str, amount: int, max_amount: bool, unit: str, asset: str, network: str):
    try:
        click.echo(
            RefundTransaction(
                network=network
            ).build_transaction(
                address=address,
                transaction_id=transaction_id,
                amount=(int(amount) if unit == "NEU" else amount_unit_converter(
                    amount=amount, unit_from=f"{unit}2NEU"
                )),
                max_amount=max_amount,
                asset=asset
            ).transaction_raw()
        )
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
