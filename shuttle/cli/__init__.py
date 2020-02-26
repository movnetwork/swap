#!/usr/bin/env python3

import textwrap
import click
import sys


# Success template
def success(_):
    return "[{}] {}".format(
        click.style("SUCCESS", fg="green"), str(_))


# Warning template
def warning(_):
    return "[{}] {}".format(
        click.style("WARNING", fg="yellow"), str(_))


# Error template
def error(_):
    return "[{}] {}".format(
        click.style("ERROR", fg="red"), str(_))


__all__ = [
    "textwrap",
    "click",
    "sys",
    "success",
    "warning",
    "error"
]
