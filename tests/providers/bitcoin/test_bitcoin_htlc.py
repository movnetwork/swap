#!/usr/bin/env python3

from shuttle.providers.bitcoin.htlc import HTLC
from shuttle.utils import sha256


# Testing HTLC init
def test_htlc_init():
    htlc = HTLC(network="testnet")

    htlc.init(secret_hash=sha256("BooOoom!".encode()), recipient_address="mrmtGq2HMmqAogSsGDjCtXUpxrb7rHThFH",
              sender_address="mqLyrNDjpENRMZAoDpspH7kR9RtgvhWzYE", sequence=5)

    htlc_bytecode = htlc.bytecode()
    assert htlc_bytecode == "63aa20b9b9a0c47ecee7fd94812573a7b14afa02ec250dbdb5875a55c4d02367" \
                            "fcc2ab8876a9147b7c4431a43b612a72f8229935c469f1f690365888ac6755b2" \
                            "7576a9146bce65e58a50b97989930e9a4ff1ac1a77515ef188ac68"

    htlc_opcode = htlc.opcode()
    assert htlc_opcode == "OP_IF OP_HASH256 b9b9a0c47ecee7fd94812573a7b14afa02ec250dbdb5875a5" \
                          "5c4d02367fcc2ab OP_EQUALVERIFY OP_DUP OP_HASH160 7b7c4431a43b612a7" \
                          "2f8229935c469f1f6903658 OP_EQUALVERIFY OP_CHECKSIG OP_ELSE OP_5 OP" \
                          "_CHECKSEQUENCEVERIFY OP_DROP OP_DUP OP_HASH160 6bce65e58a50b979899" \
                          "30e9a4ff1ac1a77515ef1 OP_EQUALVERIFY OP_CHECKSIG OP_ENDIF"

    htlc_address = htlc.address()
    assert str(htlc_address) == "2N729UBGZB3xjsGFRgKivy4bSjkaJGMVSpB"

    htlc_hash = htlc.hash()
    assert str(htlc_hash) == "a914971894c58d85981c16c2059d422bcde0b156d04487"


# Testing HTLC from bytecode
def test_htlc_from_bytecode():
    htlc = HTLC(network="testnet")

    htlc.from_bytecode(bytecode="63aa20b9b9a0c47ecee7fd94812573a7b14afa02ec250dbdb5875a55c4d02367fcc2ab8876a914"
                                "7b7c4431a43b612a72f8229935c469f1f690365888ac6755b27576a9146bce65e58a50b9798993"
                                "0e9a4ff1ac1a77515ef188ac68")

    htlc_bytecode = htlc.bytecode()
    assert htlc_bytecode == "63aa20b9b9a0c47ecee7fd94812573a7b14afa02ec250dbdb5875a55c4d02367" \
                            "fcc2ab8876a9147b7c4431a43b612a72f8229935c469f1f690365888ac6755b2" \
                            "7576a9146bce65e58a50b97989930e9a4ff1ac1a77515ef188ac68"

    htlc_opcode = htlc.opcode()
    assert htlc_opcode == "OP_IF OP_HASH256 b9b9a0c47ecee7fd94812573a7b14afa02ec250dbdb5875a5" \
                          "5c4d02367fcc2ab OP_EQUALVERIFY OP_DUP OP_HASH160 7b7c4431a43b612a7" \
                          "2f8229935c469f1f6903658 OP_EQUALVERIFY OP_CHECKSIG OP_ELSE OP_5 OP" \
                          "_CHECKSEQUENCEVERIFY OP_DROP OP_DUP OP_HASH160 6bce65e58a50b979899" \
                          "30e9a4ff1ac1a77515ef1 OP_EQUALVERIFY OP_CHECKSIG OP_ENDIF"

    htlc_address = htlc.address()
    assert str(htlc_address) == "2N729UBGZB3xjsGFRgKivy4bSjkaJGMVSpB"

    htlc_hash = htlc.hash()
    assert str(htlc_hash) == "a914971894c58d85981c16c2059d422bcde0b156d04487"


# Testing HTLC from opcode
def test_htlc_from_opcode():
    htlc = HTLC(network="testnet")

    htlc.from_opcode(opcode="OP_IF OP_HASH256 b9b9a0c47ecee7fd94812573a7b14afa02ec250dbdb5875a5" \
                            "5c4d02367fcc2ab OP_EQUALVERIFY OP_DUP OP_HASH160 7b7c4431a43b612a7" \
                            "2f8229935c469f1f6903658 OP_EQUALVERIFY OP_CHECKSIG OP_ELSE OP_5 OP" \
                            "_CHECKSEQUENCEVERIFY OP_DROP OP_DUP OP_HASH160 6bce65e58a50b979899" \
                            "30e9a4ff1ac1a77515ef1 OP_EQUALVERIFY OP_CHECKSIG OP_ENDIF")

    htlc_bytecode = htlc.bytecode()
    assert htlc_bytecode == "63aa20b9b9a0c47ecee7fd94812573a7b14afa02ec250dbdb5875a55c4d02367" \
                            "fcc2ab8876a9147b7c4431a43b612a72f8229935c469f1f690365888ac6755b2" \
                            "7576a9146bce65e58a50b97989930e9a4ff1ac1a77515ef188ac68"

    htlc_opcode = htlc.opcode()
    assert htlc_opcode == "OP_IF OP_HASH256 b9b9a0c47ecee7fd94812573a7b14afa02ec250dbdb5875a5" \
                          "5c4d02367fcc2ab OP_EQUALVERIFY OP_DUP OP_HASH160 7b7c4431a43b612a7" \
                          "2f8229935c469f1f6903658 OP_EQUALVERIFY OP_CHECKSIG OP_ELSE OP_5 OP" \
                          "_CHECKSEQUENCEVERIFY OP_DROP OP_DUP OP_HASH160 6bce65e58a50b979899" \
                          "30e9a4ff1ac1a77515ef1 OP_EQUALVERIFY OP_CHECKSIG OP_ENDIF"

    htlc_address = htlc.address()
    assert str(htlc_address) == "2N729UBGZB3xjsGFRgKivy4bSjkaJGMVSpB"

    htlc_hash = htlc.hash()
    assert str(htlc_hash) == "a914971894c58d85981c16c2059d422bcde0b156d04487"
