#!/usr/bin/env python
# coding=utf-8

import sys

from ....cli import click
from ....providers.bytom.htlc import HTLC
from ....providers.config import bytom

# Bytom config
config = bytom()


@click.command("htlc", options_metavar="[OPTIONS]",
               short_help="Select Bytom Hash Time Lock Contract (HTLC) builder.")
@click.option("-sh", "--secret-hash", type=str, required=True, help="Set secret 256 hash.")
@click.option("-rp", "--recipient-public", type=str, required=True, help="Set Bytom recipient public key.")
@click.option("-sp", "--sender-public", type=str, required=True, help="Set Bytom sender public key.")
@click.option("-sq", "--sequence", type=int, default=config["sequence"],
              help="Set Bytom sequence/expiration block.", show_default=True)
@click.option("-n", "--network", type=str, default=config["network"],
              help="Set Bytom network.", show_default=True)
def htlc(secret_hash, recipient_public, sender_public, sequence, network):
    try:
        click.echo(
            HTLC(network=network).build_htlc(
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
