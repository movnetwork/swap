#!/usr/bin/env python
# coding=utf-8

import sys

from ....cli import click
from ....providers.bytom.transaction import RefundTransaction
from ....providers.config import bytom as config


@click.command("refund", options_metavar="[OPTIONS]",
               short_help="Select Bytom Refund transaction builder.")
@click.option("-a", "--address", type=str, required=True, help="Set Bytom sender address.")
@click.option("-th", "--transaction-hash", type=str, required=True, help="Set Bytom funded transaction id/hash.")
@click.option("-as", "--asset", type=str, default=config["asset"],
              help="Set Bytom asset id.", show_default=True)
@click.option("-n", "--network", type=str, default=config["network"],
              help="Set Bytom network.", show_default=True)
def refund(address: str, transaction_hash: str, asset: str, network: str):
    try:
        click.echo(
            RefundTransaction(
                network=network
            ).build_transaction(
                address=address, transaction_hash=transaction_hash, asset=asset
            ).transaction_raw()
        )
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
