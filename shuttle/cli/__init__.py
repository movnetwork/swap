#!/usr/bin/env python3

import textwrap
import argparse
import sys

from .signature import signature

__all__ = [
    "textwrap",
    "argparse",
    "sys",
    "signature"
]

# def main(argv=None):
#     if argv is None:
#         argv = sys.argv[1:]
#     parser = argparse.ArgumentParser(
#         prog="shuttle",
#         epilog=textwrap.dedent(information),
#         description="Cross-chain atomic swaps between the networks of two cryptocurrencies."
#     )
#
#     parser.add_argument("--version", action="version",
#                         version="PyShuttle version %s" % __version__)
#
#     parser.add_argument("-u", "--url", action="store", default="http://localhost:9888",
#                         help="Bytom API url. Default(http://localhost:9888)")
#
#     parser.add_argument("-f", "--file", type=argparse.FileType("r"), required=True,
#                         help="Unsigned transaction raw file.")
#
#     parser.add_argument("-a", "--args", nargs="*",
#                         help="Parameters of contract.")
#
#     parser.add_argument("-s", "--save", action="store",
#                         help="Save signed transaction raw.")
#
#     try:
#         _args = []
#         parse_args = parser.parse_args()
#
#         if parse_args.args is not None:
#             args = parse_args.args
#             for arg in args:
#                 try:
#                     _args.append({"integer": int(arg)})
#                 except ValueError:
#                     if str2bool(arg):
#                         _args.append({"boolean": "true"})
#                     elif str2bool(arg) is None:
#                         _args.append({"string": arg})
#                     else:
#                         _args.append({"boolean": "false"})
#
#         signature(url=parse_args.url, equity_source=parse_args.file.read(),
#                  name=parse_args.file.name, args=_args, save=parse_args.save)
#
#     except Exception as exception:
#         parser.error(str(exception))
