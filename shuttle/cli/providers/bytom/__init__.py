#!/usr/bin/env python
# coding=utf-8

# IMPORT ALL PACKAGES
from shuttle.cli import click

from .fund import fund
from .htlc import htlc
from .signature import sign
from .decode import decode
from .submit import submit


@click.group("bytom", options_metavar="[OPTIONS]",
             short_help="Select Bytom provider.")
def bytom():
    pass


# Adding bitcoin fund
bytom.add_command(fund)
# Adding bitcoin htlc
bytom.add_command(htlc)
# Adding bytom sign
bytom.add_command(sign)
# Adding bytom decoder
bytom.add_command(decode)
# Adding bytom submit
bytom.add_command(submit)
