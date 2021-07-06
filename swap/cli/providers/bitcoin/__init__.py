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


@click.group("bitcoin", options_metavar="[OPTIONS]",
             short_help="Select Bitcoin provider.")
def bitcoin():
    pass


# Adding bitcoin commands
bitcoin.add_command(htlc)
bitcoin.add_command(fund)
bitcoin.add_command(withdraw)
bitcoin.add_command(refund)
bitcoin.add_command(decode)
bitcoin.add_command(sign)
bitcoin.add_command(submit)
