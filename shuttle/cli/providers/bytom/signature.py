#!/usr/bin/env python
# coding=utf-8

from base64 import b64encode, b64decode

import json
import sys
import binascii

from shuttle.cli import click
from shuttle.providers.bytom.solver \
    import FundSolver, ClaimSolver, RefundSolver
from shuttle.providers.bytom.signature \
    import FundSignature, ClaimSignature, RefundSignature

# Bytom network.
NETWORK = "solonet"  # mainnet or testnet


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
@click.option("-s", "--secret", type=str, default=str(), help="Set secret key.")
@click.option("-p", "--path", type=str, default=None,
              help="Set Bytom derivation from path.")
@click.option("-i", "--indexes", type=list, default=None,
              help="Set Bytom derivation from indexes.")
def sign(xprivate, raw, account, change, address, secret, path, indexes):
    if len(xprivate) != 128:
        click.echo("invalid Bytom xprivate key")
        sys.exit()

    unsigned_raw = str(raw + "=" * (-len(raw) % 4))
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

    if transaction["type"] == "bytom_fund_unsigned":
        # Fund HTLC solver
        fund_solver = FundSolver(xprivate_key=xprivate, account=account,
                                 change=change, address=address, path=path, indexes=indexes)
        try:
            # Fund signature
            fund_signature = FundSignature(network=transaction["network"])
            fund_signature.sign(unsigned_raw=unsigned_raw, solver=fund_solver)
            click.echo(fund_signature.signed_raw())
        except Exception as exception:
            click.echo(exception)
            sys.exit()

    elif transaction["type"] == "bytom_claim_unsigned":
        if secret != str():
            _secret = secret
        elif "secret" not in transaction or transaction["secret"] is None:
            click.echo("secret key is empty, use -s or --secret \"Hello Meheret!\", default to None")
            _secret = str()
        else:
            _secret = transaction["secret"]
        # Claim HTLC solver
        claim_solver = ClaimSolver(secret=_secret, xprivate_key=xprivate, account=account,
                                   change=change, address=address, path=path, indexes=indexes)
        try:
            # Claim signature
            claim_signature = ClaimSignature(network=transaction["network"])
            claim_signature.sign(unsigned_raw=unsigned_raw, solver=claim_solver)
            click.echo(claim_signature.signed_raw())
        except Exception as exception:
            click.echo(exception)
            sys.exit()

    elif transaction["type"] == "bytom_refund_unsigned":
        # Refunding HTLC solver
        refund_solver = RefundSolver(xprivate_key=xprivate, account=account,
                                     change=change, address=address, path=path, indexes=indexes)
        try:
            # Refund signature
            refund_signature = RefundSignature(network=transaction["network"])
            refund_signature.sign(unsigned_raw=unsigned_raw, solver=refund_solver)
            click.echo(refund_signature.signed_raw())
        except Exception as exception:
            click.echo(exception)
            sys.exit()
