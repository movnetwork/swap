#!/usr/bin/env python
# coding=utf-8

import json
import sys

from ....cli import click
from ....providers.xinfin.htlc import HTLC
from ....providers.config import xinfin as config


@click.command("htlc", options_metavar="[OPTIONS]",
               short_help="Select XinFin Hash Time Lock Contract (HTLC) builder.")
@click.option("-ca", "--contract-address", type=str, default=None,
              help="Set XinFin HTLC contact address.  [default: None]")
@click.option("-n", "--network", type=str, default=config["network"],
              help="Set XinFin network.", show_default=True)
@click.option("-i", "--indent", type=int, default=4, help="Set json indent.", show_default=True)
def htlc(contract_address: str, network: str, indent: int):
    try:
        _htlc: HTLC = HTLC(
            contract_address=contract_address, network=network
        )
        click.echo(json.dumps(dict(
            abi=_htlc.abi(), bytecode=_htlc.bytecode(), contract_address=_htlc.contract_address()
        ), indent=indent))
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
