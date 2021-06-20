#!/usr/bin/env python
# coding=utf-8

import sys

from ....cli import click
from ....providers.ethereum.transaction import RefundTransaction
from ....providers.config import ethereum as config


@click.command("refund", options_metavar="[OPTIONS]",
               short_help="Select Ethereum Refund transaction builder.")
@click.option("-th", "--transaction-hash", type=str, required=True, help="Set Ethereum funded transaction hash/id.")
@click.option("-a", "--address", type=str, required=True, help="Set Ethereum sender address.")
@click.option("-hth", "--htlc-transaction-hash", type=str, default=None,
              help="Set Ethereum HTLC transaction hash.  [default: None]")
@click.option("-n", "--network", type=str, default=config["network"],
              help="Set Ethereum network.", show_default=True)
def refund(transaction_hash: str, address: str, htlc_transaction_hash: str,  network: str):
    try:
        click.echo(
            RefundTransaction(
                network=network
            ).build_transaction(
                address=address,
                transaction_hash=transaction_hash,
                htlc_transaction_hash=htlc_transaction_hash
            ).transaction_raw()
        )
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
