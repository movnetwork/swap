#!/usr/bin/env python
# coding=utf-8

import json
import sys

from ....cli import click
from ....providers.bytom.utils import decode_transaction_raw


@click.command("decode", options_metavar="[OPTIONS]",
               short_help="Select Bytom transaction raw decoder.")
@click.option("-r", "--raw", type=str, required=True, help="Set Bytom transaction raw.")
@click.option("-i", "--indent", type=int, default=4, help="Set json indent.", show_default=True)
def decode(raw, indent):
    try:
        click.echo(
            json.dumps(
                decode_transaction_raw(transaction_raw=raw)
            )
            if indent == 0 else
            json.dumps(
                decode_transaction_raw(transaction_raw=raw),
                indent=indent
            )
        )
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
