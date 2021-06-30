#!/usr/bin/env python
# coding=utf-8

import sys

from ....cli import click
from ....providers.ethereum.htlc import HTLC
from ....providers.ethereum.transaction import FundTransaction
from ....providers.ethereum.utils import amount_unit_converter
from ....providers.config import ethereum as config
from ....utils import get_current_timestamp


@click.command("fund", options_metavar="[OPTIONS]",
               short_help="Select Ethereum Fund transaction builder.")
@click.option("-sh", "--secret-hash", type=str, required=True, help="Set secret 256 hash.")
@click.option("-ra", "--recipient-address", type=str, required=True, help="Set Ethereum recipient address.")
@click.option("-sa", "--sender-address", type=str, required=True, help="Set Ethereum sender address.")
@click.option("-e", "--endtime", type=int, required=True, help="Set Expiration block time (Seconds).")
@click.option("-am", "--amount", type=float, required=True, help="Set Ethereum fund amount.")
@click.option("-u", "--unit", type=str, default=config["unit"],
              help="Set Ethereum fund amount unit.", show_default=True)
@click.option("-hth", "--htlc-transaction-hash", type=str, default=None,
              help="Set Ethereum HTLC transaction hash.  [default: None]")
@click.option("-n", "--network", type=str, default=config["network"],
              help="Set Ethereum network.", show_default=True)
def fund(
    secret_hash: str, recipient_address: str, sender_address: str, endtime: int,
    amount: int, unit: str, htlc_transaction_hash: str, network: str
):
    try:
        _htlc: HTLC = HTLC(
            transaction_hash=htlc_transaction_hash, network=network
        ).build_htlc(
            secret_hash=secret_hash,
            recipient_address=recipient_address,
            sender_address=sender_address,
            endtime=(get_current_timestamp() + endtime)
        )
        _amount: int = (
            int(amount) if unit == "Wei" else amount_unit_converter(amount=amount, unit=f"{unit}2Wei")
        )
        click.echo(
            FundTransaction(network=network).build_transaction(
                address=sender_address, htlc=_htlc, amount=_amount
            ).transaction_raw()
        )
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
