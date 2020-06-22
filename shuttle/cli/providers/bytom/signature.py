#!/usr/bin/env python
# coding=utf-8

from base64 import b64decode

import json
import sys
import binascii

from shuttle.cli import click
from shuttle.providers.bytom.solver import (
    FundSolver, ClaimSolver, RefundSolver
)
from shuttle.providers.bytom.signature import (
    FundSignature, ClaimSignature, RefundSignature
)
from shuttle.providers.config import bytom

# Bytom config
bytom = bytom()


@click.command("sign", options_metavar="[OPTIONS]",
               short_help="Select Bytom transaction raw signer.")
@click.option("-xp", "--xprivate", type=str, required=True, help="Set Bytom xprivate key.")
@click.option("-r", "--raw", type=str, required=True,
              help="Set Bytom unsigned transaction raw.")
@click.option("-ac", "--account", type=int, default=1,
              show_default=True, help="Set Bytom derivation from account.")
@click.option("-c", "--change", type=bool, default=False,
              show_default=True, help="Set Bytom derivation from change.")
@click.option("-ad", "--address", type=int, default=1,
              show_default=True, help="Set Bytom derivation from address.")
@click.option("-b", "--bytecode", type=str, default=None, help="Set Bytom witness HTLC bytecode.")
@click.option("-s", "--secret", type=str, default=None, help="Set secret key.")
@click.option("-p", "--path", type=str, default=None,
              help="Set Bytom derivation from path.")
@click.option("-i", "--indexes", type=list, default=None,
              help="Set Bytom derivation from indexes.")
def sign(xprivate, raw, account, change, address, bytecode, secret, path, indexes):
    if len(xprivate) != 128:
        click.echo(click.style("Error: {}")
                   .format("invalid Bytom xprivate key"), err=True)
        sys.exit()

    # Cleaning unsigned raw
    unsigned_raw = str(raw + "=" * (-len(raw) % 4))
    try:
        transaction = json.loads(b64decode(unsigned_raw.encode()).decode())
    except (binascii.Error, json.decoder.JSONDecodeError) as exception:
        click.echo(click.style("Error: {}")
                   .format("invalid Bytom unsigned transaction raw"), err=True)
        sys.exit()
    if "type" not in transaction or "network" not in transaction:
        click.echo(click.style("Warning: {}", fg="yellow")
                   .format("there is no type & network provided in Bytom unsigned transaction raw"), err=True)
        click.echo(click.style("Error: {}")
                   .format("invalid Bytom unsigned transaction raw"), err=True)
        sys.exit()

    try:
        if transaction["type"] == "bytom_fund_unsigned":
            # Fund HTLC solver
            fund_solver = FundSolver(
                xprivate_key=xprivate, account=account, change=change, address=address,
                path=path, indexes=indexes
            )
            # Fund signature
            fund_signature = FundSignature(network=transaction["network"])
            fund_signature.sign(unsigned_raw=unsigned_raw, solver=fund_solver)
            click.echo(fund_signature.signed_raw())

        elif transaction["type"] == "bytom_claim_unsigned":
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
                xprivate_key=xprivate, account=account, change=change, address=address,
                path=path, indexes=indexes, secret=secret, bytecode=bytecode
            )
            # Claim signature
            claim_signature = ClaimSignature(network=transaction["network"])
            claim_signature.sign(unsigned_raw=unsigned_raw, solver=claim_solver)
            click.echo(claim_signature.signed_raw())
    
        elif transaction["type"] == "bytom_refund_unsigned":
            if bytecode is None:
                click.echo(click.style("Error: {}")
                           .format("witness bytecode is required for refund, use -b or --bytecode \"016...\""), err=True)
                sys.exit()
            # Refunding HTLC solver
            refund_solver = RefundSolver(
                xprivate_key=xprivate, account=account, change=change, address=address,
                path=path, indexes=indexes, bytecode=bytecode
            )
            # Refund signature
            refund_signature = RefundSignature(network=transaction["network"])
            refund_signature.sign(unsigned_raw=unsigned_raw, solver=refund_solver)
            click.echo(refund_signature.signed_raw())
        else:
            click.echo(click.style("Error: {}")
                       .format("unknown Bytom unsigned transaction raw type"), err=True)
            sys.exit()
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
