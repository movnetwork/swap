#!/usr/bin/env python3

from btcpy.structs.script import Script, ScriptBuilder, P2shScript, \
    IfElseScript, Hashlock256Script, RelativeTimelockScript
from btcpy.structs.transaction import Sequence

from .utils import double_sha256, script_from_address


# Hash Time Lock Contract
class HTLC:

    # Initialization
    def __init__(self, network="testnet"):
        # Bitcoin network.
        self.network = network
        # Bitcoin network boolean..
        self.testnet = True if network == "testnet" else False
        # HTLC script
        self.script = None

    # Initialize new HTLC Contract script
    def init(self, secret_hash, recipient_address, sender_address, sequence):
        # HASH TIME LOCK CONTRACT SCRIPT
        self.script = IfElseScript(
            # If branch
            Hashlock256Script(  # Hash lock 250
                double_sha256(secret_hash),  # Secret key
                script_from_address(recipient_address)  # Script hash of account two
            ),
            # Else branch
            RelativeTimelockScript(  # Relative time locked script
                Sequence(sequence),  # Expiration blocks
                script_from_address(sender_address)  # Script hash of account one
            )
        )
        return self

    # Hash time lock contract form opcode script
    def from_opcode(self, opcode):
        if isinstance(opcode, str):
            bytecode = Script.compile(opcode)
            self.script = ScriptBuilder.identify(bytecode)
            return self
        raise TypeError("OP_Code must be string format!")

    # Hash time lock contract form bytecode
    def from_bytecode(self, bytecode):
        if isinstance(bytecode, str):
            self.script = ScriptBuilder.identify(bytecode)
            return self
        raise TypeError("Bytecode must be string format!")

    # Bytecode HTLC script
    def bytecode(self):
        if self.script is None:
            raise ValueError("HTLC script is none, Please initialization htlc first.")
        return self.script.hexlify()

    # Decompiled HTLC script
    def opcode(self):
        if self.script is None:
            raise ValueError("HTLC script is none, Please initialization htlc first.")
        return self.script.decompile()

    # HTLC script hash
    def hash(self):
        if self.script is None:
            raise ValueError("HTLC script is none, Please initialization htlc first.")
        script_builder = ScriptBuilder.identify(str(self.script.decompile()).encode())
        return P2shScript(script_builder.p2sh_hash()).hexlify()

    # HTLC script address
    def address(self):
        if self.script is None:
            raise ValueError("HTLC script is none, Please initialization htlc first.")
        script_builder = ScriptBuilder.identify(str(self.script.decompile()).encode())
        return P2shScript(script_builder.p2sh_hash()).address(mainnet=(not self.testnet))
