#!/usr/bin/env python
# coding=utf-8

import json
import sys


from shuttle.cli import click
from shuttle.providers.bitcoin.utils import decode_transaction_raw


@click.command("decode", options_metavar="[OPTIONS]",
               short_help="Select Bitcoin transaction raw decoder.")
@click.option("-r", "--raw", type=str, required=True, help="Set Bitcoin transaction raw.")
def decode(raw):
    try:
        click.echo(
            json.dumps(
                decode_transaction_raw(transaction_raw=raw),
                indent=4
            )
        )
    except UnicodeDecodeError:
        click.echo(click.style("Error: {}")
                   .format("invalid Bitcoin transaction raw"), err=True)
        sys.exit()
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
