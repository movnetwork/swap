#!/usr/bin/env python
# coding=utf-8

import sys


from shuttle.cli import click
from shuttle.providers.bytom.transaction import RefundTransaction
from shuttle.providers.bytom.wallet import Wallet


@click.command("refund", options_metavar="[OPTIONS]",
               short_help="Select Bytom refund transaction builder.")
@click.option("-t", "--transaction", type=str, required=True, help="Set Bytom fund transaction id.")
@click.option("-sg", "--sender-guid", type=str, required=True, help="Set Bytom sender GUID.")
@click.option("-a", "--amount", type=int, required=True, help="Set Bytom amount to refund.")
@click.option("-as", "--asset", type=str, required=True, help="Set Bytom asset id.")
@click.option("-n", "--network", type=str, default="solonet", help="Set Bytom network.")
def refund(transaction, sender_guid, amount, asset,  network):
    try:
        click.echo(
            RefundTransaction(network=network).build_transaction(
                transaction_id=transaction,
                wallet=Wallet(network=network).from_guid(guid=sender_guid),
                amount=int(amount),
                asset=asset
            ).unsigned_raw()
        )
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
