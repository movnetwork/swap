#!/usr/bin/env python
# coding=utf-8

import sys

from shuttle.cli import click
from shuttle.providers.bytom.utils import submit_transaction_raw


@click.command("submit", options_metavar="[OPTIONS]",
               short_help="Select Bytom transaction raw submitter.")
@click.option("-r", "--raw", type=str, required=True, help="Set signed Bytom transaction raw.")
def submit(raw):
    try:
        click.echo(submit_transaction_raw(transaction_raw=raw)["tx_id"])
    except UnicodeDecodeError:
        click.echo(click.style("Error: {}")
                   .format("invalid Bytom signed transaction raw"), err=True)
        sys.exit()
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
