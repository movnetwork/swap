#!/usr/bin/env python
# coding=utf-8

import sys

from ....cli import click
from ....providers.bytom.transaction import FundTransaction
from ....providers.bytom.htlc import HTLC
from ....providers.config import bytom

# Bytom config
config = bytom()


@click.command("fund", options_metavar="[OPTIONS]",
               short_help="Select Bytom Fund transaction builder.")
@click.option("-a", "--address", type=str, required=True, help="Set Bytom sender address.")
@click.option("-b", "--bytecode", type=str, required=True, help="Set Bytom Hash Time Lock Contract (HTLC) bytecode.")
@click.option("-am", "--amount", type=int, required=True, help="Set Bytom amount (NEU).")
@click.option("-as", "--asset", type=str, default=config["asset"],
              help="Set Bytom asset id.", show_default=True)
@click.option("-n", "--network", type=str, default=config["network"],
              help="Set Bitcoin network.", show_default=True)
def fund(address, bytecode, amount, asset, network):
    try:
        click.echo(
            FundTransaction(network=network).build_transaction(
                address=address,
                htlc=HTLC(network=network).from_bytecode(bytecode=bytecode),
                amount=int(amount),
                asset=asset
            ).transaction_raw()
        )
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
