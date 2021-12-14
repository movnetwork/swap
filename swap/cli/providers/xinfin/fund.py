#!/usr/bin/env python
# coding=utf-8

from typing import Optional

import sys

from ....cli import click
from ....providers.xinfin.htlc import HTLC
from ....providers.xinfin.transaction import FundTransaction
from ....providers.xinfin.rpc import get_xrc20_decimals
from ....providers.xinfin.utils import amount_unit_converter
from ....providers.config import xinfin as config
from ....utils import get_current_timestamp


@click.command("fund", options_metavar="[OPTIONS]",
               short_help="Select XinFin Fund transaction builder.")
@click.option("-sh", "--secret-hash", type=str, required=True, help="Set secret 256 hash.")
@click.option("-ra", "--recipient-address", type=str, required=True, help="Set XinFin recipient address.")
@click.option("-sa", "--sender-address", type=str, required=True, help="Set XinFin sender address.")
@click.option("-e", "--endtime", type=int, required=True, help="Set Expiration block timestamp.")
@click.option("-am", "--amount", type=float, required=True, help="Set XinFin fund amount.")
@click.option("-u", "--unit", type=str, default=config["unit"],
              help="Set XinFin fund amount unit.", show_default=True)
@click.option("-ca", "--contract-address", type=str, default=None,
              help="Set XinFin HTLC contact address.  [default: None]")
@click.option("-ta", "--token-address", type=str, default=None,
              help="Set XinFin XRC20 token address.  [default: None]")
@click.option("-n", "--network", type=str, default=config["network"],
              help="Set XinFin network.", show_default=True)
@click.option("-x20", "--xrc20", type=bool, default=False,
              help="Set Enable XinFin XRC20 token contract.", show_default=True)
def fund(
    secret_hash: str, recipient_address: str, sender_address: str, endtime: int, amount: int, unit: str,
    contract_address: Optional[str], token_address: Optional[str], network: str, xrc20: bool
):
    try:
        _htlc: HTLC = HTLC(
            contract_address=contract_address, network=network, xrc20=xrc20
        )
        if xrc20:
            _htlc.build_htlc(
                secret_hash=secret_hash,
                recipient_address=recipient_address,
                sender_address=sender_address,
                endtime=(get_current_timestamp() + endtime),
                token_address=token_address
            )
            decimals: int = get_xrc20_decimals(
                token_address=token_address, network=network
            )
            _amount: int = int(amount) * int(10 ** decimals)
        else:
            _htlc.build_htlc(
                secret_hash=secret_hash,
                recipient_address=recipient_address,
                sender_address=sender_address,
                endtime=(get_current_timestamp() + endtime)
            )
            _amount: int = (
                int(amount) if unit == "Wei" else amount_unit_converter(amount=amount, unit_from=f"{unit}2Wei")
            )
        click.echo(
            FundTransaction(
                network=network, xrc20=xrc20
            ).build_transaction(
                address=sender_address, htlc=_htlc, amount=_amount
            ).transaction_raw()
        )
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
