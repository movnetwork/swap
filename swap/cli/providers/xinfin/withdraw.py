#!/usr/bin/env python
# coding=utf-8

from typing import Optional

import sys

from ....cli import click
from ....providers.xinfin.transaction import WithdrawTransaction
from ....providers.config import xinfin as config


@click.command("withdraw", options_metavar="[OPTIONS]",
               short_help="Select XinFin Withdraw transaction builder.")
@click.option("-th", "--transaction-hash", type=str, required=True, help="Set XinFin funded transaction hash/id.")
@click.option("-a", "--address", type=str, required=True, help="Set XinFin recipient address.")
@click.option("-sk", "--secret-key", type=str, required=True, help="Set secret password/passphrase.")
@click.option("-ca", "--contract-address", type=str, default=None,
              help="Set XinFin HTLC contact address.  [default: None]")
@click.option("-n", "--network", type=str, default=config["network"],
              help="Set XinFin network.", show_default=True)
@click.option("-x20", "--xrc20", type=bool, default=False,
              help="Set Enable XinFin XRC20 token contract.", show_default=True)
def withdraw(transaction_hash: str, address: str, secret_key: str, contract_address: Optional[str], network: str, xrc20: bool):
    try:
        click.echo(
            WithdrawTransaction(
                network=network, xrc20=xrc20
            ).build_transaction(
                address=address,
                transaction_hash=transaction_hash,
                secret_key=secret_key,
                contract_address=contract_address
            ).transaction_raw()
        )
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
