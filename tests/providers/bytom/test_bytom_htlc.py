#!/usr/bin/env python3

from equity.exceptions import ConnectionError

import pytest

from shuttle.providers.bytom.htlc import HTLC
from shuttle.utils import sha256


# Testing HTLC
def test_bytom_htlc():

    htlc = HTLC(network="mainnet").init(
        secret_hash=sha256("Hello Meheret!".encode()).hex(),
        recipient_public="91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2",
        sender_public="3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e",
        sequence=1000,
        use_script=False
    )

    assert htlc.bytecode() == "02e803203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e2091ff" \
                              "7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2203a26da82ead15a80" \
                              "533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a" \
                              "7cae7cac631f000000537acd9f6972ae7cac00c0"
    assert htlc.opcode() == "0xe803 0x3e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e 0x91ff" \
                            "7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2 0x3a26da82ead15a805" \
                            "33a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb DEPTH 0x547a6416000000557aa88853" \
                            "7a7cae7cac631f000000537acd9f6972ae7cac FALSE CHECKPREDICATE"
    assert htlc.hash() == "a5addb7eb5649d10031304ece72d9ccc9dc424abcda895d904a309727424e40e"
    assert htlc.address() == "bm1q5kkakl44vjw3qqcnqnkwwtvuejwugf9tek5ftkgy5vyhyapyus8qgcttcs"

    assert HTLC().from_bytecode(bytecode=htlc.bytecode())


def test_bytom_htlc_exception():

    with pytest.raises(ConnectionError, match=r".*http://localhost:9888*."):
        HTLC(network="mainnet").init(
            secret_hash=sha256("Hello Meheret!".encode()).hex(),
            recipient_public="ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01",
            sender_public="91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2",
            sequence=100,
            use_script=True
        )

    with pytest.raises(TypeError, match="secret hash must be string format"):
        HTLC(network="mainnet").init(int(), str(), str(), int())

    with pytest.raises(ValueError, match="invalid secret hash, length must be 64"):
        HTLC(network="mainnet").init(str(), str(), str(), int())

    with pytest.raises(ValueError, match="htlc script is none, initialization htlc first"):
        HTLC(network="mainnet").bytecode()

    with pytest.raises(ValueError, match="htlc script is none, initialization htlc first"):
        HTLC(network="mainnet").opcode()

    with pytest.raises(ValueError, match="htlc script is none, initialization htlc first"):
        HTLC(network="mainnet").hash()

    with pytest.raises(ValueError, match="htlc script is none, initialization htlc first"):
        HTLC(network="mainnet").address()

    with pytest.raises(TypeError, match="recipient public key must be string format"):
        HTLC(network="mainnet").init("3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb",
                                     float(), str(), int())

    with pytest.raises(ValueError, match="invalid recipient public key, length must be 64"):
        HTLC(network="mainnet").init("3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb",
                                     str(), str(), int())

    with pytest.raises(TypeError, match="sender public key must be string format"):
        HTLC(network="mainnet").init("3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb",
                                     "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2",
                                     bool(), int())

    with pytest.raises(ValueError, match="invalid sender public key, length must be 64"):
        HTLC(network="mainnet").init("3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb",
                                     "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2",
                                     str(), int())

    with pytest.raises(TypeError, match="sequence must be integer format"):
        HTLC(network="mainnet").init("3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb",
                                     "91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2",
                                     "ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01",
                                     str())
