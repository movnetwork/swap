#!/usr/bin/env python
# coding=utf-8

import sys


from shuttle.cli import click
from shuttle.providers.bytom.htlc import HTLC


@click.command("htlc", options_metavar="[OPTIONS]",
               short_help="Select Bitcoin Hash Time Lock Contract (HTLC) builder.")
@click.option("-sh", "--secret-hash", type=str, required=True, help="Set secret 256 hash.")
@click.option("-rp", "--recipient-public", type=str, required=True, help="Set Bitcoin recipient public key.")
@click.option("-sp", "--sender-public", type=str, required=True, help="Set Bitcoin sender public key.")
@click.option("-s", "--sequence", type=int, default=100, help="Set Bitcoin expiration block (sequence).")
def htlc(secret_hash, recipient_public, sender_public, sequence):
    try:
        click.echo(
            HTLC().init(
                secret_hash=secret_hash,
                recipient_public=recipient_public,
                sender_public=sender_public,
                sequence=sequence
            ).bytecode()
        )
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
