#!/usr/bin/env python
# coding=utf-8

from base64 import b64encode, b64decode

import json
import sys
import binascii

from shuttle.cli import click
from shuttle.providers.bitcoin.solver \
    import FundSolver, ClaimSolver, RefundSolver
from shuttle.providers.bitcoin.signature \
    import FundSignature, ClaimSignature, RefundSignature

# Bitcoin network.
NETWORK = "mainnet"  # testnet
# Bitcoin transaction version.
VERSION = 2  # 1


@click.command("sign", options_metavar="[OPTIONS]",
               short_help="Select Bitcoin transaction raw signer.")
@click.option("-p", "--private", type=str, required=True, help="Set Bitcoin private key.")
@click.option("-u", "--unsigned", type=str, required=True, help="Set Bitcoin unsigned transaction raw.")
@click.option("-s", "--secret", type=str, default=str(), help="Set secret key.")
@click.option("-v", "--version", type=int, default=VERSION,
              help="Set Bitcoin version.", show_default=True)
def sign(private, unsigned, secret, version):
    if len(private) != 64:
        click.echo("invalid Bitcoin private key")
        sys.exit()

    unsigned_raw = str(unsigned + "=" * (-len(unsigned) % 4))
    try:
        transaction = json.loads(b64decode(unsigned_raw.encode()).decode())
    except (binascii.Error, json.decoder.JSONDecodeError) as _error:
        click.echo("invalid unsigned transaction raw")
        sys.exit()
    if "type" not in transaction:
        click.echo("there is no type provided on unsigned transaction raw")
        click.echo("invalid unsigned transaction raw")
        sys.exit()
    if "network" not in transaction:
        click.echo("there is no network provided on unsigned transaction raw")
        click.echo("invalid unsigned transaction raw")
        sys.exit()

    if transaction["type"] == "bitcoin_fund_unsigned":
        # Fund HTLC solver
        fund_solver = FundSolver(private_key=private)
        try:
            # Fund signature
            fund_signature = FundSignature(network=transaction["network"], version=version)
            fund_signature.sign(unsigned_raw=unsigned_raw, solver=fund_solver)
            click.echo(fund_signature.signed_raw())
        except Exception as exception:
            click.echo(exception)
            sys.exit()

    elif transaction["type"] == "bitcoin_claim_unsigned":
        if secret != str():
            _secret = secret
        elif "secret" not in transaction or transaction["secret"] is None:
            click.echo("secret key is empty, use -s or --secret \"Hello Meheret!\"")
            _secret = str()
        else:
            _secret = transaction["secret"]
        # Claim HTLC solver
        claim_solver = ClaimSolver(
            secret=_secret,
            private_key=private
        )
        try:
            # Claim signature
            claim_signature = ClaimSignature(network=transaction["network"], version=version)
            claim_signature.sign(unsigned_raw=unsigned_raw, solver=claim_solver)
            click.echo(claim_signature.signed_raw())
        except Exception as exception:
            click.echo(exception)
            sys.exit()

    elif transaction["type"] == "bitcoin_refund_unsigned":
        if secret != str():
            _secret = secret
        elif "secret" not in transaction or transaction["secret"] is None:
            click.echo("secret key is empty, use -s or --secret \"Hello Meheret!\"")
            _secret = str()
        else:
            _secret = transaction["secret"]
        # Refunding HTLC solver
        refund_solver = RefundSolver(
            secret=_secret,
            private_key=private
        )
        try:
            # Refund signature
            refund_signature = RefundSignature(network=transaction["network"], version=version)
            refund_signature.sign(unsigned_raw=unsigned_raw, solver=refund_solver)
            click.echo(refund_signature.signed_raw())
        except Exception as exception:
            click.echo(exception)
            sys.exit()
