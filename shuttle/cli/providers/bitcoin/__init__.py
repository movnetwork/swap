#!/usr/bin/env python
# coding=utf-8

# IMPORT ALL PACKAGES
from shuttle.cli import click

from .signature import sign


@click.group("bitcoin", options_metavar="[OPTIONS]",
             short_help="Select bitcoin cryptocurrency provider.")
def bitcoin():
    """
    SHUTTLE BITCOIN
    """
    pass


# Adding bitcoin sign
bitcoin.add_command(sign)
