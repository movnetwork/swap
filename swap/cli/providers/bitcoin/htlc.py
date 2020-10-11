#!/usr/bin/env python
# coding=utf-8

import sys

from ....cli import click
from ....providers.bitcoin.htlc import HTLC
from ....providers.config import bitcoin

# Bitcoin config
config = bitcoin()


@click.command("htlc", options_metavar="[OPTIONS]",
               short_help="Select Bitcoin Hash Time Lock Contract (HTLC) builder.")
@click.option("-sh", "--secret-hash", type=str, required=True, help="Set secret 256 hash.")
@click.option("-ra", "--recipient-address", type=str, required=True, help="Set Bitcoin recipient address.")
@click.option("-sa", "--sender-address", type=str, required=True, help="Set Bitcoin sender address.")
@click.option("-s", "--sequence", type=int, default=config["sequence"],
              help="Set Bitcoin sequence/expiration block.", show_default=True)
@click.option("-n", "--network", type=str, default=config["network"],
              help="Set Bitcoin network.", show_default=True)
def htlc(secret_hash: str, recipient_address: str, sender_address: str, sequence: int, network: str):
    try:
        click.echo(
            HTLC(
                network=network
            ).build_htlc(
                secret_hash=secret_hash,
                recipient_address=recipient_address,
                sender_address=sender_address,
                sequence=sequence
            ).bytecode()
        )
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
