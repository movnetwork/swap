#!/usr/bin/env python
# coding=utf-8

import json


from shuttle.cli import click, success, warning, error
from shuttle.providers.bitcoin.utils import decode_transaction_raw


@click.command("decode", options_metavar="[OPTIONS]",
               short_help="Select bitcoin transaction raw decoder.")
@click.option("-r", "--raw", type=str, required=True, help="Set bitcoin transaction raw.")
def decode(raw):
    """
    SHUTTLE BITCOIN DECODE
    """
    try:
        click.echo(
            success(
                json.dumps(
                    decode_transaction_raw(tx_raw=raw),
                    indent=4
                )
            )
        )
    except Exception as exception:
        click.echo(error(str(exception)))
