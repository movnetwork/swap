#!/usr/bin/env python
# coding=utf-8

import sys

from ....cli import click
from ....providers.bytom.utils import submit_transaction_raw


@click.command("submit", options_metavar="[OPTIONS]",
               short_help="Select Bytom transaction raw submitter.")
@click.option("-r", "--raw", type=str, required=True, help="Set signed Bytom transaction raw.")
def submit(raw):
    try:
        click.echo(
            submit_transaction_raw(transaction_raw=raw)["transaction_id"]
        )
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
