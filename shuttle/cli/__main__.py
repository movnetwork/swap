#!/usr/bin/env python
# coding=utf-8

# IMPORT ALL PACKAGES
from shuttle import __version__, __author__, __author_email__
from shuttle.cli import *

description = textwrap.dedent("""
    PyShuttle \n
    Cross-chain atomic swaps between the networks of two cryptocurrencies
""")

information = textwrap.dedent("""
    DONATION
    BITCOIN 3LLtTQaGV8bfvqtaeJinitzob8Y8CvryA7
    BYTOM bm1qzx7pjr6whcaxmh9u0thkjuavf2ynk3zkgshhle
    
    AUTHOR %s
    AUTHOR EMAIL %s
""" % (__author__, __author_email__))


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(
        prog="shuttle",
        usage="[providers] [-h, --help] [-v, --version]",
        description=description,
        epilog=information
    )
    # Set parser error
    parser.error = lambda message: \
        print(parser.format_usage() + "error: " + message)

    parser.add_argument("-v", "--version", action="version",
                        version="PyShuttle version %s" % __version__,
                        help="show pyshuttle version number and exit")

    shuttle_subparsers = parser.add_subparsers(
        title="shuttle providers",
        metavar="btc, bitcoin          bitcoin cryptocurrency" + "\n  " +
                "btm, bytom            bytom cryptocurrency"
    )

    shuttle_parser_bitcoin = shuttle_subparsers.add_parser(
        name="bitcoin", usage="[arguments] [-h, --help]")
    shuttle_parser_bitcoin.error = lambda message: print("error: " + message)
    shuttle_subparsers_bitcoin = shuttle_parser_bitcoin.add_subparsers(
        title="bitcoin arguments",
        metavar="sign, signature       to sign bitcoin unsigned transaction raw"
    )
    shuttle_parser_bytom = shuttle_subparsers.add_parser(
        name="bytom", usage="[arguments] [-h, --help]")
    shuttle_subparsers_bytom = shuttle_parser_bytom.add_subparsers(
        title="bytom arguments",
        metavar="sign, signature       to sign bytom unsigned transaction raw"
    )

    shuttle_parser_bitcoin_sign = shuttle_subparsers_bitcoin.add_parser(
        name="sign", usage="[-p, --private] [-u, -unsigned] [-f, --file] [-s, --save]")
    shuttle_parser_bitcoin_sign.error = lambda message: \
        print(shuttle_parser_bitcoin_sign.format_usage() + "error: " + message)
    shuttle_parser_bitcoin_sign.add_argument("-p", "--private", dest="private", action="store", required=True,
                                             help="bitcoin private key")
    shuttle_parser_bitcoin_sign.add_argument("-u", "--unsigned", action="store", default=None,
                                             help="bitcoin unsigned transaction raw")
    shuttle_parser_bitcoin_sign.add_argument("-f", "--file", type=argparse.FileType("r"),
                                             help="unsigned transaction raw file")
    shuttle_parser_bitcoin_sign.add_argument("-s", "--save", action="store", default=None,
                                             help="save signed transaction raw")

    shuttle_parser_bytom_sign = shuttle_subparsers_bytom.add_parser(
        name="sign", usage="[-xp, --xprivate] [-u, -unsigned] [-f, --file] [-s, --save]")
    shuttle_parser_bytom_sign.add_argument("-xp", "--xprivate", action="store", required=True,
                                           help="bytom xprivate key")
    shuttle_parser_bytom_sign.add_argument("-u", "--unsigned", action="store", default=None,
                                           help="bytom unsigned transaction raw")
    shuttle_parser_bytom_sign.add_argument("-f", "--file", type=argparse.FileType("r"),
                                           help="unsigned transaction raw file")
    shuttle_parser_bytom_sign.add_argument("-s", "--save", action="store", default=None,
                                           help="save signed transaction raw")

    # try:
    parse_args = parser.parse_args()

    if not argv:
        print("usage: [providers] [-h, --help] [-v, --version]")

        # elif parse_args.help:
        # parser.print_help()

    # except Exception as exception:
    #     parser.error(str(exception))
