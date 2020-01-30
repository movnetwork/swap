#!/usr/bin/env python3

from btcpy.structs.script import Script, ScriptBuilder, P2shScript, \
    IfElseScript, Hashlock256Script, RelativeTimelockScript
from btcpy.structs.transaction import Sequence

from .utils import script_from_address, is_address
from ...utils.exceptions import AddressError
from ...utils import sha256


# Hash Time Lock Contract
class HTLC:

    # Initialization
    def __init__(self, network="testnet"):
        # Bitcoin network
        self.mainnet = None
        self.network = network
        if self.network == "mainnet":
            self.mainnet = True
        elif self.network == "testnet":
            self.mainnet = False
        else:
            raise ValueError("invalid network, only mainnet or testnet")
        # HTLC script
        self.script = None

    # Initialize new HTLC Contract script
    def init(self, secret_hash, recipient_address, sender_address, sequence):
        # Checking parameters
        if not isinstance(secret_hash, bytes):
            raise TypeError("secret hash must be bytes format")
        if not is_address(recipient_address, self.network):
            raise AddressError("invalid %s recipient %s address" % (self.network, recipient_address))
        if not is_address(sender_address, self.network):
            raise AddressError("invalid %s sender %s address" % (self.network, sender_address))
        if not isinstance(sequence, int):
            raise TypeError("sequence must be integer format")
        # HASH TIME LOCK CONTRACT SCRIPT
        self.script = IfElseScript(
            # If branch
            Hashlock256Script(  # Hash lock 250
                sha256(secret_hash),  # Secret key
                script_from_address(
                    address=recipient_address, network=self.network)  # Script hash of account two
            ),
            # Else branch
            RelativeTimelockScript(  # Relative time locked script
                Sequence(sequence),  # Expiration blocks
                script_from_address(
                    address=sender_address, network=self.network)  # Script hash of account one
            )
        )
        return self

    # Hash time lock contract form opcode script
    def from_opcode(self, opcode):
        if isinstance(opcode, str):
            bytecode = Script.compile(opcode)
            self.script = ScriptBuilder.identify(bytecode)
            return self
        raise TypeError("op_code must be string format")

    # Hash time lock contract form bytecode
    def from_bytecode(self, bytecode):
        if isinstance(bytecode, str):
            self.script = ScriptBuilder.identify(bytecode)
            return self
        raise TypeError("bytecode must be string format")

    # Bytecode HTLC script
    def bytecode(self):
        if self.script is None:
            raise ValueError("htlc script is none, initialization htlc first")
        return self.script.hexlify()

    # Decompiled HTLC script
    def opcode(self):
        if self.script is None:
            raise ValueError("htlc script is none, initialization htlc first")
        return self.script.decompile()

    # HTLC script hash
    def hash(self):
        if self.script is None:
            raise ValueError("htlc script is none, initialization htlc first")
        return P2shScript(self.script.p2sh_hash()).hexlify()

    # HTLC script address
    def address(self):
        if self.script is None:
            raise ValueError("htlc script is none, initialization htlc first")
        return P2shScript(self.script.p2sh_hash()).address(mainnet=self.mainnet)
