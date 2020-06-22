#!/usr/bin/env python
# coding=utf-8

from base64 import b64decode

import json
import sys
import binascii

from shuttle.cli import click
from shuttle.providers.bitcoin.solver import (
    FundSolver, ClaimSolver, RefundSolver
)
from shuttle.providers.bitcoin.signature import (
    FundSignature, ClaimSignature, RefundSignature
)
from shuttle.providers.config import bitcoin

# Bitcoin config
bitcoin = bitcoin()
# Bitcoin version
VERSION = 2  # Default


@click.command("sign", options_metavar="[OPTIONS]",
               short_help="Select Bitcoin transaction raw signer.")
@click.option("-p", "--private", type=str, required=True, help="Set Bitcoin private key.")
@click.option("-r", "--raw", type=str, required=True, help="Set Bitcoin unsigned transaction raw.")
@click.option("-b", "--bytecode", type=str, default=None, help="Set Bitcoin witness HTLC bytecode.")
@click.option("-s", "--secret", type=str, default=None, help="Set secret key.")
@click.option("-sq", "--sequence", type=int, default=bitcoin["sequence"],
              help="Set Bitcoin sequence/expiration block.")
@click.option("-v", "--version", type=int, default=VERSION,
              help="Set Bitcoin transaction version.", show_default=True)
def sign(private, raw, bytecode, secret, sequence, version):
    if len(private) != 64:
        click.echo(click.style("Error: {}")
                   .format("invalid Bitcoin private key"), err=True)
        sys.exit()

    # Cleaning unsigned raw
    unsigned_raw = str(raw + "=" * (-len(raw) % 4))
    try:
        transaction = json.loads(b64decode(unsigned_raw.encode()).decode())
    except (binascii.Error, json.decoder.JSONDecodeError) as exception:
        click.echo(click.style("Error: {}")
                   .format("invalid Bitcoin unsigned transaction raw"), err=True)
        sys.exit()
    if "type" not in transaction or "network" not in transaction:
        click.echo(click.style("Warning: {}", fg="yellow")
                   .format("there is no type & network provided in Bitcoin unsigned transaction raw"), err=True)
        click.echo(click.style("Error: {}")
                   .format("invalid Bitcoin unsigned transaction raw"), err=True)
        sys.exit()

    try:
        if transaction["type"] == "bitcoin_fund_unsigned":
            # Fund HTLC solver
            fund_solver = FundSolver(
                private_key=private
            )
            # Fund signature
            fund_signature = FundSignature(network=transaction["network"], version=version)
            fund_signature.sign(unsigned_raw=unsigned_raw, solver=fund_solver)
            click.echo(fund_signature.signed_raw())

        elif transaction["type"] == "bitcoin_claim_unsigned":
            if secret is None:
                click.echo(click.style("Error: {}")
                           .format("secret key is required for claim, use -s or --secret \"Hello Meheret!\""), err=True)
                sys.exit()
            if bytecode is None:
                click.echo(click.style("Error: {}")
                           .format("witness bytecode is required for claim, use -b or --bytecode \"016...\""), err=True)
                sys.exit()

            # Claim HTLC solver
            claim_solver = ClaimSolver(
                private_key=private, secret=secret, bytecode=bytecode
            )
            # Claim signature
            claim_signature = ClaimSignature(network=transaction["network"], version=version)
            claim_signature.sign(unsigned_raw=unsigned_raw, solver=claim_solver)
            click.echo(claim_signature.signed_raw())

        elif transaction["type"] == "bitcoin_refund_unsigned":
            if bytecode is None:
                click.echo(click.style("Error: {}")
                           .format("witness bytecode is required for refund, use -b or --bytecode \"016...\""), err=True)
                sys.exit()

            # Refunding HTLC solver
            refund_solver = RefundSolver(
                private_key=private, sequence=int(sequence), bytecode=bytecode
            )
            # Refund signature
            refund_signature = RefundSignature(network=transaction["network"], version=version)
            refund_signature.sign(unsigned_raw=unsigned_raw, solver=refund_solver)
            click.echo(refund_signature.signed_raw())
        else:
            click.echo(click.style("Error: {}")
                       .format("unknown Bitcoin unsigned transaction raw type"), err=True)
            sys.exit()
    except Exception as exception:
        click.echo(click.style("Error: {}").format(str(exception)), err=True)
        sys.exit()
