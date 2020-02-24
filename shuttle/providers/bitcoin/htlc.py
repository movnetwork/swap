#!/usr/bin/env python3

from btcpy.structs.script import Script, ScriptBuilder, P2shScript, \
    IfElseScript, Hashlock256Script, RelativeTimelockScript
from btcpy.structs.transaction import Sequence

from .utils import script_from_address, is_address
from ...utils.exceptions import AddressError
from ...utils import sha256
from ..config import bitcoin

# Bitcoin config
bitcoin = bitcoin()


# Hash Time Lock Contract
class HTLC:
    """
    Bitcoin Hash Time Lock Contract (HTLC) class.

    :param network: bitcoin network, defaults to testnet.
    :type network: str
    :returns:  HTLC -- bitcoin HTLC instance.

    .. note::
        Bitcoin has only two networks, ``mainnet`` and ``testnet``.
    """

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
    def init(self, secret_hash, recipient_address, sender_address, sequence=bitcoin["sequence"]):
        """
        Initialize bitcoin Hash Time Lock Contract (HTLC).

        :param secret_hash: secret sha-256 hash.
        :type secret_hash: hash
        :param recipient_address: bitcoin recipient address.
        :type recipient_address: str
        :param sender_address: bitcoin sender address.
        :type sender_address: str
        :param sequence: bitcoin sequence number of expiration block, defaults to bitcoin config sequence (15).
        :type sequence: int
        :returns: HTLC -- bitcoin Hash Time Lock Contract (HTLC) instance.

        >>> from shuttle.providers.bitcoin.htlc import HTLC
        >>> htlc = HTLC(network="testnet")
        >>> htlc.init(secret_hash, recipient_address, sender_address, 100)
        <shuttle.providers.bitcoin.htlc.HTLC object at 0x0409DAF0>
        """

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
        """
        Initiate bitcoin Hash Time Lock Contract (HTLC) from opcode script.

        :param opcode: Bitcoin opcode script.
        :type opcode: str.
        :returns: HTLC -- bitcoin Hash Time Lock Contract (HTLC) instance.

        >>> from shuttle.providers.bitcoin.htlc import HTLC
        >>> htlc = HTLC(network="testnet")
        >>> htlc.from_opcode(htlc_opcode_script)
        <shuttle.providers.bitcoin.htlc.HTLC object at 0x0409DAF0>
        """

        if isinstance(opcode, str):
            bytecode = Script.compile(opcode)
            self.script = ScriptBuilder.identify(bytecode)
            return self
        raise TypeError("op_code must be string format")

    # Hash time lock contract form bytecode
    def from_bytecode(self, bytecode):
        """
        Initiate bitcoin Hash Time Lock Contract (HTLC) from bytecode.

        :param bytecode: Bitcoin bytecode.
        :type bytecode: str.
        :returns: HTLC -- bitcoin Hash Time Lock Contract (HTLC) instance.

        >>> from shuttle.providers.bitcoin.htlc import HTLC
        >>> htlc = HTLC(network="testnet")
        >>> htlc.from_bytecode(htlc_bytecode)
        <shuttle.providers.bitcoin.htlc.HTLC object at 0x0409DAF0>
        """

        if isinstance(bytecode, str):
            self.script = ScriptBuilder.identify(bytecode)
            return self
        raise TypeError("bytecode must be string format")

    # Bytecode HTLC script
    def bytecode(self):
        """
        Get bitcoin htlc bytecode.

        :returns: str -- bitcoin Hash Time Lock Contract (HTLC) bytecode.

        >>> from shuttle.providers.bitcoin.htlc import HTLC
        >>> htlc = HTLC(network="testnet")
        >>> htlc.init(secret_hash, recipient_address, sender_address, 100)
        >>> htlc.bytecode()
        "63aa20b9b9a0c47ecee7fd94812573a7b14afa02ec250dbdb5875a55c4d02367fcc2ab8876a9147b7c4431a43b612a72f8229935c469f1f690365888ac6755b27576a9146bce65e58a50b97989930e9a4ff1ac1a77515ef188ac68"
        """

        if self.script is None:
            raise ValueError("htlc script is none, initialization htlc first")
        return self.script.hexlify()

    # Decompiled HTLC script
    def opcode(self):
        """
        Get bitcoin htlc opcode.

        :returns: str -- bitcoin Hash Time Lock Contract (HTLC) opcode.

        >>> from shuttle.providers.bitcoin.htlc import HTLC
        >>> htlc = HTLC(network="testnet")
        >>> htlc.init(secret_hash, recipient_address, sender_address, 100)
        >>> htlc.opcode()
        "OP_IF OP_HASH256 b9b9a0c47ecee7fd94812573a7b14afa02ec250dbdb5875a55c4d02367fcc2ab OP_EQUALVERIFY OP_DUP OP_HASH160 7b7c4431a43b612a72f8229935c469f1f6903658 OP_EQUALVERIFY OP_CHECKSIG OP_ELSE OP_5 OP_CHECKSEQUENCEVERIFY OP_DROP OP_DUP OP_HASH160 6bce65e58a50b97989930e9a4ff1ac1a77515ef1 OP_EQUALVERIFY OP_CHECKSIG OP_ENDIF"
        """

        if self.script is None:
            raise ValueError("htlc script is none, initialization htlc first")
        return self.script.decompile()

    # HTLC script hash
    def hash(self):
        """
        Get bitcoin Hash Time Lock Contract (HTLC) hash.

        :returns: str -- bitcoin Hash Time Lock Contract (HTLC) hash.

        >>> from shuttle.providers.bitcoin.htlc import HTLC
        >>> htlc = HTLC(network="testnet")
        >>> htlc.init(secret_hash, recipient_address, sender_address, 100)
        >>> htlc.hash()
        "a914971894c58d85981c16c2059d422bcde0b156d04487"
        """

        if self.script is None:
            raise ValueError("htlc script is none, initialization htlc first")
        return P2shScript(self.script.p2sh_hash()).hexlify()

    # HTLC script address
    def address(self):
        """
        Get bitcoin Hash Time Lock Contract (HTLC) address.

        :returns: str -- bitcoin Hash Time Lock Contract (HTLC) address.

        >>> from shuttle.providers.bitcoin.htlc import HTLC
        >>> htlc = HTLC(network="testnet")
        >>> htlc.init(secret_hash, recipient_address, sender_address, 100)
        >>> htlc.address()
        "2N729UBGZB3xjsGFRgKivy4bSjkaJGMVSpB"
        """

        if self.script is None:
            raise ValueError("htlc script is none, initialization htlc first")
        return P2shScript(self.script.p2sh_hash()).address(mainnet=self.mainnet)
