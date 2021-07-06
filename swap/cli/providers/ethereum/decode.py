#!/usr/bin/env python
# coding=utf-8

import json
import sys

from ....cli import click
from ....providers.ethereum.utils import decode_transaction_raw


@click.command("decode", options_metavar="[OPTIONS]",
               short_help="Select Ethereum Transaction raw decoder.")
@click.option("-tr", "--transaction-raw", type=str, required=True, help="Set Ethereum transaction raw.")
@click.option("-i", "--indent", type=int, default=4, help="Set json indent.", show_default=True)
def decode(transaction_raw: str, indent: int):
    try:
        click.echo(
            json.dumps(
                decode_transaction_raw(
                    transaction_raw=transaction_raw
                )
            )
            if indent == 0 else
            json.dumps(
                decode_transaction_raw(
                    transaction_raw=transaction_raw
                ),
                indent=indent
            )
        )
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
