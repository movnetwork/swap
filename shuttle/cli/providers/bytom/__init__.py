#!/usr/bin/env python
# coding=utf-8

# IMPORT ALL PACKAGES
from shuttle.cli import click

from .signature import sign


@click.group("bytom", options_metavar="[OPTIONS]",
             short_help="Select bytom cryptocurrency provider.")
def bytom():
    """
    SHUTTLE BYTOM
    """
    pass


# Adding bytom sign
bytom.add_command(sign)
