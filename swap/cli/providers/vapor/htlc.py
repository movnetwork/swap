#!/usr/bin/env python
# coding=utf-8

import sys

from ....cli import click
from ....providers.vapor.htlc import HTLC
from ....providers.config import vapor as config


@click.command("htlc", options_metavar="[OPTIONS]",
               short_help="Select Vapor Hash Time Lock Contract (HTLC) builder.")
@click.option("-sh", "--secret-hash", type=str, required=True, help="Set secret 256 hash.")
@click.option("-rpk", "--recipient-public-key", type=str, required=True, help="Set Vapor recipient public key.")
@click.option("-spk", "--sender-public-key", type=str, required=True, help="Set Vapor sender public key.")
@click.option("-s", "--sequence", type=int, default=config["sequence"],
              help="Set Vapor sequence/expiration block.", show_default=True)
@click.option("-n", "--network", type=str, default=config["network"],
              help="Set Vapor network.", show_default=True)
def htlc(secret_hash: str, recipient_public_key: str, sender_public_key: str, sequence: int, network: str):
    try:
        _htlc: HTLC = HTLC(
            network=network
        ).build_htlc(
            secret_hash=secret_hash,
            recipient_public_key=recipient_public_key,
            sender_public_key=sender_public_key,
            sequence=sequence
        )
        click.echo(dict(
            bytecode=_htlc.bytecode(), address=_htlc.address()
        ))
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
