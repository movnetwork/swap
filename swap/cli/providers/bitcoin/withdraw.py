#!/usr/bin/env python
# coding=utf-8

import sys

from ....cli import click
from ....providers.bitcoin.transaction import WithdrawTransaction
from ....providers.config import bitcoin as config


@click.command("withdraw", options_metavar="[OPTIONS]",
               short_help="Select Bitcoin Withdraw transaction builder.")
@click.option("-a", "--address", type=str, required=True, help="Set Bitcoin recipient address.")
@click.option("-th", "--transaction-hash", type=str, required=True, help="Set Bitcoin funded transaction hash/id.")
@click.option("-n", "--network", type=str, default=config["network"],
              help="Set Bitcoin network.", show_default=True)
@click.option("-v", "--version", type=int, default=config["version"],
              help="Set Bitcoin transaction version.", show_default=True)
def withdraw(address: str, transaction_hash: str, network: str, version: int):
    try:
        click.echo(
            WithdrawTransaction(
                network=network, version=version
            ).build_transaction(
                address=address, transaction_hash=transaction_hash
            ).transaction_raw()
        )
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
