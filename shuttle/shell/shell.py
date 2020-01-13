#!/usr/bin/env python3

from cmd import Cmd
from subprocess import call

import json

from shuttle.providers.bitcoin.wallet import Wallet as BTCWallet
from shuttle.providers.bitcoin.htlc import HTLC as BTCHTLC
from shuttle.providers.bitcoin.transaction import FundTransaction as BTCFundTransaction
from shuttle.providers.bitcoin.solver import FundSolver as BTCFundSolver
from shuttle.utils import sha256
from shuttle.providers.bytom.wallet import Wallet as BTMWallet
from shuttle.providers.bytom.htlc import HTLC as BTMHTLC
from shuttle.providers.bytom.transaction import FundTransaction as BTMFundTransaction
from shuttle.providers.bytom.solver import FundSolver as BTMFundSolver


class Shell(Cmd):
    prompt = "\033[1;38m(\033[1;0m%s\033[1;38m)\033[1;0m \033[1;31m>\033[1;0m " % "shuttle"
    intro = "Welcome to the shuttle shell. Type help or ? to list commands.\n"

    def __init__(self):
        super().__init__()
        self.btc_network, self.btm_network = None, None
        self.btc_wallet, self.btm_wallet = None, None

    def set_network(self, args):
        if args[2] == "mainnet":
            self.btc_network = "mainnet"
        elif args[2] == "testnet":
            self.btc_network = "testnet"
        else:
            print("Invalid network.")
            return

    def set_wallet(self, args):
        if args[2] in ["--passphrase", "--pass", "passphrase", "pass"]:
            passphrase = args[3].split('"')[1].encode() \
                if len(args[3].split('"')) == 3 else args[3].encode()
            if passphrase:
                self.btc_wallet = BTCWallet(self.btc_network)\
                    .from_passphrase(passphrase=passphrase)
            else:
                print("No data found, passphrase is none.")
        elif args[2] in ["--private", "--prv", "private", "prv"]:
            private_key = args[3].split('"')[2] \
                if len(args[3].split('"')) == 3 else args[3]
            if private_key:
                self.btc_wallet = BTCWallet(self.btc_network) \
                    .from_private_key(private_key=private_key)
            else:
                print("No data found, private is none.")
        else:
            print("Set wallet error, only from passphrase or private key.")
            return

    def do_bitcoin(self, bitcoin: str):
        args = bitcoin.split(" ")
        if args[0] == "set":
            if len(args) not in [3, 4]:
                print("set needs 3 or 4 more agreement's")
                return
            if args[1] == "network":
                self.set_network(args)
            elif args[1] == "wallet":
                self.set_wallet(args)
        elif args[0] == "create":
            pass
        elif args[0] == "wallet":
            pass
        elif args[0] == "fund":
            pass
        elif args[0] == "claim":
            pass
        elif args[0] == "refund":
            pass

    def help_bitcoin(self):
        pass

    @staticmethod
    def do_exit(_):
        print("Quit shuttle done.")
        return True

    @staticmethod
    def help_exit():
        print('Exit the shuttle application.')

    @staticmethod
    def do_add(inp=None):
        print("adding '{}'".format(inp))
        prompt = "Meheret"

    @staticmethod
    def help_add():
        print("Add a new entry to the system.")

    @staticmethod
    def do_clear(self):
        call("clear")

    @staticmethod
    def help_clear():
        print("To clear shell.")

    def default(self, inp):
        if inp in ["exit", "quit"]:
            return self.do_exit(inp)

        print("Default: {}".format(inp))

    do_EOF = do_exit
    help_EOF = help_exit
