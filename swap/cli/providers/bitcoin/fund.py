#!/usr/bin/env python
# coding=utf-8

import sys

from ....cli import click
from ....providers.bitcoin.htlc import HTLC
from ....providers.bitcoin.transaction import FundTransaction
from ....providers.bitcoin.utils import amount_unit_converter
from ....providers.config import bitcoin as config


@click.command("fund", options_metavar="[OPTIONS]",
               short_help="Select Bitcoin Fund transaction builder.")
@click.option("-a", "--address", type=str, required=True, help="Set Bitcoin sender address.")
@click.option("-ca", "--contract-address", type=str, required=True,
              help="Set Bitcoin Hash Time Lock Contract (HTLC) address.")
@click.option("-am", "--amount", type=float, required=True, help="Set Bitcoin fund amount.")
@click.option("-u", "--unit", type=str, default=config["unit"],
              help="Set Bitcoin fund amount unit.", show_default=True)
@click.option("-n", "--network", type=str, default=config["network"],
              help="Set Bitcoin network.", show_default=True)
@click.option("-v", "--version", type=int, default=config["version"],
              help="Set Bitcoin transaction version.", show_default=True)
def fund(address: str, contract_address: str, amount: int, unit: str, network: str, version: int):
    try:
        _htlc: HTLC = HTLC(
            network=network, contract_address=contract_address
        )
        _amount: int = (
            int(amount) if unit == "Satoshi" else amount_unit_converter(
                amount=amount, unit_from=f"{unit}2Satoshi"
            )
        )
        click.echo(
            FundTransaction(
                network=network, version=version
            ).build_transaction(
                address=address, htlc=_htlc, amount=_amount
            ).transaction_raw()
        )
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
