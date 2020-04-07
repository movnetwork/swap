#!/usr/bin/env python3

from equity.exceptions import ConnectionError

import pytest

from shuttle.providers.bytom.htlc import HTLC
from shuttle.utils import sha256


# Testing HTLC
def test_bytom_htlc():

    with pytest.raises(ConnectionError, match=r".*http://localhost:9888*."):

        htlc = HTLC(network="mainnet").init(
            secret_hash=sha256("Hello Meheret!".encode()).hex(),
            recipient_public="ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3d7ea01",
            sender_public="91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2",
            sequence=100
        )

        htlc_bytecode = htlc.bytecode()
        assert htlc_bytecode == "01642091ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b644" \
                                "8f22e220ac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122" \
                                "c3d7ea01203a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e" \
                                "9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000000537acd" \
                                "9f6972ae7cac00c0"

        htlc_opcode = htlc.opcode()
        assert htlc_opcode == "0x64 0x91ff7f525ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448" \
                              "f22e2 0xac13c0bb1445423a641754182d53f0677cd4351a0e743e6f10b35122c3" \
                              "d7ea01 0x3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e4" \
                              "5820eeb DEPTH 0x547a6416000000557aa888537a7cae7cac631f000000537acd" \
                              "9f6972ae7cac FALSE CHECKPREDICATE"
