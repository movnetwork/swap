#!/usr/bin/env python
# coding=utf-8

import sys


from shuttle.cli import click
from shuttle.providers.bytom.transaction import ClaimTransaction
from shuttle.providers.bytom.wallet import Wallet


@click.command("claim", options_metavar="[OPTIONS]",
               short_help="Select Bytom claim transaction builder.")
@click.option("-t", "--transaction", type=str, required=True, help="Set Bytom fund transaction id.")
@click.option("-rg", "--recipient-guid", type=str, required=True, help="Set Bytom recipient GUID.")
@click.option("-a", "--amount", type=int, required=True, help="Set Bytom amount to claim.")
@click.option("-as", "--asset", type=str, required=True, help="Set Bytom asset id.")
@click.option("-n", "--network", type=str, default="solonet", help="Set Bytom network.")
def claim(transaction, recipient_guid, amount, asset,  network):
    try:
        click.echo(
            ClaimTransaction(network=network).build_transaction(
                transaction_id=transaction,
                wallet=Wallet(network=network).from_guid(guid=recipient_guid),
                amount=int(amount),
                asset=asset
            ).unsigned_raw()
        )
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
