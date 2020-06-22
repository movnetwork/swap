#!/usr/bin/env python3

from shuttle.providers.bytom.wallet import Wallet
from shuttle.cli.__main__ import main as cli_main
from shuttle.utils import sha256


network = "mainnet"
sender_wallet = Wallet(network=network).from_mnemonic(
    mnemonic="hint excuse upgrade sleep easily deputy erase cluster section other ugly limit"
).from_guid(
    guid="571784a8-0945-4d78-b973-aac4b09d6439"
)
recipient_wallet = Wallet(network=network).from_mnemonic(
    mnemonic="indicate warm sock mistake code spot acid ribbon sing over taxi toast"
).from_guid(
    guid="f0ed6ddd-9d6b-49fd-8866-a52d1083a13b"
)
secret_hash = sha256("Hello Meheret!".encode()).hex()
sequence = 1000


def test_bytom_cli_htlc(cli_tester):

    htlc = cli_tester.invoke(
        cli_main, [
            "bytom",
            "htlc",
            "--secret-hash", secret_hash,
            "--recipient-public", recipient_wallet.public_key(),
            "--sender-public", sender_wallet.public_key(),
            "--sequence", sequence,
            "--network", network
        ]
    )
    assert htlc.exit_code == 0
    assert htlc.output == "02e803203e0a377ae4afa031d4551599d9bb7d5b27f4736d77f78cac4d476f0ffba5ae3e2091ff7f525" \
                          "ff40874c4f47f0cab42e46e3bf53adad59adef9558ad1b6448f22e2203a26da82ead15a80533a026966" \
                          "56b14b5dbfd84eb14790f2e1be5e9e45820eeb741f547a6416000000557aa888537a7cae7cac631f000" \
                          "000537acd9f6972ae7cac00c0" + "\n"

    htlc = cli_tester.invoke(
        cli_main, [
            "bytom",
            "htlc",
            "--secret-hash", secret_hash,
            "--recipient-public", "L5tUq6mCbE84XobZ1mphBPZf15cRFcvg7Q",
            "--sender-public", sender_wallet.public_key(),
            "--sequence", sequence,
            "--network", network
        ]
    )
    assert htlc.exit_code == 0
    assert htlc.output == "Error: invalid recipient public key, length must be 64" + "\n"
