#!/usr/bin/env python
# coding=utf-8

import sys

from ....cli import click
from ....providers.bitcoin.transaction import FundTransaction
from ....providers.bitcoin.htlc import HTLC
from ....providers.config import bitcoin

# Bitcoin config
config = bitcoin()


@click.command("fund", options_metavar="[OPTIONS]",
               short_help="Select Bitcoin Fund transaction builder.")
@click.option("-a", "--address", type=str, required=True, help="Set Bitcoin sender address.")
@click.option("-am", "--amount", type=int, required=True, help="Set Bitcoin amount (SATOSHI).")
@click.option("-b", "--bytecode", type=str, required=True, help="Set Bitcoin Hash Time Lock Contract (HTLC) bytecode.")
@click.option("-v", "--version", type=int, default=config["version"],
              help="Set Bitcoin transaction version.", show_default=True)
@click.option("-n", "--network", type=str, default=config["network"],
              help="Set Bitcoin network.", show_default=True)
def fund(address, amount, bytecode, version, network):
    try:
        click.echo(
            FundTransaction(version=version, network=network).build_transaction(
                address=address,
                htlc=HTLC(network=network).from_bytecode(bytecode=bytecode),
                amount=int(amount)
            ).transaction_raw()
        )
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
