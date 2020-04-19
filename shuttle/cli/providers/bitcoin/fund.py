#!/usr/bin/env python
# coding=utf-8

import sys


from shuttle.cli import click
from shuttle.providers.bitcoin.transaction import FundTransaction
from shuttle.providers.bitcoin.wallet import Wallet
from shuttle.providers.bitcoin.htlc import HTLC


@click.command("fund", options_metavar="[OPTIONS]",
               short_help="Select Bitcoin fund transaction builder.")
@click.option("-sa", "--sender-address", type=str, required=True, help="Set Bitcoin sender address.")
@click.option("-a", "--amount", type=int, required=True, help="Set Bitcoin amount to fund on HTLC.")
@click.option("-b", "--bytecode", type=str, required=True, help="Set Bitcoin HTLC bytecode.")
@click.option("-v", "--version", type=int, default=2, help="Set Bitcoin transaction version.")
@click.option("-n", "--network", type=str, default="testnet", help="Set Bitcoin network.")
def fund(sender_address, amount, bytecode, version, network):
    try:
        click.echo(
            FundTransaction(version=version, network=network).build_transaction(
                wallet=Wallet(network=network).from_address(address=sender_address),
                htlc=HTLC(network=network).from_bytecode(bytecode=bytecode),
                amount=int(amount)
            ).unsigned_raw()
        )
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
