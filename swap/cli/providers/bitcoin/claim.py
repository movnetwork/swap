#!/usr/bin/env python
# coding=utf-8

import sys

from ....cli import click
from ....providers.bitcoin.transaction import ClaimTransaction
from ....providers.config import bitcoin

# Bitcoin config
config = bitcoin()


@click.command("claim", options_metavar="[OPTIONS]",
               short_help="Select Bitcoin Claim transaction builder.")
@click.option("-a", "--address", type=str, required=True, help="Set Bitcoin recipient address.")
@click.option("-t", "--transaction", type=str, required=True, help="Set Bitcoin funded transaction id.")
@click.option("-am", "--amount", type=int, required=True, help="Set Bitcoin amount (SATOSHI).")
@click.option("-v", "--version", type=int, default=config["version"],
              help="Set Bitcoin transaction version.", show_default=True)
@click.option("-n", "--network", type=str, default=config["network"],
              help="Set Bitcoin network.", show_default=True)
def claim(address, transaction, amount, version, network):
    try:
        click.echo(
            ClaimTransaction(version=version, network=network).build_transaction(
                address=address,
                transaction_id=transaction,
                amount=int(amount)
            ).transaction_raw()
        )
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
