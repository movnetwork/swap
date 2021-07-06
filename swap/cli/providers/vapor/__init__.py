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


@click.group("vapor", options_metavar="[OPTIONS]",
             short_help="Select Vapor provider.")
def vapor():
    pass


# Adding vapor commands
vapor.add_command(htlc)
vapor.add_command(fund)
vapor.add_command(withdraw)
vapor.add_command(refund)
vapor.add_command(decode)
vapor.add_command(sign)
vapor.add_command(submit)
