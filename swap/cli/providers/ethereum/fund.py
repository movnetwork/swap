#!/usr/bin/env python
# coding=utf-8

from typing import Optional

import sys

from ....cli import click
from ....providers.ethereum.htlc import HTLC
from ....providers.ethereum.transaction import FundTransaction
from ....providers.ethereum.rpc import get_erc20_decimals
from ....providers.ethereum.utils import amount_unit_converter
from ....providers.config import ethereum as config
from ....utils import get_current_timestamp


@click.command("fund", options_metavar="[OPTIONS]",
               short_help="Select Ethereum Fund transaction builder.")
@click.option("-sh", "--secret-hash", type=str, required=True, help="Set secret 256 hash.")
@click.option("-ra", "--recipient-address", type=str, required=True, help="Set Ethereum recipient address.")
@click.option("-sa", "--sender-address", type=str, required=True, help="Set Ethereum sender address.")
@click.option("-e", "--endtime", type=int, required=True, help="Set Expiration block timestamp.")
@click.option("-am", "--amount", type=float, required=True, help="Set Ethereum fund amount.")
@click.option("-u", "--unit", type=str, default=config["unit"],
              help="Set Ethereum fund amount unit.", show_default=True)
@click.option("-ca", "--contract-address", type=str, default=None,
              help="Set Ethereum HTLC contact address.  [default: None]")
@click.option("-ta", "--token-address", type=str, default=None,
              help="Set Ethereum ERC20 token address.  [default: None]")
@click.option("-n", "--network", type=str, default=config["network"],
              help="Set Ethereum network.", show_default=True)
@click.option("-e20", "--erc20", type=bool, default=False,
              help="Set Enable Ethereum ERC20 token contract.", show_default=True)
def fund(
    secret_hash: str, recipient_address: str, sender_address: str, endtime: int, amount: int, unit: str,
    contract_address: Optional[str], token_address: Optional[str], network: str, erc20: bool
):
    try:
        _htlc: HTLC = HTLC(
            contract_address=contract_address, network=network, erc20=erc20
        )
        if erc20:
            _htlc.build_htlc(
                secret_hash=secret_hash,
                recipient_address=recipient_address,
                sender_address=sender_address,
                endtime=(get_current_timestamp() + endtime),
                token_address=token_address
            )
            decimals: int = get_erc20_decimals(
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
                network=network, erc20=erc20
            ).build_transaction(
                address=sender_address, htlc=_htlc, amount=_amount
            ).transaction_raw()
        )
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
