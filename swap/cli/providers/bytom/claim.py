#!/usr/bin/env python
# coding=utf-8

import sys

from ....cli import click
from ....providers.bytom.transaction import ClaimTransaction
from ....providers.bytom.wallet import Wallet


@click.command("claim", options_metavar="[OPTIONS]",
               short_help="Select Bytom claim transaction builder.")
@click.option("-t", "--transaction", type=str, required=True, help="Set Bytom fund transaction id.")
@click.option("-ad", "--address", type=str, required=True, help="Set Bytom recipient address.")
@click.option("-am", "--amount", type=int, required=True, help="Set Bytom amount to claim.")
@click.option("-as", "--asset", type=str, required=True, help="Set Bytom asset id.")
@click.option("-n", "--network", type=str, default="solonet", help="Set Bytom network.")
def claim(transaction, address, amount, asset,  network):
    try:
        click.echo(
            ClaimTransaction(network=network).build_transaction(
                transaction_id=transaction,
                address=address,
                amount=int(amount),
                asset=asset
            ).unsigned_raw()
        )
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
