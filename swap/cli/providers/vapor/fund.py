#!/usr/bin/env python
# coding=utf-8

import sys

from ....cli import click
from ....providers.vapor.transaction import FundTransaction
from ....providers.config import vapor as config


@click.command("fund", options_metavar="[OPTIONS]",
               short_help="Select Vapor Fund transaction builder.")
@click.option("-a", "--address", type=str, required=True, help="Set Vapor sender address.")
@click.option("-ha", "--htlc-address", type=str, required=True,
              help="Set Vapor Hash Time Lock Contract (HTLC) address.")
@click.option("-am", "--amount", type=int, required=True, help="Set Vapor amount (NEU).")
@click.option("-as", "--asset", type=str, default=config["asset"],
              help="Set Vapor asset id.", show_default=True)
@click.option("-n", "--network", type=str, default=config["network"],
              help="Set Bitcoin network.", show_default=True)
def fund(address: str, htlc_address: str, amount: int, asset: str, network: str):
    try:
        click.echo(
            FundTransaction(
                network=network
            ).build_transaction(
                address=address,
                htlc_address=htlc_address,
                amount=int(amount),
                asset=asset
            ).transaction_raw()
        )
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
