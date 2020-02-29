#!/usr/bin/env python
# coding=utf-8

from base64 import b64encode, b64decode

import json
import sys
import binascii

from shuttle.cli import click, success, warning, error
from shuttle.providers.bytom.solver \
    import FundSolver, ClaimSolver, RefundSolver
from shuttle.providers.bytom.signature \
    import FundSignature, ClaimSignature, RefundSignature

# Bytom network.
NETWORK = "solonet"  # mainnet or testnet


@click.command("sign", options_metavar="[OPTIONS]",
               short_help="Select bytom transaction raw signer.")
@click.option("-xp", "--xprivate", type=str, required=True, help="Set bytom xprivate key.")
@click.option("-u", "--unsigned", type=str, required=True, help="Set bytom unsigned transaction raw.")
@click.option("-s", "--secret", type=str, default=str(), help="Set secret key.")
def sign(xprivate, unsigned, secret):
    """
    SHUTTLE BYTOM SIGN
    """
    if len(xprivate) != 128:
        click.echo(error("invalid bytom xprivate key"))
        sys.exit()

    unsigned_raw = str(unsigned + "=" * (-len(unsigned) % 4))
    try:
        transaction = json.loads(b64decode(unsigned_raw.encode()).decode())
    except (binascii.Error, json.decoder.JSONDecodeError) as _error:
        click.echo(error("invalid unsigned transaction raw"))
        sys.exit()
    if "type" not in transaction:
        click.echo(warning("there is no type provided on unsigned transaction raw"))
        click.echo(error("invalid unsigned transaction raw"))
        sys.exit()
    if "network" not in transaction:
        click.echo(warning("there is no network provided on unsigned transaction raw"))
        click.echo(error("invalid unsigned transaction raw"))
        sys.exit()

    if transaction["type"] == "bytom_fund_unsigned":
        # Fund HTLC solver
        fund_solver = FundSolver(xprivate_key=xprivate)
        try:
            # Fund signature
            fund_signature = FundSignature(network=transaction["network"])
            fund_signature.sign(unsigned_raw=unsigned_raw, solver=fund_solver)
            click.echo(success(fund_signature.signed_raw()))
        except Exception as exception:
            click.echo(error(exception))
            sys.exit()

    elif transaction["type"] == "bytom_claim_unsigned":
        if secret != str():
            _secret = secret
        elif "secret" not in transaction or transaction["secret"] is None:
            click.echo(warning("secret key is empty, use -s or --secret \"Hello Meheret!\""))
            _secret = str()
        else:
            _secret = transaction["secret"]
        # Claim HTLC solver
        claim_solver = ClaimSolver(
            secret=_secret,
            xprivate_key=xprivate
        )
        try:
            # Claim signature
            claim_signature = ClaimSignature(network=transaction["network"])
            claim_signature.sign(unsigned_raw=unsigned_raw, solver=claim_solver)
            click.echo(success(claim_signature.signed_raw()))
        except Exception as exception:
            click.echo(error(exception))
            sys.exit()

    elif transaction["type"] == "bytom_refund_unsigned":
        if secret != str():
            _secret = secret
        elif "secret" not in transaction or transaction["secret"] is None:
            click.echo(warning("secret key is empty, use -s or --secret \"Hello Meheret!\""))
            _secret = str()
        else:
            _secret = transaction["secret"]
        # Refunding HTLC solver
        refund_solver = RefundSolver(
            secret=_secret,
            xprivate_key=xprivate
        )
        try:
            # Refund signature
            refund_signature = RefundSignature(network=transaction["network"])
            refund_signature.sign(unsigned_raw=unsigned_raw, solver=refund_solver)
            click.echo(success(refund_signature.signed_raw()))
        except Exception as exception:
            click.echo(error(exception))
            sys.exit()
