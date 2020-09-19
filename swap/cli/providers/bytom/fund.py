#!/usr/bin/env python
# coding=utf-8

import sys

from ....cli import click
from ....providers.bytom.transaction import FundTransaction
from ....providers.bytom.htlc import HTLC


@click.command("fund", options_metavar="[OPTIONS]",
               short_help="Select Bytom unsigned transaction builder.")
@click.option("-ad", "--address", type=str, required=True, help="Set Bytom sender address.")
@click.option("-am", "--amount", type=int, required=True, help="Set Bytom amount to fund on HTLC.")
@click.option("-as", "--asset", type=str, required=True, help="Set Bytom asset id.")
@click.option("-b", "--bytecode", type=str, required=True, help="Set Bytom HTLC bytecode.")
@click.option("-n", "--network", type=str, default="solonet", help="Set Bytom network.")
def fund(address, amount, asset, bytecode, network):
    try:
        click.echo(
            FundTransaction(network=network).build_transaction(
                address=address,
                htlc=HTLC(network=network).from_bytecode(bytecode=bytecode),
                amount=int(amount),
                asset=asset
            ).unsigned_raw()
        )
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
