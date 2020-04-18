#!/usr/bin/env python
# coding=utf-8

# IMPORT ALL PACKAGES
from shuttle.cli import click

from .fund import fund
from .htlc import htlc
from .signature import sign
from .decode import decode
from .submit import submit


@click.group("bitcoin", options_metavar="[OPTIONS]",
             short_help="Select Bitcoin provider.")
def bitcoin():
    pass


# Adding bitcoin htlc
bitcoin.add_command(fund)
# Adding bitcoin htlc
bitcoin.add_command(htlc)
# Adding bitcoin sign
bitcoin.add_command(sign)
# Adding bitcoin decoder
bitcoin.add_command(decode)
# Adding bitcoin submit
bitcoin.add_command(submit)
