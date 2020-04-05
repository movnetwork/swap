#!/usr/bin/env python
# coding=utf-8

import json


from shuttle.cli import click
from shuttle.providers.bitcoin.utils import decode_transaction_raw


@click.command("decode", options_metavar="[OPTIONS]",
               short_help="Select Bitcoin transaction raw decoder.")
@click.option("-r", "--raw", type=str, required=True, help="Set Bitcoin transaction raw.")
def decode(raw):
    try:
        click.echo(
            json.dumps(
                decode_transaction_raw(tx_raw=raw),
                indent=4
            )
        )
    except Exception as exception:
        click.echo(str(exception))
