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


@click.group("xinfin", options_metavar="[OPTIONS]",
             short_help="Select XinFin provider.")
def xinfin():
    pass


# Adding xinfin commands
xinfin.add_command(htlc)
xinfin.add_command(fund)
xinfin.add_command(withdraw)
xinfin.add_command(refund)
xinfin.add_command(decode)
xinfin.add_command(sign)
xinfin.add_command(submit)
