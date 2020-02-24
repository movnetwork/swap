#!/usr/bin/env python
# coding=utf-8

from base64 import b64encode, b64decode

import json

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
               short_help="Select bitcoin transaction raw signer.")
@click.option("-p", "--private", type=str, required=True, help="Set bitcoin private key.")
@click.option("-u", "--unsigned", type=str, required=True, help="Set bitcoin unsigned transaction raw.")
@click.option("-n", "--network", type=str, default=NETWORK,
              help="Set bitcoin network.", show_default=True)
@click.option("-v", "--version", type=int, default=VERSION,
              help="Set bitcoin version.", show_default=True)
def sign(private, unsigned, network, version):
    """
    SHUTTLE BITCOIN SIGN
    """

    unsigned_raw = str(unsigned + "=" * (-len(unsigned) % 4))
    transaction = json.loads(b64decode(unsigned_raw.encode()).decode())
    if "type" not in transaction:
        raise ValueError("invalid unsigned transaction raw")

    if transaction["type"] == "bitcoin_fund_unsigned":
        # Fund HTLC solver
        fund_solver = FundSolver(private_key=private)

        fund_signature = FundSignature(network=network, version=version)
        fund_signature.sign(unsigned_raw=unsigned_raw, solver=fund_solver)
        click.echo(fund_signature.signed_raw())

    elif transaction["type"] == "bitcoin_claim_unsigned":
        if "secret" not in transaction or transaction["secret"] is None:
            raise ValueError("invalid claim unsigned transaction raw, empty secret key")
        # Claim HTLC solver
        claim_solver = ClaimSolver(
            secret=transaction["secret"],
            private_key=private
        )
        # Claim signature
        claim_signature = ClaimSignature(network=network, version=version)
        claim_signature.sign(unsigned_raw=unsigned_raw, solver=claim_solver)
        click.echo(claim_signature.signed_raw())

    elif transaction["type"] == "bitcoin_refund_unsigned":
        if "secret" not in transaction or transaction["secret"] is None:
            raise ValueError("invalid refund unsigned transaction raw, empty secret key")
        # Refunding HTLC solver
        refund_solver = RefundSolver(
            secret=transaction["secret"],
            private_key=private
        )
        refund_signature = RefundSignature(network=network, version=version)
        refund_signature.sign(unsigned_raw=unsigned_raw, solver=refund_solver)
        click.echo(refund_signature.signed_raw())
