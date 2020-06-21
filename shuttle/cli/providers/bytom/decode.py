#!/usr/bin/env python
# coding=utf-8

import json
import sys


from shuttle.cli import click
from shuttle.providers.bytom.utils import decode_transaction_raw


@click.command("decode", options_metavar="[OPTIONS]",
               short_help="Select Bytom transaction raw decoder.")
@click.option("-r", "--raw", type=str, required=True, help="Set Bytom transaction raw.")
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
                   .format("invalid Bytom transaction raw"), err=True)
        sys.exit()
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
