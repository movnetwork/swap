#!/usr/bin/env python
# coding=utf-8

import json
import sys

from ....cli import click
from ....providers.xinfin.htlc import HTLC
from ....providers.config import xinfin as config


@click.command("htlc", options_metavar="[OPTIONS]",
               short_help="Select XinFin Hash Time Lock Contract (HTLC) builder.")
@click.option("-th", "--transaction-hash", type=str, required=True, help="Set XinFin HTLC transaction hash.")
@click.option("-n", "--network", type=str, default=config["network"],
              help="Set XinFin network.", show_default=True)
@click.option("-i", "--indent", type=int, default=4, help="Set json indent.", show_default=True)
def htlc(transaction_hash: str, network: str, indent: int):
    try:
        _htlc: HTLC = HTLC(
            transaction_hash=transaction_hash, network=network
        )
        click.echo(json.dumps(dict(
            bytecode=_htlc.bytecode(), contract_address=_htlc.contract_address()
        ), indent=indent))
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
