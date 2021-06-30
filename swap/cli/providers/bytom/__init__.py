#!/usr/bin/env python
# coding=utf-8

from ....cli import click

from .htlc import htlc
from .fund import fund
from .withdraw import withdraw
from .refund import refund
from .decode import decode
from .signature import sign
from .submit import submit


@click.group("bytom", options_metavar="[OPTIONS]",
             short_help="Select Bytom provider.")
def bytom():
    pass


# Adding bytom commands
bytom.add_command(htlc)
bytom.add_command(fund)
bytom.add_command(withdraw)
bytom.add_command(refund)
bytom.add_command(decode)
bytom.add_command(sign)
bytom.add_command(submit)
