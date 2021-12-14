#!/usr/bin/env python
# coding=utf-8

import json
import sys

from ....cli import click
from ....providers.ethereum.htlc import HTLC
from ....providers.config import ethereum as config


@click.command("htlc", options_metavar="[OPTIONS]",
               short_help="Select Ethereum Hash Time Lock Contract (HTLC) builder.")
@click.option("-ca", "--contract-address", type=str, default=None,
              help="Set Ethereum HTLC contact address.  [default: None]")
@click.option("-n", "--network", type=str, default=config["network"],
              help="Set Ethereum network.", show_default=True)
@click.option("-e20", "--erc20", type=bool, default=False,
              help="Set Enable Ethereum ERC20 token contract.", show_default=True)
@click.option("-i", "--indent", type=int, default=4, help="Set json indent.", show_default=True)
def htlc(contract_address: str, network: str, erc20: bool, indent: int):
    try:
        _htlc: HTLC = HTLC(
            contract_address=contract_address,
            network=network,
            erc20=erc20
        )
        click.echo(json.dumps(dict(
            abi=_htlc.abi(),
            bytecode=_htlc.bytecode(),
            bytecode_runtime=_htlc.bytecode_runtime(),
            contract_address=_htlc.contract_address()
        ), indent=indent))
    except Exception as exception:
        click.echo(click.style("Error: {}")
                   .format(str(exception)), err=True)
        sys.exit()
