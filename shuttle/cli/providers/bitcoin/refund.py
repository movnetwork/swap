#!/usr/bin/env python
# coding=utf-8

import sys


from shuttle.cli import click
from shuttle.providers.bitcoin.transaction import RefundTransaction
from shuttle.providers.bitcoin.wallet import Wallet


@click.command("refund", options_metavar="[OPTIONS]",
               short_help="Select Bitcoin refund transaction builder.")
@click.option("-t", "--transaction", type=str, required=True, help="Set Bitcoin fund transaction id.")
@click.option("-sa", "--sender-address", type=str, required=True, help="Set Bitcoin sender address.")
@click.option("-a", "--amount", type=int, required=True, help="Set Bitcoin amount to refund.")
@click.option("-v", "--version", type=int, default=2, help="Set Bitcoin transaction version.")
@click.option("-n", "--network", type=str, default="testnet", help="Set Bitcoin network.")
def refund(transaction, sender_address, amount, version, network):
    try:
        click.echo(
            RefundTransaction(version=version, network=network).build_transaction(
                transaction_id=transaction,
                wallet=Wallet(network=network).from_address(address=sender_address),
                amount=int(amount)
            ).unsigned_raw()
        )
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
