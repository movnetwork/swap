#!/usr/bin/env python
# coding=utf-8

import sys

from ....cli import click
from ....providers.bitcoin.transaction import RefundTransaction
from ....providers.bitcoin.utils import amount_unit_converter
from ....providers.config import bitcoin as config


@click.command("refund", options_metavar="[OPTIONS]",
               short_help="Select Bitcoin Refund transaction builder.")
@click.option("-a", "--address", type=str, required=True, help="Set Bitcoin sender address.")
@click.option("-ti", "--transaction-id", type=str, required=True, help="Set Bitcoin funded transaction id/hash.")
@click.option("-am", "--amount", type=int, default=None,
              help="Set Bitcoin refund amount.  [default: None]", show_default=True)
@click.option("-ma", "--max-amount", type=bool, default=True,
              help="Set Bitcoin refund max amount.", show_default=True)
@click.option("-u", "--unit", type=str, default=config["unit"],
              help="Set Bitcoin refund amount unit.", show_default=True)
@click.option("-n", "--network", type=str, default=config["network"],
              help="Set Bitcoin network.", show_default=True)
@click.option("-v", "--version", type=int, default=config["version"],
              help="Set Bitcoin transaction version.", show_default=True)
def refund(address: str, transaction_id: str, amount: int, max_amount: bool, unit: str, network: str, version: int):
    try:
        click.echo(
            RefundTransaction(
                network=network,
                version=version
            ).build_transaction(
                address=address,
                transaction_id=transaction_id,
                amount=(int(amount) if unit == "SATOSHI" else amount_unit_converter(
                    amount=amount, unit_from=f"{unit}2SATOSHI"
                )),
                max_amount=max_amount
            ).transaction_raw()
        )
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
