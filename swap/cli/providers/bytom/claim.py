#!/usr/bin/env python
# coding=utf-8

import sys

from ....cli import click
from ....providers.bytom.transaction import ClaimTransaction
from ....providers.bytom.utils import amount_unit_converter
from ....providers.config import bytom as config


@click.command("claim", options_metavar="[OPTIONS]",
               short_help="Select Bytom Claim transaction builder.")
@click.option("-a", "--address", type=str, required=True, help="Set Bytom recipient address.")
@click.option("-ti", "--transaction-id", type=str, required=True, help="Set Bytom funded transaction id/hash.")
@click.option("-am", "--amount", type=int, default=None,
              help="Set Bytom withdraw amount.  [default: None]", show_default=True)
@click.option("-ma", "--max-amount", type=bool, default=True,
              help="Set Bytom withdraw max amount.", show_default=True)
@click.option("-u", "--unit", type=str, default=config["unit"],
              help="Set Bytom withdraw amount unit.", show_default=True)
@click.option("-as", "--asset", type=str, default=config["asset"],
              help="Set Bytom asset id.", show_default=True)
@click.option("-n", "--network", type=str, default=config["network"],
              help="Set Bytom network.", show_default=True)
def claim(address: str, transaction_id: str, amount: int, max_amount: bool, unit: str, asset: str, network: str):
    try:
        click.echo(
            ClaimTransaction(
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
