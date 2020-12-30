#!/usr/bin/env python
# coding=utf-8

import json
import sys

from ....cli import click
from ....providers.bytom.htlc import HTLC
from ....providers.config import bytom as config


@click.command("htlc", options_metavar="[OPTIONS]",
               short_help="Select Bytom Hash Time Lock Contract (HTLC) builder.")
@click.option("-sh", "--secret-hash", type=str, required=True, help="Set secret 256 hash.")
@click.option("-rpk", "--recipient-public-key", type=str, required=True, help="Set Bytom recipient public key.")
@click.option("-spk", "--sender-public-key", type=str, required=True, help="Set Bytom sender public key.")
@click.option("-s", "--sequence", type=int, default=config["sequence"],
              help="Set Bytom sequence/expiration block.", show_default=True)
@click.option("-n", "--network", type=str, default=config["network"],
              help="Set Bytom network.", show_default=True)
@click.option("-i", "--indent", type=int, default=4, help="Set json indent.", show_default=True)
def htlc(secret_hash: str, recipient_public_key: str, sender_public_key: str, sequence: int, network: str, indent: int):
    try:
        _htlc: HTLC = HTLC(
            network=network
        ).build_htlc(
            secret_hash=secret_hash,
            recipient_public_key=recipient_public_key,
            sender_public_key=sender_public_key,
            sequence=sequence
        )
        click.echo(json.dumps(dict(
            bytecode=_htlc.bytecode(), address=_htlc.address()
        ), indent=indent))
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
