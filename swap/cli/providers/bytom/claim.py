#!/usr/bin/env python
# coding=utf-8

import sys

from ....cli import click
from ....providers.bytom.transaction import ClaimTransaction
from ....providers.config import bytom as config


@click.command("claim", options_metavar="[OPTIONS]",
               short_help="Select Bytom Claim transaction builder.")
@click.option("-a", "--address", type=str, required=True, help="Set Bytom recipient address.")
@click.option("-ti", "--transaction-id", type=str, required=True, help="Set Bytom funded transaction id/hash.")
@click.option("-am", "--amount", type=int, required=True, help="Set Bytom amount (NEU).")
@click.option("-as", "--asset", type=str, default=config["asset"],
              help="Set Bytom asset id.", show_default=True)
@click.option("-n", "--network", type=str, default=config["network"],
              help="Set Bitcoin network.", show_default=True)
def claim(address: str, transaction_id: str, amount: int, asset: str, network: str):
    try:
        click.echo(
            ClaimTransaction(
                network=network
            ).build_transaction(
                address=address,
                transaction_id=transaction_id,
                amount=int(amount),
                asset=asset
            ).transaction_raw()
        )
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
