#!/usr/bin/env python
# coding=utf-8

import json
import sys

from ....cli import click
from ....providers.bitcoin.utils import decode_transaction_raw


@click.command("decode", options_metavar="[OPTIONS]",
               short_help="Select Bitcoin transaction raw decoder.")
@click.option("-r", "--raw", type=str, required=True, help="Set Bitcoin transaction raw.")
@click.option("-i", "--indent", type=int, default=4, help="Set json indent.", show_default=True)
@click.option("-o", "--offline", type=bool, default=True,
              help="Set Offline decode transaction raw.", show_default=True)
def decode(raw, indent, offline):
    try:
        click.echo(
            json.dumps(
                decode_transaction_raw(transaction_raw=raw, offline=offline)
            )
            if indent == 0 else
            json.dumps(
                decode_transaction_raw(transaction_raw=raw, offline=offline),
                indent=indent
            )
        )
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
