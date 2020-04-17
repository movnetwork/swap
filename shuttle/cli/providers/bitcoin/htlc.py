#!/usr/bin/env python
# coding=utf-8

import sys


from shuttle.cli import click
from shuttle.providers.bitcoin.htlc import HTLC


@click.command("htlc", options_metavar="[OPTIONS]",
               short_help="Select Bitcoin Hash Time Lock Contract (HTLC) builder.")
@click.option("-sh", "--secret-hash", type=str, required=True, help="Set secret 256 hash.")
@click.option("-ra", "--recipient-address", type=str, required=True, help="Set Bitcoin recipient address.")
@click.option("-sa", "--sender-address", type=str, required=True, help="Set Bitcoin sender address.")
@click.option("-s", "--sequence", type=int, default=100, help="Set Bitcoin expiration block (sequence).")
@click.option("-n", "--network", type=str, default="testnet", help="Set Bitcoin network.")
def htlc(secret_hash, recipient_address, sender_address, sequence, network):
    try:
        click.echo(
            HTLC(network=network).init(
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
