#!/usr/bin/env python
# coding=utf-8

import sys

from ....cli import click
from ....providers.vapor.transaction import WithdrawTransaction
from ....providers.config import vapor as config


@click.command("withdraw", options_metavar="[OPTIONS]",
               short_help="Select Vapor Withdraw transaction builder.")
@click.option("-a", "--address", type=str, required=True, help="Set Vapor recipient address.")
@click.option("-th", "--transaction-hash", type=str, required=True, help="Set Vapor funded transaction hash/id.")
@click.option("-as", "--asset", type=str, default=config["asset"],
              help="Set Vapor asset id.", show_default=True)
@click.option("-n", "--network", type=str, default=config["network"],
              help="Set Vapor network.", show_default=True)
def withdraw(address: str, transaction_hash: str, asset: str, network: str):
    try:
        click.echo(
            WithdrawTransaction(
                network=network
            ).build_transaction(
                address=address, transaction_hash=transaction_hash, asset=asset
            ).transaction_raw()
        )
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
