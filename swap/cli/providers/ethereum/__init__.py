#!/usr/bin/env python
# coding=utf-8

# IMPORT ALL PACKAGES
from ....cli import click

from .htlc import htlc
from .fund import fund
from .withdraw import withdraw
from .refund import refund
from .decode import decode
from .signature import sign
from .submit import submit


@click.group("ethereum", options_metavar="[OPTIONS]",
             short_help="Select Ethereum provider.")
def ethereum():
    pass


# Adding ethereum commands
ethereum.add_command(htlc)
ethereum.add_command(fund)
ethereum.add_command(withdraw)
ethereum.add_command(refund)
ethereum.add_command(decode)
ethereum.add_command(sign)
ethereum.add_command(submit)
