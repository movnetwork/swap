#!/usr/bin/env python
# coding=utf-8

import json


from shuttle.cli import click, success, warning, error
from shuttle.providers.bytom.utils import submit_transaction_raw


@click.command("submit", options_metavar="[OPTIONS]",
               short_help="Select bytom submit transaction raw.")
@click.option("-r", "--raw", type=str, required=True, help="Set bytom transaction raw.")
def submit(raw):
    """
    SHUTTLE BYTOM SUBMIT
    """
    try:
        click.echo(
            success(
                json.dumps(
                    submit_transaction_raw(tx_raw=raw),
                    indent=4
                )
            )
        )
    except Exception as exception:
        click.echo(error(str(exception)))
